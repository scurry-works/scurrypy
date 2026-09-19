import asyncio
import aiohttp
import aiofiles
import json

from dataclasses import dataclass

from ..config import USER_AGENT

from .error import DiscordError
from .exceptions import NoSession

from .types import HTTPResponse, JSON, Serialized

import logging

logger = logging.getLogger("scurrypy.http")
logger.addHandler(logging.NullHandler())

@dataclass
class RequestItem:
    method: str
    endpoint: str
    data: Serialized | list[Serialized]
    params: JSON | None
    files: list[str] | None
    assets: Serialized | None
    future: asyncio.Future[HTTPResponse]

@dataclass
class Bucket:
    remaining: int
    reset_after: float
    reset_on: float
    sleep_task: asyncio.Task[None] | None = None # if Task is set, it returns None (HTTPClient._sleep_endpoint)

from typing import Protocol, cast

class HTTPClientProtocol(Protocol):
    """Internal contract for the HTTPClient used by the Client. Meant for testing."""
    async def start(self, token: str) -> None: ...
    async def close(self) -> None: ...
    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        data: Serialized | list[Serialized] = None,
        params: JSON | None = None,
        files: list[str] | None = None,
        assets: Serialized = None
    ) -> HTTPResponse: ...

class HTTPClient(HTTPClientProtocol):
    BASE = "https://discord.com/api/v10"
    MAX_RETRIES = 3

    def __init__(self) -> None:
        self.session: aiohttp.ClientSession | None = None

        # PRE-REQUEST
        self.queues: dict[str, asyncio.Queue[RequestItem]] = {}  # maps EP -> Q
        self.queues_lock = asyncio.Lock() # locks queues dict for editing

        self.workers: dict[str, asyncio.Task[None]] = {}  # maps EP -> worker
        # if Task is set, it returns None (HTTPClient._worker)

        # POST-REQUEST
        self.buckets: dict[str, Bucket] = {}  # maps B -> Bucket
        self.bucket_lock: dict[str, asyncio.Lock] = {} # maps B to Lock
        self.buckets_lock = asyncio.Lock() # locks buckets dict for editing

        self.global_lock: asyncio.Lock = asyncio.Lock()
        self.global_reset: float = 0.0

    async def start(self, token: str) -> None:
        """Start the HTTP session."""

        if self.session is None:
            self.session = aiohttp.ClientSession(headers={
                "Authorization": f"Bot {token}",
                "User-Agent": USER_AGENT
            })
            logger.info("HTTP session started.")
        else:
            logger.warning("HTTP session already initialized.")

    async def close(self) -> None:
        """Gracefully stop all workers and close the HTTP session."""

        if self.session: # just the session that needs to close!
            await self.session.close()
            logger.info("Session closed.")

    async def request(
        self,
        method: str,
        endpoint: str,
        *,
        data: Serialized | list[Serialized] = None,
        params: JSON | None = None,
        files: list[str] | None = None,
        assets: Serialized = None
    ) -> HTTPResponse:
        """Queue a request for the given endpoint.

        Args:
            method (str): HTTP method (e.g., POST, GET, DELETE, PATCH, etc.)
            endpoint (str): Discord endpoint (e.g., /channels/123/messages)
            data (Serialized | list[Serialized], optional): relevant data
            params (JSON | None, optional): relevant query params
            files (list[str] | None, optional): relevant files
            assets (Serialized, optional): relevant assets

        Raises:
            (DiscordError): something went wrong

        Returns:
            (HTTPResponse): result or promise of request or None if failed
        """
        # ensure a queue is in place for the requested endpoint
        async with self.queues_lock:
            queue = self.queues.setdefault(endpoint, asyncio.Queue())

        if endpoint not in self.workers:
            self.workers[endpoint] = asyncio.create_task(self._worker(endpoint))

        # set promise
        future: asyncio.Future[HTTPResponse] = asyncio.get_event_loop().create_future()

        def sanitize_query_params(params: JSON | None) -> JSON | None:
            """Sanitize a request's params for session.request

            Args:
                params (JSON | None): query params (if any)

            Returns:
                (JSON | None): the session.request-friendly version of params
            """
            if not params:
                return None
            return {k: ('true' if v is True else 'false' if v is False else v)
                for k, v in params.items() if v is not None}

        await queue.put(RequestItem(method, endpoint, data, sanitize_query_params(params), files, assets, future))

        # return promise
        try:
            return await future
        except DiscordError:
            raise # surface the error

    async def _worker(self, endpoint: str) -> None:
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

    async def _sleep_endpoint(self, endpoint: str, bucket: Bucket) -> None:
        """Let an endpoint sleep for the designated reset_after seconds.

        Args:
            endpoint (str): endpoint to sleep
            bucket (Bucket): endpoint's bucket info
        """
        logger.warning(f"Bucket {endpoint} rate limit is active. Sleeping for {bucket.reset_after}s...")
        await asyncio.sleep(bucket.reset_after)
        bucket.sleep_task = None
        logger.info(f"Bucket {endpoint} reset after {bucket.reset_after}s.")

    async def _check_global_rate_limit(self) -> None:
        """Checks if the global rate limit is after now (active)."""
        now = asyncio.get_event_loop().time()
        if self.global_reset > now:
            async with self.global_lock:
                logger.warning(f"Global reset is active. Sleeping for {self.global_reset - now}s...")
                await asyncio.sleep(self.global_reset - now)
                logger.info(f"Global has reset after {self.global_reset - now}s.")

    async def _parse_response(self, resp: aiohttp.ClientResponse) -> HTTPResponse | None:
        """Parse the request's response for response details.

        Args:
            resp (aiohttp.ClientResponse): the response object

        Raises:
            (DiscordError): Error object for pretty printing if an error is returned.

        Returns:
            (JSON | None): request info (if any)
        """

        if resp.status == 204:
            return None

        if 200 <= resp.status < 300:
            # JSON body is guaranteed if successful
            try:
                data: HTTPResponse = await resp.json()
                return data
            except aiohttp.ContentTypeError:
                data = await resp.text()
                return data

        # error handling
        try:
            body: HTTPResponse = await resp.json()
        except aiohttp.ContentTypeError:
            body = await resp.text()
        raise DiscordError(resp.status, body)
            
    async def _update_bucket_rate_limit(self, resp: aiohttp.ClientResponse, bucket_id: str, endpoint: str) -> None:
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

            logger.debug(f"[{endpoint}] {resp.method} bucket={bucket_id} reset_on={bucket.reset_on} remaining={bucket.remaining} reset_after={bucket.reset_after:.2f}s")

            if bucket.remaining == 1 and not bucket.sleep_task:
                bucket.sleep_task = asyncio.create_task(
                    self._sleep_endpoint(endpoint, bucket)
                )

            elif bucket.sleep_task and not bucket.sleep_task.done():
                await bucket.sleep_task

    async def _prepare_payload(self, item: RequestItem) -> JSON:
        """Prepares the payload based on `RequestItem`.

        Args:
            item (RequestItem): the request object

        Returns:
            (dict): kwargs to pass to session.request
        """
        if item.files and any(item.files):
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
        
        if item.assets:
            form = aiohttp.FormData()

            if item.data is not None:
                iterable = item.data.items() if isinstance(item.data, dict) else item.data
                assert isinstance(iterable, dict)
                for k, v in iterable:
                    form.add_field(k, v)
            
            assert isinstance(item.assets, dict)
            form.add_field('file', **item.assets)

            return {"data": form}

        return {"json": item.data}

    async def _send(self, item: RequestItem) -> str | JSON | None:
        """Core HTTP request executor.

        Args:
            item (RequestItem): request object

        Returns:
            (str | dict | None): Parsed JSON response if available, raw text if the
                response is not JSON, or None for HTTP 204 responses.
        """
        if self.session is None:
            raise NoSession("Session not started")
        await self._check_global_rate_limit()

        kwargs = await self._prepare_payload(item)

        url = f"{self.BASE.rstrip('/')}/{item.endpoint.lstrip('/')}"
        
        async with self.session.request(
            method=item.method, url=url, params=item.params, **kwargs
        ) as resp:
            
            if resp.headers.get("X-RateLimit-Global") == "true":
                retry_after = float(resp.headers.get("Retry-After", 0))
                self.global_reset = asyncio.get_event_loop().time() + retry_after

            bucket_id = resp.headers.get('x-ratelimit-bucket')

            if bucket_id:
                await self._update_bucket_rate_limit(resp, bucket_id, item.endpoint)

            return await self._parse_response(resp)
