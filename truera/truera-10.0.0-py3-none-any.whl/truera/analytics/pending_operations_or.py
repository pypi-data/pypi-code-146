from __future__ import annotations

from typing import Any, Generic, Optional, Sequence, TypeVar

T = TypeVar('T')


class PendingOperationsOr(Generic[T]):

    def __init__(self, operations: Optional[Sequence[str]], value: T):
        self._operations = operations
        self._value = value

    @property
    def operations(self):
        assert self.is_operations
        return self._operations

    @property
    def value(self) -> T:
        assert self._value is not None
        return self._value

    @property
    def is_operations(self):
        return self._operations and len(self._operations) > 0

    @staticmethod
    def from_operations(operations: Sequence[str]) -> PendingOperationsOr[Any]:
        assert operations and len(operations) > 0
        return PendingOperationsOr(operations, None)

    @staticmethod
    def from_value(value: T) -> PendingOperationsOr[T]:
        assert value is not None
        return PendingOperationsOr(None, value)

    @staticmethod
    def from_pending_operations(
        pending_operations_or_list: Sequence[PendingOperationsOr]
    ) -> PendingOperationsOr[Any]:
        operation_ids = []
        for pending_operations_or in pending_operations_or_list:
            if pending_operations_or is not None and pending_operations_or.is_operations:
                operation_ids.extend(pending_operations_or._operations)
        return PendingOperationsOr.from_operations(operation_ids)

    @staticmethod
    def is_any_pending(
        pending_operations_or_list: Sequence[PendingOperationsOr]
    ) -> bool:
        return any(map(lambda x: x.is_operations, pending_operations_or_list))
