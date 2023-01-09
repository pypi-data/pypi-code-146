import pytest
import privateprefs.core.database as _db

test_key = "test key"
test_key2 = "test key2"
test_value = "test value"
test_value2 = "test value2"


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # set up
    _db.delete_all()
    yield
    # tear down
    _db.delete_all()


def test__save():
    _db.write(test_key, test_value)
    assert _db.read(test_key) == test_value


def test__read():
    _db.write(test_key, test_value)
    assert _db.read(test_key) == test_value


def test__read_keys__as_dict():
    _db.write(test_key, test_value)
    _db.write(test_key2, test_value2)
    key_values = _db.read_keys()
    assert key_values[test_key] == test_value and key_values[test_key2] == test_value2


def test__read_keys__as_dict__filtered():
    _db.write(test_key, test_value)
    _db.write(test_key2, test_value2)
    key_values = _db.read_keys(keys=[test_key2])
    assert key_values[test_key2] == test_value2 and len(key_values) == 1


def test__read_keys__as_list():
    _db.write(test_key, test_value)
    _db.write(test_key2, test_value2)
    key_values = _db.read_keys(return_as_list=True)
    assert key_values[0][1] == test_value and key_values[1][1] == test_value2


def test__read_keys__as_list__filtered():
    _db.write(test_key, test_value)
    _db.write(test_key2, test_value2)
    key_values = _db.read_keys(keys=[test_key2], return_as_list=True)
    assert key_values[0][1] == test_value2 and len(key_values) == 1


def test__delete():
    _db.write(test_key, test_value)
    _db.write(test_key2, test_value2)
    _db.delete(test_key)
    assert _db.read(test_key) is None and _db.read(test_key2) == test_value2


def test__delete_all():
    _db.write(test_key, test_value)
    _db.write(test_key2, test_value2)
    _db.delete_all()
    assert _db.read(test_key) is None
