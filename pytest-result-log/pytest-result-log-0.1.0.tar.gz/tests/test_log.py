import pytest
from _pytest.pytester import Pytester

pytest_plugins = "pytester"


def test_case_is_pass(pytester: Pytester):
    pytester.makepyfile(
        """
        import pytest

        pytest_plugins = "pytester"

        def test_pass():
            assert True
    """
    )
    result = pytester.runpytest(
        "--log-cli-level",
        "info",
        "--log-cli-format",
        "%(levelname)-8s:%(message)s",
    )
    result.assert_outcomes(passed=1)

    result.stdout.fnmatch_lines(
        ["INFO    :test status is PASSED (test_case_is_pass.py::test_pass)"]
    )


def test_case_is_fail(pytester: Pytester):
    pytester.makepyfile(
        """
        import pytest

        pytest_plugins = "pytester"

        def test_fail():
            assert 0
    """
    )
    result = pytester.runpytest(
        "--log-cli-level",
        "info",
        "--log-cli-format",
        "%(levelname)-8s:%(message)s",
    )
    result.assert_outcomes(failed=1)

    result.stdout.fnmatch_lines(
        ["WARNING :test status is FAILED (test_case_is_fail.py::test_fail)"]
    )


def test_case_is_error(pytester: Pytester):
    pytester.makepyfile(
        """
        import pytest

        pytest_plugins = "pytester"

        def test_error(xxxx):
            assert 0
    """
    )
    result = pytester.runpytest(
        "--log-cli-level",
        "info",
        "--log-cli-format",
        "%(levelname)-8s:%(message)s",
    )
    result.assert_outcomes(errors=1)

    result.stdout.fnmatch_lines(
        ["ERROR   :test status is ERROR (test_case_is_error.py::test_error)"]
    )


def test_case_is_skip(pytester: Pytester):
    pytester.makepyfile(
        """
        import pytest

        pytest_plugins = "pytester"

        @pytest.mark.skip
        def test_skip():
            assert 0
    """
    )
    result = pytester.runpytest(
        "--log-cli-level",
        "info",
        "--log-cli-format",
        "%(levelname)-8s:%(message)s",
    )
    result.assert_outcomes(skipped=1)

    result.stdout.fnmatch_lines(
        ["INFO    :test status is SKIPPED (test_case_is_skip.py::test_skip)"]
    )


def test_case_is_xpass(pytester: Pytester):
    pytester.makepyfile(
        """
        import pytest

        pytest_plugins = "pytester"

        @pytest.mark.xfail
        def test_xpass():
            assert True
    """
    )
    result = pytester.runpytest(
        "--log-cli-level",
        "info",
        "--log-cli-format",
        "%(levelname)-8s:%(message)s",
    )
    result.assert_outcomes(xpassed=1)

    result.stdout.fnmatch_lines(
        ["WARNING :test status is XPASS (test_case_is_xpass.py::test_xpass)"]
    )


def test_case_is_xfail(pytester: Pytester):
    pytester.makepyfile(
        """
        import pytest

        pytest_plugins = "pytester"

        @pytest.mark.xfail
        def test_xfail():
            assert 0
    """
    )
    result = pytester.runpytest(
        "--log-cli-level",
        "info",
        "--log-cli-format",
        "%(levelname)-8s:%(message)s",
    )
    result.assert_outcomes(xfailed=1)

    result.stdout.fnmatch_lines(
        ["WARNING :test status is XFAIL (test_case_is_xfail.py::test_xfail)"]
    )
