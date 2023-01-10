import json

from fuzzywuzzy import fuzz
from utils import db, dt
from utils.cache import cache

from gig._constants import GIG_CACHE_NAME, GIG_CACHE_TIMEOUT
from gig._remote_data import _get_remote_tsv_data
from gig.ent_types import ENTITY_TYPE, get_entity_type


def clean_types(d):
    if 'area' in d:
        d['area'] = dt.parse_float(d['area'])

    if 'population' in d:
        d['population'] = dt.parse_int(d['population'])

    if 'centroid_altitude' in d:
        try:
            d['centroid_altitude'] = dt.parse_float(d['centroid_altitude'])
        except ValueError:
            d['centroid_altitude'] = 0

    for k in ['centroid', 'subs', 'supers', 'ints', 'eqs']:
        if k in d:
            if d[k]:
                d[k] = json.loads(d[k].replace('\'', '"'))
    return d


@cache(GIG_CACHE_NAME, GIG_CACHE_TIMEOUT)
def get_entities(entity_type):
    return list(
        map(
            clean_types,
            list(
                filter(
                    lambda x: x,
                    _get_remote_tsv_data('ents/%s.tsv' % (entity_type)),
                )
            ),
        )
    )


@cache(GIG_CACHE_NAME, GIG_CACHE_TIMEOUT)
def get_entity_index(entity_type):
    entities = get_entities(entity_type)
    return dict(
        zip(
            list(
                map(
                    lambda e: e[db.get_id_key(entity_type)],
                    entities,
                )
            ),
            entities,
        )
    )


@cache(GIG_CACHE_NAME, GIG_CACHE_TIMEOUT)
def get_entity(entity_id):
    entity_type = get_entity_type(entity_id)
    entity_index = get_entity_index(entity_type)
    return entity_index.get(entity_id, None)


@cache(GIG_CACHE_NAME, GIG_CACHE_TIMEOUT)
def multiget_entities(entity_ids):
    entity_map = {}
    for entity_id in entity_ids:
        entity_map[entity_id] = get_entity(entity_id)
    return entity_map


@cache(GIG_CACHE_NAME, GIG_CACHE_TIMEOUT)
def get_entity_ids(entity_type):
    return list(get_entity_index(entity_type).keys())


@cache(GIG_CACHE_NAME, GIG_CACHE_TIMEOUT)
def get_entities_by_name_fuzzy(
    fuzzy_entity_name,
    filter_entity_type=None,
    filter_parent_id=None,
    limit=5,
    min_fuzz_ratio=80,
):
    matching_entities_info = []
    for entity_type in ENTITY_TYPE.list():
        if filter_entity_type and (filter_entity_type != entity_type):
            continue

        entities = get_entities(entity_type)
        for entity in entities:
            if filter_parent_id and (filter_parent_id not in entity['id']):
                continue

            fuzz_ratio = fuzz.ratio(entity['name'], fuzzy_entity_name)

            if fuzz_ratio >= min_fuzz_ratio:
                matching_entities_info.append([entity, fuzz_ratio])

    matching_entities = list(
        map(
            lambda x: x[0],
            sorted(
                matching_entities_info,
                key=lambda x: -x[1],
            ),
        )
    )
    if len(matching_entities) >= limit:
        return matching_entities[:limit]

    return matching_entities
