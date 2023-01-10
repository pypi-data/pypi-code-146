#!/usr/bin/env python
# -*- coding:utf-8 -*-
from threading import Thread
from time import time, sleep
from typing import Callable

from ..classes import ForceType


class Ticker(object):
    """
    A simple timer.
    """
    __interval = ForceType(int)

    def __init__(self, interval: int):
        """
        A simple scheduled task trigger
        :param interval: The interval for the next execution, in seconds
        """
        self.__now = time()
        self.__interval: int = interval
        self.__next: float = self.__now + self.__interval
        self.__num: int = 1

    def apply(self, num: int = None, call: Callable = None) -> bool:
        if issubclass(type(num), int):
            raise TypeError(f"expect int, got {type(num).__name__}")
        if issubclass(type(call), Callable):
            return self.__ticker(num, call)
        else:
            return self.__ticker_no_call(num)

    def apply_sync(self, num: int = 0, call: Callable = None):
        if issubclass(type(num), int):
            raise TypeError(f"expect int, got {type(num).__name__}")
        if issubclass(type(call), Callable):
            ticker_thread = Thread(target=self.__ticker, args=(num, call))
        else:
            ticker_thread = Thread(target=self.__ticker, args=(num,))
        ticker_thread.start()

    def __ticker(self, num: int = None, call: Callable = None):
        sleep(self.__interval)
        call()
        timer = Ticker(self.__interval)
        self.__now = timer.__now
        self.__next = timer.__next
        if 0 < num <= self.__num:
            return False
        self.__num += 1
        return self.__ticker(num, call)

    def __ticker_no_call(self, num: int = None):
        sleep(self.__interval)
        timer = Ticker(self.__interval)
        self.__now = timer.__now
        self.__next = timer.__next
        if 0 < num <= self.__num:
            return False
        self.__num += 1
        return self.__ticker_no_call(num)

    @property
    def num(self) -> int:
        return self.__num

    @property
    def now(self) -> float:
        return self.__now


__all__ = [Ticker]
