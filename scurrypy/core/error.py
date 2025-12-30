class DiscordError(Exception):
    """Represents a Discord API error."""

    def __init__(self, status: int, data: dict):
        """Initialize the error with Discord's response.
            Extracts reason, code, and walks the nested errors.

        Args:
            data (dict): Discord's error JSON
        """
        self.data = data
        self.status = status
        self.reason = data.get('message', data)
        self.code = data.get('code', 'Unknown Code')

        self.error_data = data.get('errors', {})
        self.details = self.walk(self.error_data)

        self.is_fatal = status in (401, 403)

        errors = [f"→ {path}: {reason}" for path, reason in self.details]
        full_message = f"{self.reason} ({self.code})"
        if errors:
            full_message += '\n' + '\n'.join(errors)

        super().__init__(full_message)

    def walk(self, node: dict, path=None):
        """Recursively traverses errors field to flatten nested validation errors into (path, message).

        Args:
            node (dict): current error level
            path (tuple[str, str], optional): path to this error level

        Returns:
            (list): list of errors
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
