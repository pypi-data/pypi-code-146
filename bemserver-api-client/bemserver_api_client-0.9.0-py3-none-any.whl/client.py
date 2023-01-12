"""BEMServer API client"""
import logging
from packaging.version import Version, InvalidVersion
from requests.auth import HTTPBasicAuth

from .exceptions import BEMServerAPIVersionError
from .request import BEMServerApiClientRequest
from .resources import (
    AboutResources,
    UserResources,
    UserGroupResources,
    UserByUserGroupResources,
    CampaignResources,
    UserGroupByCampaignResources,
    CampaignScopeResources,
    UserGroupByCampaignScopeResources,
    TimeseriesResources,
    TimeseriesDataStateResources,
    TimeseriesPropertyResources,
    TimeseriesPropertyDataResources,
    TimeseriesDataResources,
    StructuralElementPropertyResources,
    SiteResources,
    SitePropertyResources,
    SitePropertyDataResources,
    BuildingResources,
    BuildingPropertyResources,
    BuildingPropertyDataResources,
    StoreyResources,
    StoreyPropertyResources,
    StoreyPropertyDataResources,
    SpaceResources,
    SpacePropertyResources,
    SpacePropertyDataResources,
    ZoneResources,
    ZonePropertyResources,
    ZonePropertyDataResources,
    TimeseriesBySiteResources,
    TimeseriesByBuildingResources,
    TimeseriesByStoreyResources,
    TimeseriesBySpaceResources,
    TimeseriesByZoneResources,
    IOResources,
    AnalysisResources,
    ST_CleanupByCampaignResources,
    ST_CleanupByTimeseriesResources,
    ST_CheckMissingByCampaignResources,
    EnergySourceResources,
    EnergyEndUseResources,
    EnergyConsumptionTimseriesBySiteResources,
    EnergyConsumptionTimseriesByBuildingResources,
    EventResources,
    EventCategoryResources,
    EventCategoryByUserResources,
    EventBySiteResources,
    EventByBuildingResources,
    EventByStoreyResources,
    EventBySpaceResources,
    EventByZoneResources,
    TimeseriesByEventResources,
    NotificationResources,
)


APICLI_LOGGER = logging.getLogger(__name__)

REQUIRED_API_VERSION = {
    "min": Version("0.9.0"),
    "max": Version("0.10.0"),
}


class BEMServerApiClient:
    """API client"""

    def __init__(
        self,
        host,
        use_ssl=True,
        authentication_method=None,
        uri_prefix="http",
        auto_check=False,
        request_manager=None,
    ):
        self.base_uri_prefix = uri_prefix or "http"
        self.host = host
        self.use_ssl = use_ssl

        self._request_manager = request_manager or BEMServerApiClientRequest(
            self.base_uri,
            authentication_method,
            logger=APICLI_LOGGER,
        )

        self.about = AboutResources(self._request_manager)

        if auto_check:
            api_version = self.about.getall().data["versions"]["bemserver_api"]
            self.check_api_version(api_version)

        self.io = IOResources(self._request_manager)

        self.users = UserResources(self._request_manager)
        self.user_groups = UserGroupResources(self._request_manager)
        self.user_by_user_groups = UserByUserGroupResources(self._request_manager)

        self.campaigns = CampaignResources(self._request_manager)
        self.user_groups_by_campaigns = UserGroupByCampaignResources(
            self._request_manager
        )
        self.campaign_scopes = CampaignScopeResources(self._request_manager)
        self.user_groups_by_campaign_scopes = UserGroupByCampaignScopeResources(
            self._request_manager
        )

        self.timeseries = TimeseriesResources(self._request_manager)
        self.timeseries_datastates = TimeseriesDataStateResources(self._request_manager)
        self.timeseries_properties = TimeseriesPropertyResources(self._request_manager)
        self.timeseries_property_data = TimeseriesPropertyDataResources(
            self._request_manager
        )
        self.timeseries_data = TimeseriesDataResources(self._request_manager)

        self.sites = SiteResources(self._request_manager)
        self.buildings = BuildingResources(self._request_manager)
        self.storeys = StoreyResources(self._request_manager)
        self.spaces = SpaceResources(self._request_manager)
        self.zones = ZoneResources(self._request_manager)

        self.structural_element_properties = StructuralElementPropertyResources(
            self._request_manager
        )
        self.site_properties = SitePropertyResources(self._request_manager)
        self.building_properties = BuildingPropertyResources(self._request_manager)
        self.storey_properties = StoreyPropertyResources(self._request_manager)
        self.space_properties = SpacePropertyResources(self._request_manager)
        self.zone_properties = ZonePropertyResources(self._request_manager)

        self.site_property_data = SitePropertyDataResources(self._request_manager)
        self.building_property_data = BuildingPropertyDataResources(
            self._request_manager
        )
        self.storey_property_data = StoreyPropertyDataResources(self._request_manager)
        self.space_property_data = SpacePropertyDataResources(self._request_manager)
        self.zone_property_data = ZonePropertyDataResources(self._request_manager)

        self.timeseries_by_sites = TimeseriesBySiteResources(self._request_manager)
        self.timeseries_by_buildings = TimeseriesByBuildingResources(
            self._request_manager
        )
        self.timeseries_by_storeys = TimeseriesByStoreyResources(self._request_manager)
        self.timeseries_by_spaces = TimeseriesBySpaceResources(self._request_manager)
        self.timeseries_by_zones = TimeseriesByZoneResources(self._request_manager)

        self.analysis = AnalysisResources(self._request_manager)

        self.st_cleanup_by_campaign = ST_CleanupByCampaignResources(
            self._request_manager
        )
        self.st_cleanup_by_timeseries = ST_CleanupByTimeseriesResources(
            self._request_manager
        )

        self.st_check_missing_by_campaign = ST_CheckMissingByCampaignResources(
            self._request_manager
        )

        self.energy_sources = EnergySourceResources(self._request_manager)
        self.energy_end_uses = EnergyEndUseResources(self._request_manager)
        self.energy_cons_ts_by_sites = EnergyConsumptionTimseriesBySiteResources(
            self._request_manager
        )
        self.energy_cons_ts_by_buildings = (
            EnergyConsumptionTimseriesByBuildingResources(self._request_manager)
        )

        self.events = EventResources(self._request_manager)
        self.event_categories = EventCategoryResources(self._request_manager)
        self.event_categories_by_users = EventCategoryByUserResources(
            self._request_manager
        )
        self.event_by_sites = EventBySiteResources(self._request_manager)
        self.event_by_buildings = EventByBuildingResources(self._request_manager)
        self.event_by_storeys = EventByStoreyResources(self._request_manager)
        self.event_by_spaces = EventBySpaceResources(self._request_manager)
        self.event_by_zones = EventByZoneResources(self._request_manager)
        self.timeseries_by_events = TimeseriesByEventResources(self._request_manager)

        self.notifications = NotificationResources(self._request_manager)

    @property
    def uri_prefix(self):
        uri_prefix = self.base_uri_prefix
        if self.use_ssl:
            uri_prefix = self.base_uri_prefix.replace("http", "https")
        return f"{uri_prefix}://"

    @property
    def base_uri(self):
        return f"{self.uri_prefix}{self.host}"

    @staticmethod
    def make_http_basic_auth(email, password):
        return HTTPBasicAuth(
            email.encode(encoding="utf-8"),
            password.encode(encoding="utf-8"),
        )

    @classmethod
    def check_api_version(cls, api_version):
        try:
            version_api = Version(str(api_version))
        except InvalidVersion as exc:
            raise BEMServerAPIVersionError(f"Invalid API version: {str(exc)}")
        version_min = REQUIRED_API_VERSION["min"]
        version_max = REQUIRED_API_VERSION["max"]
        if not (version_min <= version_api < version_max):
            raise BEMServerAPIVersionError(
                f"API version ({str(version_api)}) not supported!"
                f" (expected: >={str(version_min)},<{str(version_max)})"
            )
