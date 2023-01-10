import os
import sys
from argparse import ArgumentParser
from typing import List
from collections import OrderedDict

from flask import Flask
from rick.base import Di, Container, MapLoader
from rick.event import EventManager
from rick.util.loader import load_class
from rick.resource.console import ConsoleWriter

from pokie.constants import (
    DI_CONFIG,
    DI_SERVICES,
    DI_FLASK,
    DI_APP,
    DI_EVENTS,
    DI_TTY,
    DI_SIGNAL,
)
from .module import BaseModule
from .command import CliCommand
from pokie.util.cli_args import ArgParser
from .signal import SignalManager


class FlaskApplication:
    module_file_name = "module"  # module class file name
    module_class_name = "Module"  # default module class name

    system_modules = [
        "pokie.contrib.base",
    ]  # system modules to always be included

    def __init__(self, cfg: Container):
        self.di = Di()
        self.app = None
        self.modules = {}  # app module list

        self.di.add(DI_CONFIG, cfg)
        self.di.add(DI_APP, self)
        self.cfg = cfg

    def build(self, module_list: list, factories: List = None) -> Flask:
        """
        Build the application

        Factories is a list of optional callables to assemble functionality on top of Di, eg. database connection,
        cache, logging, etc. Factories are called *before* modules are initialized, to ensure all required dependencies
        are available

        :param module_list: list of module names to initialize
        :param factories: optional list of callables to be initialized with the application
        :return:
        """
        if not factories:
            factories = []

        self.app = Flask(type(self).__name__)
        self.app.di = self.di
        self.di.add(DI_FLASK, self.app)

        # initialize signal manager
        self.di.add(DI_SIGNAL, SignalManager(self.di))

        # initialize TTY
        self.di.add(DI_TTY, ConsoleWriter())

        # load modules
        self.modules = {}
        module_list = [*self.system_modules, *module_list]
        for name in module_list:
            cls = load_class(
                "{}.{}.{}".format(name, self.module_file_name, self.module_class_name)
            )
            if cls is None:
                raise RuntimeError(
                    "build(): cannot load module '{}' - Module() class not found".format(
                        name
                    )
                )
            if not issubclass(cls, BaseModule):
                raise RuntimeError(
                    "build(): Class Module on '{}' must extend BaseModule".format(name)
                )
            if name in self.modules.keys():
                raise ValueError(
                    "build(): Module named '{}' already exists".format(name)
                )
            self.modules[name] = cls(self.di)

        # build service map
        svc_map = {}
        for name, m in self.modules.items():
            services = getattr(m, "services", {})
            if type(services) is dict:
                svc_map.update(services)
            else:
                raise RuntimeError(
                    "build(): cannot load service map from module '{}'; attribute must be of type dict".format(
                        name
                    )
                )
        # register service mapper
        self.di.add(DI_SERVICES, MapLoader(self.di, svc_map))

        # run factories
        for factory in factories:
            if type(factory) is str:
                # if factory is string, assume it is a path to a callable
                factory = load_class(factory)
            if not callable(factory):
                raise RuntimeError("build(): non-callable or non-existing factory")
            else:
                factory(self.di)

        # parse events from modules
        evt_mgr = EventManager()
        for _, module in self.modules.items():
            module_events = getattr(module, "events", None)
            if isinstance(module_events, dict):
                for evt_name, evt_details in module_events.items():
                    for priority, handlers in evt_details.items():
                        for handler in handlers:
                            evt_mgr.add_handler(evt_name, handler, int(priority))

        self.di.add(DI_EVENTS, evt_mgr)

        # initialize modules
        for _, module in self.modules.items():
            module.build(self)

        return self.app

    def http(self, **kwargs):
        self.app.run(**kwargs)

    def cli(self, **kwargs):
        """
        Execute CLI commands
        :param kwargs: optional parameters for ArgumentParse
        :return:
        """
        if "writer" in kwargs.keys():
            tty = kwargs["writer"]
        else:
            tty = ConsoleWriter()

        # default command when no args detected
        command = "list"
        # extract command if specified
        if len(sys.argv) > 1:
            command = str(sys.argv[1])

        if "add_help" not in kwargs.keys():
            kwargs["add_help"] = False
        if "usage" not in kwargs.keys():
            kwargs["usage"] = "{} {} [OPTIONS...]".format(
                os.path.basename(sys.argv[0]), command
            )

        parser = ArgParser(**kwargs)

        # lookup handler
        for _, module in self.modules.items():
            if command in module.cmd.keys():
                handler = load_class(module.cmd[command])
                if not handler:
                    raise RuntimeError(
                        "cli(): handler class '{}' not found".format(
                            module.cmd[command]
                        )
                    )
                if not issubclass(handler, CliCommand):
                    raise RuntimeError(
                        "cli(): command handler does not extend CliCommand"
                    )
                handler = handler(self.di, writer=tty)  # type: CliCommand
                handler.arguments(parser)
                args = parser.parse_args(sys.argv[2:])
                if parser.failed:
                    # invalid/insufficient args
                    tty.error(parser.error_message)
                    parser.print_help(tty.stderr)
                    exit(1)

                if not handler.run(args):
                    exit(1)
                exit(0)

        # command not found
        tty.error("error executing '{}': command not found".format(command))
        exit(2)
