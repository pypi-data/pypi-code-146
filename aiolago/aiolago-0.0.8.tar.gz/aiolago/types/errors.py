
__all__ = [
    "APIError",
    "fatal_exception",   
    "LagoApiError",
    "ReportingApiError",
]

class APIError(Exception):
    def __init__(self, url: str, status, payload):
        self.url = url
        self.status = status
        self.payload = payload

    def __str__(self):
        return f"[Lago] url: {self.url}, status: {self.status}, payload: {self.payload}"


def fatal_exception(exc):
    if isinstance(exc, APIError):
        # retry on server errors and client errors
        # with 429 status code (rate limited),
        # don't retry on other client errors
        return (400 <= exc.status < 500) and exc.status != 429
    else:
        # retry on all other errors (eg. network)
        return False


class LagoApiError(Exception):
    ...

class ReportingApiError(Exception):
    ...
