#!/usr/bin/env python
# -*- coding:utf-8 -*-
from ._calculator import _Converter, Enum
from ..number import Integer


class TimeUnit(Enum):
    """
    Time unit conversion tool
    """
    PICO_SECOND = Integer(1)
    NANO_SECOND = Integer(PICO_SECOND * 1000)
    MICRO_SECOND = Integer(NANO_SECOND * 1000)
    MILLI_SECOND = Integer(MICRO_SECOND * 1000)
    SECOND = Integer(MILLI_SECOND * 1000)
    MINUTE = Integer(SECOND * 60)
    HOUR = Integer(MINUTE * 60)
    DAY = Integer(HOUR * 24)

    def of(self, num: int or float) -> '_Converter':
        converter = _Converter(num)
        setattr(converter, "_Converter__decimal", self.value)
        return converter


__all__ = [TimeUnit]
