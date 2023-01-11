import os
from aiokeydb import KeyDBClient
from aiokeydb.exceptions import ConnectionError


if os.getenv('KEYDB_HOST'):
    try:
        KeyDBClient.ping()
        NO_CACHE = False
    except ConnectionError:
        NO_CACHE = True
else:
    NO_CACHE = True


def cache_invalidator(*args, invalidate_local_cache: bool = False, **kwargs):
    return invalidate_local_cache
