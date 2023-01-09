"""BEMServer API client resources

/event_categories/ endpoints
/event_categories_by_users/ endpoints
/events/ endpoints
/events/by_site endpoint
/events/by_building endpoint
/events/by_storey endpoint
/events/by_space endpoint
/events/by_zone endpoint
/events_by_sites/ endpoints
/events_by_buildings/ endpoints
/events_by_storeys/ endpoints
/events_by_spaces/ endpoints
/events_by_zones/ endpoints
"""
from .base import BaseResources


class EventCategoryResources(BaseResources):
    endpoint_base_uri = "/event_categories/"


class EventCategoryByUserResources(BaseResources):
    endpoint_base_uri = "/event_categories_by_users/"


class EventResources(BaseResources):
    endpoint_base_uri = "/events/"

    def endpoint_uri_getall_by(self, item_type, item_id):
        return f"{self.endpoint_base_uri}by_{item_type}/{str(item_id)}"

    def getall_by_site(self, site_id, *, etag=None, **kwargs):
        return self._req.getall(
            self.endpoint_uri_getall_by("site", site_id), etag=etag, params=kwargs
        )

    def getall_by_building(self, building_id, *, etag=None, **kwargs):
        return self._req.getall(
            self.endpoint_uri_getall_by("building", building_id),
            etag=etag,
            params=kwargs,
        )

    def getall_by_storey(self, storey_id, *, etag=None, **kwargs):
        return self._req.getall(
            self.endpoint_uri_getall_by("storey", storey_id), etag=etag, params=kwargs
        )

    def getall_by_space(self, space_id, *, etag=None, **kwargs):
        return self._req.getall(
            self.endpoint_uri_getall_by("space", space_id), etag=etag, params=kwargs
        )

    def getall_by_zone(self, zone_id, *, etag=None, **kwargs):
        return self._req.getall(
            self.endpoint_uri_getall_by("zone", zone_id), etag=etag, params=kwargs
        )


class EventBySiteResources(BaseResources):
    endpoint_base_uri = "/events_by_sites/"
    disabled_endpoints = ["update"]


class EventByBuildingResources(BaseResources):
    endpoint_base_uri = "/events_by_buildings/"
    disabled_endpoints = ["update"]


class EventByStoreyResources(BaseResources):
    endpoint_base_uri = "/events_by_storeys/"
    disabled_endpoints = ["update"]


class EventBySpaceResources(BaseResources):
    endpoint_base_uri = "/events_by_spaces/"
    disabled_endpoints = ["update"]


class EventByZoneResources(BaseResources):
    endpoint_base_uri = "/events_by_zones/"
    disabled_endpoints = ["update"]
