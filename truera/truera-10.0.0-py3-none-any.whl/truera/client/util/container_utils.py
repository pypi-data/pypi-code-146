from __future__ import annotations

from dataclasses import dataclass
import itertools
from typing import (
    Any, Callable, Dict, Generic, Iterable, List, Sequence, Tuple, Type, TypeVar
)

A = TypeVar("A")
B = TypeVar("B")

# container
C = TypeVar("C")

# key
K = TypeVar("K")

# value
V = TypeVar("V")


def xor(a: A, b: A, warn=True) -> A:
    """
    Return either of a or b that is not None. If both are not None, raise
    exception or warn. Recurses to the dictionary version of xor for
    dictionaries.
    """

    if a is not None and b is not None:
        if isinstance(a, dict):
            assert isinstance(
                b, dict
            ) or b is None, f"Could not xor dictionary with a non-dict type {type(b)}"
            return DictUtils.xor(a, b, warn=warn)
        elif a != b:
            msg = f"Multiple values provided {a} != {b} but one expected."
            if warn:
                print("WARNING: " + msg)
            else:
                raise ValueError(msg)

    if a is not None:
        return a

    return b


class IterableUtils:
    # copied from trulens

    @staticmethod
    def then_(iter1: Iterable[V], iter2: Iterable[V]) -> Iterable[V]:
        """Iterate through the given iterators, one after the other."""

        for x in iter1:
            yield x
        for x in iter2:
            yield x


class DictUtils:

    @staticmethod
    def xor(a: Dict[K, V], b: Dict[K, V], warn=True) -> Dict[K, V]:
        """
        Merge two dictionaries but error or warn if the same key is given two different non-None values.
        """

        ret = dict()

        for k, v in a.items():
            if v is not None:
                ret[k] = v

        for k, v in b.items():
            if k in ret and a[k] is not None and a[k] != v:
                msg = f"Multiple values provided for key {k}, {a[k]} != {v} but one expected."
                if warn:
                    print(f"WARNING: " + msg)
                else:
                    raise ValueError(msg)
            ret[k] = v

        return ret

    # copied from trulens
    @staticmethod
    def with_(d: Dict[K, V], k: K, v: V) -> Dict[K, V]:
        """
        Copy of the given dictionary with the given key replaced by the given value.
        """

        d = d.copy()
        d[k] = v
        return d

    # copied from trulens
    @staticmethod
    def except_(d: Dict[K, V], k: K) -> Dict[K, V]:
        """
        Copy of the given dictionary with the given key removed.
        """

        return {_k: v for _k, v in d.items() if _k != k}


class SequenceUtils:
    # copied from trulens

    @staticmethod
    def with_(l: Sequence[V], i: int, v: V) -> Sequence[V]:
        """
        Copy of the given list or tuple with the given index replaced by the
        given value.
        """

        if isinstance(l, list):
            l = l.copy()
            l[i] = v
        elif isinstance(l, tuple):
            l = list(l)
            l[i] = v
            l = tuple(l)
        else:
            raise ValueError(
                f"list or tuple expected but got {l.__class__.__name__}"
            )

        return l

    @staticmethod
    def except_(l: Sequence[V], i: int) -> Sequence[V]:
        """
        Return the given sequence minus the element at index `i`.
        """

        return l[0:i] + l[i + 1:]


@dataclass
class Lens(Generic[A, B]):
    # TODO: merge with trulens lens implementation? (note: "lens" in "trulens"
    # is NOT what this is).

    get: Callable[[A], B]
    set: Callable[[A, B], A]

    # not standard, optional:
    without: Callable[[A], A] = None

    @staticmethod
    def sequence_elements(c: List[A]) -> Iterable[Lens[List[A], A]]:
        """
        Lenses focusing on elements of a list.
        """

        for i in range(len(c)):
            yield Lens(
                get=lambda l, i=i: l[i],
                set=lambda l, v, i=i: SequenceUtils.with_(l, i, v),
                without=lambda l, i=i: SequenceUtils.except_(l, i)
            )

    @staticmethod
    def dict_values(c: Dict[K, V]) -> Iterable[Lens[Dict[K, V], V]]:
        """
        Lenses focusing on values in a dictionary.
        """

        for k in c.keys():
            yield Lens(
                get=lambda d, k=k: d[k],
                set=lambda d, v, k=k: DictUtils.with_(d, k, v),
                without=lambda d, k=k: DictUtils.except_(d, k)
            )

    @staticmethod
    def compose(l1: Lens[A, B], l2: Lens[B, C]) -> Lens[A, C]:
        """
        Compose two lenses.
        """

        return Lens(
            get=lambda c: l2.get(l1.get(c)),
            set=lambda c, e: l1.set(c, l2.set(l1.get(c), e)),
            without=lambda c: l1.set(c, l2.without(l1.get(c)))
        )


@dataclass
class Args:
    """
    Container for python method arguments, i.e. positional `args` and named `kwargs`.
    """

    args: List[Any]
    kwargs: Dict[str, Any]

    lens_args = Lens(
        get=lambda s: s.args,
        set=lambda s, a: Args(a, s.kwargs),
        without=lambda s: Args([], s.kwargs)
    )
    lens_kwargs = Lens(
        get=lambda s: s.kwargs,
        set=lambda s, a: Args(s.args, a),
        without=lambda s: Args(s.args, {})
    )

    def lenses_args(self) -> Iterable[Lens[Args, Any]]:
        for l in Lens.sequence_elements(self.args):
            yield Lens.compose(Args.lens_args, l)

    def lenses_kwargs(self) -> Iterable[Lens[Args, Any]]:
        for l in Lens.dict_values(self.kwargs):
            yield Lens.compose(Args.lens_kwargs, l)

    def lenses(self) -> Iterable[Lens[Args, Any]]:
        return itertools.chain(self.lenses_args(), self.lenses_kwargs())

    def pop_named_matched(self, name: str,
                          match: Callable[[A], bool]) -> Tuple[Args, A]:
        """
        If have the kwarg named `name` matched by `match`, pop it. Otherwise try
        to find a matching object in args. If have named object but is not
        matched, raises error.
        """

        if name in self.kwargs:
            v = self.kwargs[name]
            assert match(
                v
            ), f"Have object named {name} but does not match requirements."

            return Args(self.args, DictUtils.except_(self.kwargs, name)), v

        for l in self.lenses_args():
            v = l.get(self)

            if match(v):
                return l.without(self), v

        return self, None

    def pop_named_typed(self, name: str, type: Type[A]) -> Tuple[Args, A]:
        return self.pop_named_matched(name, lambda v: isinstance(v, type))
