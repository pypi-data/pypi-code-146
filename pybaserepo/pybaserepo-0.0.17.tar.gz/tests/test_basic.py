import pytest as pytest


def test_true():
    assert True


def test_false():
    assert not False


def test_ex():
    with pytest.raises(RuntimeError):
        raise RuntimeError()
