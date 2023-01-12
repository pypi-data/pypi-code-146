from enum import Enum

URL = ""
PARALLEL_RUN = False


#########################################
# Browsers
#########################################
class Browsers(Enum):
    HEADLESS_CHROME = "headless_chrome"
    CHROME = "chrome"
    EDGE = "edge"
    FIREFOX = "firefox"
    SAFARI = "safari"
    IE = "ie"
    OPERA = "opera"


#########################################
# Operating System
#########################################
class Platforms(Enum):
    DARWIN = "darwin"
    LINUX_KERNER_BASED = "linux"
    WINDOWS = "win"


########################################
# DRIVER_NAMES
########################################
class DriverNames(Enum):
    DRIVER_NAME_CHROME = "chromedriver"


########################################
# EXTENSIONS
########################################
class Extensions(Enum):
    WINDOWS = ".exe"
    HTML = ".html"


########################################
# Wait Times - Sleep Times
########################################
class Waits(Enum):
    SLEEP_TIME = 1
    STATIC_WAIT = 0.05
    TIMEOUT = 30


# Min and Max limits to randomize time between two parallel running tests-backup
class TimeLimits(Enum):
    TIME_MIN_LIMIT_TO_MAKE_TEST_ASYNCHRONOUS = 2
    TIME_MAX_LIMIT_TO_MAKE_TEST_ASYNCHRONOUS = 5


#########################################
# TEST Markers
#########################################
class Markers(Enum):
    MARKERS_NO = "no_marker_switch"
    MARKERS_NOGUI = "nogui"
    MARKERS_SPEEDBOAT = [
        "sanity: group of sanity tests",
        "regression: group of regression tests",
        "ui: group of ui tests",
        "api: group of api tests",
        "nogui: group of NOGUI tests"
    ]


# command line switches
class CommandLineSwitchesShort(Enum):
    HELP = '-h'
    VERSION = '-v'
    APP = '-a'
    KEY = '-k'
    MARKER = '-m'
    LINK = '-l'
    USERNAME = '-u'
    PASSWORD = '-p'
    RERUN = '-r'
    BROWSER = '-b'
    REPORT_TYPE = '-t'
    INSTALL = '-i'
    PARALLEL_TEST_COUNT = '-n'


class CommandLineSwitchesLong(Enum):

    APP = "app"
    APP_NAME = "app"
    APP_LINK = "app_link"
    BROWSER = "browser"
    OMS_LINK = "oms_link"
    TEST_USER_NAME = "test_user_name"
    NAME = "name"
    USERNAME = "username"
    PASSWORD = "password"
    RERUN = "reruns"
    RERUN_DELAY = "reruns-delay"
    ALLURE_DIR = "alluredir"
    URL = "url"


# TEST REPORT
class TestReportSettings(Enum):
    APPLICATION_NAME = "APPLICATION_NAME"
    HTML_REPORT_FILE_NAME_PREFIX = "speedboat-automated-test-report"
    USER_NAME = None
    APPLICATION_LOGO_URL = 'https://www.namasteydigitalindia.com/connect/wp-content/uploads/2022/02/cropped-ndi-logo' \
                           '-1-1.png '
    REPORT_TYPE_ALLURE = "allure"
    REPORT_TYPE_PYTEST = "pytest"
    REPORT_HTML_FILE_NAME = "report_html_file_name.html"
    REPORT_SCREENSHOT_DIRECTORY = "report_screenshot_directory"
    REPORT_SCREENSHOT_DIRECTORY_WITH_SLASH = "report_screenshot_directory_with_slash"
    REPORT_SCREENSHOT_RELATIVE_DIRECTORY = "report_screenshot_relative_directory"
    REPORT_TEST_OUTPUT_DIRECTORY_PATH_WITH_SLASH = "report_test_output_directory_path_with_slash"
    REPORT_BROWSER = "report_browser_name"
    REPORT_MARKER = "report_marker"
    REPORT_PASSED = "report_passed"
    REPORT_SKIPPED = "report_skipped"
    REPORT_FAILED = "report_failed"
    REPORT_ERRORS = "report_errors"
    REPORT_EXPECTED_FAILURES = "report_expected_failures"
    REPORT_UNEXPECTED_PASSES = "report_unexpected_passes"
    REPORT_RERUN = "report_rerun"
    INTERNET_SPEED = "internet_speed"


# DATE & TIME FORMATS
class DateTimeFormats(Enum):
    DD_MM_YY_HH_MM_SS = "%d-%m-%Y %H-%M-%S"


# Paths
class Paths(Enum):
    # import constants as CONSTANTS
    # a string literal representing an forward slash
    FORWARD_SLASH = "/"
    DOT = "."

    DRIVERS_DIR = "drivers"
    DRIVERS_DIR_WITH_SLASH = DRIVERS_DIR + FORWARD_SLASH

    TESTS_DIR = "tests"
    TESTS_DIR_WITH_SLASH = TESTS_DIR + FORWARD_SLASH

    TEST_DATA_DIR = "test_data"
    TEST_DATA_DIR_WITH_SLASH = TEST_DATA_DIR + FORWARD_SLASH

    # test_output directory path
    TEST_OUTPUT_DIR = "test_output"
    TEST_OUTPUT_DIR_WITH_SLASH = TEST_OUTPUT_DIR + FORWARD_SLASH

    # screenshots directory path
    TEST_SCREENSHOT_DIR = "screenshots"
    TEST_OUTPUT_SCREENSHOT_DIR = TEST_OUTPUT_DIR_WITH_SLASH + TEST_SCREENSHOT_DIR
    TEST_OUTPUT_SCREENSHOT_DIR_WITH_SLASH = TEST_OUTPUT_DIR_WITH_SLASH + TEST_SCREENSHOT_DIR + FORWARD_SLASH
    TEST_OUTPUT_SCREENSHOT_RELATIVE_DIR = TEST_SCREENSHOT_DIR

    # tests_api-backup directory path
    TEST_API_DIRECTORY = "tests_api"
    TEST_API_DIRECTORY_WITH_SLASH = TEST_API_DIRECTORY + FORWARD_SLASH

    # tests_performance_backup directory path
    TEST_PERFORMANCE_DIRECTORY = "tests_performance"
    TEST_PERFORMANCE_DIRECTORY_WITH_SLASH = TEST_PERFORMANCE_DIRECTORY + FORWARD_SLASH

    # Allure-Reports
    TEST_ALLURE_GENERATE_DIR = "allure-report"
    TEST_ALLURE_REPORTS_DIR = "tests_advanced_reports"


# Selenium Grid Types
class GridTypes(Enum):
    STANDALONE = "standalone"
    HUB = "hub"
    NODE = "node"


# Global Locators
class GlobalLocators(Enum):
    # tuple representing element that represents, an action is complete
    action_complete_indicator_element = (None, None)

    # tuple representing element that represents that page loading is complete
    page_loading_complete_indicator_element = (None, None)

    # element representing that loading is in progress
    loader = (None, None)


class Constants(Enum):
    """
    Name
        constants.py
    Description
        This modules holds common constants say, an empty string literal, a space, an underscore character etc.
    """

    # a string literal representing an empty string
    EMPTY = ""

    # Equal
    EQUAL = "="

    # a string literal representing an blank string
    BLANK = EMPTY

    # a string literal representing an space
    SPACE = " "

    # a string literal representing a star
    STAR = "*"
    ASTERISK = "*"

    # a string literal representing an underscore
    UNDERSCORE = "_"

    # a string literal representing an forward slash
    FORWARD_SLASH = "/"

    # a string literal representing a minus sign
    MINUS = "-"

    # a string literal representing a hyphen character
    HYPEN = MINUS

    # a string literal representing https protocol string
    HTTPS = "https://"

    # a string literal representing http protocol string
    HTTP = "http://"

    # a string literal representing a dot character
    DOT = "."

    # a string literal representing a colon character
    COLON = ":"

    # a string literal representing a "At" character
    AT_ADDRESS = "@"

    # a string literal representing a question mark character
    QUESTION = "?"

    HOURS_IN_A_DAY = 24


class WebDriverStatuses(Enum):
    CURRENT_DRIVER = "current driver"


class Packages(Enum):
    NROBO = "nrobo"


class Commands(Enum):
    NROBO = "nrobo"


class FrameworkFiles(Enum):
    SPEEDBOAT_PY = "speedboat.py"
    CONFTEST_PY = "conftest.py"
    REQUIREMENTS_PY = "requirements.py"
    REQUIREMENTS_TXT = "requirements.txt"
    VERSION_PY = "version.py"


class FrameworkDirectories(Enum):
    ASSETS = "assets"

