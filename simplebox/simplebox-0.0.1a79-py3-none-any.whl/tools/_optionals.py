#!/usr/bin/env python
# -*- coding:utf-8 -*-
from typing import Generic, Callable, Optional

from simplebox._internal import _T, _U
from simplebox.exceptions import raise_exception, NonePointerException


class Optionals(Generic[_T]):
    """
    optionals tools
    """

    def __init__(self, value: Optional[_T]):
        self.__value: _T = value

    @staticmethod
    def of(value: Optional[_T]) -> 'Optionals[_T]':
        if not value:
            raise_exception(NonePointerException("value can't none"))
        return Optionals[_T](value)

    @staticmethod
    def of_none_able(value: Optional[_T]) -> 'Optionals[_T]':
        return Optionals.of(value) if value else Optionals[_T](None)

    def get(self) -> Optional[_T]:
        if not self.__value:
            raise_exception(NonePointerException("No value present"))
        return self.__value

    def is_present(self) -> bool:
        return self.__value is not None

    def is_empty(self) -> bool:
        return self.__value is None

    def if_present(self, action: Callable[[_T], None]) -> None:
        if self.__value:
            action(self.__value)

    def if_present_or_else(self, action: Callable[[_T], None], empty_action: Callable) -> None:
        if self.__value:
            action(self.__value)
        else:
            empty_action(self.__value)

    def filter(self, predicate: Callable[[_T], bool]) -> 'Optionals[_T]':
        if not self.is_present():
            return self
        else:
            return self if predicate(self.__value) else Optionals[_T](None)

    def map(self, mapper: Callable[[_T], _U]) -> 'Optionals[_U]':
        if not self.is_present():
            return Optionals[_U](None)
        else:
            return Optionals.of_none_able(mapper(self.__value))

    def flat_map(self, mapper: Callable[[_T], _U]) -> 'Optionals[_U]':
        if not self.is_present():
            return Optionals(None)
        else:
            ret: Optionals[_U] = mapper(self.__value)
            if not ret:
                raise_exception(NonePointerException("value can't none"))
            return ret

    def or_(self, supplier: 'Optionals[_T]') -> 'Optionals[_T]':
        if self.is_present():
            return self
        else:
            ret = supplier.get()
            if not ret:
                raise_exception(NonePointerException("value can't none"))
            return ret

    def or_else(self, other: _T) -> _T:
        return self.__value if self.__value else other

    def or_else_get(self, supplier: Callable[[], _T]) -> Optional[_T]:
        return self.__value if self.__value else supplier()

    def or_else_raise(self, exception: BaseException = None) -> Optional[_T]:
        if not self.__value:
            if exception:
                raise_exception(exception)
            else:
                raise_exception(NonePointerException("No value present"))
        return self.__value


__all__ = [Optionals]
