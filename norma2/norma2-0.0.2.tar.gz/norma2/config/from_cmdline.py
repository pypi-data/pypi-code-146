import argparse
import os
import sys
from pathlib import Path
from typing import List, NoReturn, Optional

import shtab
from rich.console import Console
from rich_argparse import RawDescriptionRichHelpFormatter

from norma2.__dependencies__ import dependencies
from norma2.__version__ import __version__
from norma2.config.config_class import Config, OutputFormat

__FULL_DOC = f"""SOURCE:
    https://github.com/Saverio976/NorMatrix

UPDATE:
    - if you install it with 'pip'
        pip install -U norma2
    - if you install it with git
        git pull
    - other method:
        (do it yourself)

CONFIGS:
    norma2 can read a special json file for configuration.
    -> put a `.norma2.json` file on the path where you execute norma2
    -> and execute norma2 like you did it before

    default configuration file:
        ```json
        {{
            "libc_banned_func": {Config.libc_banned_func},
            "no_libc_banned_func": [],
            "file_extension_banned": {Config.file_extension_banned},
            "no_file_extension_banned": [],
            "preview": {Config.preview}
            "operators_plugin": {Config.operators_plugin}
        }}
        ```

for further information read the README.md on
https://github.com/Saverio976/NorMatrix
"""

options = [
    {
        "name_or_flags": ["--no-operators-plugin"],
        "params": {
            "action": "store_const",
            "dest": "operators_plugin",
            "const": not Config.operators_plugin,
            "default": Config.operators_plugin,
            "help": "remove the operators pluggin (because it print"
            " some false positiv for now)",
        },
    },
    {
        "name_or_flags": ["--preview"],
        "params": {
            "action": "store_const",
            "dest": "preview",
            "const": not Config.preview,
            "default": Config.preview,
            "help": "add some plugin that are added recently",
        },
    },
    {
        "name_or_flags": ["--only-errors"],
        "params": {
            "action": "store_const",
            "dest": "only_error",
            "const": not Config.only_error,
            "default": Config.only_error,
            "help": "print only bad files with errors",
        },
    },
    {
        "name_or_flags": ["--no-fclean"],
        "params": {
            "action": "store_const",
            "dest": "no_fclean",
            "const": not Config.no_fclean,
            "default": Config.no_fclean,
            "help": 'if you want norma2 dont do a "make fclean" at the end',
        },
    },
    {
        "name_or_flags": ["--link-line"],
        "params": {
            "action": "store_const",
            "dest": "link_line",
            "const": not Config.link_line,
            "default": Config.link_line,
            "help": 'to have the "link" to the file (in vscode terminal you can'  # noqa: E501
            " click it and it will open the file at the line of the error)",
        },
    },
    {
        "name_or_flags": ["--tests-run"],
        "params": {
            "action": "store_const",
            "dest": "pass_test",
            "const": not Config.pass_test,
            "default": Config.pass_test,
            "help": "run the unit tests for norma2",
        },
    },
    {
        "name_or_flags": ["--output"],
        "params": {
            "metavar": "format",
            "choices": OutputFormat.to_list(),
            "dest": "format",
            "default": Config.format,
            "help": f"tell which output format to use {OutputFormat.to_list()}"
            " ; for html the file is norma2-result.html;"
            " for md the file is norma2-result.md, other are on stdout",
        },
    },
    {
        "name_or_flags": ["paths"],
        "params": {
            "metavar": "paths",
            "nargs": "*",
            "default": Config.paths,
            "help": "list of path to check (default: the current working directory)",  # noqa: E501
        },
    },
    {
        "name_or_flags": ["--show-conf"],
        "params": {
            "action": "store_const",
            "dest": "show_config",
            "const": not Config.show_config,
            "default": Config.show_config,
            "help": "Show config after parsing cmdline argument and .norma2.json",  # noqa: E501
        },
    },
    {
        "name_or_flags": ["--debug"],
        "params": {
            "action": "store_const",
            "dest": "debug",
            "const": not Config.debug,
            "default": Config.debug,
            "help": "show debug output",
        },
    },
    {
        "name_or_flags": ["--only-exit-code"],
        "params": {
            "action": "store_const",
            "dest": "only_exit_code",
            "const": not Config.only_exit_code,
            "default": Config.only_exit_code,
            "help": "dont show anything, only exit 42 if norm error, else, 0",
        },
    },
    {
        "name_or_flags": ["--show-explanation"],
        "params": {
            "action": "store_const",
            "dest": "show_explanation",
            "const": not Config.show_explanation,
            "default": Config.show_explanation,
            "help": "show the pdf coding style explanation for each error",
        },
    },
    {
        "name_or_flags": ["--explain"],
        "params": {
            "dest": "explain_error",
            "metavar": "error",
            "nargs": 1,
            "type": str,
            "default": Config.explain_error,
            "help": "show the pdf coding style explanation for the error code specified",  # noqa: E501
        },
    },
    {
        "name_or_flags": ["--list-errors"],
        "params": {
            "action": "store_const",
            "dest": "list_errors",
            "const": not Config.list_errors,
            "default": Config.list_errors,
            "help": "list all norm errors that norma2 have registered",
        },
    },
    {
        "name_or_flags": ["--install-completion"],
        "params": {
            "action": "store_const",
            "dest": "install_completion",
            "const": True,
            "default": False,
            "help": "install norma2 completion (need root permission)",
        },
    },
    {
        "name_or_flags": ["--version"],
        "params": {
            "action": "store_const",
            "dest": "version",
            "const": True,
            "default": False,
            "help": "install norma2 completion (need root permission)",
        },
    },
]


def _parser(argv: Optional[List[str]] = None):
    parser = argparse.ArgumentParser(
        formatter_class=RawDescriptionRichHelpFormatter,
        description="Norm Checker For the C Epitech Coding Style",
        epilog=__FULL_DOC,
    )
    shtab.add_argument_to(parser, "--print-completion")
    for args in options:
        parser.add_argument(*args["name_or_flags"], **(args["params"]))
    result = parser.parse_args(argv)
    result.format = OutputFormat(result.format)
    result.explain_error = " ".join(result.explain_error)
    return result, parser


def install_completion(parser: argparse.ArgumentParser, config: Config) -> NoReturn:
    shell = ""
    nb_try = 0
    choices = {
        "bash": (
            shtab.complete_bash,
            f"{os.getenv('BASH_COMPLETION_COMPAT_DIR')}/norma2",
        ),
        "zsh": (shtab.complete_zsh, "/usr/local/share/zsh/site-functions/_norma2"),
    }
    while shell not in ("bash", "zsh"):
        shell = config.console.input("Enter shell: {bash,zsh}: ")
        nb_try += 1
        if nb_try > 3:
            print("please enter bash or zsh", config.console.stderr)
            sys.exit(2)
    func = choices[shell]
    completions = func[0](parser)
    directory = func[1].split(os.path.sep)
    for i in range(1, len(directory) - 1):
        path = os.path.sep.join(directory[: i + 1])
        os.makedirs(path, exist_ok=True)
    Path(func[1]).write_text(completions)
    config.console.print(f"Completions writed to {func[1]}\nYou can restart {shell}")
    sys.exit(0)


def print_version(console: Console) -> NoReturn:
    console.print(f"norma2: {__version__}")
    console.print(f"norma2 dependencies: {dependencies}")
    sys.exit(0)


def from_cmdline(console: Console, argv: Optional[List[str]] = None) -> Config:
    conf = Config(console)
    args, parser = _parser(argv)
    conf = conf + args
    if args.install_completion:
        install_completion(parser, conf)
    if args.version:
        print_version(console)
    return conf
