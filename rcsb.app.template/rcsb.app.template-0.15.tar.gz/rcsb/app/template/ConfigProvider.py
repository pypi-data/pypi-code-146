##
# File:    ConfigProvider.py
# Author:  jdw
# Date:    25-Aug-2020
# Version: 0.001
#
# Updates:
##
"""
Accessors for configuration details.
"""

__docformat__ = "google en"
__author__ = "John Westbrook"
__email__ = "john.westbrook@rcsb.org"
__license__ = "Apache 2.0"

import logging
import os
import time

from rcsb.utils.io.MarshalUtil import MarshalUtil
from rcsb.utils.io.SingletonClass import SingletonClass

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))

logger = logging.getLogger(__name__)


class ConfigProvider(SingletonClass):
    """Accessors for configuration details."""

    def __init__(self):
        self.__startTime = time.time()
        # ---
        self.__cachePath = os.environ.get("CACHE_PATH", os.path.abspath("./CACHE"))
        logger.info("Using CACHE_PATH setting %r", self.__cachePath)
        self.__mU = MarshalUtil(workPath=self.__cachePath)
        self.__configD = None
        self.__dataObj = None
        # ---

    def getConfig(self):
        try:
            if not self.__configD:
                self.__readConfig()
        except Exception as e:
            logger.exception("Failing with %s", str(e))
        return self.__configD

    def getData(self):
        try:
            if not self.__dataObj:
                self.__readData()
        except Exception as e:
            logger.exception("Failing with %s", str(e))
        return self.__dataObj

    def __readData(self, fileName="example-data.cif"):
        """Read example data file ...

        Returns:
            bool: True for success or False otherwise
        """
        ok = False
        try:
            dataFilePath = os.path.join(self.__cachePath, "config", fileName)
            dataObj = None
            if self.__mU.exists(dataFilePath):
                dataObjL = self.__mU.doImport(dataFilePath, fmt="mmcif")
                if dataObjL and dataObjL[0]:
                    nL = dataObjL[0].getObjNameList()
                    logger.debug("nL %r", nL)
                    ok = len(nL) >= 6
                    dataObj = dataObjL[0]
            else:
                # Handle missing config for now
                logger.warning("Reading data file fails from path %r", dataFilePath)
                ok = True
            #
            self.__dataObj = dataObj
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            ok = False
        return ok

    def __readConfig(self, fileName="example-config.json"):
        """Read example configuration file and set internal configuration dictionary

        Returns:
            bool: True for success or False otherwise
        """
        #
        ok = False
        try:
            configFilePath = os.path.join(self.__cachePath, "config", fileName)
            configD = {}
            if self.__mU.exists(configFilePath):
                configD = self.__mU.doImport(configFilePath, fmt="json")
            logger.debug("configD: %r", configD)
            if configD and (len(configD) >= 2) and float(configD["versionNumber"]) > 0.1:
                logger.info("Read version %r sections %r from %s", configD["versionNumber"], list(configD.keys()), configFilePath)
                ok = True

            else:
                # Handle missing config for now
                logger.warning("Reading config file fails from path %r", configFilePath)
                logger.warning("Using config %r", configD)
                ok = True
            #
            self.__configD = configD
        except Exception as e:
            logger.exception("Failing with %s", str(e))
            ok = False
        return ok

    def setConfig(self, cachePath, configData=None):
        """Provide bootstrap configuration options.

        Args:
            cachePath (str): path to cache data files.

        Returns:
            bool: True for success or False otherwise

        """
        self.__configD = self.__makeBootstrapDepictConfig(cachePath, configData)
        return len(self.__configD) >= 2

    def __makeBootstrapDepictConfig(self, cachePath, fileName="example-config.json", storeConfig=True, configData=None):
        """Create example configuration bootstrap file"""
        configD = {}
        try:
            cD = configData if configData else {}
            os.environ["CACHE_PATH"] = os.path.join(cachePath)
            configDirPath = os.path.join(cachePath, "config")
            configFilePath = os.path.join(configDirPath, fileName)
            logger.info("Updating example configuration using %s", configFilePath)
            #
            configD = {"versionNumber": 0.20, "data": cD}
            if storeConfig:
                self.__mU.mkdir(configDirPath)
                self.__mU.doExport(configFilePath, configD, fmt="json", indent=3)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
        return configD
        #
