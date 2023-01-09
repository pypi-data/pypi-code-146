import pytest

from pylidator.validators import contains


def test_string_contains_seed():
    subject = 'hello world'
    seed = 'world'
    assert contains(subject, seed) is True


def test_string_contains_seed_ignore_case_false():
    subject = 'hello world'
    seed = 'WORLD'
    options = {
        'ignore_case': False
    }
    assert contains(subject, seed, options) is False


def test_string_contains_seed_ignore_case_true():
    subject = 'hello world'
    seed = 'WORLD'
    options = {
        'ignore_case': True
    }
    assert contains(subject, seed, options) is True
