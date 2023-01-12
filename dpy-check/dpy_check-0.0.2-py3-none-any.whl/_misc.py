"""Miscellaneous checks.

:copyright: (c) 2022-present Tanner B. Corcoran
:license: MIT, see LICENSE for more details.
"""

__author__ = "Tanner B. Corcoran"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2022-present Tanner B. Corcoran"


from discord.ext import commands
from . import exceptions
from . import types
from . import utils
import functools
import datetime
import discord
import typing


class in_dm(types.Check):
    def __init__(self) -> None:
        self._exc = exceptions.NotInDM
        self._args: tuple[discord.Permissions, ...] = ()
    
    async def predicate(self, utx: types.utx, /) -> bool:
        return utx.guild is None


class is_user(types.Check):
    def __init__(self, user_id: int | typing.Iterable[int], /) -> None:
        self._exc = exceptions.IsNotUser
        self._args: tuple[int] = (user_id,)
        self._user_id: int = user_id
    
    async def predicate(self, utx: types.utx, /) -> bool:
        if utils.isiterable(self._user_id):
            return utils.get_author(utx).id in self._user_id
        return utils.get_author(utx).id == self._user_id


class in_channel(types.Check):
    def __init__(self, channel_id: int | typing.Iterable[int], /) -> None:
        self._exc = exceptions.NotInChannel
        self._args: tuple[int] = (channel_id,)
        self._channel_id = channel_id
    
    async def predicate(self, utx: types.utx, /) -> bool:
        if utils.isiterable(self._channel_id):
            return utx.channel.id in self._channel_id
        return utx.channel.id == self._channel_id


class in_guild(types.Check):
    def __init__(self, guild_id: int | typing.Iterable[int]) -> None:
        self._exc = exceptions.NotInGuild
        self._args: tuple[int] = (guild_id,)
        self._guild_id = guild_id
    
    async def predicate(self, utx: types.utx, /) -> bool:
        if utx.guild is None:
            return False
        if utils.isiterable(self._guild_id):
            return utx.guild.id in self._guild_id
        return utx.guild.id == self._guild_id


class in_category(types.Check):
    def __init__(self, category_id: int | typing.Iterable[int]) -> None:
        self._exc = exceptions.NotInCategory
        self._args: tuple[int] = (category_id,)
        self._category_id = category_id

    async def predicate(self, utx: types.utx, /) -> bool:
        if utx.channel is None:
            return False
        if utx.channel.category is None:
            return False
        if utils.isiterable(self._category_id):
            return utx.channel.category.id in self._category_id
        return utx.channel.category.id == self._category_id


class is_bot_owner(types.Check):
    def __init__(self) -> None:
        self._exc = exceptions.IsNotBotOwner
        self._args: tuple = ()

    async def predicate(self, utx: types.utx, /) -> bool:
        client = utils.get_client(utx)
        author = utils.get_author(utx)
        return client.is_owner(author)


class channel_is_nsfw(types.Check):
    def __init__(self, channel_id: int = None, /) -> None:
        self._exc = exceptions.ChannelIsNotNSFW
        self._args: tuple[int] = (channel_id,)
        self._channel_id = channel_id

    async def predicate(self, utx: types.utx, /) -> bool:
        # guild=None means were inside a dm, which is always nsfw
        if utx.guild is None:
            return True
        if self._channel_id:
            client = utils.get_client(utx)
            channel = client.get_channel(self._channel_id)
        else:
            channel = utx.channel
        return isinstance(channel, (discord.TextChannel,
                                    discord.Thread,
                                    discord.VoiceChannel)) and channel.is_nsfw()


class is_guild_owner(types.Check):
    def __init__(self, guild_id: int = None) -> None:
        self._exc = exceptions.IsNotGuildOwner
        self._args: tuple[int | None] = (guild_id,)
        self._guild_id = guild_id

    async def predicate(self, utx: types.utx, /) -> bool:
        if self._guild_id:
            client = utils.get_client(utx)
            guild = client.get_guild(self._guild_id)
        else:
            guild = utx.guild
        if not guild:
            return False
        author = utils.get_author(utx)
        return author.id == guild.owner_id


class username_contains(types.Check):
    def __init__(self,
                 substr: str | typing.Callable[[commands.Context |
                                                  discord.Interaction],
                                                 tuple[str, bool]], /) -> None:
        self._exc = exceptions.UsernameDoesNotContain
        self._args: tuple[str | None] = (substr,)
        self._substr = substr
    
    async def predicate(self, utx: types.utx, /) -> bool:
        if isinstance(self._substr, str):
            author = utils.get_author(utx)
            return self._substr.lower() in author.display_name.lower()
        arg, passed = self._substr(utx)
        self._args = (arg,)
        return passed


class membership(types.Check):
    def __init__(self, timespec: typing.Literal["s", "m", "h", "d", "w",
                                                "y"] = "s") -> None:
        self._exc = exceptions.Generic
        self._args = ()
        self._predicate_set: bool = False
        timespec_multipliers = {
            "s": 1,
            "m": 60,
            "h": 60 * 60,
            "d": 60 * 60 * 24,
            "w": 60 * 60 * 24 * 7,
            "y": 60 * 60 * 24 * 7 * 52
        }
        self._tsmul = timespec_multipliers[timespec]
    
    async def predicate(self, utx: types.utx, /) -> bool:
        return True
    
    def _get_delta(self, utx: types.utx, /) -> float:
        now = datetime.datetime.utcnow()
        now = now.replace(tzinfo=datetime.timezone.utc)
        author = utils.get_author(utx)
        delta: datetime.timedelta = now - author.joined_at
        return delta.total_seconds() / self._tsmul

    def __lt__(self, other: float) -> "membership":
        if self._predicate_set:
            self._args = (self._args[0], exceptions.MembershipGE, other * self._tsmul)
            _predicate = self.predicate
            async def predicate(self: "membership", utx: types.utx, /) -> bool:
                return await _predicate(utx) and (self._get_delta(utx) < other)
        else:
            self._exc = exceptions.MembershipGE
            self._args = (other * self._tsmul,)
            async def predicate(self: "membership", utx: types.utx, /) -> bool:
                return self._get_delta(utx) < other
        self._predicate_set = True
        self.predicate = functools.partial(predicate, self)
        return self

    def __gt__(self, other: float) -> "membership":
        if self._predicate_set:
            self._args = (self._args[0], exceptions.MembershipLE,
                          other * self._tsmul)
            _predicate = self.predicate
            async def predicate(self: "membership", utx: types.utx, /
                                ) -> bool:
                return await _predicate(utx) and (self._get_delta(utx)
                                                    > other)
        else:
            self._exc = exceptions.MembershipLE
            self._args = (other * self._tsmul,)
            async def predicate(self: "membership", utx: types.utx, /
                                ) -> bool:
                return self._get_delta(utx) > other
        self._predicate_set = True
        self.predicate = functools.partial(predicate, self)
        return self

    def __le__(self, other: float) -> "membership":
        if self._predicate_set:
            self._args = (self._args[0], exceptions.MembershipGT,
                          other * self._tsmul)
            _predicate = self.predicate
            async def predicate(self: "membership", utx: types.utx, /
                                ) -> bool:
                return await _predicate(utx) and (self._get_delta(utx)
                                                    <= other)
        else:
            self._exc = exceptions.MembershipGT
            self._args = (other * self._tsmul,)
            async def predicate(self: "membership", utx: types.utx, /
                                ) -> bool:
                return self._get_delta(utx) <= other
        self._predicate_set = True
        self.predicate = functools.partial(predicate, self)
        return self

    def __ge__(self, other: float) -> "membership":
        if self._predicate_set:
            self._args = (self._args[0], exceptions.MembershipLT,
                          other * self._tsmul)
            _predicate = self.predicate
            async def predicate(self: "membership", utx: types.utx, /
                                ) -> bool:
                return await _predicate(utx) and (self._get_delta(utx)
                                                    >= other)
        else:
            self._exc = exceptions.MembershipLT
            self._args = (other * self._tsmul,)
            async def predicate(self: "membership", utx: types.utx, /
                                ) -> bool:
                return self._get_delta(utx) >= other
        self._predicate_set = True
        self.predicate = functools.partial(predicate, self)
        return self


class custom(types.Check):
    def __init__(self,
                 predicate: typing.Callable[[commands.Context |
                                               discord.Interaction],
                                              typing.Awaitable[bool]]) -> None:
        self._exc = exceptions.Generic
        self._args: tuple = ()
        self._predicate = predicate
    
    async def predicate(self, utx: types.utx, /) -> bool:
        return await self._predicate(utx)
