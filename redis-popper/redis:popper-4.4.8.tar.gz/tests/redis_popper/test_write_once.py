import time

from redis.client import Redis
from redis.key_types import KeyCacheProp


def timed(f, *args, **kwargs):
    st = time.time()
    ret = f(*args, **kwargs)
    ed = time.time()
    return ret, ed - st


def test_write_once():
    print('')
    LATENCY = 0.05 * 1e-3
    SUFFIX = "C"

    def suffixed(key):
        return key + ":" + SUFFIX

    key_types = {SUFFIX : KeyCacheProp.WRITE_ONCE}
    r = Redis(host='localhost', key_types=key_types)
    r.flushall()

    def write_once_cmd_test(set_cmd, get_cmd, set_args, get_args):
        key = set_args[0]
        set_cmd(*set_args)
        ve, t1 = timed(get_cmd, *get_args)
        key = suffixed(key)
        set_args[0] = key
        get_args[0] = key
        set_cmd(*set_args)
        v, t2 = timed(get_cmd, *get_args)
        assert v == ve
        v, t3 = timed(get_cmd, *get_args)
        assert v == ve

        assert t1 - t3 >= LATENCY
        assert t2 - t3 >= LATENCY

        print(get_cmd.__name__, t1, t2, t3)
        print(v)

    write_once_cmd_test(r.set, r.get, ['get', 'val'], ['get'])

    write_once_cmd_test(r.hset, r.hget, ['hget', 'key', 'val'], ['hget', 'key'])

    write_once_cmd_test(r.hset, r.hgetall,
                        ['hgetall', None, None, {'k1': 'v1', 'k2': 'v2'}], ['hgetall'])

    write_once_cmd_test(r.hset, r.hmget,
                        ['hmget', None, None, {'k1': 'v1', 'k2': 'v2', 'k3': 'v3'}],
                        ['hmget', ['k2', 'k3']])

    assert not r.hexists(suffixed('no'), 'key')
    assert not r.hexists(suffixed('no'), 'key')

    r.hset(suffixed('hx'), 'k1', 'v1')
    assert not r.hexists(suffixed('hx'), 'k2')
    assert not r.hexists(suffixed('hx'), 'k2')
    assert r.hexists(suffixed('hx'), 'k1')
    assert r.hexists(suffixed('hx'), 'k1')

    _, t1 = timed(r.hexists, suffixed('hx'), 'k1')
    r.hgetall(suffixed('hx'))  # should be cached now
    v, t2 = timed(r.hexists, suffixed('hx'), 'k1')

    assert t1 - t2 >= LATENCY
    print('hexists', t1, t2, v)


def test_flush():
    keys = {"c": KeyCacheProp.WRITE_ONCE}
    r = Redis(host='localhost', key_types=keys)
    r.set("k:c", "k")
    assert r.get("k:c") is not None
    r.flushall()
    assert r.get("k:c") is None
