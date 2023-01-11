#!/usr/bin/env python3
import argparse


def get_opts(prog_name="dmenuplaylist"):
    parser = argparse.ArgumentParser(
        prog=prog_name,
        description="""Simple playlist manager, meant to be used with mpv.""",
        allow_abbrev=False,
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-a",
        "--add",
        metavar="FILE(s)",
        nargs="*",
        help="""Add the given FILE(s) to your playlist.""",
    )
    group.add_argument(
        "-d",
        "--delete",
        metavar="FILE",
        help="""Delete the given entry. Useful for scripting, like mpv scripts.""",
    )
    group.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="""Display your playlist.""",
    )
    group.add_argument(
        "-r",
        "--remove",
        action="store_true",
        help="""Display your playlist and select entries to remove.""",
    )
    args = parser.parse_args()
    return args
