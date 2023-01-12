"""Exceptions raised by ``Check`` and caught by ``ErrorHandler``.

:copyright: (c) 2022-present Tanner B. Corcoran
:license: MIT, see LICENSE for more details.
"""

__author__ = "Tanner B. Corcoran"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2022-present Tanner B. Corcoran"


from discord.ext import commands
from discord import app_commands


class Generic(commands.CheckFailure, app_commands.CheckFailure): ...

class UserMissingRole(Generic): ...
class UserHasRole(Generic): ...

class BotMissingRole(Generic): ...
class BotHasRole(Generic): ...

class UserMissingChannelPerms(Generic): ...
class UserHasChannelPerms(Generic): ...

class BotMissingChannelPerms(Generic): ...
class BotHasChannelPerms(Generic): ...

class UserMissingGuildPerms(Generic): ...
class UserHasGuildPerms(Generic): ...

class BotMissingGuildPerms(Generic): ...
class BotHasGuildPerms(Generic): ...

class NotInDM(Generic): ...
class InDM(Generic): ...

class IsNotUser(Generic): ...
class IsUser(Generic): ...

class NotInChannel(Generic): ...
class InChannel(Generic): ...

class NotInGuild(Generic): ...
class InGuild(Generic): ...

class NotInCategory(Generic): ...
class InCategory(Generic): ...

class IsNotBotOwner(Generic): ...
class IsBotOwner(Generic): ...

class ChannelIsNotNSFW(Generic): ...
class ChannelIsNSFW(Generic): ...

class IsNotGuildOwner(Generic): ...
class IsGuildOwner(Generic): ...

class UsernameDoesNotContain(Generic): ...
class UsernameContains(Generic): ...

class MembershipGT(Generic): ...
class MembershipLT(Generic): ...
class MembershipGE(Generic): ...
class MembershipLE(Generic): ...


reverse_map = {
    "Generic": Generic,
    "UserMissingRole": UserHasRole,
    "UserHasRole": UserMissingRole,
    "BotMissingRole": BotHasRole,
    "BotHasRole": BotMissingRole,
    "UserMissingChannelPerms": UserHasChannelPerms,
    "UserHasChannelPerms": UserMissingChannelPerms,
    "BotMissingChannelPerms": BotHasChannelPerms,
    "BotHasChannelPerms": BotMissingChannelPerms,
    "UserMissingGuildPerms": UserHasGuildPerms,
    "UserHasGuildPerms": UserMissingGuildPerms,
    "BotMissingGuildPerms": BotHasGuildPerms,
    "BotHasGuildPerms": BotMissingGuildPerms,
    "NotInDM": InDM,
    "InDM": NotInDM,
    "IsNotUser": IsUser,
    "IsUser": IsNotUser,
    "NotInChannel": InChannel,
    "InChannel": NotInChannel,
    "NotInGuild": InGuild,
    "InGuild": NotInGuild,
    "NotInCategory": InCategory,
    "InCategory": NotInCategory,
    "IsNotBotOwner": IsBotOwner,
    "IsBotOwner": IsNotBotOwner,
    "ChannelIsNotNSFW": ChannelIsNSFW,
    "ChannelIsNSFW": ChannelIsNotNSFW,
    "IsNotGuildOwner": IsGuildOwner,
    "IsGuildOwner": IsNotGuildOwner,
    "UsernameDoesNotContain": UsernameContains,
    "UsernameContains": UsernameDoesNotContain,
    "MembershipGT": MembershipLE,
    "MembershipLT": MembershipGE,
    "MembershipGE": MembershipLT,
    "MembershipLE": MembershipGT
}

def get_exc_name(exc: Exception) -> str:
    try:
        return exc.__name__
    except AttributeError:
        return exc.__class__.__name__

def get_reverse(exc: Exception) -> Exception:
    name = get_exc_name(exc)
    if name not in reverse_map:
        return Generic
    return reverse_map[name]
