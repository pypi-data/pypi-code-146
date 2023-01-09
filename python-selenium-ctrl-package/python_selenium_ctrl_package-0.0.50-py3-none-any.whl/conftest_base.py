import traceback

import pandas as pd
import pytest
from .drivers.browsers import browser_os_name_conf
from .conf.rwd.Website import base_url_conf
from .utils import html_report_conf
from .pages.zero_page import Zero_Page
from .pages.mobile_zero_page import Mobile_Zero_Page
from datetime import datetime
import os, pytest, sys, time
from .conf import product_list


@pytest.fixture
def test_obj(base_url, browser, browser_version, os_version, os_name, remote_flag, testrail_flag, tesults_flag,
             test_run_id, remote_project_name, remote_build_name, testname, reportportal_service, interactivemode_flag,
             test_env, screenshot_option, xlsx_config, product):
    "Return an instance of Base Page that knows about the third party integrations"
    try:

        # if interactivemode_flag.lower() == "y":
        #     default_flag = interactive_mode.set_default_flag_gui(browser, browser_version, os_version, os_name,
        #                                                          remote_flag, testrail_flag, tesults_flag)
        #     if default_flag == False:
        #         browser, browser_version, remote_flag, os_name, os_version, testrail_flag, tesults_flag = interactive_mode.ask_questions_gui(
        #             browser, browser_version, os_version, os_name, remote_flag, testrail_flag, tesults_flag)
        test_obj = Zero_Page(base_url="http://", product=product_list.QCare)
        test_obj.test_env = test_env
        test_obj.screenshot = screenshot_option
        test_obj.set_calling_module(testname)
        test_obj.product = product
        test_obj.browser = browser
        test_obj.xlsx_config = xlsx_config
        # Setup and register a driver
        test_obj.register_driver(remote_flag, os_name, os_version, browser, browser_version, remote_project_name,
                                 remote_build_name)

        # Setup TestRail reporting
        # if testrail_flag.lower() == 'y':
        #     if test_run_id is None:
        #         test_obj.write(
        #             '\033[91m' + "\n\nTestRail Integration Exception: It looks like you are trying to use TestRail Integration without providing test run id. \nPlease provide a valid test run id along with test run command using -R flag and try again. for eg: pytest -X Y -R 100\n" + '\033[0m')
        #         testrail_flag = 'N'
        #     if test_run_id is not None:
        #         test_obj.register_testrail()
        #         test_obj.set_test_run_id(test_run_id)

        if tesults_flag.lower() == 'y':
            test_obj.register_tesults()

        if reportportal_service:
            test_obj.set_rp_logger(reportportal_service)
        test_obj.start_time = int(time.time())

        yield test_obj
        # Teardown
        test_obj.log_obj.remove_logger()  # Remove original log handlers
        test_obj.wait(3)
        test_obj.teardown()

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))
        traceback.print_exc()


@pytest.fixture
def test_mobile_obj(mobile_os_name, mobile_os_version, device_name, app_package, app_activity, remote_flag, device_flag,
                    testrail_flag, tesults_flag, test_run_id, app_name, app_path, appium_version, test_env,
                    interactivemode_flag, product, screenshot_option, no_reset_flag):
    """Return an instance of Base Page that knows about the third party integrations
    Need to install appium with npm first: npm install -g appium"""
    try:

        # if interactivemode_flag.lower() == "y":
        #     mobile_os_name, mobile_os_version, device_name, app_package, app_activity, remote_flag, device_flag, testrail_flag, tesults_flag, app_name, app_path = interactive_mode.ask_questions_mobile(
        #         mobile_os_name, mobile_os_version, device_name, app_package, app_activity, remote_flag, device_flag,
        #         testrail_flag, tesults_flag, app_name, app_path)
        test_mobile_obj = Mobile_Zero_Page(product=product_list.PatientPortal)
        test_mobile_obj.test_env = test_env
        test_mobile_obj.screenshot = screenshot_option

        # Setup Appium Server
        test_mobile_obj.start_appium()

        # Setup and register a driver
        test_mobile_obj.register_driver(mobile_os_name, mobile_os_version, device_name, app_package, app_activity,
                                        remote_flag, device_flag, app_name, app_path, ud_id, org_id, signing_id,
                                        no_reset_flag, appium_version)

        # # 3. Setup TestRail reporting
        # if testrail_flag.lower() == 'y':
        #     if test_run_id is None:
        #         test_mobile_obj.write(
        #             '\033[91m' + "\n\nTestRail Integration Exception: It looks like you are trying to use TestRail Integration without providing test run id. \nPlease provide a valid test run id along with test run command using -R flag and try again. for eg: pytest --testrail_flag Y -R 100\n" + '\033[0m')
        #         testrail_flag = 'N'
        #     if test_run_id is not None:
        #         test_mobile_obj.register_testrail()
        #         test_mobile_obj.set_test_run_id(test_run_id)
        #
        # if tesults_flag.lower() == 'y':
        #     test_mobile_obj.register_tesults()
        test_mobile_obj.start_time = int(time.time())

        yield test_mobile_obj

        # Teardown

        test_mobile_obj.wait(3)
        test_mobile_obj.teardown()

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def testname(request):
    "pytest fixture for testname"
    try:
        name_of_test = request.node.name
        name_of_test = name_of_test.split('[')[0]

        return name_of_test

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def test_run_id(request):
    "pytest fixture for test run id"
    try:
        return request.config.getoption("--test_run_id")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture()
def testID(request):
    if request.config.getoption("--bdd_flag") == 'Y':
        for i in request.node.own_markers:
            if i.name.startswith('ID_BDD'):
                return i.name
    else:
        raise Exception("Unable to find testID marker. It should start with ID_BDD if running with is_bdd "
                        "arguement=Y. It should be second parameterize if not runnign with bdd")


@pytest.fixture
def cases(request, product, testID):
    name = request.config.getoption("--xlsx")
    sheet = "Context"
    df = pd.read_excel("././conf/web/" + product + '/' + name, sheet_name=sheet, dtype=str, usecols=lambda x: 'Remark' not in x)
    df = df.fillna('')
    row = df.index[df['testID'] == testID].tolist()
    data = (df.loc[row[0]])
    return data

@pytest.fixture
def testrail_flag(request):
    "pytest fixture for test rail flag"
    try:
        return request.config.getoption("--testrail_flag")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def browser(request):
    """pytest fixture for browser, default browser set in here by config
    Originally default browser browser_os_name_conf when using pytest and logic set in conftest.py pytest_generate_tests() hook
    However pytest-bdd is not working with that hook, therefore comments that hook"""
    name = browser_os_name_conf.default_browser
    try:
        if len(request.config.getoption("--browser")) != 0:
            name = request.config.getoption("--browser")[0].lower()
    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))
    return name


@pytest.hookimpl()
def pytest_configure(config):
    global if_reportportal
    if_reportportal = config.getoption('--reportportal')

    # Registering custom markers to supress warnings
    config.addinivalue_line("markers", "GUI: mark a test as part of the GUI regression suite.")
    config.addinivalue_line("markers", "API: mark a test as part of the GUI regression suite.")
    config.addinivalue_line("markers", "MOBILE: mark a test as part of the GUI regression suite.")


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    filename = 'report_' + datetime.now().strftime(
        "%Y%m%d_%H%M%S") + '_' + config.known_args_namespace.keyword + ".html"  # report_YYYYMMDD_HHMMSS_[target].html
    path = os.path.join(config.rootdir, 'reports', filename)
    if html_report_conf.gen_report:
        config.option.htmlpath = path


def pytest_addoption(parser):
    "Method to add the option to ini."
    try:
        parser.addini("rp_uuid", 'help', type="pathlist")
        parser.addini("rp_endpoint", 'help', type="pathlist")
        parser.addini("rp_project", 'help', type="pathlist")
        parser.addini("rp_launch", 'help', type="pathlist")

        parser.addoption("--browser",
                         dest="browser",
                         action="append",
                         default=[],
                         help="Browser. Valid options are ff, ie, chrome, opera, safari")
        parser.addoption("--app_url",
                         dest="url",
                         default=base_url_conf.base_url,
                         help="The url of the application")
        parser.addoption("--api_url",
                         dest="url",
                         default="http://35.167.62.251",
                         help="The url of the api")
        parser.addoption("--testrail_flag",
                         dest="testrail_flag",
                         default='N',
                         help="Y or N. 'Y' if you want to report to TestRail")
        parser.addoption("--test_run_id",
                         dest="test_run_id",
                         default=None,
                         help="The test run id in TestRail")
        parser.addoption("--remote_flag",
                         dest="remote_flag",
                         default="N",
                         help="Run the test in Browserstack/Sauce Lab: Y or N")
        parser.addoption("--os_version",
                         dest="os_version",
                         action="append",
                         help="The operating system: xp, 7",
                         default=[])
        parser.addoption("--ver",
                         dest="browser_version",
                         action="append",
                         help="The version of the browser: a whole number",
                         default=[])
        parser.addoption("--os_name",
                         dest="os_name",
                         action="append",
                         help="The operating system: Windows 7, Linux",
                         default=[])
        parser.addoption("--remote_project_name",
                         dest="remote_project_name",
                         help="The project name if its run in BrowserStack",
                         default=None)
        parser.addoption("--remote_build_name",
                         dest="remote_build_name",
                         help="The build name if its run in BrowserStack",
                         default=None)
        parser.addoption("--slack_flag",
                         dest="slack_flag",
                         default="N",
                         help="Post the test report on slack channel: Y or N")
        parser.addoption("--mobile_os_name",
                         dest="mobile_os_name",
                         help="Enter operating system of mobile. Ex: Android, iOS",
                         default="Android")
        parser.addoption("--mobile_os_version",
                         dest="mobile_os_version",
                         help="Enter version of operating system of mobile: 8.1.0",
                         default="8.0")
        parser.addoption("--device_name",
                         dest="device_name",
                         help="Enter device name. Ex: Emulator, physical device name")
        parser.addoption("--app_package",
                         dest="app_package",
                         help="Enter name of app package. Ex: com.qhms.eportal.clinicone")
        parser.addoption("--app_activity",
                         dest="app_activity",
                         help="Enter name of app activity. Ex: com.qhms.eportal.clinicone.Views.Splash.DeepLinkEntryActivity")
        parser.addoption("--device_flag",
                         dest="device_flag",
                         help="Enter Y or N. 'Y' if you want to run the test on device. 'N' if you want to run the test on emulator.",
                         default="Y")
        parser.addoption("--email_pytest_report",
                         dest="email_pytest_report",
                         help="Email pytest report: Y or N",
                         default="N")
        parser.addoption("--tesults",
                         dest="tesults_flag",
                         default='N',
                         help="Y or N. 'Y' if you want to report results with Tesults")
        parser.addoption("--app_name",
                         dest="app_name",
                         help="Enter application name to be uploaded.Ex:Bitcoin Info_com.dudam.rohan.bitcoininfo.apk.",
                         default="Bitcoin Info_com.dudam.rohan.bitcoininfo.apk")
        parser.addoption("--ud_id",
                         dest="ud_id",
                         help="Enter your iOS device UDID which is required to run appium test in iOS device",
                         default=None)
        parser.addoption("--org_id",
                         dest="org_id",
                         help="Enter your iOS Team ID which is required to run appium test in iOS device",
                         default=None)
        parser.addoption("--signing_id",
                         dest="signing_id",
                         help="Enter your iOS app signing id which is required to run appium test in iOS device",
                         default="iPhone Developer")
        parser.addoption("--no_reset_flag",
                         dest="no_reset_flag",
                         help="Pass false if you want to reset app everytime you run app else false",
                         default="true")
        parser.addoption("--app_path",
                         dest="app_path",
                         help="Enter app path")
        parser.addoption("--appium_version",
                         dest="appium_version",
                         help="The appium version if its run in BrowserStack",
                         default="1.17.0")
        parser.addoption("--interactive_mode_flag",
                         dest="questionary",
                         default="n",
                         help="set the questionary flag")
        parser.addoption("--test_env",
                         dest="testenv",
                         default="",
                         help="Set testing environment. Eg. Prod, UAT",
                         required=True)
        parser.addoption("--screenshot",
                         dest="screenshot",
                         default='off',
                         help="Set on/off for screenshot feature. 3 mode can be set: 'all'/'failonly'/'off'. Default off")
        parser.addoption("--xlsx",
                         dest="xlsx",
                         default='',
                         help="Excel File name which need to get for config")
        parser.addoption("--case",
                         dest="case",
                         default="-1",
                         help="Number of case which need to run in Excel config. Do no use this option for running all cases. Input number > 0")
        parser.addoption("--caseid",
                         dest="caseid",
                         default='',
                         help="Case ID which need to run in Excel config. Do no use this option for running all cases. Only support 1 case")
    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


# def addoption_base(parser):
# "Method to add the option to ini."
# try:
#     parser.addini("rp_uuid", 'help', type="pathlist")
#     parser.addini("rp_endpoint", 'help', type="pathlist")
#     parser.addini("rp_project", 'help', type="pathlist")
#     parser.addini("rp_launch", 'help', type="pathlist")
#
#     parser.addoption("--browser",
#                      dest="browser",
#                      action="append",
#                      default=[],
#                      help="Browser. Valid options are ff, ie, chrome, opera, safari")
#     parser.addoption("--app_url",
#                      dest="url",
#                      default=base_url_conf.base_url,
#                      help="The url of the application")
#     parser.addoption("--api_url",
#                      dest="url",
#                      default="http://35.167.62.251",
#                      help="The url of the api")
#     parser.addoption("--testrail_flag",
#                      dest="testrail_flag",
#                      default='N',
#                      help="Y or N. 'Y' if you want to report to TestRail")
#     parser.addoption("--test_run_id",
#                      dest="test_run_id",
#                      default=None,
#                      help="The test run id in TestRail")
#     parser.addoption("--remote_flag",
#                      dest="remote_flag",
#                      default="N",
#                      help="Run the test in Browserstack/Sauce Lab: Y or N")
#     parser.addoption("--os_version",
#                      dest="os_version",
#                      action="append",
#                      help="The operating system: xp, 7",
#                      default=[])
#     parser.addoption("--ver",
#                      dest="browser_version",
#                      action="append",
#                      help="The version of the browser: a whole number",
#                      default=[])
#     parser.addoption("--os_name",
#                      dest="os_name",
#                      action="append",
#                      help="The operating system: Windows 7, Linux",
#                      default=[])
#     parser.addoption("--remote_project_name",
#                      dest="remote_project_name",
#                      help="The project name if its run in BrowserStack",
#                      default=None)
#     parser.addoption("--remote_build_name",
#                      dest="remote_build_name",
#                      help="The build name if its run in BrowserStack",
#                      default=None)
#     parser.addoption("--slack_flag",
#                      dest="slack_flag",
#                      default="N",
#                      help="Post the test report on slack channel: Y or N")
#     parser.addoption("--mobile_os_name",
#                      dest="mobile_os_name",
#                      help="Enter operating system of mobile. Ex: Android, iOS",
#                      default="Android")
#     parser.addoption("--mobile_os_version",
#                      dest="mobile_os_version",
#                      help="Enter version of operating system of mobile: 8.1.0",
#                      default="8.0")
#     parser.addoption("--device_name",
#                      dest="device_name",
#                      help="Enter device name. Ex: Emulator, physical device name")
#     parser.addoption("--app_package",
#                      dest="app_package",
#                      help="Enter name of app package. Ex: com.qhms.eportal.clinicone")
#     parser.addoption("--app_activity",
#                      dest="app_activity",
#                      help="Enter name of app activity. Ex: com.qhms.eportal.clinicone.Views.Splash.DeepLinkEntryActivity")
#     parser.addoption("--device_flag",
#                      dest="device_flag",
#                      help="Enter Y or N. 'Y' if you want to run the test on device. 'N' if you want to run the test on emulator.",
#                      default="Y")
#     parser.addoption("--email_pytest_report",
#                      dest="email_pytest_report",
#                      help="Email pytest report: Y or N",
#                      default="N")
#     parser.addoption("--tesults",
#                      dest="tesults_flag",
#                      default='N',
#                      help="Y or N. 'Y' if you want to report results with Tesults")
#     parser.addoption("--app_name",
#                      dest="app_name",
#                      help="Enter application name to be uploaded.Ex:Bitcoin Info_com.dudam.rohan.bitcoininfo.apk.",
#                      default="Bitcoin Info_com.dudam.rohan.bitcoininfo.apk")
#     parser.addoption("--ud_id",
#                      dest="ud_id",
#                      help="Enter your iOS device UDID which is required to run appium test in iOS device",
#                      default=None)
#     parser.addoption("--org_id",
#                      dest="org_id",
#                      help="Enter your iOS Team ID which is required to run appium test in iOS device",
#                      default=None)
#     parser.addoption("--signing_id",
#                      dest="signing_id",
#                      help="Enter your iOS app signing id which is required to run appium test in iOS device",
#                      default="iPhone Developer")
#     parser.addoption("--no_reset_flag",
#                      dest="no_reset_flag",
#                      help="Pass false if you want to reset app everytime you run app else false",
#                      default="true")
#     parser.addoption("--app_path",
#                      dest="app_path",
#                      help="Enter app path")
#     parser.addoption("--appium_version",
#                      dest="appium_version",
#                      help="The appium version if its run in BrowserStack",
#                      default="1.17.0")
#     parser.addoption("--interactive_mode_flag",
#                      dest="questionary",
#                      default="n",
#                      help="set the questionary flag")
#     parser.addoption("--test_env",
#                      dest="testenv",
#                      default="",
#                      help="Set testing environment. Eg. Prod, UAT",
#                      required=True)
#     parser.addoption("--screenshot",
#                      dest="screenshot",
#                      default='off',
#                      help="Set on/off for screenshot feature. 3 mode can be set: 'all'/'failonly'/'off'. Default off")
#     parser.addoption("--xlsx",
#                      dest="xlsx",
#                      default='',
#                      help="Excel File name which need to get for config")
#     parser.addoption("--case",
#                      dest="case",
#                      default="-1",
#                      help="Number of case which need to run in Excel config. Do no use this option for running all cases. Input number > 0")
# except Exception as e:
#     print("Exception when trying to run test: %s" % __file__)
#     print("Python says:%s" % str(e))


# def configure(config):
#     filename = 'report_' + datetime.now().strftime(
#         "%Y%m%d_%H%M%S") + '_' + config.known_args_namespace.keyword + ".html"  # report_YYYYMMDD_HHMMSS_[target].html
#     path = os.path.join(config.rootdir, 'reports', filename)
#     if html_report_conf.gen_report:
#         config.option.htmlpath = path


# def configure_base(config):
#     """Sets the launch name based on the marker selected."""
#     global if_reportportal
#     if_reportportal = config.getoption('--reportportal')
#
#     # Registering custom markers to supress warnings
#     config.addinivalue_line("markers", "GUI: mark a test as part of the GUI regression suite.")
#     config.addinivalue_line("markers", "API: mark a test as part of the GUI regression suite.")
#     config.addinivalue_line("markers", "MOBILE: mark a test as part of the GUI regression suite.")


# @pytest.hookimpl()
# def pytest_configure(config):
#     global if_reportportal
#     if_reportportal = config.getoption('--reportportal')
#
#     # Registering custom markers to supress warnings
#     config.addinivalue_line("markers", "GUI: mark a test as part of the GUI regression suite.")
#     config.addinivalue_line("markers", "API: mark a test as part of the GUI regression suite.")
#     config.addinivalue_line("markers", "MOBILE: mark a test as part of the GUI regression suite.")

@pytest.fixture(scope="session")
def base_url(request):
    "pytest fixture for base url"
    try:
        return request.config.getoption("--app_url")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def api_url(request):
    "pytest fixture for base url"
    try:
        return request.config.getoption("--api_url")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def remote_flag(request):
    "pytest fixture for browserstack/sauce flag"
    try:
        return request.config.getoption("--remote_flag")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def browser_version(request):
    "pytest fixture for browser version"
    try:
        return request.config.getoption("--ver")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def os_name(request):
    "pytest fixture for os_name"
    try:
        return request.config.getoption("--os_name")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def os_version(request):
    "pytest fixture for os version"
    try:
        return request.config.getoption("--os_version")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def remote_project_name(request):
    "pytest fixture for browserStack project name"
    try:
        return request.config.getoption("--remote_project_name")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def remote_project_name(request):
    "pytest fixture for browserStack project name"
    try:
        return request.config.getoption("--remote_project_name")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def remote_build_name(request):
    "pytest fixture for browserStack build name"
    try:
        return request.config.getoption("--remote_build_name")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def slack_flag(request):
    "pytest fixture for sending reports on slack"
    try:
        return request.config.getoption("--slack_flag")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def tesults_flag(request):
    "pytest fixture for sending results to tesults"
    try:
        return request.config.getoption("--tesults")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def mobile_os_name(request):
    "pytest fixture for mobile os name"
    try:
        return request.config.getoption("--mobile_os_name")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def mobile_os_version(request):
    "pytest fixture for mobile os version"
    try:
        return request.config.getoption("--mobile_os_version")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def device_name(request):
    "pytest fixture for device name"
    try:
        return request.config.getoption("--device_name")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def app_package(request):
    "pytest fixture for app package"
    try:
        return request.config.getoption("--app_package")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def app_activity(request):
    "pytest fixture for app activity"
    try:
        return request.config.getoption("--app_activity")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def device_flag(request):
    "pytest fixture for device flag"
    try:
        return request.config.getoption("--device_flag")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def email_pytest_report(request):
    "pytest fixture for device flag"
    try:
        return request.config.getoption("--email_pytest_report")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def app_name(request):
    "pytest fixture for app name"
    try:
        return request.config.getoption("--app_name")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def ud_id(request):
    "pytest fixture for iOS udid"
    try:
        return request.config.getoption("--ud_id")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def org_id(request):
    "pytest fixture for iOS team id"
    try:
        return request.config.getoption("--org_id")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def signing_id(request):
    "pytest fixture for iOS signing id"
    try:
        return request.config.getoption("--signing_id")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def appium_version(request):
    "pytest fixture for app name"
    try:
        return request.config.getoption("--appium_version")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def no_reset_flag(request):
    "pytest fixture for no_reset_flag"
    try:
        return request.config.getoption("--no_reset_flag")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def app_path(request):
    "pytest fixture for app path"
    try:
        return request.config.getoption("--app_path")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def interactivemode_flag(request):
    "pytest fixture for questionary module"
    try:
        return request.config.getoption("--interactive_mode_flag")

    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))


@pytest.fixture
def reportportal_service(request):
    "pytest service fixture for reportportal"
    reportportal_pytest_service = None
    try:
        if request.config.getoption("--reportportal"):
            reportportal_pytest_service = request.node.config.py_test_service
    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))

    return reportportal_pytest_service


@pytest.fixture
def test_env(request):
    "pytest service fixture for set test environment"
    test_env = "UAT"
    try:
        if request.config.getoption("--test_env"):
            test_env = request.config.getoption("--test_env").lower()
    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))

    return test_env


@pytest.fixture
def xlsx_config(request):
    "pytest service fixture for set test environment"
    xlsx_config = None
    try:
        if request.config.getoption("--xlsx"):
            xlsx_config = request.config.getoption("--xlsx")
    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))

    return xlsx_config


@pytest.fixture
def screenshot_option(request):
    """pytest service fixture for set enable or disable screenshot"""
    setup = "off"
    setting = request.config.getoption("--screenshot")
    try:
        if setting and setting.lower() == "all":
            setup = "all"
        elif setting and setting.lower() == "failonly":
            setup = "failonly"
        elif setting and setting.lower() == "off":
            setup = "off"
        elif setting:
            raise ValueError(
                "--screenshot option only allow all/failonly/off. Not allow %s. Set --screenshot off in this test" % setting)
    except Exception as e:
        print("Exception when trying to run test: %s" % __file__)
        print("Python says:%s" % str(e))

    return setup
