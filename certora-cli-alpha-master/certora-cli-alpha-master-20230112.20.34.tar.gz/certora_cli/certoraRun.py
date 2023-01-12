#!/usr/bin/env python3


import sys
import time
import logging
from typing import List, Optional
from pathlib import Path

scripts_dir_path = Path(__file__).parent.resolve()  # containing directory
sys.path.insert(0, str(scripts_dir_path))
from Shared.certoraUtils import run_jar_cmd
from Shared.certoraUtils import check_results_from_file, is_ci_or_git_action, run_local_spec_check
from Shared.certoraUtils import remove_file
from Shared.certoraUtils import CertoraUserInputError
from Shared.certoraUtils import get_certora_internal_dir, safe_create_dir
from Shared.certoraUtils import Mode, reset_certora_internal_dir
from Shared.certoraUtils import print_completion_message, mode_has_spec_file
from EVMVerifier.certoraCloudIO import CloudVerification, validate_version_and_branch
from EVMVerifier.certoraCollectRunMetadata import collect_run_metadata
from Shared.certoraLogging import LoggingManager
from EVMVerifier.certoraBuild import build
from EVMVerifier.certoraContext import get_local_run_cmd, get_args
from EVMVerifier import certoraContextVerifier as Cv

BUILD_SCRIPT_PATH = Path("EVMVerifier/certoraBuild.py")

# logger for issues regarding the general run flow.
# Also serves as the default logger for errors originating from unexpected places.
run_logger = logging.getLogger("run")


def run_certora(args: List[str], is_library: bool = False) -> Optional[Path]:
    """
    The main function that is responsible for the general flow of the script.
    The general flow is:
    1. Parse program arguments
    2. Run the necessary steps (type checking/ build/ cloud verification/ local verification)
    3. Shut down

    IMPORTANT - if run_certora is not run with is_library set to true we assume the scripts always reaches the
    shut down code. DO NOT USE SYS.EXIT() IN THE SCRIPT FILES!


    If is_library is set to False The program terminates with an exit code of 0 in case of success and 1 otherwise
    If is_library is set to True and the prover does not run locally the link to the status url is returned, else None
    is returned
    """

    # If we are not in debug mode, we do not want to print the traceback in case of exceptions.
    if '--debug' not in args:  # We check manually, because we want no traceback in argument parsing exceptions
        sys.tracebacklimit = 0

    # creating the default internal dir, files may be copied to user defined build directory after
    # parsing the input

    reset_certora_internal_dir()
    safe_create_dir(get_certora_internal_dir())
    LoggingManager()

    # adds ' around arguments with spaces
    pretty_args = [f"'{arg}'" if ' ' in str(arg) else str(arg) for arg in args]

    CL_ARGS = ' '.join(pretty_args)

    context, conf_dict = get_args(args)  # Parse arguments

    if context.short_output is False:
        if is_ci_or_git_action():
            context.short_output = True

    timings = {}
    exit_code = 0  # The exit code of the script. 0 means success, any other number is an error.
    return_value = None

    try:
        collect_run_metadata(wd=Path.cwd(), raw_args=sys.argv, conf_dict=conf_dict, context=context) \
            .dump()

        # When a TAC file is provided, no build arguments will be processed
        if context.mode not in [Mode.TAC, Mode.REPLAY]:
            run_logger.debug(f"There is no TAC file. Going to script {BUILD_SCRIPT_PATH} to main_with_args()")
            build_start = time.perf_counter()

            # If we are not in CI, we also check the spec for Syntax errors.
            build(context, ignore_spec_syntax_check=is_library)
            build_end = time.perf_counter()
            timings["buildTime"] = round(build_end - build_start, 4)

        if not context.build_only and exit_code == 0:  # either we skipped building (TAC MODE) or build succeeded
            if context.local:
                compare_with_expected_file = Path(context.expected_file).exists()
                specified_tool_output = context.tool_output is not None

                # If we want to compare results we have tell the jar where to store the output of the current run,
                # But we don't want to override the path if it was specified
                if compare_with_expected_file and not specified_tool_output:
                    context.tool_output = 'tmpOutput.json'

                check_cmd = get_local_run_cmd(context)

                # In local mode, this is reserved for Certora devs, so let the script print it
                print(f"Verifier run command:\n {check_cmd}", flush=True)
                run_result = \
                    run_jar_cmd(check_cmd, compare_with_expected_file, logger_topic="verification", print_output=True)
                if run_result != 0:
                    exit_code = 1
                else:
                    print_completion_message("Finished running verifier:")
                    print(f"\t{check_cmd}")

                    if compare_with_expected_file:
                        print("Comparing tool output to the expected output:")
                        result = check_results_from_file(context.tool_output, context.expected_file)
                        if not result:
                            exit_code = 1
                        if not specified_tool_output:
                            # Remove actual before starting the current test
                            remove_file(context.tool_output)

            else:  # Remote run
                # In cloud mode, we first run a local type checker

                '''
                Before running the local type checker, we see if the current package version is compatible with
                the latest. We check it before running the local type checker, because local type checking
                errors could be simply a result of syntax introduced in the newest version.
                The line below Will raise an exception if the local version is incompatible.
                '''
                validate_version_and_branch(context.cloud if context.cloud else context.staging)

                # Syntax checking and typechecking
                if mode_has_spec_file(context.mode):
                    if context.disableLocalTypeChecking:
                        run_logger.warning(
                            "Local checks of CVL specification files disabled. It is recommended to enable "
                            "the checks.")
                    else:
                        typechecking_start = time.perf_counter()
                        spec_check_failed = run_local_spec_check(with_typechecking=True)
                        if spec_check_failed:
                            raise CertoraUserInputError("Specification file error")
                        else:
                            typechecking_end = time.perf_counter()
                            timings['typecheckingTime'] = round(typechecking_end - typechecking_start, 4)

                if not context.typecheck_only and exit_code == 0:  # Local typechecking either succeeded or skipped
                    context.key = Cv.validate_certora_key()
                    cloud_verifier = CloudVerification(context, timings)

                    # Wrap strings with space with ' so it can be copied and pasted to shell
                    pretty_args = [f"'{arg}'" if ' ' in arg else arg for arg in args]
                    cl_args = ' '.join(pretty_args)

                    LoggingManager().remove_debug_logger()
                    result = cloud_verifier.cli_verify_and_report(cl_args, context.send_only)
                    if cloud_verifier.statusUrl:
                        return_value = Path(cloud_verifier.statusUrl)
                    if not result:
                        exit_code = 1

    except Exception as e:
        err_msg = "Encountered an error running Certora Prover"
        if isinstance(e, CertoraUserInputError):
            err_msg = f"{err_msg}:\n{e}"
        else:
            err_msg += ", please contact Certora"
            if not LoggingManager().is_debugging:
                err_msg += f"; consider running the script again with --debug to find out why it failed:\n" \
                           f"certoraRun {CL_ARGS} --debug"
        run_logger.debug("Failure traceback: ", exc_info=e)
        run_logger.fatal(err_msg)
        exit_code = 1
    except KeyboardInterrupt:
        print('\nInterrupted by user', flush=True)  # We go down a line because last characters in terminal were ^C
        sys.exit(1)  # We exit ALWAYS, even if we are running from a library

    # If the exit_code is 0, we do not call sys.exit() -> calling sys.exit() also exits any script that wraps this one
    if not is_library and exit_code != 0:
        sys.exit(exit_code)
    return return_value


def entry_point() -> None:
    """
    This function is the entry point of the certora_cli customer-facing package, as well as this script.
    It is important this function gets no arguments!
    """
    run_certora(sys.argv[1:], is_library=False)


if __name__ == '__main__':
    entry_point()
