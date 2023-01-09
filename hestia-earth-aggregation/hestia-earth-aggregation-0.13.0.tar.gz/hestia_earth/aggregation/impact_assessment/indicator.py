from hestia_earth.schema import IndicatorJSONLD, IndicatorStatsDefinition
from hestia_earth.utils.model import linked_node

from hestia_earth.aggregation.utils import _aggregated_version
from hestia_earth.aggregation.utils.term import METHOD_MODEL


def _new_indicator(data: dict, value: float = None, include_methodModel=False):
    node = IndicatorJSONLD().to_dict()
    node['term'] = linked_node(data.get('term'))
    node['methodModel'] = linked_node(data.get('methodModel')) if include_methodModel else METHOD_MODEL
    if value is not None:
        node['value'] = value
        node['statsDefinition'] = IndicatorStatsDefinition.IMPACTASSESSMENTS.value
    return _aggregated_version(node, 'term', 'methodModel', 'statsDefinition', 'value')
