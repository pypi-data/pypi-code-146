# from pyPhases.exporter.ObjectExporter import ObjectExporter
# import pyPhases


from pyPhases.Project import ConfigNotFoundException
from tests.util.PhaseGenerator import PhaseGenerator
from pyPhases.test.TestCase import TestCase


class TestBaseTest(TestCase):
    phase = TestCase.project.phases[0]
    isPrepared = False

    def config(self):
        return {"option1": 1, "c1": "o"}

    def defaultConfig(self):
        return {**PhaseGenerator.completeConfig(), **self.config()}

    def testSetProject(self):
        self.assertIsNotNone(self.project)
        self.assertEqual("testProject", self.project.name)

    def testConfig(self):
        self.assertEqual(self.getConfig("p1"), 1)
        self.assertEqual(self.getConfig("p2"), 2)

        self.assertEqual(self.getConfig("option1"), 1)
        self.assertEqual(self.getConfig("c1"), "o")

        self.setConfig("oN", 5)
        self.assertEqual(self.getConfig("oN"), 5)

        with self.assertRaises(ConfigNotFoundException):
            self.getConfig("doesNotExist")

    def testData(self):
        self.project.registerData("dataphase1", 5)
        self.assertEqual(self.getData("dataphase1"), 5)
        self.assertDataEqual("dataphase1", 5)

    def testPrepare(self):
        self.assertEqual(self.getConfig("p1c1"), 1)
        self.assertEqual(self.getConfig("p1c2"), 2)

    def setUp(self) -> None:
        self.assertIsNone(self.restoreConfig)
        super().setUp()
        self.assertEqual(self.restoreConfig, PhaseGenerator.completeConfig())

    def tearDown(self) -> None:
        self.assertEqual(self.restoreConfig, PhaseGenerator.completeConfig())
        self.project.config["randomOverwrite"] = 5
        super().tearDown()
        self.assertEqual(self.project.config, PhaseGenerator.completeConfig())

    def beforePrepare(self):
        self.isPrepared = True

    def testBeforePrepare(self):
        self.assertTrue(self.isPrepared)
