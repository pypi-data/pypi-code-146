from pyPhases.test.TestCase import TestCase


class TestCaseIntegration(TestCase):
    def setUp(self):
        super().setUp()

    @classmethod
    def setUpClass(c):
        o = c()
        o.prepare()
        o.beforeRun()
        c.phase.run()
        o.afterRun()

    @staticmethod
    def beforeRun():
        pass

    @staticmethod
    def afterRun():
        pass
