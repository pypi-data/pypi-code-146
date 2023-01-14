import sys
import time
from builtins import FileNotFoundError
import random

import getopt
import os
import shutil
import re

try:
    import nrobo.speedboat
except ModuleNotFoundError as mnfe:
    import speedboat
except ImportError as ie:
    from nrobo import speedboat


def run_tests(cli_switches):
    # print(sys.argv)

    from nrobo.helpers import common
    from nrobo.config import nRoboConfig

    # Create virtualenv venv
    speedboat.create_virtual_environment()

    # Install Requirements
    speedboat.install_requirements()

    print("\n\n\n")

    # Validate Command Line Switches if they are correct.
    # cli_switches = speedboat.validateCommandLineSwitches()

    # print(cli_switches)

    # Prepare test luncher
    test_launch_command = speedboat.prepare_test_launcher(cli_switches)
    print("Launch Command: {0}".format(test_launch_command))

    # Clean test_output directory for fresh test results
    speedboat.clean_test_output_directory()

    # do some pre launch security-backup checks
    print("Perform security-backup checks...")

    # delete package and reimport to handle circular import error
    del nrobo.security.security_checks  # delete package

    # reimport again
    from nrobo.security.security_checks import SecurityChecks

    # perform url security-backup check
    security_checks = SecurityChecks()
    # security_checks.perform_url_security_check()

    # Parse CLI commands
    # installer.parse_cli()

    # system_command("behave -f allure_behave.formatter:AllureFormatter -o %" + paths.TEST_ALLURE_REPORTS_DIR + "% ./features")
    # Launch tests-backup
    time.sleep(nRoboConfig.Waits.SLEEP_TIME.value)

    speedboat.system_command(test_launch_command)

    if speedboat.get_value_of_cli_switch(cli_switches, nRoboConfig.CommandLineSwitchesShort.REPORT_TYPE.value).lower() \
            == nRoboConfig.TestReportSettings.REPORT_TYPE_ALLURE.value.lower():
        # run and host allure report on local server
        speedboat.run_allure_report(cli_switches)


def launch():
    # Validate Command Line Switches if they are correct.
    cli_switches = speedboat.validateCommandLineSwitches()

    run_tests(cli_switches)
