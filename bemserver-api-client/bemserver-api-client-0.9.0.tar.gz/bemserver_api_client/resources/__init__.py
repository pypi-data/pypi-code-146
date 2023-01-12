"""BEMServer API client resources"""

from .about import AboutResources  # noqa
from .analysis import AnalysisResources  # noqa
from .campaigns import (  # noqa
    CampaignResources,
    UserGroupByCampaignResources,
    CampaignScopeResources,
    UserGroupByCampaignScopeResources,
)
from .energy import (  # noqa
    EnergySourceResources,
    EnergyEndUseResources,
    EnergyConsumptionTimseriesBySiteResources,
    EnergyConsumptionTimseriesByBuildingResources,
)
from .events import (  # noqa
    EventResources,
    EventCategoryResources,
    EventCategoryByUserResources,
    EventBySiteResources,
    EventByBuildingResources,
    EventByStoreyResources,
    EventBySpaceResources,
    EventByZoneResources,
)
from .io import IOResources  # noqa
from .notifications import NotificationResources  # noqa
from .services import (  # noqa
    ST_CleanupByCampaignResources,
    ST_CleanupByTimeseriesResources,
    ST_CheckMissingByCampaignResources,
)
from .structural_elements import (  # noqa
    SiteResources,
    BuildingResources,
    StoreyResources,
    SpaceResources,
    ZoneResources,
    StructuralElementPropertyResources,
    SitePropertyResources,
    BuildingPropertyResources,
    StoreyPropertyResources,
    SpacePropertyResources,
    ZonePropertyResources,
    SitePropertyDataResources,
    BuildingPropertyDataResources,
    StoreyPropertyDataResources,
    SpacePropertyDataResources,
    ZonePropertyDataResources,
)
from .timeseries import (  # noqa
    TimeseriesResources,
    TimeseriesDataStateResources,
    TimeseriesPropertyResources,
    TimeseriesPropertyDataResources,
    TimeseriesDataResources,
    TimeseriesBySiteResources,
    TimeseriesByBuildingResources,
    TimeseriesByStoreyResources,
    TimeseriesBySpaceResources,
    TimeseriesByZoneResources,
    TimeseriesByEventResources,
)
from .users import (  # noqa
    UserResources,
    UserGroupResources,
    UserByUserGroupResources,
)
