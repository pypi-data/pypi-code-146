import math
import time

from redis.client import Redis, AsyncWriter


def test_async_writer():
    r = Redis()
    r.flushall()

    ar = AsyncWriter()

    for i in range(100):
        ar.set(str(i), i)

    ar.wait_all()

    for i in range(100):
        x = r.get(str(i))
        assert int(x) == i

    bench_async_writer()


def bench_async_writer():
    r = Redis()
    r.flushall()

    ar = AsyncWriter()

    def bench(rds):
        for i in range(10000):
            x = math.factorial(i % 5000) + 3 // 7
            rds.set(str(i), x % 100)

    st = time.time()
    bench(ar)
    ar.wait_all()
    ed = time.time()

    print("async writes:", ed - st)

    r.flushall()

    st = time.time()
    bench(r)
    ed = time.time()
    print("sync writes:", ed - st)
