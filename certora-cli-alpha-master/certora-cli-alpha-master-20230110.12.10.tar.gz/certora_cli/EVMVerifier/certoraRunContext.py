#!/usr/bin/env python3

import sys
import logging

from typing import List

import itertools
from pathlib import Path

scripts_dir_path = Path(__file__).parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))
from Shared.certoraUtils import get_certora_root_directory, COINBASE_FEATURES_MODE_CONFIG_FLAG
from Shared.certoraUtils import CertoraUserInputError, get_certora_internal_dir, Mode
from types import SimpleNamespace


class CertoraContext(SimpleNamespace):
    pass


# logger for issues regarding the general run flow.
# Also serves as the default logger for errors originating from unexpected places.
run_logger = logging.getLogger("run")


def get_local_run_cmd(context: CertoraContext) -> str:
    """
    Assembles a jar command for local run
    @param context: A namespace including all command line input arguments
    @return: A command for running the prover locally
    """
    run_args = []
    if context.mode == Mode.TAC:
        run_args.append(context.files[0])
    if context.cache is not None:
        run_args.extend(['-cache', context.cache])
    if context.tool_output is not None:
        run_args.extend(['-json', context.tool_output])
    if context.settings is not None:
        for setting in context.settings:
            run_args.extend(setting.split('='))
    if context.coinbaseMode:
        run_args.append(COINBASE_FEATURES_MODE_CONFIG_FLAG)
    if context.skip_payable_envfree_check:
        run_args.append("-skipPayableEnvfreeCheck")
    run_args.extend(['-buildDirectory', str(get_certora_internal_dir())])
    if context.jar is not None:
        jar_path = context.jar
    else:
        certora_root_dir = get_certora_root_directory().as_posix()
        jar_path = f"{certora_root_dir}/emv.jar"

    '''
    This flag prevents the focus from being stolen from the terminal when running the java process.
    Stealing the focus makes it seem like the program is not responsive to Ctrl+C.
    Nothing wrong happens if we include this flag more than once, so we always add it.
    '''
    java_args = "-Djava.awt.headless=true"
    if context.java_args is not None:
        java_args = f"{context.java_args} {java_args}"

    return " ".join(["java", java_args, "-jar", jar_path] + run_args)


def check_conflicting_link_args(context: CertoraContext) -> None:
    """
    Detects contradicting definitions of slots in link and throws.
    DOES NOT check for file existence, format legality, or anything else.
    We assume the links contain no duplications.
    @param context: A namespace, where context.link includes a list of strings that are the link arguments
    @raise CertoraUserInputError if a slot was given two different definitions
    """
    pair_list = itertools.permutations(context.link, 2)
    for pair in pair_list:
        link_a = pair[0]
        link_b = pair[1]
        slot_a = link_a.split('=')[0]
        slot_b = link_b.split('=')[0]
        if slot_a == slot_b:
            raise CertoraUserInputError(f"slot {slot_a} was defined multiple times: {link_a}, {link_b}")


def __remove_parsing_whitespace(arg_list: List[str]) -> None:
    """
    Removes all whitespaces added to args by __alter_args_before_argparse():
    1. A leading space before a dash (if added)
    2. space between commas
    :param arg_list: A list of options as strings.
    """
    for idx, arg in enumerate(arg_list):
        arg_list[idx] = arg.strip().replace(', ', ',')
