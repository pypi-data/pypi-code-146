import unittest
from typing import Iterable
from unittest.loader import TestLoader
from unittest.suite import TestSuite

from pyPhases.test.TestCase import TestCase


class TestRun(unittest.TestCase):
    phaseTests: Iterable[TestCase] = []

    def testAll(self):
        pass

    def afterRun(self):
        pass

    def countTestCases(self):
        return len(self.phaseTests)

    def run(self, result=None):
        testSuite = TestSuite()
        loader = TestLoader()

        for testCase in self.phaseTests:
            tests = loader.loadTestsFromTestCase(testCase)
            testSuite.addTests(tests)
        results = testSuite.run(result)
        self.afterRun()
        return results
