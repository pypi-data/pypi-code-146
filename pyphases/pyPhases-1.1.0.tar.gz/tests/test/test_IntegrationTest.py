from pyPhases.test.TestCaseIntegration import TestCaseIntegration
from pyPhases.test.TestCase import TestCase


class TestIntegrationTest(TestCaseIntegration):
    beforeRunCheck = False
    afterRunCheck = False
    phase = TestCase.project.phases[0]

    def testExecution(self):
        self.assertEqual(self.phase.mainExecuted, 1)

    def testSingleExecution(self):
        self.assertEqual(self.phase.mainExecuted, 1)

    @staticmethod
    def beforeRun():
        TestIntegrationTest.beforeRunCheck = True
        assert TestIntegrationTest.phase.mainExecuted == 0

    @staticmethod
    def afterRun():
        TestIntegrationTest.afterRunCheck = True
        assert TestIntegrationTest.phase.mainExecuted == 1

    def testRunDecorators(self):
        self.assertTrue(TestIntegrationTest.afterRunCheck)
        self.assertTrue(TestIntegrationTest.beforeRunCheck)
