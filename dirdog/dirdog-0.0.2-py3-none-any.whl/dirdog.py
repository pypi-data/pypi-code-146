import os
import time
from threading import Thread
from typing import Callable, Any
import logging

_logger = logging.getLogger(__name__)


class DirDog:

    def __init__(self, path, seconds_between_checks=1) -> None:
        self._path = path
        self._file_list = os.listdir(self._path)
        self._new_file_callbacks = []
        self._deleted_file_callbacks = []
        self._changed_file_callbacks = []
        self._seconds_between_checks = seconds_between_checks
        self._last_check = time.time()
        self._stopped = False
        self._thread = Thread(target=self._run, daemon=True)
        self._thread.start()
        _logger.debug("Setup complete, monitoring %s",
                      os.path.abspath(path))

    def __del__(self):
        self._stopped = True

    def join(self):
        return self._thread.join()

    def on_new_file(self, callback: Callable[[str], Any]) -> None:
        self._new_file_callbacks.append(callback)

    def on_deleted_file(self, callback: Callable[[str], Any]) -> None:
        self._deleted_file_callbacks.append(callback)

    def on_changed_file(self, callback: Callable[[str], Any]) -> None:
        self._changed_file_callbacks.append(callback)

    def _notify_new_files(self, new_files: list[str]):
        for file in new_files:
            for callback in self._new_file_callbacks:
                callback(file)

    def _notify_deleted_files(self, deleted_files: list[str]):
        for file in deleted_files:
            for callback in self._deleted_file_callbacks:
                callback(file)

    def _notify_changed_file(self, file: str):
        for callback in self._changed_file_callbacks:
            callback(file)

    def _run(self):
        while not self._stopped:
            self._check_folder()
            time.sleep(self._seconds_between_checks)

    def _check_folder(self):
        _logger.debug("checking %s", self._path)
        current_file_list = os.listdir(self._path)
        _logger.debug("Content: %s", current_file_list)
        if self._new_file_callbacks:
            new_files = [
                file for file in current_file_list if file not in self._file_list]
            if new_files:
                _logger.debug("Detected new files: %s", new_files)
                self._notify_new_files(new_files)
        if self._deleted_file_callbacks:
            deleted_files = [
                file for file in self._file_list if file not in current_file_list]
            if deleted_files:
                _logger.debug("Detected deleted files: %s", deleted_files)
                self._notify_deleted_files(deleted_files)
        self._file_list = current_file_list
        if self._changed_file_callbacks:
            current_time = time.time()
            for file in current_file_list:
                mod_time = os.path.getmtime(os.path.join(self._path,file))
                _logger.debug("%s: %s vs %s", file, mod_time, current_time)
                if current_time - mod_time < self._seconds_between_checks:
                    _logger.debug("File %s has changed!", file)
                    self._notify_changed_file(file)
