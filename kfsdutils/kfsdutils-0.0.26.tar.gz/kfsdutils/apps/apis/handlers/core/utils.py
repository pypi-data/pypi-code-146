import functools, os, shutil, json
from collections.abc import Mapping
from .logger import Logger, LogLevel

class ArrUtils:
    def __init(self):
        self.__logger = Logger.getSingleton(__name__, LogLevel.DEBUG)

    @staticmethod
    def joinArrayToStr(joinByStr, arr):
        return joinByStr.join(arr)

    @staticmethod
    def intersection(arr1, arr2):
        return list((set(arr1) & set(arr2)))

    @staticmethod
    def mergeByMatchingDictItemKeyInArray(dict1, dict2, matchKey):
        return [ DictUtils.mergeDicts(x,y) if x[matchKey] == y[matchKey] else x  for x in dict1 for y in dict2 ]

    @staticmethod
    def mergeArray(d, u):
        uniq_list = []
        all_list = d + u
        for i in all_list:
            if i not in uniq_list:
                uniq_list.append(i)
        return uniq_list

    @staticmethod
    def sortKeysByLength(keys, isReverse=False):
        return sorted(keys, key=len, reverse=isReverse)

    @staticmethod
    def isSubset(list1, list2):
        set1 = set(list1)
        set2 = set(list2)
        if set2.issubset(set1):
            return True

        return False

    @staticmethod
    def getAllSubsetKeys(arr, parentArr):
        return [x for x in arr if ArrUtils.isSubset(parentArr, x)]

    @staticmethod
    def toDict(arr, key):
        return {item[key]: item for item in arr}

class FileUtils():
    def __init__(self):
        self.__logger = Logger.getSingleton(__name__, LogLevel.DEBUG)

    def constructPath(self, dir, dest):
        return os.path.join(dir, dest)

    def copyDir(self, src, dest):
        self.__logger.debug("Copy Dir: src: {}, dest: {}".format(src, dest))
        shutil.copytree(src, dest)

    def createDir(self, dirPath):
        self.__logger.debug("Create Directory: {}".format(dirPath))
        os.makedirs(dirPath)

    def pathExists(self, destPath):
        if not os.path.exists(destPath):
            return False
        return True

    def readJsonFromFile(self, filePath):
        with open(filePath) as json_file:
            return json.load(json_file)

        return None

    def readFileAsString(self, filePath, removeLineBreaks=True):
        fileStr = ""
        with open(filePath, 'r') as file:
            fileStr = file.read()
        return fileStr.replace("\n", " ") if removeLineBreaks else fileStr

    def readFile(self, filePath, startLineNum=0, endLineNum=None, removeLineBreaks=True):
        lines = []
        with open(filePath, 'r') as file:
            lines = file.readlines()
        return [x.replace("\n","") for x in lines][startLineNum:endLineNum] if removeLineBreaks else lines[startLineNum:endLineNum]

    def writeToFile(self, filePath, data):
        with open(filePath, 'w') as file:
            file.write(data)
            file.close()

    def updateJsonFile(self, jsonFilePath, dictData):
        with open(jsonFilePath, 'w') as jsonFile:
            json.dump(dictData, jsonFile)

    def moveFile(self, srcFile, destDir):
        shutil.move(srcFile, destDir)

    def copyFile(self, srcFile, destFilePath):
        shutil.copy(srcFile, destFilePath)

    def rmDir(self, dirPath):
        if self.pathExists(dirPath):
            shutil.rmtree(dirPath)

class DictUtils:
    @staticmethod
    def getAllDictKeys(arr, d):
        for k, v in d.items():
            arr.append(k)
            if isinstance(d.get(k), dict) and isinstance(v, Mapping):
                DictUtils.getAllDictKeys(arr, d.get(k, {}))
                
    @staticmethod
    def getDictValue(d: dict, k: str, default=None):
        if k in d:
            return d[k]
        return default

    @staticmethod
    def copyDicts(d: dict, d1: dict):
        return {**d, **d1}

    @staticmethod
    def createDictTreeByKeysAndValueEdge(keys, edgeValue):
        return functools.reduce((lambda x, y: {y: x}), keys[::-1], edgeValue)

    @staticmethod
    def isKeyInDict(d: dict, k: str) -> bool:
        if k in d:
            return True
        return False

    @staticmethod
    def getValueFromKeyPath(key:str, dictionary: dict):
        keys = key.split(".")
        return functools.reduce(lambda d, key: (d.get(key) if isinstance(d, dict) else None) if d else None, keys, dictionary)

    @staticmethod
    def mergeDicts(d, u):
        for k, v in u.items():
            if isinstance(d.get(k), dict) and isinstance(v, Mapping):
                d[k] = DictUtils.mergeDicts(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    @staticmethod
    def filterDictByKeysList(dictionary: dict, visibleKeys: list) -> dict:
        return {k: v for k, v in dictionary.items() if k in visibleKeys }

    @staticmethod
    def filterDictByKeysListNeg(dictionary: dict, visibleKeys: list) -> dict:
        return {k: v for k, v in dictionary.items() if k not in visibleKeys }

    @staticmethod
    def isAllKeyInDict(d: dict, keys: list) -> bool:
        if all(key in d for key in keys): 
            return True
        return False

    @staticmethod
    def createSubDict(d, keys):
        return {x:d[x] for x in keys}

    @staticmethod
    def createDic(**kwargs):
        return kwargs

    @staticmethod
    def sortByValues(d, isReverse):
        sortedD = sorted(d.items(), key=lambda x:x[1], reverse=isReverse)
        return dict(sortedD)


class InstanceUtils():
    def __init__(self, instance):
        self.__instance = instance
        self.__modelSerializer = None
        self.__model = None
        self.__dataIndex = None
        self.__qs = None
        self.__modelSerializer = None

    def getInstance(self):
        return self.__instance

    def setModel(self, model):
        self.__model = model

    def setDataIndex(self, flag):
        self.__dataIndex = flag
    
    def setModelSerializer(self, modelSerializer):
        self.__modelSerializer = modelSerializer

    def setQS(self, qs):
        self.__qs = qs
    
    def getName(self):
        return self.__model.__name__

    def getQS(self):
        return self.__qs
    
    def getModel(self):
        return self.__model

    def isDataIndex(self):
        return self.__dataIndex
    
    def getModelSerializer(self):
        return self.__modelSerializer


class Relation():
    ARG_QS = "qs"
    ARG_INSTANCE_UTILS = "instance_utils"
    def __init__(self, **kwargs):
        self.__instanceUtils = DictUtils.getDictValue(kwargs, self.ARG_INSTANCE_UTILS)
        self.__qs = DictUtils.getDictValue(kwargs, self.ARG_QS)
        self.__source = self.__instanceUtils(self.__qs.source)
        self.__target = self.__instanceUtils(self.__qs.target)

    def getTarget(self):
        return self.__target

    def getSource(self):
        return self.__source

    def setName(self, newName):
        self.__qs.name = newName

    def getName(self):
        if hasattr(self.__qs, 'name'):
            return self.__qs.name
        return None
    
    def getData(self):
        return self.__qs.getModelQSData()
    
    def getTargetIdentifier(self):
        return self.__target.getInstance().identifier

    def getTargetExternalIdentifier(self):
        return self.__target.getInstance().external_identifier

    def getSourceIdentifier(self):
        return self.__source.getInstance().identifier

    def getSourceType(self):
        return self.__qs.source_type

    def getTargetType(self):
        return self.__qs.target_type

    def getLink(self):
        if hasattr(self.__qs, 'link'):
            return self.__qs.link
        return None

    def setLink(self, linkVals):
        self.__qs.link = linkVals

    def getQS(self):
        return self.__qs

    def save(self):
        self.__qs.save()

    def delete(self):
        self.__qs.delete()

    def getUniqKey(self):
        linkVal = ""
        if self.getLink():
            linkVal = ":".join(self.getLink())
        return (self.getName(), self.getSourceIdentifier(), self.getSourceType(), self.getTargetIdentifier(), self.getTargetType(), linkVal)


class Relations():
    def __init__(self):
        self.__dict = {}
    
    def add(self, relation):
        key = relation.getUniqKey()
        if not key in self.__dict:
            self.__dict[key] = relation

    def get(self, key):
        return DictUtils.getDictValue(self.__dict, key)

    def remove(self, key):
        self.__dict.pop(key, None)
            
    def getAll(self):
        return self.__dict

    def getIdentifiers(self):
        identifiersSet =  {relation.getTargetIdentifier() for relation in self.__dict.values()}
        return list(identifiersSet)

    def getExternalIdentifiers(self):
        identifiersSet =  {relation.getTargetExternalIdentifier() for relation in self.__dict.values()}
        return list(identifiersSet)
