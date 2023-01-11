import logging
from enum import Enum
from functools import wraps
from .singleton import Singleton

class Logger:
	__defaultFormat = '[%(asctime)s][%(name)s][%(levelname)s] %(message)s'
	
	def __init__(self, fileName, logLevel):
		self.__logger = logging.getLogger(fileName)
		self.__loglevel = self.__getLoggerLevel(logLevel)
		self.setFormat(self.__defaultFormat)

	@classmethod
	@Singleton
	def getSingleton(cls, fileName, logLevel):
		return cls(fileName, logLevel)

	def setFormat(self, format):
		formatter = logging.Formatter(format)
		stream_handler = logging.StreamHandler()
		stream_handler.setFormatter(formatter)
		self.__logger.addHandler(stream_handler)

	def __getLogger(self):
		return self.__logger

	def debug(self, msg, *args, **kwargs):
		self.__getLogger().debug(msg, *args, **kwargs)

	def info(self, msg, *args, **kwargs):
		self.__getLogger().info(msg, *args, **kwargs)

	def error(self, msg, *args, **kwargs):
		self.__getLogger().error(msg, *args, **kwargs)

	def warn(self, msg, *args, **kwargs):
		self.__getLogger().warn(msg, *args, **kwargs)

	def exception(self, msg, *args, **kwargs):
		self.__getLogger().exception(msg, *args, **kwargs)

	def critical(self, msg, *args, **kwargs):
		self.__getLogger().critical(msg, *args, **kwargs)

	def __getLoggerLevel(self, logLevel):
		if logLevel is not None:
			loggerLevelDict = {}
			loggerLevelDict[str(LogLevel.CRITICAL)] = logging.CRITICAL
			loggerLevelDict[str(LogLevel.ERROR)] = logging.ERROR
			loggerLevelDict[str(LogLevel.WARNING)] = logging.WARNING
			loggerLevelDict[str(LogLevel.INFO)] = logging.INFO
			loggerLevelDict[str(LogLevel.DEBUG)] = logging.DEBUG
			loggerLevelDict[str(LogLevel.NOTSET)] = logging.NOTSET
			loggingLevel = loggerLevelDict[str(logLevel)] if str(logLevel) in loggerLevelDict else logging.NOTSET
			return self.__logger.setLevel(loggingLevel)

		return self.__logger.setLevel(logging.NOTSET)


class LogLevel(Enum):
	CRITICAL = 0
	ERROR = 1
	WARNING = 2
	INFO = 3
	DEBUG = 4
	NOTSET = 5

def InstanceDebug(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		selfObj = args[0]
		result = func(*args, **kwargs)
		selfObj.getLogObj().debug("Input:{}, Output: {}".format(args, result))
		return result
	return wrapper

def Debug(logger):
	def debugWrapper(func):
		@wraps(func)
		def wrapper(*args, **kwargs):
			result = func(*args, **kwargs)
			logger.debug("Input:{}, Output: {}".format(args, result))
			return result
		return wrapper
	return debugWrapper
