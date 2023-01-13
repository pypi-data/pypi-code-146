from .resource_balancer import BoundedResourceBalancer
from threading import Thread
from unittest import TestCase


class AsyncRunner(Thread):
    def __init__(self, target):
        def main():
            try:
                self.result = target()
            except BaseException as e:
                self.exception = e

        super().__init__(target=main)
        super().start()

    def join(self, timeout=None):
        super().join(timeout)
        if self.is_alive():
            raise TimeoutError()
        if hasattr(self, "exception"):
            raise self.exception
        else:
            return self.result


class ResourceBalancerTest(TestCase):
    def test_basic_function(self):
        b = BoundedResourceBalancer()
        b.provision([1, 2])

        with b.acquire() as resource1:
            with b.acquire() as resource2:
                assert resource1 != resource2
            with b.acquire() as resource2:
                assert resource1 != resource2
                with b.acquire() as resource3:
                    assert resource3 in (resource1, resource2)
                    with b.acquire() as resource4:
                        assert resource3 != resource4

    def test_delayed_init(self):
        b = BoundedResourceBalancer()

        t = AsyncRunner(b.acquire)
        with self.assertRaises(TimeoutError):
            t.join(0.001)

        b.provision([1])
        assert t.join().__enter__() == 1

    def test_ghosts(self):
        b = BoundedResourceBalancer()
        b.provision([1])

        resource1 = b.acquire()
        with resource1:
            b.provision([])

            t = AsyncRunner(b.acquire)
            with self.assertRaises(TimeoutError):
                t.join(0.001)

            b.provision([1])
            resource2 = t.join()

            assert resource1._instance is resource2._instance
            assert resource2._instance.usage == 2
            assert resource2._instance.resource == 1

    def test_vanishing_resource(self):
        b = BoundedResourceBalancer()
        b.provision([1])

        with b.acquire():
            b.provision([])
            assert b._ghosts[0].usage == 1
            assert b._ghosts[0].resource == 1

        assert b._ghosts[0].usage == 0
        b.provision([])
        assert b._ghosts == []

    def test_even_load(self):
        b = BoundedResourceBalancer()
        b.provision([1, 2])

        with b.acquire() as resource1:
            pass

        with b.acquire() as resource2:
            pass

        assert resource1 != resource2
