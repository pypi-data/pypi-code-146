import dataclasses
from typing import TypeVar, Generic, cast, Union, Callable

__all__ = ['Either', 'Left', 'Right']

LeftT = TypeVar('LeftT')
RightT = TypeVar('RightT')


class Either(Generic[LeftT, RightT], object):
    def map_left(self, callable_):
        # type: (Callable) -> Union[Left, Right]
        if isinstance(self, Left):
            return Left(callable_(self.val))
        else:
            return cast(Right, self)

    def into_inner(self):
        # type: () -> Union[LeftT, RightT]
        if isinstance(self, Left):
            return self.val
        else:
            return cast(Right, self).val


@dataclasses.dataclass()
class Left(Either[LeftT, RightT]):
    val: LeftT


@dataclasses.dataclass()
class Right(Either[LeftT, RightT]):
    val = RightT


EitherT = TypeVar('EitherT', bound=Either)
