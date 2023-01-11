import importlib
import json
from unittest import TestCase
from pyPhases.Data import Data, DataNotFound
from pyPhases.Project import ConfigNotFoundException, Project, PhaseNotFoundException
from pyPhases.decorator.Decorator import Decorator
from pyPhases.exporter.PickleExporter import PickleExporter
from unittest.mock import MagicMock, patch, mock_open
from pyPhases.Phase import Phase
from pyPhases.util.pdict import pdict


class TestProject(TestCase):

    def test_registerDecorator(self):
        decorator = Decorator()
        project = Project()
        project.registerDecorator(decorator)
        self.assertIn(decorator, project.decorators)

    def test_registerExporter(self):
        exporter = PickleExporter()
        project = Project()
        project.registerExporter(exporter)
        self.assertIn(exporter, project.exporters)

    def test_getExporterForIntsance(self):
        project = Project()
        project.getExporterForType = MagicMock()

        project.getExporterForIntsance("test")
        project.getExporterForType.assert_called_with(str)

        project.getExporterForIntsance(5)
        project.getExporterForType.assert_called_with(int)

        class A:
            pass

        project.getExporterForIntsance(A())
        project.getExporterForType.assert_called_with(A)

    def test_getExporterForType(self):
        project = Project()

        self.assertEqual(project.getExporterForType(None), None)
        self.assertEqual(project.getExporterForType(str), None)

        exporter = PickleExporter()
        project.registerExporter(exporter)
        self.assertEqual(project.getExporterForType(str, reinit=False), exporter)

        self.assertNotEqual(project.getExporterForType(str, reinit=True), exporter)
        self.assertIsInstance(project.getExporterForType(str, reinit=True), PickleExporter)

    def test_getDataFromName(self):
        project = Project()
        Data("test", project)
        dataObj = project.getDataFromName("test", "testversion")

        self.assertEqual(dataObj.name, "test")
        self.assertEqual(dataObj.version, "testversion")
        self.assertEqual(dataObj.project, project)

    def test_registerStreamExporterNotExist(self):
        project = Project()
        Data("test", project)

        self.assertRaises(Exception, project.registerStream, "test", str, {})

    def test_registerStream(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporterObject = MagicMock()
        exporter.stream = exporterObject
        exporter.reinit = MagicMock(return_value=exporterObject)

        project.registerStream("test", str, {"foo": "bar"})

        exporter.reinit.assert_called_once()
        exporterObject.stream.assert_called_with("test--current", {"foo": "bar"})

    def test_getExporterAndId(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporter, id = project.getExporterAndId("test", str)
        self.assertIsInstance(exporter, PickleExporter)
        self.assertEqual(id, "test--current")

    def test_getExporterAndIdNoExporter(self):
        project = Project()
        Data("test", project)
        exporter, id = project.getExporterAndId("test", str)
        self.assertEqual(exporter, None)
        self.assertEqual(id, "test--current")

    def test_getExporterAndIdNoData(self):
        project = Project()
        self.assertRaises(Exception, project.getExporterAndId, "test", str)

    def test_dataExists(self):
        project = Project()
        dataObj = Data("test", project)

        project.registerData("test", "myTestStr")

        self.assertTrue(project.dataExists(dataObj))
        self.assertFalse(project.dataExists(Data("test2", project)))

    def test_dataExistIn(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporterObject = MagicMock()
        exporter.stream = exporterObject
        exporter.reinit = MagicMock(return_value=exporterObject)

        project.dataExistIn("test", str, "testversion", options={"foo": "bar"})

        exporter.reinit.assert_called_once()
        exporterObject.exists.assert_called_with("test--testversion", {"foo": "bar"})

    def test_dataExistInIsRegistered(self):
        project = Project()
        Data("test", project)

        project.registerData("test", "test")

        exist = project.dataExistIn("test", str)
        self.assertTrue(exist)

    def test_dataExistInNoExporter(self):
        project = Project()
        Data("test", project)

        r = project.dataExistIn("test", str, "testversion", options={"foo": "bar"})

        self.assertEqual(r, False)

    def test_unregister(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporterObject = MagicMock()
        exporter.stream = exporterObject
        exporter.reinit = MagicMock(return_value=exporterObject)

        project.registeredData["test--testversion"] = "test"

        project.unregister("test", str, "testversion", options={"foo": "bar"})

        self.assertNotIn("test--testversion", project.registeredData)

    def test_unregisterNonExisting(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporterObject = MagicMock()
        exporter.stream = exporterObject
        exporter.reinit = MagicMock(return_value=exporterObject)

        self.assertRaises(KeyError, project.unregister, "test", str, "testversion", options={"foo": "bar"})

    def test_getDataRegistered(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporterObject = MagicMock()
        exporter.stream = exporterObject
        exporter.reinit = MagicMock(return_value=exporterObject)

        project.registeredData["test--testversion"] = "test"

        data = project.getData("test", str, "testversion", options={"foo": "bar"})

        self.assertEqual(data, "test")

    def test_getDataExporter(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporterObject = MagicMock()
        exporter.stream = exporterObject
        exporter.reinit = MagicMock(return_value=exporterObject)

        project.getData("test", str, "testversion", options={"foo": "bar"})

        exporterObject.read.assert_called_with("test--testversion", {"foo": "bar"})

    def test_getDataGenerate(self):
        project = Project()
        project.generateData = MagicMock()
        Data("test", project)

        project.getData("test", str, "current", options={"foo": "bar"})
        project.generateData.called_once_with("test", str, "current", options={"foo": "bar"})

    def test_generateData(self):
        project = Project()
        phase = Phase([Data("dataname", project)])
        project.addPhaseAndPrepare(phase)

        def generateData(id):
            phase.registerData("dataname", "test")
        phase.generateData = generateData

        teststr = project.generateData("dataname", str, "current")
        self.assertEqual(teststr, "test")
        self.assertEqual(project.registeredData["dataname--current"], "test")

    def test_generateDataWithoutRegister(self):
        project = Project()
        phase = Phase([Data("test", project)])
        project.addPhaseAndPrepare(phase)

        def generateData(id):
            return "test"
        phase.generateData = generateData

        teststr = project.generateData("test", str, "current")
        self.assertEqual(teststr, "test")
        self.assertNotIn("dataname--current", project.registeredData)

    def test_getDataGenerateNoGeneration(self):
        project = Project()
        phase = Phase([Data("test", project)])
        project.addPhaseAndPrepare(phase)

        self.assertRaises(DataNotFound, project.generateData, "test", str, "current", options={"foo": "bar"})

    def test_registerData(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporterObject = MagicMock()
        exporter.stream = exporterObject
        exporter.reinit = MagicMock(return_value=exporterObject)

        project.registerData("test", "teststr", version="testversion", options={"foo": "bar"})

        exporterObject.write.assert_called_with("test--testversion", "teststr", {"foo": "bar"})
        self.assertEqual(exporterObject.currentDataObj, project.dataNames["test"])
        self.assertEqual(project.registeredData["test--testversion"], "teststr")

    def test_registerDataNoSave(self):
        project = Project()
        exporter = PickleExporter()
        project.registerExporter(exporter)
        Data("test", project)

        exporterObject = MagicMock()
        exporter.stream = exporterObject
        exporter.reinit = MagicMock(return_value=exporterObject)

        project.registerData("test", "teststr", version="testversion", options={"foo": "bar"}, save=False)

        exporterObject.write.assert_not_called()
        self.assertEqual(project.registeredData["test--testversion"], "teststr")

    def test_setConfig(self):
        project = Project()
        project.setConfig("test", "test")
        self.assertEqual(project.config["test"], "test")

    def test_setConfigDotNotation(self):
        project = Project()
        project.setConfig("test.blub", "test")
        self.assertEqual(project.config["test"]["blub"], "test")

    def test_getConfig(self):
        project = Project()
        project.config["test"] = "test"
        self.assertEqual(project.getConfig("test"), "test")

    def test_getConfigDotNotation(self):
        project = Project()
        project.config["test"] = {"blub": "test"}
        self.assertEqual(project.getConfig("test.blub"), "test")

    def test_getConfigKeyError(self):
        project = Project()
        self.assertRaises(ConfigNotFoundException, project.getConfig, "test")

    @patch('builtins.open', new_callable=mock_open, read_data='data')
    def test_saveConfig(self, m):
        json.dump = MagicMock()
        project = Project()
        project.setConfig("foo", "bar")

        m.return_value.__enter__.return_value = "data"
        project.saveConfig("myConfig.json")

        m.assert_called_with("myConfig.json", "w+")
        json.dump.assert_called_with({"foo": "bar"}, "data")

    @patch('builtins.open', new_callable=mock_open, read_data='')
    def test_saveConfig_tailor(self, m):
        json.dump = MagicMock()
        project = Project()
        Data("test", project, ["subconfig"])
        project.config = {"subconfig": {"foo": "bar"}, "othervalue": "test"}
        m.return_value.__enter__.return_value = "data"

        project.saveConfig("myConfig.json", "test")

        m.assert_called_with("myConfig.json", "w+")
        json.dump.assert_called_with({"subconfig": {"foo": "bar"}}, "data")

    @patch('builtins.open', new_callable=mock_open, read_data='{"foo": "bar"}')
    def test_loadConfig(self, m):
        project = Project()

        project.loadConfig("myConfig.json")

        m.assert_called_with("myConfig.json", "rb")
        self.assertIn("foo", project.config)
        self.assertEqual(project.config["foo"], "bar")

    def test_addConfig(self):
        project = Project()
        project.config = pdict({"foo": "keep", "foofoo": {"bar": "overwrite", "foo2": "keep"}})
        updateConfig = pdict({"foo2": "add", "foofoo": {"bar": "foo", "bar2": "add"}})
        project.addConfig(updateConfig)

        self.assertEqual(project.config, {
            "foo": "keep",
            "foo2": "add",
            "foofoo": {
                "bar": "foo",
                "foo2": "keep",
                "bar2": "add"
            }
        })

    def test_addPhaseAndPrepare(self):
        project = Project()
        phase = Phase()
        project.addPhaseAndPrepare(phase)
        self.assertEqual(project.phases[0], phase)
        self.assertEqual(project.phases[0].name, "Phase")
        self.assertEqual(project.phaseMap["Phase"], phase)

    def test_addPhaseAndPrepareWithName(self):
        project = Project()
        phase = Phase()
        project.addPhaseAndPrepare(phase, "test")
        self.assertEqual(project.phases[0], phase)
        self.assertEqual(project.phases[0].name, "test")
        self.assertEqual(project.phaseMap["test"], phase)

    def test_addPlugin(self):
        project = Project()
        importlib.import_module = MagicMock()
        project.addPlugin("myPlugin", {"foo": "bar"})
        plugin = importlib.import_module.return_value.Plugin
        pluginObj = importlib.import_module.return_value.Plugin.return_value

        importlib.import_module.assert_called_once_with(".Plugin", package="myPlugin")
        plugin.assert_called_once_with(project, {"foo": "bar"})
        self.assertEqual(project.plugins[0], pluginObj)
        pluginObj.initPlugin.assert_not_called()
        project.trigger("configChanged", None)
        pluginObj.initPlugin.assert_called_once()

    def test_prepareAllPhases(self):
        project = Project()
        phase = MagicMock()
        project.addPhaseAndPrepare(phase)

        phase.prepare.assert_called_once()
        phase.prepare.reset_mock()

        project.prepareAllPhases()

        phase.prepare.assert_called_once()

    def test_run(self):
        project = Project()
        phase = Phase()
        phase.run = MagicMock()
        project.addPhaseAndPrepare(phase)

        project.run("Phase")

        phase.run.assert_called_once()

    def test_runPhase(self):
        project = Project()
        phase = Phase()
        project.addPhaseAndPrepare(phase)
        project.trigger = MagicMock()
        phase.run = MagicMock()

        project.runPhase(phase)

        phase.run.assert_called_once()
        project.trigger.called_once_with("afterRun")

    def test_getPhase(self):
        project = Project()
        phase = Phase()
        project.addPhaseAndPrepare(phase)

        self.assertEqual(project.getPhase("Phase"), phase)

    def test_getPhaseNotExist(self):
        project = Project()
        self.assertRaises(PhaseNotFoundException, project.getPhase, "Phase")


    def test_enterContext(self):
        project = Project()
        project.config = pdict({"foo": "bar"})
        project.trigger = MagicMock()

        with project as p:
            p.setConfig("foo", "bar2")
            self.assertEqual(project.config["foo"], "bar2")
            project.trigger.assert_called_once_with("configChanged", "foo")

        self.assertEqual(project.config["foo"], "bar")
        project.trigger.assert_called_with("configChanged", None)

