from coinlib.PluginLoader import PluginLoader

class StatisticsMethodFactory(PluginLoader):

    def __init__(self, parentdirectory=""):
        super(StatisticsMethodFactory, self).__init__(parentdirectory=parentdirectory)
        return None
        
    def getLoaderPath(self):
        return ".statsmethod_modules"
    
    
    
    
    