import argparse
from collections import namedtuple
from datetime import datetime
import re
import traceback
from .utils import strptime
import discord.app_commands
from discord.utils import MISSING
import inspect
from typing import Union
import logging

logger = logging.getLogger('beymax.args')

mention_pattern = re.compile(r'<@\D?(\d+)>')
channel_mention_pattern = re.compile(r'<#(\d+)>')

PLACEHOLDER_NAME = '_placeholder_'

DISCORD_BUILTIN_TYPES = {
    str: discord.AppCommandOptionType.string,
    int: discord.AppCommandOptionType.integer,
    bool: discord.AppCommandOptionType.boolean,
    discord.User: discord.AppCommandOptionType.user,
    discord.Role: discord.AppCommandOptionType.role,
    float: discord.AppCommandOptionType.number
}

for t in list(discord.AppCommandOptionType):
    DISCORD_BUILTIN_TYPES[t] = t

async def dummy_callback(interaction):
    pass

class Command(discord.app_commands.Command):
    def __init__(self, name, description, *, callback, nsfw = False, parent = None, guild_ids = None, auto_locale_strings=False, extras = None):
        super().__init__(name=name, description=description, callback=dummy_callback, nsfw=nsfw, parent=parent, guild_ids=guild_ids, extras=extras, auto_locale_strings=False)
        self._callback = callback
        self._params = callback.__annotations__
        for arg_name, arg in self._params.items():
            if arg.name == PLACEHOLDER_NAME:
                arg.name = arg_name

        try:
            self.binding = callback.__self__
            self._callback = callback = callback.__func__
        except AttributeError:
            self.binding = None
    
    def subscribe_command(self, bot):
        @bot.subscribe('cmd:{}'.format(self.name))
        async def run_cmd(bot, event, interaction, **kwargs):
            return await self._callback(interaction, **kwargs)

    async def on_error(self, interaction, error):
        if isinstance(error, Transformer.InvalidInputForTransformation):
            await interaction.response.send_message(
                "Your input didn't quite match what I was expecting: ".format(error.args[0]),
                ephemeral=True
            )

    async def _do_call(self, interaction, params):
        logger.info("Invoked command {} with {} arguments".format(
            self.name,
            len(params)
        ))
        logger.debug("Starting command dispatch {}".format(params))
        try:
            # return await super()._do_call(interaction, params)
            return await (interaction.client.dispatch('cmd:{}'.format(self.name), interaction, **params))
        except:
            logger.error("Exception in command", exc_info=True)
            raise
        finally:
            logger.debug("Command complete")

class PrebuiltException(Exception):
    def __init__(self, message):
        self.message = message

Argtuple = namedtuple('Arg', ['args', 'kwargs'])

class Transformer(discord.app_commands.Transformer):

    class InvalidInputForTransformation(discord.app_commands.AppCommandError):
        pass

class DollarType(Transformer):
    async def transform(self, interaction, value, /):
        if not (isinstance(value, str) and value.startswith('$')):
            raise Transformer.InvalidInputForTransformation("Value {} not in correct format for DollarType".format(value))

class DateType(Transformer):
    async def transform(self, interaction, value, /):
        try:
            return strptime(value)
        except Exception as e:
            raise Transformer.InvalidInputForTransformation("Value {} not in correct datestamp format".format(value)) from e

class ListType(Transformer):
    def __init__(self, baseType, delimiter=',', *args, min_values=1, max_values=None, **kwargs):
        super().__init__(*args, **kwargs)
        if baseType in discord.app_commands.transformers.BUILT_IN_TRANSFORMERS:
            baseType = discord.app_commands.transformers.BUILT_IN_TRANSFORMERS[baseType]
        self.baseType = baseType
        self.delimiter = delimiter
        self.min_values = min_values
        self.max_values = max_values
    
    async def transform(self, interaction, value, /):
        try:
            values = [v.strip() for v in value.split(self.delimiter)]
            if self.min_values is not None:
                assert len(values) >= self.min_values
            elif self.max_values is not None:
                assert len(values) <= self.max_values
            return [
                await self.baseType.transform(interaction, val)
                for val in values
            ]
        except Exception as e:
            raise Transformer.InvalidInputForTransformation("Value {} not in correct list format".format(value)) from e

UserOrMemberType = Union[discord.User, discord.Member]

# Pattern 1) Args return a command parameter. Our Command Type manually updates self._params etc with meaningful info
# Pattern 2) Args return a Transformer type. This misses out on descriptions
class Arg(discord.app_commands.transformers.CommandParameter):

    def __init__(self, name=None, description = MISSING, required = True, default = MISSING, choices = MISSING, type = str, min_value = None, max_value = None):
        self._transformed_type = None
        if isinstance(type, discord.app_commands.Transformer):
            self._transformed_type = type
        elif inspect.isclass(type) and issubclass(type, discord.app_commands.Transformer):
            self._transformed_type = type()
        elif type in discord.app_commands.transformers.BUILT_IN_TRANSFORMERS:
            self._transformed_type = discord.app_commands.transformers.BUILT_IN_TRANSFORMERS[type]
        if name is not None:
            logger.warning("Argument with overriden name may cause command failures if declared name does not match function parameter name")
        if isinstance(choices, dict):
            choices = [
                discord.app_commands.Choice(name=key, value=value)
                for key, value in choices.items()
            ]
        elif isinstance(choices, list):
            choices = [
                item if isinstance(item, discord.app_commands.Choice) else discord.app_commands.Choice(name=str(item), value=str(item))
                for item in choices
            ]
        super().__init__(
            name=name if name is not None else PLACEHOLDER_NAME,
            description=description,
            required=required,
            default=default,
            choices=choices,
            type=DISCORD_BUILTIN_TYPES[type] if self._transformed_type is None else self._transformed_type.type,
            min_value=min_value,
            max_value=max_value,
            _annotation=discord.app_commands.transformers.BUILT_IN_TRANSFORMERS[type] if self._transformed_type is None else self._transformed_type
        )