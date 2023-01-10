from .module_imports import *


@headers({"Ocp-Apim-Subscription-Key": key})
class Information(Consumer):
    """Inteface to Information resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    def sites(self):
        return self.__Sites(self)

    def brands(self):
        return self.__Brands(self)

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Sites(Consumer):
        """Inteface to Sites resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @http_get("information/sites")
        def list(
            self,
        ):
            """This call will return a list of sites."""

    @headers({"Ocp-Apim-Subscription-Key": key})
    class __Brands(Consumer):
        """Inteface to Brands resource for the RockyRoad API."""

        def __init__(self, Resource, *args, **kw):
            super().__init__(base_url=Resource._base_url, *args, **kw)

        @returns.json
        @http_get("information/brands")
        def list(
            self,
        ):
            """This call will return a list of brands."""
