from functools import reduce
from hestia_earth.schema import (
    CycleStartDateDefinition, CycleFunctionalUnit, SchemaType, CompletenessJSONLD, CycleDefaultMethodClassification
)
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.tools import list_sum, non_empty_list, list_average, safe_parse_date
from hestia_earth.utils.model import find_term_match, find_primary_product

from hestia_earth.aggregation.utils import _aggregated_node, _aggregated_version, _set_dict_array, _save_json
from hestia_earth.aggregation.utils.queries import _download_node
from hestia_earth.aggregation.utils.term import _format_country_name, _format_organic, _format_irrigated
from hestia_earth.aggregation.utils.site import (
    _group_by_measurements, _format_results as format_site, _create_site, _update_site
)
from hestia_earth.aggregation.models.terms import aggregate as aggregate_by_term
from .emission import _new_emission
from .input import _new_input
from .practice import _new_practice
from .product import _new_product

AGGREGATION_KEYS = ['inputs', 'products', 'emissions']


def _format_aggregate(new_func):
    def format(aggregate: dict):
        term = aggregate.get('term')
        value = aggregate.get('value')
        min = aggregate.get('min')
        max = aggregate.get('max')
        sd = aggregate.get('sd')
        observations = aggregate.get('observations')
        node = new_func(term, value)
        _set_dict_array(node, 'observations', observations)
        _set_dict_array(node, 'min', min)
        _set_dict_array(node, 'max', max)
        _set_dict_array(node, 'sd', sd, True)
        return _aggregated_version(node, 'min', 'max', 'sd', 'observations')
    return format


def _format_site(sites: list):
    groups = _group_by_measurements(sites)
    aggregates = aggregate_by_term('measurements', groups)
    return format_site(aggregates[0]) if len(aggregates) > 0 else None


def _aggregate_completeness(cycles: list):
    def is_complete(key: str):
        return any([cycle.get('completeness', {}).get(key) is True for cycle in cycles])

    completeness = CompletenessJSONLD().to_dict()
    keys = list(completeness.keys())
    keys.remove('@type')
    return {
        **completeness,
        **reduce(lambda prev, curr: {**prev, curr: is_complete(curr)}, keys, {}),
    }


def _format_terms_results(results: dict, include_matrix=True):
    products, data = results.get('products')
    inputs, _ = results.get('inputs')
    emissions, _ = results.get('emissions')
    cycles = data.get('nodes', [])
    if len(cycles) > 0:
        cycle = cycles[0]
        # set the site if any measurements
        site = _format_site(data.get('sites', []))
        cycle['site'] = site or _create_site(cycle['site'], False)
        # set the primary product
        product_id = (find_primary_product(cycle) or {}).get('term').get('@id')
        cycle = {
            **_create_cycle(cycle, include_matrix),
            'completeness': _aggregate_completeness(cycles),
            'inputs': list(map(_format_aggregate(_new_input), inputs)),
            'products': list(map(_format_aggregate(_new_product), products)),
            'emissions': list(map(_format_aggregate(_new_emission), emissions))
        }
        if product_id:
            product = find_term_match(cycle.get('products'), product_id)
            product['primary'] = True
            product['economicValueShare'] = list_average([
                p['node'].get('economicValueShare') for p in products if p['node'].get('term').get('@id') == product_id
            ], None)
            return cycle
    return None


def _format_country_results(results: dict):
    _, data = results.get('products')
    cycles = data.get('nodes', [])
    if len(cycles) > 0:
        cycle = cycles[0]
        primary_product = find_primary_product(cycle)
        return {
            **_format_terms_results(results, False),
            'name': _cycle_name(cycle, primary_product, False, False, False),
            'id': _cycle_id(cycle, primary_product, False, False, False)
        } if primary_product else None
    return None


def _format_world_results(results: dict):
    return _format_terms_results(results)


def _download_site(site: dict):
    # aggregated site will not have a recalculated version
    data = _download_node('recalculated')(site) or _download_node()(site) or {}
    _save_json(data, f"{data.get('@type')}-{data.get('@id')}")
    return data if data.get('@type') else None


def _format_grouping_relative(product_value: float, cycle: dict, list_key: str):
    is_relative = cycle.get('functionalUnit', CycleFunctionalUnit._1_HA.value) == CycleFunctionalUnit.RELATIVE.value
    items = cycle.get(list_key, [])
    return [
        {**item, 'value': [v / product_value for v in item.get('value', [])]} for item in items
    ] if is_relative else items


def _format_for_grouping(cycles: dict):
    def format(cycle: dict):
        product = find_primary_product(cycle) or {}
        site = cycle.get('site')
        site = _download_site(site) if not site.get('siteType') else site
        value = list_sum(product.get('value', []), None)
        return {
            **cycle,
            'inputs': _format_grouping_relative(value, cycle, 'inputs'),
            'products': _format_grouping_relative(value, cycle, 'products'),
            'emissions': _format_grouping_relative(value, cycle, 'emissions'),
            'site': site,
            'product': product.get('term'),
            'yield': value,
            'country': site.get('country'),
            'organic': _is_organic(cycle),
            'irrigated': _is_irrigated(cycle)
        } if product.get('economicValueShare', 0) > 0 and value is not None and site else None
    return non_empty_list(map(format, cycles))


def _is_organic(cycle: dict):
    lookup = download_lookup('standardsLabels.csv', True)

    def term_organic(lookup, term_id: str):
        return get_table_value(lookup, 'termid', term_id, column_name('isOrganic')) == 'organic'

    practices = list(filter(lambda p: p.get('term') is not None, cycle.get('practices', [])))
    return any([term_organic(lookup, p.get('term', {}).get('@id')) for p in practices])


def _is_irrigated(cycle: dict):
    practice = find_term_match(cycle.get('practices', []), 'irrigated', None)
    return practice is not None and list_sum(practice.get('value', [100])) > 0


def _cycle_id(n: dict, primary_product: dict, organic: bool, irrigated: bool, include_matrix=True):
    return '-'.join(non_empty_list([
        primary_product.get('term', {}).get('@id'),
        _format_country_name(n.get('site', {}).get('country', {}).get('name')),
        _format_organic(organic) if include_matrix else '',
        _format_irrigated(irrigated) if include_matrix else '',
        n.get('startDate'),
        n.get('endDate')
    ]))


def _cycle_name(n: dict, primary_product: dict, organic: bool, irrigated: bool, include_matrix=True):
    return ' - '.join(non_empty_list([
        primary_product.get('term', {}).get('name'),
        n.get('site', {}).get('country', {}).get('name'),
        ', '.join(non_empty_list([
            ('Organic' if organic else 'Conventional') if include_matrix else '',
            ('Irrigated' if irrigated else 'Non Irrigated') if include_matrix else ''
        ])),
        '-'.join([n.get('startDate'), n.get('endDate')])
    ]))


def _create_cycle(data: dict, include_matrix=False):
    cycle = {'type': SchemaType.CYCLE.value}
    # copy properties from existing ImpactAssessment
    cycle['startDate'] = data.get('startDate')
    cycle['endDate'] = data.get('endDate')
    cycle['functionalUnit'] = data['functionalUnit']
    cycle['startDateDefinition'] = CycleStartDateDefinition.START_OF_YEAR.value
    cycle['dataPrivate'] = False
    cycle['defaultMethodClassification'] = CycleDefaultMethodClassification.MODELLED.value
    if include_matrix:
        if data.get('organic') or _is_organic(data):
            cycle['practices'] = cycle.get('practices', []) + [_new_practice('organic')]
        if data.get('irrigated') or _is_irrigated(data):
            cycle['practices'] = cycle.get('practices', []) + [_new_practice('irrigated')]
    if data.get('site'):
        cycle['site'] = data['site']
    return _aggregated_node(cycle)


def _update_cycle(country_name: str, start: int, end: int, source: dict = None, include_matrix=True):
    def update(cycle: dict):
        cycle['startDate'] = str(start)
        cycle['endDate'] = str(end)
        cycle['site'] = _update_site(country_name, source, False)(cycle['site'])
        primary_product = find_primary_product(cycle)
        organic = _is_organic(cycle)
        irrigated = _is_irrigated(cycle)
        cycle['name'] = _cycle_name(cycle, primary_product, organic, irrigated, include_matrix)
        cycle['site']['name'] = cycle['name']
        cycle['id'] = _cycle_id(cycle, primary_product, organic, irrigated, include_matrix)
        cycle['site']['id'] = cycle['id']
        return cycle if source is None else {**cycle, 'defaultSource': source}
    return update


def _cycle_end_year(cycle: dict):
    date = safe_parse_date(cycle.get('endDate'))
    return date.year if date else None
