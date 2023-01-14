from abc import abstractmethod
from typing import TypeVar, Protocol


class Equatable(Protocol):
    @abstractmethod
    def __eq__(self: 'EqType', other: 'EqType') -> bool:
        pass


class Hashable(Protocol):
    @abstractmethod
    def __hash__(self: 'HashType'):
        pass


class Comparable(Protocol):
    @abstractmethod
    def __lt__(self: 'CompType', other: 'CompType') -> bool:
        pass

    @abstractmethod
    def __gt__(self: 'CompType', other: 'CompType') -> bool:
        pass

    @abstractmethod
    def __eq__(self: 'CompType', other: 'CompType') -> bool:
        pass


CompType = TypeVar('CompType', bound=Comparable)
EqType = TypeVar('EqType', bound=Equatable)
HashType = TypeVar('HashType', bound=Hashable)
