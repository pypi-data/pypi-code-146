#######################################
# Global Constants
#######################################
PARALLEL_RUN = False
URL = ""
APP = "app"
APP_NAME = "app"
APP_LINK = "app_link"
BROWSER = "browser"
OMS_LINK = "oms_link"
TEST_USER_NAME = "test_user_name"
NAME = "name"
USERNAME = "username"
PASSWORD = "password"
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


#########################################
# Browsers
#########################################
BROWSER_HEADLESS_CHROME = "headless_chrome"
BROWSER_CHROME = "chrome"
BROWSER_EDGE = "edge"
BROWSER_FIREFOX = "firefox"
BROWSER_SAFARI = "safari"
BROWSER_IE = "ie"
BROSER_OPERA = "opera"

##########################################
# Global Locators
##########################################
# tuple representing element that represents, an action is complete
action_complete_indicator_element=(None, None)
# tuple representing element that represents that page loading is complete
page_loading_complete_indicator_element=(None, None)
# element representing that loading is in progress
loader = (None, None)

#########################################
# Operating System
#########################################
OS_DARWIN = "darwin"
OS_LINUX_KERNER_BASED = "linux"
OS_WINDOWS = "windows"

########################################
# DRIVER_NAMES
########################################
DRIVER_NAME_CHROME = "chromedriver"

########################################
# EXTENSIONS
########################################
EXTENTION_WINDOWS = ".exe"
EXTENTION_HTML = ".html"

########################################
# Wait Times - Sleep Times
########################################
SLEEP_TIME = 1
STATIC_WAIT = 0.05
TIMEOUT=30

# Min and Max limits to randomize time between two parallel running tests-backup
TIME_MIN_LIMIT_TO_MAKE_TEST_ASYNCHRONOUS=2
TIME_MAX_LIMIT_TO_MAKE_TEST_ASYNCHRONOUS=5


#########################################
# TEST Markers
#########################################
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
CLI_SWITCH_HELP = '-h'
CLI_SWITCH_APP = '-a'
CLI_SWITCH_KEY = '-k'
CLI_SWITCH_MARKER = '-m'
CLI_SWITCH_LINK = '-l'
CLI_SWITCH_USERNAME = '-u'
CLI_SWITCH_PASSWORD = '-p'
CLI_SWITCH_RERUN = '-r'
CLI_SWITCH_BROWSER = '-b'
CLI_SWITCH_REPORT_TYPE = '-t'
CLI_SWITCH_INSTALL = '-i'

# TEST REPORT
TEST_APPLICATION_NAME = "APPLICATION_NAME"
TEST_HTML_REPORT_FILE_NAME_PREFIX = "speedboat-automated-test-report"
TEST_USER_NAME = None
TEST_APPLICATION_LOGO_URL = 'https://www.namasteydigitalindia.com/connect/wp-content/uploads/2022/02/cropped-ndi-logo-1-1.png'
TEST_REPORT_TYPE_ALLURE = "allure"
TEST_REPORT_TYPE_PYTEST = "pytest"

# DATE & TIME FORMATS
DATETIME_FORMAT_DD_MM_YY_HH_MM_SS = "%d-%m-%Y %H-%M-%S"