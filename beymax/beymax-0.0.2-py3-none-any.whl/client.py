from multiprocessing import Event
import pdb
from .utils import DBView, ensure_localtz, getname, standard_intents, TIMESTAMP_FORMAT, strptime, trim, as_bytes, DATABASE
from .args import Command, Arg
from .suite import CommandSuite
from .db import DBConnection
import discord
from discord.utils import MISSING
import discord.app_commands
import discord.ext.tasks
import discord.ui
import asyncio
import time
import os
import yaml
from math import ceil
import sys
import shlex
from functools import wraps, partial
import re
import traceback
import warnings
import json
from datetime import datetime, timedelta
from emoji import emojize
import logging
import sqlalchemy as alchemy
import pickle
from contextvars import ContextVar
import base64

logger = logging.getLogger('beymax.core.client')
background_tasks = set()

# mention_pattern = re.compile(r'<@.*?(\d+)>')

class EventChain(object):
    def __init__(self, eventname):
        self.name = eventname
        self.cancelled = False
    
    def cancel(self):
        self.cancelled = True
        logger.info("Event {} cancelled".format(self.name))
    
    async def run_listeners(self, before=None, during=None, after=None):
        total_listeners =  (len(before) if before is not None else 0) + (len(during) if during is not None else 0) + (len(after) if after is not None else 0)
        if total_listeners <= 0:
            return
        logger.info("Running {} listeners for event {}".format(
           total_listeners,
            self.name
        ))
        if before is not None:
            logger.debug("before:{}".format(self.name))
            await asyncio.gather(*before, return_exceptions=True)
        if not (self.cancelled or during is None):
            logger.debug("during:{}".format(self.name))
            await asyncio.gather(*during, return_exceptions=True)
        if not (self.cancelled or after is None):
            logger.debug("after:{}".format(self.name))
            await asyncio.gather(*after, return_exceptions=True)

class Client(discord.Client):
    """
    Beymax Client
    This Client class adds an additional layer on top of the standard discord api.
    Beymax's API is bot-focused with features like commands and background tasks.
    This Client is geared towards custom single-server bots, although it can
    serve multiple servers
    """
    def __init__(self, *args, status=discord.Status.dnd, activity=discord.Game(name="Starting up, please wait..."), **kwargs):
        super().__init__(*args, status=status, activity=activity, **kwargs)
        self.nt = 0
        self.configuration = {}
        self.primary_guild = None
        self.channel_references = {} # reference name -> channel name/id
        self.event_listeners = {} # event name -> [listener functions (self, event)]
        # changed to set in favor of event API
        self.event_preemption = {} # event name -> counter for preempting beymax-level events
        self.commands = {} # !cmd -> docstring. Functions take (self, message, content)
        self.ignored_users = set()
        self.tasks = {} # taskname (auto generated) -> (current exec interval, permanent exec interval)
        self.special = [] # list of (check, handler)
        self.suites = {}
        self.channel_lock = asyncio.Lock()
        config_path = os.environ.get('BEYMAX_CONFIG_PATH', 'config.yml')
        if os.path.exists(config_path):
            with open(config_path) as reader:
                self.configuration = yaml.load(reader, Loader=yaml.SafeLoader)
        self.command_prefix = self.config_get('prefix', default='!')
        self.tree = discord.app_commands.CommandTree(self)

        self.db = DBConnection(self.config_get('database', 'url'))

        # Add the core api tasks and event subscriptions
        APIEssentials.attach(self)

    
    async def get_value(self, key, default=None):
        async with self.db.session() as session:
            result = (await session.execute(
                alchemy.select(APIEssentials.schema.KeyValue).where(
                    APIEssentials.schema.KeyValue.key == key
                )
            )).scalars().first()
            if result:
                return result.value
            return default

    async def set_value(self, key, value):
        async with self.db.session() as session:
            result = (await session.execute(
                alchemy.select(APIEssentials.schema.KeyValue).where(
                    APIEssentials.schema.KeyValue.key == key
                )
            )).scalars().first()
            if result:
                result.value = value
            else:
                session.add_all([
                    APIEssentials.schema.KeyValue(key=key, value=value)
                ])
            await session.commit()

    async def setup_hook(self):
        await self.db.__aenter__()
    
    def add_context(self, name, nsfw=False, auto_locale_strings=True):
        def wrapper(func):

            @self.subscribe('before:command-init', once=True)
            async def register_context(self, evt):                
                

                @self.tree.context_menu(name=name, nsfw=nsfw, guild=self.primary_guild if self.primary_guild is not None else MISSING)
                @wraps(func)
                async def context_wrapper(interaction, *args, **params):
                    logger.info("Invoking context manager {}".format(name))
                    try:
                        return await (interaction.client.dispatch('ctx:{}'.format(name), interaction, *args, **params))
                    except:
                        logger.error("Exception in context manager", exc_info=True)
                        raise
                    finally:
                        logger.debug("Context complete")

                
                # Impossible to set fail-safe defaults
                context_wrapper.default_permissions = discord.Permissions(use_application_commands=True)
                
                @self.subscribe('ctx:{}'.format(name))
                async def run_context(bot, event, interaction, *args, **params):
                    print(interaction, args, params)
                    return await func(interaction, *args, **params)

            return func
        
        return wrapper


    def add_command(self, command, description=None, nsfw=False, parent=None, auto_locale_strings=True, command_suite_group=None): #decorator. Attaches the decorated function to the given command(s)
        """
        Decorator. Registers the given function as the handler for the specified command.
        Arguments:
        command : The name of the command. This will become a new slash command
        description : The command description. If none, it will be parsed from the command docstring
        nsfw : Whether or not to flag the command as NSFW. The command will only function in NSFW channels
        parent : A CommandGroup
        auto_locale_strings : If True (default) all translatable strings will be converted to locale-specific strings

        The decorated function must be a coroutine (async def) and use one of the following call signatures:
        The first argument will be an Interaction object for the interaction which triggered this command
        Remaining arguments will be user inputs parsed into appropriate types. ALL arguments (other than the interaction)
        must be annotated with an appropriate discord type annotation or a beymax.args.Arg() object

        Note: The docstring of command functions is used as the command's help text.
        """
        def wrapper(func):
            nonlocal description
            if description is None:
                if func.__doc__ is None:
                    raise ValueError("A description must be set either as a add_command argument or on the command handler's docstring")
                else:
                    description = trim(func.__doc__)
            
            if len(description) < 1 or len(description) > 100:
                raise ValueError("Description for command {} must be between 1 and 100 characters".format(command))
            
            cmd = Command(
                name=command,
                description=description,
                callback=func,
                nsfw=nsfw,
                parent=parent,
                guild_ids=[self.primary_guild.id] if self.primary_guild is not None else None,
                auto_locale_strings=auto_locale_strings,
            )
            # I would like to default to off, but that's apparently impossible to override @everyone
            cmd.default_permissions = discord.Permissions(use_application_commands=True)
            cmd.subscribe_command(self)

            if command_suite_group is None:

                @self.subscribe('before:command-init', once=True)
                async def register_command(self, evt):

                    self.tree.add_command(
                        cmd,
                        guild=self.primary_guild if self.primary_guild is not None else MISSING
                    )
            else:
                command_suite_group.add_command(cmd)
           
            return func

        return wrapper

    def add_task(self, seconds=None, *, minutes=None, hours=None, times=None, count=None, reconnect=None): #decorator. Sets the decorated function to run on the specified interval
        """
        Decorator. Sets the decorated function to run on the specified interval.
        Arguments:
        interval : The interval in which to run the function, in seconds

        The decorated function must be a coroutine (async def) and take only the bot object as an argument
        """
        if times is None:
            times = MISSING
        def wrapper(func):
            taskname = 'task:'+func.__name__
            if taskname in self.tasks:
                raise NameError("This task already exists! Change the name of the task function")

            self.tasks[taskname] = {
                'seconds': seconds, 
                'minutes': minutes,
                'hours': hours,
                'times': times,
                'temp_interval': None,
                'count_remaining': count
            }

            @discord.ext.tasks.loop(seconds=seconds, minutes=minutes, hours=hours, time=times, count=count, reconnect=reconnect)
            async def run_task():
                if self.tasks[taskname]['temp_interval'] is not None:
                    self.tasks[taskname]['task'].change_interval(
                        seconds=self.tasks[taskname]['temp_interval']['seconds'],
                        minutes=self.tasks[taskname]['temp_interval']['minutes'],
                        hours=self.tasks[taskname]['temp_interval']['hours'],
                        time=self.tasks[taskname]['temp_interval']['times']
                    )
                    self.tasks[taskname]['temp_interval'] = None
                async with self.db.session() as session:
                    result = (await session.execute(
                        alchemy.select(APIEssentials.schema.Task).where(
                            APIEssentials.schema.Task.name == taskname
                        )
                    )).scalars().first()
                    if result is not None:
                        result.date = discord.utils.utcnow().timestamp()
                    else:
                        session.add_all([
                            APIEssentials.schema.Task(name=taskname, date=discord.utils.utcnow().timestamp())
                        ])
                    await session.commit()
                if self.tasks[taskname]['count_remaining'] is not None:
                    self.tasks[taskname]['count_remaining'] -= 1
                self.dispatch(taskname)
            
            @self.subscribe(taskname) # This is separated into runtask->task only for triggers/hooks on the task event
            async def task_wrapper(_1, _2):
                logger.debug("Starting task {}".format(taskname))
                await func(self)
                logger.info("Task complete {}".format(taskname))
            
            self.tasks[taskname]['task'] = run_task

            return run_task
        return wrapper

    def update_interval(self, taskname, seconds=None, *, minutes=None, hours=None, times=None, permanent=True):
        if times is None:
            times = MISSING
        if not taskname.startswith('task:'):
            taskname = 'task:{}'.format(taskname)
        if taskname not in self.tasks:
            raise NameError("No such task", taskname)
        if permanent:
            self.tasks[taskname]['seconds'] = seconds
            self.tasks[taskname]['minutes'] = minutes
            self.tasks[taskname]['hours'] = hours
            self.tasks[taskname]['times'] = times
        else:
            self.tasks[taskname]['temp_interval'] = {
                'seconds': seconds,
                'minutes': minutes,
                'hours': hours,
                'times': times
            }
        self.tasks[taskname]['task'].change_interval(
            seconds=seconds,
            minutes=minutes,
            hours=hours,
            time=times
        )
        logger.info(
            "Task {} new interval: {}s {}m {}h {}abs times {}".format(
                taskname,
                seconds,
                minutes,
                hours,
                times,
                '(persistent)' if permanent else '(temporary)'
            )
        )
    
    def add_legacy_task_chain(self, seconds):
        if seconds < 30:
            warnings.warn("Legacy task chains cannot guarantee a granularity less than 30 seconds")
        def wrapper(func):
            taskname = 'task:'+func.__name__
            if taskname in self.tasks:
                raise NameError("This task already exists! Change the name of the task function")

            self.tasks[taskname] = {
                'seconds': seconds, 
                'minutes': None,
                'hours': None,
                'times': None,
                'temp_interval': None,
                'count_remaining': None
            }

            @self.subscribe('after:schema', once=True)
            async def verify_task_schedule(bot, *args):
                async with bot.db.session() as session:
                    task_schedule = (await session.execute(
                        alchemy.select(APIEssentials.schema.FutureDispatch).where(
                            (APIEssentials.schema.FutureDispatch.event == taskname)
                            & (APIEssentials.schema.FutureDispatch.date < time.time())
                        )
                    )).scalars().first()
                    if task_schedule is None:
                        logger.info("Scheduling future task chain {}".format(taskname))
                        await bot.dispatch_future(
                            seconds,
                            taskname
                        )
            
            @self.subscribe(taskname) # This is separated into runtask->task only for triggers/hooks on the task event
            async def task_wrapper(*args):
                logger.debug("Starting task {}".format(taskname))
                try:
                    await func(self)
                    logger.info("Task complete {}".format(taskname))
                finally:
                    await verify_task_schedule(self)
        return wrapper   
            

    def add_special(self, check, flavor='blind'): #decorator. Sets the decorated function to run whenever the check is true
        """
        Decorator. Sets the decorated function to run whenever the given check function is True.
        Arguments:
        check : A function which takes a message argument and returns True if the decorated function should be run

        The decorated function must be a coroutine (async def) and take the three following arguments:
        * The bot object
        * The message object
        * A list of lowercased, whitespace delimited strings

        Note: Special message handlers are exclusive. The first one with a matching
        condition will be executed and no others
        """
        # NOTE: If exclusivity is not required, just use subscribe(after:message)
        def wrapper(func):
            event = 'special:{}'.format(func.__name__)
            if event in self.event_listeners:
                raise NameError("Special handler already defined")
            # Ugly lambda function: parse out and drop the event argument
            if flavor == 'legacy':
                def flavor_check(slf, e, msg):
                    return slf.intents.message_content and len(msg.content)
            elif flavor == 'blind':
                def flavor_check(slf, e, msg):
                    return True
            elif flavor == 'modern':
                def flavor_check(slf, e, msg):
                    return len(msg.content)
            self.subscribe(event, condition=flavor_check)(lambda s,e,*a,**k: func(s,*a,**k)) # If we add the condition we can double check
            self.special.append((check, event))
            return func
        return wrapper

    async def dispatch_future(self, when, event, *args, **kwargs):
        """
        Schedule the given event to be dispatched at a time in the future.
        When can be a (timezone aware) datetime object, timedelta object, or integer (interpreted as seconds in the future).
        Event should be the string name of an event to dispatch.
        Remaining arguments will be passed to the event handler on dispatch.
        Note: Arguments and keyword arguments must be serializable.
        To save discord objects, use DB serializers (planned)
        """
        if isinstance(when, int):
            when = discord.utils.utcnow() + timedelta(seconds=when)
        elif isinstance(when, timedelta):
            when = discord.utils.utcnow() + when
        elif not isinstance(when, datetime):
            raise TypeError("When must be a datetime, timedelta, or int object, not {}".format(type(when)))
        logger.info("Scheduled event {} to run in {} seconds".format(
            event,
            (when - discord.utils.utcnow()).total_seconds()
        ))
        async with self.db.session() as session:
            session.add_all([
                APIEssentials.schema.FutureDispatch(
                    date=when.timestamp(),
                    event=event,
                    pickled_args=base64.b64encode(pickle.dumps(args)).decode(),
                    pickled_kwargs=base64.b64encode(pickle.dumps(kwargs)).decode(),
                )
            ])
            await session.commit()
        self.update_interval(
            'check_future_dispatch',
            # Update the next check_future_dispatch invocation to take place ASAP
            # task runner will trigger in at most 30 seconds
            # cfd will run and self-update its interval to best match the next dispatch
            1,
            permanent=False
        )

    def migration(self, key):
        """
        Migrations run after the bot has connected to discord and has readied.
        Discord interactions will be ready
        """
        def wrapper(func):
            @self.subscribe('migration', once=True)
            async def run_migration(self, _):
                # check migration
                async with self.db.session() as session:
                    result = (await session.execute(
                        alchemy.select(APIEssentials.schema.Migration).where(
                            APIEssentials.schema.Migration.key == key
                        )
                    )).scalars().first()
                    if result is None:
                        logger.info("Running migration {}".format(key))
                        DBView.migration_state.set(True)
                        try:
                            await func(self)
                        except FileNotFoundError:
                            logger.info("Unable to locate legacy database file. Skipping migration {} and marking as complete".format(key))
                        except:
                            logger.error("Database migration {} failed".format(key))
                            raise
                        finally:
                            DBView.migration_state.set(False)
                        session.add_all([
                            APIEssentials.schema.Migration(key=key, date=discord.utils.utcnow())
                        ])
                        await session.commit()
        return wrapper

    def subscribe(self, event, *, condition=None, once=False): # decorator. Sets the decorated function to run on events
        """
        Decorator. Sets the decorated function to be run whenever the given event
        is dispatched.
        Arguments:
        event : A string argument name. WHen that argument is dispatched, the decorated function will run
        condition: Optional condition run with the same arguments as the event. If true, subscriber is run
        once: If true, subscriber will unsubscribe after running

        Note: If a condition is set and once is true, but the listener raises an exception, it will still unsubscribe

        The decorated function must be a coroutine (async def). The function must take
        the event name as the first argument, and any additional arguments/keyword arguments
        are determined by the arguments to the dispatch() function
        """
        # event functions should take the event, followed by expected arguments
        def wrapper(func):
            if str(event) not in self.event_listeners:
                self.event_listeners[str(event)] = []

            async def handle_event(*args, **kwargs):
                try:
                    if condition is None or condition(*args, **kwargs):
                        if once:
                            func.unsubscribe(event)
                        return await func(*args, **kwargs)
                except:
                    await self.trace()
                    logger.error("Unhandled exception in event listener for {}".format(event))
                    raise

            handle_event.orig = id(func)

            self.event_listeners[str(event)].append(handle_event)
            # func.unsubscribe will unsubscribe the function from the event
            # calling without args unsubscribes from the most recent event that this
            # function was subscribed to. An event can be specified to unsubscribe
            # from a specific event, if the function was subscribed to several

            def unsubscribe(evt=event):
                if evt in self.event_listeners:
                    for handler in self.event_listeners[evt]:
                        if handler.orig == id(func):
                            self.event_listeners[evt] = [
                                hdl
                                for hdl in self.event_listeners[evt]
                                if hdl.orig != id(func)
                            ]
                            return
                logger.warning("Event handler {} already unsubscribed from {}".format(func, evt))

            # func.unsubscribe = lambda x=str(event):self.event_listeners[x].remove(handle_event)
            func.unsubscribe = unsubscribe
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
        # creates a channel reference by that name
        # channel references can be changed in configuration
        self.channel_references[name] = None

    def fetch_channel(self, name):
        """
        Fetch the channel object for a given reference name. If the reference is
        undefined, it returns general
        Arguments:
        name : A string channel reference to lookup
        """
        channel = self.channel_references[name] if name in self.channel_references else None
        if channel is None:
            return self._general
        return channel

    def enableSuites(self, *suites):
        """
        Enables all the given command suites
        Arguments:
        *suites : One or more CommandSuites
        """
        for suite in suites:
            suite.attach(self)
        return self
    
    def get_suite(self, suite):
        return self.suites[suite]

    def strip_prefix(self, command):
        """
        Returns a string with the command prefix removed.
        Arguments:
        command : A string to remove the command prefix from
        """
        if command.startswith(self.command_prefix):
            return command[len(self.command_prefix):]
        return command

    def dispatch(self, event, *args, manual=False, **kwargs):
        """
        Manually dispatches an event (may be used to trigger tasks, commands, etc programatically).
        Arguments:
        event : The string event name to dispatch
        *args : Arguments to provide to the event handler
        manual : (Optional) If True, do not attempt to dispatch before: and after: events
        **kwargs : Keyword arguments to provide to the event handler

        By default, when dispatch is called:
        * Run any functions subscribed to before:{event}
        * Run any functions subscribed to the event in the base class (discord.Client)
        * Run any functions subscribed to the event
        * Run any functions subscribed to after:{event}
        """
        self.nt += 1
        chain = EventChain(event)
        if not manual:
            
            super().dispatch(event, *args, **kwargs)
            return asyncio.create_task(
                chain.run_listeners(
                    before=self.prepare_listeners('before:{}'.format(event), chain, *args, **kwargs),
                    during=self.prepare_listeners(event, chain, *args, **kwargs),
                    after=self.prepare_listeners('after:{}'.format(event), chain, *args, **kwargs)
                )
            )
        else:
           return asyncio.create_task(
                chain.run_listeners(
                    during=self.prepare_listeners(event, chain, *args, **kwargs),
                )
            )

    def prepare_listeners(self, event, chain, *args, **kwargs):
        """
        Called internally. Sets the internal event loop to run event handlers for
        a given event
        """
        if event in self.event_preemption and self.event_preemption[event] > 0:
            # If this event is currently being preempted, do not alert listeners
            return []
        if event not in self.event_listeners:
            return []
        return [
            listener(self, chain, *args, **kwargs)
            for listener in self.event_listeners[event]
        ]


    def config_get(self, *keys, default=None):
        """
        Retrieve a given key from the configuration. A multiple keys may be given to retrieve a nested value.
        Arguments:
        *keys : List of nested keys to read from the configuration
        default : (Optional) The fallback value to return if the requested key path does not exist or is undefined. Defaults to None
        """
        obj = self.configuration
        for key in keys:
            try:
                if key in obj:
                    obj = obj[key]
                else:
                    return default
            except TypeError:
                return default
        return obj

    async def trace(self, send=True, channel=None):
        """
        Coroutine. Prints a stack trace to the console, and optionally sends it to the registered
        bugs channel
        Arguments:
        send : (Optional) If True (the default) post the stack trace to the bugs channel
        """
        x,y,z = sys.exc_info()
        if x is None and y is None and z is None:
            msg = traceback.format_stack()
            traceback.print_stack()
            logger.debug("Manual stack trace", stack_info=True)
        else:
            msg = traceback.format_exc()
            logger.debug("Exception stack trace", exc_info=True)
        if isinstance(msg, list):
            msg = ''.join(msg)
        if send and self.config_get('send_traces'):
            await (self.fetch_channel('dev') if channel is None else channel).send(
                '```{}```'.format(msg[-3990:])
            )

    async def shutdown(self):
        """
        Coroutine. Use this function for a clean shutdown.
        Dispatches the 'cleanup' event, waits for all tasks to complete, then disconnects
        the bot
        """
        await self.change_presence(status=discord.Status.offline)
        tasks = self.dispatch('cleanup')
        logger.info("Waiting for cleanup tasks to complete")
        await tasks
        await self.close()
        await self.db.__aexit__(None, None, None)

    async def send_rich_message(self, destination, *, content=None, author=None, author_url=None, author_icon_url=None, title=None, description=None, colour=None, footer=None, image=None, thumbnail=None, __video=None, url=None, reference=None, mention_author=True):
        """
        Coroutine. Send a message with rich content.
        Arguments:
        destination : A channel or user object to specify where to send the message.
        content (optional): Text to display above the rich embed
        author (optional): Creator. If a User object is passed, this will use the
        user's nickname or username. If a string is passed, the author name will be set to that string
        author_url (optional): Link to embed in the author's name
        author_icon_url (optional): Link to the author's icon. If this is None and
        author is a user object, this will use the user's avatar.
        title (optional): Bold title displayed below author
        description (optional): Main embed content
        colour (optional): Discord color object for sidebar
        footer (optional): Small text to display below embedded content
        image (optional): URL for an image to display
        thumbnail (optional): URL for thumbnail to display in the top right
        ~~video (optional): URL for video to embed~~
        url (optional): Large link to place in center of embed
        """
        if isinstance(author, Client):
            author = author.user

        def apply_kwargs(func, **kwargs):
            return func(**{k:v for k,v in kwargs.items() if v is not None})

        embed = apply_kwargs(discord.Embed, colour=colour, title=title, url=url, description=description)
        if author_icon_url is None and isinstance(author, discord.abc.User):
            author_icon_url = 'https://cdn.discordapp.com/avatars/{}/{}'.format(
                author.id,
                author.default_avatar if author.avatar is None else author.avatar
            )
        if isinstance(author, discord.abc.User):
            author = getname(author)
        if author is not None or author_url is not None or author_icon_url is not None:
            embed = apply_kwargs(embed.set_author, name=author, url=author_url, icon_url=author_icon_url)
        if footer is not None:
            embed = embed.set_footer(text=footer)
        if image is not None:
            embed = embed.set_image(url=image)
        if thumbnail is not None:
            embed = embed.set_thumbnail(url=thumbnail)
        return await destination.send(content=content, embed=embed, reference=reference, mention_author=mention_author)


    def get_user(self, reference, *guilds):
        """
        Gets a user object given a form of reference. Optionaly provide a subset of guilds to check
        Arguments:
        reference : A string reference which can either be a user's id or a username to identify a user
        *guilds : A list of guilds to check. By default, this function checks the primary_guild, then all others

        Checks guilds for a user based on id first, then username. Returns the first match
        """
        if not self.intents.members:
            logger.warning("members intent is not enabled. Consider using client.fetch_member() instead")
        if not len(guilds):
            guilds = list(self.guilds)
            if self.primary_guild is not None:
                guilds = [self.primary_guild]
        if isinstance(reference, int):
            for guild in guilds:
                result = guild.get_member(reference)
                if result is not None:
                    return result
        elif isinstance(reference, str):
            for guild in guilds:
                result = guild.get_member_named(reference)
                if result is not None:
                    return result
        elif reference is None:
            return None
        else:
            raise TypeError("Unacceptable reference type {}".format(type(reference)))
    
    async def fetch_user_or_member(self, user_id, guild_id=None):
        if guild_id is not None:
            guild = self.get_guild(guild_id)
            if guild is not None:
                return await guild.fetch_member(user_id)
        return await self.fetch_user(user_id)


    def getid(self, username):
        """
        Gets the id of a user based on a reference.
        Arguments:
        username : A reference which may be the full discriminated username or their id
        """
        #Get the id of a user from an unknown reference (could be their username, fullname, or id)
        result = self.get_user(username)
        if result is not None:
            if result.id != username and '#' not in username:
                raise NameError("Username '%s' not valid, must containe #discriminator" % username)
            return result.id
        raise NameError("Unable to locate member '%s'. Must use a user ID, username, or username#discriminator" % username)

    async def on_message(self, message):
        """
        Coroutine. Default handler for incomming messages. Do not override.
        Immediately skips message handling and returns if:
        * The message was sent by this bot
        * The message was sent in a DM by a user who does not have any guilds in common with this bot
        * The message was sent by a user in this bot's ignore list

        Splits the message content by whitespace (or the shlex parser if enabled)

        If the first word starts with the command prefix and is in the list of registered
        commands, dispatch the command handler, which checks permissions then runs the command

        Otherwise, check if any registered special functions should run on this message

        If you wish to add additional handling for messages, use @bot.subscribe('message').
        """
        if message.author == self.user:
            return
        if self.get_user(message.author.id) is None:
            #User is not a member of any known guild
            #silently ignore
            return

        if message.author.id in self.ignored_users:
            logger.debug("Ignoring message from ignored user {}".format(message.author))
            return
        # build the user struct and update the users object
        try:
            content = message.content.strip().split()
            content[0] = content[0].lower()
        except:
            return
        # Check if any of the special functions
        # would like to run on this message
        for check, event in self.special:
            if check(self, message):
                self.dispatch(event, message)
                break

    async def on_guild_join(self, guild):
        """
        Coroutine. Handler for joining guilds. Do not override.
        If you wish to add handling for joining guilds use @bot.subscribe('guild_join')

        If a primary guild is defined and this is not the primary guild, leave it.
        Otherwise, print a warning that a primary guild is not defined
        """
        if self.primary_guild is not None and self.primary_guild != guild:
            try:
                await (discord.utils.get(
                        guild.channels,
                        name='general',
                        type=discord.ChannelType.text
                    )).send_message(
                    "Unfortunately, this instance of {0} is not configured"
                    " to run on multiple servers. Please contact the owner"
                    " of this instance, or run your own instance of {0}."
                    " Goodbye!".format(self.user.name)
                )
            except:
                pass
            await guild.leave()
        elif len(self.guilds) > 1:
            logger.warning("Joining multiple guilds is not currently supported behavior")

    def wait_for(self, event, *, check=None, timeout=None):
        """
        Wait for a single instance of an event.
        Optional condition and timeout values.

        If you wait for a message and apply a condition, there is some special
        logic to preempt conflicting special message handlers
        """
        if event == 'message' and check is not None:
            key = os.urandom(4).hex() # Get a random dummy event name
            # Inject a phony special handler to the front of the queue
            # If this wait_for accepts a message, then it will preempt other handlers
            # Ugly lambda to drop the self argument when running wait_for conditions
            self.special = [((lambda s,m: check(m)), key)] + self.special

            waitable = super().wait_for(event, check=check, timeout=timeout)

            # coroutine to add the try-finally logic
            async def waiter():
                try:
                    return await waitable
                finally:
                    self.special = [
                        (cond, evt) for cond, evt in self.special
                        if evt != key
                    ]

            return waiter()
        return super().wait_for(event, check=check, timeout=timeout)

APIEssentials = CommandSuite('Beymax Core API Essentials')

# Future dispatch events are handled as a task
# But tasks must be added to an existing bot
@APIEssentials.add_task(30)
async def check_future_dispatch(self):
    now = discord.utils.utcnow()
    async with self.db.session() as session:
        results = await session.execute(
            alchemy.select(APIEssentials.schema.FutureDispatch).where(
                APIEssentials.schema.FutureDispatch.date <= now.timestamp()
            )
        )
        for event in results.scalars():
            overshoot = int(now.timestamp() - event.date)
            if overshoot > 1:
                logger.warning("Future dispatch {} overshot by {}s. The server may be overloaded".format(
                    event.event,
                    overshoot
                ))
            await session.delete(event)
            
            try:
                self.dispatch(
                    event.event,
                    *pickle.loads(base64.b64decode(as_bytes(event.pickled_args))),
                    **pickle.loads(base64.b64decode(as_bytes(event.pickled_kwargs)))
                )
            except:
                logger.error("Unable to load event from future dispatch (data type error?). Please check your database", exc_info=True)
        
        results = (await session.execute(
            alchemy.select(APIEssentials.schema.FutureDispatch).where(
                APIEssentials.schema.FutureDispatch.date > now.timestamp()
            )
        )).scalars().all()
        await session.commit() # Remove the event even if dispatch fails
        if len(results):
            self.update_interval(
                'check_future_dispatch',
                min(
                    ceil(evt.date - now.timestamp())
                    for evt in results
                ),
                permanent=False
            )
        

@APIEssentials.subscribe('ready', once=True)
async def first_ready(self, event):
    try:
        if 'primary_guild' in self.configuration:
            self.primary_guild = discord.utils.get(
                self.guilds,
                id=self.configuration['primary_guild']
            )
            if self.primary_guild is None:
                logger.critical("Primary guild set but no matching guild was found")
                sys.exit("Primary guild set, but no matching guild was found")
            else:
                logger.info("Validated primary guild: {}".format(self.primary_guild.name))
        else:
            logger.warning("No primary guild set in configuration. This is not supported behavior")
        for guild in list(self.guilds):
            logger.debug("Connected to guild {} ({})".format(guild.name, guild.id))
            await self.on_guild_join(guild)
        logger.debug("{} Tasks in schedule".format(len(self.tasks)))
        self._general = discord.utils.get(
            self.get_all_channels(),
            name='general',
            type=discord.ChannelType.text
        )
        
        if 'channels' in self.configuration:
            for name in self.channel_references:
                if name in self.configuration['channels']:
                    channel = discord.utils.get(
                        self.get_all_channels(),
                        name=self.configuration['channels'][name],
                        type=discord.ChannelType.text
                    )
                    if channel is None:
                        channel = discord.utils.get(
                            self.get_all_channels(),
                            id=self.configuration['channels'][name],
                            type=discord.ChannelType.text
                        )
                    if channel is None:
                        raise NameError("No channel by name of "+self.configuration['channels'][name])
                    self.channel_references[name] = channel
                else:
                    logger.warning("Channel reference {} not defined".format(name))

        
        
        await (self.dispatch('schema', self.db)) # Returns a task
        await self.db.connection.run_sync(self.db.base.metadata.create_all)
        await self.db.connection.commit()
        taskkey = ''.join(sorted(self.tasks))
        key = await self.get_value('task_key')
        if key != taskkey:
            logger.info("Invalidating task time cache")
            await self.set_value('task_key', taskkey)
            async with self.db.session() as session:
                await session.execute(
                    alchemy.delete(APIEssentials.schema.Task)
                )
        else:
            logger.debug("Not invalidating task cache")

        # Add legacy lock
        DATABASE['lock'] = asyncio.Lock()
        try:
            await asyncio.wait_for(
                self.dispatch('migration'),
                180 # migrations can take up to 3 minutes
            )
        except TimeoutError:
            logger.error("Migrations timed out after 3 minutes")
        except:
            logger.error("Errors encountered during migrations", exc_info=True)

        for task in self.tasks.values():
            if 'task' in task: # Legacy task chains do not set a task attribute
                task['task'].start()
        
        logger.info("Database ready, now syncing commands")

        self.dispatch('command-init')

    except:
        logger.critical("Unhandled exception during 'ready' event", exc_info=True)
        sys.exit("Unhandled exception during startup")

@APIEssentials.subscribe('command-init', once=True)
async def sync_commands(self, evt):
    
    commands = self.tree.get_commands(guild=self.primary_guild)

    logger.debug("Syncing {} commands".format(len(commands)))

    await self.tree.sync(guild = self.primary_guild)
    logger.info("Startup complete")
    await self.change_presence()

@APIEssentials.subscribe('guild_role_create')
@APIEssentials.subscribe('guild_role_delete')
@APIEssentials.subscribe('before:ready', once=True)
async def update_ignore_roles(self, event, *args):
    """
    Updates Beymax's list of roles to ignore
    """
    references = self.config_get('ignore_role', default=[])
    if not isinstance(references, list):
        references = [references]
    self.ignore_roles = {
        role
        for guild in self.guilds
        for role in guild.roles
        if role.name in references or role.id in references
    }
    logger.debug("Populated {} roles to ignore".format(len(self.ignore_roles)))
    if len(references) > 0 and len(self.ignore_roles) == 0:
        warnings.warn(
            "No ignore roles matched. There is currently no way to blacklist users"
        )
        logger.warning("No ignore roles matched. There is currently no way to blacklist users")
    self.ignored_users = set()
    for member in self.get_all_members():
        if len(set(member.roles) & self.ignore_roles):
            logger.debug("Ignoring user {}".format(member))
            self.ignored_users.add(member.id)

@APIEssentials.subscribe('after:member_update')
async def update_ignore_users(self, event, before, after):
    """
    Updates Beymax's list of users to ignore
    """
    if len(set(after.roles) & self.ignore_roles):
        logger.debug("Ignoring user {}".format(after))
        self.ignored_users.add(after.id)
    elif after.id in self.ignored_users:
        logger.debug("Unignoring user {}".format(after))
        self.ignored_users.remove(after.id)

@APIEssentials.add_command('parse', description="Parse this string and run special message handlers")
async def cmd_parse(interaction, message: Arg('message', description="Message to pass to the bot", type=str)):
    msg = lambda : None # Dummy namespace object
    msg.content = message
    msg.author = interaction.user
    msg.channel = interaction.channel
    msg.guild = interaction.guild
    await interaction.response.send_message("OK", ephemeral=True)
    await interaction.client.on_message(msg)

@APIEssentials.table
class Migration(object):
    __tablename__ = 'core_migrations'
    key = alchemy.Column(alchemy.String, primary_key=True)
    date = alchemy.Column(alchemy.DateTime(timezone=True))

@APIEssentials.table
class FutureDispatch(object):
    __tablename__ = 'core_future_dispatch'
    date = alchemy.Column(alchemy.Integer, primary_key=True)
    event = alchemy.Column(alchemy.String, primary_key=True)
    pickled_args = alchemy.Column(alchemy.TEXT)
    pickled_kwargs = alchemy.Column(alchemy.TEXT)

@APIEssentials.table
class KeyValue(object):
    __tablename__ = 'core_key_value'
    key = alchemy.Column(alchemy.String, primary_key=True)
    value = alchemy.Column(alchemy.String)

@APIEssentials.table
class Task(object):
    __tablename__ = 'core_tasks'
    name = alchemy.Column(alchemy.String, primary_key=True)
    date = alchemy.Column(alchemy.Integer)

@APIEssentials.migration('core-migrate-to-db')
async def migrate_db_backend(bot):
    async with DBView('tasks', 'core_future_dispatch', core_future_dispatch=[], tasks={'key': None, 'tasks': {}}) as db:
        await bot.set_value('task_key', db['tasks']['key'])
        async with bot.db.session() as session:
            tuples = []
            tuples += [
                APIEssentials.schema.Task(
                    name=name,
                    date=int(timestamp)
                )
                for name, timestamp in db['tasks']['tasks'].items()
            ]
            tuples += [
                APIEssentials.schema.FutureDispatch(
                    date=strptime(event['date']).timestamp(),
                    event=event['event'],
                    pickled_args=base64.b64encode(pickle.dumps(event['args'])).decode(),
                    pickled_kwargs=base64.b64encode(pickle.dumps(event['kwargs'])).decode()
                )
                for event in db['core_future_dispatch']
            ]
            # tuples += [
            #     APIEssentials.schema.Migration(
            #         key=key,
            #         date=strptime(date)
            #     )
            #     for key, date in db['core_migrations'].items()
            # ]
            session.add_all(tuples)
            await session.commit()

class MultiserverClient(Client):
    """
    This is a multi-server version of the standard Beymax client. This class
    requires more setup than a standard client.
    * Supports auto-sharding controlled by a master shard which controls load balance
    * Supports manual-sharding to allow geo-scaling
    * Handshake between shards uses a public key exchange
    * Supports database eventual-consistency for server-specific databases to
        eventually sync between shards
    * Supports live configuration changes, with contextual config loaded within
        each command
    * Supports background tasks being run globally or in the context of each server
    * Permissions and more generally, commands, not supported in DMs

    This client is planned but has no release target
    """
    pass
