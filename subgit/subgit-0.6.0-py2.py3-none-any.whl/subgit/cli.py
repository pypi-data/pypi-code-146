# -*- coding: utf-8 -*-

# python std lib
import logging
import os
import pdb
import sys
import traceback

# 3rd party imports
from docopt import docopt, extras, Option, DocoptExit

base_args = """
Usage:
    subgit <command> [options] [<args> ...]

Commands:
    fetch    Fetch one or all Git repos
    init     Initialize a new subgit repo
    pull     Update one or all Git repos
    status   Show status of each configured repo
    delete   Delete one or more local Git repos
    import   import repos from github or gitlab and creates a config file
    reset    Reset repo(s) previous tracked state
    clean    Clean repo(s) from untracked files

Options:
    --help          Show this help message and exit
    --version       Display the version number and exit
"""


sub_fetch_args = """
Usage:
    subgit fetch [<repo> ...] [options]

Options:
    -y, --yes                  Answers yes to all questions (use with caution)
    -c <file>, --conf <file>   For using optional config file (use if conf file is
                               something other than '.subgit.yml' or '.sgit.yml')
    -h, --help                 Show this help message and exit
"""


sub_init_args = """
Usage:
    subgit init [<name> <url>] [options]

Options:
    -y, --yes                  Answers yes to all questions (use with caution)
    -c <file>, --conf <file>   For using optional config file (use if conf file is
                               something other than '.subgit.yml' or '.sgit.yml')
    -h, --help                 Show this help message and exit
"""


sub_pull_args = """
Usage:
    subgit pull [<repo> ...] [options]

Options:
    <repo>       Name of repo to pull
    -y, --yes                  Answers yes to all questions (use with caution)
    -c <file>, --conf <file>   For using optional config file (use if conf file is
                               something other than '.subgit.yml' or '.sgit.yml')
    -h, --help                 Show this help message and exit
"""


sub_status_args = """
Usage:
    subgit status [options]

Options:
    -y, --yes                  Answers yes to all questions (use with caution)
    -c <file>, --conf <file>   For using optional config file (use if conf file is
                               something other than '.subgit.yml' or '.sgit.yml')
    -h, --help                 Show this help message and exit
"""


sub_delete_args = """
Usage:
    subgit delete [<repo> ...] [options]

Options:
    -y, --yes                  Answers yes to all questions (use with caution)
    -c <file>, --conf <file>   For using optional config file (use if conf file is
                               something other than '.subgit.yml' or '.sgit.yml')
    -h, --help                 Show this help message and exit
"""


sub_reset_args = """
Usage:
    subgit reset [<repo> ...] [options]

Options:
    -y, --yes                  Answers yes to all questions (use with caution)
    --hard                     Resets the index and working tree. Any changes to tracked
                               files in the working tree since <commit> are discarded.
                               Any untracked files or directories in the way of writing any
                               tracked files are simply deleted.
    -c <file>, --conf <file>   For using optional config file (use if conf file is
                               something other than '.subgit.yml' or '.sgit.yml')
    -h, --help                 Show this help message and exit
"""


sub_import_args = """
Usage:
    subgit import (github | gitlab) <owner> [options]

Options:
    -y, --yes                                Answers yes to all questions (use with caution)
    -o <filename>, --output-file <filename>  Used to specify output filename
    -a, --archived                           Writes only archived repos to output file
    -h, --help                               Show this help message and exit

Information:
    The argument 'owner' must be either username or organisation name. Make sure the
    username/organisation corresponds to the chosen source (github | gitlab)
"""


sub_clean_args = """
Usage:
    subgit clean (-d|-f|-n)... [<repo> ...]

Options:
    -d                         Normally, when no <pathspec> is specified, git clean will not recurse
                               into untracked directories to avoid removing too much. Specify -d
                               to have it recurse into such directories as well. If a <pathspec> is specified,-d is irrelevant;
                               all untracked files matching the specified paths
                               (with exceptions for nested git directories mentioned under --force) will be removed.

    -f, --force                If the Git configuration variable clean.requireForce is not set to false,
                               git clean will refuse to delete files or directories unless given -f or -i.
                               Git will refuse to modify untracked nested git repositories
                               (directories with a .git subdirectory) unless a second -f is given.

    -n, --dry-run              Don’t actually remove anything, just show what would be done.

    -c <file>, --conf <file>   For using optional config file (use if conf file is
                               something other than '.subgit.yml' or '.sgit.yml')

    -h, --help                 Show this help message and exit
"""


def parse_cli():
    """Parse the CLI arguments and options."""
    import subgit

    try:
        cli_args = docopt(
            base_args,
            options_first=True,
            version=subgit.__version__,
            help=True,
        )
    except DocoptExit:
        extras(
            True,
            subgit.__version__,
            [Option("-h", "--help", 0, True)],
            base_args,
        )

    # Set INFO by default, else DEBUG log level
    subgit.init_logging(5 if "DEBUG" in os.environ else 4)
    log = logging.getLogger(__name__)

    argv = [cli_args["<command>"]] + cli_args["<args>"]

    if cli_args["<command>"] == "fetch":
        sub_args = docopt(sub_fetch_args, argv=argv)
    elif cli_args["<command>"] == "init":
        sub_args = docopt(sub_init_args, argv=argv)
    elif cli_args["<command>"] == "pull":
        sub_args = docopt(sub_pull_args, argv=argv)
    elif cli_args["<command>"] == "status":
        sub_args = docopt(sub_status_args, argv=argv)
    elif cli_args["<command>"] == "delete":
        sub_args = docopt(sub_delete_args, argv=argv)
    elif cli_args["<command>"] == "import":
        sub_args = docopt(sub_import_args, argv=argv)
    elif cli_args["<command>"] == "reset":
        sub_args = docopt(sub_reset_args, argv=argv)
    elif cli_args["<command>"] == "clean":
        sub_args = docopt(sub_clean_args, argv=argv)
    else:
        extras(
            True,
            subgit.__version__,
            [Option("-h", "--help", 0, True)],
            base_args,
        )
        sys.exit(1)

    # In some cases there is no additional sub args of things to extract
    if cli_args["<args>"]:
        sub_args["<sub_command>"] = cli_args["<args>"][0]

    return (cli_args, sub_args)


def run(cli_args, sub_args):
    """
    Execute the CLI
    """
    log = logging.getLogger(__name__)

    retcode = 0

    log.debug(cli_args)
    log.debug(sub_args)

    from subgit.core import SubGit
    from subgit.importer.git_importer import GitImport

    core = SubGit(
        config_file_path=sub_args.get("--conf"),
        answer_yes=sub_args.get("--yes"),
        hard_flag=sub_args.get("--hard")
    )

    if cli_args["<command>"] == "fetch":
        repos = sub_args["<repo>"]
        repos = repos or None

        retcode = core.fetch(repos)

    if cli_args["<command>"] == "init":
        repo_name = sub_args["<name>"]
        repo_url = sub_args["<url>"]

        retcode = core.init_repo(repo_name, repo_url)

    if cli_args["<command>"] == "pull":
        repos = sub_args["<repo>"]
        repos = repos or None

        retcode = core.pull(repos)

    if cli_args["<command>"] == "status":
        retcode = core.repo_status()

    if cli_args["<command>"] == "delete":
        repos = sub_args["<repo>"]
        repos = repos or None

        retcode = core.delete(repo_names=repos)

    if cli_args["<command>"] == "reset":
        repos = sub_args["<repo>"]
        repos = repos or None

        retcode = core.reset(repo_names=repos)

    if cli_args["<command>"] == "import":
        git_importer = GitImport(
            config_file_name=sub_args.get("--output-file"), 
            answer_yes=sub_args["--yes"],
            is_archived=sub_args.get("--archived")
        )
        github = sub_args["github"]
        gitlab = sub_args["gitlab"]
        owner = sub_args["<owner>"]
        
        if github:
            retcode = git_importer.import_github(owner)
        
        if gitlab:
            retcode = git_importer.import_gitlab(owner)

    if cli_args["<command>"] == "clean":
        repos = sub_args["<repo>"]
        repos = repos or None

        retcode = core.clean(
            repo_names=repos, 
            recurse_into_dir=sub_args.get("-d"),
            force=sub_args.get("--force"),
            dry_run=sub_args.get("--dry-run")
        )

    return retcode


def cli_entrypoint():
    """Used by setup.py to create a cli entrypoint script."""
    try:
        cli_args, sub_args = parse_cli()
        exit_code = run(cli_args, sub_args)
        sys.exit(exit_code)
    except Exception:
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
