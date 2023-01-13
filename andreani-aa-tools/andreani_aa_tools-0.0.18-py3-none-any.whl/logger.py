
from datetime import datetime
from copy import deepcopy
import threading

class logger:

    def __init__(self, app_name, function_name):
        start_at = datetime.now()
        self._start_at = start_at
        self._app_name = app_name
        self._function_name = function_name

        self._log_console(f"Starting: {self._app_name}", "INFO", self._function_name)

    def start_function(self, function_name):
        start_at = datetime.now()
        function_logger = deepcopy(self)
        function_logger._function_name = function_name
        function_logger.start_at = start_at
        self._log_console(f"Starting function: {function_name}", "INFO", function_name)
        return function_logger

    def log_console(self, message, log_level):
        self._log_console(message, log_level, self._function_name)

    def close(self):
        self.log_console(f"Ending function: {self._function_name} - time in function: {(datetime.now() - self._start_at).total_seconds()} Seconds", "INFO")

    def _log_console(self, message, log_level, function_name):
        thread_id = threading.get_ident()
        log = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')} | {thread_id} | {log_level} | {self._app_name} | {function_name} | {message}"
        print(log)
