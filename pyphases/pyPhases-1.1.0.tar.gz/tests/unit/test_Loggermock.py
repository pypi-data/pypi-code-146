import unittest
from unittest.mock import MagicMock, patch

from pyPhases import LogLevel
from pyPhases.test.MockLogger import LoggerMock, mockLogger
from pyPhases.util.Logger import classLogger


@classLogger
class TestLoggerMock(unittest.TestCase):

    @mockLogger
    def test_log_info(self, mock):
        self.log("test message")
        mock.expectLogMessage("test message", "TestLoggerMock", LogLevel.INFO)
        self.assertRaises(AssertionError, mock.expectLogMessage, "message", "TestLoggerMock", LogLevel.INFO)

    @mockLogger
    def test_log_warning(self, mock):
        self.logWarning("test message")
        mock.expectLogMessage("test message", "TestLoggerMock", LogLevel.WARNING)

    @mockLogger
    def test_log_error(self, mock):
        self.logError("test message")
        mock.expectLogMessage("test message", "TestLoggerMock", LogLevel.ERROR)

    @mockLogger
    def test_log_success(self, mock):
        self.logSuccess("test message")
        mock.expectLogMessage("test message", "TestLoggerMock", LogLevel.SUCCESS)

    @mockLogger
    def test_assertLogMessageLike_info(self, mock):
        self.log("test message")
        mock.assertLogMessageLike("message", "TestLoggerMock")
        mock.assertLogMessageLike("test message", "TestLoggerMock")

    @mockLogger
    def test_assertLogMessageLike_warning(self, mock):
        self.logWarning("test message")
        mock.assertLogMessageLike("message", "TestLoggerMock")
        mock.assertWarningLike("message", "TestLoggerMock")
        self.assertRaises(AssertionError, mock.assertErrorLike, "message", "TestLoggerMock")
        self.assertRaises(AssertionError, mock.assertSuccessLike, "message", "TestLoggerMock")

    @mockLogger
    def test_assertLogMessageLike_error(self, mock):
        self.logError("test message")
        mock.assertLogMessageLike("message", "TestLoggerMock")
        mock.assertErrorLike("test message", "TestLoggerMock")
        self.assertRaises(AssertionError, mock.assertSuccessLike, "message", "TestLoggerMock")
        self.assertRaises(AssertionError, mock.assertWarningLike, "message", "TestLoggerMock")

    @mockLogger
    def test_assertLogMessageLike_success(self, mock):
        self.logSuccess("test message")
        mock.assertLogMessageLike("message", "TestLoggerMock")
        mock.assertSuccessLike("test message", "TestLoggerMock")
        self.assertRaises(AssertionError, mock.assertErrorLike, "message", "TestLoggerMock")
        self.assertRaises(AssertionError, mock.assertWarningLike, "message", "TestLoggerMock")

    @patch("pyPhases.Project")
    @mockLogger
    def test_decoratorOrderingBottomUp(self, mock, magicmock):
        self.assertIsInstance(magicmock, MagicMock)
        self.assertIsInstance(mock, LoggerMock)

    @patch("pyPhases.Project")
    @patch("pyPhases.Project")
    @mockLogger
    def test_decoratorOrderingBottomUp2(self, mock, magicmock, magicmock2):
        self.assertIsInstance(magicmock, MagicMock)
        self.assertIsInstance(magicmock2, MagicMock)
        self.assertIsInstance(mock, LoggerMock)
