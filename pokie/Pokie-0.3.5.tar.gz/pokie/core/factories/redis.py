from rick.base import Di
from rick.resource.redis import RedisCache

from pokie.constants import (
    CFG_REDIS_HOST,
    DI_CONFIG,
    CFG_REDIS_PORT,
    DI_REDIS,
    CFG_REDIS_PASSWORD,
    CFG_REDIS_DB,
    CFG_REDIS_SSL,
)


def RedisFactory(_di: Di):
    """
    REDIS factory
    Note: The connection is only created when the resource is accessed on Di
    :param _di:
    :return:
    """

    @_di.register(DI_REDIS)
    def _factory(_di: Di):
        cfg = _di.get(DI_CONFIG)
        redis_cfg = {
            "host": cfg.get(CFG_REDIS_HOST, "localhost"),
            "port": int(cfg.get(CFG_REDIS_PORT, 6379)),
            "password": cfg.get(CFG_REDIS_PASSWORD, ""),
            "db": int(cfg.get(CFG_REDIS_DB, 0)),
            "ssl": True if cfg.get(CFG_REDIS_SSL, None) else False,
        }
        return RedisCache(**redis_cfg)
