import importlib
import json
from typing import Iterator

from pyPhases.Data import Data, DataNotFound
from pyPhases.Phase import Phase
from pyPhases.util.EventBus import EventBus
from pyPhases.util.Logger import Logger
from pyPhases.util.Optionizable import Optionizable
from pyPhases.util.pdict import pdict
from pyPhases.exporter.DataExporter import DataExporter


class ConfigNotFoundException(Exception):
    pass


class PhaseNotFoundException(Exception):
    pass


class Project(Optionizable, EventBus):
    """
    Represents a whole project that can run code and produce data depending on config values

    Parameters
    ----------
    name : string
        name of the project
    namespace : string
        namespace of the project e.e tud.ibmt
    """

    def __init__(self, name="myProject", namespace=""):
        self.phases = []
        self.name = name
        self.namespace = namespace
        self.dataNames = {}
        self.classes = []
        self.exporters = []
        self.classesMap = {}
        self.registeredData = {}
        self.config = pdict()
        self.configBackup = None
        self.phaseIndex = 0
        self.decorators = []
        self.debug = False
        self.testRun = False
        self.phaseMap = {}
        self.logLevel = None
        self.gridOutput = None
        self.plugins = []
        self.systemExporter = {"PickleExporter": "pyPhases"}

    def registerDecorator(self, decorator):
        """registers a decorator to the project that is run before and after each phase"""
        self.logDebug("Register Decorator: " + type(decorator).__name__)
        self.decorators.append(decorator)

    def registerExporter(self, exporter):
        """registers an exporter to the project that can handle data types and transform oder save objects"""
        self.logDebug("Register Exporter: " + type(exporter).__name__)
        self.exporters.append(exporter)

    def getExporterForIntsance(self, instance) -> DataExporter:
        """return a exporter that can handle the given instance, if such a exporter exists else None"""
        self.logDebug("Get Exporter For: " + type(instance).__name__)
        return self.getExporterForType(type(instance))

    def getExporterForType(self, theType, reinit=True) -> DataExporter:
        """return a exporter that can handle the given type, if such a exporter exists else None

        Args:
            theType (_type_): the type that should be exported
            reinit (bool, optional): reload the exporter

        Returns:
            Exporter: the exporter that can handle the given type
        """
        exporters = self.exporters

        if theType is None:
            return None

        for exporter in exporters:
            self.logDebug("Check: " + type(exporter).__name__)
            if exporter.checkType(theType):
                self.logDebug("Found exporter")
                if reinit:
                    return exporter.reinit()
                else:
                    return exporter
        return None

    def getDataFromName(self, dataName: str, version: str = "current") -> Data:
        """returns a data object for the given data name

        Args:
            dataName (str): the name of the data
            version (str, optional): version string

        Returns:
            Data: the data object
        """

        if dataName not in self.dataNames:
            raise Exception("The DataWrapper with name %s was not defined and does not exist in any phase" % (dataName))

        dataObj = self.dataNames[dataName]
        dataObj.version = version

        return dataObj

    def registerStream(self, dataName, expectedReturnType, options, version: str = "current"):
        """registers a stream for the given data name, a stream can be a reference to a file for example"""
        dataObj = self.getDataFromName(dataName, version=version)
        dataId = dataObj.getDataId()

        exporter = self.getExporterForType(expectedReturnType)
        if exporter is None:
            raise Exception("No stream exporter found for type %s" % (expectedReturnType))
        return exporter.stream(dataId, options)

    def getExporterAndId(self, dataName, expectedReturnType, options={}, version: str = "current"):
        """returns a exporter and the data id as a string for the given data name

        Args:
            dataName (str): the identifiation name of the data
            expectedReturnType (type): the expedted type of the data (is required to select the right exporter)

        Returns:
            (Exporter, str): a tuple of the exporter and the data id
        """

        dataObj = self.getDataFromName(dataName, version=version)
        dataId = dataObj.getDataId()

        try:
            exporter = self.getExporterForType(expectedReturnType, reinit=False)
            return exporter, dataId
        except Exception:
            raise Exception("No stream exporter found for this")

    def dataExists(self, data: Data):
        """returns true if the given data object is registered in the project"""
        return data.getDataId() in self.registeredData

    def dataExistIn(self, dataName: str, expectedReturnType=None, version: str = "current", options=None):
        """returns true if the exporter can read the data"""

        dataObj = self.getDataFromName(dataName, version=version)
        dataId = dataObj.getDataId()

        if dataId in self.registeredData:
            return True

        # check if the can be loaded by the exporter
        exporter = self.getExporterForType(expectedReturnType)
        if exporter is None:
            return False

        return exporter.exists(dataId, options)

    def unregister(self, dataName: str, expectedReturnType=None, version: str = "current", options=None):
        """unregisters a data from the project memory, it will not delete the data itself"""
        dataObj = self.getDataFromName(dataName, version=version)
        dataId = dataObj.getDataId()
        del self.registeredData[dataId]

    def getData(self, dataName: str, expectedReturnType=None, version: str = "current", options=None, generate=True):
        """
        returns either a registerd data in the project memory,
        loads the data from a exporter or generates the data from a phase
        """

        options = options or {}

        dataObj = self.getDataFromName(dataName, version=version)
        dataId = dataObj.getDataId()

        self.logDebug("Try to get Data: " + dataId)

        # just generated Data
        if dataId in self.registeredData:
            self.logDebug("Data in memory: " + dataId)
            return self.registeredData[dataId]

        # load from exporter layer
        exporter = self.getExporterForType(expectedReturnType)
        if exporter is not None:
            try:
                exporter.currentDataObj = dataObj
                return exporter.read(dataId, options)
            except DataNotFound:
                pass

        # data not found, generate from phase
        if generate and version == "current":
            self.logWarning("Data " + dataId + " was not found, try to find phase to generate it")
            return self.generateData(dataName, expectedReturnType, version, options)

        raise DataNotFound("Data " + dataName + " was not found: %s" % dataId)

    def generateData(self, dataName: str, expectedReturnType=None, version: str = "current", options={}):
        """forces the data generation for a specific dataName"""
        for phase in self.getPhases():
            if dataName in phase.exportDataStrings:
                returnedData = phase.generateData(dataName)
                if returnedData is not None:
                    return returnedData
                try:
                    return self.getData(dataName, expectedReturnType, version, options, generate=False)
                except DataNotFound:
                    raise DataNotFound(
                        "try to generate data %s with phase %s but it was not registerd" % (dataName, phase.getId())
                    )

        raise DataNotFound("Data " + dataName + " was not found")

    def registerData(self, dataName: str, data, version: str = "current", save: bool = True, options=None):
        """registers a data object in the project memory and saves it through the exporter

        Args:
            dataName (str): the identifiation name of the data
            data: the data object
            save (bool): if set to false the project will not try to save the data

        Returns:
            (Exporter, str): a tuple of the exporter and the data id
        """
        options = options or {}
        dataObj = self.getDataFromName(dataName, version=version)
        dataId = dataObj.getDataId()

        # save to runtime project
        self.registeredData[dataId] = data

        if save is False:
            return

        # save through exporter
        exporter = self.getExporterForIntsance(data)
        if exporter is None:
            self.logWarning(
                "No exporter for datatype (" + type(data).__name__ + ") the data " + dataName + " will not be automaticly save"
            )
            return
        exporter.currentDataObj = dataObj
        exporter.write(dataId, data, options)

    def setConfig(self, name: str, value):
        """
        sets a config value in the project. Dot notation is supported for nested config values
        (f.e. project.setConfig('foo.bar.value1', 'v1')
        """
        if "." in name:
            name = name.split(".")
        self.config[name] = value
        self.trigger("configChanged", name)

    def getConfig(self, name: str, defaultValue=None, raiseException=True) -> str:
        """
        gets a config value in the project. Dot notation is supported for nested config values
        (f.e. project.getConfig('foo.bar.value1')
        """
        if name not in self.config:
            if "." in name:
                name = name.split(".")
            try:
                return self.config[name]
            except KeyError:
                self.config[name] = defaultValue
                if defaultValue is None and raiseException:
                    raise ConfigNotFoundException(
                        "The Config entry '%s' was not found, if you rely on a earlier config entry in a previous phase make sure you put the config entry in the __init__ section of the phase"
                        % (name)
                    )
        return self.config[name]

    def saveConfig(
        self,
        path: str,
        dataName=None,
        version: str = "current",
    ):
        """Save the current project configuration to a JSON file.

        Args:
            path (str): filepath for the json file
            dataName (str): only store the config for a given nested value
        """
        if dataName is not None:
            config = self.getDataFromName(dataName, version=version).getDependencyDict()
        else:
            config = self.config

        with open(path, "w+") as f:
            self.log("save config from file %s" % path)
            json.dump(config, f)

    def loadConfig(self, path: str):
        """Load project configuration from a JSON file .

        Args:
            path (str): filepath for the json file
        """
        with open(path, "rb") as f:
            self.log("load config from file %s" % path)
            config = json.loads(f.read())
            self.config.update(config)
            self.trigger("configChanged", None)

    def addConfig(self, config) -> None:
        self.config.update(config)

    def addPhase(self, phase: Phase, name: str = None):
        name = name or phase.getId()

        phase.name = name
        self.addConfig(phase.config)
        phase.project = self

        self.phaseMap[name] = phase
        self.phases += [phase]

    def addPhaseAndPrepare(self, phase: Phase, name: str = None):
        self.addPhase(phase, name)
        phase.prepare()

    def addPlugin(self, pluginName, options={}):
        """adds a pyPhases plugin to the project"""

        pluginClass = importlib.import_module(".Plugin", package=pluginName).Plugin
        plugin = pluginClass(self, options)

        # only init plugins if the whole config changes
        def initPlugins(chanedField):
            if chanedField is None:
                plugin.initPlugin()

        self.on("configChanged", initPlugins)
        self.plugins.append(plugin)

    def prepareAllPhases(self):
        """run prepare in all phases to reset computed config"""
        for index in self.phaseMap:
            phase = self.phaseMap[index]
            phase._prepared = False
            phase.prepare()

    def run(self, phaseName):
        """run a specific phase"""
        if self.logLevel is not None:
            Logger.verboseLevel = self.logLevel

        phase = self.getPhase(phaseName)
        self.runPhase(phase)

    def runPhase(self, phase: Phase):
        phase.run()
        self.trigger("afterRun")

    def getPhase(self, name: str) -> Phase:
        """get a specific phase by name"""

        if name not in self.phaseMap:
            raise PhaseNotFoundException("Phase %s not found" % name)

        return self.phaseMap[name]

    def getPhases(self) -> Iterator[Phase]:
        """get a generator for all phases"""
        for phase in self.phases:
            yield phase

    def __enter__(self):
        """enter a config scope and backup the old config"""
        self.configBackup = pdict(self.config.copy())
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """exit the config scope and restore the old config"""
        self.config = self.configBackup
        self.trigger("configChanged", None)
