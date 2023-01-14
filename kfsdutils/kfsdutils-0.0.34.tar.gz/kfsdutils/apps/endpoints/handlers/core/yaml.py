from kfsdutils.apps.endpoints.handlers.core.logger import Logger, LogLevel
import ruamel.yaml
from ruamel.yaml import YAML
from ruamel.yaml.compat import StringIO
from ruamel.yaml.scalarstring import LiteralScalarString


class Yaml(YAML):
    def __init__(self):
        self.__logger = Logger.getSingleton(__name__, LogLevel.DEBUG)
        self.__YAML = YAML()

    def getRuamelYaml(self):
        return self.__YAML

    def isMultiLineKey(self, key):
        return key.endswith("|")

    def formatMultiLineKey(self, key):
        return key[:-1]

    def formattedKey(self, key):
        return (self.formatMultiLineKey(key) if self.isMultiLineKey(key) else key)

    def isMultiLineStrVal(self, value):
        return True if ("\n" in value) else False

    def convertValToYamlByType(self, value):
        if isinstance(value, str) and self.isMultiLineStrVal(value):
            return self.convertStrToMultiLine(value)
        elif isinstance(value, dict):
            return self.convertDictToMultiLine(value)
        elif isinstance(value, list):
            return self.convertListToMultiLine(value)

        return value

    def convertStrToMultiLine(self, value):
        return LiteralScalarString(self.formatFinalMultiLineStr("""\
{}
""".format(value)))

    def convertDictToMultiLine(self, value):
        dictYamlStr = self.getYaml(value)
        return LiteralScalarString(self.formatFinalMultiLineStr("""\
{}
""".format(dictYamlStr)))

    def convertListToMultiLine(self, value):
        return LiteralScalarString(self.formatFinalMultiLineStr("""\
{}
""".format("\n".join(value[0:]))))

    def formatFinalMultiLineStr(self, str):
        return str.strip()+"\n"

    def formatListConfig(self, value):
        return [self.formattedValueByType(item) for item in value]

    def formattedDictValue(self, key, value):
        if self.isMultiLineKey(key):
            return self.convertValToYamlByType(value)

        return self.formattedValueByType(value)

    def formattedValueByType(self, value):
        if isinstance(value, dict):
            return self.formatDictConfig(value)
        elif isinstance(value, list):
            return self.formatListConfig(value)
        elif isinstance(value, str) and self.isMultiLineStrVal(value):
            return self.convertStrToMultiLine(value)

        return value

    def formatDictConfig(self, config):
        return {self.formattedKey(k): self.formattedDictValue(k, v) for (k, v) in config.items()}

    def getYaml(self, data, **kw):
        stream = StringIO()
        self.__YAML.dump(data, stream, **kw)
        return stream.getvalue()

    def getPythonObj(self, config):
        return ruamel.yaml.safe_load(self.getYaml(config))
