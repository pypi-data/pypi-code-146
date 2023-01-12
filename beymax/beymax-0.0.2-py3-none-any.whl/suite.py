import logging
from textwrap import wrap
from unittest.mock import patch
import sqlalchemy.orm
import discord.app_commands
from discord.utils import MISSING

logger = logging.getLogger('beymax.core.suite')

class Schema(object):
    pass

class CommandSuite(object):
    def __init__(self, name, group_description=None, group_name=None):
        self.name = name
        self.bot = None
        self.commands = []
        self.tasks = []
        self.special = []
        self.subscriptions = []
        self.migrations = []
        self.channels = []
        self.context = []
        self.schema = Schema()
        self.dependencies = []
        self.tables = []
        self.command_group = None
        
        if group_description is not None:
            logger.warning("Grouping commands in suite {}. Command permissions are fully grouped, so ensure it's okay to lose granular control".format(self.name))
            if group_name is None:
                group_name = name.lower().replace(' ', '_')[:32]
                logger.debug("A group description was provided with no name. Auto-generating name for suite {}".format(name))
            self.command_group = discord.app_commands.Group(
                name=group_name,
                description=group_description,
                default_permissions=discord.Permissions(use_application_commands=False)
            )
    
    def add_dependency(self, suite):
        self.dependencies.append(suite)

    def table(self, cls):
        # Maybe no need for a schema event if the declarative base class is just globally available
        @self.subscribe('schema', once=True)
        async def add_table(bot, evt, db):
            class Table(db.base, cls):
                pass
                # if hasattr(cls, '_relationships_'):
                #     for attr, val in cls._relationships_.items():
                #         setattr(Table, attr, sqlalchemy.orm.relationship(val))

            setattr(self.schema, cls.__name__, Table)
            cls._table = Table
        cls.table = lambda : cls._table
        cls._table = None
        self.tables.append(add_table)
        return cls
    
    async def debug_schema(self, db):
        for table in self.tables:
            await table(None, None, db)

    def attach(self, bot):
        """
        Attaches this command suite to the given bot
        """
        if self.bot == bot or self.name in bot.suites:
            logger.info("Skipping suite {} (already enabled)".format(self.name))
            
        logger.info(
            "Enabling command suite {}: {} commands, {} context menus, {} tasks, {} special message handlers, {} event handlers, {} db migrations, {} channel references".format(
                self.name,
                len(self.commands),
                len(self.context),
                len(self.tasks),
                len(self.special),
                len(self.subscriptions),
                len(self.migrations),
                len(self.channels)
            )
        )

        for dependency in self.dependencies:
            dependency.attach(bot)

        self.bot = bot
        bot.suites[self.name] = self
        for channel in self.channels:
            bot.reserve_channel(channel)

        for migration in self.migrations:
            bot.migration(migration['key'])(migration['function'])

        for subscription in self.subscriptions:
            bot.subscribe(
                subscription['event'],
                condition=subscription['condition'],
                once=subscription['once']
            )(subscription['function'])

        for special in self.special:
            bot.add_special(special['checker'], flavor=special['flavor'])(special['function'])

        for task in self.tasks:
            if task['legacy']:
                bot.add_legacy_task_chain(
                    task['seconds']
                )(task['function'])
            else:
                bot.add_task(
                    task['seconds'], minutes=task['minutes'], 
                    hours=task['hours'], times=task['times'], 
                    count=task['count'], reconnect=task['reconnect']
                )(task['function'])

        for command in self.commands:
            bot.add_command(command['command'], *command['args'], command_suite_group=self.command_group, **command['kwargs'])(command['function'])
        
        for ctx in self.context:
            bot.add_context(ctx['name'], *ctx['args'], **ctx['kwargs'])(ctx['function'])
        
        if self.command_group is not None:
            @bot.subscribe('before:command-init', once=True)
            async def add_command_group(bot, event):
                if len(self.command_group.commands):
                    bot.tree.add_command(
                        self.command_group,
                        guild=bot.primary_guild if bot.primary_guild is not None else MISSING
                    )

    def add_command(self, command, *args, **kwargs):
        def wrapper(func):
            self.commands.append(
                {
                    'command': command,
                    'args': args,
                    'kwargs': kwargs,
                    'function': func
                }
            )
            return func
        return wrapper
    
    def add_context(self, name, *args, **kwargs):
        def wrapper(func):
            self.context.append({
                'name': name,
                'args': args,
                'kwargs': kwargs,
                'function': func
            })
            return func
        return wrapper

    def add_task(self, seconds=None, *, minutes=None, hours=None, times=None, count=None, reconnect=None, legacy=False):
        if legacy and not (minutes is None and hours is None and times is None and count is None and reconnect is None):
            raise ValueError("Cannot create legacy task chain with complex scheduling argumentsß")
        def wrapper(func):
            self.tasks.append(
                {
                    'seconds': seconds,
                    'minutes': minutes,
                    'hours': hours,
                    'times': times,
                    'count': count,
                    'reconnect': reconnect,
                    'function': func,
                    'legacy': legacy
                }
            )
            return func
        return wrapper

    def add_special(self, checker, flavor='legacy'):
        def wrapper(func):
            self.special.append(
                {
                    'checker': checker,
                    'function': func,
                    'flavor': flavor
                }
            )
            return func
        return wrapper

    def subscribe(self, event, *, condition=None, once=False):
        def wrapper(func):
            self.subscriptions.append(
                {
                    'event': event,
                    'function': func,
                    'condition': condition,
                    'once': once
                }
            )
            return func
        return wrapper

    def migration(self, key):
        """
        Migrations run after the bot has connected to discord and has readied.
        Discord interactions will be ready
        """
        def wrapper(func):
            self.migrations.append(
                {
                    'key': key,
                    'function': func
                }
            )
            return func
        return wrapper

    def reserve_channel(self, name):
        """
        Call to declare a channel reference. The bot configuration can then map
        this reference to an actual channel. By default all undefined references
        map to general
        Arguments:
        name : A string channel reference to reserve
        """
        self.channels.append(name)
