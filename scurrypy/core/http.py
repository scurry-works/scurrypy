"""
R = request
EP = endpoint
L = Lock
Q = Queue
H = header
B = Bucket
A + B = {A:B}

[R + EP]--|L|-->[Q + EP]--|send R|-->[add/update H + B]
    1. request by endpoint
    2. push request to queue with lock
    3. add/update header by bucket ID with send request

    * Queue by ENDPOINT/REQUEST
    * Bucket by HEADER
"""

import asyncio
import aiohttp
import aiofiles
import json
from typing import Any

from dataclasses import dataclass

from .error import DiscordError

import logging

logger = logging.getLogger(__name__)

@dataclass
class RequestItem:
    method: str
    endpoint: str
    data: dict = None
    params: dict = None
    files: dict = None
    future: asyncio.Future = None

@dataclass
class Bucket:
    remaining: int
    reset_after: float
    reset_on: float
    sleep_task: asyncio.Task = None

class HTTPClient:
    BASE = "https://discord.com/api/v10"
    MAX_RETRIES = 3

    def __init__(self):
        self.session = None

        # PRE-REQUEST
        self.queues: dict[str, asyncio.Queue] = {}  # maps EP -> Q
        self.queues_lock = asyncio.Lock() # locks queues dict for editing

        self.workers: dict[str, asyncio.Task] = {}  # maps EP -> worker

        # POST-REQUEST
        self.buckets: dict[str, Bucket] = {}  # maps B -> Bucket
        self.bucket_lock: dict[str, asyncio.Lock] = {} # maps B to Lock
        self.buckets_lock = asyncio.Lock() # locks buckets dict for editing

        self.global_lock = asyncio.Lock()
        self.global_reset = 0.0

    async def start(self, token: str):
        """Start the HTTP session."""

        if not self.session:
            self.session = aiohttp.ClientSession(headers={"Authorization": f"Bot {token}"})
            logger.info("HTTP session started.")
        else:
            logger.warning("HTTP session already initialized.")

    async def close(self):
        """Gracefully stop all workers and close the HTTP session."""

        if self.session: # just the session that needs to close!
            await self.session.close()
            logger.info("Session closed.")

    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        data: dict | None = None,
        params: dict | None = None,
        files: Any | None = None,
    ):
        """Queue a request for the given endpoint.

        Args:
            method (str): HTTP method (e.g., POST, GET, DELETE, PATCH, etc.)
            endpoint (str): Discord endpoint (e.g., /channels/123/messages)
            data (dict | None, optional): relevant data
            params (dict | None, optional): relevant query params
            files (Any | None, optional): relevant files

        Returns:
            (Future | None): result or promise of request or None if failed
        """
        # ensure a queue is in place for the requested endpoint
        async with self.queues_lock:
            queue = self.queues.setdefault(endpoint, asyncio.Queue())

        if endpoint not in self.workers:
            self.workers[endpoint] = asyncio.create_task(self._worker(endpoint))

        # set promise
        future = asyncio.get_event_loop().create_future()

        def sanitize_query_params(params: dict | None) -> dict | None:
            """Sanitize a request's params for session.request

            Args:
                params (dict | None): query params (if any)

            Returns:
                (dict | None): the session.request-friendly version of params
            """
            if not params:
                return None
            return {k: ('true' if v is True else 'false' if v is False else v)
                for k, v in params.items() if v is not None}

        await queue.put(RequestItem(method, endpoint, data, sanitize_query_params(params), files, future))

        # return promise
        try:
            return await future
        except DiscordError as e:
            logger.error(e)
            return None

    async def _worker(self, endpoint: str):
        """Background worker that processes requests for this endpoint.

        Args:
            endpoint (str): the endpoint to receive requests
        """
        # fetch the queue by endpoint
        queue = self.queues[endpoint]

        while True:
            # get the next item in the queue
            item: RequestItem = await queue.get()

            if item is None: # sentinel = time to stop
                queue.task_done()
                break

            try:
                result = await self._send(item)
            except Exception as e:
                item.future.set_exception(e)
            else:
                item.future.set_result(result)
            finally:
                queue.task_done()

    async def _sleep_endpoint(self, endpoint: str, bucket: Bucket):
        """Let an endpoint sleep for the designated reset_after seconds.

        Args:
            endpoint (str): endpoint to sleep
            bucket (Bucket): endpoint's bucket info
        """
        logger.warning(f"Bucket {endpoint} rate limit is active. Sleeping for {bucket.reset_after}s...")
        await asyncio.sleep(bucket.reset_after)
        bucket.sleep_task = None
        logger.info(f"Bucket {endpoint} reset after {bucket.reset_after}s")

    async def _check_global_rate_limit(self):
        """Checks if the global rate limit is after now (active)."""
        now = asyncio.get_event_loop().time()
        if self.global_reset > now:
            async with self.global_lock:
                logger.warning(f"Global reset is active. Sleeping for {self.global_reset - now}s...")
                await asyncio.sleep(self.global_reset - now)
                logger.info(f"Global has reset after {self.global_reset - now}s...")

    async def _parse_response(self, resp: aiohttp.ClientResponse):
        """Parse the request's response for response details.

        Args:
            resp (aiohttp.ClientResponse): the response object

        Raises:
            DiscordError: Error object for pretty printing if an error is returned.

        Returns:
            (str | dict | None): request info (if any)
        """
        match resp.status:
            case 204:
                # No content
                return None

            case 200:
                # JSON body is guaranteed if successful
                try:
                    return await resp.json()
                except aiohttp.ContentTypeError:
                    return await resp.text()

            case _:
                # error handling
                try:
                    body = await resp.json()
                except aiohttp.ContentTypeError:
                    body = await resp.text()
                raise DiscordError(resp.status, body)
            
    async def _update_bucket_rate_limit(self, resp: aiohttp.ClientResponse, bucket_id: str, endpoint: str):
        """Update the bucket for this endpoint and sleep if necessary.

        Args:
            resp (aiohttp.ClientResponse): the response object
            bucket_id (str): bucket ID provided by Discord's headers
            endpoint (str): endpoint in which request was sent
        """
        # grab lock from dict of bucket locks with a lock on dict access
        async with self.buckets_lock:
            lock = self.bucket_lock.setdefault(bucket_id, asyncio.Lock())

        # update/add the bucket with Bucket lock
        async with lock:
            remaining = int(resp.headers.get('x-ratelimit-remaining', 1))
            reset_after = float(resp.headers.get('x-ratelimit-reset-after', 0))
            reset_on = float(resp.headers.get('x-ratelimit-reset', 0))

            bucket = self.buckets.get(bucket_id)

            if not bucket:
                bucket = Bucket(remaining, reset_after, reset_on)
                self.buckets[bucket_id] = bucket
            else:
                bucket.remaining = remaining
                bucket.reset_after = reset_after
                bucket.reset_on = reset_on

            if bucket.remaining == 0 and not bucket.sleep_task:
                bucket.sleep_task = asyncio.create_task(
                    self._sleep_endpoint(endpoint, bucket)
                )

            elif bucket.sleep_task and not bucket.sleep_task.done():
                await bucket.sleep_task

    async def _prepare_payload(self, item: RequestItem):
        """Prepares the payload based on `RequestItem`.

        Args:
            item (RequestItem): the request object

        Returns:
            (dict): kwargs to pass to session.request
        """
        if item.files and any(item.files):
            # payload = await self._make_payload(item.data, item.files)
            form = aiohttp.FormData()
            form.add_field("payload_json", json.dumps(item.data))

            for idx, file_path in enumerate(item.files):
                async with aiofiles.open(file_path, 'rb') as f:
                    f_data = await f.read()
                    form.add_field(
                        f'files[{idx}]',
                        f_data,
                        filename=file_path.split('/')[-1],
                        content_type='application/octet-stream'
                    )

            return {"data": form}

        return {"json": item.data}

    async def _send(self, item: RequestItem):
        """Core HTTP request executor.

        Args:
            item (RequestItem): request object

        Returns:
            (dict | str | None): Parsed JSON response if available, raw text if the
                response is not JSON, or None for HTTP 204 responses.
        """
        await self._check_global_rate_limit()

        kwargs = await self._prepare_payload(item)

        url = f"{self.BASE.rstrip('/')}/{item.endpoint.lstrip('/')}"
        
        async with self.session.request(
            method=item.method, url=url, params=item.params, timeout=15, **kwargs
        ) as resp:
            
            if resp.headers.get("X-RateLimit-Global") == "true":
                retry_after = float(resp.headers.get("Retry-After", 0))
                self.global_reset = asyncio.get_event_loop().time() + retry_after

            bucket_id = resp.headers.get('x-ratelimit-bucket')

            if bucket_id:
                await self._update_bucket_rate_limit(resp, bucket_id, item.endpoint)

            return await self._parse_response(resp)
