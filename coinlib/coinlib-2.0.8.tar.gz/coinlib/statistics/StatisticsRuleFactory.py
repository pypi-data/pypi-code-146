from coinlib.PluginLoader import PluginLoader

class StatisticsRuleFactory(PluginLoader):

    def __init__(self, parentdirectory=""):
        super(StatisticsRuleFactory, self).__init__(parentdirectory=parentdirectory)
        return None
        
    def getLoaderPath(self):
        return ".statsrules_modules"
    
    
    
    
    