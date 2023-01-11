from unittest import TestCase
from pyPhases.Phase import Phase
from pyPhases.Project import Project
from unittest.mock import MagicMock
from pyPhases.Data import Data

class TestPhase(TestCase):

    def getDefaultPhase(self):
        return self.getDefaultPhaseAndProject()[0]

    def getDefaultPhaseAndProject(self):
        testProject = Project()
        testProject.config = {"a": "foo", "b": "bar", "Phase": {"phaseConfig": "value"}}
        testPhase = Phase(["a", "b"], {"foo": "bar"})

        # wire project and phase without prepare
        testProject.phaseMap["Phase"] = testPhase
        testProject.phases = [testPhase]
        testPhase.project = testProject

        return testPhase, testProject

    def test_init(self):
        testPhase = Phase(["a", "b"], {"foo": "bar"})
        self.assertEqual(testPhase.exportData, ["a", "b"])
        self.assertEqual(testPhase.options, {"foo": "bar"})
        self.assertEqual(testPhase.exportDataStrings, None)
        self.assertEqual(testPhase._prepared, False)

    def test_getId(self):
        testPhase = self.getDefaultPhase()
        class MyPhase(Phase):
            pass
        self.assertEqual(testPhase.getId(), "Phase")
        self.assertEqual(MyPhase().getId(), "MyPhase")

    def test_getId_name(self):
        testPhase = Phase()
        testPhase.name = "CustomName"
        self.assertEqual(testPhase.getId(), "CustomName")

    def test_prepare(self):
        testPhase, testProject = self.getDefaultPhaseAndProject()

        testPhase.prepareConfig = MagicMock()
        testPhase.prepare()
        self.assertIsInstance(testPhase.exportData[0], Data)
        self.assertEqual(testPhase.exportData[0].project, testProject)
        self.assertEqual(testPhase.exportDataStrings, ["a", "b"])
        testPhase.prepareConfig.assert_called_once()
        self.assertEqual(testPhase.phaseConfig, "value")

        testPhase.prepareConfig.reset_mock()
        # only prepare on default if full config changed
        testProject.trigger("configChanged", None)
        testPhase.prepareConfig.assert_called_once()
        testProject.trigger("configChanged", "test")
        testPhase.prepareConfig.assert_called_once()

    def test_getDecorators(self):
        testPhase, testProject = self.getDefaultPhaseAndProject()
        decorator = MagicMock()
        projectDecorators = [decorator]
        testProject.decorators = projectDecorators

        self.assertEqual(testPhase.getDecorators(), projectDecorators)
        decorator.filter.assert_called_once_with(testPhase)

        decorator.filter.reset_mock()
        testPhase.decorators = projectDecorators
        self.assertEqual(testPhase.getDecorators(), projectDecorators)
        decorator.filter.assert_not_called()


    def test_getConfig(self):
        testPhase = self.getDefaultPhase()
        testPhase.project = MagicMock()
        testPhase.getConfig("test")
        testPhase.project.getConfig.assert_called_with("test",None)
        testPhase.getConfig("test", 5)
        testPhase.project.getConfig.assert_called_with("test",5)

    def test_setConfig(self):
        testPhase = self.getDefaultPhase()
        testPhase.project = MagicMock()
        testPhase.setConfig("test", "value")
        testPhase.project.setConfig.assert_called_with("test","value")

    def test_getData(self):
        testPhase = self.getDefaultPhase()
        testPhase.project = MagicMock()
        testPhase.getData("test", None, "current", {}, True)
        testPhase.project.getData.assert_called_with(dataName="test", expectedReturnType=None, version="current", options={}, generate=True)

    def test_registerData(self):
        testPhase = self.getDefaultPhase()
        testPhase.project = MagicMock()
        testPhase.registerData("test", {}, "current", True)
        testPhase.project.registerData.assert_called_with(dataName="test", data={}, version="current", save=True)

    def test_runOnDefaultGenerateData(self):
        testPhase = self.getDefaultPhase()
        testPhase.run = MagicMock()
        testPhase.generateData("myData")
        testPhase.run.assert_called_once()

    def test_run(self):
        MagicMock()
        testPhase = self.getDefaultPhase()
        testPhase.main = MagicMock()
        decoratorMock = MagicMock()
        testPhase.decorators = [decoratorMock]

        testPhase.run()

        testPhase.main.assert_called_once()
        decoratorMock.before.assert_called_once_with(testPhase)
        decoratorMock.after.assert_called_once_with(testPhase)

    def test_runOverwrite(self):
        Phase.runMethod = "main2"
        MagicMock()
        testPhase = self.getDefaultPhase()
        testPhase.main2 = MagicMock()
        decoratorMock = MagicMock()
        testPhase.decorators = [decoratorMock]

        testPhase.run()

        testPhase.main2.assert_called_once()
        decoratorMock.before.assert_called_once_with(testPhase)
        decoratorMock.after.assert_called_once_with(testPhase)




