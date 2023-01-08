import logging
from ._els_logger import ELSHandler, ElasticSearchConf
from .contract import IIndexFormatter, ITimeFormatter
from ._time import TimeFormatter


class AdvancedLogHandler(logging.StreamHandler):

    def __init__(self, els_conf: ElasticSearchConf = None,
                 els_index_formatter: IIndexFormatter = None,
                 time_formatter: ITimeFormatter = None):
        super(AdvancedLogHandler, self).__init__()
        self.__elsHandler = ...
        self.__elsConf: ElasticSearchConf = els_conf
        self.__isElsActive = False

        self.__elsEvaluation(els_index_formatter, time_formatter)

    def __elsEvaluation(self, els_index_formatter: IIndexFormatter, time_formatter: ITimeFormatter):
        if not time_formatter:
            time_formatter = TimeFormatter()

        if self.__elsConf:
            self.__elsHandler = ELSHandler(self.__elsConf, time_formatter, els_index_formatter)
            if self.__elsConf.isActive:
                self.__elsHandler.start()
                self.__isElsActive = True

    def emit(self, record: logging.LogRecord) -> None:
        if self.__isElsActive:
            self.__elsHandler.emit(record)
        super().emit(record)
