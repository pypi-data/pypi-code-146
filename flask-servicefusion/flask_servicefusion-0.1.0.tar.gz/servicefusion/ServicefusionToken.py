from time import time


class ServicefusionToken:
    def __init__(self, **kwargs):
        self.access_token = kwargs.get("access_token", None)
        self.refresh_token = kwargs.get("refresh_token", None)
        self.expires_in = kwargs.get("expires_in", 0)
        self.expires_at = kwargs.get("expires_at")
        self.scope = kwargs.get("scope", None)

    @property
    def is_expired(self):
        return self.expires_at < int(time())

    @property
    def exists(self):
        return self.access_token is not None
