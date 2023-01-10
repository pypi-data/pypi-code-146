class InsightClientError(Exception):
    """Base exception for inSight client."""


class ExpiredSession(InsightClientError):
    """Raised when the session cookie is expired and we can no longer authenticate
    with the server.
    """

    def __str__(self) -> str:
        return "Signed out. Please refresh session config"