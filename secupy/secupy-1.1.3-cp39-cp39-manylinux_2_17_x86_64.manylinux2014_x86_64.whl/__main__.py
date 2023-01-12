import argparse
import importlib
import socket

from secupy import __version__
from secupy.commands.module import main as runpy


class RunPy(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        try:
            runpy()
        except Exception as ex:
            print(ex)
        parser.exit()


def main():
    # fmt: off
    parser = argparse.ArgumentParser("secupy")
    parser.add_argument("--version", action="version", version=f"{__version__}")
    parser.add_argument("-m", action=RunPy, help="like 'python -m package.module'")
    parser.set_defaults(which="secupy")
    # fmt: on

    subparsers = parser.add_subparsers(help="help")

    # fmt: off
    parser_activate = subparsers.add_parser("activate", help="activate -h, --help")
    parser_activate.add_argument("-t", "--token", dest="token", type=str, help="authentication token", required=True)
    parser_activate.add_argument("-l", "--label", dest="label", type=str, default=socket.gethostname(), help="machine label")
    parser_activate.add_argument("-v", "--verbose", dest='verbose', action="store_true", help="enable debug")
    parser_activate.set_defaults(which="activate")
    # fmt: on

    # fmt: off
    parser_activate = subparsers.add_parser("status", help="status -h, --help")
    parser_activate.add_argument("-v", "--verbose", dest='verbose', action="store_true", help="enable debug")
    parser_activate.set_defaults(which="status")
    # fmt: on

    # fmt: off
    parser_build = subparsers.add_parser("build", help="build -h, --help")
    parser_build.add_argument("-s","--source", dest="source", help="source directory or single file", required=True,)
    parser_build.add_argument("-d","--destination", dest="destination", help="destination directory", required=True,)
    parser_build.add_argument("-t", "--ttl", dest="ttl", type=float, default=0.0, help="ttl in days")
    parser_build.add_argument("--password", dest="password", type=str, help="user aes password")
    parser_build.add_argument("--salt", dest="salt", type=str, help="user aes salt")
    parser_build.add_argument("-e","--exclude", dest="exclude", action="append", help='can be multiple. Patterns are the same as for fnmatch, with the addition of "**" which means "src directory and all subdirectories, recursively"',)
    parser_build.add_argument("-i","--include", dest="include", action="append", help='can be multiple. Patterns are the same as for fnmatch, with the addition of "**" which means "src directory and all subdirectories, recursively"',)
    parser_build.add_argument("-u","--unprotect", dest="unprotect", action="append", help='can be multiple. Patterns are the same as for fnmatch, with the addition of "**" which means "src directory and all subdirectories, recursively"',)
    parser_build.add_argument("--pyinstaller", dest="pyinstaller", action="append", help="can be multiple. Create pyinstaller hook",)
    parser_build.add_argument("-v", "--verbose", dest="verbose", action="store_true", help="enable debug")
    parser_build.set_defaults(which="build")
    # fmt: on

    args = parser.parse_args()

    if not hasattr(args, "which") or args.which == "secupy":
        parser.print_help()
    else:
        try:
            importlib.import_module(f"secupy.commands.{args.which}").main(args)
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    main()
