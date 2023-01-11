##
# File:    HtmlPathInfo.py
# Author:  jdw
# Date:    19-Aug-2013
# Version: 0.001
#
# Updates:
#
#  30-Sep-2013  jdw add paths for directories containing images -
#  28-Dec-2020  jdw cleanup and py39
##
"""
Classes to manage physical organization and path information for the HTML rendering of dictionaries.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2,0"


import logging
import os

logger = logging.getLogger(__name__)


class HtmlPathInfo(object):
    def __init__(self, dictFilePath, dictDirectoryName=None, htmlDocsPath=".", htmlTopDirectoryName="dictionaries", verbose=False):
        """Manage the physical organization and path information for the HTML rendering of dictionaries."""
        self.__verbose = verbose
        self.__dictFilePath = dictFilePath
        self.__htmlDocsPath = htmlDocsPath
        self.__htmlTopDir = htmlTopDirectoryName
        #
        #  Assign the subdirectory name for the input dictionary  from dictionary file path.
        #
        self.__dictDirectoryName = self.__getDictName(dictFilePath) if dictDirectoryName is None else dictDirectoryName
        #
        # Full path to target content path - Typically HTDOCs root path plus "dictionaries"
        #
        self.__topPath = self.__setTopPath(self.__htmlDocsPath, self.__htmlTopDir)
        #
        # The HTML rendering is divided into the logical sections that are mapped to physical paths in this module.
        self.__contentTypeList = [("Index", "Dictionary"), ("Groups", "Category Groups"), ("Categories", "Data Categories"), ("Items", "Data Items"), ("Data", "Supporting Data")]
        #
        self.__contentTypeD = {}
        for v in self.__contentTypeList:
            self.__contentTypeD[v[0]] = v[1]
        #

    def getContentTypeList(self):
        """Major content types (subdirectories) within the generated HTML content."""
        return [v[0] for v in self.__contentTypeList]

    def getContentTypeDisplayName(self, contentType):
        try:
            return self.__contentTypeD[contentType]
        except Exception as e:
            logger.error("HtmlGenerator.getContentTypeDisplayName() failed for %s", contentType)
            logger.exception("Failing with %s", str(e))
            return ""

    def getDictFilePath(self):
        """Full path to target dictionary text file."""
        return self.__dictFilePath

    def getHtmlDocsPath(self):
        """HTTPD document root -"""
        return self.__htmlDocsPath

    def getHtmlTopDirectoryName(self):
        """Relative path within the HTTPD document root containing HTML content."""
        return self.__htmlTopDir

    def getHtmlTopPath(self):
        """Full path to dictectory containing HTML content."""
        return self.__topPath

    def getDictDirectoryName(self):
        return self.__dictDirectoryName

    def getContentTypeIndexUrl(self, contentType):
        return os.path.join("/", self.__htmlTopDir, self.__dictDirectoryName, contentType, "index.html")

    def getContentTypeIndexPath(self, contentType):
        return os.path.join(self.__topPath, self.__dictDirectoryName, contentType, "index.html")

    def __escapeFileName(self, name):
        """Handle limited set of cases of a file names containing problematic characters -"""
        return name.replace("/", "_over_")

    def getContentTypeObjUrl(self, contentObjName, contentType):
        return os.path.join("/", self.__htmlTopDir, self.__dictDirectoryName, contentType, self.__escapeFileName(contentObjName) + ".html")

    def getContentTypeObjPath(self, contentObjName, contentType):
        return os.path.join(self.__topPath, self.__dictDirectoryName, contentType, self.__escapeFileName(contentObjName) + ".html")

    def getContentTypePath(self, contentType):
        return os.path.join(self.__topPath, self.__dictDirectoryName, contentType)

    def getDictContentPath(self):
        return os.path.join(self.__topPath, self.__dictDirectoryName)

    def getDictCategoryImagePath(self):
        return os.path.join(self.__topPath, self.__dictDirectoryName, "Images", "Categories")

    def getDictCategoryImageDirUrl(self):
        return os.path.join("/", self.__htmlTopDir, self.__dictDirectoryName, "Images", "Categories")

    def getDictItemImagePath(self):
        return os.path.join(self.__topPath, self.__dictDirectoryName, "Images", "Items")

    def __getDictName(self, dictFilePath):
        """Extract the dictionary name from the dictioary file path."""
        try:
            (_, fN) = os.path.split(dictFilePath)
            return fN
        except Exception as e:
            logger.error("HtmlGenerator.__getDictName() failed for %s", dictFilePath)
            logger.exception("Failing with %s", str(e))
        return None

    def __setTopPath(self, htmlDocsPath, htmlTopDir):
        """Set a writeable path corresponding to the top path to contain generated html content.

        Input path corresponds to the html document root  path for the target web server.

        Returns:  Top writeable path for html generated content or None

        """
        try:
            htmlDocsPath = os.path.abspath(htmlDocsPath)
            pth = os.path.join(htmlDocsPath, htmlTopDir)
            if not os.access(pth, os.W_OK):
                os.makedirs(pth, 0o755)
            return pth

        except Exception as e:
            logger.error("HtmlGenerator.setTopPath() setting to content path failed for %s %s", htmlDocsPath, htmlTopDir)
            logger.exception("Failing with %s", str(e))
        return None

    #
    # OBSOLETE
    def getCategoryUrl(self, categoryName):
        return os.path.join("/", self.__htmlTopDir, self.__dictDirectoryName, "Categories", categoryName + ".html")

    def getGroupUrl(self, groupName):
        return os.path.join("/", self.__htmlTopDir, self.__dictDirectoryName, "Groups", groupName + ".html")

    def getItemUrl(self, itemName):
        return os.path.join("/", self.__htmlTopDir, self.__dictDirectoryName, "Items", itemName + ".html")

    def getDataUrl(self, dataName):
        return os.path.join("/", self.__htmlTopDir, self.__dictDirectoryName, "Data", dataName + ".html")
