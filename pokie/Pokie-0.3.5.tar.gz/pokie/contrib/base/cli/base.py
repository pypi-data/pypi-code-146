import os
import sys
from argparse import ArgumentParser

from rick.resource.console import AnsiColor
from rick.util.loader import load_class

import pokie
from pokie.constants import DI_APP, DI_FLASK
from pokie.core import CliCommand
from pokie.util.cli_args import ArgParser


class BaseCommand(CliCommand):
    def get_modules(self) -> dict:
        return self.get_di().get(DI_APP).modules

    def get_cmd_map(self) -> dict:
        result = {}
        for _, module in self.get_modules().items():
            for cmd, cmd_class in module.cmd.items():
                result[cmd] = cmd_class
        return result

    def run(self, args) -> bool:
        di = self.get_di()
        color = AnsiColor()
        self.tty.write("Available commands:\n")
        for _, module in di.get(DI_APP).modules.items():
            for cmd, cmd_path in module.cmd.items():
                cls = load_class(cmd_path)
                if not cls:
                    raise RuntimeError(
                        "Error: class '{}' not found while listing available CLI commands".format(
                            cmd_path
                        )
                    )
                if not issubclass(cls, CliCommand):
                    raise RuntimeError(
                        "Error: class '{}' does not extend CliCommand".format(cmd_path)
                    )
                obj = cls(di)
                self.tty.write(
                    "{} \t {}".format(color.green(cmd), color.white(obj.description))
                )

        return True


class VersionCmd(BaseCommand):
    description = "display pokie version"

    def run(self, args) -> bool:
        self.tty.write(pokie.get_version())
        return True


class HelpCmd(BaseCommand):
    description = "display usage information for a given command"

    def arguments(self, parser: ArgumentParser):
        parser.add_argument("command", type=str, help="Command to get usage details.")

    def run(self, args) -> bool:
        map = self.get_cmd_map()
        if args.command not in map.keys():
            self.tty.error("Error: command '{}' not found".format(args.command))
            return False

        cls = load_class(map[args.command])
        handler = cls(self.get_di())  # type: CliCommand
        self.show(args.command, handler)
        return True

    def show(self, cmd, cmd_object):
        """
        Show command detail
        :param cmd: command
        :param cmd_object: command object
        :return:
        """
        program = os.path.basename(sys.argv[0])

        self.tty.write("{}: {}\n".format(cmd, cmd_object.description))
        self.tty.write("usage: {} {} [OPTIONS...]\n".format(program, cmd))

        parser = ArgParser(add_help=False)
        cmd_object.arguments(parser)
        self.tty.write(parser.format_parameters())


class ListCmd(BaseCommand):
    description = "list available commands"

    def run(self, args) -> bool:
        color = AnsiColor()
        self.tty.write(
            "\nusage: {} <command> [OPTIONS...]\n".format(os.path.basename(sys.argv[0]))
        )
        self.tty.write("available commands:")
        for cmd, cmd_path in self.get_cmd_map().items():
            cls = load_class(cmd_path)

            if not cls:
                raise RuntimeError(
                    "Error: class '{}' not found while listing available CLI commands".format(
                        cmd_path
                    )
                )

            if not issubclass(cls, CliCommand):
                raise RuntimeError(
                    "Error: class '{}' does not extend CliCommand".format(cmd_path)
                )

            # show details
            self.tty.write(
                "{} \t {}".format(
                    color.green(cmd), color.white(cls.description)
                ).expandtabs(32)
            )

        return True


class RunServerCmd(CliCommand):
    description = "run Flask webserver for development purposes"

    # flask_name: args_name
    flask_args = {
        "host": "host",
        "port": "port",
        "debug": "debug",
        "use_reloader": "reload",
    }

    def arguments(self, parser: ArgumentParser):
        parser.add_argument(
            "-h",
            "--host",
            help="The interface to bind to (default: 127.0.0.1)",
            required=False,
            default="127.0.0.1",
        )
        parser.add_argument(
            "-p",
            "--port",
            help="The port to bind to (default: 5000)",
            required=False,
            default="5000",
        )
        parser.add_argument(
            "-d",
            "--debug",
            help="Enable debug mode (default: false)",
            required=False,
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "-r",
            "--reload",
            help="Enable automatic reload (default: false)",
            required=False,
            action="store_true",
            default=False,
        )

    def run(self, args) -> bool:
        kwargs = {}
        for a, b in self.flask_args.items():
            kwargs[a] = getattr(args, b)

        # run flask
        self.get_di().get(DI_FLASK).run(**kwargs)

        return True
