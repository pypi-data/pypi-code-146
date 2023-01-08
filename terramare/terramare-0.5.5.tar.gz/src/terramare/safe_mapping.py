"""MutableMapping that can handle unhashable types."""
import collections.abc
from dataclasses import dataclass, field
from typing import (
    Dict,
    Generic,
    Iterable,
    Iterator,
    List,
    Mapping,
    MutableMapping,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
)

from typing_extensions import final

_K_in = TypeVar("_K_in")
_V_in = TypeVar("_V_in")

_V_co = TypeVar("_V_co", covariant=True)


# collections.abc.Mapping (and similar collections ABCs) are not subscriptable -
# providing type arguments causes an error at runtime!
@dataclass(init=False)
class EqMapping(Generic[_K_in, _V_co], collections.abc.Mapping):  # type: ignore[type-arg]
    """Mapping using __eq__ for comparison instead of __hash__."""

    _inner: Sequence[Tuple[_K_in, _V_co]] = field(default_factory=list)

    def __init__(
        self,
        elements: Iterable[Tuple[_K_in, _V_co]] = (),
    ) -> None:
        inner: List[Tuple[_K_in, _V_co]] = []
        for k, v in elements:
            if not any(k_ == k for k_, _ in inner):
                inner.append((k, v))
        self._inner = inner

    def __getitem__(self, k: _K_in) -> _V_co:
        index = self._get_index_of(k)
        if index is None:
            raise KeyError(k)
        return self._inner[index][1]

    def __iter__(self) -> Iterator[_K_in]:
        for k, _ in self._inner:
            yield k

    def __len__(self) -> int:
        return len(self._inner)

    def _get_index_of(self, k: _K_in) -> Optional[int]:
        for i, (k_, _) in enumerate(self._inner):
            if k_ == k:
                return i
        return None


@final
@dataclass(init=False)
class EqMutableMapping(
    EqMapping[_K_in, _V_in], collections.abc.MutableMapping  # type: ignore[type-arg]
):
    """MutableMapping using __eq__ for comparison instead of __hash__."""

    _inner: List[Tuple[_K_in, _V_in]] = field(default_factory=list)

    def __setitem__(self, k: _K_in, v: _V_in) -> None:
        index = self._get_index_of(k)
        if index is None:
            index = len(self._inner)
        else:
            del self._inner[index]
        self._inner.insert(index, (k, v))

    def __delitem__(self, k: _K_in) -> None:
        index = self._get_index_of(k)
        if index is None:
            raise KeyError(k)
        del self._inner[index]


@dataclass(init=False)
class SafeMapping(Generic[_K_in, _V_co], collections.abc.Mapping):  # type: ignore[type-arg]
    """Mapping that can handle unhashable types."""

    _hashable: Mapping[_K_in, _V_co]
    _unhashable: EqMapping[_K_in, _V_co]

    def __init__(
        self,
        elements: Iterable[Tuple[_K_in, _V_co]] = (),
    ) -> None:
        hashable = {}
        unhashable = []
        for k, v in elements:
            try:
                hash(k)
            except TypeError:
                unhashable.append((k, v))
            else:
                hashable[k] = v
        self._hashable = hashable
        self._unhashable = EqMutableMapping(unhashable)

    def __getitem__(self, k: _K_in) -> _V_co:
        try:
            hash(k)
            mapping: Mapping[_K_in, _V_co] = self._hashable
        except TypeError:
            mapping = self._unhashable
        return mapping[k]

    def __iter__(self) -> Iterator[_K_in]:
        yield from self._hashable
        yield from self._unhashable

    def __len__(self) -> int:
        return len(self._hashable) + len(self._unhashable)


@final
@dataclass(init=False)
class SafeMutableMapping(
    SafeMapping[_K_in, _V_in], collections.abc.MutableMapping  # type: ignore[type-arg]
):
    """MutableMapping that can handle unhashable types."""

    _hashable: Dict[_K_in, _V_in]
    _unhashable: EqMutableMapping[_K_in, _V_in]

    def __setitem__(self, k: _K_in, v: _V_in) -> None:
        self._get_mapping(k)[k] = v

    def __delitem__(self, k: _K_in) -> None:
        del self._get_mapping(k)[k]

    def _get_mapping(self, k: _K_in) -> MutableMapping[_K_in, _V_in]:
        try:
            hash(k)
        except TypeError:
            return self._unhashable
        return self._hashable
