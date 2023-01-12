"""Checks that require other checks.

:copyright: (c) 2022-present Tanner B. Corcoran
:license: MIT, see LICENSE for more details.
"""

__author__ = "Tanner B. Corcoran"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2022-present Tanner B. Corcoran"


import typing
from . import types
from . import exceptions


class Not(types.Check):
    def __init__(self, check: types.Check) -> None:
        self._exc = exceptions.get_reverse(check._exc)
        self._args = check._args
        self._check = check
    
    async def predicate(self, utx: types.utx, /) -> bool:
        return not await self._check.predicate(utx)


class Any(types.Check):
    def __init__(self, *checks: types.Check) -> None:
        self._exc = exceptions.Generic
        self._args: tuple = ()
        self._checks = checks
    
    async def predicate(self, utx: types.utx, /) -> bool:
        for c in self._checks:
            if await c.predicate(utx) is True:
                return True
        return False
Or = Any


class All(types.Check):
    def __init__(self, *checks: types.Check) -> None:
        self._exc = exceptions.Generic
        self._args: tuple[typing.Any, ...] = ()
        self._checks = checks

    async def predicate(self, utx: types.utx, /) -> bool:
        for c in self._checks:
            if await c.predicate(utx) is not True:
                self._exc = c._exc
                self._args = c._args
                return False
        return True
And = All
