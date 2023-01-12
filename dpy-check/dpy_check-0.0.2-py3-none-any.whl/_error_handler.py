"""The main class for handling command errors.

:copyright: (c) 2022-present Tanner B. Corcoran
:license: MIT, see LICENSE for more details.
"""

__author__ = "Tanner B. Corcoran"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2022-present Tanner B. Corcoran"


from discord.ext import commands
from discord import app_commands
from . import types
from . import exceptions
from . import constants
from . import utils
import traceback
import datetime
import textwrap
import discord
import asyncio
import typing


class Formatter:
    """Used to format errors in `ErrorHandler`.
    
    Methods can be overwritten in a subclass, and methods for additional exceptions can be added by
    created a method called `custom_<excname>` where `<excname>` is the name of the exception. It
    must take one argument (the exception) and, similar to the other methods, must return a string.
    
    """
    def __init__(self) -> None:
        self.error_prefix = "*Error: "
        self.error_postfix = "*"
        self._inequality_map = {
            "MembershipLT": "greater than or equal to",
            "MembershipGT": "less than or equal to",
            "MembershipLE": "greater than",
            "MembershipGE": "less than"
        }

    def _get_timestr(self, seconds: int) -> str:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        return f"UPTIME: {d}d {h}h {m}m {s}s"

    def _make_membership_message(self, exc: commands.CheckFailure,
                                 seconds: int,
                                 alt_exc: commands.CheckFailure = None,
                                 alt_seconds: int = None) -> str:
        timestr = self._get_timestr(seconds)
        phrase = self._inequality_map[exceptions.get_exc_name(exc)]
        if alt_exc is None:
            return f"Your length of server membership must be {phrase} `{timestr}` in order to use this command."
        alt_timestr = self._get_timestr(alt_seconds)
        alt_phrase = self._inequality_map[exceptions.get_exc_name(alt_exc)]
        return f"Your length of server membership must be {phrase} `{timestr}` and {alt_phrase} `{alt_timestr}` in order to use this command."
    
    def Generic(self) -> str:
        return "You or the bot are missing one or more of the permissions required to use this command."
    
    def UserMissingRole(self, role: int | str | typing.Iterable[int | str], guild_id: int | None) -> str:
        return "You are missing one or more of the roles required to use this command."
    
    def UserHasRole(self, role: int | str | typing.Iterable[int | str], guild_id: int | None) -> str:
        return "You have one or more of the roles that are not allowed by this command."
    
    def BotMissingRole(self, role: int | str | typing.Iterable[int | str], guild_id: int | None) -> str:
        return "The bot is missing one or more of the roles required to use this command."
    
    def BotHasRole(self, role: int | str | typing.Iterable[int | str], guild_id: int | None) -> str:
        return "The bot has one or more of the roles that are not allowed by this command."
    
    def UserMissingChannelPerms(self, channel_id: int | None, *perms: discord.Permissions) -> str:
        return "You are missing one or more of the channel permissions required to use this command."
    
    def UserHasChannelPerms(self, channel_id: int | None, *perms: discord.Permissions) -> str:
        return "You have one or more of the channel permissions that are not allowed by this command."
    
    def BotMissingChannelPerms(self, channel_id: int | None, *perms: discord.Permissions) -> str:
        return "The bot is missing one or more of the channel permissions required to use this command."
    
    def BotHasChannelPerms(self, channel_id: int | None, *perms: discord.Permissions) -> str:
        return "The bot has one or more of the channel permissions that are not allowed by this command."
    
    def UserMissingGuildPerms(self, guild_id: int | None, *perms: discord.Permissions) -> str:
        return "You are missing one or more of the guild permissions required to use this command."
    
    def UserHasGuildPerms(self, guild_id: int | None, *perms: discord.Permissions) -> str:
        return "You have one or more of the guild permissions that are not allowed by this command."
    
    def BotMissingGuildPerms(self, guild_id: int | None, *perms: discord.Permissions) -> str:
        return "The bot is missing one or more of the guild permissions required to use this command."
    
    def BotHasGuildPerms(self, guild_id: int | None, *perms: discord.Permissions) -> str:
        return "The bot has one or more of the guild permissions that are not allowed by this command."
    
    def NotInDM(self) -> str:
        return "This command can only be used through DMs (private messages)."
    
    def InDM(self) -> str:
        return "This command may not be used through DMs (private messages)."
    
    def IsNotUser(self, user_id: int) -> str:
        return "You are not in this command's whitelist."
    
    def IsUser(self, user_id: int) -> str:
        return "You are in this command's blacklist."
    
    def NotInChannel(self, channel_id: int | typing.Iterable[int]) -> str:
        if utils.isiterable(channel_id):
            return f"This command may only be used within the following channels: <#{'>, <#'.join(str(id) for id in channel_id)}>."
        return f"This command may only be used within <#{channel_id}>."
    
    def InChannel(self, channel_id: int | typing.Iterable[int]) -> str:
        if utils.isiterable(channel_id):
            return f"This command may not be used within the following channels: <#{'>, <#'.join(str(id) for id in channel_id)}>."
        return f"This command may not be used within <#{channel_id}>."
    
    def NotInGuild(self, guild_id: int | typing.Iterable[int]) -> str:
        if utils.isiterable(guild_id):
            return f"This command may only be used within the following guilds: {', '.join(str(id) for id in guild_id)}."
        return f"This command may only be used within the guild {guild_id}."
    
    def InGuild(self, guild_id: int | typing.Iterable[int]) -> str:
        if utils.isiterable(guild_id):
            return f"This command may not be used within the following guilds: {', '.join(str(id) for id in guild_id)}."
        return f"This command may not be used within the guild {guild_id}."
    
    def NotInCategory(self, category_id: int | typing.Iterable[int]) -> str:
        if utils.isiterable(category_id):
            return f"This command may only be used within the following categories: <#{'>, <#'.join(str(id) for id in category_id)}>."
        return f"This command may only be used within the category <#{category_id}>."
    
    def InCategory(self, category_id: int | typing.Iterable[int]) -> str:
        if utils.isiterable(category_id):
            return f"This command may not be used within the following categories: <#{'>, <#'.join(str(id) for id in category_id)}>."
        return f"This command may not be used within the category <#{category_id}>."
    
    def IsNotBotOwner(self) -> str:
        return "This command may only be used by the bot owner."
    
    def IsBotOwner(self) -> str:
        return "This command may not be used by the bot owner."
    
    def ChannelIsNotNSFW(self, channel_id: int | None) -> str:
        return "This command may only be used in NSFW channels."
    
    def ChannelIsNSFW(self, channel_id: int | None) -> str:
        return "This command may not be used in NSFW channels."
    
    def IsNotGuildOwner(self, guild_id: int | None) -> str:
        return "This command may only be used by the guild owner."
    
    def IsGuildOwner(self, guild_id: int | None) -> str:
        return "This command may not be used by the guild owner."
    
    def UsernameDoesNotContain(self, substr: str | None) -> str:
        return f"Your username must contain '{substr}'."
    
    def UsernameContains(self, substr: str | None) -> str:
        return f"Your username must not contain '{substr}'."
    
    def MembershipLT(self, seconds: int,
                     alt_exc: commands.CheckFailure = None,
                     alt_seconds: int = None) -> str:
        return self._make_membership_message(exceptions.MembershipLT, seconds,
                                             alt_exc, alt_seconds)
    
    def MembershipGT(self, seconds: int,
                     alt_exc: commands.CheckFailure = None,
                     alt_seconds: int = None) -> str:
        return self._make_membership_message(exceptions.MembershipGT, seconds,
                                             alt_exc, alt_seconds)
    
    def MembershipGE(self, seconds: int,
                     alt_exc: commands.CheckFailure = None,
                     alt_seconds: int = None) -> str:
        return self._make_membership_message(exceptions.MembershipGE, seconds,
                                             alt_exc, alt_seconds)
    
    def MembershipLE(self, seconds: int,
                     alt_exc: commands.CheckFailure = None,
                     alt_seconds: int = None) -> str:
        return self._make_membership_message(exceptions.MembershipLE, seconds,
                                             alt_exc, alt_seconds)

    def __missing__(self, utx: types.utx, exc: Exception
                    ) -> tuple[discord.Embed, list[discord.Attachment | discord.Embed]]:
        error_embed = discord.Embed(description="**An unknown error has "
                                    "occured. The developers have been "
                                    "notified and will attempt to fix the "
                                    "issue as soon as possible. Thank you for "
                                    "your patience.**",
                                    color=constants.EMBED_COLOR__NEG)

        # get exc info
        author = utils.get_author(utx)
        info = textwrap.dedent(f"""
            - ctx.author.id
            + {author.id}
            - ctx.author.name
            + {author.name}
            - ctx.author.display_name
            + {author.display_name}
            - ctx.command.callback.__name__
            + {utx.command.callback.__name__}
            - ctx.command.qualified_name
            + {utx.command.qualified_name}
            - invokation timestamp
            + {datetime.datetime.utcnow().isoformat(timespec='seconds')}"""[1:])
        tb = "".join(traceback.format_exception(exc))

        # ensure we don't break the 4096 character limit, and sacrifice
        # early early traceback if needed. `22` is the number of characters in
        # "```diff\n``````yaml\n```"
        if len(tb) + len(info) + 22:
            tb = f"[!!!]{tb[-(4096 - len(info) - 22 - 5):]}" # less 5 for [!!!]
        
        content = f"```diff\n{info}``````yaml\n{tb}```"
        data = []
        data.append(discord.Embed(description=content, color=constants.EMBED_COLOR__NEG))

        # add additional information
        addl: list = getattr(exc, "__dpy_check_additional_arguments__", None)
        if addl is not None:

            for v in addl:
                if isinstance(v, str):
                    data.append(discord.Embed(description=f"```\n{v}```",
                                              color=constants.EMBED_COLOR__NEG))
                elif isinstance(v, (discord.Attachment, discord.Embed)):
                    data.append(v)
                elif isinstance(v, Exception):
                    data.append(discord.Embed(description=f"```\nERROR: {str(v)}```",
                                              color=constants.EMBED_COLOR__NEG))
                elif isinstance(v, dict):
                    embed_dict = {"color": constants.EMBED_COLOR__NEG}
                    embed_dict.update(v)
                    data.append(discord.Embed.from_dict(embed_dict))

        return error_embed, data


class ErrorHandler:
    """A class used to handle errors raised by `...Check`.
    
    """
    def __init__(self, ids: typing.Iterable[typing.Iterable[int]],
                 attach_to: object = None, formatter: Formatter = ...) -> None:
        """
        Arguments
        ---------
        ids : iterable of iterable of int
            A 2D iterable where each bottom-level iterable contains a channel ID and optionally one
            or more users (as user IDs) to mention during the handling of unknown errors.
        attach_to : object
            If defined, an attribute named `__dpy_check__` will be added to the given object with
            a value of this instance. It can be reacquired through normal means, or with the
            `ErrorHandler.get` static method.
        formatter : Formatter
            If defined, the given formatter instance will be used. Otherwise, a new instance will
            be created.
        
        """
        if attach_to:
            setattr(attach_to, "__dpy_check__", self)
        self.ids = ids
        self.formatter = formatter if formatter != ... else Formatter()

    @staticmethod
    def set_additional(exc: Exception,
                       *additional: discord.Embed | discord.Attachment | Exception | str | dict
                       ) -> None:
        """Set additional arguments that will be processed with the error handler (non-Check
        exceptions only) and sent after the main info embed.

        Arguments
        ---------
        *additional : Embed or Attachment or Exception or str or dict
            If provided an Embed or Attachment, they will be sent directly. If an Exception or str
            is provided, they will be turned into Embeds (wrapped in a code block). If a dict is
            provided, it will be turned into an Embed (with default color matching that of the main
            error message).
        
        """
        addl: list = getattr(exc, "__dpy_check_additional_arguments__", None)
        if addl is None:
            return setattr(exc, "__dpy_check_additional_arguments__", list(additional))
        addl.extend(additional)

    @staticmethod
    def get(obj: object, /, ignore: bool = False) -> "ErrorHandler":
        """Acquire the ErrorHandler attached to `obj`.

        Arguments
        ---------
        obj : object
            The object that has an ErrorHandler instance attached.
        ignore : bool, default=False
            If True, `None` will be returned if no ErrorHandler is found instead
            of raising an error.
        
        """
        if not ignore and not hasattr(obj, "__dpy_check__"):
            raise ValueError("the given object does not have an attached "
                             "ErrorHandler")
        return getattr(obj, "__dpy_check__", None)
    
    @staticmethod
    def placeholder(cmd):
        """Placeholder to be used in classes such as cogs.
        
        """
        if not isinstance(cmd, (commands.Command, app_commands.Command,
                                app_commands.ContextMenu)):
            raise ValueError("The decoration target must be a Command "
                                "instance; one fix may be to ensure this "
                                "decorator is at the top")
        setattr(cmd._callback, "__dpy_check_placeholder__", True)
        return cmd
    
    def resolve_placeholders(self, obj: object) -> None:
        """Resolve any placeholders contained in `obj`.
        
        """
        for name in dir(obj):
            child = getattr(obj, name)

            # skip if child isn't able to be decorated
            # with our decorator anyway
            if not isinstance(child, (commands.Command, app_commands.Command,
                                      app_commands.ContextMenu)):
                continue
            placeholder_present = getattr(child._callback, "__dpy_check_placeholder__", False)
            
            # skip if the given command/menu isn't decorated
            # with a placeholder
            if not placeholder_present:
                continue
            child.on_error = self.error

    async def error(self, *args) -> None:
        """The error handler. Not meant to be called directly, and should
        instead be used for a command or menu's `on_error` event.
        
        """
        # if used within a cog, groupcog, etc, the first argument will
        # be the cog instance
        exc: commands.CheckFailure | app_commands.CheckFailure | commands.CommandInvokeError
        if isinstance(args[0], (commands.Context, discord.Interaction)):
            utx: types.utx = args[0]
            exc = args[1]
        else:
            utx: types.utx = args[1]
            exc = args[2]
        exc_name = exc.__class__.__name__
        sender = utils.get_sender(utx)

        # formats an error embed and sends to the user
        async def send(content: str) -> None:
            embed = discord.Embed(description=f"{self.formatter.error_prefix}{content}"
                                              f"{self.formatter.error_postfix}",
                                  color=constants.EMBED_COLOR__NEG)
        
            await sender(embed=embed)
            return

        # non-check exception with content func present in formatter
        content_func = getattr(self.formatter, f"custom_{exc_name}", None)
        if content_func:
            try:
                return await send(content_func(exc))
            except Exception:
                pass
        
        # non-check exception
        if not isinstance(exc, (commands.CheckFailure, app_commands.CheckFailure)):
            error_embed, data = self.formatter.__missing__(utx, exc.original)
            
            # error embed (sent to user)
            await sender(embed=error_embed)

            # info (sent to error channel)
            client = utils.get_client(utx)
            for channel_id, *mention_ids in self.ids:
                channel = client.get_channel(channel_id)
                if mention_ids:
                    await channel.send(f"<@{'> <@'.join(str(id) for id in mention_ids)}>")
                for value in data:
                    if isinstance(value, discord.Embed):
                        await channel.send(embed=value)
                    elif isinstance(value, discord.Attachment):
                        await channel.send(file=await value.to_file())
                    await asyncio.sleep(0.1) # so as to not overload the API
            return
        
        # check exception with content func present in formatter
        content_func = getattr(self.formatter, exc_name, None)
        if content_func:
            try:
                return await send(content_func(*exc.args[0]))
            except Exception:
                pass
        
        # check exception with no content func present in formatter
        return await send(self.formatter.Generic())
