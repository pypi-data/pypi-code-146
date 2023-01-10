import logging
import os
from logging import handlers
from pathlib import Path

from log_ocr.GbOcrTrack import GbOcrContext

hushed_once: bool = False

class AORunActivityLog:
    """
    Class to support activity and runtime logs
    """

    _prefix: str
    _home: str
    _run_descriptor: str
    _log_descriptor: str
    _runtime_logger: logging
    _activity_logger: logging
    _activity_db_logger: GbOcrContext
    logger_set: bool = False

    def __init__(self, prefix: str, level: int, home: str = '', run_descriptor: str = "runtime",
                 log_descriptor: str = 'content'):
        """
        Initializes logging structures. Sets logging to home/prefix-(run-descriptor|log_descriptor).log
        :param prefix: the activity being logged
        :param home: the directory to contain (or which contains) the log file
        :param run_descriptor: suffix of runtime file log (mirrors console)
        """
        # use fields here. Their setters call reset()
        self._prefix = prefix

        if not home:
            from gb_ocr.GRINConfig import GRINConfig
            grin_config: GRINConfig = GRINConfig()
            _ = grin_config.cfg_log_dir
            if not _ :
                raise ValueError("No valid value available for Log Home. check Config file log_home value ")

        self._home = home
        self._run_descriptor = run_descriptor
        self._log_descriptor = log_descriptor
        self._level = level

        # log_home never null. Parser has default
        if not os.access(str(home), os.W_OK):
            raise NotADirectoryError(home)

        self.reset()
        self.hush_lib()

    @classmethod
    def hush_lib(cls):
        """
        Quiet some components we don't care about
        :return:
        """
        global hushed_once
        if not hushed_once:
            for quiet_logger in ['boto', 'botocore', 'boto3', 'requests', 'urllib3', 'request', 's3transfer' ]:
                ql = logging.getLogger(quiet_logger)
                ql.setLevel(logging.CRITICAL)
                ql.propagate = True
            hushed_once = True

    def reset(self):
        """
        Resets file logging to allow for changed descriptors
        :return:
        """
        logging.basicConfig(level=self._level)

        # Each individual run is not important, so accumulate them in a log
        instance_id_log_path = f"{self.prefix}-{self.run_descriptor}.log"

        # log_date_fmt='%m-%d-%YT%H-%M-%S'
        log_date_fmt='[ %Z: %Y-%m-%d %X ]'
        # basic_formatter = logging.Formatter(fmt='%(asctime)s:%(levelname)s:%(name)s:%(message)s', datefmt='%m-%d %H:%M')
        # These values are found in https://docs.python.org/3/library/logging.html#logrecord-attributes
        thread_formatter = logging.Formatter(
            fmt='%(asctime)s:[%(threadName)s]:%(module)s.%(funcName)s:%(levelname)s:%(message)s',
            datefmt=log_date_fmt)
        # More time, fewer other details in activity

        # will this just get the root logger?
        self.runtime_logger = logging.getLogger('AORunlog')
        # runtime_logger = logging.getLogger(run_logger_name)
        # add a console handler to the runtime logger
        # Not needed - the console is where the root logger goes.
        # console = logging.StreamHandler()
        # console.setFormatter(basic_formatter)
        #    runtime_logger.addHandler(console)

        if not AORunActivityLog.logger_set:
            file_handler = handlers.RotatingFileHandler(Path(self.home, instance_id_log_path), maxBytes=4096000,
                                                        backupCount=100)

            # file_handler = logging.FileHandler(Path(log_root, f"{instance_id_log_path}"))
            file_handler.setFormatter(thread_formatter)
            self.runtime_logger.addHandler(file_handler)

        self.activity_logger = logging.getLogger('activity')


        if not AORunActivityLog.logger_set:
            # Dont rotate file
            activity_file_handler = logging.FileHandler(Path(self.home, f"{self.prefix}-{self.log_descriptor}.log"))
            activity_file_handler.setLevel(logging.INFO)
            activity_formatter = logging.Formatter(fmt='%(asctime)s:%(message)s', datefmt=log_date_fmt)
            activity_file_handler.setFormatter(activity_formatter)
            self.activity_logger.addHandler(activity_file_handler)
        AORunActivityLog.logger_set = True
        #
        # jimk archive-ops-752: add db handler
        # Not sure if this is such a good idea, to open a separate context - lets' see
        self.activity_db_logger = GbOcrContext()

    @property
    def prefix(self):
        return self._prefix

    @prefix.setter
    def prefix(self, value):
        self._prefix = value
        self.reset()

    @property
    def home(self):
        """
        Directory containing logging
        :return:
        """
        return self._home

    @home.setter
    def home(self, value):
        self._home = value
        self.reset()

    @property
    def run_descriptor(self):
        return self._run_descriptor

    @run_descriptor.setter
    def run_descriptor(self, value):
        self._run_descriptor = value
        self.reset()

    @property
    def log_descriptor(self):
        return self._log_descriptor

    @log_descriptor.setter
    def log_descriptor(self, value):
        self._log_descriptor = value
        self.reset()

    @property
    def runtime_logger(self):
        return self._runtime_logger

    @runtime_logger.setter
    def runtime_logger(self, value):
        self._runtime_logger = value

    @property
    def activity_logger(self):
        return self._activity_logger

    _activity_logger: logging

    @activity_logger.setter
    def activity_logger(self, value):
        self._activity_logger = value

    @property
    def activity_db_logger(self):
        return self._activity_db_logger


    @activity_db_logger.setter
    def activity_db_logger(self, value):
        self._activity_db_logger = value
