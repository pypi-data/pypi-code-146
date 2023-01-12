from __future__ import annotations

import logging
import os
import signal
import time
from argparse import ArgumentParser
from glob import glob
from os.path import abspath, dirname, join

from _pytest.config import ExitCode
from _pytest.config import main as pytest_main

from sila2_interop_communication_tester import test_server
from sila2_interop_communication_tester.test_server.helpers.spy import ARGS_DICT
from sila2_interop_communication_tester.test_server.server_implementation.server import Server
from sila2_interop_communication_tester.test_server.tests import conftest


def main(args: list[str] | None = None):
    # parse args
    parser = ArgumentParser(
        prog=test_server.__name__,
        description="SiLA 2 Server for testing client implementations",
    )
    parser.add_argument("tests", nargs="*", help="Tests to execute (default: all)")
    parser.add_argument("--report-file", default=None, help="If set, generate JUnit-like XML report file")
    parser.add_argument("--testsuite-name", default=None, help="Testsuite name for report file")
    parser.add_argument("--html-file", default=None, help="If set, generate HTML report file")
    parser.add_argument(
        "--server-address", default="127.0.0.1:50052", help="Server address (default: '127.0.0.1:50052')"
    )
    parser.add_argument(
        "--cert-file",
        default=None,
        help="PEM-encoded certificate file. If none, unencrypted communication is used",
    )
    parser.add_argument(
        "--key-file",
        default=None,
        help="PEM-encoded private key file. If none, unencrypted communication is used",
    )
    parsed_args = parser.parse_args(args)

    # configure logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s:%(levelname)s:%(message)s")

    # create and start server
    server = Server(parsed_args.server_address, cert_file=parsed_args.cert_file, key_file=parsed_args.key_file)
    server.start()
    print("Server started")

    # wait for shutdown
    signal.signal(signal.SIGINT, lambda *_: server.stop(10))  # handle interrupt signal (Ctrl+C)
    signal.signal(signal.SIGTERM, lambda *_: server.stop(10))  # handle termination signal
    server.wait_for_termination()
    print("Stopping server...")
    time.sleep(3)  # wait until all things are properly handled for pytest setup
    print("Server stopped")

    # switch to module directory
    original_dir = abspath(".")
    os.chdir(join(dirname(__file__), "tests"))
    tests_to_run: list[str] = glob("test_*") if parsed_args.tests is None else parsed_args.tests
    pytest_options: list[str] = [
        "-r A",  # print verbose test summary
    ]

    if parsed_args.report_file is not None:
        pytest_options.append(f"--junitxml={join(original_dir, parsed_args.report_file)}")
    if parsed_args.testsuite_name is not None:
        pytest_options.append("-o")
        pytest_options.append(f"junit_suite_name={parsed_args.testsuite_name}")
    if parsed_args.html_file is not None:
        pytest_options.append(f"--html={join(original_dir, parsed_args.html_file)}")
        pytest_options.append("--self-contained-html")

    conftest.RPC_CALL_ARGS = ARGS_DICT

    return pytest_main(args=tests_to_run + pytest_options)


if __name__ == "__main__":
    code = main()
    if isinstance(code, ExitCode):
        code = code.value

    exit(code)
