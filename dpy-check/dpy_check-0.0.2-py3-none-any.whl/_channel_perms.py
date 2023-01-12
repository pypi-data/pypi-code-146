"""Checks for channel permissions.

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


def _predicate(self: types.Check, utx: types.utx, channel_id: int | None,
               user_id: int, perms: dict[str, discord.Permissions]
               ) -> bool:
    if channel_id:
        client = utils.get_client(utx)
        channel = client.get_channel(channel_id)
        if not channel:
            return False
        member = channel.guild.get_member(user_id)
        if not member:
            return False
        _perms = channel.permissions_for(member)
    else:
        _perms = utx.permissions
    missing = [p for p, v in perms.items() if getattr(_perms, p) != v]
    if not missing:
        return True
    self._args = tuple([channel_id] + missing)
    return False


class user_has_channel_perms(types.Check):
    """A check for user channel perms.
    
    """
    def __init__(self, channel_id: int = None, **perms: bool) -> None:
        """
        Arguments
        ---------
        channel_id : int, default=None
            If defined, the permissions will be checked on the given channel.
            Otherwise, the current channel will be used.
        **perms : bool
            The discord permissions (key) and whether the user has it (value).
            All valid flags can be found through
            `discord.Permissions.VALID_FLAGS`.
        
        """
        invalid = set(perms) - set(discord.Permissions.VALID_FLAGS)
        if invalid:
            raise TypeError(f"Invalid permission(s): {', '.join(invalid)}")
        self._exc = exceptions.UserMissingChannelPerms
        self._args: tuple[int | None | discord.Permissions, ...] = ()
        self._channel_id = channel_id
        self._perms = perms
    
    async def predicate(self, utx: types.utx, /) -> bool:
        return _predicate(self, utx, self._channel_id,
                          utils.get_author(utx).id, self._perms)


class bot_has_channel_perms(types.Check):
    """A check for bot channel perms.
    
    """
    def __init__(self, channel_id: int = None, **perms: bool) -> None:
        """
        Arguments
        ---------
        channel_id : int, default=None
            If defined, the permissions will be checked on the given channel.
            Otherwise, the current channel will be used.
        **perms : bool
            The discord permissions (key) and whether the user has it (value).
            All valid flags can be found through
            `discord.Permissions.VALID_FLAGS`.
        
        """
        invalid = set(perms) - set(discord.Permissions.VALID_FLAGS)
        if invalid:
            raise TypeError(f"Invalid permission(s): {', '.join(invalid)}")
        self._exc = exceptions.BotMissingChannelPerms
        self._args: tuple[int | None | discord.Permissions, ...] = ()
        self._channel_id = channel_id
        self._perms: dict[str, bool] = perms

    async def predicate(self, utx: types.utx, /) -> bool:
        return _predicate(self, utx, self._channel_id,
                          utils.get_me(utx).id, self._perms)
