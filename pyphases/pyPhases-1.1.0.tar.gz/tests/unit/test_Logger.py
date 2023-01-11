from unittest import TestCase
from pyPhases.util.EventBus import EventBus
from unittest.mock import MagicMock, patch
from pyPhases.util.Logger import classLogger, Logger, LogLevel


class TestLogger(TestCase):

    @patch('builtins.print')
    def test_Logger(self, mockPrint):
        Logger.verboseLevel = LogLevel.DEBUG
        Logger.log("test message", "test")
        mockPrint.assert_called_with("[test] test message", end="\n")

    @patch('builtins.print')
    def test_LoggerToHigh(self, mockPrint):
        Logger.verboseLevel = LogLevel.ERROR
        Logger.log("test message", "test")
        mockPrint.assert_not_called()

    @patch('builtins.print')
    def test_LoggerWarning(self, mockPrint):
        Logger.verboseLevel = LogLevel.DEBUG
        Logger.log("test message", "test", LogLevel.WARNING)
        mockPrint.assert_called_with("\033[33;1;4m%s\033[0m"%"[test] test message", end="\n")

    @patch('builtins.print')
    def test_LoggerError(self, mockPrint):
        Logger.verboseLevel = LogLevel.DEBUG
        Logger.log("test message", "test", LogLevel.ERROR)
        mockPrint.assert_called_with("\033[31;1;4m%s\033[0m"%"[test] test message", end="\n")

    @patch('builtins.print')
    def test_LoggerSuccess(self, mockPrint):
        Logger.verboseLevel = LogLevel.DEBUG
        Logger.log("test message", "test", LogLevel.SUCCESS)
        mockPrint.assert_called_with("\033[32;1;4m%s\033[0m"%"[test] test message", end="\n")

    @patch('pyPhases.util.Logger.Logger.log')
    def test_classLoggerLog(self, logMock):
        @classLogger
        class MyClass:
            pass
        myClass = MyClass()

        myClass.log("test message", LogLevel.SUCCESS)
        logMock.assert_called_with("test message", "MyClass", LogLevel.SUCCESS)

    @patch('pyPhases.util.Logger.Logger.log')
    def test_classLoggerDebug(self, logMock):
        @classLogger
        class MyClass:
            pass
        myClass = MyClass()

        myClass.logDebug("test message")
        logMock.assert_called_with("test message", "MyClass", level=LogLevel.DEBUG)

    @patch('pyPhases.util.Logger.Logger.log')
    def test_classLoggerSuccess(self, logMock):
        @classLogger
        class MyClass:
            pass
        myClass = MyClass()

        myClass.logSuccess("test message")
        logMock.assert_called_with("test message", "MyClass", level=LogLevel.SUCCESS)

    @patch('pyPhases.util.Logger.Logger.log')
    def test_classLoggerWarning(self, logMock):
        @classLogger
        class MyClass:
            pass
        myClass = MyClass()

        myClass.logWarning("test message")
        logMock.assert_called_with("test message", "MyClass", level=LogLevel.WARNING)

    @patch('pyPhases.util.Logger.Logger.log')
    def test_classLoggerError(self, logMock):
        @classLogger
        class MyClass:
            pass
        myClass = MyClass()

        myClass.logError("test message")
        logMock.assert_called_with("test message", "MyClass", level=LogLevel.ERROR)
