import os
import sys
import argparse
import json
import shutil
import re
import logging
import itertools
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

scripts_dir_path = Path(__file__).parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))

from EVMVerifier.certoraContextClass import CertoraContext
from Shared import certoraUtils as Util
from Shared.certoraLogging import LoggingManager
from EVMVerifier.certoraConfigIO import read_from_conf_file, current_conf_to_file, read_from_conf
import EVMVerifier.certoraContextVerifier as Cv

context_logger = logging.getLogger("context")


def get_local_run_cmd(context: CertoraContext) -> str:
    """
    Assembles a jar command for local run
    @param context: A namespace including all command line input arguments
    @return: A command for running the prover locally
    """
    run_args = []
    if context.mode == Util.Mode.TAC:
        run_args.append(context.files[0])
    if context.cache is not None:
        run_args.extend(['-cache', context.cache])
    if context.tool_output is not None:
        run_args.extend(['-json', context.tool_output])
    if context.settings is not None:
        for setting in context.settings:
            run_args.extend(setting.split('='))
    if context.coinbaseMode:
        run_args.append(Util.COINBASE_FEATURES_MODE_CONFIG_FLAG)
    if context.skip_payable_envfree_check:
        run_args.append("-skipPayableEnvfreeCheck")
    run_args.extend(['-buildDirectory', str(Util.get_certora_internal_dir())])
    if context.jar is not None:
        jar_path = context.jar
    else:
        certora_root_dir = Util.get_certora_root_directory().as_posix()
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
            raise Util.CertoraUserInputError(f"slot {slot_a} was defined multiple times: {link_a}, {link_b}")


def __get_argparser() -> argparse.ArgumentParser:
    """
    @return: argparse.ArgumentParser with all relevant option arguments, types and logic.

    Do not use `default` as this will cause the conf file loading to be incorrect (conf file will consider the default
    as a user-override, even if the user did not override the option).
    """

    parser = argparse.ArgumentParser(prog="certora-cli arguments and options", allow_abbrev=False)
    parser.add_argument('files', type=Cv.type_input_file, nargs='*',
                        help='[contract.sol[:contractName] ...] or CONF_FILE.conf or TAC_FILE.tac')

    mode_args = parser.add_argument_group("Mode of operation. Please choose one, unless using a .conf or .tac file")
    mode_args.add_argument("--verify", nargs='+', type=Cv.type_verify_arg, action='append',
                           help='Matches specification files to contracts. For example: '
                                '--verify [contractName:specName.spec ...]')
    mode_args.add_argument("--assert", nargs='+', dest='assert_contracts', type=Cv.type_contract, action='append',
                           help='The list of contracts to assert. Usage: --assert [contractName ...]')
    mode_args.add_argument("--bytecode", nargs='+', dest='bytecode_jsons', type=Cv.type_json_file, action='append',
                           help='List of EVM bytecode json descriptors. Usage: --bytecode [bytecode1.json ...]')
    mode_args.add_argument("--bytecode_spec", type=Cv.type_readable_file, action=Cv.UniqueStore,
                           help='Spec to use for the provided bytecodes. Usage: --bytecode_spec myspec.spec')

    # ~~ Useful arguments ~~

    useful_args = parser.add_argument_group("Most frequently used options")
    useful_args.add_argument("--msg", help='Add a message description (alphanumeric string) to your run.',
                             action=Cv.UniqueStore)
    useful_args.add_argument("--rule", "--rules", nargs='+', action='append',
                             help="List of specific properties (rules or invariants) you want to verify. "
                                  "Usage: --rule [rule1 rule2 ...] or --rules [rule1 rule2 ...]")

    # ~~ Run arguments ~~

    run_args = parser.add_argument_group("Options affecting the type of verification run")
    run_args.add_argument("--multi_assert_check", action='store_true',
                          help="Check each assertion separately by decomposing every rule "
                               "into multiple sub-rules, each of which checks one assertion while it assumes all "
                               "preceding assertions")

    run_args.add_argument("--include_empty_fallback", action='store_true',
                          help="check the fallback method, even if it always reverts")

    run_args.add_argument("--rule_sanity", action=Cv.UniqueStore,
                          type=Cv.type_rule_sanity_flag,
                          nargs="?",
                          default=None,  # default when no --rule_sanity given, may take from --settings
                          const="basic",  # default when --rule_sanity is given, but no argument to it
                          help="Sanity checks for all the rules")

    run_args.add_argument("--short_output", action='store_true',
                          help="Reduces verbosity. It is recommended to use this option in continuous integration")

    # used for build + typechecking only (relevant only when sending to cloud)
    run_args.add_argument('--typecheck_only', action='store_true', help='Stop after typechecking')

    # when sending to the cloud, do not wait for the results
    '''
    Note: --send_only also implies --short_output.
    '''
    run_args.add_argument('--send_only', action='store_true', help='Do not wait for verifications results')

    # ~~ Solidity arguments ~~

    solidity_args = parser.add_argument_group("Options that control the Solidity compiler")
    solidity_args.add_argument("--solc", action=Cv.UniqueStore, help="Path to the solidity compiler executable file")
    solidity_args.add_argument("--solc_args", type=Cv.type_list, action=Cv.UniqueStore,
                               help="List of string arguments to pass for the Solidity compiler, for example: "
                                    "\"['--evm-version', 'istanbul', '--experimental-via-ir']\"")
    solidity_args.add_argument("--solc_map", action=Cv.UniqueStore, type=Cv.type_solc_map,
                               help="Matches each Solidity file with a Solidity compiler executable. "
                                    "Usage: <sol_file_1>=<solc_1>,<sol_file_2>=<solc_2>[,...] ")
    solidity_args.add_argument("--path", type=Cv.type_dir, action=Cv.UniqueStore,
                               help='Use the given path as the root of the source tree instead of the root of the '
                                    'filesystem. Default: $PWD/contracts if exists, else $PWD')
    solidity_args.add_argument("--optimize", type=Cv.type_non_negative_integer, action=Cv.UniqueStore,
                               help="Tells the Solidity compiler to optimize the gas costs of the contract for a given "
                                    "number of runs")
    solidity_args.add_argument("--optimize_map", type=Cv.type_optimize_map, action=Cv.UniqueStore,
                               help="Matches each Solidity source file with a number of runs to optimize for. "
                                    "Usage: <sol_file_1>=<num_runs_1>,<sol_file_2>=<num_runs_2>[,...]")

    # ~~ Package arguments (mutually exclusive) ~~
    solidity_args.add_argument("--packages_path", type=Cv.type_dir, action=Cv.UniqueStore,
                               help="Path to a directory including the Solidity packages (default: $NODE_PATH)")
    solidity_args.add_argument("--packages", nargs='+', type=Cv.type_package, action=Cv.UniqueStore,
                               help='A mapping [package_name=path, ...]')

    # ~~ Loop handling arguments ~~

    loop_args = parser.add_argument_group("Options regarding source code loops")
    loop_args.add_argument("--optimistic_loop", action='store_true',
                           help="After unrolling loops, assume the loop halt conditions hold")
    loop_args.add_argument("--loop_iter", type=Cv.type_non_negative_integer, action=Cv.UniqueStore,
                           help="The maximal number of loop iterations we verify for. Default: 1")

    # ~~ Options that help reduce the running time ~~

    run_time_args = parser.add_argument_group("Options that help reduce running time")

    # Currently the jar only accepts a single rule with -rule
    run_time_args.add_argument("--method", action=Cv.UniqueStore, type=Cv.type_method,
                               help="Parametric rules will only verify given method. "
                                    "Usage: --method 'fun(uint256,bool)'")
    run_time_args.add_argument("--cache", help='name of the cache to use', action=Cv.UniqueStore)
    run_time_args.add_argument("--smt_timeout", type=Cv.type_positive_integer, action=Cv.UniqueStore,
                               help="Set max timeout for all SMT solvers in seconds, default is 600")

    # ~~ Linkage arguments ~~

    linkage_args = parser.add_argument_group("Options to set addresses and link contracts")
    linkage_args.add_argument("--link", nargs='+', type=Cv.type_link_arg, action='append',
                              help='Links a slot in a contract with another contract. Usage: ContractA:slot=ContractB')
    linkage_args.add_argument("--address", nargs='+', type=Cv.type_address, action=Cv.UniqueStore,
                              help='Set an address manually. Default: automatic assignment by the python script. '
                                   'Format: <contractName>:<number>')
    linkage_args.add_argument("--structLink", nargs='+', type=Cv.type_struct_link, action=Cv.UniqueStore,
                              dest='struct_link',
                              help='Linking to a struct field, <contractName>:<number>=<contractName>')

    # ~~ Dynamic creation arguments ~~
    creation_args = parser.add_argument_group("Options to model contract creation")
    creation_args.add_argument("--prototype", nargs='+', type=Cv.type_prototype_arg, action='append',
                               help="Execution of constructor bytecode with the given prefix should yield a unique"
                                    "instance of the given contract")
    creation_args.add_argument("--dynamic_bound", type=Cv.type_non_negative_integer, action=Cv.UniqueStore,
                               help="Maximum number of instances of a contract that can be created "
                                    "with the CREATE opcode; if 0, CREATE havocs (default: 0)")
    creation_args.add_argument("--dynamic_dispatch", action="store_true",
                               help="If set, on a best effort basis automatically use dispatcher summaries for external"
                                    " calls on contract instances generated by CREATE"
                               )
    # ~~ Debugging arguments ~~
    info_args = parser.add_argument_group("Debugging options")
    info_args.add_argument("--debug", nargs='?', default=None, const=[], action=Cv.SplitArgsByCommas,
                           help="Use this flag to see debug statements. A comma separated list filters logger topics")
    info_args.add_argument("--debug_topics", action="store_true", help="Include topic names in debug messages")

    # --version was handled before, it is here just for the help message
    info_args.add_argument('--version', action='version', help='Show the tool version',
                           version='This message should never be reached')

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Hidden flags ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    # ~~ Java arguments ~~

    java_args = parser.add_argument_group("Arguments passed to the .jar file")

    # Path to the Certora prover's .jar file
    java_args.add_argument("--jar", type=Cv.type_jar, action=Cv.UniqueStore, help=argparse.SUPPRESS)

    # arguments to pass to the .jar file
    java_args.add_argument("--javaArgs", type=Cv.type_java_arg, action='append', dest='java_args',
                           help=argparse.SUPPRESS)

    # ~~ Partial run arguments ~~

    partial_args = parser.add_argument_group("These arguments run only specific parts of the tool, or skip parts")

    # used for debugging command line option parsing.
    partial_args.add_argument('--check_args', action='store_true', help=argparse.SUPPRESS)

    # used for debugging the build only
    partial_args.add_argument('--build_only', action='store_true', help=argparse.SUPPRESS)

    partial_args.add_argument("--build_dir", action=Cv.UniqueStore, type=Cv.type_build_dir,
                              help="Path to the build directory")

    # A setting for disabling the local type checking (e.g., if we have a bug in the jar published with the python and
    # want users not to get stuck and get the type checking from the cloud instead).
    partial_args.add_argument('--disableLocalTypeChecking', action='store_true', help=argparse.SUPPRESS)

    # Do not compare the verification results with expected.json
    partial_args.add_argument("--no_compare", action='store_true', help=argparse.SUPPRESS)
    partial_args.add_argument("--expected_file", type=Cv.type_optional_readable_file, action=Cv.UniqueStore,
                              help='JSON file to use as expected results for comparing the output')

    # ~~ Cloud control arguments ~~

    cloud_args = parser.add_argument_group("Fine cloud control arguments")

    cloud_args.add_argument('--queue_wait_minutes', type=Cv.type_non_negative_integer, action=Cv.UniqueStore,
                            help=argparse.SUPPRESS)
    cloud_args.add_argument('--max_poll_minutes', type=Cv.type_non_negative_integer, action=Cv.UniqueStore,
                            help=argparse.SUPPRESS)
    cloud_args.add_argument('--log_query_frequency_seconds', type=Cv.type_non_negative_integer, action=Cv.UniqueStore,
                            help=argparse.SUPPRESS)
    cloud_args.add_argument('--max_attempts_to_fetch_output', type=Cv.type_non_negative_integer, action=Cv.UniqueStore,
                            help=argparse.SUPPRESS)
    cloud_args.add_argument('--delay_fetch_output_seconds', type=Cv.type_non_negative_integer, action=Cv.UniqueStore,
                            help=argparse.SUPPRESS)
    cloud_args.add_argument('--process', action=Cv.UniqueStore, default='emv', help=argparse.SUPPRESS)

    # ~~ Miscellaneous hidden arguments ~~

    misc_hidden_args = parser.add_argument_group("Miscellaneous hidden arguments")

    misc_hidden_args.add_argument("--settings", type=Cv.type_settings_arg, action='append', help=argparse.SUPPRESS)

    misc_hidden_args.add_argument("--log_branch", action=Cv.UniqueStore, help=argparse.SUPPRESS)

    # Disable automatic cache key generation. Useful for CI testing
    misc_hidden_args.add_argument("--disable_auto_cache_key_gen", action='store_true', help=argparse.SUPPRESS)

    # If the control flow graph is deeper than this argument, do not draw it
    misc_hidden_args.add_argument("--max_graph_depth", type=Cv.type_non_negative_integer, action=Cv.UniqueStore,
                                  help=argparse.SUPPRESS)

    # Path to a directory at which tool output files will be saved
    misc_hidden_args.add_argument("--toolOutput", type=Cv.type_tool_output_path, action=Cv.UniqueStore,
                                  dest='tool_output', help=argparse.SUPPRESS)

    # A json file containing a map from public function signatures to internal function signatures for function finding
    # purposes
    misc_hidden_args.add_argument("--internal_funcs", type=Cv.type_json_file, action=Cv.UniqueStore,
                                  help=argparse.SUPPRESS)

    # Run in Coinbase features mode
    misc_hidden_args.add_argument("--coinbaseMode", action='store_true', help=argparse.SUPPRESS)

    # Generate only the .conf file
    misc_hidden_args.add_argument("--get_conf", type=Cv.type_conf_file, action=Cv.UniqueStore,
                                  help=argparse.SUPPRESS)

    # Turn on the prover -skipPayableEnvfreeCheck flag.
    misc_hidden_args.add_argument("--skip_payable_envfree_check", action="store_true", help=argparse.SUPPRESS)

    # ~~ Running Environment arguments ~~
    """
    IMPORTANT: This argument group must be last!
    There is a known bug in generating the help text when adding a mutually exclusive group with all its options as
    suppressed. For details, see:
    https://stackoverflow.com/questions/60565750/python-argparse-assertionerror-when-using-mutually-exclusive-group
    """

    env_args = parser.add_mutually_exclusive_group()
    env_args.add_argument("--staging", nargs='?', default=None, const="", action=Cv.UniqueStore, help=argparse.SUPPRESS)
    env_args.add_argument("--cloud", nargs='?', default=None, const="", action=Cv.UniqueStore, help=argparse.SUPPRESS)

    return parser


def get_args(args_list: Optional[List[str]] = None) -> Tuple[CertoraContext, Dict[str, Any]]:
    if args_list is None:
        args_list = sys.argv

    '''
    Compiles an argparse.Namespace from the given list of command line arguments.
    Additionally returns the prettified dictionary version of the input arguments as generated by current_conf_to_file
    and printed to the .conf file in .lastConfs.

    Why do we handle --version before argparse?
    Because on some platforms, mainly CI tests, we cannot fetch the installed distribution package version of
    certora-cli. We want to calculate the version lazily, only when --version was invoked.
    We do it pre-argparse, because we do not care bout the input validity of anything else if we have a --version flag
    '''
    handle_version_flag(args_list)

    pre_arg_fetching_checks(args_list)
    parser = __get_argparser()

    # if there is a --help flag, we want to ignore all parsing errors, even those before it:
    if '--help' in args_list:
        parser.print_help()
        exit(0)

    args = parser.parse_args(args_list)
    context = CertoraContext(**vars(args))

    __remove_parsing_whitespace(args_list)
    format_input(context)

    Cv.check_mode_of_operation(context)  # Here context.mode is set

    if context.mode == Util.Mode.CONF:
        read_from_conf_file(context)
        # verifying context info that was stored in the conf file

    verifier = Cv.CertoraContextVerifier(context)
    verifier.verify()
    current_build_directory = Util.get_certora_internal_dir()
    if context.build_dir is not None and current_build_directory != context.build_dir:
        Util.reset_certora_internal_dir(context.build_dir)
        os.rename(current_build_directory, context.build_dir)

    LoggingManager().set_log_level_and_format(is_quiet=context.short_output, debug_topics=context.debug,
                                              show_debug_topics=context.debug_topics)
    last_conf_dir = Util.get_last_confs_directory().resolve()
    Util.safe_create_dir(last_conf_dir)

    if context.mode == Util.Mode.REPLAY:
        prepare_replay_mode(context)

    # Store current options (including the ones read from .conf file)
    conf_options = current_conf_to_file(context)

    if '--get_conf' in args_list:
        del conf_options["get_conf"]
        write_output_conf_to_path(conf_options, Path(context.get_conf))
        sys.exit(0)

    # set this environment variable if you want to only get the .conf file and terminate.
    # This helps tools like the mutation tester that need to modify the arguments to the run scripts.
    # Dumping the conf file lets us use the json library to modify the args and not tamper with the .sh files
    # via string ops (which is a really bad idea).
    # NOTE: if you want to run multiple CVT instances simultaneously,
    # you should use consider the --get_conf flag and not this.
    conf_path = os.environ.get("CERTORA_DUMP_CONFIG")
    if conf_path is not None:
        write_output_conf_to_path(conf_options, Path(conf_path))
        sys.exit(0)

    Cv.check_args_post_argparse(context)
    setup_cache(context)  # Here context.cache, context.user_defined_cache are set

    # Setup defaults (defaults are not recorded in conf file)
    if context.expected_file is None:
        context.expected_file = "expected.json"

    context_logger.debug("parsed args successfully.")
    context_logger.debug(f"args= {context}")
    if context.check_args:
        sys.exit(0)
    return context, conf_options


def print_version() -> None:
    package_name, version = Util.get_package_and_version()
    print(f"{package_name} {version}")


def handle_version_flag(args_list: List[str]) -> None:
    for arg in args_list:
        if arg == "--version":
            print_version()  # exits the program
            exit(0)


def __remove_parsing_whitespace(arg_list: List[str]) -> None:
    """
    Removes all whitespaces added to args by __alter_args_before_argparse():
    1. A leading space before a dash (if added)
    2. space between commas
    :param arg_list: A list of options as strings.
    """
    for idx, arg in enumerate(arg_list):
        arg_list[idx] = arg.strip().replace(', ', ',')


def prepare_replay_mode(context: CertoraContext) -> None:
    """
    extract all input files from json and dump them
     - a conf file will be used as in CONF mode
     - .certora_build.json and .certora_verify.json will be used as if they
       had been produced by certoraBuild.py:build(..)
    """
    print('Got a .json file as input. Running in replay mode.')
    replay_json_filename = Path(context.files[0])
    replay_conf, context_opt = dump_replay_files(replay_json_filename)
    if replay_conf:
        context_logger.debug("using conf from replay to update args")
        read_from_conf(replay_conf, context)
    elif context_opt:
        context_logger.debug("using args from replay file as args")
        context = context_opt
        # do our args postprocessing on the imported args
        flatten_arg_lists(context)
        Cv.check_mode_of_operation(context)


def dump_replay_files(replay_json_filename: Path) -> Tuple[Optional[Dict[str, Any]], Optional[CertoraContext]]:
    """
    Dump the replay data from the replay_json (files .certora_build.json, etc)
    Also return the config (format as in .conf files).
    :param replay_json_filename: json file with replay data
    :return: config as a json object in .conf file format, if available in the replay file, alternatively a namespace
        created from the raw_args entry in the replay file
    """
    with replay_json_filename.open() as replay_json_file:
        context_logger.debug(f'Reading replay json configuration from: {Util.abs_posix_path(replay_json_filename)}')
        replay_json = json.load(replay_json_file)
        repro = replay_json['reproduction']
        certora_config_dir = Util.get_certora_config_dir()
        # dump certora_[build,verify,metadata]
        pairs = [(repro['certoraMetaData'], Util.get_certora_metadata_file()),
                 (repro['certoraBuild'], Util.get_certora_build_file()),
                 (repro['certoraVerify'], Util.get_certora_verify_file()),
                 ]

        for json_data, dump_target_name in pairs:
            with dump_target_name.open("w") as dump_target:
                json.dump(json_data, dump_target)

        # dump certora_settings (directory and all contents)
        if certora_config_dir.is_dir():
            context_logger.debug(f'deleting dir {Util.abs_posix_path(certora_config_dir)}')
            shutil.rmtree(certora_config_dir)

        context_logger.debug(f'creating dir {Util.abs_posix_path(certora_config_dir)}')
        certora_config_dir.mkdir()

        for file_name, file_contents in repro['certoraConfig'].items():
            split_path = Path(file_name).parts

            split_path_from_configdir = split_path[split_path.index(certora_config_dir.name):]

            file_path_from_conf_dir = Util.path_in_certora_internal(Path(os.path.join(*split_path_from_configdir)))

            # Recursively create all the directories in the path of the extra directory, if they do not exist
            dir_containing_file = file_path_from_conf_dir.parent
            if not (Util.path_in_certora_internal(dir_containing_file).is_dir()):
                dir_containing_file.mkdir(parents=True, exist_ok=True)

            with file_path_from_conf_dir.open("w") as dump_target:
                context_logger.debug(f"dumping: {file_path_from_conf_dir}")
                dump_target.write(file_contents)

        # read conf (in .conf file format) from corresponding entry in json
        try:
            conf_json = repro['certoraMetaData']['conf']
            context = None
        except KeyError:
            # no conf entry, trying to reconstruct from raw_args
            raw_args = repro['certoraMetaData']['raw_args']
            __alter_args_before_argparse(raw_args)
            parser = __get_argparser()
            namespace = parser.parse_args(raw_args[1:])
            context = CertoraContext(**vars(namespace))
            context_logger.debug(f'parsed back raw_args from replay json: {namespace}')
            conf_json = None

    return conf_json, context


def __alter_args_before_argparse(args_list: List[str]) -> None:
    """
    This function is a hack so we can accept the old syntax and still use argparse.
    This function alters the CL input so that it will be parsed correctly by argparse.

    Currently, it fixes two issues:

    1. We want to accept --javaArgs '-a,-b'
    By argparse's default, it is parsed as two different arguments and not one string.
    The hack is to preprocess the arguments, replace the comma with a commaspace.

    2. A problem with --javaArgs -single_flag. The fix is to add a space before the dash artificially.

    NOTE: Must use remove_parsing_whitespace() to undo these changes on argparse.ArgumentParser.parse_args() output!
    :param args_list: A list of CLI options as strings
    """
    for idx, arg in enumerate(args_list):
        if isinstance(arg, str):
            if ',' in arg:
                args_list[idx] = arg.replace(",", ", ")
                arg = args_list[idx]
            if len(arg) > 1 and arg[0] == "-" and arg[1] != "-":  # fixes a problem with --javaArgs -single_flag
                args_list[idx] = " " + arg


def pre_arg_fetching_checks(args_list: List[str]) -> None:
    """
    This function runs checks on the raw arguments before we attempt to read them with argparse.
    We also replace certain argument values so the argparser will accept them.
    NOTE: use remove_parsing_whitespace() on argparse.ArgumentParser.parse_args() output!
    :param args_list: A list of CL arguments
    :raises CertoraUserInputError if there are errors (see individual checks for more details):
        - There are wrong quotation marks “ in use
    """
    Cv.__check_no_pretty_quotes(args_list)
    __alter_args_before_argparse(args_list)


def format_input(context: CertoraContext) -> None:
    """
    Formats the input as it was parsed by argParser. This allows for simpler reading and treatment of context
    * Removes whitespace from input
    * Flattens nested lists
    * Removes duplicate values in lists
    * Sorts values in lists in alphabetical order
    :param context: Namespace containing all command line arguments, generated by get_args()
    """
    flatten_arg_lists(context)
    __cannonize_settings(context)
    Cv.sort_deduplicate_list_args(context)


def flatten_arg_lists(context: CertoraContext) -> None:
    """
    Flattens lists of lists arguments in a given namespace.
    For example,
    [[a], [b, c], []] -> [a, b, c]

    This is applicable to all options that can be used multiple times, and each time get multiple arguments.
    For example: --assert, --verify and --link
    @param context: Namespace containing all command line arguments, generated by get_args()
    """
    for arg_name in vars(context):
        arg_val = getattr(context, arg_name)
        # We assume all list members are of the same type
        if isinstance(arg_val, list) and len(arg_val) > 0 and isinstance(arg_val[0], list):
            flat_list = Util.flatten_nested_list(arg_val)
            flat_list.sort()
            setattr(context, arg_name, flat_list)


def __cannonize_settings(context: CertoraContext) -> None:
    """
    Converts the context.settings into a standard form.
    The standard form is a single list of strings, each string contains no whitespace and represents a single setting
    (that might have one or more values assigned to it with an = sign).

    @dev - --settings are different from all other list arguments, which are formatted by flatten_list_arg(). This is
           because while settings can be inserted multiple times, each time it gets a single string argument (which
           contains multiple settings, separated by commas).

    @param context: Namespace containing all command line arguments, generated by get_args()
    """
    if not hasattr(context, 'settings') or context.settings is None:
        return

    all_settings = list()

    for setting_list in context.settings:
        # Split by commas followed by a dash UNLESS they are inside quotes. Each setting will start with a dash.
        for setting in Util.split_by_delimiter_and_ignore_character(setting_list, ", -", '"',
                                                                    last_delimiter_chars_to_include=1):

            '''
            Lines below remove whitespaces inside the setting argument.
            An example for when this might occur:
            -m 'foo(uint, uint)'
            will result in settings ['-m', 'foo(uint, uint)']
            We wish to replace it to be ['-m', '-foo(uint,uint)'], without the space after the comma
            '''
            setting_split = setting.strip().split('=')
            for i, setting_word in enumerate(setting_split):
                setting_split[i] = setting_word.replace(' ', '')

            setting = '='.join(setting_split)
            all_settings.append(setting)

    context.settings = all_settings


def setup_cache(context: CertoraContext) -> None:
    """
    Sets automatic caching up, unless it is disabled (only relevant in VERIFY and ASSERT modes).
    The list of contracts, optimistic loops and loop iterations are determining uniquely a cache key.
    If the user has set their own cache key, we will not generate an automatic cache key, but we will also mark it
    as a user defined cache key.

    This function first makes sure to set user_defined_cache to either True or False,
    and then if necessary, sets up the cache key value.
    """

    # we have a user defined cache key if the user provided a cache key
    context.user_defined_cache = context.cache is not None
    if not context.disable_auto_cache_key_gen and not os.environ.get("CERTORA_DISABLE_AUTO_CACHE") is not None:
        if context.mode == Util.Mode.VERIFY or context.mode == Util.Mode.ASSERT:
            if context.cache is None:
                optimistic_loop = context.optimistic_loop
                loop_iter = context.loop_iter
                files = sorted(context.files)
                context.cache = '-'.join(files) + f"-optimistic{optimistic_loop}-iter{loop_iter}"
                context_logger.debug(f"setting cache key to {context.cache}")


"""
dually-defined argumentsb are command line arguments that can also be passed as a setting.
For example, we can use either '--rule law' or '--settings -rule=law'
Another example is: '--loop_iter 2' or '--settings -b=2'

The argparser does not handle the value of --settings at all. This is so that jar developers can add flags quickly
 without changing the scripts.
"""

# Note: we do not check if the argument is defined in the ArgumentParser.
val_arg_to_setting = {
    'loop_iter': 'b',
    "rule_sanity": "ruleSanityChecks",
    'max_graph_depth': 'graphDrawLimit',
    'method': 'method',
    'smt_timeout': 't',
    'bytecode_spec': 'spec',
    'dynamic_bound': 'dynamicCreationBound',
    'tool_output': 'json'
}

val_arg_to_list_setting = {
    'bytecode_jsons': 'bytecode',
    'rule': 'rule'
}

setting_aliases = {
    'rule': 'rules',
    'rules': 'rules',
}

'''
The options below are boolean, and their default in the CVT is False. If in the future, the CVT default of an options
will change, we should remove that option from the dictionary.
'''
bool_arg_to_implicit_setting = {
    "optimistic_loop": "assumeUnwindCond",
    "multi_assert_check": "multiAssertCheck"}

'''
The options below are boolean, their default in the CVT is False, and require to explicitly set their value to true.
If in the future, the CVT default of an options will change, we should remove that option from the dictionary.
'''
bool_arg_to_explicit_setting = {
    'short_output': 'ciMode',
    "dynamic_dispatch": "dispatchOnCreated",
    "include_empty_fallback": "includeEmptyFallback"
}


def __check_single_arg_and_setting_consistency(context: CertoraContext, arg_name: str, setting_name: str,
                                               is_list_setting: bool) -> None:
    """
    We accept two syntaxes for settings: --rule or --settings -rule.
    This function checks that:
    1. The two syntaxes are consistent within the same command line (do not have contradicting values)
    2. The --settings syntax is consistent (gets a single setting -setting_name at most)
    3. If we use both the setting and the argument, warn of the redundancy

    After running this function, the value will be stored both in the settings and in context.
    The arguments in settings may now be unsorted.

    @param context: a namespace containing command line arguments
    @param arg_name: name of the argument, for example: --rule or --loop_iterations
    @param setting_name: name of the setting, for example: -rule or -b
    @raises CertoraUserInputError if there is an inconsistent use of the argument.
    """
    setting_value = None
    all_settings_vals = set()
    setting_names = [setting_name]
    if setting_name in setting_aliases:
        setting_names.append(setting_aliases[setting_name])
    if context.settings is not None:
        for setting in context.settings:
            for sname in setting_names:
                setting_match = re.search(r'^-' + sname + r'(\S*)', setting)
                if setting_match is not None:
                    curr_val = setting_match[1]
                    if curr_val == "" or curr_val == "=":
                        raise Util.CertoraUserInputError(f"No value was provided for setting {sname}")
                    if re.search(r"^=[^=\s]+", curr_val):
                        if curr_val in all_settings_vals:
                            context_logger.warning(
                                f"Used --settings -{sname} more than once with the same value: {setting}"
                            )
                        all_settings_vals.add(curr_val[1:])  # remove the leading =
                    elif not re.search(r"^\w+(=[^=\s]+)?$", curr_val):
                        # there might a setting for which this setting is a substring, like -rule and -ruleSanityChecks
                        raise Util.CertoraUserInputError(f"wrong syntax for --settings -{arg_name}: {setting}")
        if len(all_settings_vals) > 1:
            all_vals_str = ' '.join(sorted(list(all_settings_vals)))
            raise Util.CertoraUserInputError(
                f"Multiples values were given to setting {setting_name}: {all_vals_str}")
        if len(all_settings_vals) > 0:
            setting_value = list(all_settings_vals)[0]

    arg_val = getattr(context, arg_name, None)
    if arg_val is not None:
        if is_list_setting:
            arg_val = ','.join(arg_val)
        else:
            arg_val = arg_val.replace(' ', '')
            # needed in case where we have --method foo(bool,address),
            # as we include an artificial space after the comma inside the parenthesis

    if arg_val is None and setting_value is None:
        return

    # given both as an argument and as a setting
    if arg_val is not None and setting_value is not None and arg_val != setting_value:
        raise Util.CertoraUserInputError(
            f"There is a conflict between argument {arg_name} value of {arg_val} "
            f"and --settings -{setting_name} value of {setting_value}")

    if arg_val is None:  # backfill argument
        setattr(context, arg_name, setting_value)  # settings value is not None

    if setting_value is None:  # backfill settings
        settings_str = f'-{setting_name}={arg_val}'
        if context.settings is None:
            context.settings = list()
        context.settings.append(settings_str)  # it is now unsorted!


def __check_bool_arg_and_implicit_setting_consistency(context: CertoraContext, arg_name: str,
                                                      setting_name: str) -> None:
    """
    We accept two syntaxes for settings: --rule or --settings -rule.
    This function checks boolean settings, that can either appear, or not.
    This function reverts if a value is erroneously given to the boolean setting.

    If we use both the setting and the argument syntaxes, we warn of the redundancy. We also warn if the setting is
     given more than once.

    After running this function, the value will be stored both in the settings and in the argument namespace.
    The order of flags in settings may now no longer be sorted alphabetically.

    @param context: a namespace containing command line arguments
    @param arg_name: name of the argument, for example: --optimistic_loop or --rule_sanity
    @param setting_name: name of the setting, for example: -assumeUnwindCondition or -ruleSanityChecks
    @raises CertoraUserInputError if there is an inconsistent use of the argument.
    """
    setting_appeared = False
    all_warnings = set()

    if context.settings is not None:
        for setting in context.settings:
            setting_match = re.search(r'^-' + setting_name + r'(=[^=]+)?$', setting)
            if setting_match is not None:
                if '=' in setting_match[0]:
                    raise Util.CertoraUserInputError(
                        f"Boolean setting {setting_name} cannot get a value, given {setting_match[1]}")
                if setting_appeared:
                    all_warnings.add(f"Setting {setting_name} appeared more than once, this is redundant")
                else:
                    setting_appeared = True

    arg_val = getattr(context, arg_name, None)
    if arg_val is not None and not isinstance(arg_val, bool):
        raise Util.CertoraUserInputError(f"value of {arg_name} must be a boolean (true or false) (was {arg_val})")
    arg_appeared = arg_val is not None and arg_val

    if not arg_appeared and not setting_appeared:
        return

    if not arg_appeared and setting_appeared:
        setattr(context, arg_name, True)
    elif arg_appeared and not setting_appeared:  # add value to settings
        settings_str = f'-{setting_name}'
        if context.settings is None:
            context.settings = list()
        context.settings.append(settings_str)  # the settings are now no longer sorted alphabetically
    else:  # both a setting and an argument were used
        all_warnings.add(f"Redundant use of argument {arg_name} and setting {setting_name}")

    for warning in all_warnings:
        context_logger.warning(warning)


def __check_bool_arg_and_explicit_setting_consistency(context: CertoraContext, arg_name: str,
                                                      setting_name: str) -> None:
    """
    We accept two syntaxes for settings: --rule or --settings -rule.
    This function checks boolean settings, that can appear with explicit value, like -ci_mode=true, or -ci_mode=false.
    We assume that by default the value of the setting is false. One can use -ci_mode=false, even though it should have
    no effect. --short_output, without any arguments, is the equivalent of -ci_mode=true.

    This function raises an exception if any of the following holds:
    1. The setting has no argument
    2. The setting has a non-boolean argument
    3. The settings appears multiple times with conflicting truth values, like --settings -ci_mode=false,-ci_mode=true
    4. The option appears, but also a setting with truth value false: --short_output --settings -ci_mode=false

    This function warns if it does not raise an exception, in each of the following redundant scenarios:
    1. The setting has truth value false
    2. We use both an option and a setting with truth value true

    After running this function, the value will be stored both in the settings and in the argument namespace.
    The order of flags in settings may now no longer be sorted alphabetically.

    @param context: a namespace containing command line arguments
    @param arg_name: name of the argument, for example: --optimistic_loop or --rule_sanity
    @param setting_name: name of the setting, for example: -assumeUnwindCondition or -ruleSanityChecks
    @raises CertoraUserInputError if there is an inconsistent use of the argument.
    """
    setting_truth_val = None
    all_warnings = set()

    if context.settings is not None:
        for setting in context.settings:
            setting_match = re.search(r'^-' + setting_name + r'(=[^=]+)?$', setting)
            if setting_match is not None:
                setting_expr = setting_match[0]
                if '=' not in setting_expr:
                    raise Util.CertoraUserInputError(
                        f"Setting {setting_name} must get a boolean value: {setting_name}=true/false")
                else:
                    curr_truth_val = setting_match[0].split('=')[1].lower()
                    if curr_truth_val == 'true':
                        if setting_truth_val is None:
                            setting_truth_val = True
                        elif setting_truth_val:
                            all_warnings.add(f"setting {setting_name} was given the same value more than once: true")
                        else:
                            raise Util.CertoraUserInputError(
                                f"setting {setting_name} was given two conflicting values: true and false")
                    elif curr_truth_val == 'false':
                        if setting_truth_val is None:
                            setting_truth_val = False
                        elif not setting_truth_val:
                            all_warnings.add(f"setting {setting_name} was given the same value more than once: false")
                        else:
                            raise Util.CertoraUserInputError(
                                f"setting {setting_name} was given two conflicting values: true and false")
                    else:
                        raise Util.CertoraUserInputError(
                            f"Setting {setting_name} must get a boolean value: {setting_name}=true/false")

    arg_val = getattr(context, arg_name, None)
    if arg_val is not None and not isinstance(arg_val, bool):
        raise Util.CertoraUserInputError(f"value of {arg_name} must be a boolean (true or false) (was {arg_val})")

    arg_appeared = arg_val is not None and arg_val

    if not arg_appeared and setting_truth_val is None:
        return

    if not arg_appeared and setting_truth_val is not None:  # Add value to context
        setattr(context, arg_name, setting_truth_val)
    elif arg_appeared and setting_truth_val is None:  # add value to settings
        settings_str = f'-{setting_name}=true'
        if context.settings is None:
            context.settings = list()
        context.settings.append(settings_str)  # the settings are now no longer sorted alphabetically
    else:  # both a setting and an argument were used
        if not setting_truth_val:
            raise Util.CertoraUserInputError(f"{arg_name} and --setting -{setting_name}=false conflict each other")
        all_warnings.add(f"Redundant use of argument {arg_name} and setting {setting_name} with value false")

    for warning in all_warnings:
        context_logger.warning(warning)


def check_arg_and_setting_consistency(context: CertoraContext) -> None:
    """
    Check consistency for all dually-defined arguments.
    An argument is consistent if it has at most a single value.
    If an argument is defined both as a command-line argument and inside settings, we warn the user.
    At the end of this functions, all the dually-defined argument values will appears in both the argument namespace and
     inside the settings list in the namespace.
    context.settings will be sorted in ascending order.
    @param context: a namespace containing command line arguments
    @raises CertoraUserInputError if there is a dually-defined argument.
    """
    for (argument, setting) in val_arg_to_setting.items():
        __check_single_arg_and_setting_consistency(context, argument, setting, False)

    for (argument, setting) in val_arg_to_list_setting.items():
        __check_single_arg_and_setting_consistency(context, argument, setting, True)

    for (argument, setting) in bool_arg_to_implicit_setting.items():
        __check_bool_arg_and_implicit_setting_consistency(context, argument, setting)

    for (argument, setting) in bool_arg_to_explicit_setting.items():
        __check_bool_arg_and_explicit_setting_consistency(context, argument, setting)

    if context.settings is not None:
        context.settings.sort()

def write_output_conf_to_path(json_content: Dict[str, Any], path: Path) -> None:
    """
    Write the json object to the path
    @param json_content: the json object
    @param path: the location of the output path
    @:return: None
    """
    with path.open("w+") as out_file:
        json.dump(json_content, out_file, indent=4, sort_keys=True)
