# from pyPhases.exporter.ObjectExporter import ObjectExporter
# import pyPhases


import unittest
from unittest.runner import TextTestRunner
from pyPhases.test.TestRun import TestRun
from pyPhases.test.TestCaseIntegration import TestCaseIntegration

from pyPhases.test.TestCase import TestCase


class PhaseTestSample(TestCaseIntegration):
    phase = TestCase.project.phases[0]

    def testExecuted(self):
        pass

    def testSingleExecution(self):
        pass


class ATestRun(TestRun):
    phaseTests = [PhaseTestSample, PhaseTestSample, PhaseTestSample]


class TestTestRun(unittest.TestCase):
    def testRun(self):
        suite = ATestRun()

        runner = TextTestRunner()
        result = runner.run(suite)

        self.assertEqual(len(result.errors), 0)
        self.assertEqual(len(result.failures), 0)
