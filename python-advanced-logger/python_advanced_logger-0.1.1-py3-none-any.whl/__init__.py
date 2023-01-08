from ._els_logger._index import IndexFormatter
from .contract import IIndexFormatter, ITimeFormatter
from ._handler import AdvancedLogHandler
from ._formatter import AdvancedLogFormatter
from ._formatter import FmtConf
from ._els_logger import ElasticSearchConf
from ._time import TimeFormatter


__title__ = "advancelogger"

__author__ = "Matin Karbasioun"

__publish__ = "2022"

__license__ = "MIT License"

__copyright__ = f"Copyright (c) {__publish__} " + __author__

from .contract import IIndexFormatter

ElsConfig: ElasticSearchConf = ...
DateFormatter = TimeFormatter()
