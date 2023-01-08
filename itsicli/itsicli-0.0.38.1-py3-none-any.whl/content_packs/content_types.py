from itsimodels.correlation_search import CorrelationSearch
from itsimodels.deep_dive import DeepDive
from itsimodels.entity_type import EntityType
from itsimodels.event_management_state import EventManagementState
from itsimodels.glass_table import GlassTable
from itsimodels.glass_table_icon import GlassTableIcon
from itsimodels.glass_table_image import GlassTableImage
from itsimodels.kpi_base_search import KpiBaseSearch
from itsimodels.kpi_threshold_template import KpiThresholdTemplate
from itsimodels.neap import NotableEventAggregationPolicy
from itsimodels.service import Service
from itsimodels.service_analyzer import ServiceAnalyzer
from itsimodels.service_template import ServiceTemplate
from itsimodels.team import Team


class ContentType(object):
    CORRELATION_SEARCH = 'correlation_searches'
    DEEP_DIVE = 'deep_dives'
    ENTITY_TYPE = 'entity_types'
    EVENT_MANAGEMENT_STATE = 'event_management_states'
    GLASS_TABLE = 'glass_tables'
    GLASS_TABLE_ICON = 'glass_table_icons'
    GLASS_TABLE_IMAGE = 'glass_table_images'
    KPI_BASE_SEARCH = 'kpi_base_searches'
    KPI_THRESHOLD_TEMPLATE = 'kpi_threshold_templates'
    NOTABLE_EVENT_AGGREGATION_POLICY = 'notable_event_aggregation_policies'
    SERVICE_ANALYZER = 'service_analyzers'
    SERVICE_TEMPLATE = 'service_templates'
    SERVICE = 'services'
    TEAM = 'teams'


ContentTypes = {
    ContentType.CORRELATION_SEARCH: CorrelationSearch,
    ContentType.DEEP_DIVE: DeepDive,
    ContentType.ENTITY_TYPE: EntityType,
    ContentType.EVENT_MANAGEMENT_STATE: EventManagementState,
    ContentType.GLASS_TABLE: GlassTable,
    ContentType.GLASS_TABLE_ICON: GlassTableIcon,
    ContentType.GLASS_TABLE_IMAGE: GlassTableImage,
    ContentType.KPI_BASE_SEARCH: KpiBaseSearch,
    ContentType.KPI_THRESHOLD_TEMPLATE: KpiThresholdTemplate,
    ContentType.NOTABLE_EVENT_AGGREGATION_POLICY: NotableEventAggregationPolicy,
    ContentType.SERVICE: Service,
    ContentType.SERVICE_ANALYZER: ServiceAnalyzer,
    ContentType.SERVICE_TEMPLATE: ServiceTemplate,
    ContentType.TEAM: Team
}


def get_content_type_for_model_class(model_class):
    for content_type, cls in ContentTypes.items():
        if cls == model_class:
            return content_type
    return None
