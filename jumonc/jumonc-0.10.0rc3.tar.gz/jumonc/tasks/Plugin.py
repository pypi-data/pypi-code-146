from jumonc.models import pluginInformation

class Plugin:
    works = None
    
    def __init__(self) -> None:
        """Base class for all plugins to use."""
    
    def isWorking(self) -> bool:
        if self.works is None:
            self.works = self._isWorking()
            pluginInformation.addPluginStatus("jumonc" + type(self).__name__, self.works)
        return self.works
    
    def notWorkingAnymore(self) -> None:
        self.works = False
        pluginInformation.disablePlugin("jumonc" + type(self).__name__)
    
    def _isWorking(self) -> bool:
        raise NotImplementedError("Please Implement this method")
