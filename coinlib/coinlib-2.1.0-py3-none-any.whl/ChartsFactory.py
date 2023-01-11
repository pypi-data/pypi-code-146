from coinlib.PluginLoader import PluginLoader

class ChartsFactory(PluginLoader):

    def __init__(self, parentdirectory=""):
        super(ChartsFactory, self).__init__(parentdirectory=parentdirectory)
        return None
        
    def getLoaderPath(self):
        return ".chart_modules"
    
    
    
    
    