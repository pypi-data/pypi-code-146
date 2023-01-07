import time
from threading import Thread

from the_spymaster_util.ttl_dict import TTLDict

TTL_DEFAULT = 0.01
TTL_LONG = TTL_DEFAULT * 5

SLEEP_DEFAULT = TTL_DEFAULT * 2
SLEEP_LONG = TTL_LONG * 2


def test_get():
    ttl_dict = TTLDict(TTL_DEFAULT)
    ttl_dict["a"] = 1
    assert ttl_dict.get("a") == 1
    assert ttl_dict.get("b") is None
    assert ttl_dict.get("b", "default") == "default"
    assert len(ttl_dict) == 1
    time.sleep(SLEEP_DEFAULT)
    assert ttl_dict.get("a") is None
    assert ttl_dict.get("a", "default") == "default"
    assert len(ttl_dict) == 0


def test_set():
    ttl_dict = TTLDict(TTL_DEFAULT)
    ttl_dict["a"] = 1
    ttl_dict.set("b", 2, ttl=TTL_LONG)
    assert ttl_dict["a"] == 1
    assert ttl_dict["b"] == 2
    assert len(ttl_dict) == 2
    time.sleep(SLEEP_DEFAULT)
    assert ttl_dict.get("a") is None
    assert ttl_dict.get("b") == 2
    assert len(ttl_dict) == 1
    time.sleep(SLEEP_LONG - SLEEP_DEFAULT)
    assert ttl_dict.get("b") is None
    assert len(ttl_dict) == 0


def test_contains():
    ttl_dict = TTLDict(TTL_DEFAULT)
    ttl_dict["a"] = 1
    assert "a" in ttl_dict
    assert "b" not in ttl_dict
    time.sleep(SLEEP_DEFAULT)
    assert "a" not in ttl_dict
    assert "b" not in ttl_dict


def test_is_expired():
    ttl_dict = TTLDict(TTL_DEFAULT, a=1, b=2)
    assert not ttl_dict.is_expired("a")
    assert not ttl_dict.is_expired("b")
    assert len(ttl_dict) == 2
    time.sleep(SLEEP_DEFAULT)
    assert ttl_dict.is_expired("a")
    assert ttl_dict.is_expired("b")
    assert len(ttl_dict) == 0


def test_len():
    ttl_dict = TTLDict(SLEEP_DEFAULT)
    assert len(ttl_dict) == 0
    ttl_dict["a"] = 1
    ttl_dict["b"] = 2
    assert len(ttl_dict) == 2
    time.sleep(SLEEP_DEFAULT)
    assert len(ttl_dict) == 0


def test_iter_empty():
    ttl_dict = TTLDict(TTL_DEFAULT)
    for key in ttl_dict:
        assert False, f"Iterating empty dictionary gave a key {key}"


def test_iter():
    ttl_dict = TTLDict(TTL_DEFAULT)
    orig_dict = {"a": 1, "b": 2, "c": 3}
    ttl_dict.update(orig_dict)
    assert len(ttl_dict) == len(orig_dict)
    for key in ttl_dict:
        assert ttl_dict[key] == orig_dict[key]


def test_keys():
    ttl_dict = TTLDict(TTL_DEFAULT, a=1, b=2)
    assert set(ttl_dict.keys()) == {"a", "b"}
    time.sleep(SLEEP_DEFAULT)
    assert len(ttl_dict) == 0
    assert set(ttl_dict.keys()) == set()


def test_values():
    ttl_dict = TTLDict(TTL_DEFAULT)
    orig_dict = {"a": 1, "b": 2}
    ttl_dict.update(orig_dict)
    values = set(ttl_dict.values())
    assert len(values) == 2
    assert values == {1, 2}


def test_items():
    ttl_dict = TTLDict(TTL_DEFAULT)
    orig_dict = {"a": 1, "b": 2}
    ttl_dict.update(orig_dict)
    items = list(ttl_dict.items())
    assert len(items) == 2
    assert items == [("a", 1), ("b", 2)]


def test_ttl_dict_from_multiple_threads():
    ttl = 0.2
    ttl_dict = TTLDict(ttl)
    threads = []
    thread_count = 1000

    def lazy_set(n: int):
        ttl_dict[n] = n
        time.sleep(0.05)

    for i in range(thread_count):
        thread = Thread(target=lazy_set, args=(i,))
        threads.append(thread)
    for thread in threads:
        thread.start()
    assert len(ttl_dict) > 0
    for thread in threads:
        thread.join()

    assert len(ttl_dict) == thread_count
    for i in range(thread_count):
        assert ttl_dict[i] == i

    time.sleep(ttl)
    assert len(ttl_dict) == 0
