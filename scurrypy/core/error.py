from .types import HTTPResponse

class DiscordError(Exception):
    """Represents a Discord API error."""

    def __init__(self, status: int, data: HTTPResponse):
        """Initialize the error with Discord's response.
            Extracts reason, code, and walks the nested errors.

        Args:
            status (int): response status
            data (HTTPResponse): Discord's error response, either structured JSON
                or an unstructured response body.
        """
        self.data = data
        self.status = status

        errors = None
        if isinstance(data, dict):
            self.reason = data.get('message', data)
            self.code = data.get('code', 'Unknown Code')
            self.error_data: HTTPResponse = data.get('errors', {})
            self.details = self.walk(self.error_data)
            errors = [f"→ {path}: {reason}" for path, reason in self.details]
        else:
            self.reason = data
            self.code = "Unknown Code"

        self.full_message = f"{self.reason} ({self.code})"
        if errors:
            self.full_message += '\n' + '\n'.join(errors)

        super().__init__(self.full_message)

    def walk(self, node: HTTPResponse, path: list[str] | None = None) -> list[tuple[str, str]]:
        """Recursively traverses errors field to flatten nested validation errors into (path, message).

        Args:
            node (HTTPResponse): current error level
            path (list[str], optional): path to this error level

        Returns:
            (list[tuple[str, str]]): list of errors
        """
        if path is None:
            path = []
        result = []

        if isinstance(node, dict):
            for key, value in node.items():
                if key == '_errors' and isinstance(value, list):
                    msg = value[0].get('message', 'Unknown error')
                    result.append(('.'.join(path), msg))

                # the value should not be a dict -- keep going
                elif isinstance(value, dict):
                    result.extend(self.walk(value, path + [key]))
        return result
