import pytest


def test_pass():
    ...


def test_fail():
    1 / 0


def test_error(x):
    ...


@pytest.mark.skip
def test_skip():
    ...


@pytest.mark.xfail
def test_xpass():
    ...


@pytest.mark.xfail
def test_xfail():
    assert 0
