from functools import reduce
from hestia_earth.utils.tools import non_empty_list, list_sum

from hestia_earth.aggregation.log import logger
from hestia_earth.aggregation.utils import _min, _max, _sd
from hestia_earth.aggregation.utils.term import _blank_node_completeness


def _debugNodes(nodes: list):
    for node in nodes:
        if node.get('yield'):
            logger.debug(
                'id=%s, yield=%s, weight=%s, ratio=%s/%s, organic=%s, irrigated=%s',
                node.get('@id'),
                round(node.get('yield')),
                100/len(nodes),
                1,
                len(nodes),
                node.get('organic'),
                node.get('irrigated')
            )


def _weighted_value(node: dict):
    value = node.get('value')
    weight = node.get('productValue', 1)
    return None if value is None else (list_sum(value, value), weight)


def _aggregate(nodes: list, completeness: dict):
    first_node = nodes[0]
    term = first_node.get('term')
    completeness_key = _blank_node_completeness(first_node)
    completeness_count = len([node for node in nodes if node.get('completeness', False)])
    completeness_count_total = completeness.get(completeness_key, 0)
    completeness_count_missing = (
        completeness_count_total - completeness_count
    ) if completeness_count_total > completeness_count else 0

    values = non_empty_list(map(_weighted_value, nodes))
    # account for complete nodes which have no value
    values_with_completeness = values + ([(0, 1)] * completeness_count_missing)
    values = [value for value, _w in values_with_completeness]
    total_weight = sum(weight for _v, weight in values_with_completeness)
    weighted_values = [value * weight for value, weight in values_with_completeness]
    value = sum(weighted_values) / (total_weight if total_weight != 0 else 1)

    return {
        'node': first_node,
        'term': term,
        'value': value,
        'max': _max(values),
        'min': _min(values),
        'sd': _sd(values),
        'observations': len(values)
    } if len(values) > 0 else None


def _aggregate_term(aggregates_map: dict, completeness: dict):
    def aggregate(term_id: str):
        blank_nodes = [node for node in aggregates_map.get(term_id, []) if not node.get('deleted')]
        return _aggregate(blank_nodes, completeness) if len(blank_nodes) > 0 else None
    return aggregate


def _aggregate_nodes(aggregate_key: str, index=0):
    def aggregate(data: dict):
        if index == 0:
            _debugNodes(data.get('nodes', []))
        completeness = data.get('completeness', {})
        terms = data.get(aggregate_key).keys()
        aggregates = non_empty_list(map(_aggregate_term(data.get(aggregate_key), completeness), terms))
        return (aggregates, data) if len(aggregates) > 0 else ([], {})

    def aggregate_multiple(data: dict):
        return reduce(
            lambda prev, curr: {**prev, curr[1]: _aggregate_nodes(curr[1], curr[0])(data)}, enumerate(aggregate_key), {}
        )

    return aggregate if isinstance(aggregate_key, str) else aggregate_multiple


def aggregate(aggregate_key: str, groups: dict) -> list:
    return non_empty_list(map(_aggregate_nodes(aggregate_key), groups.values()))
