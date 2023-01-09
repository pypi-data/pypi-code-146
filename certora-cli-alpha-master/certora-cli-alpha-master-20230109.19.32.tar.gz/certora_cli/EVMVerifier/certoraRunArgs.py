
import os
import sys
import argparse
import logging
import json
import shutil

from typing import Dict, List, Optional, Tuple, Any

from pathlib import Path
from EVMVerifier.certoraRunInputValidation import check_mode_of_operation, check_args_post_argparse, UniqueStore
from EVMVerifier.certoraRunInputValidation import __check_no_pretty_quotes
import EVMVerifier.certoraRunType as Tc
from EVMVerifier.certoraConfigIO import write_output_conf_to_path
from EVMVerifier.certoraRunContext import CertoraContext
from Shared.certoraUtils import safe_create_dir, get_last_confs_directory
from EVMVerifier.certoraContextVerifier import CertoraContextVerifier, sort_deduplicate_list_args

scripts_dir_path = Path(__file__).parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))

from Shared import certoraUtils as Util
from Shared.certoraLogging import LoggingManager
from EVMVerifier.certoraConfigIO import read_from_conf_file, current_conf_to_file, read_from_conf
arg_logger = logging.getLogger("arguments")


def __get_argparser() -> argparse.ArgumentParser:
    """
    @return: argparse.ArgumentParser with all relevant option arguments, types and logic.

    Do not use `default` as this will cause the conf file loading to be incorrect (conf file will consider the default
    as a user-override, even if the user did not override the option).
    """

    parser = argparse.ArgumentParser(prog="certora-cli arguments and options", allow_abbrev=False)
    parser.add_argument('files', type=Tc.type_input_file, nargs='*',
                        help='[contract.sol[:contractName] ...] or CONF_FILE.conf or TAC_FILE.tac')

    mode_args = parser.add_argument_group("Mode of operation. Please choose one, unless using a .conf or .tac file")
    mode_args.add_argument("--verify", nargs='+', type=Tc.type_verify_arg, action='append',
                           help='Matches specification files to contracts. For example: '
                                '--verify [contractName:specName.spec ...]')
    mode_args.add_argument("--assert", nargs='+', dest='assert_contracts', type=Tc.type_contract, action='append',
                           help='The list of contracts to assert. Usage: --assert [contractName ...]')
    mode_args.add_argument("--bytecode", nargs='+', dest='bytecode_jsons', type=Tc.type_json_file, action='append',
                           help='List of EVM bytecode json descriptors. Usage: --bytecode [bytecode1.json ...]')
    mode_args.add_argument("--bytecode_spec", type=Tc.type_readable_file, action=UniqueStore,
                           help='Spec to use for the provided bytecodes. Usage: --bytecode_spec myspec.spec')

    # ~~ Useful arguments ~~

    useful_args = parser.add_argument_group("Most frequently used options")
    useful_args.add_argument("--msg", help='Add a message description (alphanumeric string) to your run.',
                             action=UniqueStore)
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

    run_args.add_argument("--rule_sanity", action=UniqueStore,
                          type=Tc.type_rule_sanity_flag,
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
    solidity_args.add_argument("--solc", action=UniqueStore, help="Path to the solidity compiler executable file")
    solidity_args.add_argument("--solc_args", type=Tc.type_list, action=UniqueStore,
                               help="List of string arguments to pass for the Solidity compiler, for example: "
                                    "\"['--evm-version', 'istanbul', '--experimental-via-ir']\"")
    solidity_args.add_argument("--solc_map", action=UniqueStore, type=Tc.type_solc_map,
                               help="Matches each Solidity file with a Solidity compiler executable. "
                                    "Usage: <sol_file_1>=<solc_1>,<sol_file_2>=<solc_2>[,...] ")
    solidity_args.add_argument("--path", type=Tc.type_dir, action=UniqueStore,
                               help='Use the given path as the root of the source tree instead of the root of the '
                                    'filesystem. Default: $PWD/contracts if exists, else $PWD')
    solidity_args.add_argument("--optimize", type=Tc.type_non_negative_integer, action=UniqueStore,
                               help="Tells the Solidity compiler to optimize the gas costs of the contract for a given "
                                    "number of runs")
    solidity_args.add_argument("--optimize_map", type=Tc.type_optimize_map, action=UniqueStore,
                               help="Matches each Solidity source file with a number of runs to optimize for. "
                                    "Usage: <sol_file_1>=<num_runs_1>,<sol_file_2>=<num_runs_2>[,...]")

    # ~~ Package arguments (mutually exclusive) ~~
    solidity_args.add_argument("--packages_path", type=Tc.type_dir, action=UniqueStore,
                               help="Path to a directory including the Solidity packages (default: $NODE_PATH)")
    solidity_args.add_argument("--packages", nargs='+', type=Tc.type_package, action=UniqueStore,
                               help='A mapping [package_name=path, ...]')

    # ~~ Loop handling arguments ~~

    loop_args = parser.add_argument_group("Options regarding source code loops")
    loop_args.add_argument("--optimistic_loop", action='store_true',
                           help="After unrolling loops, assume the loop halt conditions hold")
    loop_args.add_argument("--loop_iter", type=Tc.type_non_negative_integer, action=UniqueStore,
                           help="The maximal number of loop iterations we verify for. Default: 1")

    # ~~ Options that help reduce the running time ~~

    run_time_args = parser.add_argument_group("Options that help reduce running time")

    # Currently the jar only accepts a single rule with -rule
    run_time_args.add_argument("--method", action=UniqueStore, type=Tc.type_method,
                               help="Parametric rules will only verify given method. "
                                    "Usage: --method 'fun(uint256,bool)'")
    run_time_args.add_argument("--cache", help='name of the cache to use', action=UniqueStore)
    run_time_args.add_argument("--smt_timeout", type=Tc.type_positive_integer, action=UniqueStore,
                               help="Set max timeout for all SMT solvers in seconds, default is 600")

    # ~~ Linkage arguments ~~

    linkage_args = parser.add_argument_group("Options to set addresses and link contracts")
    linkage_args.add_argument("--link", nargs='+', type=Tc.type_link_arg, action='append',
                              help='Links a slot in a contract with another contract. Usage: ContractA:slot=ContractB')
    linkage_args.add_argument("--address", nargs='+', type=Tc.type_address, action=UniqueStore,
                              help='Set an address manually. Default: automatic assignment by the python script. '
                                   'Format: <contractName>:<number>')
    linkage_args.add_argument("--structLink", nargs='+', type=Tc.type_struct_link, action=UniqueStore,
                              dest='struct_link',
                              help='Linking to a struct field, <contractName>:<number>=<contractName>')

    # ~~ Dynamic creation arguments ~~
    creation_args = parser.add_argument_group("Options to model contract creation")
    creation_args.add_argument("--prototype", nargs='+', type=Tc.type_prototype_arg, action='append',
                               help="Execution of constructor bytecode with the given prefix should yield a unique"
                                    "instance of the given contract")
    creation_args.add_argument("--dynamic_bound", type=Tc.type_non_negative_integer, action=UniqueStore,
                               help="Maximum number of instances of a contract that can be created "
                                    "with the CREATE opcode; if 0, CREATE havocs (default: 0)")
    creation_args.add_argument("--dynamic_dispatch", action="store_true",
                               help="If set, on a best effort basis automatically use dispatcher summaries for external"
                                    " calls on contract instances generated by CREATE"
                               )
    # ~~ Debugging arguments ~~
    info_args = parser.add_argument_group("Debugging options")
    info_args.add_argument("--debug", nargs='?', default=None, const=[], action=Tc.SplitArgsByCommas,
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
    java_args.add_argument("--jar", type=Tc.type_jar, action=UniqueStore, help=argparse.SUPPRESS)

    # arguments to pass to the .jar file
    java_args.add_argument("--javaArgs", type=Tc.type_java_arg, action='append', dest='java_args',
                           help=argparse.SUPPRESS)

    # ~~ Partial run arguments ~~

    partial_args = parser.add_argument_group("These arguments run only specific parts of the tool, or skip parts")

    # used for debugging command line option parsing.
    partial_args.add_argument('--check_args', action='store_true', help=argparse.SUPPRESS)

    # used for debugging the build only
    partial_args.add_argument('--build_only', action='store_true', help=argparse.SUPPRESS)

    partial_args.add_argument("--build_dir", action=UniqueStore, type=Tc.type_build_dir,
                              help="Path to the build directory")

    # A setting for disabling the local type checking (e.g., if we have a bug in the jar published with the python and
    # want users not to get stuck and get the type checking from the cloud instead).
    partial_args.add_argument('--disableLocalTypeChecking', action='store_true', help=argparse.SUPPRESS)

    # Do not compare the verification results with expected.json
    partial_args.add_argument("--no_compare", action='store_true', help=argparse.SUPPRESS)
    partial_args.add_argument("--expected_file", type=Tc.type_optional_readable_file, action=UniqueStore,
                              help='JSON file to use as expected results for comparing the output')

    # ~~ Cloud control arguments ~~

    cloud_args = parser.add_argument_group("Fine cloud control arguments")

    cloud_args.add_argument('--queue_wait_minutes', type=Tc.type_non_negative_integer, action=UniqueStore,
                            help=argparse.SUPPRESS)
    cloud_args.add_argument('--max_poll_minutes', type=Tc.type_non_negative_integer, action=UniqueStore,
                            help=argparse.SUPPRESS)
    cloud_args.add_argument('--log_query_frequency_seconds', type=Tc.type_non_negative_integer, action=UniqueStore,
                            help=argparse.SUPPRESS)
    cloud_args.add_argument('--max_attempts_to_fetch_output', type=Tc.type_non_negative_integer, action=UniqueStore,
                            help=argparse.SUPPRESS)
    cloud_args.add_argument('--delay_fetch_output_seconds', type=Tc.type_non_negative_integer, action=UniqueStore,
                            help=argparse.SUPPRESS)
    cloud_args.add_argument('--process', action=UniqueStore, default='emv', help=argparse.SUPPRESS)

    # ~~ Miscellaneous hidden arguments ~~

    misc_hidden_args = parser.add_argument_group("Miscellaneous hidden arguments")

    misc_hidden_args.add_argument("--settings", type=Tc.type_settings_arg, action='append', help=argparse.SUPPRESS)

    misc_hidden_args.add_argument("--log_branch", action=UniqueStore, help=argparse.SUPPRESS)

    # Disable automatic cache key generation. Useful for CI testing
    misc_hidden_args.add_argument("--disable_auto_cache_key_gen", action='store_true', help=argparse.SUPPRESS)

    # If the control flow graph is deeper than this argument, do not draw it
    misc_hidden_args.add_argument("--max_graph_depth", type=Tc.type_non_negative_integer, action=UniqueStore,
                                  help=argparse.SUPPRESS)

    # Path to a directory at which tool output files will be saved
    misc_hidden_args.add_argument("--toolOutput", type=Tc.type_tool_output_path, action=UniqueStore, dest='tool_output',
                                  help=argparse.SUPPRESS)

    # A json file containing a map from public function signatures to internal function signatures for function finding
    # purposes
    misc_hidden_args.add_argument("--internal_funcs", type=Tc.type_json_file, action=UniqueStore,
                                  help=argparse.SUPPRESS)

    # Run in Coinbase features mode
    misc_hidden_args.add_argument("--coinbaseMode", action='store_true', help=argparse.SUPPRESS)

    # Generate only the .conf file
    misc_hidden_args.add_argument("--get_conf", type=Tc.type_conf_file, action=UniqueStore,
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
    env_args.add_argument("--staging", nargs='?', default=None, const="", action=UniqueStore, help=argparse.SUPPRESS)
    env_args.add_argument("--cloud", nargs='?', default=None, const="", action=UniqueStore, help=argparse.SUPPRESS)

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

    check_mode_of_operation(context)  # Here context.mode is set

    if context.mode == Util.Mode.CONF:
        read_from_conf_file(context)
        # verifying context info that was stored in the conf file

    verifier = CertoraContextVerifier(context)
    verifier.verify()
    current_build_directory = Util.get_certora_internal_dir()
    if context.build_dir is not None and current_build_directory != context.build_dir:
        Util.reset_certora_internal_dir(context.build_dir)
        os.rename(current_build_directory, context.build_dir)

    LoggingManager().set_log_level_and_format(is_quiet=context.short_output, debug_topics=context.debug,
                                              show_debug_topics=context.debug_topics)
    last_conf_dir = get_last_confs_directory().resolve()
    safe_create_dir(last_conf_dir)

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

    check_args_post_argparse(context)
    setup_cache(context)  # Here context.cache, context.user_defined_cache are set

    # Setup defaults (defaults are not recorded in conf file)
    if context.expected_file is None:
        context.expected_file = "expected.json"

    arg_logger.debug("parsed args successfully.")
    arg_logger.debug(f"args= {context}")
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
        arg_logger.debug("using conf from replay to update args")
        read_from_conf(replay_conf, context)
    elif context_opt:
        arg_logger.debug("using args from replay file as args")
        context = context_opt
        # do our args postprocessing on the imported args
        flatten_arg_lists(context)
        check_mode_of_operation(context)


def dump_replay_files(replay_json_filename: Path) -> Tuple[Optional[Dict[str, Any]], Optional[CertoraContext]]:
    """
    Dump the replay data from the replay_json (files .certora_build.json, etc)
    Also return the config (format as in .conf files).
    :param replay_json_filename: json file with replay data
    :return: config as a json object in .conf file format, if available in the replay file, alternatively a namespace
        created from the raw_args entry in the replay file
    """
    with replay_json_filename.open() as replay_json_file:
        arg_logger.debug(f'Reading replay json configuration from: {Util.abs_posix_path(replay_json_filename)}')
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
            arg_logger.debug(f'deleting dir {Util.abs_posix_path(certora_config_dir)}')
            shutil.rmtree(certora_config_dir)

        arg_logger.debug(f'creating dir {Util.abs_posix_path(certora_config_dir)}')
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
                arg_logger.debug(f"dumping: {file_path_from_conf_dir}")
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
            arg_logger.debug(f'parsed back raw_args from replay json: {namespace}')
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
    __check_no_pretty_quotes(args_list)
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
    sort_deduplicate_list_args(context)


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
                arg_logger.debug(f"setting cache key to {context.cache}")
