from slink.sequences import (
    dict_generator,
    DictChain,
    IterativeDictProcessing,
    Repeater,
    _call_from_dict,
)

from know.base import SlabsIter
from meshed import DAG
from i2 import Sig
import itertools


class SimpleRepeater:
    def __init__(self, obj, n_iter):
        self.obj = obj
        self.n_iter = n_iter
        self.iterator = itertools.repeat(self.obj, self.n_iter)

    def __iter__(self):
        return self.iterator

    def __next__(self):
        return next(self.iterator)

    def __call__(self):
        return next(self)


class IterativeDictProcessingDAG:
    def __init__(self, *funcs):
        self.dag = DAG([*funcs])

    def __call__(self, **kwargs):
        _call_from_dict(kwargs=kwargs, func=self.dag, sig=Sig(self.dag))
        return self.dag.last_scope


if __name__ == '__main__':

    def phase(session):
        return session * 10

    def something_dependent(session, phase):
        return session + phase

    def something_independent():
        return 'hi'

    dd = IterativeDictProcessingDAG(phase, something_dependent, something_independent)
    assert dd(session=201) == {
        'session': 201,
        'something_independent': 'hi',
        'phase': 2010,
        'something_dependent': 2211,
    }
