##
# File:    NeighborFigures.py
# Author:  J. Westbrook
# Date:    27-Sep-2013
# Version: 0.001
#
# Updates:
#
#  03-Oct-2013 jdw  -  Add guard characters before category and attribute names in dot files
#                      to protect against leading digits in cif names.
#   8-Oct-2013 jdw -   Adjust cell padding for for attribute name display
#  28-Dec-2020 jdw -   cleanup and py39
##
"""
Utility methods for generating depictions of data category neighbor relationships.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2,0"

import logging
import os

from mmcif.api.PdbxContainers import CifName

logger = logging.getLogger(__name__)


class NeighborFigures(object):
    """Utility methods for generating depictions of data category neighbor relationships"""

    def __init__(self, dictApiObj, pathInfoObj=None, pathDot="/usr/local/bin/dot", verbose=False):
        """"""
        self.__verbose = verbose
        self.__dApi = dictApiObj
        self.__pI = pathInfoObj
        self.__pathDot = pathDot
        # Default font settings ----
        self.__fontFace = "helvetica"
        # self.__fontSize='10'
        self.__fontSizeCategory = "10"
        self.__fontSizeAttribute = "9"
        self.__titleFontFace = "helvetica"
        self.__titleFontSize = "18"
        self.__subTitleFontSize = "14"
        #
        self.__itemCounts = {"archive": {}, "prd": {}, "cc": {}, "family": {}}
        self.__categoryCounts = {"archive": {}, "prd": {}, "cc": {}, "family": {}}

    def setFonts(self, fontFace="helvetica", fontSizeCategory="10", fontSizeAttribute="10", titleFontSize="18", subTitleFontSize="14"):
        self.__fontFace = fontFace
        self.__fontSizeCategory = fontSizeCategory
        self.__fontSizeAttribute = fontSizeAttribute
        self.__titleFontFace = fontFace
        self.__titleFontSize = titleFontSize
        self.__subTitleFontSize = subTitleFontSize

    def setItemCounts(self, itemNameD, deliveryType="archive"):
        for itemName, itemCount in itemNameD.items():
            self.__itemCounts[deliveryType][itemName] = itemCount
            categoryName = CifName.categoryPart(itemName)
            if categoryName not in self.__categoryCounts[deliveryType]:
                self.__categoryCounts[deliveryType][categoryName] = itemCount
            else:
                self.__categoryCounts[deliveryType][categoryName] = max(itemCount, self.__categoryCounts[deliveryType][categoryName])

        logger.debug("+NeighborFigures.setItemCounts() items      in archive count %d", len(self.__itemCounts[deliveryType]))
        logger.debug("+NeighborFigures.setItemCounts() categories in archive count %d", len(self.__categoryCounts[deliveryType]))

    def getCategoryUseCount(self, categoryName, deliveryType="archive"):
        if categoryName in self.__categoryCounts[deliveryType]:
            return self.__categoryCounts[deliveryType][categoryName]
        else:
            return 0

    def __isCategoryUsed(self, categoryName, deliveryType="archive"):
        if categoryName in self.__categoryCounts[deliveryType]:
            return True
        else:
            return False

    def __isItemUsed(self, itemName, deliveryType="archive"):
        if self.__getItemCount(itemName, deliveryType) > 0:
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

            if pc > 1:
                return "%5d" % (pc)
            elif pc > 0.10:
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

            if pc > 1:
                return "%5d" % (pc)
            elif pc > 0.10:
                return "%5.1f" % (pc)
            elif pc > 0.01:
                return "%5.2f" % (pc)
            else:
                return "%6.3f" % (pc)
        else:
            return "0.0"

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
            inBirdDict = self.__getItemCount(itemName, deliveryType="prd") > 0 or self.__getItemCount(itemName, deliveryType="family") > 0

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
            inBirdDict = self.__isCategoryUsed(categoryName, deliveryType="prd") or self.__isCategoryUsed(categoryName, deliveryType="family")
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

    def __getOrderedItemNameList(self, categoryName, fkList=None, filterDelivery=False, deliveryType="archive"):
        """Return the item name list for the input category with the order: key items, items with FK relationships,
        and remaining items.    Items which do are not key nor participate in any parent child relationships
        can be filtered according to their presence in current archive entries.
        """
        allItemList = sorted(self.__dApi.getItemNameList(categoryName))
        rList = []
        for itemName in allItemList:
            if fkList and itemName in fkList:
                rList.append(itemName)

        tList = []
        keyItemNameList = sorted(self.__dApi.getCategoryKeyList(categoryName))
        if filterDelivery:
            for itemName in allItemList:
                if itemName in keyItemNameList:
                    tList.append(itemName)
                    continue
                if itemName in rList:
                    tList.append(itemName)
                    continue
                if self.__isItemUsed(itemName, deliveryType=deliveryType):
                    tList.append(itemName)
        else:
            tList = allItemList

        #
        for keyItemName in keyItemNameList:
            if keyItemName in rList:
                rList.remove(keyItemName)
            if keyItemName in tList:
                tList.remove(keyItemName)
            else:
                logger.warning("+NeighborFigures.__getOrderedItemNameList() Category %s is missing key definition for %s", categoryName, keyItemName)

        for rItemName in rList:
            if rItemName in tList:
                tList.remove(rItemName)
        #
        minItemCount = len(keyItemNameList) + len(rList)
        #
        itemNameList = []
        itemNameList.extend(keyItemNameList)
        itemNameList.extend(rList)
        itemNameList.extend(tList)
        return itemNameList, minItemCount

    def __getParentCategories(self, itemNameList):
        parentCategories = set()
        for itemName in itemNameList:
            categoryName = CifName.categoryPart(itemName)
            attributeName = CifName.attributePart(itemName)
            parentItemList = self.__dApi.getFullParentList(categoryName, attributeName)
            for parentItem in parentItemList:
                parentCategoryName = CifName.categoryPart(parentItem)
                parentCategories.add(parentCategoryName)
        return list(parentCategories)

    def __getChildCategories(self, itemNameList):
        childCategories = set()
        for itemName in itemNameList:
            categoryName = CifName.categoryPart(itemName)
            attributeName = CifName.attributePart(itemName)
            childItemList = self.__dApi.getFullChildList(categoryName, attributeName)
            for childItem in childItemList:
                childCategoryName = CifName.categoryPart(childItem)
                childCategories.add(childCategoryName)
        return list(childCategories)

    def __getRelativesAdjacent(self, itemNameList):
        aR = {}
        for itemName in itemNameList:
            categoryName = CifName.categoryPart(itemName)
            attributeName = CifName.attributePart(itemName)
            tD = {}
            tD["parentItems"] = self.__dApi.getFullParentList(categoryName, attributeName)
            tD["childItems"] = self.__dApi.getFullChildList(categoryName, attributeName)
            aR[itemName] = tD
        # if (self.__verbose):
        #    for k,v in aR.items():
        #        logger.debug("Item %s\n       parents: %s\n       children  %s\n\n" % (k,v['parentItems'],v['childItems']))
        return aR

    def __renderCategory(self, categoryName, fkList=None, highLight="adjacent", maxItems=10, filterDelivery=False, deliveryType="archive"):
        """Create graphviz object with embedded tabular HTML represenation of the input data category

             * Add _ guard characters before graph name and port names --

        _categoryName_1 [label=<
        <table border="0" cellborder="1" cellspacing="0" align="left">
        <tr><td BGCOLOR="Lavender">categoryName_1</td></tr>
        <tr><td PORT="__attribute_1">attribute_1</td></tr>
        <tr><td PORT="__attribute_2">attribute_2</td></tr>
        <tr><td PORT="__attribute_3">attribute_3</td></tr>
        </table>>];

        """
        colorD = {
            "op1": 'BGCOLOR="#7fc97f"',
            "other": 'BGCOLOR="#beaed4"',
            "op2": 'BGCOLOR="#fdc086"',
            "key": 'BGCOLOR="#ffff99"',
            "op4": 'BGCOLOR="#386cb0"',
            "current": 'BGCOLOR="#f0027f"',
            "adjacent": 'BGCOLOR="#99c49b"',
        }
        oList = []
        itemNameList, minItemCount = self.__getOrderedItemNameList(categoryName, fkList=fkList, filterDelivery=filterDelivery, deliveryType=deliveryType)
        itemsToRender = max(minItemCount, maxItems)
        #
        categoryUrl = os.path.join(self.__pI.getContentTypeObjUrl(contentObjName=categoryName, contentType="Categories"))
        logger.debug("Rendering %s categoryUrl %r itemNameList %r itemsToRender %r fkList %r", categoryName, categoryUrl, itemNameList, itemsToRender, fkList)
        if len(itemNameList) > 0:
            iconTypeList = self.__assignItemIconType(itemNameList)
            oList.append('_%s [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" ALIGN="LEFT">' % (categoryName))
            tdText = '<FONT POINT-SIZE="%s" FACE="%s">%s</FONT>' % (self.__fontSizeCategory, self.__fontFace, categoryName.upper())
            oList.append('    <tr><td %s CELLPADDING="4" HREF="%s" TARGET="_top">%s</td></tr>' % (colorD[highLight], categoryUrl, tdText))

            for iconType, itemName in list(zip(iconTypeList, itemNameList))[:itemsToRender]:
                itemUrl = os.path.join(self.__pI.getContentTypeObjUrl(contentObjName=itemName, contentType="Items"))
                attributeName = CifName.attributePart(itemName)
                tdText = '<FONT POINT-SIZE="%s" FACE="%s">%s</FONT>' % (self.__fontSizeAttribute, self.__fontFace, attributeName)
                if "key" in iconType:
                    oList.append('<tr><td %s PORT="__%s" CELLPADDING="4" HREF="%s" TARGET="_top" ALIGN="LEFT">%s</td></tr>' % (colorD["key"], attributeName, itemUrl, tdText))
                else:
                    oList.append('<tr><td PORT="__%s" CELLPADDING="4" HREF="%s" TARGET="_top" ALIGN="LEFT">%s</td></tr>' % (attributeName, itemUrl, tdText))

            if len(itemNameList) > itemsToRender:
                tdText = '<FONT POINT-SIZE="%s" FACE="%s">%s</FONT>' % (self.__fontSizeAttribute, self.__fontFace, "... and others ...")
                oList.append("<tr><td>%s</td></tr>" % tdText)
            oList.append("</TABLE>>];")
        else:
            # Placeholder for missing category
            oList.append('_%s [label=<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" ALIGN="LEFT">' % (categoryName))
            tdText = '<FONT POINT-SIZE="%s" FACE="%s">%s</FONT>' % (self.__fontSizeCategory, self.__fontFace, categoryName.upper())
            oList.append('    <tr><td %s CELLPADDING="4"  TARGET="_top">%s</td></tr>' % (colorD[highLight], tdText))

            for itemName in fkList:
                iconType = "none"
                itemUrl = os.path.join(self.__pI.getContentTypeObjUrl(contentObjName=itemName, contentType="Items"))
                attributeName = CifName.attributePart(itemName)
                tdText = '<FONT POINT-SIZE="%s" FACE="%s">%s</FONT>' % (self.__fontSizeAttribute, self.__fontFace, attributeName)
                if "key" in iconType:
                    oList.append('<tr><td %s PORT="__%s" CELLPADDING="4" TARGET="_top" ALIGN="LEFT">%s</td></tr>' % (colorD["key"], attributeName, tdText))
                else:
                    oList.append('<tr><td PORT="__%s" CELLPADDING="4" TARGET="_top" ALIGN="LEFT">%s</td></tr>' % (attributeName, tdText))

            oList.append("</TABLE>>];")
        #
        return oList

    def __getRelatedList(self, categoryName, adjacentD):
        #
        relatedSet = set()
        for itemName, adjD in adjacentD.items():
            cName = CifName.categoryPart(itemName)
            if len(adjD["parentItems"]) > 0:
                if cName == categoryName:
                    relatedSet.add(itemName)
                for parentItemName in adjD["parentItems"]:
                    pName = CifName.categoryPart(parentItemName)
                    if pName == categoryName:
                        relatedSet.add(parentItemName)
            if len(adjD["childItems"]) > 0:
                if cName == categoryName:
                    relatedSet.add(itemName)
                for childItemName in adjD["childItems"]:
                    chName = CifName.categoryPart(childItemName)
                    if chName == categoryName:
                        relatedSet.add(childItemName)
        relatedList = sorted(list(relatedSet))

        logger.debug("%s items with parent/child relationships %s", categoryName, len(relatedList))
        #
        return relatedList

    def __generateDotInstructions(
        self,
        categoryName,
        graphTitle=None,
        graphSubTitle=None,
        titleFormat="text",
        maxItems=20,
        filterDelivery=False,
        deliveryType="archive",
        neighborCategoryList=None,
        maxCategories=None,
    ):
        """Internal method producing GraphViz 'dot' instructions depicting data category relationships between the input category and either all
        of its adjacent neighbors or for selected 'neighborCategoryList'.    Optionally apply filtering to categories in current use within the archive.

        maxItems       controls target maximum number of attributes in any category object depiction.
        maxCategories  limits the number of related category objects depicted.
        """
        #
        # Skip cases where the principal category is not associated with the input delivery type -
        #
        if filterDelivery and not self.__isCategoryUsed(categoryName=categoryName, deliveryType=deliveryType):
            logger.debug("skipping category %r delivery %r", categoryName, deliveryType)
            return [], 0
        #
        numCategoriesRendered = 0
        itemNameList = self.__dApi.getItemNameList(categoryName)
        aR = self.__getRelativesAdjacent(itemNameList)

        #
        for k, v in aR.items():
            logger.debug("%s relatives %s", k, v)
        #
        adjacentCategories = []
        adjacentCategories.append(categoryName)
        if neighborCategoryList is None:
            adjacentCategories.extend(self.__getParentCategories(itemNameList))
            adjacentCategories.extend(self.__getChildCategories(itemNameList))
        else:
            adjacentCategories.extend(neighborCategoryList)
            #
        adjacentCategories = sorted(list(set(adjacentCategories)))

        if maxCategories is not None:
            adjacentCategories = adjacentCategories[:maxCategories]

        logger.debug("adjacent categories %s", adjacentCategories)
        #
        oL = []
        oL.append("digraph %s {" % categoryName)
        #  Some previous layout parameters --- jdw
        #        oL.append('splines=true; overlap=portho; model=subset;')
        #        oL.append('splines=ortho; overlap=compress; model=subset; ratio=1.0;')
        oL.append("splines=true; overlap=compress; ")
        #
        # Option graph title -
        if graphTitle is not None:
            if titleFormat == "text":
                # dot instructions do not recognize the font settings.
                # oL.append('graph [labelloc=b, labeljust=left, labelfontname=Helvetica, labelfontsize=18, label="%s"];' % (self.__titleFontFace, self.__titleFontSize, graphTitle))
                oL.append('graph [labelloc=b, labeljust=left, labelfontname=%s, labelfontsize=%s, label="%s"];' % (self.__titleFontFace, self.__titleFontSize, graphTitle))
            else:
                # Title is rendered with this font detail.

                titleText = '<FONT POINT-SIZE="%s" FACE="%s">%s</FONT>' % (self.__titleFontSize, self.__titleFontFace, graphTitle)
                if graphSubTitle is not None:
                    titleText += '<FONT POINT-SIZE="%s" FACE="%s"> <br/> %s</FONT>' % (self.__subTitleFontSize, self.__titleFontFace, graphSubTitle)
                oL.append("graph [labelloc=b, label=<%s>];" % (titleText))

        oL.append("node [shape=plaintext]")

        for catName in adjacentCategories:
            if filterDelivery and not self.__isCategoryUsed(categoryName=catName, deliveryType=deliveryType):
                continue
            if catName == categoryName:
                highLight = "current"
            else:
                highLight = "adjacent"
            relatedList = self.__getRelatedList(categoryName=catName, adjacentD=aR)
            oL.extend(self.__renderCategory(catName, fkList=relatedList, highLight=highLight, maxItems=maxItems, filterDelivery=filterDelivery, deliveryType=deliveryType))
            numCategoriesRendered += 1

        #  --------
        # JDW regenerate full item list -
        #
        itemNameList = []
        for catName in adjacentCategories:
            itemNameList.extend(self.__dApi.getItemNameList(catName))
        aR = {}
        aR = self.__getRelativesAdjacent(itemNameList)
        #
        # --------
        lD = {}
        #
        for itemName in itemNameList:
            if filterDelivery and not self.__isItemUsed(itemName=itemName, deliveryType=deliveryType):
                continue
            tD = aR[itemName]
            for parentItemName in tD["parentItems"]:
                if filterDelivery and not self.__isItemUsed(itemName=parentItemName, deliveryType=deliveryType):
                    continue
                catName = CifName.categoryPart(itemName)
                attName = CifName.attributePart(itemName)
                catParent = CifName.categoryPart(parentItemName)
                attParent = CifName.attributePart(parentItemName)
                #
                if (itemName, parentItemName) in lD:
                    continue
                if catParent not in adjacentCategories:
                    continue
                if catParent != catName:
                    oL.append(" _%s:__%s:w -> _%s:__%s:w;" % (catName, attName, catParent, attParent))
                else:
                    oL.append(" _%s:__%s:e -> _%s:__%s:e;" % (catName, attName, catParent, attParent))

                lD[(itemName, parentItemName)] = 1
                lD[(parentItemName, itemName)] = 1

            for childItemName in tD["childItems"]:
                if filterDelivery and not self.__isItemUsed(itemName=childItemName, deliveryType=deliveryType):
                    continue
                catName = CifName.categoryPart(itemName)
                attName = CifName.attributePart(itemName)
                catChild = CifName.categoryPart(childItemName)
                attChild = CifName.attributePart(childItemName)
                #
                if (itemName, childItemName) in lD:
                    continue
                if catChild not in adjacentCategories:
                    continue
                if catChild != catName:
                    oL.append(" _%s:__%s:w -> _%s:__%s:w;" % (catChild, attChild, catName, attName))
                else:
                    oL.append(" _%s:__%s:e -> _%s:__%s:e;" % (catChild, attChild, catName, attName))

                lD[(itemName, childItemName)] = 1
                lD[(childItemName, itemName)] = 1

        oL.append("}")
        return oL, numCategoriesRendered

    def makeNeighborFigure(
        self,
        categoryName,
        graphTitle=None,
        graphSubTitle=None,
        titleFormat="text",
        figFormat="svg",
        size=None,
        maxItems=20,
        filterDelivery=False,
        deliveryType="archive",
        neighborCategoryList=None,
        maxCategories=None,
        cleanup=False,
        imageFilePath=None,
    ):
        """Driver method to create diagrams of data category relationships between the input category and either all
        of its adjacent neighbors or for selected categories in 'neighborCategoryList'.

        Optionally apply filtering to categories in current use within the archive.

        maxItems       controls target maximum number of attributes in any category object depiction.
        maxCategories  limits the number of related category objects depicted.
        cleanup        True to remove 'dot' files after processing

        Output files are in SVG format, named and stored in conventional locations for this application.

        """
        logger.debug("deliveryType %r neighborCategoryList %r ", deliveryType, neighborCategoryList)
        dotList, numCategoriesRendered = self.__generateDotInstructions(
            categoryName,
            graphTitle=graphTitle,
            graphSubTitle=graphSubTitle,
            titleFormat=titleFormat,
            maxItems=maxItems,
            filterDelivery=filterDelivery,
            deliveryType=deliveryType,
            neighborCategoryList=neighborCategoryList,
            maxCategories=maxCategories,
        )
        logger.debug("deliveryType %r numCategoriesRendered %d", deliveryType, numCategoriesRendered)
        if numCategoriesRendered == 0:
            return False
        #
        if imageFilePath is None:
            dotfn = os.path.join(self.__pI.getDictCategoryImagePath(), categoryName + "_neighbors.dot")
            svgfn = os.path.join(self.__pI.getDictCategoryImagePath(), categoryName + "_neighbors.svg")
            if filterDelivery:
                dotfn = os.path.join(self.__pI.getDictCategoryImagePath(), categoryName + "_neighbors_" + deliveryType + ".dot")
                svgfn = os.path.join(self.__pI.getDictCategoryImagePath(), categoryName + "_neighbors_" + deliveryType + ".svg")
        else:
            dotfn = os.path.join(imageFilePath, categoryName + "_neighbors.dot")
            svgfn = os.path.join(imageFilePath, categoryName + "_neighbors.svg")
            if filterDelivery:
                dotfn = os.path.join(imageFilePath, categoryName + "_neighbors_" + deliveryType + ".dot")
                svgfn = os.path.join(imageFilePath, categoryName + "_neighbors_" + deliveryType + ".svg")
        #
        #
        ofh = open(dotfn, "w", encoding="utf-8")
        ofh.write("%s" % "\n".join(dotList))
        ofh.close()
        #
        if size is not None:
            cmd = self.__pathDot + ' -T%s  -Gsize="%s" %s > %s' % (figFormat, size, dotfn, svgfn)
        else:
            cmd = self.__pathDot + " -T%s %s > %s" % (figFormat, dotfn, svgfn)
        ok = os.system(cmd)
        #
        # Remove any failed image files --
        if ok != 0:
            logger.debug("status %s for %s", ok, svgfn)
            cmd = "rm -f  %s" % svgfn
            os.system(cmd)
        #
        if cleanup:
            cmd = "rm -f  %s" % dotfn
            os.system()
        #
        return ok == 0


if __name__ == "__main__":
    pass
