"""BEMServer API client resources base class"""


class BaseResources:
    endpoint_base_uri = ""
    disabled_endpoints = []

    def __init__(self, request_manager):
        self._req = request_manager

    def _verify_disabled(self, endpoint_name):
        if not hasattr(self, endpoint_name):
            raise ValueError(
                f"{self.__class__.__name__}.{endpoint_name} does not exist!"
            )
        if endpoint_name in self.disabled_endpoints:
            raise NotImplementedError(
                f"{self.__class__.__name__}.{endpoint_name} is disabled!"
            )

    def enpoint_uri_by_id(self, id):
        return f"{self.endpoint_base_uri}{str(id)}"

    def getall(self, *, etag=None, **kwargs):
        self._verify_disabled("getall")
        return self._req.getall(self.endpoint_base_uri, etag=etag, params=kwargs)

    def getone(self, id, *, etag=None):
        self._verify_disabled("getone")
        return self._req.getone(self.enpoint_uri_by_id(id), etag=etag)

    def create(self, payload):
        self._verify_disabled("create")
        return self._req.create(self.endpoint_base_uri, payload)

    def update(self, id, payload, *, etag=None):
        self._verify_disabled("update")
        return self._req.update(self.enpoint_uri_by_id(id), payload, etag=etag)

    def delete(self, id, *, etag=None):
        self._verify_disabled("delete")
        return self._req.delete(self.enpoint_uri_by_id(id), etag=etag)
