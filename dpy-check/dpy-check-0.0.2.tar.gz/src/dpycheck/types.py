"""Types.

:copyright: (c) 2022-present Tanner B. Corcoran
:license: MIT, see LICENSE for more details.
"""

__author__ = "Tanner B. Corcoran"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2022-present Tanner B. Corcoran"


from discord.ext import commands
import discord
import typing


ctx = commands.Context[commands.Bot]
itx = discord.Interaction
utx = ctx | itx
VT = typing.TypeVar("VT")


class Check:
    _exc: Exception
    _args: tuple
    def predicate(self, utx: utx) -> bool:
        ...

class PartialErrorHandler:
    def __init__(self, channel_id: int, *mention_ids: int,
                 attach_to: object = None) -> None: ...
    async def error(self, *args) -> None: ...
