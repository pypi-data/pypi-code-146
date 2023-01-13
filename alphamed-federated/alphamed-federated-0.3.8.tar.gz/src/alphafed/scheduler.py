"""Algorithm scheduler."""


from abc import ABC, abstractmethod
from functools import wraps
import inspect
import os
import sys
from typing import Dict, Iterable, Set, Tuple
from zipfile import ZipFile

import cloudpickle as pickle

from . import logger, task_logger
from .bass import BassProxy
from .contractor import TaskContractor
from .metrics_trace import MetricsTrace


class ConfigError(Exception):
    ...


class TaskFailed(Exception):
    ...


class TaskComplete(Exception):
    ...


class DataChecker(ABC):
    """To verify local data state."""

    def __init__(self, task_id: str) -> None:
        super().__init__()
        assert task_id and isinstance(task_id, str), 'Must specify task ID.'
        self.task_id = task_id

    @property
    def bass_proxy(self) -> BassProxy:
        if not hasattr(self, '_bass_proxy'):
            self._bass_proxy = BassProxy()
        return self._bass_proxy

    @abstractmethod
    def verify_data(self) -> Tuple[bool, str]:
        """Verify if local data is ready or not.

        Return:
            Tuple[verification result, explanation of the cause of the failure]
        """

    def execute_verification(self):
        """Run data verification logic and deal with the result."""
        is_succ, err_msg = self.verify_data()
        self.bass_proxy.notify_dataset_state(task_id=self.task_id,
                                             verified=is_succ,
                                             cause_of_failuer=err_msg)
        logger.info(f'Local dataset verification returns: {is_succ} : {err_msg}.')


class Scheduler(ABC):

    def __init__(self) -> None:
        super().__init__()
        self._metrics_bucket: Dict[str, MetricsTrace] = {}

    @property
    def bass_proxy(self) -> BassProxy:
        if not hasattr(self, '_bass_proxy'):
            self._bass_proxy = BassProxy()
        return self._bass_proxy

    def launch_task(self, task_id: str):
        """Launch current task.

        `Only for platform developers`:
        This method is running in `notebook` context, so it cannot access the common
        local directory shared by federated-service. Thus it have to upload files in a stream.
        """
        assert task_id and isinstance(task_id, str), f'invalid task ID: {task_id}'

        save_dir = os.path.join('/tmp', task_id)
        os.makedirs(save_dir, exist_ok=True)
        pickle_file = os.path.join(save_dir, 'model.pickle')
        with open(pickle_file, 'wb') as f:
            pickle.dump(self, f)

        dependencies: Set[str] = set()
        # sys.modules could change in the iteration.
        for _module in dict(sys.modules).values():
            try:
                _module_file = inspect.getabsfile(_module)
                if _module_file.startswith(save_dir):
                    dependencies.add(_module_file)
            except (TypeError, ModuleNotFoundError):
                pass

        zip_file = os.path.join(save_dir, 'src.zip')
        offset = len(save_dir)
        with ZipFile(zip_file, 'w') as src_zip:
            # include pickle of code in notebook cell
            src_zip.write(pickle_file, os.path.basename(pickle_file))
            # include dependent python files under same directory
            for _file in dependencies:
                src_zip.write(_file, _file[offset:])
            # include requirements.txt if exists
            requirements_file = os.path.join(save_dir, 'requirements.txt')
            if os.path.exists(requirements_file):
                src_zip.write(requirements_file, os.path.basename(requirements_file))

        with open(zip_file, 'rb') as src_zip:
            task_contractor = TaskContractor(task_id=task_id)
            file_key = task_contractor.upload_file(upload_name='src.zip',
                                                   fp=src_zip,
                                                   persistent=True)

        self.bass_proxy.launch_task(task_id=task_id, pickle_file_key=file_key)

    def push_log(self, message: str):
        """Push a running log message to the task manager."""
        assert message and isinstance(message, str), f'invalid log message: {message}'
        if hasattr(self, 'task_id') and self.task_id:
            task_logger.info(message, extra={"task_id": self.task_id})
        else:
            logger.warn('Failed to push a message because context is not initialized.')

    def get_metrics(self, name: str) -> MetricsTrace:
        return self._metrics_bucket.get(name)

    def _switch_status(self, _status: str):
        """Switch to a new status and leave a log."""
        self.status = _status
        logger.debug(f'{self.status=}')

    @abstractmethod
    def _run(self, id: str, task_id: str, is_initiator: bool = False, recover: bool = False):
        """Run the scheduler.

        This function is used by the context manager, DO NOT modify it, otherwize
        there would be strange errors raised.

        Args:
            id:
                the node id of the running context
            task_id:
                the id of the task to be scheduled
            is_initiator:
                is this scheduler the initiator of the task
            recover:
                whether to try recovering from last failed running
        """


def register_metrics(name: str, keys: Iterable[str]):
    """Register a metrics trace.

    NOTE: Deprecated.

    The trace fo the metrics during training will be included in the task's
    running result and can be downloaded. However, the trace content should
    be appended manually.

    If the specified name has already registered before, nothing changes.

    :args
        :name
            The name of the metrics trace.
        :keys
            The names of the metrics items.
    """
    def decorate(func):
        import warnings
        warnings.warn('`register_metrics` is deprecated and will be removed sooner',
                      category=DeprecationWarning)
        if not name or not isinstance(name, str):
            raise ValueError(f'invalid name of the metrics: {name}')
        if not keys or not isinstance(keys, Iterable):
            raise ValueError(f'invalid keys of the metrics: {keys}')

        @wraps(func)
        def wrapper(_self, *args, **kwargs):
            if not isinstance(_self, Scheduler) or func.__name__ != 'test':
                raise RuntimeError(
                    'Only applicable on "test" function of a "Scheduler" object.'
                )
            if name not in _self._metrics_bucket:
                _self._metrics_bucket[name] = MetricsTrace(headers=keys)
            return func(_self, *args, **kwargs)

        return wrapper
    return decorate
