from dints.abc import AbstractDistLock



"""TODO: Implement distributed lock interface for Redis backend"""
class RedisDistLock(AbstractDistLock):
    """Distributed lock supported by Redis backend."""