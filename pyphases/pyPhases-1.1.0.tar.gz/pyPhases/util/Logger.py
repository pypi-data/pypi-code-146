from enum import Enum


class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    SUCCESS = 4


class Logger:
    verboseLevel: LogLevel = LogLevel.INFO

    @staticmethod
    def log(msg, system=None, level=LogLevel.INFO, end="\n"):
        msg = str(msg)
        if system != None:
            msg = "[" + system + "] " + msg

        if level == LogLevel.WARNING:
            msg = "\033[33;1;4m%s\033[0m" % (msg)
        if level == LogLevel.ERROR:
            msg = "\033[31;1;4m%s\033[0m" % (msg)
        if level == LogLevel.SUCCESS:
            msg = "\033[32;1;4m%s\033[0m" % (msg)

        if Logger.verboseLevel.value <= level.value:
            print(msg, end=end)


def classLogger(class_):
    def log(self, msg, level=LogLevel.INFO):
        system = type(self).__name__
        Logger.log(msg, system, level)

    def logDebug(self, msg):
        system = type(self).__name__
        Logger.log(msg, system, level=LogLevel.DEBUG)

    def logSuccess(self, msg):
        system = type(self).__name__
        Logger.log(msg, system, level=LogLevel.SUCCESS)

    def logWarning(self, msg):
        system = type(self).__name__
        Logger.log(msg, system, level=LogLevel.WARNING)

    def logError(self, msg):
        system = type(self).__name__
        Logger.log(msg, system, level=LogLevel.ERROR)

    class_.log = log
    class_.logDebug = logDebug
    class_.logWarning = logWarning
    class_.logError = logError
    class_.logSuccess = logSuccess
    return class_
