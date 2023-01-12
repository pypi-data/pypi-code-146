"""BEMServer API client resources

/users/ endpoints
/user_groups/ endpoints
/users_by_user_groups/ endpoints
"""
from .base import BaseResources


class UserResources(BaseResources):
    endpoint_base_uri = "/users/"

    def set_admin(self, id, state, *, etag=None):
        endpoint = f"{self.enpoint_uri_by_id(id)}/set_admin"
        return self._req.update(endpoint, {"value": state}, etag=etag)

    def set_active(self, id, state, *, etag=None):
        endpoint = f"{self.enpoint_uri_by_id(id)}/set_active"
        return self._req.update(endpoint, {"value": state}, etag=etag)


class UserGroupResources(BaseResources):
    endpoint_base_uri = "/user_groups/"


class UserByUserGroupResources(BaseResources):
    endpoint_base_uri = "/users_by_user_groups/"
    disabled_endpoints = ["update"]
