import pytest
from simple_caching.storage import DictMemory

set_counter = 0

@pytest.fixture(autouse=True)
def run_around_tests():
    TestCache.set_counter = 0
    TestCache.key_counter = 0
    yield

class TestCache:
    set_counter = 0
    key_counter = 0

    @staticmethod
    def set_fn(x):
        TestCache.set_counter += 1
        return x**2

    @staticmethod
    def key_fn(x):
        TestCache.key_counter += 1
        return x

    def test_ctor_1(self):
        cache = DictMemory("test")
        assert not cache is None

    def test_setitem_1(self):
        cache = DictMemory("test")
        cache[2] = TestCache.set_fn(2)
        assert TestCache.set_counter == 1

    def test_setitem_2(self):
        cache = DictMemory("test")
        cache[2] = TestCache.set_fn(2)
        cache[2] = TestCache.set_fn(2)
        assert TestCache.set_counter == 2

    def test_setitem_3(self):
        cache = DictMemory("test", key_encode_fn=lambda x: x+1)
        cache[2] = TestCache.set_fn(2)
        cache[2] = TestCache.set_fn(2)
        assert TestCache.set_counter == 2

    def test_setitem_4(self):
        """Lazy variant"""
        cache = DictMemory("test", key_encode_fn=lambda x: x+1)
        cache[2] = TestCache.set_fn
        cache[2] = TestCache.set_fn
        assert TestCache.set_counter == 1

    def test_setitem_5(self):
        cache = DictMemory("test", key_encode_fn=TestCache.key_fn)
        cache[2] = TestCache.set_fn
        cache[2] = TestCache.set_fn
        assert TestCache.set_counter == 1
        assert TestCache.key_counter == 2

    def test_getitem_1(self):
        cache = DictMemory("test")
        item = TestCache.set_fn(20)
        cache[20] = item
        assert cache[20] == item
        assert TestCache.set_counter == 1
        assert TestCache.key_counter == 0

    def test_getitem_2(self):
        cache = DictMemory("test", key_encode_fn=TestCache.key_fn)
        item = TestCache.set_fn(20)
        cache[20] = item
        assert cache[20] == item
        assert TestCache.set_counter == 1
        assert TestCache.key_counter == 2

    def test_getitem_vs_get_1(self):
        """Warning! get() does not call the key_encode_fn, just __getitem__ !"""
        cache = DictMemory("test", key_encode_fn=lambda x: x+1)
        item = TestCache.set_fn(20)
        cache[20] = item
        try:
            _ = cache._get(20)
            assert False
        except:
            pass
        assert cache._get(21) == item

    def test_getitem_vs_get_2(self):
        """Warning! get() does not call the key_encode_fn, just __getitem__ !"""
        cache = DictMemory("test", key_encode_fn=lambda x: x+1)
        item = TestCache.set_fn(20)
        cache[20] = item
        try:
            _ = cache[21]
            assert False
        except:
            pass
        assert cache[20] == item

    def test_contains_vs_check_1(self):
        """Same with check(key) vs __contains__(key)"""
        cache = DictMemory("test", key_encode_fn=lambda x: x+1)
        cache[2] = TestCache.set_fn(20)
        assert cache._check(2) == False
        assert cache._check(3) == True

    def test_contains_vs_check_2(self):
        cache = DictMemory("test", key_encode_fn=lambda x: x+1)
        cache[2] = TestCache.set_fn(20)
        assert 2 in cache
        assert 3 not in cache

    def test_map_1(self):
        cache = DictMemory("test", key_encode_fn=lambda x: x+1)
        cache.map(TestCache.set_fn, [2, 3, 4, 2])
        assert TestCache.set_counter == 3
        assert cache[2] == TestCache.set_fn(2)
