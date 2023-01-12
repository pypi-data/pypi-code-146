"""Checks for guild permissions.

:copyright: (c) 2022-present Tanner B. Corcoran
:license: MIT, see LICENSE for more details.
"""

__author__ = "Tanner B. Corcoran"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2022-present Tanner B. Corcoran"


from . import types
from . import exceptions
from . import utils
import discord


def _predicate(self: types.Check, utx: types.utx, guild_id: int | None,
               user_id: int, perms: dict[str, discord.Permissions]
               ) -> bool:
    client = utils.get_client(utx)
    if guild_id:
        guild = client.get_guild(guild_id)
        if not guild:
            return False
        member = guild.get_member(user_id)
        if not member:
            return False
        _perms = member.guild_permissions
    else:
        if not utx.guild:
            self._args = (guild_id,)
            return False
        _perms = utx.guild.get_member(user_id).guild_permissions
    missing = [p for p, v in perms.items() if getattr(_perms, p) != v]
    if not missing:
        return True
    self._args = tuple([guild_id] + missing)
    return False


class user_has_guild_perms(types.Check):
    def __init__(self, guild_id: int = None, **perms: bool) -> None:
        invalid = set(perms) - set(discord.Permissions.VALID_FLAGS)
        if invalid:
            raise TypeError(f"Invalid permission(s): {', '.join(invalid)}")
        self._exc = exceptions.UserMissingGuildPerms
        self._args: tuple[int | None | discord.Permissions, ...] = ()
        self._guild_id = guild_id
        self._perms = perms
    
    async def predicate(self, utx: types.utx, /) -> bool:
        return _predicate(self, utx, self._guild_id,
                          utils.get_author(utx).id, self._perms)


class bot_has_guild_perms(types.Check):
    def __init__(self, guild_id: int = None, **perms: bool) -> None:
        invalid = set(perms) - set(discord.Permissions.VALID_FLAGS)
        if invalid:
            raise TypeError(f"Invalid permission(s): {', '.join(invalid)}")
        self._exc = exceptions.BotMissingGuildPerms
        self._args: tuple[int | None | discord.Permissions, ...] = ()
        self._guild_id = guild_id
        self._perms: dict[str, bool] = perms
    
    async def predicate(self, utx: types.utx, /) -> bool:
        return _predicate(self, utx, self._guild_id,
                          utils.get_me(utx).id, self._perms)
