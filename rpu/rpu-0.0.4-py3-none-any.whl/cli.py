import sys
from typing import Any, Callable, Optional

from .consts import MISSING

__all__ = ["Command", "ConsoleClient"]


class ExecutableAlreadyTaken(BaseException):
    def __init__(self) -> None:
        super().__init__("Command Name or alias(s) already taken")


class Command:
    def __init__(
        self,
        *,
        name: str,
        description: str,
        brief: str,
        callback: Callable,
        aliases: Optional[list[str]] = MISSING,
    ):
        """Creates a command object

        Parameters
        ----------
        name: `str`
            The commands name
        description: `str`
            The commands long description
        brief: `str`
            a brief description for the command
        callback: `typing.Callable`
            The commands callback
        aliases: Optional[list[`str`]]
            The commands aliases

        Attributes
        ----------
        name: `str`
            The commands name
        description: `str`
            The commands long description
        brief: `str`
            a brief description for the command
        callback: `typing.Callable`
            The commands callback
        aliases: list[`str`]
            The commands aliases
        exes: list[`str`]
            the commands aliases, but it also has the commands name
        """

        self.name = name
        self.aliases = aliases or []
        self.description = description
        self.callback = callback
        self.brief = brief
        self.exes = self.aliases + [name]


class HelpCmd(Command):
    def __init__(self, client):
        self.client = client
        super().__init__(
            name="help",
            description="the help menu",
            brief="shows this menu",
            callback=self.callback,
        )

    def show_commands(self):
        nl = "\n"
        print(
            f"""
CLI Arguments

{nl.join(
    [
        f" - {cmd.name}: {cmd.brief}"
        for cmd in self.client.commands
    ]
)}
"""
        )

    def show_command(self, cmd_name: str):
        found_cmds = [cmd for cmd in self.client.commands if cmd_name in cmd.exes]
        if len(found_cmds) == 0:
            print(":show")
            self.client.dispatch("command_not_found", cmd_name)
            return
        else:
            cmd: Command = found_cmds[0]

        print(f"""\nHelp - {cmd.name}\n""")
        if cmd.brief:
            print(f"""Brief:\n     {cmd.brief}""")
        if cmd.aliases:
            print(f"""Aliases:\n     {', '.join(cmd.aliases)}""")
        if cmd.description:
            print(f"""Description:\n     {cmd.description}""")

    def callback(self, cmd: str = MISSING):
        if cmd is MISSING:
            self.show_commands()
        else:
            self.show_command(cmd)


class ConsoleClient:
    def __init__(self, *, help_command: Optional[Command] = MISSING):
        """Creates a CLI console client

        Parameters
        ----------
        help_command: Optional[`cli.Command`]
            An optional help_command. if not supplied, default one will be used

        Attributes
        ----------
        help_command: `cli.Command`
            The help command
        commands: list[`cli.Command`]
            A list of all commands
        """

        self.help_command = help_command or HelpCmd(self)
        self.commands = [self.help_command]

    def on_command_error(self, command: str, error: Exception) -> None:
        """This function gets called when an error happens during the execution of a command

        This is an event, and thus can be overrided

        Parameters
        ----------
        command: `str`
            the commands name
        error: `Exception`
            The error
        """

        raise error

    def on_command_not_found(self, command: str) -> None:
        """This function gets called when the client can not find the specificed command

        This is an event, and thus can be overrided

        Parameters
        ----------
        command: `str`
            the commands name
        """

        print(f"Command not found: {command}")

    def on_arg_not_given(self, command: str, arg: str) -> None:
        """This function gets called when a required arg was not given during the execution of a command

        This is an event, and thus can be overrided

        Parameters
        ----------
        command: `str`
            the commands name
        arg: `str`
            the argument that was not supplied
        """

        print(f"Argument not provided: {arg}")

    def on_extra_arg_given(self, command: str) -> None:
        """This function gets called when an extra arg was given when executing a command

        This is an event, and thus can be overrided

        Parameters
        ----------
        command: `str`
            the commands name
        """

        print("Extra arg given")

    def event(self, func):
        """|decorator|

        Creates an event by overriding the events name
        """

        setattr(self, func.__name__, func)
        return func

    def dispatch(self, event_name: str, /, *args: Any, **kwargs: Any) -> None:
        method = "on_" + event_name

        if hasattr(self, method):
            event = getattr(self, method)
            event(*args, **kwargs)

    def command(
        self,
        *,
        name: Optional[str] = MISSING,
        description: Optional[str] = MISSING,
        brief: Optional[str] = MISSING,
        aliases: Optional[list[str]] = MISSING,
    ):
        """|decorator|

        Turns a function into a `cli.Command` object, and auto-adds it to the client

        Parameters
        ----------
        name: Optional[`str`]
            The commands name. if not given, it will use the functions name
        description: Optional[`str`]
            The commands description. If not given, will be the functions docstring
        brief: Optional[`str`]
            The commands brief description.
        aliases: Optional[list[`str`]]
            The commands aliases
        """

        def inner(func: Callable):
            cmd = Command(
                name=name or func.__name__,
                description=description or func.__doc__ or "",
                brief=brief or "",
                aliases=aliases,
                callback=func,
            )

            if any(
                "d"
                for cmd2 in self.commands
                for executable in cmd2.exes
                if executable in cmd.exes
            ):
                raise ExecutableAlreadyTaken()

            self.commands.append(cmd)
            return cmd

        return inner

    def run(self):
        """Starts the client"""

        args = sys.argv

        if len(args) == 1:
            given_cmd = "help"
            cmd_args = []
        elif len(args) == 2:
            given_cmd = args[1]
            cmd_args = []
        else:
            given_cmd = args[1]
            cmd_args = args
            cmd_args.pop(0)
            cmd_args.pop(0)

        found_cmds = [cmd for cmd in self.commands if given_cmd in cmd.exes]
        if len(found_cmds) == 0:
            self.dispatch("command_not_found", given_cmd)
            return
        else:
            cmd = found_cmds[0]

        try:
            cmd.callback(*cmd_args)
        except TypeError as e:
            if "positional arguments but" in str(e):
                self.dispatch("extra_arg_given", given_cmd)
            elif "required positional argument" in str(e):
                arg = str(e).split("'")[1].split("'")[0]
                self.dispatch("arg_not_given", given_cmd, arg)
            else:
                self.dispatch("command_error", given_cmd, e)
        except Exception as e:
            self.dispatch("command_error", given_cmd, e)
