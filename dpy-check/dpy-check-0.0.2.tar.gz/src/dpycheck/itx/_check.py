"""The main ``Check`` class for Interaction commands.

:copyright: (c) 2022-present Tanner B. Corcoran
:license: MIT, see LICENSE for more details.
"""

__author__ = "Tanner B. Corcoran"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2022-present Tanner B. Corcoran"


from .. import types
from .. import exceptions
from discord import app_commands


class Check:
    @staticmethod
    def any(*checks: types.Check):
        async def predicate(itx: types.itx) -> bool:
            for c in checks:
                if await c.predicate(itx) is True:
                    return True
            raise exceptions.Generic()
        return app_commands.check(predicate)

    @staticmethod
    def all(*checks: types.Check):
        async def predicate(itx: types.itx) -> bool:
            for c in checks:
                if await c.predicate(itx) is False:
                    raise c._exc(None, c._args)
            return True
        return app_commands.check(predicate)
