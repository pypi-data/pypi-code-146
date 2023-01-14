import os
import time
from collections import OrderedDict
import os as OS
from datetime import datetime

import allure

# report_configurations = COMMON.read_yaml(paths.REPORT_CONFIGURATION_YAML_FILE)
import pytest
import random

from py.xml import html, raw
from selenium.common import InvalidSessionIdException
from selenium.webdriver.support.wait import WebDriverWait

from config import nRoboConfig
import speedboat as speedboat
from helpers.DriverManager import DriverManager as DriverManager
from helpers.SeleniumWebdriverWrapper import SeleniumWebdriverWrapper as Report
from helpers import common as COMMON

# global driver reference
G_DRIVER = None

# global additional_drivers dictionary reference
G_DRIVERS_BY_WINDOW_NAME = None

# global additional_drivers dictionary reference
G_DRIVERS_BY_STATUS = None

# global current driver in focus dictionary reference
G_CURRENT_DRIVER_IN_FOCUS = None

# global marker reference
G_CURRENT_MARKER = None

# global runtime report configuration
G_REPORT_RUNTIME = {}


@pytest.fixture(scope="function")
def setup(request, pytestconfig):

    # user current marker reference
    global G_CURRENT_MARKER

    # Check if requested for NOGUI tests-backup
    # read expected report filename from report configuration yaml file
    # report_configurations = Common.read_yaml(paths.REPORT_CONFIGURATION_YAML_FILE)

    # just set current marker
    current_marker = nRoboConfig.TestReportSettings.REPORT_MARKER.value

    request.cls.current_marker = G_CURRENT_MARKER

    # get the test_output directory path
    if current_marker == nRoboConfig.Markers.MARKERS_NOGUI.value:
        # do nothing, and skip driver instance creation
        pass
    else:
        # use driver reference from global context
        global G_DRIVER

        # use additional_drivers reference from global context
        global G_DRIVERS_BY_WINDOW_NAME

        # use current_driver_in_focus reference from global context
        global G_CURRENT_DRIVER_IN_FOCUS

        global G_REPORT_RUNTIME

        # now, add random pause between tests-backup
        time.sleep(random.randint(
            nRoboConfig.TimeLimits.TIME_MIN_LIMIT_TO_MAKE_TEST_ASYNCHRONOUS.value,
            nRoboConfig.TimeLimits.TIME_MAX_LIMIT_TO_MAKE_TEST_ASYNCHRONOUS.value
        ))

        # set the application url

        G_REPORT_RUNTIME[nRoboConfig.CommandLineSwitchesLong.URL.value] = os.environ[nRoboConfig.CommandLineSwitchesLong.URL.value]  # pytestconfig.getoption(CONFIG.APP_LINK)
        G_REPORT_RUNTIME[nRoboConfig.CommandLineSwitchesLong.APP_NAME.value] = os.environ[nRoboConfig.CommandLineSwitchesLong.APP_NAME.value]  # pytestconfig.getoption(CONFIG.APP_NAME)
        G_REPORT_RUNTIME[nRoboConfig.CommandLineSwitchesLong.USERNAME.value] = os.environ[nRoboConfig.CommandLineSwitchesLong.USERNAME.value]  # pytestconfig.getoption(CONFIG.USERNAME)
        G_REPORT_RUNTIME[nRoboConfig.CommandLineSwitchesLong.BROWSER.value] = os.environ[nRoboConfig.CommandLineSwitchesLong.BROWSER.value]  # pytestconfig.getoption(CONFIG.USERNAME)

        # create an instance of Chrome webdriver
        driver = DriverManager.get_browser(os.environ[nRoboConfig.CommandLineSwitchesLong.BROWSER.value])

        # maximize the browser window
        driver.maximize_window()

        # Log it
        Report.log.info("Step: Open Sphere WMS in browser.")

        # launch the application url
        # driver.get("http://google.com")

        # wait until page loads
        WebDriverWait(driver, nRoboConfig.Waits.TIMEOUT.value).until(
            lambda driver: driver.execute_script('return document.readyState') == 'complete')
        # assert driver.title == "SphereWMS", "Failed to open Shpere WMS in browser."

        # set class driver to driver
        request.cls.driver = driver

        # set class additional drivers-backup
        G_DRIVERS_BY_WINDOW_NAME = {'main': driver}
        request.cls.drivers_by_window_name = G_DRIVERS_BY_WINDOW_NAME

        # set class current driver
        G_CURRENT_DRIVER_IN_FOCUS = {"current_driver": driver}
        request.cls.current_driver_in_focus = G_CURRENT_DRIVER_IN_FOCUS

    # wait until test completes
    yield driver, G_DRIVERS_BY_WINDOW_NAME, G_REPORT_RUNTIME, G_CURRENT_MARKER, G_CURRENT_DRIVER_IN_FOCUS

    # raise Exception("After test completion")
    if current_marker == nRoboConfig.Markers.MARKERS_NOGUI.value:
        """do nothing, just return to the world of humans"""
        return

    # print(current_driver_in_focus)
    # print(additional_drivers)
    # print(driver)

    # delete all browser cookies, close driver, quit browser
    for key in G_DRIVERS_BY_WINDOW_NAME:

        try:
            # delete all browser cookies
            G_DRIVERS_BY_WINDOW_NAME[key].delete_all_cookies()
        except InvalidSessionIdException as ise:
            pass

        # close browser
        # additional_drivers[key].close()

        # quit browser
        G_DRIVERS_BY_WINDOW_NAME[key].quit()

    # assert "Speedboat" == "Speedboat", "Hey Spherobot failed to live."


def pytest_addoption(parser):
    """
    Description
        Override pytest addoption fixture
    """
    # get the credentials from credentials.yaml file, in case, user has not supplied it in command line argument
    # credentials = Common.read_yaml(paths.CREDENTIALS_YAML_FILE)
    # print(credentials)

    # set pytest additional options
    parser.addoption("--app", action="store", default=None, help="Application Name")
    parser.addoption("--app_link", action="store", default=None, help="Application link")
    parser.addoption("--username", action="store", default=None, help="Username")
    parser.addoption("--password", action="store", default=None, help="Password")
    parser.addoption("--browser", action="store", default=nRoboConfig.Browsers.HEADLESS_CHROME.value, help="Browser")


@pytest.fixture(scope="function")
def username(pytestconfig):
    """
    Description
        This method when called returns username

    Returns
        username -> str obj : current username
    """

    # Check if username was supplied as pytest command line arguments
    if len(pytestconfig.getoption(nRoboConfig.CommandLineSwitchesLong.USERNAME.value)) > 0:
        """if username is supplied, return username"""
        return pytestconfig.getoption(nRoboConfig.CommandLineSwitchesLong.USERNAME.value)
    else:
        # try to find username from credentials.yaml file
        # credentials = Common.read_yaml(paths.CREDENTIALS_YAML_FILE)
        # return credentials[field_constants.USERNAME]
        pass


@pytest.fixture(scope="function")
def password(pytestconfig):
    """
    Description
        This method when called returns username

    Returns
        password -> str obj : current user's password
    """

    # Check if username was supplied as pytest command line arguments
    if len(pytestconfig.getoption(nRoboConfig.CommandLineSwitchesLong.PASSWORD.value)) > 0:
        """if username is supplied, return username"""
        return pytestconfig.getoption(nRoboConfig.CommandLineSwitchesLong.PASSWORD.value)
    else:
        # try to find username from credentials.yaml file
        # credentials = Common.read_yaml(paths.CREDENTIALS_YAML_FILE)
        # return credentials[field_constants.PASSWORD]
        pass


@pytest.fixture(scope="function")
def url(pytestconfig):
    """
    Description
        This method when called returns url

    Returns
        url -> str obj : current url
    """

    # Check if url was supplied as pytest command line arguments
    if len(pytestconfig.getoption(nRoboConfig.CommandLineSwitchesLong.APP_LINK.value)) > 0:
        """if URL is supplied, return URL"""
        return pytestconfig.getoption(nRoboConfig.Constants.HYPEN.value + nRoboConfig.Constants.HYPEN.value + nRoboConfig.CommandLineSwitchesLong.APP_LINK.value)
    else:
        # try to find url from credentials.yaml file
        # credentials = Common.read_yaml(paths.CREDENTIALS_YAML_FILE)
        # return credentials[field_constants.APP_LINK]
        pass


@pytest.fixture(scope="function")
def browser(pytestconfig):
    """
    Description
        This method when called returns url

    Returns
        url -> str obj : current url
    """

    # Check if url was supplied as pytest command line arguments
    if len(pytestconfig.getoption(nRoboConfig.CommandLineSwitchesLong.BROWSER.value)) > 0:
        """if URL is supplied, return URL"""
        return pytestconfig.getoption(nRoboConfig.Constants.HYPEN.value + nRoboConfig.Constants.HYPEN.value + nRoboConfig.CommandLineSwitchesLong.BROWSER.value)
    else:
        # try to find url from credentials.yaml file
        # credentials = Common.read_yaml(paths.CREDENTIALS_YAML_FILE)
        # return credentials[field_constants.APP_LINK]
        pass


#@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Description

    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    print(str(item.function.__doc__))
    extra = getattr(report, 'extra', [])
    if report.when == 'call':
        # load report configurations
        # report_configurations = Common.read_yaml(paths.REPORT_CONFIGURATION_YAML_FILE)

        # always add url to report
        extra.append(pytest_html.extras.url(nRoboConfig.URL))

        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) \
                or (report.failed and not xfail) \
                or (report.passed and not xfail):
            """if failure, only add additional html on failure """

            # generate a random file name
            file_name = str(round(time.time() * 1000)) + ".png"

            # get the screenshots directory
            screenshot_directory = nRoboConfig.Paths.TEST_OUTPUT_SCREENSHOT_DIR_WITH_SLASH.value

            # screenshots' full name
            save_screenshot_name = screenshot_directory + file_name

            # screenshots' relative path
            relative_fileName = nRoboConfig.Paths.TEST_OUTPUT_SCREENSHOT_RELATIVE_DIR.value \
                                + OS.path.sep + file_name

            # current directory name
            current_directory = OS.path.dirname(__file__)

            if not OS.path.exists(screenshot_directory):
                """if screenshot directory does not exist, create it"""
                OS.makedirs(screenshot_directory)

            # print("report")
            # print(additional_drivers)
            # print(current_driver_in_focus)
            # #print(driver)
            # print("report...")

            if G_CURRENT_MARKER == nRoboConfig.Markers.MARKERS_NOGUI.value:
                """if current marker is NOGUI, then no need to take screenshot"""
                return

            # save screenshot by using webdrivers' method
            driver = G_CURRENT_DRIVER_IN_FOCUS["current_driver"]  # reset current driver in focus
            driver.save_screenshot(save_screenshot_name)

            # get base64 screenshot
            failure_screen_shot = driver.get_screenshot_as_base64()

            # attach screenshot with html report
            extra.append(pytest_html.extras.image(failure_screen_shot))

            # add relative url to screenshot in the html report
            extra.append(pytest_html.extras.url(relative_fileName, name="View Screenshot"))

            # Handle screenshot for Allure Report
            if speedboat.get_value_of_cli_switch(speedboat.validateCommandLineSwitches(),
                                                 nRoboConfig.CommandLineSwitchesShort.REPORT_TYPE.value) == nRoboConfig.TestReportSettings.REPORT_TYPE_ALLURE.value:
                    try:
                        allure.attach(
                            driver.get_screenshot_as_png(),
                            name='screenshot',
                            attachment_type=allure.attachment_type.PNG
                        )
                    except Exception as e:
                        print('Fail to take screen-shot: {}'.format(e))

        # Finally, add all extra table column data in the html report
        report.extra = extra

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield

    report = outcome.get_result()
    extra = getattr(report, 'extra', [])

    if report.when == 'call' : #and rep.failed:

        pytest_html = item.config.pluginmanager.getplugin('html')
        extra.append(pytest_html.extras.url(nRoboConfig.URL))

        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail):
            return # Nothing to do
        elif (report.failed and not xfail) \
                or (report.passed and not xfail):

            driver = G_CURRENT_DRIVER_IN_FOCUS["current_driver"]  # reset current driver in focus

            try:

                allure.attach(
                    driver.get_screenshot_as_png(),
                    name='screenshot',
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print('Fail to take screen-shot: {}'.format(e))

            try:


                # generate a random file name
                file_name = str(round(time.time() * 1000)) + ".png"

                # get the screenshots directory
                screenshot_directory = nRoboConfig.Paths.TEST_OUTPUT_SCREENSHOT_DIR_WITH_SLASH.value

                # screenshots' full name
                save_screenshot_name = screenshot_directory + file_name

                # screenshots' relative path
                relative_fileName = nRoboConfig.Paths.TEST_OUTPUT_SCREENSHOT_RELATIVE_DIR.value \
                                    + OS.path.sep + file_name

                # current directory name
                current_directory = OS.path.dirname(__file__)

                if not OS.path.exists(screenshot_directory):
                    """if screenshot directory does not exist, create it"""
                    OS.makedirs(screenshot_directory)

                if G_CURRENT_MARKER == nRoboConfig.Markers.MARKERS_NOGUI.value:
                    """if current marker is NOGUI, then no need to take screenshot"""
                    return

                driver.save_screenshot(save_screenshot_name)

                # get base64 screenshot
                failure_screen_shot = driver.get_screenshot_as_base64()

                # attach screenshot with html report
                extra.append(pytest_html.extras.image(failure_screen_shot))

                # add relative url to screenshot in the html report
                extra.append(pytest_html.extras.url(relative_fileName, name="View Screenshot"))

            except Exception as e:
                print(e)

        # Finally, add all extra table column data in the html report
        report.extra = extra



def pytest_html_results_summary(prefix, summary, postfix):
    """
    Description
        This pytest html report hook is called before adding the summary section to the report
    """

    # Add Sphere Logo in the report
    prefix.append(html.div(
        html.img(id='sphere_logo', src_=nRoboConfig.TestReportSettings.APPLICATION_LOGO_URL, style_='height: 40px'),
        # class_='chart-container', style_='position: absolute; height:10px; top: 5px; right: 30px')
        style_='position: absolute; top: 10px; right: 30px')
    )

    # Help url
    # https://www.chartjs.org/docs/latest/charts/doughnut.html
    with open(
            OS.path.join(OS.path.dirname(__file__),
                         "assets" + OS.path.sep +
                         "chartjs" + OS.path.sep +
                         "3_2_1" + OS.path.sep +
                         "package" + OS.path.sep +
                         "dist", "chart.js")
    ) as main_js_fp:
        chart_js = main_js_fp.read()

    prefix.append(html.script(raw(chart_js)))
    prefix.append(html.script(raw("""
        src='https://cdn.jsdelivr.net/npm/chart.js@3.2.1/dist/chart.min.js'
    """)))
    prefix.append(html.div(
        html.canvas(id='spherobot_result_chart'),
        # class_='chart-container', style_='position: absolute; height:20vh; width:20vw; top: 0px; right: 0px')
        class_='chart-container', style_='position: absolute; width:20.5rem; top: 60px; right: 30px')
    )

    # report_configurations = Common.read_yaml(paths.REPORT_CONFIGURATION_YAML_FILE)

    # update report configuration
    passed = G_REPORT_RUNTIME[nRoboConfig.TestReportSettings.REPORT_PASSED.value]
    skipped = G_REPORT_RUNTIME[nRoboConfig.TestReportSettings.REPORT_SKIPPED.value]
    failed = G_REPORT_RUNTIME[nRoboConfig.TestReportSettings.REPORT_FAILED.value]
    errors = G_REPORT_RUNTIME[nRoboConfig.TestReportSettings.REPORT_ERRORS.value]
    expected_failures = G_REPORT_RUNTIME[nRoboConfig.TestReportSettings.REPORT_EXPECTED_FAILURES.value]
    unexpected_passes = G_REPORT_RUNTIME[nRoboConfig.TestReportSettings.REPORT_UNEXPECTED_PASSES.value]
    reruns = G_REPORT_RUNTIME[nRoboConfig.TestReportSettings.REPORT_RERUN.value]

    with open(
            OS.path.join(OS.path.dirname(__file__),
                         "assets", "report_chart_js_dataset_and_config_snippet.js")
    ) as main_js_fp:
        report_chart_js_dataset_and_config_snippet = main_js_fp.read()

    prefix.append(html.script(raw(
        report_chart_js_dataset_and_config_snippet.replace("[]", "[{}, {}, {}, {}, {}, {}, {}]"
                                                           .format(
            passed, skipped, failed, errors,
            expected_failures, unexpected_passes, reruns
        ))
    )))

    with open(
            OS.path.join(OS.path.dirname(__file__),
                         "assets", "report_chart_javascript_snippet.js")
    ) as main_js_fp:
        report_chart_javascript_snippet_js = main_js_fp.read()

    summary.extend([html.script(raw(report_chart_javascript_snippet_js))])
    postfix.extend([html.p("")])


def pytest_html_results_table_header(cells):
    """
    Description
        This pytest html report hook is called after building results table header.
    """
    pass


def pytest_html_results_table_html(report, data):
    """
    Description
        This pytest html report is called after building results table additional HTML.
    """

    pass


def pytest_html_results_table_row(report, cells):
    """
    Description
        This pytest html report is called after building results table row.
    """

    pass


def pytest_html_report_title(report):
    """
    Description
        This pytest html report hook is called before adding the title to the report
    """
    # report_configurations = Common.read_yaml(paths.REPORT_CONFIGURATION_YAML_FILE)
    # report.title = report_configurations[field_constants.APP_NAME].upper() + " Automation Test Result Report"

    report.title = (os.environ[nRoboConfig.CommandLineSwitchesLong.APP.value] + nRoboConfig.Constants.SPACE.value + "automated test Report").title()

    # now load the actual test status counts and update report configuration
    G_REPORT_RUNTIME[nRoboConfig.TestReportSettings.REPORT_PASSED.value] = report.passed
    G_REPORT_RUNTIME[nRoboConfig.TestReportSettings.REPORT_SKIPPED.value] = report.skipped
    G_REPORT_RUNTIME[nRoboConfig.TestReportSettings.REPORT_FAILED.value] = report.failed
    G_REPORT_RUNTIME[nRoboConfig.TestReportSettings.REPORT_ERRORS.value] = report.errors
    G_REPORT_RUNTIME[nRoboConfig.TestReportSettings.REPORT_EXPECTED_FAILURES.value] = report.xfailed
    G_REPORT_RUNTIME[nRoboConfig.TestReportSettings.REPORT_UNEXPECTED_PASSES.value] = report.xpassed
    G_REPORT_RUNTIME[nRoboConfig.TestReportSettings.REPORT_RERUN.value] = report.rerun


def pytest_configure(config):
    """
    Description
        pytest configure fixture method.
    """

    # read expected report filename from report configuration yaml file
    # report_configurations = COMMON.read_yaml(paths.REPORT_CONFIGURATION_YAML_FILE)

    # get the test_output directory path
    source = nRoboConfig.Paths.TEST_OUTPUT_DIR_WITH_SLASH.value

    if not OS.path.exists(source):
        """if test_output directory does not exist, create it"""
        OS.makedirs(source)

    # set pytest-html config option
    config.option.htmlpath = nRoboConfig.Paths.TEST_OUTPUT_DIR_WITH_SLASH.value \
                             + nRoboConfig.TestReportSettings.HTML_REPORT_FILE_NAME_PREFIX.value \
                             + datetime.now().strftime(nRoboConfig.DateTimeFormats.DD_MM_YY_HH_MM_SS.value) \
                             + nRoboConfig.Extensions.HTML.value

    # set pytest-html config option
    config.option.self_contained_html = True

    # Save config values as ENVIRONMENT VARIABLES
    os.environ[nRoboConfig.CommandLineSwitchesLong.APP_NAME.value] = config.getoption(nRoboConfig.CommandLineSwitchesLong.APP_NAME.value).capitalize()
    os.environ[nRoboConfig.CommandLineSwitchesLong.URL.value] = config.getoption(nRoboConfig.CommandLineSwitchesLong.APP_LINK.value).lower()
    os.environ[nRoboConfig.CommandLineSwitchesLong.USERNAME.value] = config.getoption(nRoboConfig.CommandLineSwitchesLong.USERNAME.value)
    os.environ[nRoboConfig.CommandLineSwitchesLong.BROWSER.value] = config.getoption(nRoboConfig.CommandLineSwitchesLong.BROWSER.value)

    #print(os.environ)
    config._metadata = build_metadata(
        os.environ[nRoboConfig.CommandLineSwitchesLong.APP.value],
        os.environ[nRoboConfig.CommandLineSwitchesLong.URL.value],
        os.environ[nRoboConfig.CommandLineSwitchesLong.USERNAME.value])

    # add custom markers
    for marker in nRoboConfig.Markers.MARKERS_SPEEDBOAT.value:
        config.addinivalue_line("markers", marker)


def pytest_metadata(metadata):
    """
    Description
        overriding pytest metadata fixture
    """

    # pop all the python environment table data
    metadata.pop("Packages", None)
    metadata.pop("Platform", None)
    metadata.pop("Plugins", None)
    metadata.pop("Python", None)


def build_metadata(app_name: str, app_link: str, username: str) -> OrderedDict:
    """
    Description
        Builds the environment table data from the given params.

    Params
        app_name -> str : Application name
        app_link -> str : Application URL

    Return
        metadata -> OrderedDict : An object of OrderedDict that contains all the envionment data.
    """

    # create an instance of OrderedDict()
    metadata = OrderedDict()

    # add environment details

    metadata['Product'] = app_name  # add Product name
    metadata['URL'] = app_link  # add application url under test

    metadata['Run By'] = "{0}".format(username.capitalize())  # add application url under test

    # metadata['Host Internet Speed'] = "{} Mbps".format(internet_speed)  # add Host internet speed in Mbps

    return metadata  # build and return environment metadata

#
# @pytest.fixture
# def attach_screenshot():
#     yield
#     allure.attach(body="body", name="attachment from teardown")