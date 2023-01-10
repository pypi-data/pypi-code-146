from utils import dt
from utils.cache import cache

from gig._constants import GIG_CACHE_NAME, GIG_CACHE_TIMEOUT
from gig._remote_data import _get_remote_tsv_data
from gig.ent_types import get_entity_type


@cache(GIG_CACHE_NAME, GIG_CACHE_TIMEOUT)
def _get_table(table_id):
    table = _get_remote_tsv_data(f'gig2/{table_id}.tsv')

    return list(
        map(
            lambda row: dict(
                zip(
                    row.keys(),
                    list(map(lambda v: dt.parse_float(v, v), row.values())),
                )
            ),
            table,
        )
    )


@cache(GIG_CACHE_NAME, GIG_CACHE_TIMEOUT)
def _get_table_index(table_id):
    table = _get_table(table_id)
    return dict(
        zip(
            list(map(lambda d: d['entity_id'], table)),
            table,
        )
    )


@cache(GIG_CACHE_NAME, GIG_CACHE_TIMEOUT)
def get_table_data(table_id, entity_ids=None, entity_type=None):
    table_index = _get_table_index(table_id)
    if entity_ids:
        data_map = {}
        for entity_id in entity_ids:
            data_map[entity_id] = table_index.get(entity_id, {})
        return data_map

    if entity_type:
        data_map = {}
        for entity_id, data in table_index.items():
            entity_type0 = get_entity_type(entity_id)
            if entity_type == entity_type0:
                data_map[entity_id] = data
        return data_map

    return table_index
