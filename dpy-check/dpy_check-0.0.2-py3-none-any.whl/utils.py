"""General utilities.

:copyright: (c) 2022-present Tanner B. Corcoran
:license: MIT, see LICENSE for more details.
"""

__author__ = "Tanner B. Corcoran"
__license__ = "MIT License"
__copyright__ = "Copyright (c) 2022-present Tanner B. Corcoran"


from . import types
from discord.ext import commands
import discord


def get_author(utx: types.utx) -> discord.User | discord.Member:
    return utx.author if isinstance(utx, commands.Context) else utx.user


def get_client(utx: types.utx) -> commands.Bot | discord.Client:
    return utx.bot if isinstance(utx, commands.Context) else utx.client


def get_me(utx: types.utx) -> discord.Member | discord.ClientUser:
    return utx.me if isinstance(utx, commands.Context) else utx.guild.me


def get_sender(utx: types.utx):
    if isinstance(utx, commands.Context):
        return utx.send
    if utx.response.is_done():
        return utx.followup.send
    return utx.response.send_message


def isiterable(obj: object) -> bool:
    try:
        iter(obj)
    except TypeError:
        return False
    return True
