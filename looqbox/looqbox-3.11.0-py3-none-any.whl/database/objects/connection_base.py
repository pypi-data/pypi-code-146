from abc import ABC, abstractmethod
from looqbox.database.database_exceptions import TimeOutException, alarm_handler
from looqbox.global_calling import GlobalCalling
from multimethod import multimethod
from platform import system
import pandas as pd
import datetime
import signal
import os


class BaseConnection(ABC):

    def __init__(self):
        self.timeout_settings = {"set": {"Windows": self._set_timeout_for_windows,
                                         "Linux": self._set_timeout_for_unix},
                                 "reset": {"Windows": self._reset_timeout_for_windows,
                                           "Linux": self._reset_timeout_for_unix}}
        self.test_mode = GlobalCalling.looq.test_mode
        self.connection_alias = ""
        self.query = ""
        self.retrieved_data = pd.DataFrame()
        self.query_metadata = dict()

    @staticmethod
    def _set_timeout_for_windows(response_timeout: int) -> None:
        # Since Windows OS doesn't support signal usage and is use only in a local development scenario
        # no timeout will be set for this OS.
        pass

    @staticmethod
    def _reset_timeout_for_windows() -> None:
        # Since Windows OS doesn't support signal usage and is use only in a local development scenario
        # no timeout will be set for this OS.
        pass

    @staticmethod
    def _set_timeout_for_unix(response_timeout: int) -> None:
        signal.signal(signal.SIGALRM, alarm_handler)
        signal.alarm(response_timeout)

    @staticmethod
    def _reset_timeout_for_unix() -> None:
        signal.alarm(0)

    def _get_timeout_methods(self):
        set_timeout = self.timeout_settings.get("set").get(system(), self._set_timeout_for_unix)
        reset_timeout = self.timeout_settings.get("reset").get(system(), self._set_timeout_for_unix)
        return set_timeout, reset_timeout

    @abstractmethod
    def set_query_script(self, sql_script):
        pass

    @abstractmethod
    def connect(self):
        pass

    def _get_response_timeout(self) -> int:
        timeout = int(GlobalCalling.looq.response_timeout) if not self.test_mode else 0
        return timeout

    def _update_response_timeout(self, consumed_time: datetime.timedelta) -> None:
        GlobalCalling.looq.response_timeout -= int(round(consumed_time.total_seconds(), 0))

    @multimethod
    def execute(self, cache_time: None) -> None:
        set_timeout, reset_timeout = self._get_timeout_methods()

        response_timeout = self._get_response_timeout()
        set_timeout(response_timeout)

        start_time = datetime.datetime.now()

        try:
            self._call_query_executor(start_time)
            reset_timeout()

        except TimeOutException as ex:
            self.close_connection()
            reset_timeout()

            total_sql_time = datetime.datetime.now() - start_time
            GlobalCalling.log_query({"connection": self.connection_alias, "query": self.query,
                                     "time": str(total_sql_time), "success": False})
            raise ex

    @multimethod
    def execute(self, cache_time: int) -> None:
        set_timeout, reset_timeout = self._get_timeout_methods()

        response_timeout = self._get_response_timeout()
        set_timeout(response_timeout)
        start_time = datetime.datetime.now()
        try:
            self.use_query_cache(cache_time, start_time)
        except TimeOutException as ex:
            self.close_connection()
            reset_timeout()

            total_sql_time = datetime.datetime.now() - start_time
            GlobalCalling.log_query({"connection": self.connection_alias, "query": self.query,
                                     "time": str(total_sql_time), "success": False})
            raise ex
        except Exception as folder_exception:
            self.close_connection()
            signal.alarm(0)
            raise folder_exception

    @abstractmethod
    def _call_query_executor(self, query_timer, query_mode="single"):
        """
        Method that call _get_query_result implementing the try-except statement using the connection type
        specific error handlers
        """
        pass

    @abstractmethod
    def _get_query_result(self):
        """
        Method to execute the query properly without any try-except statements
        this model allow the execution of several queries in parallel
        """
        pass

    @abstractmethod
    def close_connection(self):
        pass

    @abstractmethod
    def _generate_cache_file_name(self):
        pass

    def use_query_cache(self, cache_time, start_time, query_mode="single"):
        # since cache is saved in rds format, it's necessary
        # to load the equivalent R functions

        # data frame name used in rds file, since R and Python shared the same files,
        # no name has to be attached to the data
        DF_NAME = None
        cache_name = self._generate_cache_file_name()

        if self.test_mode:
            self.check_if_temp_folder_exists()
        cache_file = GlobalCalling.looq.temp_file(cache_name, add_hash=False)

        if self._is_cache_still_valid(cache_file, cache_time):
            self._get_cached_data(DF_NAME, cache_file, start_time, query_mode)
        else:
            self._create_new_cache_file(cache_file, start_time, query_mode)

    def _create_new_cache_file(self, cache_file: str, start_time, query_mode) -> None:
        from pyreadr import write_rds

        self._call_query_executor(start_time, query_mode)

        if self.retrieved_data.empty:
            return None

        if self.test_mode:
            print("creating cache\npath:", cache_file)

        try:
            write_rds(cache_file, self.retrieved_data)
        except Exception as error:
            raise error

    def _get_cached_data(self, DF_NAME: None, cache_file: str, start_time, query_mode="single") -> None:
        from pyreadr import read_r

        if self.test_mode:
            print("using cache\npath:", cache_file)
        try:
            cached_data = read_r(cache_file)[DF_NAME]
            self.retrieved_data = pd.DataFrame(cached_data, columns=cached_data.keys())
            self.query_metadata = {}  # temporally disable metadata for cache
            total_sql_time = datetime.datetime.now() - start_time
            GlobalCalling.log_query({"connection": "Cache File", "query": self.query,
                                     "time": str(total_sql_time), "success": True, "mode": query_mode})

        except FileNotFoundError as file_exception:
            raise file_exception

    def _get_connection_file(self) -> dict:
        import json
        try:
            if isinstance(GlobalCalling.looq.connection_config, dict):
                file_connections = GlobalCalling.looq.connection_config
            else:
                file_connections = open(GlobalCalling.looq.connection_config)
                file_connections = json.load(file_connections)
        except FileNotFoundError:
            raise Exception("File connections.json not found")
        return file_connections

    def _is_cache_still_valid(self, cache_file, cache_time) -> bool:
        import time
        return os.path.isfile(cache_file) and (time.time() - os.stat(cache_file).st_mtime) < cache_time

    def check_if_temp_folder_exists(self) -> None:
        temp_path = GlobalCalling.looq.temp_dir
        if not os.path.isdir(temp_path):
            os.mkdir(temp_path)
