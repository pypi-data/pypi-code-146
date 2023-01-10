import pytest
from plunk.sb.slabsiter_experiments.dict_generators import (
    IterativeDictProcessingDAG,
    SimpleRepeater,
)

import itertools
from know.base import SlabsIter


def phase(session):
    return session * 10


def something_dependent(session, phase):
    return session + phase


def something_independent():
    return 'hi'


def test_iterative_dict_processing():
    dd = IterativeDictProcessingDAG(phase, something_dependent, something_independent)
    assert dd(session=201) == {
        'session': 201,
        'something_independent': 'hi',
        'phase': 2010,
        'something_dependent': 2211,
    }


def test_dict_generator_with_slabsiter():
    counter = itertools.count()

    def count():
        return next(counter)

    s = SlabsIter(x=lambda: 7, y=lambda: next(counter), z=SimpleRepeater('hey', 3))
    assert list(s) == [
        {'x': 7, 'y': 0, 'z': 'hey'},
        {'x': 7, 'y': 1, 'z': 'hey'},
        {'x': 7, 'y': 2, 'z': 'hey'},
    ]
