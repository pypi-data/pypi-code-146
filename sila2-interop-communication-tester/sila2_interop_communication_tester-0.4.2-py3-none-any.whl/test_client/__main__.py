from __future__ import annotations

import os
from argparse import ArgumentParser
from glob import glob
from os.path import abspath, dirname, join

import grpc
from _pytest.config import ExitCode
from _pytest.config import main as pytest_main

from sila2_interop_communication_tester import test_client

from . import conftest


def main(args: list[str] | None = None) -> int | ExitCode:
    parser = ArgumentParser(
        prog=test_client.__name__,
        description="SiLA 2 Client for testing server implementations",
    )
    parser.add_argument("tests", nargs="*", help="Tests to execute (default: all)", default=None)
    parser.add_argument("--report-file", default=None, help="If set, generate JUnit-like XML report file")
    parser.add_argument("--testsuite-name", default=None, help="Testsuite name for report file")
    parser.add_argument("--timeout", default=30, type=int, help="Timeout per test (default: 30 s, disable with 0)")
    parser.add_argument("--html-file", default=None, help="If set, generate HTML report file")
    parser.add_argument(
        "--server-address", default="127.0.0.1:50052", help="Server address (default: '127.0.0.1:50052')"
    )
    parser.add_argument(
        "--roots-cert-file",
        default=None,
        help="PEM-encoded root certificates file. If none, unencrypted communication is attempted",
    )
    parsed_args = parser.parse_args(args)

    original_dir = abspath(".")

    # switch to module directory
    os.chdir(dirname(__file__))
    tests_to_run: list[str] = glob("test_*/") if parsed_args.tests is None else parsed_args.tests

    pytest_options: list[str] = [
        "-r A",  # print verbose test summary
        "--timeout",
        f"{parsed_args.timeout}",
    ]

    if parsed_args.report_file is not None:
        pytest_options.append(f"--junitxml={join(original_dir, parsed_args.report_file)}")
    if parsed_args.testsuite_name is not None:
        pytest_options.append("-o")
        pytest_options.append(f"junit_suite_name={parsed_args.testsuite_name}")
    if parsed_args.html_file is not None:
        pytest_options.append(f"--html={join(original_dir, parsed_args.html_file)}")
        pytest_options.append("--self-contained-html")

    if parsed_args.roots_cert_file is None:
        conftest.CHANNEL = grpc.insecure_channel(parsed_args.server_address)
    else:
        with open(join(original_dir, parsed_args.roots_cert_file), "rb") as roots_cert_pem_fp:
            conftest.CHANNEL = grpc.secure_channel(
                parsed_args.server_address, credentials=grpc.ssl_channel_credentials(roots_cert_pem_fp.read())
            )

    return pytest_main(
        args=tests_to_run + pytest_options,
    )


if __name__ == "__main__":
    code = main()
    if isinstance(code, ExitCode):
        code = code.value

    exit(code)
