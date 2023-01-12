class BackendServiceException(Exception):
    """Base class for all exceptions from downstream services."""

    def __init__(self, status_code: int, error_code: str, error_message: str) -> None:
        self.status_code = status_code
        self.error_code = error_code
        self.error_message = error_message
        super().__init__(error_message)

    def is_client_side(self) -> bool:
        return self.status_code >= 400 and self.status_code < 500
