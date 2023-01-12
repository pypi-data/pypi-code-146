"""The main ``Check`` class for Context commands.

:copyright: (c) 2022-present Tanner B. Corcoran
:license: MIT, see LICENSE for more details.
"""

__author__ = "Tanner B. Corcoran"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2022-present Tanner B. Corcoran"


from .. import types
from .. import exceptions
from discord.ext import commands


class Check:
    @staticmethod
    def any(*checks: types.Check):
        async def predicate(ctx: types.ctx) -> bool:
            for c in checks:
                if await c.predicate(ctx) is True:
                    return True
            raise exceptions.Generic()
        return commands.check(predicate)

    @staticmethod
    def all(*checks: types.Check):
        async def predicate(ctx: types.ctx) -> bool:
            for c in checks:
                if await c.predicate(ctx) is False:
                    raise c._exc(None, c._args)
            return True
        return commands.check(predicate)
