import argparse
from enum import Enum

from ._arguments._groups import make_arguments
from ._arguments._container import _Arguments
from .parameters import valid_arguments


class SessionType(Enum):
    CLI = 0
    PyAPI = 1
    # TODO (sjr) Maybe add a JupyterAPI literal here in the future
    #            if we want different behaviour for plotting / printing
    #            when in a Jupyter environment


class _CavCalcSession:
    def __init__(self):
        # Default to Python API mode, and only reset this to CLI if we're in __main__:main
        self.mode = SessionType.PyAPI
        self.parser = argparse.ArgumentParser(
            description="A tool to calculate Fabry-Perot cavity parameters."
        )
        make_arguments(self.parser)

    @property
    def is_api_mode(self) -> bool:
        return self.mode == SessionType.PyAPI

    @property
    def is_cli_mode(self) -> bool:
        return self.mode == SessionType.CLI

    def parse_args(self, command: list[str] = None):
        # Get the order in which each physical argument was specified
        opts = filter(lambda x: x.startswith("-"), command)
        phys_args = tuple(arg for opt in opts if (arg := opt.split("-")[1]) in valid_arguments)
        arg_order = {arg_name: i for i, arg_name in enumerate(phys_args)}

        args = _Arguments()
        self.parser.parse_args(command, namespace=args)
        args.process(arg_order)
        args.verify()
        return args
