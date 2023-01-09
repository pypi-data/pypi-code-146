import cryt


class BaseClient:
    def __init__(self, base_url=None, public_key=None, private_key=None):
        self.base_url = base_url
        self.public_key = public_key
        self.public_key = private_key
        self.session = None

    def _init_session(self):
        raise NotImplementedError

    def _create_api_uri(self, path):
        return f"{self.base_url}/{path}"

    def _get_headers(self):
        headers = {
            "Accept": "application/json",
            "User-Agent": f"Python CRYT API Client/{cryt.__version__}",
        }
        return headers
