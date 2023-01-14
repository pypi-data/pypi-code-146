from coinlib.PluginLoader import PluginLoader


class LogicFactory(PluginLoader):

    def __init__(self, parentdirectory=""):
        super(LogicFactory, self).__init__(parentdirectory=parentdirectory)
        return None

    def hasPlugins(self):
        return False

    def getLoaderPath(self):
        return ".logic_modules"

    def loadBrokerModulesForTrader(self):

        self.registrar.brokerFactory.loadPlugins()

        return True

    def loadChildModules(self, module):

        if self.registrar.isLiveEnvironment():
            if module.startswith("online"):
                self.loadBrokerModulesForTrader()



