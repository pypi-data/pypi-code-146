import copy
import logging
from queue import Queue

from ._conf import ElasticSearchConf
from ._formatter import ElasticSearchFormatter
from ._els_logger import ElasticSearchLogger
from ._index import IndexFormatter
from advancedLogger.contract import ITimeFormatter, IIndexFormatter


class ELSHandler:

    def __init__(self, els_conf: ElasticSearchConf,
                 time_formatter: ITimeFormatter,
                 els_index_formatter: IIndexFormatter = None):

        super().__init__()
        self.__elsConf = els_conf
        self.__elsQueue: Queue = ...
        self.__elsLogger: ElasticSearchLogger = ...
        self.__indexFormatter: IIndexFormatter = els_index_formatter
        self.__timeFormatter: ITimeFormatter = time_formatter
        self.__elsFormatter: ElasticSearchFormatter = ElasticSearchFormatter(time_formatter)
        self.__setupElastic(els_conf)

    def __setupElastic(self, els_conf: ElasticSearchConf):
        self.__elsQueue = Queue()
        self.__setupIndexFormatter()
        self.__elsLogger = ElasticSearchLogger(index_formatter=self.__indexFormatter,
                                               config=els_conf,
                                               queue=self.__elsQueue)

    def start(self):
        self.__elsLogger.start()

    def __setupIndexFormatter(self):
        if not self.__indexFormatter:
            self.__indexFormatter = IndexFormatter(self.__elsConf.indicator, self.__timeFormatter)

    def emit(self, record: logging.LogRecord):
        match record.levelname:
            case "CRITICAL":
                if self.__elsConf.isCriticalActive:
                    self.__emit(record)

            case "ERROR":
                if self.__elsConf.isErrorActive:
                    self.__emit(record)

            case "INFO":
                if self.__elsConf.isInfoActive:
                    self.__emit(record)

            case "DEBUG":
                if self.__elsConf.isDebugActive:
                    self.__emit(record)

            case "WARNING":
                if self.__elsConf.isWarningActive:
                    self.__emit(record)

            case "FATAL":
                if self.__elsConf.isCriticalActive:
                    self.__emit(record)

    def __emit(self, record: logging.LogRecord):
        elsLogRecord = self.__elsFormatter.format(record)
        self.__elsQueue.put(elsLogRecord)


