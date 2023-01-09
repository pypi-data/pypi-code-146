import argparse
import logging

from rctl.cli.command import CmdBase
from rctl.cli.utils import run_command_on_subprocess

logger = logging.getLogger(__name__)

class CmdPutFile(CmdBase):
    def __init__(self, args):
        super().__init__(args)
    def run(self):
        run_command_on_subprocess('dvc pull')        
        return 0


def add_parser(subparsers, parent_parser):
    REPO_HELP = "Get File or folder. Use: `rctl get`"
    REPO_DESCRIPTION = (
        "Get File or folder. Use: `rctl get`"
    )

    repo_parser = subparsers.add_parser(
        "get",
        parents=[parent_parser],
        description=REPO_DESCRIPTION,
        help=REPO_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    repo_parser.set_defaults(func=CmdPutFile)
