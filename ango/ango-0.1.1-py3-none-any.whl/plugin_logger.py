import logging
import socketio


class PluginLogger(logging.Logger):

    def __init__(self, name: str, plugin_id: str, org_id: str, run_by: str, session: str, plugin: socketio.ClientNamespace, level=logging.NOTSET):
        super().__init__(name, level)
        self.plugin_id = plugin_id
        self.org_id = org_id
        self.plugin = plugin
        self.run_by = run_by
        self.session = session

    def warning(self, msg, *args, **kwargs):
        log = self.__log("WARNING", msg, *args, **kwargs)
        return super().warning(log)

    def error(self, msg, *args, **kwargs):
        log = self.__log("ERROR", msg, *args, **kwargs)
        return super().error(log)

    def debug(self, msg, *args, **kwargs):
        log = self.__log("DEBUG", msg, *args, **kwargs)
        return super().debug(log)

    def info(self, msg, *args, **kwargs):
        log = self.__log("INFO", msg, *args, **kwargs)
        super().info(log)

    def __log(self, level, msg, *args, **kwargs):
        data = kwargs
        data["level"] = level
        data["organization"] = self.org_id
        data["pluginId"] = self.plugin_id
        data["runBy"] = self.run_by
        data["session"] = self.session
        data["msg"] = msg + ' '.join(args)
        self.plugin.emit("log", data)
        return data
