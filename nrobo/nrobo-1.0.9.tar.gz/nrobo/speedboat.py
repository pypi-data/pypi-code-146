# Namastey world _/\_
# ===================
#
# This is "Birbal".
# A bot designed and developed at NamasteyDigitalIndia.com,
# That helps software companies and software teams in automating various testing tasks.
#
# This file is the entry point of the "Birbal Automation Framework", BAF.
# speedboat.py is the command line utility to install, debug and run your automation tests-backup.
#
# Author: Panchdev Singh Chauhan
# Email: erpanchdev@gmail.com

import shutil
import sys
import getopt
import random
import time
import os
import re

try:
    import security
except ModuleNotFoundError as e:
    import nrobo.security

try:
    from config import nRoboConfig
except ModuleNotFoundError as e:
    from nrobo.config import nRoboConfig

try:
    from nrobo.helpers import common
except ModuleNotFoundError as e:
    from helpers import common

try:
    from security.security_checks import SecurityChecks
except ModuleNotFoundError as e:
    from nrobo.security.security_checks import SecurityChecks

try:
    from helpers import common as common
except ModuleNotFoundError as e:
    from nrobo.helpers import common as common

color_info = 'magenta'
color_info_on = 'on_blue'
color_error = 'red'
color_error_on = color_info_on
color_success = 'green'
color_attribute = ['concealed']


def create_virtual_environment():
    # Install dependencies from requirements.txt
    try:
        system_command("pip3 install virtualenv")
        # system_command("pip3 install -r requirements.txt")
    except Exception as e:
        system_command("pip install virtualenv")
        # system_command("pip install -r requirements.txt")
        pass
    finally:
        pass

    system_command("virtualenv venv")

    # try:
    #     system_command("python3 -m virtualenv env")
    # except Exception as e:
    #     print (e)

    # activate virtual environment
    if common.Common.get_os().startswith(nRoboConfig.Platforms.WINDOWS.value):
        system_command("venv" + os.sep + "Scripts" + os.sep + "activate")  # For Windows
    elif common.Common.get_os().startswith(nRoboConfig.Platforms.DARWIN.value) or \
            common.Common.get_os().startswith(nRoboConfig.Platforms.LINUX_KERNER_BASED):
        system_command("source venv" + os.sep + "bin" + os.sep + "activate")  # For Unix and MacOS

    time.sleep(2)


def install_requirements():
    try:
        # system_command("pip3 install virtualenv")
        system_command("pip3 install numpy")
        system_command("pip3 install -r requirements.txt")
    except Exception as e:
        # system_command("pip install virtualenv")
        system_command("pip install numpy")
        system_command("pip install -r requirements.txt")
        pass
    finally:
        pass


def create_directory(dir_path):
    try:
        os.mkdir(dir_path)
        if os.path.isdir(dir_path):
            print("Directory, " + dir_path + ", created successfully!")
        elif os.path.isfile(dir_path):
            print("File, " + dir_path + ", created successfully!")
    except OSError as osError:
        if os.path.isdir(dir_path):
            print("Directory, " + dir_path + ", already exists!")
        elif os.path.isfile(dir_path):
            print("File, " + dir_path + ", already exists!")
        pass


"""
|- assets
|- config
|- helpers
|- pages
|- security
|- tests
|- test_data
|- test_output
|- tests_advanced_reports
|- tests_api
|- tests_performance
|- tools
"""

dir_structure = [
    "assets",
    "config",
    "helpers",
    "pages",
    "security",
    "tests",
    "test_data",
    "test_output",
    "tests_advanced_reports",
    "tests_api",
    "tests_performance",
    "tools"
]


def create_dir_structure():
    """
    Create directory structure for tests development

    :return:
    """

    for index in range(len(dir_structure)):
        # iterate through dir_structure and create folder structure

        import site
        dir_site_packages = site.getsitepackages()

        if common.Common.get_os().startswith(nRoboConfig.Platforms.WINDOWS.value):
            dir_site_package = dir_site_packages[1]
        elif common.Common.get_os().startswith(nRoboConfig.Platforms.DARWIN.value) or \
                common.Common.get_os().startswith(nRoboConfig.Platforms.LINUX_KERNER_BASED.value):
            dir_site_package = dir_site_packages[0]

        # STEP-2: Copy framework files to respective project directory
        framework_dir = dir_site_package + os.sep + nRoboConfig.Packages.NROBO.value
        sep = os.sep
        source_dir = framework_dir + sep + dir_structure[index]
        target_dir = dir_structure[index]

        # Copy folder tree
        try:
            shutil.copytree(source_dir, target_dir)
        except OSError as oserror:
            print(oserror)
            pass

    # Copy file only
    try:
        shutil.copy(framework_dir + os.sep + nRoboConfig.FrameworkFiles.SPEEDBOAT_PY.value,
                    nRoboConfig.FrameworkFiles.SPEEDBOAT_PY.value)
        shutil.copy(framework_dir + os.sep + nRoboConfig.FrameworkFiles.CONFTEST_PY.value,
                    nRoboConfig.FrameworkFiles.CONFTEST_PY.value)
        shutil.copy(framework_dir + os.sep + nRoboConfig.FrameworkFiles.VERSION_PY.value,
                    nRoboConfig.FrameworkFiles.VERSION_PY.value)
        # shutil.copy(framework_dir + os.sep + "__init__.py", "__init__.py")
        # shutil.copy(framework_dir + os.sep + "__main__.py", "__main__.py")
        # shutil.copy(framework_dir + os.sep + "requirements.py", "requirements.py")
    except OSError as oserror:
        print(oserror)

    # Rename requirements.py to requirements.txt
    try:
        requirements = common.Common.read_file_as_string(
            framework_dir + os.sep + nRoboConfig.FrameworkFiles.REQUIREMENTS_PY.value)
        common.Common.write_text_to_file(nRoboConfig.FrameworkFiles.REQUIREMENTS_TXT.value, requirements)
    except OSError as e:
        print(oserror)


def install_framework():
    # Get site-packages directory

    create_dir_structure()


def validateCommandLineSwitches():
    """
    Description
        Parses the spherobot command line arguments.
        and Returns command line options and arguments.
        If there is any option or argument is missing,
        Program stops and exist.

    Parameters
        None

    Returns
        options : iterable object that holds command line options and arguments
    """

    # Fix imports

    # Get the arguments from the command-line except the filename

    argv = sys.argv[1:]
    # print (argv)
    # exit(4)

    try:
        # Check if user is asking for help
        # print(argv)
        if len(argv) == 1 and argv[0] == nRoboConfig.CommandLineSwitchesShort.HELP.value:
            options, arguments = getopt.getopt(argv, 'h', ["help"])
            print("PRINT HELP!!! Pending...")
            exit(1)
            # return options

        elif len(argv) == 1 and argv[0] == nRoboConfig.CommandLineSwitchesShort.VERSION.value:
            options, arguments = getopt.getopt(argv, 'v', ["version"])
            try:
                import version
            except ModuleNotFoundError as e:
                from nrobo import version
                #print(e)

            print(version.version)

            exit(1)
            # return options

        elif len(argv) == 1 and argv[0] == nRoboConfig.CommandLineSwitchesShort.INSTALL.value:
            options, arguments = getopt.getopt(argv, 'i', ["install"])

            # Perform installation of speedboat framework in current directory
            install_framework()
            create_virtual_environment()
            # install_requirements()
            print("\n\n\n")
            print("Installation is complete. Now, Run your tests:")
            print(
                "\t\t " +
                nRoboConfig.Commands.NROBO.value + nRoboConfig.Constants.SPACE.value +
                nRoboConfig.CommandLineSwitchesShort.APP.value + nRoboConfig.Constants.SPACE.value + "google" + nRoboConfig.Constants.SPACE.value +
                nRoboConfig.CommandLineSwitchesShort.LINK.value + nRoboConfig.Constants.SPACE.value + "http://google.com" + nRoboConfig.Constants.SPACE.value +
                nRoboConfig.CommandLineSwitchesShort.USERNAME.value + nRoboConfig.Constants.SPACE.value + "panchdev" + nRoboConfig.Constants.SPACE.value +
                nRoboConfig.CommandLineSwitchesShort.PASSWORD.value + nRoboConfig.Constants.SPACE.value + "Passw0rd" + nRoboConfig.Constants.SPACE.value +
                nRoboConfig.CommandLineSwitchesShort.PARALLEL_TEST_COUNT.value + nRoboConfig.Constants.SPACE.value + "4" + nRoboConfig.Constants.SPACE.value +
                nRoboConfig.CommandLineSwitchesShort.RERUN.value + nRoboConfig.Constants.SPACE.value + "0" + nRoboConfig.Constants.SPACE.value +
                nRoboConfig.CommandLineSwitchesShort.BROWSER.value + " " + nRoboConfig.Browsers.CHROME.value + nRoboConfig.Constants.SPACE.value +
                nRoboConfig.CommandLineSwitchesShort.REPORT_TYPE.value + nRoboConfig.Constants.SPACE.value + nRoboConfig.TestReportSettings.REPORT_TYPE_ALLURE.value
            )
            exit(1)
            # return options
        else:

            # Check if user has entered all the mandatory command line arguments
            # Define the getopt parameters
            options, arguments = getopt.getopt(argv, 'a:n:k:m:l:u:p:r:b:t:',
                                               ["app_name", "parallel_test_count", "only_test_that_contains",
                                                "having_marker",
                                                "app_url", "username", "password", "rerun_count", "on_browser",
                                                "target_env"]
                                               )

            return options

    except getopt.GetoptError as e:
        print(e)
        sys.exit(2)  # No need to proceed with test if the test launcher arguments are missing


def namastey_world(my_name=None):
    """
    Print the greeting message!

    :param my_name:
    :return:
    """

    greeting = "_/\_ Namastey "
    greeting += "World! " if my_name is None else my_name + "! "
    greeting += 'I am "Birbal".'
    print(greeting)


def prepare_test_launcher(options):
    """
    Description
        This function parses the given command line arguments supplied in the <options> parameter
    and prepares the pytest command to trigger the test execution

    Parameters
        options -> iterable object : Holds Spherobot command line arguments

    Returns
        str obj : String representation of pytest command
        Foe example:
            pytest --reruns 2 --reruns-delay 1  -s -v  -n 1 -k hqp  --url=https://staging.v2.spherewms.com --username=erpanchdev@gmail.com --password=Passw0rd$ tests-backup/v2
    """

    # Add support for re-running a test if it fails,
    # because sometimes a test fails with many other unknown reasons
    # That are not actual test failures
    # test_launcher = "pytest --reruns 2 --only-rerun AssertionError --reruns-delay 1 "
    test_launcher = "pytest "

    # add -s and -v (increase verbosity) switch
    test_launcher += " -s -v "

    # add support for test results in xml format
    test_launcher += " --junitxml=" + nRoboConfig.Paths.TEST_OUTPUT_DIR.value + "/result.xml "

    # application under test
    app_test_dir = nRoboConfig.Paths.TESTS_DIR_WITH_SLASH.value + nRoboConfig.Constants.ASTERISK.value

    # boolean variable to check if -a switch is provided
    is_app_switch_found = False

    # boolean variable to check if -l switch is provided
    is_link_switch_found = False

    # boolean variable to check if -m switch is provided
    marker_switch_found = False

    # boolean variable to check if -u switch is provided
    is_username_switch_found = False

    # boolean variable to check if -p switch is provided
    is_password_switch_found = False

    # boolean variable to check if -r switch is provided
    is_rerun_switch_found = False

    is_report_type_allure_found = False

    # command builder
    command = nRoboConfig.FrameworkFiles.SPEEDBOAT_PY.value + nRoboConfig.Constants.SPACE.value

    # set browser = chrome always by default
    # in future, we will support more browsers,
    # and then, we probably support a new switch -b for the same.
    # but for now, make it always set to chrome

    for opt, arg in options:
        """
        Iterate through command line options and arguments
        """

        command += opt + nRoboConfig.Constants.SPACE.value + arg + nRoboConfig.Constants.SPACE.value

        if opt == nRoboConfig.CommandLineSwitchesShort.HELP.value:
            """if option is -h"""

            print("Team is currently working on showing help document.")
            sys.exit(3)

        elif opt == nRoboConfig.CommandLineSwitchesShort.APP.value:
            """If option is -a"""

            # save that app switch is found
            is_app_switch_found = True

            # get the application under test information from the argument
            app_under_test = arg.upper()

            test_launcher += nRoboConfig.Constants.SPACE.value + nRoboConfig.Constants.HYPEN.value + nRoboConfig.Constants.HYPEN.value \
                             + nRoboConfig.CommandLineSwitchesLong.APP_NAME.value + nRoboConfig.Constants.SPACE.value + arg \
                             + nRoboConfig.Constants.SPACE.value

            # print user message
            print("Application under test is {0}".format(app_under_test))

        elif opt == nRoboConfig.CommandLineSwitchesShort.KEY.value:
            """If option is -k"""

            # add the -k switch to test launcher command
            test_launcher += nRoboConfig.Constants.SPACE.value + opt + nRoboConfig.Constants.SPACE.value + arg + nRoboConfig.Constants.SPACE.value

        elif opt == nRoboConfig.CommandLineSwitchesShort.MARKER.value:
            """If option is -m"""

            # add the -m switch to test launcher command
            test_launcher += nRoboConfig.Constants.SPACE.value + opt + nRoboConfig.Constants.SPACE.value + arg + nRoboConfig.Constants.SPACE.value

            # marker switch found
            marker_switch_found = True

        elif opt == nRoboConfig.CommandLineSwitchesShort.LINK.value:
            """If option is -l"""

            # link switch found
            is_link_switch_found = True

            nRoboConfig.URL = arg + "MYTESTURL"

            # add the --url switch to test launcher command
            test_launcher += nRoboConfig.Constants.SPACE.value + nRoboConfig.Constants.HYPEN.value + \
                             nRoboConfig.Constants.HYPEN.value + nRoboConfig.CommandLineSwitchesLong.APP_LINK.value + \
                             nRoboConfig.Constants.EQUAL.value + arg.lower()

        elif opt == nRoboConfig.CommandLineSwitchesShort.USERNAME.value:
            """If option is -u"""

            # username switch found
            is_username_switch_found = True

            # add the --username switch to test launcher command
            test_launcher += nRoboConfig.Constants.SPACE.value + \
                             nRoboConfig.Constants.HYPEN.value + nRoboConfig.Constants.HYPEN.value + \
                             nRoboConfig.CommandLineSwitchesLong.USERNAME.value + nRoboConfig.Constants.EQUAL.value + arg

        elif opt == nRoboConfig.CommandLineSwitchesShort.PASSWORD.value:
            """If option is -p"""

            # password switch found
            is_password_switch_found = True

            # add the --password switch to test launcher command
            test_launcher += nRoboConfig.Constants.SPACE.value + nRoboConfig.Constants.HYPEN.value + nRoboConfig.Constants.HYPEN.value + \
                             nRoboConfig.CommandLineSwitchesLong.PASSWORD.value + nRoboConfig.Constants.EQUAL.value + arg

        elif opt == nRoboConfig.CommandLineSwitchesShort.BROWSER.value:
            """If option is -b"""

            # password switch found
            # is_password_switch_found = True

            # add the --password switch to test launcher command
            test_launcher += nRoboConfig.Constants.SPACE.value + nRoboConfig.Constants.HYPEN.value + nRoboConfig.Constants.HYPEN.value + \
                             nRoboConfig.CommandLineSwitchesLong.BROWSER.value + nRoboConfig.Constants.EQUAL.value + arg

        elif opt == nRoboConfig.CommandLineSwitchesShort.RERUN.value:

            # rerun switch found
            is_rerun_switch_found = True

            # get random sleep time
            random_sleep_time = random.randint(4, 10)

            # add --rerun switch
            test_launcher += nRoboConfig.Constants.SPACE.value + nRoboConfig.Constants.HYPEN.value + nRoboConfig.Constants.HYPEN.value + \
                             nRoboConfig.CommandLineSwitchesLong.RERUN.value + nRoboConfig.Constants.SPACE.value + str(
                arg) + nRoboConfig.Constants.SPACE.value + \
                             nRoboConfig.Constants.HYPEN.value + nRoboConfig.Constants.HYPEN.value + \
                             nRoboConfig.CommandLineSwitchesLong.RERUN_DELAY.value + nRoboConfig.Constants.SPACE.value + str(
                random_sleep_time) + \
                             nRoboConfig.Constants.SPACE.value

        elif opt == nRoboConfig.CommandLineSwitchesShort.PARALLEL_TEST_COUNT.value:

            if int(arg) > 1:
                nRoboConfig.PARALLEL_RUN = True

            test_launcher += nRoboConfig.Constants.SPACE.value + opt + nRoboConfig.Constants.SPACE.value + arg

        elif opt == nRoboConfig.CommandLineSwitchesShort.REPORT_TYPE.value:

            if arg.lower() == nRoboConfig.TestReportSettings.REPORT_TYPE_ALLURE.value.lower():
                is_report_type_allure_found = True


        else:
            """else """

            # add the opt switch and arg to test launcher command
            test_launcher += nRoboConfig.Constants.SPACE.value + opt + nRoboConfig.Constants.SPACE.value + arg

    # inform user and exit if app switch is not provided
    if not is_app_switch_found:
        """if app switch is not found"""
        print("Mandatory switch {0} missing!!!".format(nRoboConfig.CommandLineSwitchesShort.APP.value))
        # exit the spherobot program
        sys.exit(1)
    elif not is_link_switch_found:
        """if link switch is not found"""
        print("Mandatory switch {0} missing!!!".format(nRoboConfig.CommandLineSwitchesShort.LINK.value))
        # exit the spherobot program
        sys.exit(1)
    elif not is_username_switch_found:
        """if username switch is not found"""
        print("Mandatory switch {0} missing!!!".format(nRoboConfig.CommandLineSwitchesShort.USERNAME.value))
        # exit the spherobot program
        sys.exit(1)
    elif not is_password_switch_found:
        """if password switch is not found"""
        print("Mandatory switch {0} missing!!!".format(nRoboConfig.CommandLineSwitchesShort.PASSWORD.value))
        # exit the spherobot program
        sys.exit(1)
    elif not is_rerun_switch_found:
        """if rerun switch is not found"""

        # get random sleep time
        random_sleep_time = random.randint(4, 10)

        # Add support for re-running a test if it fails,
        # because sometimes a test fails with many other unknown reasons
        # That are not actual test failures
        # Thus, add --rerun switch
        test_launcher += nRoboConfig.Constants.SPACE.value + nRoboConfig.Constants.HYPEN.value + nRoboConfig.Constants.HYPEN.value + \
                         nRoboConfig.CommandLineSwitchesLong.RERUN.value + nRoboConfig.Constants.SPACE.value + "1" + \
                         nRoboConfig.Constants.SPACE.value + nRoboConfig.Constants.HYPEN.value + nRoboConfig.Constants.HYPEN.value + \
                         nRoboConfig.CommandLineSwitchesLong.RERUN_DELAY.value + nRoboConfig.Constants.SPACE.value + str(
            random_sleep_time) + \
                         nRoboConfig.Constants.SPACE.value

    # add the correct test directory to test launcher command
    test_launcher += nRoboConfig.Constants.SPACE.value + app_test_dir

    if not is_link_switch_found:
        """if Link switch is not provided"""

        print("Mandatory switch {0} missing!!!".format(nRoboConfig.CommandLineSwitchesShort.LINK.value))
        sys.exit(1)

    if not marker_switch_found:
        """if marker switch is not found"""

        pass

    # inform user of received of command line arguments
    print("Received the following command line request: {0}".format(command))

    # pause execution for 2 seconds
    time.sleep(nRoboConfig.Waits.SLEEP_TIME.value)

    if is_report_type_allure_found:
        # inject and activate allure reports listner
        test_launcher += nRoboConfig.Constants.SPACE.value + \
                         nRoboConfig.Constants.HYPEN.value + nRoboConfig.Constants.HYPEN.value + \
                         nRoboConfig.CommandLineSwitchesLong.ALLURE_DIR.value + nRoboConfig.Constants.EQUAL.value + \
                         nRoboConfig.Paths.TEST_ALLURE_REPORTS_DIR.value
        # \
        #                 + nRoboConfig.Constants.SPACE + "--allure-severities normal,critical"

        # Integreate allure behave listener
        # test_launcher += nRoboConfig.Constants.SPACE + "--alluredir=" + paths.TEST_ALLURE_REPORTS_DIR

    # return actual pytest test-launcher command to the caller
    return test_launcher  # + " -vv --order-scope=module"


def clean_test_output_directory():
    """
    Description
        This function cleans the test_output directory before running a new test execution

    Parameters
        None

    Returns
        None
    """

    # inform user of cleaning the test output directory
    print("Clean test output directory...")

    # pause for 2 seconds
    time.sleep(nRoboConfig.Waits.SLEEP_TIME.value)

    try:
        if common.Common.get_os() == nRoboConfig.Platforms.DARWIN.value \
                or nRoboConfig.Platforms.LINUX_KERNER_BASED.value in common.Common.get_os():
            """if operating is ios or linux based os"""

            # Hey!!! I found that we are on OS using linux kernel. I hope, you are not a hacker. :)

            # Clear test_output directory
            os.system("rm -fv {0}/*.html".format(nRoboConfig.Paths.TEST_OUTPUT_DIR.value))
            os.system("rm -fv {0}/*.xml".format(nRoboConfig.Paths.TEST_OUTPUT_DIR.value))
            os.system(
                "rm -fv {0}/*.yaml".format(nRoboConfig.Paths.TEST_OUTPUT_DIR.value))

            # Clear test_output screenshots directory
            os.system(
                "rm -fv {0}/*.png".format(nRoboConfig.Paths.TEST_OUTPUT_SCREENSHOT_DIR.value))

            # Clean tests_advanced_report directory
            os.system("rm -fv {0}/*.json".format(nRoboConfig.Paths.TEST_ALLURE_REPORTS_DIR.value))
            os.system("rm -fv {0}/*.txt".format(nRoboConfig.Paths.TEST_ALLURE_REPORTS_DIR.value))
        else:
            """else os is windows"""

            # Hey!!! I found that we are using windows machine...
            os.system("del /q /S {0}\\*.html".format(nRoboConfig.Paths.TEST_OUTPUT_DIR.value))
            os.system("del /q /S {0}\\*.yaml".format(nRoboConfig.Paths.TEST_OUTPUT_DIR.value))
            os.system("del /q /S {0}\\*.xml".format(nRoboConfig.Paths.TEST_OUTPUT_DIR.value))
            os.system("del /q /S {0}\\*.png".format(nRoboConfig.Paths.TEST_OUTPUT_SCREENSHOT_DIR.value))

            # Clean tests_advanced_report directory
            os.system("del /q /S {0}\\*.json".format(nRoboConfig.Paths.TEST_ALLURE_REPORTS_DIR.value))
            os.system("del /q /S {0}\\*.txt".format(nRoboConfig.Paths.TEST_ALLURE_REPORTS_DIR.value))
    except Exception as e:
        print(e)

    print("test_output directory cleaned...")
    time.sleep(nRoboConfig.Waits.SLEEP_TIME.value)


def system_command(command):
    """
    Description
        This function executes the given <command>

    Parameters
        command -> str obj : command to execute

    Returns
        status_code - integer status code. 0 means success and any other mean failure.
    """

    try:
        # Execute the given <command>
        status_code = os.system(command)
    except Exception as e:
        print(e)

    # return with status_code.
    return status_code


def generate_cool_test_report():
    system_command("allure generate " + nRoboConfig.Paths.TEST_ALLURE_REPORTS_DIR.value + " --clean")


def get_value_of_cli_switch(cli_switches, switch):
    for opt, arg in cli_switches:

        if opt == switch:
            return arg

    return ""


def update_allure_report_title(cli_switches):
    allure_summary_widget_path = 'allure-report/widgets/summary.json'
    data = common.Common.read_json(allure_summary_widget_path)
    data['reportName'] = get_value_of_cli_switch(cli_switches,
                                                 nRoboConfig.CommandLineSwitchesShort.APP.value).title() + " automated test report".title()
    common.Common.write_json(allure_summary_widget_path, data)


def update_allure_report_logo():
    FILE_COMPANY_LOGO = "company-logo.png"

    DIR_SOURCE = nRoboConfig.FrameworkDirectories.ASSETS.value
    shutil.copy2(os.path.join(DIR_SOURCE, FILE_COMPANY_LOGO), nRoboConfig.Paths.TEST_ALLURE_GENERATE_DIR.value)

    STYLE_CSS_FILE_PATH = os.path.join(nRoboConfig.Paths.TEST_ALLURE_GENERATE_DIR.value, "styles.css")
    STYLE_CSS_CONTENT_AS_STRING = common.Common.read_file_as_string(STYLE_CSS_FILE_PATH)
    MODIFIED_STYLE_CSS_CONTENT_AS_STRING = re.sub("side-nav__brand{background:url\([a-z:\/+;\d,A-Z]+\)",
                                                  "side-nav__brand{background:url(" + FILE_COMPANY_LOGO + ")",
                                                  STYLE_CSS_CONTENT_AS_STRING)
    common.Common.write_text_to_file(STYLE_CSS_FILE_PATH, MODIFIED_STYLE_CSS_CONTENT_AS_STRING)


def update_allure_report_company_name():
    ALLURE_APP_JS_FILE_NAME = "app.js"
    ALLURE_APP_JS_FILE_PATH = os.path.join(nRoboConfig.Paths.TEST_ALLURE_GENERATE_DIR.value, ALLURE_APP_JS_FILE_NAME)

    app_name = get_value_of_cli_switch(validateCommandLineSwitches(),
                                       nRoboConfig.CommandLineSwitchesShort.APP.value).title()
    ALLURE_APP_JS_CONTENT_AS_STRING = common.Common.read_file_as_string(ALLURE_APP_JS_FILE_PATH)
    MODIFIED_STYLE_CSS_CONTENT_AS_STRING = re.sub(">Allure<",
                                                  ">" + app_name + "<",
                                                  ALLURE_APP_JS_CONTENT_AS_STRING)
    common.Common.write_text_to_file(ALLURE_APP_JS_FILE_PATH, MODIFIED_STYLE_CSS_CONTENT_AS_STRING)


def run_allure_report(cli_switches):
    # Generate cool test report
    generate_cool_test_report()

    # Update allure report time
    update_allure_report_title(cli_switches)

    # update allure logo
    update_allure_report_logo()

    # Update allure report company name
    update_allure_report_company_name()

    # Open report
    system_command("allure open allure-report")
    # system_command("allure serve " + paths.TEST_ALLURE_REPORTS_DIR)


if __name__ == '__main__':
    """
    Entry point of the framework.
    """
    namastey_world()  # :)

    # print(sys.argv)

    create_virtual_environment()

    # Install Pre-requisites
    install_requirements()

    print("\n\n\n")

    import security
    from config import nRoboConfig
    from helpers import common
    from security.security_checks import SecurityChecks

    # Validate Command Line Switches if they are correct.
    cli_switches = validateCommandLineSwitches()

    # Prepare test luncher
    test_launch_command = prepare_test_launcher(cli_switches)
    print("Launch Command: {0}".format(test_launch_command))

    # Clean test_output directory for fresh test results
    clean_test_output_directory()

    # do some pre launch security-backup checks
    print("Perform security-backup checks...")

    # delete package and reimport to handle circular import error
    del security  # delete package

    # reimport again
    from security.security_checks import SecurityChecks

    # perform url security-backup check
    security_checks = SecurityChecks()
    # security_checks.perform_url_security_check()

    # Parse CLI commands
    # installer.parse_cli()

    # system_command("behave -f allure_behave.formatter:AllureFormatter -o %" + paths.TEST_ALLURE_REPORTS_DIR + "% ./features")
    # Launch tests-backup
    time.sleep(nRoboConfig.Waits.SLEEP_TIME.value)

    system_command(test_launch_command)

    if get_value_of_cli_switch(cli_switches,
                               nRoboConfig.CommandLineSwitchesShort.REPORT_TYPE.value).lower() == nRoboConfig.TestReportSettings.REPORT_TYPE_ALLURE.value.lower():
        # run and host allure report on local server
        run_allure_report(cli_switches)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
