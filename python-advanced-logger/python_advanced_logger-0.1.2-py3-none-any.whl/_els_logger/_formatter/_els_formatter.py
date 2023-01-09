import copy
import logging
import uuid

from advancedLogger.contract import ITimeFormatter


class ElasticSearchFormatter:
    def __init__(self, time_formatter: ITimeFormatter):
        self.__time_formatter: ITimeFormatter = time_formatter

    def format(self, logRecord: logging.LogRecord) -> dict:
        logDict = copy.deepcopy(logRecord.__dict__)
        logDict.pop("args")
        logDict.update({"@timestamp": self.__time_formatter.convert(logRecord.created)})
        logDict.update({"traceId": str(uuid.uuid4())})
        return logDict
