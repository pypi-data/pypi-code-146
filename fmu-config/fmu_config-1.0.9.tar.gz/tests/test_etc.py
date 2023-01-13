"""Testing the classes/functions in in the etc module."""
import os

import pytest

from fmu.config import etc

fmux = etc.Interaction()
logger = fmux.basiclogger(__name__)

logger.info("Running tests...")


# always this statement
if not fmux.testsetup():
    raise SystemExit()


def test_info_logger_plain():
    """Test basic logger behaviour plain, will capture output to stdin"""
    logger.info("This is a test")
    # no assert is intended


@pytest.fixture(name="mylogger")
def fixture_mylogger():
    """Add logger"""
    # need to do it like this...
    mlogger = fmux.basiclogger(__name__, level="DEBUG")
    return mlogger


def test_info_logger(mylogger, caplog):
    """Test basic logger behaviour, will capture output to stdin"""

    mylogger.info("This is a test")
    assert "This is a test" in caplog.text

    logger.warning("This is a warning")
    assert "This is a warning" in caplog.text


def test_more_logging_tests(caplog):
    """Testing on the logging levels, see that ENV variable will override
    the basiclogger setting.
    """

    os.environ["FMU_LOGGING_LEVEL"] = "INFO"

    fmumore = etc.Interaction()  # another instance
    locallogger = fmumore.basiclogger(__name__, level="WARNING")
    locallogger.debug("Display debug")
    assert caplog.text == ""  # shall be empty
    locallogger.info("Display info")
    assert "info" in caplog.text  # INFO shall be shown, overrided by ENV!
    locallogger.warning("Display warning")
    assert "warning" in caplog.text
    locallogger.critical("Display critical")
    assert "critical" in caplog.text


def test_timer(capsys):
    """Test the timer function"""

    time1 = fmux.timer()
    for inum in range(100000):
        inum += 1

    fmux.echo(f"Used time was {fmux.timer(time1)}")
    captured = capsys.readouterr()
    assert "Used time was" in captured[0]
    # repeat to see on screen
    fmux.echo("")
    fmux.warn(f"Used time was {fmux.timer(time1)}")


def test_print_fmu_header():
    """Test writing an app header."""
    fmux.print_fmu_header("MYAPP", "0.99", info="Beta release (be careful)")


def test_user_msg():
    """Testing user messages"""

    fmux.echo("")
    fmux.echo("This is a message")
    fmux.warn("This is a warning")
    fmux.warning("This is also a warning")
    fmux.error("This is an error")
    fmux.critical("This is a critical error", sysexit=False)
