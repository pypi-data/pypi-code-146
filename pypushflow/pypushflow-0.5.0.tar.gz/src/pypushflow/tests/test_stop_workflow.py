import os
import sys
import signal
from time import sleep
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ProcessPoolExecutor

import pytest
from pypushflow.Workflow import Workflow
from pypushflow.StopActor import StopActor
from pypushflow.StartActor import StartActor
from pypushflow.PythonActor import PythonActor
from pypushflow.ThreadCounter import ThreadCounter
from pypushflow.ErrorHandler import ErrorHandler
from pypushflow.stop_workflows import DEFAULT_STOP_SIGNALS


@pytest.mark.parametrize("forced_interruption", [True, False])
@pytest.mark.parametrize("sleep_time", [0, 2])
def test_stop_workflow(forced_interruption, sleep_time, workflow_cleanup):
    if os.name == "nt" and forced_interruption:
        pytest.skip("not supported on windows")
    testWorkflow1 = WorkflowSleep("Test workflow Sleep")

    def run_normal():
        inData = {"sleep_time": 0, "counter": 0}
        future = executor.submit(
            testWorkflow1.run,
            inData,
            timeout=15,
            scaling_workers=False,
            max_workers=-1,
        )
        result = future.result()
        assert "WorkflowException" not in result
        assert result["counter"] == 3

    def run_stopped():
        inData = {"sleep_time": 2, "counter": 0}
        future = executor.submit(
            testWorkflow1.run,
            inData,
            timeout=15,
            scaling_workers=False,
            max_workers=-1,
        )
        if sleep_time:
            sleep(sleep_time)
        testWorkflow1.stop(
            reason="reason for stopping", forced_interruption=forced_interruption
        )
        result = future.result()
        assert result["counter"] < 3
        assert "WorkflowException" in result

    with ThreadPoolExecutor() as executor:
        run_normal()
        run_stopped()
        run_stopped()
        run_normal()


@pytest.mark.parametrize("forced_interruption", [True, False])
@pytest.mark.parametrize("sleep_time", [2])
def test_stop_signal_workflow(
    forced_interruption, sleep_time, skip_when_gevent, skip_on_windows
):
    def run_normal():
        inData = {"sleep_time": 0, "counter": 0}
        future = executor.submit(
            _run_workflow,
            inData,
            timeout=15,
            scaling_workers=False,
            max_workers=-1,
            forced_interruption=forced_interruption,
        )
        result = future.result()
        assert "WorkflowException" not in result
        assert result["counter"] == 3

    def run_stopped():
        inData = {"sleep_time": 2, "counter": 0}
        future = executor.submit(
            _run_workflow,
            inData,
            timeout=15,
            scaling_workers=False,
            max_workers=-1,
            forced_interruption=forced_interruption,
        )
        if sleep_time:
            sleep(sleep_time)
        for pid in list(executor._processes):
            # TODO: doesn't work on windows (it kills the subprocess)
            os.kill(pid, DEFAULT_STOP_SIGNALS[0])

        result = future.result()
        assert result["counter"] < 3
        assert "WorkflowException" in result

    if sys.version_info < (3, 7):
        pool = ProcessPoolExecutor(max_workers=1)
        pool.submit(_process_initializer).result()
    else:
        pool = ProcessPoolExecutor(initializer=_process_initializer)

    with pool as executor:
        run_normal()
        run_stopped()
        run_stopped()
        run_normal()


def _process_initializer():
    try:
        signal.signal(DEFAULT_STOP_SIGNALS[0], signal.SIG_IGN)
    except (OSError, AttributeError, ValueError, RuntimeError):
        pass


def _run_workflow(*args, forced_interruption: bool = False, **kwargs):
    testWorkflow1 = WorkflowSleep(
        "Test workflow Sleep",
        stop_on_signals=True,
        forced_interruption=forced_interruption,
    )
    return testWorkflow1.run(*args, **kwargs)


class WorkflowSleep(Workflow):
    def __init__(self, name, **kw):
        super().__init__(name, **kw)
        ctr = ThreadCounter(parent=self)
        self.startActor = StartActor(parent=self, thread_counter=ctr)
        self.errorActor = ErrorHandler(parent=self, thread_counter=ctr)
        self.pythonActor1 = PythonActor(
            parent=self,
            script="pypushflow.tests.tasks.pythonActorInterrupt.py",
            name="Python Actor Sleep",
            thread_counter=ctr,
        )
        self.pythonActor2 = PythonActor(
            parent=self,
            script="pypushflow.tests.tasks.pythonActorInterrupt.py",
            name="Python Actor Sleep",
            thread_counter=ctr,
        )
        self.pythonActor3 = PythonActor(
            parent=self,
            script="pypushflow.tests.tasks.pythonActorInterrupt.py",
            name="Python Actor Sleep",
            thread_counter=ctr,
        )
        self.stopActor = StopActor(parent=self, thread_counter=ctr)
        self.startActor.connect(self.pythonActor1)
        self.pythonActor1.connect(self.pythonActor2)
        self.pythonActor2.connect(self.pythonActor3)
        self.pythonActor3.connect(self.stopActor)
        self.errorActor.connect(self.stopActor)
        self.pythonActor1.connectOnError(self.errorActor)
        self.pythonActor2.connectOnError(self.errorActor)
        self.pythonActor3.connectOnError(self.errorActor)
