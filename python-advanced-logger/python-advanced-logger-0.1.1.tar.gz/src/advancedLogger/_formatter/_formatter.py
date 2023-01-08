import logging
import json
# from advancelogger._elasticsearch_logger import ElasticSearchConf, ElasticSearchLogger, IndexFormatter
# from ._fmt_conf import FmtConf


class AdvancedLogFormatter(logging.Formatter):
    """
        Use Advance Log Formatter to emphasize on how and which contents your want in your log

        Based on built-in logging library in python, Formatters responsible for converting
        a LogRecord to a string which be human-readable and can show important information
        on the log record

        Advance log formatter needs to know about which information and how order them for
        log record. This can define by the initial string call fmt (short stand for format) at
        initialize the logger in the python code.

         %(name)s            Name of the logger (logging channel)
        %(levelno)s         Numeric logging level for the message (DEBUG, INFO,
                            WARNING, ERROR, CRITICAL)
        %(levelname)s       Text logging level for the message ("DEBUG", "INFO",
                            "WARNING", "ERROR", "CRITICAL")
        %(pathname)s        Full pathname of the source file where the logging
                            call was issued (if available)
        %(filename)s        Filename portion of pathname
        %(module)s          Module (name portion of filename)
        %(lineno)d          Source line number where the logging call was issued
                            (if available)
        %(funcName)s        Function name
        %(created)f         Time when the LogRecord was created (time.time()
                            return value)
        %(asctime)s         Textual time when the LogRecord was created
        %(msecs)d           Millisecond portion of the creation time
        %(relativeCreated)d Time in milliseconds when the LogRecord was created,
                            relative to the time the logging module was loaded
                            (typically at application startup time)
        %(thread)d          Thread ID (if available)
        %(threadName)s      Thread name (if available)
        %(process)d         Process ID (if available)
        %(message)s         The result of record.getMessage(), computed just as
                            the record is emitted

    """

    def __init__(self, log_fmt: str | None = None, date_fmt: str | None = None, index_splitter: str | None = '%'):
        super().__init__(fmt=log_fmt, datefmt=date_fmt, style=index_splitter)
        self.__isJsonActive = False

    def useJson(self):
        self.__isJsonActive = True

    def formatMessage(self, record) -> dict:
        """
        Overwritten to return a dictionary of the relevant LogRecord attributes instead of a string.
        KeyError is raised if an unknown attribute is provided in the fmt_dict.
        """

        return record.__dict__

    def format(self, record) -> str:
        """
        Mostly the same as the parent's class method, the difference being that a dict is manipulated and dumped as JSON
        instead of a string.
        """
        record.message = record.getMessage()

        if self.usesTime():
            record.asctime = self.formatTime(record, self.datefmt)

        message_dict = self.formatMessage(record)

        if record.exc_info:
            # Cache the traceback text to avoid converting it multiple times
            # (it's constant anyway)
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)

        if record.exc_text:
            message_dict["exc_info"] = record.exc_text

        if record.stack_info:
            message_dict["stack_info"] = self.formatStack(record.stack_info)

        if self.__isJsonActive:
            return json.dumps(message_dict, default=str)

        else:
            return record.message
