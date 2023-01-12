"""BEMServer API client resources

/energy_sources/ endpoints
/energy_end_uses/ endpoints
/energy_consumption_timeseries_by_sites/ endpoints
/energy_consumption_timeseries_by_buildings/ endpoints
"""
from .base import BaseResources


class EnergySourceResources(BaseResources):
    endpoint_base_uri = "/energy_sources/"
    disabled_endpoints = ["getone", "create", "update", "delete"]


class EnergyEndUseResources(BaseResources):
    endpoint_base_uri = "/energy_end_uses/"
    disabled_endpoints = ["getone", "create", "update", "delete"]


class EnergyConsumptionTimseriesBySiteResources(BaseResources):
    endpoint_base_uri = "/energy_consumption_timeseries_by_sites/"


class EnergyConsumptionTimseriesByBuildingResources(BaseResources):
    endpoint_base_uri = "/energy_consumption_timeseries_by_buildings/"
