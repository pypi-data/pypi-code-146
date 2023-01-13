# -*- coding: utf-8 -*-

# python std lib
import os
import pdb
import re
import sys
import traceback

# 3rd party imports
from docopt import docopt


base_args = """
Usage:
    sgit <command> [options] [<args> ...]

Commands:
    init          Initialize a new sgit repo
    list          Show the config for all repos in the config file
    repo          Commands to manipulate .sgit.yml
    update        Update a sub repo
    fetch         Runs git fetch on all repos

Options:
    --help          Show this help message and exit
    --version       Display the version number and exit
"""


sub_repo_args = """
Usage:
    sgit repo add <name> <url> [<rev>] [options]
    sgit repo set <name> branch <branch> [options]
    sgit repo set <name> tag <tag> [options]

Options:
    <rev>               Revision to set for a given repo [default: master]
    -y, --yes           Answers yes to all questions (use with caution)
    -h, --help          Show this help message and exit
"""


sub_update_args = """
Usage:
    sgit update [<repo> ...] [options]

Options:
    <repo>      Name of repo to update
    -y, --yes   Answers yes to all questions (use with caution)
    -h, --help  Show this help message and exit
"""


sub_list_args = """
Usage:
    sgit list [options]

Options:
    -y, --yes   Answers yes to all questions (use with caution)
    -h, --help  Show this help message and exit
"""


sub_init_args = """
Usage:
    sgit init [options]

Options:
    -y, --yes   Answers yes to all questions (use with caution)
    -h, --help  Show this help message and exit
"""


sub_fetch_args = """
Usage:
    sgit fetch [<repo> ...] [options]

Options:
    -y, --yes       Answers yes to all questions (use with caution)
    -h, --help  Show this help message and exit
"""


def parse_cli():
    """Parse the CLI arguments and options."""
    import sgit

    from docopt import extras, Option, DocoptExit

    try:
        cli_args = docopt(
            base_args, options_first=True, version=sgit.__version__, help=True
        )
    except DocoptExit:
        extras(True, sgit.__version__, [Option("-h", "--help", 0, True)], base_args)

    argv = [cli_args["<command>"]] + cli_args["<args>"]

    if cli_args["<command>"] == "repo":
        sub_args = docopt(sub_repo_args, argv=argv)
    elif cli_args["<command>"] == "update":
        sub_args = docopt(sub_update_args, argv=argv)
    elif cli_args["<command>"] == "init":
        sub_args = docopt(sub_init_args, argv=argv)
    elif cli_args["<command>"] == "list":
        sub_args = docopt(sub_list_args, argv=argv)
    elif cli_args["<command>"] == "fetch":
        sub_args = docopt(sub_fetch_args, argv=argv)
    else:
        extras(True, sgit.__version__, [Option("-h", "--help", 0, True)], base_args)
        sys.exit(1)

    # In some cases there is no additional sub args of things to extract
    if cli_args["<args>"]:
        sub_args["<sub_command>"] = cli_args["<args>"][0]

    return (cli_args, sub_args)


def run(cli_args, sub_args):
    """Execute the CLI."""
    retcode = 0

    if "DEBUG" in os.environ:
        print(cli_args)
        print(sub_args)

    from sgit.core import Sgit

    core = Sgit(answer_yes=sub_args["--yes"])

    if cli_args["<command>"] == "repo":
        if sub_args["add"]:
            retcode = core.repo_add(
                sub_args["<name>"],
                sub_args["<url>"],
                sub_args["<rev>"] or "master",
            )
        elif sub_args["set"]:
            if sub_args["tag"]:
                retcode = core.repo_set(
                    sub_args["<name>"],
                    "tag",
                    sub_args["<tag>"]
                )
            elif sub_args["branch"]:
                retcode = core.repo_set(
                    sub_args["<name>"],
                    "branch",
                    sub_args["<branch>"],
                )
            else:
                retcode = 1

    if cli_args["<command>"] == "list":
        retcode = core.repo_list()

    if cli_args["<command>"] == "update":
        repos = sub_args["<repo>"]
        repos = repos or None

        retcode = core.update(repos)

    if cli_args["<command>"] == "init":
        retcode = core.init_repo()

    if cli_args["<command>"] == "fetch":
        repos = sub_args["<repo>"]
        repos = repos or None

        retcode = core.fetch(repos)

    return retcode


def cli_entrypoint():
    """Used by setup.py to create a cli entrypoint script."""
    try:
        cli_args, sub_args = parse_cli()
        exit_code = run(cli_args, sub_args)
        sys.exit(exit_code)
    except Exception as e:
        ex_type, ex_value, ex_traceback = sys.exc_info()

        if "DEBUG" in os.environ:
            extype, value, tb = sys.exc_info()
            traceback.print_exc()
            if "PDB" in os.environ:
                pdb.post_mortem(tb)
            raise
        else:
            print(f"Exception type : {ex_type.__name__}")
            print(f"EXCEPTION MESSAGE: {ex_value}")
            print(f"To get more detailed exception set environment variable 'DEBUG=1'")
            print(f"To PDB debug set environment variable 'PDB=1'")
