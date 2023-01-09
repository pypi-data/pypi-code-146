from dints.abc import AbstractDistLock



"""TODO: Implement distributed lock interface for Memcached backend"""
class MemcachedDistLock(AbstractDistLock):
    """Distributed lock supported by Memcached backend."""