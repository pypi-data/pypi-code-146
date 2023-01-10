import argparse
import logging
from os import path

from rctl.cli.command import CmdBase
from rctl.cli.utils import run_command_on_subprocess
from rctl.cli import RctlValidReqError

logger = logging.getLogger(__name__)

def put(args):
    message = args.message      
    path = args.path
    if path.endswith("/"):
        path = args.path.rsplit("/", 1)[0]   
    print("Files adding...") 
    run_command_on_subprocess("dvc add {}".format(path))
    run_command_on_subprocess("git add {}.dvc".format(path))
    run_command_on_subprocess("git commit -m '{}' -a".format(message), None, True)
    run_command_on_subprocess("git push", None, True)
    run_command_on_subprocess("dvc push")
    print("Files added successfully")


class CmdPutFile(CmdBase):
    def __init__(self, args):
        super().__init__(args)
        if not getattr(self.args, "message", None):                               
            raise RctlValidReqError("Error: Please provide a message, -m")
        if getattr(self.args, "path", None):
            if not path.exists(self.args.path):
                raise RctlValidReqError("Error: Please provide a valid path")      
        else:
            raise RctlValidReqError("Error: Please provide a valid path")           

    def run(self):
        put(self.args)        
        return 0


def add_parser(subparsers, parent_parser):
    REPO_HELP = "Put File or folder. Use: `rctl put <file or folder path> -m <commit message>`"
    REPO_DESCRIPTION = (
        "Put File or folder. Use: `rctl put <file or folder path> -m <commit message>`"
    )

    repo_parser = subparsers.add_parser(
        "put",
        parents=[parent_parser],
        description=REPO_DESCRIPTION,
        help=REPO_HELP,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    repo_parser.add_argument(
        "path", 
        nargs="?", 
        default="data",
        help="File or Folder path",
    )

    repo_parser.add_argument(
        "-m", 
        "--message", 
        nargs="?", 
        help="Commit message",
    )
    
 
    
    repo_parser.set_defaults(func=CmdPutFile)
