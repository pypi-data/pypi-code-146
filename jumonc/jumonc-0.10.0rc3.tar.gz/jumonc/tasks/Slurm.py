from jumonc.tasks import Plugin

class _SlurmPlugin(Plugin.Plugin):
    
    def _isWorking(self) -> bool:
        return False


plugin = _SlurmPlugin()
