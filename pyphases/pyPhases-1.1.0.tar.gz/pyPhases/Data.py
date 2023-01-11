import hashlib
import re

from pyPhases import Project
from pyPhases.util.Logger import classLogger
from pyPhases.util.Optionizable import Optionizable


class DataNotFound(Exception):
    pass


class Data(Optionizable):
    project: Project
    version = "current"

    def __init__(self, name, project, dataTags=None):
        self.name = name
        self.dataTags = dataTags or []
        self.project = project
        self.project.dataNames[name] = self

    @staticmethod
    def flattenLongString(s: str):
        return hashlib.sha1(bytes(s, "utf-8")).hexdigest()[0:8]

    @staticmethod
    def hasTobeHashed(o):
        return isinstance(o, dict) or isinstance(o, list)

    @staticmethod
    def flatten(o) -> str:
        if Data.hasTobeHashed(o):
            return Data.flattenLongString(str(o))

        return None if o is None else re.sub("[^a-zA-Z0-9]", "-", re.sub("[ \(\)]", "", str(o)))

    @staticmethod
    def flattenConfigValues(o):
        return Data.flatten(o)

    def _getTagValue(self, tagname):
        # TODO: circle detection
        if tagname in self.project.dataNames:
            tags = self.project.dataNames[tagname].dataTags
            self.logDebug("Data %s depends on different dataset %s: %s" % (self.name, tagname, tags))
            return self.parseDatanames(self.project.dataNames[tagname].dataTags)

        value = self.project.getConfig(tagname)
        flat = Data.flatten(value)
        if self.hasTobeHashed(value):
            self.logDebug("config value %s has to be hashed: %s" % (tagname, flat))
        return flat

    def getDependencyDict(self, tagNames = None):
        dep = {}
        tagNames = tagNames if tagNames is not None else self.dataTags
        for tagname in tagNames:
            if tagname in self.project.dataNames:
                tags = self.project.dataNames[tagname].dataTags
                self.logDebug("Data %s depends on different dataset %s: %s" % (self.name, tagname, tags))
                dep.update(self.getDependencyDict(self.project.dataNames[tagname].dataTags))
            else:
                value = self.project.getConfig(tagname)
                dep[tagname] = value
        return dep

    def parseDatanames(self, tags):
        tagList = map(self._getTagValue, tags)
        return "-".join([t for t in tagList if t is not None])

    def getTagString(self):
        return self.parseDatanames(self.dataTags)

    def getDataName(self):
        return self.name + self.getTagString()

    def __str__(self):
        return self.getDataName()

    def getDataId(self):
        return self.getDataName() + "--" + self.version

    @staticmethod
    def create(val, project, dependsOn=None):
        dataObj = None
        if isinstance(val, Data):
            dataObj = val
        elif isinstance(val, str):
            dataObj = Data(val, project)
        else:
            raise Exception("Unsupported type as data identifier")

        if dependsOn is not None:
            dataObj.dataTags = dependsOn or []

        return dataObj
