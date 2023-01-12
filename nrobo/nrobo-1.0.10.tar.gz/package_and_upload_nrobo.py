import getopt
import re
import sys
from enum import Enum

# Framework specific packages
from nrobo import speedboat
from nrobo.helpers.common import Common
from nrobo.config import nRoboConfig


class PyPiEnvironments(Enum):
    TEST = "test"
    PROD = "prod"


class VersionFileNames(Enum):
    TEST = "version_test.yaml"
    PROD = "version_prod.yaml"


def update_version_information(file_content, pattern, replacement):
    # print(file_content)

    file_content = re.sub(pattern, replacement, file_content, count=1)

    # print(file_content)

    return file_content


def change_version_before_packaging(pypi_environment):
    # Grab version number
    if pypi_environment == PyPiEnvironments.TEST.value:
        VERSION = Common.read_yaml(VersionFileNames.TEST.value)['version']
    elif pypi_environment == PyPiEnvironments.PROD.value:
        VERSION = Common.read_yaml(VersionFileNames.PROD.value)['version']

    ###############################
    # UPDATE VERSION IN README FILE
    ###############################

    # README file path
    FILE_NAME = "README.rst"

    # Read file content as string
    file_content = str(Common.read_file_as_string(FILE_NAME))

    # README pattern for finding version setting
    if pypi_environment == PyPiEnvironments.TEST.value:

        PATTERN_PREFIX = "- pip3 install (-i https://test.pypi.org/simple/)"
        # PATTERN_REGULAR_EXPRESSION = PATTERN_PREFIX + "([\d.]+)"
        PATTERN_REGULAR_EXPRESSION = PATTERN_PREFIX

        # Replacement text
        REPLACEMENT_TEXT = "- pip3 install -i https://test.pypi.org/simple/"

        # Update version number in README file
        file_content = update_version_information(file_content, PATTERN_REGULAR_EXPRESSION, REPLACEMENT_TEXT)

        PATTERN_PREFIX = "- pip3 install " + nRoboConfig.Commands.NROBO.value + "=="
        PATTERN_REGULAR_EXPRESSION = PATTERN_PREFIX + "([\d.]+)"

        # Replacement text
        REPLACEMENT_TEXT = "- pip3 install -i https://test.pypi.org/simple/ " + \
                           nRoboConfig.Commands.NROBO.value + nRoboConfig.Constants.EQUAL.value + nRoboConfig.Constants.EQUAL.value + VERSION

        # Update version number in README file
        file_content = update_version_information(file_content, PATTERN_REGULAR_EXPRESSION, REPLACEMENT_TEXT)

        PATTERN_PREFIX = "- pip3 install -i https://test.pypi.org/simple/ " + \
                         nRoboConfig.Commands.NROBO.value + nRoboConfig.Constants.EQUAL.value + nRoboConfig.Constants.EQUAL.value
        PATTERN_REGULAR_EXPRESSION = PATTERN_PREFIX + "([\d.]+)"

        # Replacement text
        REPLACEMENT_TEXT = "- pip3 install -i https://test.pypi.org/simple/ " + \
                           nRoboConfig.Commands.NROBO.value + nRoboConfig.Constants.EQUAL.value + nRoboConfig.Constants.EQUAL.value + VERSION

        # Update version number in README file
        file_content = update_version_information(file_content, PATTERN_REGULAR_EXPRESSION, REPLACEMENT_TEXT)

        # Write file_content
        Common.write_text_to_file(FILE_NAME, file_content)

    elif pypi_environment == PyPiEnvironments.PROD.value:

        PATTERN_PREFIX = "- pip3 install (-i https://test.pypi.org/simple/)"
        PATTERN_REGULAR_EXPRESSION = PATTERN_PREFIX

        # Replacement text
        REPLACEMENT_TEXT = "- pip3 install"

        # Update version number in README file
        file_content = update_version_information(file_content, PATTERN_REGULAR_EXPRESSION, REPLACEMENT_TEXT)

        PATTERN_PREFIX = "- pip3 install " + \
                         nRoboConfig.Commands.NROBO.value + nRoboConfig.Constants.EQUAL.value + nRoboConfig.Constants.EQUAL.value
        PATTERN_REGULAR_EXPRESSION = PATTERN_PREFIX + "([\d.]+)"

        # Replacement text
        REPLACEMENT_TEXT = "- pip3 install " + \
                           nRoboConfig.Commands.NROBO.value + nRoboConfig.Constants.EQUAL.value + nRoboConfig.Constants.EQUAL.value + VERSION

        # Update version number in README file
        file_content = update_version_information(file_content, PATTERN_REGULAR_EXPRESSION, REPLACEMENT_TEXT)

        PATTERN_PREFIX = "- pip3 install -i https://test.pypi.org/simple/ " + \
                         nRoboConfig.Commands.NROBO.value + nRoboConfig.Constants.EQUAL.value + nRoboConfig.Constants.EQUAL.value
        PATTERN_REGULAR_EXPRESSION = PATTERN_PREFIX + "([\d.]+)"

        # Replacement text
        REPLACEMENT_TEXT = "- pip3 install " + nRoboConfig.Commands.NROBO.value + nRoboConfig.Constants.EQUAL.value + nRoboConfig.Constants.EQUAL.value + VERSION

        # Update version number in README file
        file_content = update_version_information(file_content, PATTERN_REGULAR_EXPRESSION, REPLACEMENT_TEXT)

        # Write file_content
        Common.write_text_to_file(FILE_NAME, file_content)

    #####################################
    # UPDATE VERSION IN SPEEDBOAD.py FILE
    #####################################

    # README file path
    FILE_NAME = "nrobo/version.py"

    # Read file content as string
    file_content = str(Common.read_file_as_string(FILE_NAME))

    # README pattern for finding version setting
    PATTERN_PREFIX = "version = "
    PATTERN_REGULAR_EXPRESSION = "([\d.\"]+)"

    # Replacement text
    REPLACEMENT_TEXT = "\"" + VERSION + "\""

    # Update version number in README file
    file_content = update_version_information(file_content, PATTERN_REGULAR_EXPRESSION, REPLACEMENT_TEXT)

    # Write file_content
    Common.write_text_to_file(FILE_NAME, file_content)

    ########################################
    # UPDATE VERSION IN pyproject.toml FILE
    ########################################

    # README file path
    FILE_NAME = "pyproject.toml"

    # Read file content as string
    file_content = str(Common.read_file_as_string(FILE_NAME))

    # README pattern for finding version setting
    PATTERN_PREFIX = "version = "
    PATTERN_REGULAR_EXPRESSION = PATTERN_PREFIX + "([\d.\"]+)"

    # Replacement text
    REPLACEMENT_TEXT = PATTERN_PREFIX + "\"" + VERSION + "\""

    # Update version number in README file
    file_content = update_version_information(file_content, PATTERN_REGULAR_EXPRESSION, REPLACEMENT_TEXT)

    # Write file_content
    Common.write_text_to_file(FILE_NAME, file_content)


def package_and_upload_nRoBo_to_target_environment(target_environment=PyPiEnvironments.TEST):
    change_version_before_packaging(target_environment)

    # Delete existing build(s)
    speedboat.system_command("rm -rf dist")

    # Prepare build
    speedboat.system_command("python3 -m build")

    # Check build
    speedboat.system_command("twine check  dist/*")

    if target_environment == PyPiEnvironments.TEST.value:
        speedboat.system_command("python3 -m twine upload --repository testpypi dist/* --verbose")
    elif target_environment == PyPiEnvironments.PROD.value:
        speedboat.system_command("python3 -m twine upload --repository pypi dist/* --verbose")


if __name__ == '__main__':

    # Check command line switch -t / Target Environment
    argv = sys.argv[1:]
    # print(argv)

    try:
        # Check if user is asking for help
        # print(argv)
        target = "-t"
        ERROR_MISSING_MANDATORY_SWITCH_TARGET = "Target is mandatory. Please provide target with -t switch. Possible " \
                                                "values are 'test' | 'prod' "
        INCORRECT_TARGET_SWITCH = "-t switch can only have one of two values, 'test' or 'prod'. Rerun command with " \
                                  "correct value. "
        if (len(argv) == 1 or len(argv) == 2) \
                and argv[0] == target:
            options, arguments = getopt.getopt(argv, 't', ["target"])
            if arguments[0].lower() == "":
                raise Exception(ERROR_MISSING_MANDATORY_SWITCH_TARGET)
            elif arguments[0].lower() == PyPiEnvironments.TEST.value:
                package_and_upload_nRoBo_to_target_environment(PyPiEnvironments.TEST.value)

            elif arguments[0].lower() == PyPiEnvironments.PROD.value:
                package_and_upload_nRoBo_to_target_environment(PyPiEnvironments.PROD.value)

            else:
                raise Exception(INCORRECT_TARGET_SWITCH)

            exit(1)

        else:
            raise Exception(ERROR_MISSING_MANDATORY_SWITCH_TARGET)

    except getopt.GetoptError as e:
        print(e)
        sys.exit(1)  # No need to proceed with test if the test launcher arguments are missing
    except IndexError as ie:
        print("Command line switch value is missing! Please rerun the command with value.")
