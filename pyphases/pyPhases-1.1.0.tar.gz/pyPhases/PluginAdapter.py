from pyPhases.util.EventBus import EventBus
from pyPhases.util.Optionizable import Optionizable
from pyPhases import Project

class PluginAdapter(Optionizable, EventBus):

    def __init__(self, project: Project, options=...):
        super().__init__(options)
        self.project = project

    def getConfig(self, key):
        return self.project.getConfig(key)

    def initPlugin(self, project):
        self.project = project
        self.logDebug("Plugin loaded")
