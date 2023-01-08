import abc
import yaml
import uuid
import requests
from time import sleep
from datetime import datetime
from cerberus import Validator
import autom8it.logger as b_logger
from importlib import import_module


class Log:

    _stopwatches = {}
    _warning_msgs_count = 0
    _error_msgs_count = 0
    _critical_msgs_count = 0

    @staticmethod
    def set_log_level(level: int):
        b_logger.set_log_level(level=level)

    @staticmethod
    def get_log_level() -> int:
        return b_logger.get_log_level()

    @staticmethod
    def get_log_level_name() -> str:
        return b_logger.get_log_level_name()

    @staticmethod
    def debug(msg: str):
        b_logger.log_msg(level=10, message=msg, current_run_level=3)

    @staticmethod
    def info(msg: str):
        b_logger.log_msg(level=20, message=msg, current_run_level=3)

    @staticmethod
    def warning(msg: str):
        Log._warning_msgs_count += 1
        b_logger.log_msg(level=30, message=msg, current_run_level=3)

    @staticmethod
    def error(msg: str):
        Log._error_msgs_count += 1
        b_logger.log_msg(level=40, message=msg, current_run_level=3)

    @staticmethod
    def critical(msg: str):
        Log._critical_msgs_count += 1
        b_logger.log_msg(level=50, message=msg, current_run_level=3)

    @staticmethod
    def exception(msg: str):
        b_logger.log_exception(message=msg)
        # Log._critical_msgs_count += 1
        # b_logger.log_msg(level=50, message=msg, current_run_level=3)

    @staticmethod
    def warning_count() -> int:
        return Log._warning_msgs_count

    @staticmethod
    def error_count() -> int:
        return Log._error_msgs_count

    @staticmethod
    def critical_count() -> int:
        return Log._critical_msgs_count

    @staticmethod
    def start_stopwatch(msg: str, print_it: bool = False) -> str:
        stopwatch_id = str(uuid.uuid4())
        Log._stopwatches[stopwatch_id] = [datetime.now(), msg]
        if print_it:
            b_logger.log_msg(
                level=10,
                message=f'Start stopwatch: {msg}\t id={stopwatch_id}',
                current_run_level=3
            )
        return stopwatch_id

    @staticmethod
    def stopwatch_seconds(stopwatch_id: str, print_it: bool = True) -> float:
        if stopwatch_id in Log._stopwatches:
            start_time, msg = Log._stopwatches[stopwatch_id]
            time_delta = datetime.now() - start_time
            seconds = time_delta.total_seconds()
            if print_it:
                b_logger.log_msg(
                    level=10,
                    message=f'{seconds} seconds from start, {Log._stopwatches[stopwatch_id][1]}.',
                    current_run_level=3
                )
            return seconds
        else:
            return -1

    @staticmethod
    def stop_stopwatch(stopwatch_id: str, print_it: bool = False) -> bool:
        if stopwatch_id in Log._stopwatches:
            start_time, msg = Log._stopwatches[stopwatch_id]
            if print_it:
                seconds = Log.stopwatch_seconds(stopwatch_id=stopwatch_id, print_it=False)
                b_logger.log_msg(
                    level=10,
                    message=f'{msg} took {seconds} seconds.',
                    current_run_level=3
                )
            try:
                del Log._stopwatches[stopwatch_id]
            except KeyError:
                pass
            return True
        else:
            return False


class AutomationTask:

    def __init__(self, task_data: dict, timeout: int = 900, check_done_interval: int = 5):
        validator = Validator(self.validation_schema)
        validator.allow_unknown = True
        if validator.validate(task_data):
            self._task_data = task_data
            self._check_done_interval = check_done_interval
            self._timeout = timeout
        else:
            for error in validator.errors:
                Log.error(error)
            raise ValueError(f'There are {len(validator.errors)} in task data.')

    @property
    @abc.abstractmethod
    def task_type(self) -> str:
        pass

    """
    https://docs.python-cerberus.org/en/stable/validation-rules.html#
    Validation schema example
        {
            'name': {
                'required': True, 
                'type': 'string'
            }, 
            'age': {
                'type': 'integer'
                'min': 18,
                'max': 120
            }
            'gender': {
                'type': 'string',
                'allowed': ['male', 'female', 'unknown']
        }
    """
    @property
    @abc.abstractmethod
    def validation_schema(self) -> dict:
        pass

    @abc.abstractmethod
    def do(self):
        pass

    @abc.abstractmethod
    def is_done(self) -> bool:
        pass

    def get_task_attribute(self, key: str, default=None):
        return self._task_data.get(key, default)

    def run(self):
        sw_id = Log.start_stopwatch(msg=self.task_type)
        Log.debug(f"Task returned: {self.do()}")
        while not self.is_done() and self._timeout > Log.stopwatch_seconds(stopwatch_id=sw_id, print_it=False):
            sleep(self._check_done_interval)


def run_yaml(file_path: str):
    with open(file_path, "r") as f:
        run_def = yaml.safe_load(f)
    run(run_def=run_def)


TASK_CLASS_KEY = 'class'
TASK_PARAMETERS_KEY = 'parameters'


def run(run_def: dict):
    main_sw_id = Log.start_stopwatch(msg='Run')
    for task_name, task_def in run_def.items():
        if TASK_CLASS_KEY in task_def:
            task = get_task_instance(class_name=task_def[TASK_CLASS_KEY], parameters=task_def[TASK_PARAMETERS_KEY])
            first_row = f'*   Task {task_name} ({task.task_type}) is starting *'
            Log.info(msg="*" * len(first_row))
            Log.info(msg=first_row)
            Log.info(msg="*" * len(first_row))
            Log.info(f'Task parameters: {task_def[TASK_PARAMETERS_KEY]}')
            task_sw_id = Log.start_stopwatch(msg=first_row)
            task.run()
            Log.info(
                f'*** Task {task.task_type} finished after '
                f'{Log.stopwatch_seconds(stopwatch_id=task_sw_id, print_it=False)} seconds ***'
            )
        else:
            raise SyntaxError(f'Missing {TASK_CLASS_KEY} definition.')
    Log.info(f'Process finished after {Log.stopwatch_seconds(stopwatch_id=main_sw_id, print_it=False)} seconds.')


def get_task_instance(class_name: str, parameters: dict) -> AutomationTask:
    task_cls = get_class_by_name(class_name=class_name, requested_type=AutomationTask)
    return task_cls(parameters)


def get_class_by_name(class_name: str, requested_type: object = None):

    try:
        module_path, c_name = class_name.rsplit('.', 1)
        module = import_module(module_path)
        result = getattr(module, c_name)
        if requested_type is not None and not issubclass(result, requested_type):
            raise ValueError(f'Class {result} does not match type {requested_type}.')
        return result
    except (ImportError, AttributeError):
        raise ImportError(class_name)


class HttpRequestTask(AutomationTask):

    HTTP_METHOD = 'method'
    URL = 'url'
    DATA = 'data'
    HEADERS = 'headers'
    PARAMETERS = 'parameters'

    def __init__(self, task_data: dict):
        super().__init__(task_data=task_data, check_done_interval=0)

    @property
    def validation_schema(self) -> dict:
        return {
            self.HTTP_METHOD: {
                'required': True,
                'type': 'string',
                'allowed': ['post', 'POST', 'get', 'GET']
            },
            self.URL: {
                'required': True,
                'type': 'string'
            },
            self.DATA: {
                'type': ['string', 'dict']
            },
            self.HEADERS: {
                'type': 'dict'
            },
            self.PARAMETERS: {
                'type': 'dict'
            }
        }

    @property
    def task_type(self) -> str:
        return 'Send HTTP reqeust'

    def do(self):
        resp = 'Error'
        url = self.get_task_attribute(key=self.URL)
        http_method = self.get_task_attribute(key=self.HTTP_METHOD, default='get').lower()
        headers = self.get_task_attribute(key=self.HEADERS, default={})
        parameters = self.get_task_attribute(key=self.PARAMETERS, default={})
        data = self.get_task_attribute(key=self.DATA, default='')

        if http_method == 'get':
            resp = requests.get(
                url,
                headers=headers,
                params=parameters
            )
        elif http_method == 'post':
            if isinstance(data, dict):
                resp = requests.post(
                    url,
                    json=data,
                    headers=headers,
                    params=parameters
                )
            else:
                resp = requests.post(
                    url,
                    data=data,
                    headers=headers,
                    params=parameters
                )

        Log.debug(f'Task got HTTP response: {resp}, {resp.text}')
        return resp

    def is_done(self) -> bool:
        return True
