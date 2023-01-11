#!/usr/bin/env python

import random
import threading
import time
import unittest

from test.test_helper import ExecutionProbe, Poller
from plico.utils.decorator import synchronized, override
from plico.utils.fake_convergeable import FakeConvergeable
from plico.utils.concurrent_loop import ConcurrentLoopException, ConcurrentLoop


class FakeOperatorLog(object):

    def __init__(self):
        self._logCnt = 0
        self._mtx = threading.Lock()

    @synchronized("_mtx")
    @override
    def onLoopFailure(self, message):
        self._logCnt += 1

    @synchronized("_mtx")
    def getLoopFailureLogCount(self):
        return self._logCnt


class Test(unittest.TestCase):

    def setUp(self):
        self.interStepTimeSec = 0.001
        self.convergeable = FakeConvergeable()
        self.operatorLog = FakeOperatorLog()
        self.loop = None
        self.buildInitializedLoop()

    def buildUninitializedLoop(self):
        if self.loop is not None:
            self.loop.deinitialize()

        self.loop = ConcurrentLoop(
            "object under test",
            self.convergeable, self.interStepTimeSec,
            self.operatorLog.onLoopFailure)

    def buildInitializedLoop(self):
        self.buildUninitializedLoop()
        self.loop.initialize()

    def tearDown(self):
        self.loop.deinitialize()

    def test_creation(self):
        self.assertFalse(self.loop.isClosed())
        self.assertEqual(0, self.loop.getConvergenceStepCount())
        Poller(2).check(ExecutionProbe(
            lambda: self.assertTrue(
                self.convergeable.getMeasureConvergenceCount() > 1)))

    def test_awakes_from_long_running_sleeps(self):
        self.interStepTimeSec = 10
        cnt = self.convergeable.getMeasureConvergenceCount()
        self.buildInitializedLoop()
        t0Sec = time.time()
        Poller(2).check(ExecutionProbe(
            lambda: self.assertTrue(
                self.convergeable.getMeasureConvergenceCount() > cnt)))
        self.loop.deinitialize()
        t1Sec = time.time()
        self.assertTrue(t1Sec - t0Sec < self.interStepTimeSec / 10)

    def test_close_request_starts_truth_sensor(self):
        self.loop.close()
        self.waitForAtLeastConvergenceSteps(3)
        self.assertTrue(self.loop.isClosed())

    def waitForAtLeastConvergenceSteps(self,
                                       expectedSteps,
                                       timeoutSec=2):
        Poller(timeoutSec).check(ExecutionProbe(
            lambda: self.assertTrue(
                self.convergeable.getConvergenceStepCount() >= expectedSteps)))

    def test_loop_waits_between_steps(self):
        self.interStepTimeSec = 0.02
        self.buildInitializedLoop()
        self.assertEqual(0, self.convergeable.getConvergenceStepCount())
        t0Sec = time.time()
        self.loop.close()
        self.waitForAtLeastConvergenceSteps(2)
        t1Sec = time.time()
        diffSec = t1Sec - t0Sec
        self.assertTrue(t1Sec - t0Sec >= self.interStepTimeSec,
                        ("A loop step must take at least %.3f s but "
                         "it has taken only %.3f s") % (self.interStepTimeSec,
                                                        diffSec))

    def test_waits_between_sensor_failures(self):
        self.interStepTimeSec = 0.1
        self.buildUninitializedLoop()
        self.convergeable.requestPanic()
        self.loop.initialize()
        t0Sec = time.time()
        self.loop.close()
        self.waitForAtLeastConvergenceSteps(2)
        t1Sec = time.time()
        diffSec = t1Sec - t0Sec
        self.assertTrue(diffSec >= self.interStepTimeSec)

    def test_open_request_stops_loop_activity(self):
        self.loop.close()
        self.loop.open()
        cnt = self.convergeable.getConvergenceStepCount()
        self.assertEqual(cnt, self.convergeable.getConvergenceStepCount())
        self.assertEqual(self.loop.getConvergenceStepCount(),
                         self.convergeable.getConvergenceStepCount())
        self.assertFalse(self.loop.isClosed())

    def test_ignores_closing_of_loop_that_is_already_started(self):
        self.loop.close()
        self.loop.close()

    def closeLoopAndWaitForStep(self):
        self.loop.close()
        Poller(2).check(ExecutionProbe(
            lambda: self.assertTrue(
                self.convergeable.getConvergenceStepCount() > 0)))

    def test_complains_when_worker_fails_to_stop(self):
        self.loop.setStopDurationLimitSec(0.001)
        self.convergeable.blockStep()
        self.closeLoopAndWaitForStep()
        self.assertRaises(ConcurrentLoopException,
                          self.loop.deinitialize)
        self.convergeable.unblockStep()

    def test_ignores_open_request_on_open_loop(self):
        self.assertFalse(self.loop.isClosed())
        self.loop.open()

    def test_ignores_step_failures(self):
        self.convergeable.requestPanic()
        self.closeLoopAndWaitForStep()
        Poller(1).check(ExecutionProbe(
            lambda: self.assertTrue(
                self.operatorLog.getLoopFailureLogCount() >= 1)))
        self.loop.open()

    def test_performs_one_pass(self):
        self.loop.performOnePass()
        self.assertEqual(1, self.loop.getConvergenceStepCount())

    def test_convergence_during_close_loop(self):
        self.loop.close()
        self.convergeable.setAsConverged()
        self.assertTrue(self.loop.hasConverged())

        self.convergeable.setAsUnconverged()
        self.assertFalse(self.loop.hasConverged())

    def test_deinitialize_and_reinitialize_restarts_in_open_loop(self):
        self.closeLoopAndWaitForStep()
        self.loop.deinitialize()
        closedLoopCnt = \
            self.convergeable.getConvergenceStepCount()
        openLoopCnt = \
            self.convergeable.getMeasureConvergenceCount()

        self.loop.initialize()
        self.assertFalse(self.loop.isClosed())
        Poller(4).check(ExecutionProbe(
            lambda: self.assertEqual(
                closedLoopCnt,
                self.convergeable.getConvergenceStepCount())))

        Poller(4).check(ExecutionProbe(
            lambda: self.assertTrue(
                self.convergeable.getMeasureConvergenceCount() >
                openLoopCnt)))

        self.loop.close()

        Poller(4).check(ExecutionProbe(
            lambda: self.assertTrue(
                closedLoopCnt <
                self.convergeable.getConvergenceStepCount())))

    def test_concurrent_stress(self):
        N_THREADS = 500
        N_ACTIONS_PER_THREAD = 100
        self.convergeable.setStepSleepDurationSec(0.0005)

        class Stresser(threading.Thread):

            def __init__(self, loop, nIterations):
                threading.Thread.__init__(self)
                self._loop = loop
                self._nIterations = nIterations

            @override
            def run(self):
                for _ in range(0, self._nIterations):
                    try:
                        self._performLoopAction()
                    except Exception:
                        pass

            def _performLoopAction(self):
                N_ACTIONS = 5
                r = random.randint(0, N_ACTIONS - 1)
                if r == 0:
                    self._loop.close()
                elif r == 1:
                    self._loop.open()
                elif r == 2:
                    self._loop.setGain(7.0)
                elif r == 3:
                    self._loop.getGain()
                elif r == 4:
                    self._loop.isClosed()
                else:
                    raise ValueError("Programming mistake")

        stressers = []
        for _ in range(0, N_THREADS):
            stresser = Stresser(self.loop, N_ACTIONS_PER_THREAD)
            stressers.append(stresser)

        for each in stressers:
            each.start()

        for each in stressers:
            each.join(10)
            assert not each.is_alive()


if __name__ == "__main__":
    unittest.main()
