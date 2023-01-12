"""Checks for roles.

:copyright: (c) 2022-present Tanner B. Corcoran
:license: MIT, see LICENSE for more details.
"""

__author__ = "Tanner B. Corcoran"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2022-present Tanner B. Corcoran"


import typing
import discord
from . import types
from . import exceptions
from . import utils


def _get_role(roles: typing.Iterable[discord.Role],
              identifier: int | str) -> typing.Optional[discord.Role]:
    if isinstance(identifier, int):
        return discord.utils.get(roles, id=identifier)
    return discord.utils.get(roles, name=identifier)

def _predicate(utx: types.utx, guild_id: int | None, role: int | str | typing.Iterable[int | str],
               user_id: int) -> bool:
        if guild_id:
            client = utils.get_client(utx)
            guild = client.get_guild(guild_id)
        else:
            guild = utx.guild
        if not guild:
            return False

        member = guild.get_member(user_id)
        if not member:
            return False

        user_role_ids = [role.id for role in member.roles]
        
        if utils.isiterable(role):
            roles = [_get_role(guild.roles, id) for id in role]
            role_ids = [role.id for role in roles if role is not None]
            if set(user_role_ids).intersection(role_ids):
                return True
            return False

        _role = _get_role(guild.roles, role)
        if not _role:
            return False
        if _role.id in user_role_ids:
            return True
        return False


class user_has_role(types.Check):
    def __init__(self, role: int | str | typing.Iterable[int | str],
                 guild_id: typing.Optional[int] = None, /) -> None:
        self._exc = exceptions.UserMissingRole
        self._args = (role, guild_id)
        self._role: int = role
        self._guild_id: typing.Optional[int] = guild_id
    
    async def predicate(self, utx: types.utx, /) -> bool:
        return _predicate(utx, self._guild_id, self._role,
                          utils.get_author(utx).id)


class bot_has_role(types.Check):
    def __init__(self, role: int | str | typing.Iterable[int | str],
                 guild_id: typing.Optional[int] = None, /) -> None:
        self._exc = exceptions.BotMissingRole
        self._args = (role, guild_id)
        self._role: int = role
        self._guild_id: typing.Optional[int] = guild_id

    async def predicate(self, utx: types.utx, /) -> bool:
        return _predicate(utx, self._guild_id, self._role,
                          utils.get_me(utx).id)
