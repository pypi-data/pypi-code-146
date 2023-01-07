import logging

import pytest
from _pytest.reports import BaseReport

logger = logging.getLogger("pytest_result_log")

__test_set = set()


def pytest_cmdline_parse():
    global __test_set

    __test_set = set()


@pytest.hookimpl(hookwrapper=True, trylast=True)
def pytest_report_teststatus(report: BaseReport):
    outcome = yield
    result = outcome.get_result()

    if report.nodeid in __test_set:
        return

        # return
    if report.when == "setup":
        match result[1]:
            case "s":
                logger.info(f"test status is {result[2]} ({report.nodeid})")
                __test_set.add(report.nodeid)
            case "E":
                logger.error(f"test status is {result[2]} ({report.nodeid})")
                __test_set.add(report.nodeid)

    if report.when == "call":

        match result[1]:
            case ".":
                logger.info(f"test status is {result[2]} ({report.nodeid})")
                __test_set.add(report.nodeid)
            case _:
                logger.warning(f"test status is {result[2]} ({report.nodeid})")
                __test_set.add(report.nodeid)
