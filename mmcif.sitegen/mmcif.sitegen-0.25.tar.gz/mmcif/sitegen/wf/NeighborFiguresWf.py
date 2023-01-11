##
# File:    NeighborFiguresWf.py
# Author:  jdw
# Date:    29-Dec-2020
# Version: 0.001
#
# Updates:
#
##
"""
Workflow for generating category neighbor diagram figures.
"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2,0"


import logging
import os
import time

from mmcif.sitegen.dictionary import __version__
from mmcif.sitegen.dictionary.DictionaryFileUtils import DictionaryFileUtils
from mmcif.sitegen.dictionary.DictionaryItemCoverage import DictionaryItemCoverage
from mmcif.sitegen.dictionary.DictionaryRegistry import DictionaryRegistry
from mmcif.sitegen.dictionary.HtmlGenerator import HtmlGenerator
from mmcif.sitegen.dictionary.HtmlPathInfo import HtmlPathInfo
from mmcif.sitegen.dictionary.NeighborFigures import NeighborFigures

logger = logging.getLogger(__name__)

HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))
## JDW starting on path adjustments


class NeighborFiguresWf(object):
    def __init__(self, websiteGenPath="/var/www/mmcif_website_generated", websiteFileAssetsPath="/var/www/mmcif_website_file_assets", testMode=False):
        self.__verbose = True
        self.__testMode = testMode
        #
        # site path details --
        self.__pathDot = self.__findGraphvizDot()
        # Top path for generated content
        self.__webGenPath = websiteGenPath
        #
        # Source files live in website file assets path -
        self.__webFileAssetsPath = websiteFileAssetsPath
        self.__dictTopDir = "dictionaries"
        self.__pdbxResourcePath = os.path.join(self.__webFileAssetsPath, self.__dictTopDir)
        self.__coveragePath = os.path.join(self.__webFileAssetsPath, "coverage")
        self.__registryPath = os.path.join(self.__webFileAssetsPath, "config", "mmcif_dictionary_registry.json")
        #
        self.__dR = DictionaryRegistry(self.__registryPath)
        self.__dictionaryNameList = self.__dR.getDictionaryNameList()
        self.__internalDictionaryNameList = self.__dR.getInternalDictionaryNameList()
        self.__deliveryTypeL = ["archive", "cc", "prd", "family"]
        self.__itemCountD = self.__getItemCounts(self.__deliveryTypeL)
        #
        self.__fullDictionaryNameList = []
        self.__fullDictionaryNameList.extend(self.__dictionaryNameList)
        self.__fullDictionaryNameList.extend(self.__internalDictionaryNameList)
        if self.__testMode:
            self.__fullDictionaryNameList = self.__fullDictionaryNameList[:1]

        self.__startTimeD = {}

    def __logBegin(self, taskName="task"):
        self.__startTimeD[taskName] = time.time()
        logger.info("Starting %s at %s", taskName, time.strftime("%Y %m %d %H:%M:%S", time.localtime()))

    def __logEnd(self, taskName="task"):
        endTime = time.time()
        logger.info("Completed %s at %s (%.4f seconds)", taskName, time.strftime("%Y %m %d %H:%M:%S", time.localtime()), endTime - self.__startTimeD[taskName])

    def run(self):
        """Run workflow to render of all category-level figures for current dictionary list."""
        try:
            ok = True
            for dictName in self.__fullDictionaryNameList:
                logger.info("Starting figures generation for dictionary %s", dictName)
                self.__logBegin(taskName=dictName)
                dictPath = os.path.join(self.__pdbxResourcePath, dictName + ".dic")
                pI = HtmlPathInfo(dictFilePath=dictPath, htmlDocsPath=self.__webGenPath, htmlTopDirectoryName=self.__dictTopDir, verbose=self.__verbose)
                dfu = DictionaryFileUtils(dictFilePath=dictPath, verbose=self.__verbose)
                dApi = dfu.getApi()
                self.__makeDirectories(pathInfoObj=pI, purge=False)
                categoryNameList = dApi.getCategoryList()
                figureCount = self.__makeCategoryNeighborFiguresAuto(categoryNameList=categoryNameList, dApi=dApi, pathInfoObj=pI)
                ok1 = figureCount > 0
                ok = ok1 and ok
                self.__logEnd(taskName=dictName)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
        return ok

    def __findGraphvizDot(self):
        pathDot = os.getenv("GRAPHVIZ_DOT_BINARY", default=None)
        pthList = [pathDot] if pathDot else []
        pthList.extend(["/usr/bin/dot", "/usr/local/bin/dot", "/opt/bin/dot"])
        for pth in pthList:
            if os.path.isfile(pth) and os.access(pth, os.X_OK):
                return pth
        return None

    def __getItemCounts(self, deliveryTypeL):
        itemCountD = {}
        self.__dIC = DictionaryItemCoverage(self.__coveragePath)
        for deliveryType in deliveryTypeL:
            itemCountD[deliveryType] = self.__dIC.getItemCoverage(deliveryType=deliveryType)
        for dT, cD in itemCountD.items():
            logger.debug("dT %r length %d", dT, len(cD))
        return itemCountD

    def __makeCategoryNeighborFiguresAuto(self, categoryNameList, dApi=None, pathInfoObj=None):
        """Create neighbor figures for input categories using the input dictionary api and pathInfo objects."""
        try:
            # size=".7,.7"
            size = None
            #
            nf = NeighborFigures(dictApiObj=dApi, pathInfoObj=pathInfoObj, pathDot=self.__pathDot, verbose=self.__verbose)
            for deliveryType in self.__deliveryTypeL:
                nf.setItemCounts(self.__itemCountD[deliveryType], deliveryType=deliveryType)
            #
            dictTitle = dApi.getDictionaryTitle()
            dictVersion = dApi.getDictionaryVersion()

            figureCount = 0
            for categoryName in categoryNameList:

                title = " <br/> <br/> Category Relationship Diagram for <b>%s</b> " % categoryName.upper()
                subTitle = " in dictionary %s version %s " % (dictTitle, dictVersion)
                ok = nf.makeNeighborFigure(
                    categoryName,
                    graphTitle=title,
                    graphSubTitle=subTitle,
                    titleFormat="html",
                    figFormat="svg",
                    size=size,
                    maxItems=20,
                    filterDelivery=False,
                    deliveryType="archive",
                )
                if ok:
                    figureCount += 1
                #
                title = " <br/> <br/> Abbreviated Category Relationship Diagram for <b>%s</b> " % categoryName.upper()
                subTitle = " in dictionary %s version %s <br/> including only data categories used in current PDB entries." % (dictTitle, dictVersion)
                ok = nf.makeNeighborFigure(
                    categoryName, graphTitle=title, graphSubTitle=subTitle, titleFormat="html", figFormat="svg", size=size, maxItems=20, filterDelivery=True, deliveryType="archive"
                )

                if ok:
                    figureCount += 1

                if nf.getCategoryUseCount(categoryName, deliveryType="cc") > 0:
                    title = " <br/> <br/> Abbreviated Category Relationship Diagram for <b>%s</b> " % categoryName.upper()
                    subTitle = " in dictionary %s version %s <br/> including only data categories used in the chemical reference dictionary." % (dictTitle, dictVersion)
                    ok = nf.makeNeighborFigure(
                        categoryName, graphTitle=title, graphSubTitle=subTitle, titleFormat="html", figFormat="svg", size=size, maxItems=20, filterDelivery=True, deliveryType="cc"
                    )
                    if ok:
                        figureCount += 1

                if nf.getCategoryUseCount(categoryName, deliveryType="prd") > 0:
                    title = " <br/> <br/> Abbreviated Category Relationship Diagram for <b>%s</b> " % categoryName.upper()
                    subTitle = " in dictionary %s version %s <br/> including only data categories used in the BIRD reference dictionary." % (dictTitle, dictVersion)
                    ok = nf.makeNeighborFigure(
                        categoryName, graphTitle=title, graphSubTitle=subTitle, titleFormat="html", figFormat="svg", size=size, maxItems=20, filterDelivery=True, deliveryType="prd"
                    )
                    if ok:
                        figureCount += 1

                if nf.getCategoryUseCount(categoryName, deliveryType="family") > 0:
                    title = " <br/> <br/> Abbreviated Category Relationship Diagram for <b>%s</b> " % categoryName.upper()
                    subTitle = " in dictionary %s version %s <br/> including only data categories used in the BIRD family reference dictionary." % (dictTitle, dictVersion)
                    ok = nf.makeNeighborFigure(
                        categoryName,
                        graphTitle=title,
                        graphSubTitle=subTitle,
                        titleFormat="html",
                        figFormat="svg",
                        size=size,
                        maxItems=20,
                        filterDelivery=True,
                        deliveryType="family",
                    )
                    if ok:
                        figureCount += 1

            logger.debug("%s category count %d figure count %d", dictTitle, len(categoryNameList), figureCount)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
        return figureCount

    def __makeDirectories(self, pathInfoObj=None, purge=True):
        """Create file system structure for HTML dictionary rendering"""
        ok = False
        try:
            hg = HtmlGenerator(pathInfoObj=pathInfoObj, verbose=self.__verbose)
            ok = hg.makeDirectories(purge=purge)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
        return ok
