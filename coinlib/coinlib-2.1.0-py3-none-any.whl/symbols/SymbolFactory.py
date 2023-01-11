from coinlib.PluginLoader import PluginLoader

class SymbolFactory(PluginLoader):

    def __init__(self, parentdirectory=""):
        super(SymbolFactory, self).__init__(parentdirectory=parentdirectory)
        return None
        
    def getLoaderPath(self):
        return ".symbolbroker_modules"
    
    
    
    
    