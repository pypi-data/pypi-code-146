from coinlib.PluginLoader import PluginLoader


class FeatureFactory(PluginLoader):

    def __init__(self, parentdirectory=""):
        super(FeatureFactory, self).__init__(parentdirectory=parentdirectory)
        return None

    def getLoaderPath(self):
        return ".feature_modules"




