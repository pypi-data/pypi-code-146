from pyPhases import LogLevel
from unittest.mock import patch

class LoggerMock():

    def __init__(self, mock) -> None:
        self.mock = mock

    def expectLogMessage(self, msg, system=None, level=LogLevel.INFO):
        self.assertLogMessageLike(msg, system, level, exact=True)


    def assertLogMessageLike(self, contains, expectedSystem=None, expectedLevel=None, exact=False):
        """Assert that a log message contains the given message."""
        self.mock.assert_called()
        args = list(self.mock.call_args[0]) + list(self.mock.call_args[1].values())
        if len(args) == 1:
            message = args
            system = None
            level = LogLevel.INFO
        elif len(args) == 2:
            message, system = args
            level = LogLevel.INFO
        else:
            message, system, level = args

        if expectedLevel is not None:
            assert level == expectedLevel, "The Log message is of a diffrent type: %s"%level
        if expectedSystem is not None:
            assert system == expectedSystem, "The Log message if from a diffrent system: %s"%system

        if exact:
            assert message == contains, "The last log message does not match '%s': %s"%(contains, message)
        else:
            assert contains in message, "The last log message does not contain '%s': %s"%(contains, message)

    def assertWarningLike(self, contains, expectedSystem=None):
        self.assertLogMessageLike(contains, expectedSystem=expectedSystem, expectedLevel=LogLevel.WARNING)

    def assertErrorLike(self, contains, expectedSystem=None):
        self.assertLogMessageLike(contains, expectedSystem=expectedSystem, expectedLevel=LogLevel.ERROR)

    def assertSuccessLike(self, contains, expectedSystem=None):
        self.assertLogMessageLike(contains, expectedSystem=expectedSystem, expectedLevel=LogLevel.SUCCESS)



def mockLogger(func):

    def inner1(*args, **kwargs):

        patcher = patch('pyPhases.Logger.log')
        mock_read = patcher.start()

        args = list(args)
        selfArg = args.pop(0)

        # args = [selfArg] + [LoggerMock(mock_read)] + args
        args = [selfArg] + [LoggerMock(mock_read)] + args
        r = func(*args)
        patcher.stop()

        return r

    return inner1
