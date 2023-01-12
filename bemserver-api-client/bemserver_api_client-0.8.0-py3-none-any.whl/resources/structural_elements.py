"""BEMServer API client resources

/sites/ endpoints
/buildings/ endpoints
/storeys/ endpoints
/spaces/ endpoints
/zones/ endpoints
/structural_element_properties/ endpoints
/site_properties/ endpoints
/building_properties/ endpoints
/storey_properties/ endpoints
/space_properties/ endpoints
/zone_properties/ endpoints
/site_property_data/ endpoints
/building_property_data/ endpoints
/storey_property_data/ endpoints
/space_property_data/ endpoints
/zone_property_data/ endpoints
"""
from .base import BaseResources


class SiteResources(BaseResources):
    endpoint_base_uri = "/sites/"


class BuildingResources(BaseResources):
    endpoint_base_uri = "/buildings/"


class StoreyResources(BaseResources):
    endpoint_base_uri = "/storeys/"


class SpaceResources(BaseResources):
    endpoint_base_uri = "/spaces/"


class ZoneResources(BaseResources):
    endpoint_base_uri = "/zones/"


class StructuralElementPropertyResources(BaseResources):
    endpoint_base_uri = "/structural_element_properties/"


class SitePropertyResources(BaseResources):
    endpoint_base_uri = "/site_properties/"
    disabled_endpoints = ["update"]


class BuildingPropertyResources(BaseResources):
    endpoint_base_uri = "/building_properties/"
    disabled_endpoints = ["update"]


class StoreyPropertyResources(BaseResources):
    endpoint_base_uri = "/storey_properties/"
    disabled_endpoints = ["update"]


class SpacePropertyResources(BaseResources):
    endpoint_base_uri = "/space_properties/"
    disabled_endpoints = ["update"]


class ZonePropertyResources(BaseResources):
    endpoint_base_uri = "/zone_properties/"
    disabled_endpoints = ["update"]


class SitePropertyDataResources(BaseResources):
    endpoint_base_uri = "/site_property_data/"


class BuildingPropertyDataResources(BaseResources):
    endpoint_base_uri = "/building_property_data/"


class StoreyPropertyDataResources(BaseResources):
    endpoint_base_uri = "/storey_property_data/"


class SpacePropertyDataResources(BaseResources):
    endpoint_base_uri = "/space_property_data/"


class ZonePropertyDataResources(BaseResources):
    endpoint_base_uri = "/zone_property_data/"
