try:
    import requests
except ImportError:
    requests = None

from . import base
from tippisell_api import methods, models


class Client(base.BaseClient):
    def __init__(self, *args, **kwargs):
        if requests is None:
            raise ImportError("Required requests")

        super().__init__(*args, **kwargs)
