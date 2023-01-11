##
# File:    DictionaryRegistry.py
# Author:  jdw
# Date:    3-Oct-2013
# Version: 0.001
#
# Updates:
#     7-Jul-2018  ep  mmcif_ma and remove generation of mmcif_mdb to registry
##
"""
Classes providing a registry of essential information about known data dictionaries and data item coverage statistics.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2,0"

import logging

from rcsb.utils.io.MarshalUtil import MarshalUtil

logger = logging.getLogger(__name__)


class DictionaryRegistry(object):
    def __init__(self, registryPath):
        rObj = self.__getRegistry(registryPath)
        self.__otherDictionaryNameList = rObj["otherDictionaryNameList"]
        self.__internalDictionaryNameList = rObj["internalDictionaryNameList"]
        self.__pdbxDictionaryNameList = rObj["pdbxDictionaryNameList"]
        self.__dictionaryNameList = []
        self.__dictionaryNameList.extend(self.__pdbxDictionaryNameList)
        self.__dictionaryNameList.extend(self.__otherDictionaryNameList)
        self.__dictInfoD = rObj["dictionaryInfo"]

    def __getRegistry(self, registryPath):
        """"""
        try:
            mU = MarshalUtil()
            obj = mU.doImport(registryPath, fmt="json")
            return obj["mmcif_dictionary_registry"]
        except Exception as e:
            logger.exception("Failing for %r with %s", registryPath, str(e))

    def getDictionaryNameList(self):
        return self.__dictionaryNameList

    def getInternalDictionaryNameList(self):
        return self.__internalDictionaryNameList

    def getPdbxDictionaryNameList(self):
        return self.__pdbxDictionaryNameList

    def getPdbmlSchemaNameList(self):
        oL = ["mmcif_pdbx_v42"]
        oL.extend(self.__dictionaryNameList)
        return oL

    def get(self):
        return self.__dictInfoD

    def getTitle(self, dictionaryName):
        try:
            return self.__dictInfoD[dictionaryName]["title"]
        except Exception as e:
            logger.debug("Failing with %s", str(e))
            return None

    def getDescription(self, dictionaryName):
        try:
            return self.__dictInfoD[dictionaryName]["description"]
        except Exception as e:
            logger.debug("Failing with %s", str(e))
            return None

    def getDevelopers(self, dictionaryName):
        try:
            return self.__dictInfoD[dictionaryName]["developers"]
        except Exception as e:
            logger.debug("Failing with %s", str(e))
            return None

    def getMaintainers(self, dictionaryName):
        try:
            return self.__dictInfoD[dictionaryName]["maintainers"]
        except Exception as e:
            logger.debug("Failing with %s", str(e))
            return None

    def getSchemaName(self, dictionaryName):
        try:
            return self.__dictInfoD[dictionaryName]["schema"]
        except Exception as e:
            logger.debug("Failing with %s", str(e))
            return None
