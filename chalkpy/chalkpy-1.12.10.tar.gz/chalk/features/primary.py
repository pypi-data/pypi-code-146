from typing import Type, TypeVar, cast

from typing_extensions import Annotated

T = TypeVar("T")


class PrimaryMeta(type):
    def __getitem__(self, item: Type[T]) -> Type[T]:
        return cast(Type[T], Annotated[item, "__chalk_primary__"])


Primary = PrimaryMeta("Primary", (object,), {})
