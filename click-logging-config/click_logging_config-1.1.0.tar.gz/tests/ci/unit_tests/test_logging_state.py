#
#  Copyright (c) 2022 Russell Smiley
#
#  This file is part of click_logging_config.
#
#  You should have received a copy of the MIT License along with click_logging_config.
#  If not, see <https://opensource.org/licenses/MIT>.
#

import json
import logging
import pathlib
import re
import typing
from json import JSONDecodeError

import pytest

from click_logging_config._default_values import (
    DEFAULT_LOG_FILE,
    VALID_LOG_LEVELS,
)
from click_logging_config._logging import LoggingConfiguration, LoggingState
from tests.ci.support.directory import change_directory  # noqa: F401

EXPECTED_NONJSON_FORMAT = r"[0-9\-]+T[0-9:.+]+::INFO::.+::{0}"


@pytest.fixture()
def mock_config() -> typing.Callable[
    [typing.Optional[dict]], LoggingConfiguration
]:
    def _apply(
        attributes: typing.Optional[dict] = None,
    ) -> LoggingConfiguration:
        if attributes:
            f = attributes
        else:
            f = {"log_level": "debug"}
        v = LoggingConfiguration.parse_obj(f)

        return v

    return _apply


def test_clean(capsys, caplog, mock_config):
    this_config = mock_config()
    expected_log_level_value = getattr(logging, this_config.log_level.upper())

    root_logger = logging.getLogger()

    assert root_logger.getEffectiveLevel() != expected_log_level_value

    with change_directory() as c:
        under_test = LoggingState(this_config)

    assert root_logger.getEffectiveLevel() == expected_log_level_value


def test_file_logging(mock_config):
    this_config = mock_config()
    this_config.enable_file_logging = True

    with change_directory() as c:
        under_test = LoggingState(this_config)

        assert under_test._rotation_handler is not None
        handlers = logging.getLogger().handlers
        assert under_test._rotation_handler in handlers


def test_disabled_file_logging(mock_config):
    this_config = mock_config()
    this_config.enable_file_logging = False

    with change_directory() as c:
        under_test = LoggingState(this_config)

        assert under_test._rotation_handler is None


def test_file_json_enabled(mock_config):
    this_config = mock_config()
    this_config.enable_file_logging = True
    this_config.file_logging.json_enabled = True

    expected_message = f"test message, {__name__}"

    with change_directory() as c:
        file_log = this_config.file_logging.log_file_path
        under_test = LoggingState(this_config)
        log = logging.getLogger(__name__)
        log.info(expected_message)
        log.debug("another message")

        with file_log.open(mode="r") as f:
            content = f.read()

    s = content.splitlines(keepends=False)
    data = [json.loads(x) for x in s]

    assert any(expected_message in x["message"] for x in data)


def test_file_json_disabled(mock_config):
    this_config = mock_config()
    this_config.enable_file_logging = True
    this_config.file_logging.json_enabled = False

    expected_message = f"test message, {__name__}"

    with change_directory() as c:
        file_log = this_config.file_logging.log_file_path
        under_test = LoggingState(this_config)
        log = logging.getLogger(__name__)
        log.info(expected_message)

        with file_log.open(mode="r") as f:
            content = f.read()

    try:
        json.loads(content)

        pytest.fail("json file logging is supposed to have been disabled")
    except JSONDecodeError:
        # error reading json is okay because the content should not be json
        pass

    assert any(
        [
            re.match(EXPECTED_NONJSON_FORMAT.format("test message,.*"), x)
            for x in content.splitlines(keepends=False)
        ]
    )


def test_disabled_file_post_construction(mock_config):
    this_config = mock_config()
    this_config.enable_file_logging = True

    with change_directory() as c:
        under_test = LoggingState(this_config)

        assert under_test._rotation_handler is not None
        under_test.configuration.enable_file_logging = False
        under_test.set_logging_state()

        assert under_test._rotation_handler is None


def _count_stream_handlers() -> int:
    stream_handlers = [
        isinstance(h, logging.StreamHandler)
        for h in logging.getLogger().handlers
    ]
    return len(stream_handlers)


def test_enabled_console_logging(mock_config):
    this_config = mock_config()
    this_config.enable_file_logging = False
    this_config.enable_console_logging = True

    sh_before = _count_stream_handlers()
    with change_directory() as c:
        under_test = LoggingState(this_config)

        sh_after = _count_stream_handlers()
        assert sh_after == sh_before + 1


def test_disabled_console_logging(mock_config):
    this_config = mock_config()
    this_config.enable_file_logging = False
    this_config.enable_console_logging = False
    this_config.console_logging.json_enabled = True

    sh_before = _count_stream_handlers()
    with change_directory() as c:
        under_test = LoggingState(this_config)

        sh_after = _count_stream_handlers()
        # expect no change to stream handlers
        assert sh_after == sh_before


def test_enabled_console_json(capsys, mock_config):
    this_config = mock_config()
    this_config.enable_file_logging = False
    this_config.enable_console_logging = True
    this_config.console_logging.json_enabled = True

    expected_message = f"test message, {__name__}"

    with change_directory() as c:
        under_test = LoggingState(this_config)
        log = logging.getLogger(__name__)
        log.info(expected_message)

    content = capsys.readouterr().err

    s = content.splitlines(keepends=False)
    data = [json.loads(x) for x in s]

    assert any(expected_message in x["message"] for x in data)


def test_disabled_console_json(capsys, mock_config):
    this_config = mock_config()
    this_config.enable_file_logging = False
    this_config.enable_console_logging = True
    this_config.console_logging.json_enabled = False

    expected_message = f"test message, {__name__}"

    with change_directory() as c:
        under_test = LoggingState(this_config)
        log = logging.getLogger(__name__)
        log.info(expected_message)

    console_content = capsys.readouterr()
    content = console_content.err

    try:
        json.loads(content)

        pytest.fail("json console logging is supposed to have been disabled")
    except JSONDecodeError:
        # error reading json is okay because the content should not be json
        pass

    assert any(
        [
            re.match(EXPECTED_NONJSON_FORMAT.format("test message,.*"), x)
            is not None
            for x in content.splitlines(keepends=False)
        ]
    )


def test_disabled_console_post_construction(mock_config):
    this_config = mock_config()
    this_config.enable_file_logging = False
    this_config.enable_console_logging = True

    with change_directory() as c:
        under_test = LoggingState(this_config)

        sh_before = _count_stream_handlers()

        under_test.configuration.enable_console_logging = False
        under_test.set_logging_state()

        sh_after = _count_stream_handlers()
        # the exact reduction seems to be unpredictable...
        assert sh_after < sh_before


def test_enabled_console_post_construction(mock_config):
    this_config = mock_config()
    this_config.enable_file_logging = False
    this_config.enable_console_logging = False

    with change_directory() as c:
        under_test = LoggingState(this_config)

        sh_before = _count_stream_handlers()

        under_test.configuration.enable_console_logging = True
        under_test.set_logging_state()

        sh_after = _count_stream_handlers()
        assert sh_after == sh_before + 1


class TestLoggingStateGeneratedLogs:
    @pytest.mark.skip("not sure if this test is valid")
    def test_disable_console_logging(self, capsys, mock_config):
        attributes = {
            "enable_file_logging": False,
            "enable_console_logging": False,
            "log_level": "warning",
        }
        this_config = mock_config(attributes)
        this_config.log_level = "warning"

        captured_err, captured_out, _ = self._do_test(this_config, capsys)

        assert not captured_err
        assert not captured_out

    def _do_test(
        self, this_config: LoggingConfiguration, this_capsys
    ) -> typing.Tuple[str, str, typing.Optional[str]]:
        with change_directory() as temp_dir:
            expected_log_file: pathlib.Path = (
                this_config.file_logging.log_file_path
            )
            under_test = LoggingState(this_config)

            log = logging.getLogger("MockLogging")
            log.debug("debug message")
            log.info("info message")
            log.warning("warning message")
            log.error("error message")
            log.critical("critical message")

            assert (
                under_test.configuration.enable_file_logging
                is this_config.enable_file_logging
            )
            assert (
                under_test.configuration.enable_console_logging
                is this_config.enable_console_logging
            )
            assert (
                under_test.configuration.log_level.upper()
                == this_config.log_level.upper()
            )

            if not this_config.enable_file_logging:
                assert not expected_log_file.exists()

                file_contents = None
            else:
                assert (
                    under_test.configuration.file_logging.log_file_path
                    == DEFAULT_LOG_FILE
                )
                assert expected_log_file.is_file()

                with expected_log_file.open("r") as f:
                    file_contents = f.read()
            (captured_out, captured_err) = this_capsys.readouterr()

        return captured_err, captured_out, file_contents

    def test_enable_console_logging(self, capsys, mock_config):
        attributes = {
            "enable_file_logging": False,
            "enable_console_logging": True,
            "log_level": "warning",
        }
        this_config = mock_config(attributes)

        captured_err, captured_out, _ = self._do_test(this_config, capsys)

        assert not captured_out
        assert "debug" not in captured_err
        assert "info" not in captured_err
        assert "warning message" in captured_err
        assert "error message" in captured_err
        assert "critical message" in captured_err

    def test_disable_file_logging(self, capsys, mock_config):
        attributes = {
            "enable_file_logging": False,
            "enable_console_logging": False,
            "file_logging": {"json_enabled": False},
            "log_level": "warning",
        }
        this_config = mock_config(attributes)

        captured_err, captured_out, file_contents = self._do_test(
            this_config, capsys
        )

        assert not file_contents

    def test_enable_file_logging(self, capsys, mock_config):
        attributes = {
            "enable_file_logging": True,
            "enable_console_logging": False,
            "file_logging": {"json_enabled": False},
            "log_level": "warning",
        }
        this_config = mock_config(attributes)

        captured_err, captured_out, file_contents = self._do_test(
            this_config, capsys
        )

        assert not captured_out

        assert "debug" not in file_contents
        assert "info" not in file_contents
        assert "warning message" in file_contents
        assert "error message" in file_contents
        assert "critical message" in file_contents

    def test_enable_both_file_console(self, capsys, mock_config):
        attributes = {
            "enable_file_logging": True,
            "enable_console_logging": True,
            "file_logging": {"json_enabled": False},
            "log_level": "warning",
        }
        this_config = mock_config(attributes)

        captured_err, captured_out, file_contents = self._do_test(
            this_config, capsys
        )

        assert "debug" not in captured_err
        assert "info" not in captured_err
        assert "warning message" in captured_err
        assert "error message" in captured_err
        assert "critical message" in captured_err

        assert "debug" not in file_contents
        assert "info" not in file_contents
        assert "warning message" in file_contents
        assert "error message" in file_contents
        assert "critical message" in file_contents

    def test_log_levels(self, capsys, mock_config):
        for this_level in VALID_LOG_LEVELS:
            attributes = {
                "enable_file_logging": True,
                "enable_console_logging": True,
                "log_level": this_level,
            }
            this_config = mock_config(attributes)

            captured_err, captured_out, _ = self._do_test(this_config, capsys)

            if captured_out:
                pytest.fail("Captured stdout should be empty")

            if this_level != "notset":
                expected_level = this_level.upper()
                if (expected_level not in captured_err) and (
                    "{0} message".format(expected_level.lower())
                    not in captured_err
                ):
                    pytest.fail(
                        "Log level {0} not present in captured stderr, "
                        "{1}".format(
                            expected_level,
                            captured_err if captured_err else "<empty>",
                        )
                    )
            else:
                # notset enables logging at all levels
                for log_level in VALID_LOG_LEVELS:
                    if log_level != "notset":
                        assert "{0} message".format(log_level) in captured_err
