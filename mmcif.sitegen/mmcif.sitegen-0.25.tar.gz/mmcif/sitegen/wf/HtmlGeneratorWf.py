##
# File:    HtmlGeneratorWf.py
# Author:  jdw
# Date:    29-Dec-2020
# Version: 0.001
#
# Updates:
##
"""
Workflow methods for rendering mmCIF dictionaries in HTML
"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2,0"


import logging
import os
import stat
import time

from mmcif.sitegen.dictionary import __version__
from mmcif.sitegen.dictionary.DictionaryFileUtils import DictionaryFileUtils
from mmcif.sitegen.dictionary.DictionaryItemCoverage import DictionaryItemCoverage
from mmcif.sitegen.dictionary.DictionaryRegistry import DictionaryRegistry
from mmcif.sitegen.dictionary.HtmlContentUtils import HtmlContentUtils
from mmcif.sitegen.dictionary.HtmlGenerator import HtmlGenerator
from mmcif.sitegen.dictionary.HtmlGenerator import HtmlTemplates
from mmcif.sitegen.dictionary.HtmlMarkupUtils import HtmlComponentMarkupUtils
from mmcif.sitegen.dictionary.HtmlMarkupUtils import HtmlMarkupUtils
from mmcif.sitegen.dictionary.HtmlPathInfo import HtmlPathInfo

logger = logging.getLogger(__name__)


class HtmlGeneratorWf(object):
    def __init__(self, websiteGenPath="/var/www/mmcif_website_generated", websiteFileAssetsPath="/var/www/mmcif_website_file_assets", testMode=False):
        self.__verbose = True
        self.__testMode = testMode
        # Top path for generated content
        self.__webGenPath = websiteGenPath
        #
        # Source files live in website file assets path -
        self.__webFileAssetsPath = websiteFileAssetsPath
        self.__dictTopDir = "dictionaries"
        self.__pdbxResourcePath = os.path.join(self.__webFileAssetsPath, self.__dictTopDir)
        # self.__pdbmlResourcePath = os.path.join(self.__webFileAssetsPath, "schema")
        self.__coveragePath = os.path.join(self.__webFileAssetsPath, "coverage")
        self.__registryPath = os.path.join(self.__webFileAssetsPath, "config", "mmcif_dictionary_registry.json")
        #
        self.__dR = DictionaryRegistry(self.__registryPath)
        self.__dictionaryNameList = self.__dR.getDictionaryNameList()
        self.__internalDictionaryNameList = self.__dR.getInternalDictionaryNameList()
        self.__schemaNameList = self.__dR.getPdbmlSchemaNameList()
        #
        self.__fullDictionaryNameList = []
        self.__fullDictionaryNameList.extend(self.__dictionaryNameList)
        self.__fullDictionaryNameList.extend(self.__internalDictionaryNameList)
        #
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
        """Run workflow to render dictionaries in HTML --"""
        ok = False
        try:
            ok = self.__renderDownloadList()
            for dictName in self.__fullDictionaryNameList:
                self.__logBegin(taskName=dictName)
                dictPath = os.path.join(self.__pdbxResourcePath, dictName + ".dic")
                ok = self.__makeDirectories(pathDictionary=dictPath)
                leadingGroupList = None
                if dictName == "mmcif_mdb":
                    leadingGroupList = ["mdb_group"]
                elif dictName == "mmcif_sas":
                    leadingGroupList = ["sas_group"]
                elif dictName == "mmcif_ma":
                    leadingGroupList = ["ma_group"]
                elif dictName == "mmcif_nef":
                    leadingGroupList = ["nef_group"]
                elif dictName == "mmcif_ihm":
                    leadingGroupList = ["ihm_group"]

                ok1 = self.__renderHtmlDictionary(dictionaryName=dictName, pathDictionary=dictPath, leadingGroupList=leadingGroupList)
                ok = ok1 and ok
                self.__logEnd(taskName=dictName)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
        return ok

    def __makeDirectories(self, pathDictionary):
        """Create file system structure for HTML dictionary rendering"""
        ok = False
        try:
            pI = HtmlPathInfo(dictFilePath=pathDictionary, htmlDocsPath=self.__webGenPath, htmlTopDirectoryName=self.__dictTopDir, verbose=self.__verbose)
            hg = HtmlGenerator(pathInfoObj=pI, verbose=self.__verbose)
            ok = hg.makeDirectories(purge=False)
        except Exception as e:
            logger.exception("Failing with %s", str(e))
        return ok

    def __writeAnyFile(self, title, subTitle, filePath, htmlContentList, flavor="PDBx"):
        """Render any page using common header and footer.

        Input HTML content list is inserted within the body of the page.

        """
        try:
            if self.__verbose:
                logger.debug("writing file flavor %s path %s", flavor, filePath)
            #
            pth, _ = os.path.split(filePath)
            if not os.access(pth, os.W_OK):
                os.makedirs(pth, 0o755)
            #
            ht = HtmlTemplates()
            ofh = open(filePath, "w", encoding="utf-8")
            pageTitle = str(title) + " " + str(subTitle)
            if flavor in ["PDBx"]:
                ofh.write("%s\n" % ht.getPageHeader(title=pageTitle))
            elif flavor in ["PDBML"]:
                ofh.write("%s\n" % ht.getPdbmlPageHeader(title=pageTitle))
            else:
                ofh.write("%s\n" % ht.getPageHeader(title=pageTitle))
            ofh.write("%s\n" % ht.getPageTitle(title, subTitle))
            ofh.write("%s" % "\n".join(htmlContentList))
            ofh.write("%s\n" % ht.getPageTrailer())
            ofh.close()
            st = os.stat(filePath)
            os.chmod(filePath, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            return True
        except Exception as e:
            logger.error("Failed for %s", filePath)
            logger.exception("Failing with %s", str(e))
        return False

    #
    def __makePdbxDownloadPage(self, dictionaryNameList, dictionaryInfoD, dictionaryPath="/dictionaries", schemaPath="/schema"):
        """Make the download list of PDBx dictionaries"""
        mU = HtmlMarkupUtils(verbose=self.__verbose)
        html = HtmlComponentMarkupUtils(verbose=self.__verbose)
        html.clear()
        html.beginDescriptionList(style="vertical")
        for dictionaryName in dictionaryNameList:
            dList = []
            url = os.path.join(dictionaryPath, dictionaryName + ".dic", "Index")
            dList.append(mU.getAnchor(contentUrl=url, contentLabel="Dictionary Browser  &raquo;", cssClassString=None, fmt="html"))

            url = os.path.join(dictionaryPath, "ascii", dictionaryName + ".dic")
            dList.append(mU.getAnchor(contentUrl=url, contentLabel="Dictionary Text  &raquo;", cssClassString=None, fmt="html"))

            url = os.path.join(dictionaryPath, "ascii", dictionaryName + ".dic.gz")
            dList.append(mU.getAnchor(contentUrl=url, contentLabel="Dictionary Text (gz)  &raquo;", cssClassString=None, fmt="html"))

            if dictionaryInfoD[dictionaryName]["schema"] is not None:
                url = os.path.join(schemaPath, dictionaryInfoD[dictionaryName]["schema"] + ".xsd")
                dList.append(mU.getAnchor(contentUrl=url, contentLabel="PDBML Schema  &raquo;", cssClassString=None, fmt="html"))
            #
            tS = dictionaryInfoD[dictionaryName]["title"]
            dS = dictionaryInfoD[dictionaryName]["description"] + "<br />" + "&nbsp;|&nbsp;".join(dList)
            html.addDescription(termSt=tS, descriptionSt=dS, formatTerm="html", formatDescription="html", extraSpace=True)

        html.endDescriptionList()
        return html.getHtmlList()

    def __makePdbmlDownloadPage(self, dictionaryNameList, dictionaryInfoD, dictionaryPath="/dictionaries", schemaPath="/schema"):
        """Make the download list of PDBML schema -"""
        mU = HtmlMarkupUtils(verbose=self.__verbose)
        html = HtmlComponentMarkupUtils(verbose=self.__verbose)
        html.clear()
        html.beginDescriptionList(style="vertical")
        for dictionaryName in dictionaryNameList:
            dList = []
            if dictionaryInfoD[dictionaryName]["schema"] is not None:
                url = os.path.join(schemaPath, dictionaryInfoD[dictionaryName]["schema"] + ".xsd")
                dList.append(mU.getAnchor(contentUrl=url, contentLabel="PDBML Schema  &raquo;", cssClassString=None, fmt="html"))

                if "dictionary" in dictionaryInfoD[dictionaryName]:
                    myName = dictionaryInfoD[dictionaryName]["dictionary"]
                else:
                    myName = dictionaryName

                url = os.path.join(dictionaryPath, myName + ".dic", "Index")
                dList.append(mU.getAnchor(contentUrl=url, contentLabel="Dictionary Browser  &raquo;", cssClassString=None, fmt="html"))

                url = os.path.join(dictionaryPath, "ascii", myName + ".dic")
                dList.append(mU.getAnchor(contentUrl=url, contentLabel="Dictionary Text  &raquo;", cssClassString=None, fmt="html"))

                url = os.path.join(dictionaryPath, "ascii", myName + ".dic.gz")
                dList.append(mU.getAnchor(contentUrl=url, contentLabel="Dictionary Text (gz)  &raquo;", cssClassString=None, fmt="html"))
                #
                tS = "PDBML schema for the " + dictionaryInfoD[dictionaryName]["title"]
                dS = dictionaryInfoD[dictionaryName]["description"] + "<br />" + "&nbsp;|&nbsp;".join(dList)
                html.addDescription(termSt=tS, descriptionSt=dS, formatTerm="html", formatDescription="html", extraSpace=True)

        html.endDescriptionList()
        return html.getHtmlList()

    def __renderDownloadList(self):
        """Create HTML pages for the input dictionary --"""
        ok = False
        try:
            filePath = os.path.join(self.__webGenPath, "downloads", "downloads.html")
            htmlContentList = self.__makePdbxDownloadPage(
                dictionaryNameList=self.__dictionaryNameList, dictionaryInfoD=self.__dR.get(), dictionaryPath="/dictionaries", schemaPath="/schema"
            )
            self.__writeAnyFile(title="Browse/Download ", subTitle="Dictionaries and Schema", filePath=filePath, htmlContentList=htmlContentList)
            #
            filePath = os.path.join(self.__webGenPath, "downloads", "internal-downloads.html")
            htmlContentList = self.__makePdbxDownloadPage(
                dictionaryNameList=self.__internalDictionaryNameList, dictionaryInfoD=self.__dR.get(), dictionaryPath="/dictionaries", schemaPath="/schema"
            )
            self.__writeAnyFile(title="Browse/Download ", subTitle="Internal Dictionaries and Schema", filePath=filePath, htmlContentList=htmlContentList)

            #
            filePath = os.path.join(self.__webGenPath, "downloads", "pdbml-downloads.html")
            htmlContentList = self.__makePdbmlDownloadPage(
                dictionaryNameList=self.__schemaNameList, dictionaryInfoD=self.__dR.get(), dictionaryPath="/dictionaries", schemaPath="/schema"
            )
            ok = self.__writeAnyFile(title="Browse/Download ", subTitle="PDBML Schema", filePath=filePath, htmlContentList=htmlContentList, flavor="PDBML")

        except Exception as e:
            logger.exception("Failing with %s", str(e))
        return ok

    def __renderHtmlDictionary(self, dictionaryName, pathDictionary, leadingGroupList=None):
        """Create HTML pages for the input dictionary --"""
        ok = False
        try:
            pI = HtmlPathInfo(dictFilePath=pathDictionary, htmlDocsPath=self.__webGenPath, htmlTopDirectoryName=self.__dictTopDir, verbose=self.__verbose)
            hg = HtmlGenerator(pathInfoObj=pI, verbose=self.__verbose)

            dfu = DictionaryFileUtils(dictFilePath=pathDictionary, verbose=self.__verbose)

            dApi = dfu.getApi()
            hcU = HtmlContentUtils(dictApiObj=dApi, pathInfoObj=pI, verbose=self.__verbose)
            #
            #

            dIC = DictionaryItemCoverage(self.__coveragePath)
            archiveItemNameD = dIC.getItemCoverage(deliveryType="archive")
            ccItemNameD = dIC.getItemCoverage(deliveryType="cc")
            prdItemNameD = dIC.getItemCoverage(deliveryType="prd")

            hcU.setItemCounts(archiveItemNameD, deliveryType="archive")
            hcU.setItemCounts(ccItemNameD, deliveryType="cc")
            hcU.setItemCounts(prdItemNameD, deliveryType="prd")

            try:
                tS = self.__dR.getTitle(dictionaryName=dictionaryName)
                dS = self.__dR.getDescription(dictionaryName=dictionaryName)
                aS = self.__dR.getDevelopers(dictionaryName=dictionaryName)
                mS = self.__dR.getMaintainers(dictionaryName=dictionaryName)
            except Exception as e:
                logger.warning("Missing dictionary info for %s", dictionaryName)
                tS = None
                dS = None
                aS = None
                mS = None
            downloadPath = os.path.join("/", self.__dictTopDir, "ascii")
            #
            # handle history list order -
            order = "reverse"
            if dictionaryName == "mmcif_img":
                order = "forward"
            pageHtmlList = hcU.makeDictionaryIndex(downloadPath=downloadPath, dictionaryName=dictionaryName, title=tS, description=dS, authors=aS, maintainers=mS, order=order)

            subTitle = dApi.getDictionaryTitle()
            hg.writeHtmlFile("index", title="Dictionary Index", subTitle=subTitle, contentType="Index", htmlContentList=pageHtmlList)
            #
            pageHtmlList = hcU.makeCategoryGroupIndex(leadingList=leadingGroupList)
            hg.writeHtmlFile("index", title="Category Group Index", subTitle=subTitle, contentType="Groups", htmlContentList=pageHtmlList)
            groupNameList = dApi.getCategoryGroups()
            for groupName in groupNameList:
                pageHtmlList = hcU.makeCategoryGroupPage(groupName)
                hg.writeHtmlFile(groupName, title="Category Group", subTitle=groupName, contentType="Groups", htmlContentList=pageHtmlList, navBarContentType="none")

            #
            #
            pageHtmlList = hcU.makeCategoryAlphaIndex()
            hg.writeHtmlFile("index", title="Category Index", subTitle=subTitle, contentType="Categories", htmlContentList=pageHtmlList)

            pageHtmlList = hcU.makeItemCategoryAlphaIndex(openFirst=True)
            hg.writeHtmlFile("index", title="Item Index", subTitle=subTitle, contentType="Items", htmlContentList=pageHtmlList)

            pageCount = 0
            categoryNameList = dApi.getCategoryList()
            for categoryName in categoryNameList:
                pageHtmlList = hcU.makeCategoryPage(categoryName)
                hg.writeHtmlFile(categoryName, title="Data Category", subTitle=categoryName, contentType="Categories", htmlContentList=pageHtmlList, navBarContentType="none")
                pageCount += 1
                itemNameList = dApi.getItemNameList(categoryName)
                for itemName in itemNameList:
                    pageHtmlList = hcU.makeItemPage(itemName)
                    hg.writeHtmlFile(itemName, title="Data Item", subTitle=itemName, contentType="Items", htmlContentList=pageHtmlList, navBarContentType="none")
                    pageCount += 1
            logger.debug("HTML page count %d", pageCount)
            #
            pageHtmlList = hcU.makeSupportingDataIndex()
            subTitle = dApi.getDictionaryTitle()
            ok = hg.writeHtmlFile("index", title="Supporting Data", subTitle=subTitle, contentType="Data", htmlContentList=pageHtmlList)

        except Exception as e:
            logger.exception("Failing with %s", str(e))
        return ok
