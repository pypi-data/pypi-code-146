##
# File:    HtmlContentUtils.py
# Author:  J. Westbrook
# Date:    2-Sep-2013
# Version: 0.001
#
# Updates:
#    8-Oct-2013  -  Reorder category page sections --
#   29-Dec-2020  -  Cleanup and py39
##
# pylint: disable=too-many-lines
"""
Utility methods for extracting content require for HTML rendering.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2,0"

import logging
import os

from mmcif.api.PdbxContainers import CifName

from mmcif.sitegen.dictionary.HtmlMarkupUtils import HtmlComponentMarkupUtils
from mmcif.sitegen.dictionary.HtmlMarkupUtils import HtmlMarkupUtils

logger = logging.getLogger(__name__)


class HtmlContentUtils(object):
    """Utility methods for extracting content require for HTML rendering."""

    def __init__(self, dictApiObj, pathInfoObj=None, verbose=False):
        """"""
        self.__verbose = verbose
        self.__debug = False
        self.__dApi = dictApiObj
        self.__pI = pathInfoObj
        self.__html = HtmlComponentMarkupUtils(verbose=self.__verbose)
        self.__mU = HtmlMarkupUtils(verbose=self.__verbose)

        self.__glyphPathKey = "/assets/images/glyphicons-dot-com/png/glyphicons_044_keys.png"
        self.__glyphPathBang = "/assets/images/glyphicons-dot-com/png/glyphicons_196_circle_exclamation_mark.png"
        self.__glyphPathUserInput = "/assets/images/glyphicons-dot-com/png/glyphicons_006_user_add.png"
        self.__glyphPathInfo = "/assets/images/glyphicons-dot-com/png/glyphicons_195_circle_info.png"
        self.__glyphPathDatabase = "/assets/images/glyphicons-dot-com/png/glyphicons_141_database_plus.png"
        self.__glyphPathCoffee = "/assets/images/glyphicons-dot-com/png/glyphicons_294_coffe_cup.png"
        self.__glyphPathLink = "/assets/images/glyphicons-dot-com/png/glyphicons_050_link.png"
        self.__glyphPathBookOpen = "/assets/images/glyphicons-dot-com/png/glyphicons_351_book_open.png"
        self.__glyphPathBook = "/assets/images/glyphicons-dot-com/png/glyphicons_071_book.png"
        self.__glyphPathDownload = "/assets/images/glyphicons-dot-com/png/glyphicons_181_download_alt.png"
        self.__glyphPathQuestionMark = "/assets/images/glyphicons-dot-com/png/glyphicons_194_circle_question_mark.png"
        self.__glyphPathRegex = "/assets/images/misc/regex-35.png"
        self.__glyphPathDiagram = "/assets/images/glyphicons-dot-com/png/glyphicons_138_picture.png"
        self.__glyphPathParent = "/assets/images/misc/parent-child-40.png"

        self.__itemCounts = {"archive": {}, "prd": {}, "cc": {}}
        self.__categoryCounts = {"archive": {}, "prd": {}, "cc": {}}

    def setItemCounts(self, itemNameD, deliveryType="archive"):
        for itemName, itemCount in itemNameD.items():
            self.__itemCounts[deliveryType][itemName] = itemCount
            categoryName = CifName.categoryPart(itemName)
            if categoryName not in self.__categoryCounts[deliveryType]:
                self.__categoryCounts[deliveryType][categoryName] = itemCount
            else:
                self.__categoryCounts[deliveryType][categoryName] = max(itemCount, self.__categoryCounts[deliveryType][categoryName])

        logger.debug("items      in archive count %d", len(self.__itemCounts[deliveryType]))
        logger.debug("categories in archive count %d", len(self.__categoryCounts[deliveryType]))

    def __isCategoryUsed(self, categoryName, deliveryType="archive"):
        if categoryName in self.__categoryCounts[deliveryType]:
            return True
        else:
            return False

    def __getItemCount(self, itemName, deliveryType="archive"):
        if itemName in self.__itemCounts[deliveryType]:
            return self.__itemCounts[deliveryType][itemName]
        else:
            return 0

    def __getCategoryUsePercent(self, categoryName, deliveryType="archive"):
        if categoryName in self.__categoryCounts[deliveryType]:
            denom = self.__itemCounts[deliveryType]["_entry.id"]
            pc = 100.0 * float(self.__categoryCounts[deliveryType][categoryName]) / float(denom)

            if pc > 0.10:
                return "%5.1f" % (pc)
            elif pc > 0.01:
                return "%5.2f" % (pc)
            else:
                return "%6.3f" % (pc)
        else:
            return "0.0"

    def __getItemUsePercent(self, itemName, deliveryType="archive"):
        if itemName in self.__itemCounts[deliveryType]:
            denom = self.__itemCounts[deliveryType]["_entry.id"]
            pc = 100.0 * float(self.__itemCounts[deliveryType][itemName]) / float(denom)
            if pc > 0.10:
                return "%5.1f" % (pc)
            elif pc > 0.01:
                return "%5.2f" % (pc)
            else:
                return "%6.3f" % (pc)
        else:
            return "0.0"

    def __renderTable(self, rowList, columnNameList, newLines="verbatim", columnNameFormat="html", dataFormat="ascii", markupMath=False):
        html = HtmlComponentMarkupUtils(verbose=self.__verbose)
        html.clear()
        html.beginTable(columnNameList=columnNameList, fmt=columnNameFormat)
        for row in rowList:
            html.addTableRow(rowValueList=row, fmt=dataFormat, newLines=newLines, markupMath=markupMath)

        html.endTable()
        return html.getHtmlList()

    def makeDictionaryIndex(self, downloadPath, dictionaryName, title=None, description=None, authors=None, maintainers=None, order="reverse"):
        """Render the main dictionary index page -"""
        dictName = self.__dApi.getDictionaryTitle()
        dictVersion = self.__dApi.getDictionaryVersion()

        # revisionCount = self.__dApi.getDictionaryRevisionCount()

        revisionDate = self.__dApi.getDictionaryUpdate(order=order)
        historyList = self.__dApi.getDictionaryHistory(order=order)
        #
        historyHtmlList = self.__renderTable(
            rowList=historyList, columnNameList=["Version", "Revision&nbsp;Date", "Revision&nbsp;Description"], columnNameFormat="html", dataFormat="ascii"
        )
        #
        self.__html.clear()

        self.__html.beginContainer(cType="row")
        iconText, addClass = self.__getIconAnchorAndClass(contentIconType="general", cssClass="pull-right")
        self.__html.beginPanel("General " + iconText, style="panel-default " + addClass, fmt="html")
        # self.__html.beginContainer()
        #
        self.__html.beginDescriptionList()
        if title is not None:
            self.__html.addDescription(termSt="Dictionary title", descriptionSt=title)
        if description is not None:
            self.__html.addDescription(termSt="Dictionary description", descriptionSt=description)
        if authors is not None:
            self.__html.addDescription(termSt="Original developers", descriptionSt=authors)
        if maintainers is not None:
            self.__html.addDescription(termSt="Dictionary maintainers", descriptionSt=maintainers)
        #
        self.__html.addDescription(termSt="Dictionary name", descriptionSt=dictName)
        self.__html.addDescription(termSt="Dictionary version", descriptionSt=dictVersion)
        self.__html.addDescription(termSt="Last update", descriptionSt=revisionDate)
        self.__html.endDescriptionList()
        #
        # self.__html.endContainer()
        self.__html.endPanel()
        self.__html.endContainer()
        #
        # Downloads -
        #
        self.__html.beginContainer(cType="row")
        iconText, addClass = self.__getIconAnchorAndClass(contentIconType="download", cssClass="pull-right")
        self.__html.beginPanel("Downloads " + iconText, style="panel-default " + addClass, fmt="html")
        self.__html.beginContainer(cType="col-md-10 col-md-offset-1")
        dList = []
        downloadClass = "btn-lg btn-wwpdb-green"
        url = os.path.join(downloadPath, dictionaryName + ".dic")
        dList.append(self.__mU.getButtonAnchor(contentLabel="Dictionary Text", url=url, fmt="ascii", cssClassAdd=downloadClass))

        url = os.path.join(downloadPath, dictionaryName + ".dic.gz")
        dList.append(self.__mU.getButtonAnchor(contentLabel="Dictionary Text (gz)", url=url, fmt="ascii", cssClassAdd=downloadClass))
        #
        # JDW 23-Sep-2013   Naming differences here --
        # url=os.path.join(downloadPath,dictionaryName+'.xsd')
        # dList.append(self.__mU.getButtonAnchor(contentLabel="PDBML Schema",url=url,format="ascii",cssClassAdd=downloadClass))
        # url=os.path.join(downloadPath,dictionaryName+'.xsd.gz')
        # dList.append(self.__mU.getButtonAnchor(contentLabel="PDBML Schema (gz)",url=url,format="ascii",cssClassAdd=downloadClass))
        #
        self.__html.addContent(dList)
        self.__html.endContainer()
        self.__html.endPanel()
        self.__html.endContainer()
        #
        #
        self.__html.beginContainer()
        self.__html.beginAccordionPanelGroup(panelGroupId="pg1")
        self.__html.addAccordionPanel(
            title="Dictionary Revision History", panelTextList=historyHtmlList, panelId="p1", panelGroupId="pg1", openFlag=True, toggleText="View/Hide revision history list"
        )
        self.__html.endAccordionPanelGroup()
        self.__html.endContainer()

        return self.__html.getHtmlList()

    def makeSupportingDataIndex(self):
        """Render the supporting data index page ---"""
        #
        self.__html.clear()
        #
        self.__html.beginContainer()
        self.__html.beginAccordionPanelGroup(panelGroupId="pg1")
        #
        rowList = self.__dApi.getDictionaryHistory(order="reverse")
        htmlList = self.__renderTable(rowList=rowList, columnNameList=["Version", "Revision&nbsp;Date", "Revision&nbsp;Description"], columnNameFormat="html", dataFormat="ascii")
        self.__html.addAccordionPanel(
            title="Dictionary Revision History", panelTextList=htmlList, panelId="sdp1", panelGroupId="pg1", openFlag=False, toggleText="View/Hide revision history list"
        )

        #
        rowList = self.__dApi.getDataTypeList()
        htmlList = self.__renderTable(
            rowList=rowList,
            columnNameList=["Data&nbsp;Type&nbsp;Code", "Primitive&nbsp;Type&nbsp;Code", "Regular&nbsp;Expression", "Description"],
            columnNameFormat="html",
            dataFormat="ascii",
        )
        self.__html.addAccordionPanel(title="Data Type List", panelTextList=htmlList, panelId="sdp2", panelGroupId="pg1", openFlag=False, toggleText="View/Hide data type list")

        rowList = self.__dApi.getSubCategoryList()
        htmlList = self.__renderTable(rowList=rowList, columnNameList=["SubCategory&nbsp;Identifier", "Description"], columnNameFormat="html", dataFormat="ascii")
        self.__html.addAccordionPanel(title="SubCategory List", panelTextList=htmlList, panelId="sdp3", panelGroupId="pg1", openFlag=False, toggleText="View/Hide subcategory list")

        rowList = self.__dApi.getUnitsList()
        htmlList = self.__renderTable(rowList=rowList, columnNameList=["Units&nbsp;Identifier", "Description"], columnNameFormat="html", dataFormat="ascii", markupMath=True)
        self.__html.addAccordionPanel(title="Units List", panelTextList=htmlList, panelId="sdp4", panelGroupId="pg1", openFlag=False, toggleText="View/Hide units list")

        rowList = self.__dApi.getUnitsConversionList()
        htmlList = self.__renderTable(
            rowList=rowList,
            columnNameList=["From&nbsp;Units&Identifier", "To&nbsp;Units&Identifier", "Operator", "Conversion&nbsp;Factor"],
            columnNameFormat="html",
            dataFormat="ascii",
        )
        self.__html.addAccordionPanel(
            title="Units Conversion List", panelTextList=htmlList, panelId="sdp5", panelGroupId="pg1", openFlag=False, toggleText="View/Hide units conversion list"
        )

        #
        self.__html.endAccordionPanelGroup()
        self.__html.endContainer()

        return self.__html.getHtmlList()

    def __renderLinkGroup(self, contentNameList, contentType):
        html = HtmlComponentMarkupUtils(verbose=self.__verbose)
        html.clear()
        html.beginLinkListGroup()
        for contentName in contentNameList:
            linkUrl = self.__pI.getContentTypeObjUrl(contentObjName=contentName, contentType=contentType)
            html.addLinkListItem(linkUrl, contentName, fmt="ascii", active=False)
        html.endLinkListGroup()
        return html.getHtmlList()

    def __getIconAnchorAndClass(self, contentIconType, cssClass="pull-right"):
        #
        _ = cssClass
        if contentIconType in ["key", "key+database", "key+chem-dict", "key+bird-dict"]:
            iconText = self.__mU.getGlyphAnchor(tipText="Category key item", glyphPath=self.__glyphPathKey)
            addClass = "key-item"
        elif contentIconType in ["default", "default+database", "default+chem-dict", "default+bird-dict"]:
            iconText = self.__mU.getGlyphAnchor(tipText="Additional information", glyphPath=self.__glyphPathInfo)
            addClass = "default"
        elif contentIconType in ["download", "download+database", "download+chem-dict", "download+bird-dict"]:
            iconText = self.__mU.getGlyphAnchor(tipText="Download options", glyphPath=self.__glyphPathDownload)
            addClass = "default"
        elif contentIconType in ["help", "help+database", "help+chem-dict", "help+bird-dict"]:
            iconText = self.__mU.getGlyphAnchor(tipText="Additional help information", glyphPath=self.__glyphPathQuestionMark)
            addClass = "default"
        elif contentIconType in ["general", "general+database", "general+chem-dict", "general+bird-dict"]:
            # iconText=self.__mU.getGlyphAnchor(tipText="General information",glyphPath=self.__glyphPathCoffee)
            iconText = self.__mU.getGlyphAnchor(tipText="General information", glyphPath=self.__glyphPathInfo)
            addClass = "general"
        elif contentIconType in ["mandatory", "mandatory+database", "mandatory+chem-dict", "mandatory+bird-dict"]:
            iconText = self.__mU.getGlyphAnchor(tipText="Mandatory data item", glyphPath=self.__glyphPathBang)
            addClass = "mandatory-item"
        elif contentIconType in ["info", "info+database", "info+chem-dict", "info+bird-dict"]:
            iconText = self.__mU.getGlyphAnchor(tipText="Descriptive information", glyphPath=self.__glyphPathInfo)
            addClass = "info"
        elif contentIconType in ["deposit-info", "deposit-info+database", "deposit-info+chem-dict", "deposit-info+bird-dict"]:
            iconText = self.__mU.getGlyphAnchor(tipText="Descriptive information", glyphPath=self.__glyphPathInfo)
            addClass = "deposit-description"
        elif contentIconType in ["deposit-mandatory", "deposit-mandatory+database", "deposit-mandatory+chem-dict", "deposit-mandatory+bird-dict"]:
            iconText = self.__mU.getGlyphAnchor(tipText="Required data item for deposition of new entries", glyphPath=self.__glyphPathUserInput)
            addClass = "mandatory-item"
        elif contentIconType in ["regex", "regex+database", "regex+chem-dict", "regex+bird-dict"]:
            iconText = self.__mU.getGlyphAnchor(tipText="Data type information", glyphPath=self.__glyphPathRegex, imageCssClass="my-image-glyph-margin")
            addClass = "regex-item"
        elif contentIconType in ["category-image"]:
            iconText = self.__mU.getGlyphAnchor(tipText="Category relationship diagram", glyphPath=self.__glyphPathDiagram, imageCssClass="my-image-glyph-margin")
            addClass = "image-item"
        elif contentIconType in ["parent-child", "parent-child+database", "parent-child+chem-dict", "parent-child+bird-dict"]:
            iconText = self.__mU.getGlyphAnchor(tipText="Parent-child data item relationships", glyphPath=self.__glyphPathParent, imageCssClass="my-image-glyph-margin")
            addClass = "parent-child-item"
        elif contentIconType in ["related-item", "related-item+database", "related-item+chem-dict", "related-item+bird-dict"]:
            iconText = self.__mU.getGlyphAnchor(tipText="Related and dependent data items", glyphPath=self.__glyphPathLink, imageCssClass="my-image-glyph-margin")
            addClass = "related-item"
        elif contentIconType in ["all-mandatory", "all-mandatory+database", "all-mandatory+chem-dict", "all-mandatory+bird-dict"]:
            iconText = self.__mU.getGlyphAnchor(tipText="Required data item for archive entries", glyphPath=self.__glyphPathBang)
            iconText += self.__mU.getGlyphAnchor(tipText="Required data item deposition of new entries", glyphPath=self.__glyphPathUserInput)
            addClass = "mandatory-item"
        else:
            iconText = ""
            addClass = ""
        #
        if "+database" in contentIconType:
            iconText = self.__mU.getGlyphAnchor(tipText="Used in current PDB entries", glyphPath=self.__glyphPathDatabase) + iconText
            if len(addClass) < 1:
                addClass = "in-archive-item"

        if "+chem-dict" in contentIconType:
            iconText = self.__mU.getGlyphAnchor(tipText="Used in the Chemical Component Reference Dictionary", glyphPath=self.__glyphPathBookOpen) + iconText
            if len(addClass) < 1:
                addClass = "in-ref-chem-dict-item"

        if "+bird-dict" in contentIconType:
            iconText = self.__mU.getGlyphAnchor(tipText="Used in the BIRD Reference Dictionary", glyphPath=self.__glyphPathBookOpen) + iconText
            if len(addClass) < 1:
                addClass = "in-ref-bird-dict-item"

        return iconText, addClass

    def __renderLinkGroupWithIcons(self, contentNameList, contentIconTypeList=None, contentType="Items"):
        """"""
        if contentIconTypeList is None:
            contentIconTypeList = ["none" for c in contentNameList]
        html = HtmlComponentMarkupUtils(verbose=self.__verbose)
        html.clear()
        html.beginListGroup()
        for contentName, contentIconType in zip(contentNameList, contentIconTypeList):
            linkUrl = self.__pI.getContentTypeObjUrl(contentObjName=contentName, contentType=contentType)
            linkAnchor = self.__mU.getAnchor(contentUrl=linkUrl, contentLabel=contentName, cssClassString=None, fmt="ascii")
            iconText, addClass = self.__getIconAnchorAndClass(contentIconType=contentIconType, cssClass="pull-right")
            listValue = linkAnchor + iconText
            html.addListItem(listValue, fmt="html", active=False, cssClass=addClass)
        html.endListGroup()
        return html.getHtmlList()

    def makeCategoryGroupPage(self, groupName):
        """Render the category group page -"""
        self.__html.clear()
        self.__html.beginContainer()
        #
        pId = 0
        descriptionS = self.__dApi.getCategoryGroupDescription(groupName)
        catNameList = self.__dApi.getCategoryGroupCategories(groupName)
        if len(catNameList) > 0:
            pId += 1
            pIdS = "p" + str(pId)
            openF = True
            iconTypeList = self.__assignCategoryIconType(catNameList)
            catHtmlList = self.__renderLinkGroupWithIcons(catNameList, iconTypeList, contentType="Categories")
            self.__html.addAccordionPanel(
                title=groupName,
                subTitle=descriptionS,
                panelTextList=catHtmlList,
                panelId=pIdS,
                panelGroupId="pg1",
                openFlag=openF,
                toggleText="View/Hide category list",
                topId=groupName,
            )
        self.__html.endContainer()
        return self.__html.getHtmlList()

    def makeCategoryGroupIndex(self, openFirst=True, leadingList=None):
        """Render the category group index page - Each category group expand to a list of categories."""
        gList = self.__dApi.getCategoryGroups()
        if leadingList is not None:
            groupNameList = []
            for grp in leadingList:
                groupNameList.append(grp)
            for grp in gList:
                if grp in leadingList:
                    continue
                groupNameList.append(grp)
        else:
            groupNameList = gList
        #
        self.__html.clear()
        self.__html.beginContainer()
        #
        self.__html.beginAccordionPanelGroup(panelGroupId="pg1")
        pId = 0
        ii = 0
        for groupName in groupNameList:
            descriptionS = self.__dApi.getCategoryGroupDescription(groupName)
            catNameList = self.__dApi.getCategoryGroupCategories(groupName)
            if len(catNameList) > 0:
                pId += 1
                pIdS = "p" + str(pId)
                #
                if openFirst and ii == 0:
                    openF = True
                else:
                    openF = False

                iconTypeList = self.__assignCategoryIconType(catNameList)
                catHtmlList = self.__renderLinkGroupWithIcons(catNameList, iconTypeList, contentType="Categories")
                self.__html.addAccordionPanel(
                    title=groupName,
                    subTitle=descriptionS,
                    panelTextList=catHtmlList,
                    panelId=pIdS,
                    panelGroupId="pg1",
                    openFlag=openF,
                    toggleText="View/Hide category list",
                    topId=groupName,
                )
                ii += 1

        self.__html.endAccordionPanelGroup()
        self.__html.endContainer()
        #
        return self.__html.getHtmlList()

    def __assignItemIconType(self, itemNameList):
        iconTypeList = []
        #
        categoryName = CifName.categoryPart(itemNameList[0])
        keyItemNameList = self.__dApi.getCategoryKeyList(categoryName)
        for itemName in itemNameList:
            tType = "none"
            attributeName = CifName.attributePart(itemName)
            aMan = self.__dApi.getMandatoryCode(categoryName, attributeName) in ["yes", "y"]
            dMan = self.__dApi.getMandatoryCodeAlt(categoryName, attributeName, fallBack=False) in ["yes", "y"]
            inArchive = self.__getItemCount(itemName, deliveryType="archive") > 0
            inChemDict = self.__getItemCount(itemName, deliveryType="cc") > 0
            inBirdDict = self.__getItemCount(itemName, deliveryType="prd") > 0

            isKey = itemName in keyItemNameList
            if isKey:
                tType = "key"
            elif aMan and dMan:
                tType = "all-mandatory"
            elif aMan:
                tType = "mandatory"
            elif dMan:
                tType = "deposit-mandatory"
            if inArchive:
                tType += "+database"
            if inChemDict:
                tType += "+chem-dict"
            if inBirdDict:
                tType += "+bird-dict"

            iconTypeList.append(tType)

        return iconTypeList

    def __assignCategoryIconType(self, categoryNameList):
        iconTypeList = []
        #
        for categoryName in categoryNameList:
            tType = "none"
            cMan = self.__dApi.getCategoryMandatoryCode(categoryName) in ["yes", "y"]
            inArchive = self.__isCategoryUsed(categoryName, deliveryType="archive")
            inChemDict = self.__isCategoryUsed(categoryName, deliveryType="cc")
            inBirdDict = self.__isCategoryUsed(categoryName, deliveryType="prd")
            if cMan:
                tType = "mandatory"
            if inArchive:
                tType += "+database"
            if inChemDict:
                tType += "+chem-dict"
            if inBirdDict:
                tType += "+bird-dict"

            iconTypeList.append(tType)

        return iconTypeList

    def __getOrderedItemNameList(self, categoryName):
        tList = sorted(self.__dApi.getItemNameList(categoryName))
        keyItemNameList = sorted(self.__dApi.getCategoryKeyList(categoryName))
        for keyItemName in keyItemNameList:
            if keyItemName in tList:
                tList.remove(keyItemName)
            else:
                logger.debug("Category %s is missing key definition for %s", categoryName, keyItemName)
        itemNameList = []
        itemNameList.extend(keyItemNameList)
        itemNameList.extend(tList)
        return itemNameList

    def __renderItemLinkList(self, categoryName):
        htmlList = []
        itemNameList = self.__getOrderedItemNameList(categoryName)
        if len(itemNameList) > 0:
            iconTypeList = self.__assignItemIconType(itemNameList)
            htmlList = self.__renderLinkGroupWithIcons(itemNameList, iconTypeList, contentType="Items")
        return len(itemNameList), htmlList

    def makeItemCategoryIndex(self, openFirst=True):
        """Render the item & category index page. For the item index the 'openFirst' argument can be used to open
        the first accordion component exposing the list of data items within the category.
        """
        catNameList = self.__dApi.getCategoryList()

        #
        self.__html.clear()
        self.__html.beginContainer()
        #
        self.__html.beginAccordionPanelGroup(panelGroupId="pg1")
        pId = 0
        for ii, catName in enumerate(catNameList):
            itemCount, htmlList = self.__renderItemLinkList(catName)
            pId += 1
            pIdS = "p" + str(pId)

            categoryUrl = self.__pI.getContentTypeObjUrl(contentObjName=catName, contentType="Categories")
            categoryTitle = self.__mU.getAnchor(contentUrl=categoryUrl, contentLabel=catName, cssClassString="my-link-color", fmt="ascii")
            if openFirst and ii == 0:
                openF = True
            else:
                openF = False

            subTitle = "Items " + self.__mU.getBadge(itemCount)
            self.__html.addAccordionPanel(
                title=categoryTitle, subTitle=subTitle, panelTextList=htmlList, panelId=pIdS, panelGroupId="pg1", openFlag=openF, toggleText="Item list view/hide"
            )

        self.__html.endAccordionPanelGroup()
        self.__html.endContainer()
        #

        return self.__html.getHtmlList()

    def __makeItemCategoryIndex(self, categoryNameList, pgId="cita", openFirst=False):
        """Render a related list of categories with expandable item lists. For the item index the 'openFirst' argument can be used to open
        the first accordion component exposing the list of data items within the category.

        pgId - should be a unique id on the target page.
        """
        #
        idPrefix = pgId
        html = HtmlComponentMarkupUtils(verbose=self.__verbose)
        html.beginContainer(cType="col-md-10 col-md-offset-1")
        #
        html.beginAccordionPanelGroup(panelGroupId=pgId)

        for ii, categoryName in enumerate(categoryNameList):
            itemCount, htmlList = self.__renderItemLinkList(categoryName)
            pIdS = idPrefix + str(ii + 1)
            categoryUrl = self.__pI.getContentTypeObjUrl(contentObjName=categoryName, contentType="Categories")
            categoryTitle = self.__mU.getAnchor(contentUrl=categoryUrl, contentLabel=categoryName, cssClassString="my-link-color", fmt="ascii")
            if openFirst and ii == 0:
                openF = True
            else:
                openF = False
            subTitle = "Items " + self.__mU.getBadge(itemCount)

            html.addAccordionPanel(title=categoryTitle, subTitle=subTitle, panelTextList=htmlList, panelId=pIdS, panelGroupId=pgId, openFlag=openF, toggleText="Item list view/hide")

        html.endAccordionPanelGroup()
        html.endContainer()
        #
        return html.getHtmlList()

    def makeItemCategoryAlphaIndex(self, openFirst=False):
        """Embed the categories in another accordion group.

        Render the item & category index page. For the item index the 'openFirst' argument can be used to open
            the first accordion component exposing the list of data items within the category.
        """
        idPrefix = "alIdA"
        pgId = idPrefix
        #
        # Organize categories by leading character ...
        #
        catNameListFull = self.__dApi.getCategoryList()
        cIdx = {}
        for catName in catNameListFull:
            aC = catName[0]
            if aC not in cIdx:
                cIdx[aC] = []
            cIdx[aC].append(catName)
        #
        self.__html.clear()
        self.__html.beginContainer()
        self.__html.beginAccordionPanelGroup(panelGroupId=pgId)
        #

        #
        cKeys = sorted(cIdx.keys())
        for ii, cN in enumerate(cKeys):
            abbrevNameList = cIdx[cN]
            pIdS = idPrefix + str(ii + 1)
            pgIdS = idPrefix + cN + str(ii + 1)

            # top of the alpha index A, B, C --
            htmlList = self.__makeItemCategoryIndex(categoryNameList=abbrevNameList, pgId=pgIdS, openFirst=False)

            if openFirst and ii == 0:
                openF = True
            else:
                openF = False

            subTitle = "Categories " + self.__mU.getBadge(len(abbrevNameList))
            title = self.__mU.getIndexTitle(cN.upper())
            self.__html.addAccordionPanel(title=title, subTitle=subTitle, panelTextList=htmlList, panelId=pIdS, panelGroupId=pgId, openFlag=openF, toggleText="Category list view/hide")

        self.__html.endAccordionPanelGroup()
        self.__html.endContainer()
        #

        return self.__html.getHtmlList()

    def makeCategoryAlphaIndex(self, openFirst=True):
        """Embed the categories in another accordion group.

        Render the item & category index page. For the item index the 'openFirst' argument can be used to open
            the first accordion component exposing the list of data items within the category.
        """
        idPrefix = "alIdA"
        pgId = idPrefix
        #
        # Organize categories by leading character ...
        #
        catNameListFull = self.__dApi.getCategoryList()
        cIdx = {}
        for catName in catNameListFull:
            aC = catName[0]
            if aC not in cIdx:
                cIdx[aC] = []
            cIdx[aC].append(catName)
        #
        self.__html.clear()
        self.__html.beginContainer()
        self.__html.beginAccordionPanelGroup(panelGroupId=pgId)
        #
        cKeys = sorted(cIdx.keys())
        for ii, cN in enumerate(cKeys):
            abbrevNameList = cIdx[cN]
            pIdS = idPrefix + str(ii + 1)
            # pgIdS = idPrefix + cN + str(ii + 1)

            # top of the alpha index A, B, C --
            iconTypeList = self.__assignCategoryIconType(abbrevNameList)
            htmlList = self.__renderLinkGroupWithIcons(abbrevNameList, iconTypeList, contentType="Categories")

            if openFirst and ii == 0:
                openF = True
            else:
                openF = False

            subTitle = "Categories " + self.__mU.getBadge(len(abbrevNameList))
            title = self.__mU.getIndexTitle(cN.upper())
            self.__html.addAccordionPanel(title=title, subTitle=subTitle, panelTextList=htmlList, panelId=pIdS, panelGroupId=pgId, openFlag=openF, toggleText="Category list view/hide")

        self.__html.endAccordionPanelGroup()
        self.__html.endContainer()
        #

        return self.__html.getHtmlList()

    def makeCategoryIndex(self):
        """Render the category index page -"""
        catNameList = self.__dApi.getCategoryList()
        #

        #
        self.__html.clear()
        self.__html.beginContainer()
        #
        self.__html.beginLinkListGroup()

        for catName in catNameList:
            linkUrl = self.__pI.getContentTypeObjUrl(contentObjName=catName, contentType="Categories")
            self.__html.addLinkListItem(linkUrl, catName, fmt="ascii", active=False)
        self.__html.endLinkListGroup()
        self.__html.endContainer()
        #
        return self.__html.getHtmlList()

    def __notNull(self, cifString):
        if cifString is None or len(cifString) == 0 or cifString in [".", "?"]:
            return False
        else:
            return True

    def __contentPanelList(self, panelTitle, idPrefix, contentList):
        """Collection of collaspable examples in a static panel. First collapsable example is left open."""
        html = HtmlComponentMarkupUtils(verbose=self.__verbose)
        html.beginPanel(panelTitle)
        for ii, eTup in enumerate(contentList):
            pId = idPrefix + str(ii + 1)
            pgIdI = idPrefix + "g" + str(ii + 1)
            ht = self.__mU.getFormatted(eTup[0], wrapper="pre", fmt="none")
            if ii == 0:
                opF = True
            else:
                opF = False
            html.addAccordionPanel(
                title=panelTitle + str(ii + 1), subTitle=None, panelTextList=[ht], panelId=pId, panelGroupId=pgIdI, openFlag=opF, toggleText="View/Hide " + panelTitle
            )
        html.endPanel()
        return html.getHtmlList()

    def __contentPanelListAlt(self, panelTitle, subPanelTitle, idPrefix, contentList):
        """Collapsable outer panel encapsulates examples in collapsable panels."""
        #
        # Render the individual examples in sub-panels  -
        #
        html = HtmlComponentMarkupUtils(verbose=self.__verbose)
        for ii, eTup in enumerate(contentList):
            pId = idPrefix + str(ii + 1)
            pgIdI = idPrefix + "g" + str(ii + 1)
            ht = self.__mU.getFormatted(eTup[0], wrapper="pre", fmt="none")
            if ii == 0:
                opF = True
            else:
                opF = False
            html.addAccordionPanel(
                title=subPanelTitle + str(ii + 1), subTitle=None, panelTextList=[ht], panelId=pId, panelGroupId=pgIdI, openFlag=opF, toggleText="View/Hide " + subPanelTitle
            )

        hL = html.getHtmlList()
        html.clear()

        # Insert the individual examples into an enclosing collapsable panel --
        #
        pId = idPrefix + str(0)
        pgIdI = idPrefix + "g" + str(0)
        #
        subTitle = self.__mU.getBadge(len(contentList))
        html.beginAccordionPanelGroup(panelGroupId=pgIdI)
        html.addAccordionPanel(title=panelTitle, subTitle=subTitle, panelTextList=hL, panelId=pId, panelGroupId=pgIdI, openFlag=True, toggleText="View/hide " + panelTitle)
        html.endAccordionPanelGroup()
        return html.getHtmlList()

    def __renderExamples(self, exampleList, titleSingle, titleMulti, idSuffix="a"):
        exCount = len(exampleList)
        pgId = "pgex" + idSuffix
        pId = "pcex" + idSuffix
        html = HtmlComponentMarkupUtils(verbose=self.__verbose)
        if exCount > 0:
            if exCount > 1:
                ht = self.__contentPanelListAlt(panelTitle=titleMulti, subPanelTitle=titleSingle, idPrefix=pId, contentList=exampleList)
                html.addContent(ht)
            else:
                eTup = exampleList[0]
                ht = self.__mU.getFormatted(eTup[0], wrapper="pre", fmt="none")
                html.addAccordionPanel(title=titleSingle, subTitle=None, panelTextList=[ht], panelId=pId, panelGroupId=pgId, openFlag=True, toggleText="View/hide Example")
        return html.getHtmlList()

    def __addCategoryFigures(self, categoryName):
        #
        imgDirUrl = self.__pI.getDictCategoryImageDirUrl()
        imgDirPath = self.__pI.getDictCategoryImagePath()
        imgCount = 0

        imgFilePath = os.path.join(imgDirPath, categoryName + "_neighbors.svg")
        okFull = os.access(imgFilePath, os.F_OK)
        if okFull:
            imgCount += 1
        imgFilePath = os.path.join(imgDirPath, categoryName + "_neighbors_archive.svg")
        okAbbrev = os.access(imgFilePath, os.F_OK)
        if okAbbrev:
            imgCount += 1

        imgFilePath = os.path.join(imgDirPath, categoryName + "_neighbors_cc.svg")
        okCc = os.access(imgFilePath, os.F_OK)
        if okCc:
            imgCount += 1

        imgFilePath = os.path.join(imgDirPath, categoryName + "_neighbors_prd.svg")
        okPrd = os.access(imgFilePath, os.F_OK)
        if okPrd:
            imgCount += 1

        imgFilePath = os.path.join(imgDirPath, categoryName + "_neighbors_family.svg")
        okFamily = os.access(imgFilePath, os.F_OK)
        if okFamily:
            imgCount += 1

        if not (okFull or okAbbrev or okCc or okPrd or okFamily):
            return

        # At least one image exists --

        iconText, addClass = self.__getIconAnchorAndClass(contentIconType="category-image", cssClass="pull-right")
        self.__html.beginContainer(cType="row")
        self.__html.beginPanel("Category Relationship Diagrams " + iconText, style="panel-default " + addClass, fmt="html")
        self.__html.beginContainer(cType="row")

        if okFull:
            if imgCount > 2:
                self.__html.beginContainer(cType="col-md-1")
            else:
                self.__html.beginContainer(cType="col-md-1 col-md-offset-1")

            htText = self.__mU.getImage(src="/assets/images/cr-figure-icon.svg", altText="Category relationship diagram", width=70, height=70, cssClassAdd="img-thumbnail")
            bText = self.__mU.getButtonAnchor(
                contentLabel=htText, url="#image-modal-full-1", fmt="html", cssClassAdd="btn-wwpdb-green btn-wwpdb-lg", dataAttributes='data-toggle="modal"'
            )
            self.__html.addContent([bText])
            self.__html.endContainer()
            #
            self.__html.beginContainer(cType="col-md-3")
            self.__html.addContent(["View <b>full</b> category relationship diagram including all dictionary data categories"])
            self.__html.endContainer()
            #
        if okAbbrev:
            self.__html.beginContainer(cType="col-md-1")
            htText = self.__mU.getImage(src="/assets/images/cr-figure-icon.svg", altText="Category relationship diagram", width=70, height=70, cssClassAdd="img-thumbnail")
            bText = self.__mU.getButtonAnchor(
                contentLabel=htText, url="#image-modal-abbrev-1", fmt="html", cssClassAdd="btn-wwpdb-green btn-wwpdb-lg", dataAttributes='data-toggle="modal"'
            )
            self.__html.addContent([bText])
            self.__html.endContainer()
            #
            self.__html.beginContainer(cType="col-md-3")
            self.__html.addContent([" View <b>abbreviated</b> category relationship diagram including only those categories used in <b>current PDB entries</b>."])
            self.__html.endContainer()
            #
        if okCc:
            self.__html.beginContainer(cType="col-md-1")
            htText = self.__mU.getImage(src="/assets/images/cr-figure-icon.svg", altText="Category relationship diagram", width=70, height=70, cssClassAdd="img-thumbnail")
            bText = self.__mU.getButtonAnchor(contentLabel=htText, url="#image-modal-cc-1", fmt="html", cssClassAdd="btn-wwpdb-green btn-wwpdb-lg", dataAttributes='data-toggle="modal"')
            self.__html.addContent([bText])
            self.__html.endContainer()
            #
            self.__html.beginContainer(cType="col-md-3")
            self.__html.addContent([" View <b>abbreviated</b> category relationship diagram including only those categories used in the <b>chemical reference dictionary</b>."])
            self.__html.endContainer()
            #

        if okPrd:
            self.__html.beginContainer(cType="col-md-1")
            htText = self.__mU.getImage(src="/assets/images/cr-figure-icon.svg", altText="Category relationship diagram", width=70, height=70, cssClassAdd="img-thumbnail")
            bText = self.__mU.getButtonAnchor(
                contentLabel=htText, url="#image-modal-bird-1", fmt="html", cssClassAdd="btn-wwpdb-green btn-wwpdb-lg", dataAttributes='data-toggle="modal"'
            )
            self.__html.addContent([bText])
            self.__html.endContainer()
            #
            self.__html.beginContainer(cType="col-md-3")
            self.__html.addContent([" View <b>abbreviated</b> category relationship diagram including only those categories used in the <b>BIRD reference dictionary</b>."])
            self.__html.endContainer()
            #

        if okFamily:
            self.__html.beginContainer(cType="col-md-1")
            htText = self.__mU.getImage(src="/assets/images/cr-figure-icon.svg", altText="Category relationship diagram", width=70, height=70, cssClassAdd="img-thumbnail")
            bText = self.__mU.getButtonAnchor(
                contentLabel=htText, url="#image-modal-bird-family-1", fmt="html", cssClassAdd="btn-wwpdb-green btn-wwpdb-lg", dataAttributes='data-toggle="modal"'
            )
            self.__html.addContent([bText])
            self.__html.endContainer()
            #
            self.__html.beginContainer(cType="col-md-3")
            self.__html.addContent([" View <b>abbreviated</b> category relationship diagram including only those categories used in the <b>BIRD Family reference dictionary</b>."])
            self.__html.endContainer()
            #

        self.__html.endContainer()
        self.__html.endPanel()
        self.__html.endContainer()

        #
        # Now write the markup for the dialogs --
        #
        if okFull:
            imgFileUrl = os.path.join(imgDirUrl, categoryName + "_neighbors.svg")
            titleText = "Category Relationship Diagram for %s" % str(categoryName).upper()
            self.__html.addModalImageDialog(
                modalId="image-modal-full-1", modalTitle=titleText, imagePath=imgFileUrl, imageText=titleText, cssModalSect="my-image-scrollable", cssModalClose="btn-default"
            )

        if okAbbrev:
            imgFileUrl = os.path.join(imgDirUrl, categoryName + "_neighbors_archive.svg")
            titleText = "Abbreviated Category Relationship Diagram for %s" % str(categoryName).upper()
            self.__html.addModalImageDialog(
                modalId="image-modal-abbrev-1", modalTitle=titleText, imagePath=imgFileUrl, imageText=titleText, cssModalSect="my-image-scrollable", cssModalClose="btn-default"
            )

        if okCc:
            imgFileUrl = os.path.join(imgDirUrl, categoryName + "_neighbors_cc.svg")
            titleText = "Category Relationship Diagram for %s" % str(categoryName).upper()
            self.__html.addModalImageDialog(
                modalId="image-modal-cc-1", modalTitle=titleText, imagePath=imgFileUrl, imageText=titleText, cssModalSect="my-image-scrollable", cssModalClose="btn-default"
            )

        if okPrd:
            imgFileUrl = os.path.join(imgDirUrl, categoryName + "_neighbors_prd.svg")
            titleText = "Category Relationship Diagram for %s" % str(categoryName).upper()
            self.__html.addModalImageDialog(
                modalId="image-modal-bird-1", modalTitle=titleText, imagePath=imgFileUrl, imageText=titleText, cssModalSect="my-image-scrollable", cssModalClose="btn-default"
            )

        if okFamily:
            imgFileUrl = os.path.join(imgDirUrl, categoryName + "_neighbors_family.svg")
            titleText = "Category Relationship Diagram for %s" % str(categoryName).upper()
            self.__html.addModalImageDialog(
                modalId="image-modal-bird-family-1",
                modalTitle=titleText,
                imagePath=imgFileUrl,
                imageText=titleText,
                cssModalSect="my-image-scrollable",
                cssModalClose="btn-default",
            )

    def __renderCategoryPage(self, categoryName):
        """Render the information page for the input category."""
        self.__html.clear()
        self.__html.beginContainer()

        # ---
        context = self.__dApi.getCategoryContextList(categoryName)
        isLocalCategory = len(context) > 0 and context[0].upper() in ["WWPDB_LOCAL"]
        mandatoryCode = self.__dApi.getCategoryMandatoryCode(categoryName)
        if (mandatoryCode is None) or (len(mandatoryCode) < 1) or (mandatoryCode in [".", "?"]):
            mandatoryCode = "No"
            if self.__debug:
                logger.debug("no mandatory code for %s", categoryName)
        #
        groupAnchorList = []
        categoryGroupList = sorted(self.__dApi.getCategoryGroupList(categoryName))
        for groupName in categoryGroupList:
            if groupName not in ["inclusive_group"]:
                groupUrl = self.__pI.getContentTypeObjUrl(contentObjName=groupName, contentType="Groups")
                groupAnchor = self.__mU.getAnchor(contentUrl=groupUrl, contentLabel=groupName, cssClassString="my-link-color", fmt="ascii")
                groupAnchorList.append(groupAnchor)

        #
        self.__html.beginContainer()
        iconText, addClass = self.__getIconAnchorAndClass(contentIconType="general", cssClass="pull-right")
        self.__html.beginPanel("General " + iconText, style="panel-default " + addClass, fmt="html")
        self.__html.beginContainer()
        self.__html.beginDescriptionList()
        catUrl = self.__pI.getContentTypeObjUrl(contentObjName=categoryName, contentType="Categories")
        catAnchor = self.__mU.getAnchor(contentUrl=catUrl, contentLabel=categoryName, cssClassString="my-link-color", fmt="ascii")
        self.__html.addDescription(termSt="Category name", descriptionSt=catAnchor, formatDescription="html")
        self.__html.addDescription(termSt="Required in PDB entries", descriptionSt=mandatoryCode)
        self.__html.addDescription(termSt="Category group membership", descriptionSt="&nbsp;&nbsp;".join(sorted(groupAnchorList)), formatDescription="html")

        if self.__isCategoryUsed(categoryName, deliveryType="archive"):
            fS = self.__getCategoryUsePercent(categoryName, deliveryType="archive")
            if isLocalCategory:
                self.__html.addDescription(termSt="Used internally by PDB", descriptionSt="Yes, in about %s %s of entries" % (fS, "%"))
            else:
                self.__html.addDescription(termSt="Used in current PDB entries", descriptionSt="Yes, in about %s %s of entries" % (fS, "%"))
        else:
            self.__html.addDescription(termSt="Used in current PDB entries", descriptionSt="No")
            if isLocalCategory:
                self.__html.addDescription(termSt="Used internally by PDB", descriptionSt="Yes")

        if self.__isCategoryUsed(categoryName, deliveryType="cc"):
            self.__html.addDescription(termSt="Used in the Chemical Component dictionary", descriptionSt="Yes")

        if self.__isCategoryUsed(categoryName, deliveryType="prd"):
            self.__html.addDescription(termSt="Used in the BIRD dictionary", descriptionSt="Yes")

        self.__html.endDescriptionList()
        #
        self.__html.endContainer()
        self.__html.endPanel()
        self.__html.endContainer()
        #
        # --------------------------
        # Category relationship figures - above the fold.
        #
        self.__addCategoryFigures(categoryName)
        # -------------------------
        #
        # -- description --
        description = self.__dApi.getCategoryDescription(categoryName)
        iconText, addClass = self.__getIconAnchorAndClass(contentIconType="info", cssClass="pull-right")
        self.__html.beginContainer(cType="row")
        self.__html.beginPanel("Category Description " + iconText, style="panel-default " + addClass, fmt="html")
        ht = self.__mU.getFormatted(description, wrapper="pre", fmt="ascii")
        #
        self.__html.addContent([ht])
        self.__html.endPanel()
        self.__html.endContainer()

        altDescription = self.__dApi.getCategoryDescriptionAlt(categoryName, fallBack=False)
        if self.__notNull(altDescription):
            iconText, addClass = self.__getIconAnchorAndClass(contentIconType="deposit-info", cssClass="pull-right")
            self.__html.beginContainer(cType="row")
            self.__html.beginPanel("Additional Descriptive Information for Depositors " + iconText, style="panel-default " + addClass, fmt="html")
            ht = self.__mU.getFormatted(description, wrapper="pre", fmt="none")
            self.__html.addContent([ht])
            self.__html.endPanel()
            self.__html.endContainer()
        #
        nxMapping = self.__dApi.getCategoryNxMappingDetails(categoryName)
        if self.__notNull(nxMapping):
            iconText, addClass = self.__getIconAnchorAndClass(contentIconType="deposit-info", cssClass="pull-right")
            self.__html.beginContainer(cType="row")
            self.__html.beginPanel("NeXus Mapping Details" + iconText, style="panel-default " + addClass, fmt="html")
            ht = self.__mU.getFormatted(nxMapping, wrapper="pre", fmt="none")
            self.__html.addContent([ht])
            self.__html.endPanel()
            self.__html.endContainer()
        #
        # -- examples --
        exampleList = self.__dApi.getCategoryExampleList(categoryName)
        htmlList = self.__renderExamples(exampleList, "Category Example", "Category Examples", idSuffix="a")

        self.__html.beginContainer(cType="row")
        self.__html.addContent(htmlList)
        self.__html.endContainer()
        #
        #
        altExampleList = self.__dApi.getCategoryExampleListAlt(categoryName, fallBack=False)
        htmlList = self.__renderExamples(altExampleList, "Additional Category Example for Depositors", "Additional Category Examples for Depositors", idSuffix="b")
        self.__html.beginContainer(cType="row")
        self.__html.addContent(htmlList)
        self.__html.endContainer()
        #
        keyItemNameList = sorted(self.__dApi.getCategoryKeyList(categoryName))
        iconText, addClass = self.__getIconAnchorAndClass(contentIconType="key", cssClass="pull-right")
        self.__html.beginContainer(cType="row")
        self.__html.beginPanel("Key Data Items " + iconText, style="panel-default " + addClass, fmt="html")

        self.__html.beginInLineList()
        for keyItemName in keyItemNameList:
            itemUrl = self.__pI.getContentTypeObjUrl(contentObjName=keyItemName, contentType="Items")
            itemAnchor = self.__mU.getAnchor(contentUrl=itemUrl, contentLabel=keyItemName, cssClassString="my-link-color", fmt="ascii")
            listValue = itemAnchor
            self.__html.addInLineListItem(listValue, fmt="html")
        self.__html.endInLineList()
        self.__html.endPanel()
        self.__html.endContainer()

        #
        doThis = False
        if doThis:
            categoryGroupList = sorted(self.__dApi.getCategoryGroupList(categoryName))
            self.__html.beginContainer(cType="row")
            self.__html.beginPanel("Category Groups", style="panel-default", fmt="html")
            self.__html.beginInLineList()
            for groupName in categoryGroupList:
                if groupName not in ["inclusive_group"]:
                    groupUrl = self.__pI.getContentTypeObjUrl(contentObjName=groupName, contentType="Groups")
                    groupAnchor = self.__mU.getAnchor(contentUrl=groupUrl, contentLabel=groupName, cssClassString="my-link-color", fmt="ascii")
                    self.__html.addInLineListItem(groupAnchor, fmt="html")
            self.__html.endInLineList()
            self.__html.endPanel()
            self.__html.endContainer()

        #
        _, htmlList = self.__renderItemLinkList(categoryName)
        self.__html.beginContainer(cType="row")
        self.__html.addAccordionPanel(
            title="Category Data Items", subTitle=None, panelTextList=htmlList, panelId="pit0", panelGroupId="pgit0", openFlag=True, toggleText="View/hide item list"
        )
        self.__html.endContainer()

        self.__html.endContainer()
        return self.__html.getHtmlList()

    def makeCategoryPage(self, categoryName):
        return self.__renderCategoryPage(categoryName)

    def __addPanelWithInLineItemList(self, itemNameList, panelTitle, contentObjName="default"):
        """"""
        iconText, addClass = self.__getIconAnchorAndClass(contentIconType=contentObjName, cssClass="pull-right")
        self.__html.beginContainer()
        self.__html.beginPanel(panelTitle + iconText, style="panel-default " + addClass, fmt="html")
        self.__html.beginInLineList()
        for itemName in itemNameList:
            itemUrl = self.__pI.getContentTypeObjUrl(contentObjName=itemName, contentType="Items")
            itemAnchor = self.__mU.getAnchor(contentUrl=itemUrl, contentLabel=itemName, cssClassString="my-link-color", fmt="ascii")
            listValue = itemAnchor
            self.__html.addInLineListItem(listValue, fmt="html")
        self.__html.endInLineList()
        self.__html.endPanel()
        self.__html.endContainer()

    def __addPanelWithInLineList(self, valueList, panelTitle, contentObjName="default", fmt="ascii"):
        """"""
        iconText, addClass = self.__getIconAnchorAndClass(contentIconType=contentObjName, cssClass="pull-right")
        self.__html.beginContainer()
        self.__html.beginPanel(panelTitle + iconText, style="panel-default " + addClass, fmt="html")
        self.__html.beginInLineList()
        self.__html.addInLineList(valueList, fmt=fmt)
        self.__html.endInLineList()
        self.__html.endPanel()
        self.__html.endContainer()

    def __addAccordionPanelWithTable(
        self,
        rowList,
        columnNameList,
        panelTitle,
        contentObjName="default",
        columnNameFormat="ascii",
        dataFormat="ascii",
        newLines="verbatim",
        idSuffix="a",
        openFlag=True,
        toggleText="View/Hide Table",
    ):
        """"""
        _ = contentObjName
        htmlList = self.__renderTable(rowList=rowList, columnNameList=columnNameList, columnNameFormat=columnNameFormat, dataFormat=dataFormat, newLines=newLines)
        #
        pgId = "pgapwt" + idSuffix
        pId = "papwt" + idSuffix
        self.__html.beginContainer()
        self.__html.beginAccordionPanelGroup(panelGroupId=pgId)
        self.__html.addAccordionPanel(title=panelTitle, panelTextList=htmlList, panelId=pId, panelGroupId=pgId, openFlag=openFlag, toggleText=toggleText)
        self.__html.endAccordionPanelGroup()
        self.__html.endContainer()

    def __addPanelWithTable(self, rowList, columnNameList, panelTitle, contentObjName="default", columnNameFormat="ascii", dataFormat="ascii", newLines="verbatim"):
        """"""
        htmlList = self.__renderTable(rowList=rowList, columnNameList=columnNameList, columnNameFormat=columnNameFormat, dataFormat=dataFormat, newLines=newLines)

        iconText, addClass = self.__getIconAnchorAndClass(contentIconType=contentObjName, cssClass="pull-right")
        self.__html.beginContainer(cType="row")
        self.__html.beginPanel(panelTitle + iconText, style="panel-default " + addClass, fmt="html")
        self.__html.addContent(htmlList)
        self.__html.endPanel()
        self.__html.endContainer()

    def __renderItemPage(self, itemName):
        """Render the information page for the input item."""
        categoryName = CifName.categoryPart(itemName)
        attributeName = CifName.attributePart(itemName)
        #
        self.__html.clear()
        self.__html.beginContainer()
        #
        #
        mandatoryCode = self.__dApi.getMandatoryCode(categoryName, attributeName)
        mandatoryCodeAlt = self.__dApi.getMandatoryCodeAlt(categoryName, attributeName, fallBack=False)

        # -- general info --
        self.__html.beginContainer()
        iconText, addClass = self.__getIconAnchorAndClass(contentIconType="default", cssClass="pull-right")
        self.__html.beginPanel("General " + iconText, style="panel-default " + addClass, fmt="html")
        self.__html.beginContainer()
        self.__html.beginDescriptionList()
        catUrl = self.__pI.getContentTypeObjUrl(contentObjName=categoryName, contentType="Categories")
        catAnchor = self.__mU.getAnchor(contentUrl=catUrl, contentLabel=categoryName, cssClassString="my-link-color", fmt="ascii")
        self.__html.addDescription(termSt="Item name", descriptionSt=itemName)
        self.__html.addDescription(termSt="Category name", descriptionSt=catAnchor, formatDescription="html")
        self.__html.addDescription(termSt="Attribute name", descriptionSt=attributeName)

        self.__html.addDescription(termSt="Required in PDB entries", descriptionSt=mandatoryCode)
        if mandatoryCodeAlt is not None and len(mandatoryCodeAlt) > 0 and mandatoryCodeAlt != mandatoryCode:
            self.__html.addDescription(termSt="Required for PDB deposition", descriptionSt=mandatoryCodeAlt)

        if self.__getItemCount(itemName, deliveryType="archive") > 0:
            fS = self.__getItemUsePercent(itemName, deliveryType="archive")
            self.__html.addDescription(termSt="Used in current PDB entries", descriptionSt="Yes, in about %s %s of entries" % (fS, "%"))
        else:
            self.__html.addDescription(termSt="Used in currrent PDB entries", descriptionSt="No")

        if self.__getItemCount(itemName, deliveryType="prd") > 0:
            self.__html.addDescription(termSt="Used in the BIRD dictionary", descriptionSt="Yes")

        if self.__getItemCount(itemName, deliveryType="cc") > 0:
            self.__html.addDescription(termSt="Used in the Chemical Component dictionary", descriptionSt="Yes")

        self.__html.endDescriptionList()
        #
        self.__html.endContainer()
        self.__html.endPanel()
        self.__html.endContainer()

        # -- description --
        description = self.__dApi.getDescription(categoryName, attributeName)
        iconText, addClass = self.__getIconAnchorAndClass(contentIconType="info", cssClass="pull-right")
        self.__html.beginContainer(cType="row")
        self.__html.beginPanel("Item Description " + iconText, style="panel-default " + addClass, fmt="html")
        # ht=self.__mU.getFormatted(description,wrapper='pre',  fmt='ascii')
        ht = self.__mU.getFormatted(description, wrapper="verbatim", fmt="ascii", markupMath=True)
        self.__html.addContent([ht])
        self.__html.endPanel()
        self.__html.endContainer()

        #
        altDescription = self.__dApi.getDescriptionAlt(categoryName, attributeName, fallBack=False)
        if self.__notNull(altDescription):
            iconText, addClass = self.__getIconAnchorAndClass(contentIconType="deposit-info", cssClass="pull-right")
            self.__html.beginContainer(cType="row")
            self.__html.beginPanel("Additional Descriptive Information for  Depositors " + iconText, style="panel-default " + addClass, fmt="html")
            ht = self.__mU.getFormatted(description, wrapper="pre", fmt="none")
            self.__html.addContent([ht])
            self.__html.endPanel()
            self.__html.endContainer()

        #
        # -- examples --
        exampleList = self.__dApi.getExampleList(categoryName, attributeName)
        htmlList = self.__renderExamples(exampleList, "Item Example", "Item Examples", idSuffix="a")

        self.__html.beginContainer(cType="row")
        self.__html.addContent(htmlList)
        self.__html.endContainer()
        #
        altExampleList = self.__dApi.getExampleListAlt(categoryName, attributeName, fallBack=False)
        htmlList = self.__renderExamples(altExampleList, "Additional Item Example for Depositors", "Additional Item Examples for Depositors", idSuffix="b")

        self.__html.beginContainer(cType="row")
        self.__html.addContent(htmlList)
        self.__html.endContainer()
        #
        # --------------------------------------------------------------------------------------------
        #  Context -
        #
        context = self.__dApi.getContextList(categoryName, attributeName)

        #
        #  ---Data type -
        #
        typeCode = self.__dApi.getTypeCode(categoryName, attributeName)
        typePrimitive = self.__dApi.getTypePrimitive(categoryName, attributeName)
        typeDetail = self.__dApi.getTypeDetail(categoryName, attributeName)
        typeRegex = self.__dApi.getTypeRegex(categoryName, attributeName)
        #
        typeCodeAlt = self.__dApi.getTypeCodeAlt(categoryName, attributeName, fallBack=False)
        typeRegexAlt = self.__dApi.getTypeRegexAlt(categoryName, attributeName, fallBack=False)
        #

        defaultValue = self.__dApi.getDefaultValue(categoryName, attributeName)
        units = self.__dApi.getUnits(categoryName, attributeName)
        enumClosedFlag = self.__dApi.getEnumerationClosedFlag(categoryName, attributeName)
        # if enumClosedFlag is not None:
        #    logger.debug("+INFO - closed flag - category %s attribute %s  = %r\n " % (categoryName,attributeName,enumClosedFlag))

        #
        # -- data type  --
        #
        self.__html.beginContainer()
        iconText, addClass = self.__getIconAnchorAndClass(contentIconType="regex", cssClass="pull-right")
        self.__html.beginPanel("Data Type " + iconText, style="panel-default " + addClass, fmt="html")
        self.__html.beginContainer()
        self.__html.beginDescriptionList()

        if typeCode is not None and len(typeCode) > 0:
            self.__html.addDescription(termSt="Data type code", descriptionSt=typeCode)
            self.__html.addDescription(termSt="Data type detail", descriptionSt=typeDetail)
            self.__html.addDescription(termSt="Primitive data type code", descriptionSt=typePrimitive)
            self.__html.addDescription(termSt="Regular expression", descriptionSt=typeRegex, cssClassDescription="my-font-monospace")
        else:
            logger.warning("+ERROR missing type for item %s", itemName)

        if typeCodeAlt is not None and len(typeCodeAlt) > 0 and typeCode != typeCodeAlt:
            self.__html.addDescription(termSt="Deposition data type", descriptionSt=typeCodeAlt)
        if typeRegexAlt is not None and len(typeRegexAlt) > 0 and typeRegex != typeRegexAlt:
            self.__html.addDescription(termSt="Deposition regular expression", descriptionSt=typeRegexAlt)

        if defaultValue is not None and len(defaultValue) > 0:
            self.__html.addDescription(termSt="Default value", descriptionSt=defaultValue)

        if units is not None and len(units) > 0:
            self.__html.addDescription(termSt="Units", descriptionSt=units)

        if context is not None and len(context) > 0 and "local" in context[0].lower():
            self.__html.addDescription(termSt="Internal data item", descriptionSt="Yes")

        if enumClosedFlag is not None and enumClosedFlag == "no":
            self.__html.addDescription(termSt="Values limited by enumeration list ", descriptionSt="no")

        self.__html.endDescriptionList()
        #
        self.__html.endContainer()
        self.__html.endPanel()
        self.__html.endContainer()

        #
        # Only enum values with details
        #
        enumListWithDetail = self.__dApi.getEnumListWithDetail(categoryName, attributeName)
        if enumListWithDetail is not None and len(enumListWithDetail) > 0:
            columnNameList = ["Allowed&nbsp;Value", "Details"]
            self.__addAccordionPanelWithTable(
                rowList=enumListWithDetail,
                columnNameList=columnNameList,
                panelTitle="Controlled Vocabulary",
                contentObjName="default",
                columnNameFormat="html",
                dataFormat="ascii",
                newLines="verbatim",
                idSuffix="enum",
                openFlag=True,
                toggleText="View/Hide Table",
            )

        enumListAltWithDetail = self.__dApi.getEnumListAltWithDetail(categoryName, attributeName)
        if enumListAltWithDetail is not None and len(enumListAltWithDetail) > 0:
            columnNameList = ["Allowed&nbsp;Value", "Details"]
            self.__addAccordionPanelWithTable(
                rowList=enumListAltWithDetail,
                columnNameList=columnNameList,
                panelTitle="Controlled Vocabulary at Deposition",
                contentObjName="default",
                columnNameFormat="html",
                dataFormat="ascii",
                newLines="verbatim",
                idSuffix="enumalt",
                openFlag=True,
                toggleText="View/Hide Table",
            )

        #
        # Boundary values -
        #  (min, max)
        skipEquivalentBounds = True
        bndList = self.__dApi.getBoundaryList(categoryName, attributeName)
        boundaryList = []
        for bnd in bndList:
            bMin = bnd[0]
            bMax = bnd[1]
            if skipEquivalentBounds and bMin == bMax:
                continue
            if bMin == ".":
                bMin = "<h3>-&infin;</h3>"
            if bMax == ".":
                bMax = "<h3>+&infin;</h3>"
            boundaryList.append((bMin, bMax))

        if boundaryList is not None and len(boundaryList) > 0:
            columnNameList = ["Minimum&nbsp;Value", "Maximum&nbsp;Value"]
            self.__addPanelWithTable(
                rowList=boundaryList,
                columnNameList=columnNameList,
                panelTitle="Allowed Boundary Conditions",
                contentObjName="default",
                columnNameFormat="html",
                dataFormat="html",
                newLines="verbatim",
            )
        #
        bndList = self.__dApi.getBoundaryListAlt(categoryName, attributeName, fallBack=False)
        boundaryListAlt = []
        for bnd in bndList:
            bMin = bnd[0]
            bMax = bnd[1]
            if skipEquivalentBounds and bMin == bMax:
                continue
            if bMin == ".":
                bMin = "<h3>-&infin;</h3>"
            if bMax == ".":
                bMax = "<h3>+&infin;</h3>"
            boundaryListAlt.append((bMin, bMax))

        if boundaryListAlt is not None and len(boundaryListAlt) > 0:
            columnNameList = ["Minimum&nbsp;Value", "Maximum&nbsp;Value"]
            self.__addPanelWithTable(
                rowList=boundaryListAlt,
                columnNameList=columnNameList,
                panelTitle="Advisory Boundary Conditions",
                contentObjName="default",
                columnNameFormat="html",
                dataFormat="html",
                newLines="verbatim",
            )
        #
        # --
        # Parent-child -
        #
        parentList = self.__dApi.getFullParentList(categoryName, attributeName, stripSelfParent=True)
        if parentList is not None and len(parentList) > 0:
            self.__addPanelWithInLineItemList(sorted(parentList), "Parent Data Items", contentObjName="parent-child")
            #
            uP = self.__dApi.getUltimateParent(categoryName, attributeName)
            if uP != parentList[0]:
                self.__addPanelWithInLineItemList([uP], "Leading Parent Item", contentObjName="parent-child")
                logger.debug("Ultimate parent of %s is %s", parentList[0], uP)
            if len(parentList) > 1:
                logger.debug("Multiple parents for %s  %s %r", categoryName, attributeName, parentList)

        childList = self.__dApi.getFullChildList(categoryName, attributeName)
        if childList is not None and len(childList) > 0:
            self.__addPanelWithInLineItemList(sorted(childList), "Child Data Items", contentObjName="parent-child")

        #
        relatedList = self.__dApi.getItemRelatedList(categoryName, attributeName)
        if relatedList is not None and len(relatedList) > 0:
            rList = []
            for itemName, relationType in relatedList:
                linkUrl = self.__pI.getContentTypeObjUrl(contentObjName=itemName, contentType="Items")
                linkAnchor = self.__mU.getAnchor(contentUrl=linkUrl, contentLabel=itemName, cssClassString=None, fmt="ascii")
                rList.append((linkAnchor, relationType))

            columnNameList = ["Related&nbsp;Item&nbsp;Name", "Relation&nbsp;Type"]
            self.__addPanelWithTable(
                rowList=rList,
                columnNameList=columnNameList,
                panelTitle="Related Items",
                contentObjName="related-item",
                columnNameFormat="html",
                dataFormat="html",
                newLines="verbatim",
            )
        #
        dependentList = self.__dApi.getItemDependentNameList(categoryName, attributeName)
        if dependentList is not None and len(dependentList) > 0:
            self.__addPanelWithInLineItemList(dependentList, "Dependent Items", contentObjName="related-item")

        subCategoryList = self.__dApi.getItemSubCategoryIdList(categoryName, attributeName)
        if subCategoryList is not None and len(subCategoryList) > 0:
            dList = []
            for subCategory in subCategoryList:
                dS = self.__dApi.getSubCategoryDescription(subCategory)
                dList.append((subCategory, dS))
            # self.__addPanelWithDescriptionList(dList,'SubCategories',contentObjName='default')
            columnNameList = ["Subcategory&nbsp;Name", "Subcategory&nbsp;Description"]
            self.__addPanelWithTable(
                rowList=dList, columnNameList=columnNameList, panelTitle="Subcategories", contentObjName="info", columnNameFormat="html", dataFormat="ascii", newLines="verbatim"
            )
        #
        # --  aliases
        #
        aliasTupleList = self.__dApi.getItemAliasList(categoryName, attributeName)
        if aliasTupleList is not None and len(aliasTupleList) > 0:
            columnNameList = ["Alias&nbsp;Item&nbsp;Name", "Dictionary&nbsp;Name", "Dictionary&nbsp;Version"]
            self.__addPanelWithTable(
                rowList=aliasTupleList, columnNameList=columnNameList, panelTitle="Aliases", contentObjName="info", columnNameFormat="html", dataFormat="ascii", newLines="verbatim"
            )

        # ----------------------------------------------------------------------------------------------

        self.__html.endContainer()
        return self.__html.getHtmlList()

    def makeItemPage(self, itemName):
        return self.__renderItemPage(itemName)

    def __addPanelWithDescriptionList(self, termDescriptionList, panelTitle, contentObjName="default"):
        _ = contentObjName
        self.__html.beginContainer()
        iconText, addClass = self.__getIconAnchorAndClass(contentIconType="default", cssClass="pull-right")
        self.__html.beginPanel(panelTitle + iconText, style="panel-default " + addClass, fmt="html")
        self.__html.beginContainer()
        self.__html.beginDescriptionList()
        for termSt, descriptionSt in termDescriptionList:
            self.__html.addDescription(termSt=termSt, descriptionSt=descriptionSt, formatDescription="ascii")
        self.__html.endDescriptionList()
        #
        self.__html.endContainer()
        self.__html.endPanel()
        self.__html.endContainer()


if __name__ == "__main__":
    pass
