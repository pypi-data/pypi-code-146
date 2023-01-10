import psutil
import unittest
import logging

logger = logging.getLogger(__name__)


class WorkflowTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self._current_process = psutil.Process()
        self._subprocesses = {
            child.pid for child in self._current_process.children(recursive=True)
        }
        self._fail_on_subprocesses = True

    def tearDown(self) -> None:
        has_new_subprocesses = False
        for child in self._current_process.children(recursive=True):
            if child.pid not in self._subprocesses:
                has_new_subprocesses = True
                logger.error("dangling child %s", child)
                try:
                    child.terminate()
                except psutil.NoSuchProcess:
                    pass
        if has_new_subprocesses and self._fail_on_subprocesses:
            raise RuntimeError("not all subprocesses have finished")
