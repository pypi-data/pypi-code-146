from coinlib.PluginLoader import PluginLoader


class NotificationFactory(PluginLoader):

    def __init__(self, parentdirectory=""):
        super(NotificationFactory, self).__init__(parentdirectory=parentdirectory)
        return None

    def getLoaderPath(self):
        return ".notification_modules"




