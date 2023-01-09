from functools import reduce
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name, extract_grouped_data_closest_date
from hestia_earth.utils.model import find_primary_product
from hestia_earth.utils.tools import list_sum, safe_parse_float, flatten

from hestia_earth.aggregation.log import debugRequirements
from hestia_earth.aggregation.utils import value_difference
from hestia_earth.aggregation.utils.emission import get_emissions_system_boundary
from .utils import _cycle_end_year

FAOSTAT_PRODUCTION_LOOKUP_COLUMN = 'cropGroupingFaostatProduction'
YIELD_THRESHOLD = 20


def _faostat_crop_grouping(term_id: str):
    lookup = download_lookup('crop.csv')
    return get_table_value(lookup, 'termid', term_id, column_name(FAOSTAT_PRODUCTION_LOOKUP_COLUMN))


def _faostat_crop_yield(country_id: str, grouping: str, date: int):
    lookup = download_lookup(f"region-crop-{FAOSTAT_PRODUCTION_LOOKUP_COLUMN}-yield.csv")
    value = get_table_value(lookup, 'termid', country_id, column_name(grouping))
    return safe_parse_float(extract_grouped_data_closest_date(value, date), 0) / 10


def _calculate_score_yield(cycle: dict):
    country_id = cycle.get('site', {}).get('country', {}).get('@id')
    year = _cycle_end_year(cycle)
    product = find_primary_product(cycle)
    grouping = _faostat_crop_grouping((product or {}).get('term', {}).get('@id'))
    faostat_yield = _faostat_crop_yield(country_id, grouping, year) if grouping else None
    product_yield = list_sum(product.get('value')) if product else None
    delta = value_difference(product_yield, faostat_yield) * 100 if faostat_yield and product_yield else 0

    debugRequirements(id=cycle.get('id'),
                      faostat_yield=faostat_yield,
                      product_yield=product_yield,
                      delta=delta,
                      delta_min=YIELD_THRESHOLD)

    return delta <= YIELD_THRESHOLD


def _list_max_observations(values: list):
    values = flatten(v.get('observations', 0) for v in values if isinstance(v, dict))
    return max(values) if len(values) > 0 else 0


def _calculate_score_nb_cycles(cycle: dict):
    max_observations = [_list_max_observations(v) for v in cycle.values() if isinstance(v, list)]
    nb_observations = max(max_observations)

    debugRequirements(id=cycle.get('id'),
                      nb_observations=nb_observations)

    return nb_observations >= 50


def _calculate_score_completeness(cycle: dict):
    values = [v for v in cycle.get('completeness', {}).values() if isinstance(v, bool)]
    is_complete = all(values)

    debugRequirements(id=cycle.get('id'),
                      is_complete=is_complete)

    return is_complete


def _calculate_score_emissions_system_boundary(cycle: dict):
    all_emission_ids = get_emissions_system_boundary()
    cycle_emission_ids = list(set([e.get('term', {}).get('@id') for e in cycle.get('emissions', [])]))
    all_included = all([id in all_emission_ids for id in cycle_emission_ids])

    debugRequirements(id=cycle.get('id'),
                      total_emissions=len(all_emission_ids),
                      included_emissions=len(cycle_emission_ids),
                      all_included=all_included)

    return all_included


SCORES = [
    _calculate_score_yield,
    _calculate_score_nb_cycles,
    _calculate_score_completeness,
    _calculate_score_emissions_system_boundary
]


def calculate_score(cycle: dict):
    score = reduce(lambda total, func: total + (1 if func(cycle) else 0), SCORES, 0)
    return {
        **cycle,
        'aggregatedQualityScore': score
    }
