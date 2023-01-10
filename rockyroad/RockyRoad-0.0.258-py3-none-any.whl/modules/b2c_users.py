from .module_imports import *


@headers({"Ocp-Apim-Subscription-Key": key})
class B2C_Users(Consumer):
    """Inteface to B2C users resource for the RockyRoad API."""

    def __init__(self, Resource, *args, **kw):
        self._base_url = Resource._base_url
        super().__init__(base_url=Resource._base_url, *args, **kw)

    @returns.json
    @http_get("b2c-users")
    def list(
        self,
        user_role: Query(type=str) = None,
        company_uid: Query(type=str) = None,
    ):
        """This call will return B2C user information for the specified criteria."""

    @returns.json
    @http_get("b2c-users/{uid}")
    def get(
        self,
        uid: str,
    ):
        """This call will return the B2C user for the specified uid."""
