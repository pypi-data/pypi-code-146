from coinlib.PluginLoader import PluginLoader


class BrokerFactory(PluginLoader):

    def __init__(self, parentdirectory=""):
        super(BrokerFactory, self).__init__(parentdirectory=parentdirectory)
        return None

    def getLoaderPath(self):
        return ".broker_modules"




