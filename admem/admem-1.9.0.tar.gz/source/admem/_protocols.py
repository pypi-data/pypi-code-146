# Copyright (c) 2022-2023 Mario S. Könz; License: MIT
import typing as tp

T = tp.TypeVar("T")  # pylint: disable=invalid-name


class BackendStoreProtocol(tp.Protocol):
    def dump(self, obj: T) -> tp.Any:
        pass  # pragma: no cover

    def load_all(self, dataclass: type[T], **filter_kwgs: tp.Any) -> tp.Iterator[T]:
        pass  # pragma: no cover

    def parse(self, backend_obj: tp.Any) -> tp.Any:
        pass  # pragma: no cover

    def backend_manager(self, dataclass: type[T]) -> tp.Any:
        pass  # pragma: no cover
