import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

DEFAULT_RETRY_STRATEGY = Retry(
    total=4,
    backoff_factor=1.5,
    status_forcelist=[429, 500, 502, 503, 504],
)

DEFAULT_TIMEOUT = (10.0, 100.0)


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(
        self, timeout=DEFAULT_TIMEOUT, max_retries=DEFAULT_RETRY_STRATEGY, **kwargs
    ):
        self.timeout = timeout
        super().__init__(max_retries=max_retries, **kwargs)

    def send(self, request, **kwargs):
        if kwargs.get("timeout") is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


HTTP_SESSION_WITH_TIMEOUT_AND_RETRY = requests.Session()
_adapter = TimeoutHTTPAdapter()
HTTP_SESSION_WITH_TIMEOUT_AND_RETRY.mount("http://", _adapter)
HTTP_SESSION_WITH_TIMEOUT_AND_RETRY.mount("https://", _adapter)
