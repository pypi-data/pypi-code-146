##
# File:    HtmlGenerator.py
# Author:  jdw
# Date:    19-Aug-2013
# Version: 0.001
#
#  Updates:
#   10-Mar-2018 jdw Py2-P3 and refactor for Python packaging --
#   30-Dec-2020 jdw cleanup and Py39
##
"""
Classes to manage creation of files and directories representing PDBx/mmCIF
dictionaries in HTML format.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2,0"


import logging
import os
import shutil
import stat

logger = logging.getLogger(__name__)


class HtmlTemplates(object):
    def __init__(self):
        #
        # These are very thin templates that rely on server-side includes for
        # the particulars.
        #
        # Top of page template
        #
        self.__templatePageHeader = """<!DOCTYPE html>
<html lang="en">
  <head>
   <!--#include virtual="/includes/head_common_bs.html"-->
    <meta name="description" content="PDBx/mmCIF Data Dictionary %s">
    <meta name="author" content="Worldwide Protein Data Bank">
    <title>%s</title>
  </head>

  <body>
    <!-- Wrap all page content here -->
    <div id="wrap">

      <!--#include virtual="/includes/page_header_bs.html"-->
      <div class="container">
    """
        #
        self.__templatePdbmlPageHeader = """<!DOCTYPE html>
<html lang="en">
  <head>
   <!--#include virtual="/includes/head_common_bs.html"-->
    <meta name="description" content="PDBx/mmCIF Resources %s">
    <meta name="author" content="Worldwide Protein Data Bank">
    <title>%s</title>
  </head>

  <body>
    <!-- Wrap all page content here -->
    <div id="wrap">

      <!--#include virtual="/includes/pdbml_page_header_bs.html"-->
      <div class="container">
    """
        #
        self.__templatePageTrailer = """
     </div> <!-- end top container-->
     </div> <!-- end wrap -->

    <!-- END TEXT HERE  -->
    <!--#include virtual="/includes/page_javascript_bs.html"-->
    <!--#include virtual="/includes/page_footer_bs.html"-->
  </body>
</html>
    """
        #

    def getPageHeader(self, title="Pdbx/mmCIF Dictionary Resources"):
        return self.__templatePageHeader % (title, title)

    def getPdbmlPageHeader(self, title="Pdbx/mmCIF Dictionary Resources"):
        return self.__templatePdbmlPageHeader % (title, title)

    def getPageTrailer(self):
        return self.__templatePageTrailer

    def getPageTitle(self, title, subTitle):
        oL = []
        oL.append('    <div class="my-page-header">')
        oL.append("      <h2>%s <small>%s</small></h2>" % (title, subTitle))
        oL.append("    </div>")
        return "\n".join(oL)

    def getTopNavbar(self, navTitle, contentTypeKey, pathInfoObj):
        #  Template for tabbed navigation within each generated page.
        #
        #  Customizable: title, subtitle, and a key to set a tab active property.
        #
        pI = pathInfoObj
        contentTypeList = pI.getContentTypeList()

        oL = []
        oL.append('    <div class="row">')
        oL.append('      <div class="col-md-1 my-nav-title"><div class="pull-right"> <h4>%s</h4></div></div>' % navTitle)
        oL.append('       <div class="col-md-11">')
        oL.append('        <ul class="nav nav-tabs">')
        for contentType in contentTypeList:
            dN = pI.getContentTypeDisplayName(contentType)
            sUrl = pI.getContentTypeIndexUrl(contentType)
            if contentType == contentTypeKey:
                oL.append('<li class="active">               <a href="%s">%s</a></li>' % (sUrl, dN))
            else:
                oL.append('<li               >               <a href="%s">%s</a></li>' % (sUrl, dN))
        oL.append("</ul>")
        oL.append("</div>")
        oL.append("</div>")
        return "\n".join(oL)

    def getTopNavbarSimple(self, contentTypeKey, pathInfoObj):
        #  Template for tabbed navigation within each generated page.
        #
        #  Customizable: title, subtitle, and a key to set a tab active property.
        #
        pI = pathInfoObj
        contentTypeList = pI.getContentTypeList()

        oL = []
        oL.append('    <div class="row">')
        # oL.append('      <h2>%s <small>%s</small></h2>' % (title,subTitle))
        oL.append('       <ul class="nav nav-tabs">')
        for contentType in contentTypeList:
            dN = pI.getContentTypeDisplayName(contentType)
            sUrl = pI.getContentTypeIndexUrl(contentType)
            if contentType == contentTypeKey:
                oL.append('<li class="active">               <a href="%s">%s</a></li>' % (sUrl, dN))
            else:
                oL.append('<li               >               <a href="%s">%s</a></li>' % (sUrl, dN))
        oL.append("</ul>")
        oL.append("</div>")
        return "\n".join(oL)


class HtmlGenerator(object):
    """HTML file and directory generator utilities."""

    def __init__(self, pathInfoObj, verbose=False):
        """"""
        self.__verbose = verbose
        self.__pI = pathInfoObj
        self.__subDirPath = self.__pI.getDictDirectoryName()
        self.__htmlTopPath = self.__pI.getHtmlTopPath()
        self.__contentTypeList = self.__pI.getContentTypeList()

    def makeDirectories(self, purge=False):
        return self.__makeDirs(self.__subDirPath, self.__htmlTopPath, purge=purge)

    def __makeDirs(self, subDirPath, htmlTopPath, purge=True):
        """internal method to make directory tree for HTML content generation."""
        try:
            pth = self.__pI.getDictContentPath()
            if purge and os.access(pth, os.F_OK):
                shutil.rmtree(pth)
            #
            for contentType in self.__contentTypeList:
                pth = self.__pI.getContentTypePath(contentType)
                if not os.access(pth, os.F_OK):
                    os.makedirs(pth, 0o755)

            pth = self.__pI.getDictCategoryImagePath()
            if not os.access(pth, os.F_OK):
                os.makedirs(pth, 0o755)

            pth = self.__pI.getDictItemImagePath()
            if not os.access(pth, os.F_OK):
                os.makedirs(pth, 0o755)
            return True
        except Exception as e:
            logger.error("HtmlGenerator.__makeDirs() failed for %s and %s", subDirPath, htmlTopPath)
            logger.exception("Failing with %s", str(e))
        return False

    def writeHtmlFile(self, contentObjName, title, subTitle, contentType, htmlContentList, navBarContentType="default"):
        """Render a standard page using common header and footer and navbar.

        Input HTML content list is inserted within the body of the page.

        """
        try:
            navBarContentSelector = contentType if navBarContentType == "default" else navBarContentType
            filePath = self.__pI.getContentTypeObjPath(contentObjName, contentType)
            logger.debug("writing file %s", filePath)

            ht = HtmlTemplates()
            ofh = open(filePath, "w", encoding="utf-8")
            pageTitle = str(title) + " " + str(subTitle)
            ofh.write("%s\n" % ht.getPageHeader(title=pageTitle))
            ofh.write("%s\n" % ht.getPageTitle(title, subTitle))
            ofh.write("%s\n" % ht.getTopNavbar("Browse:", navBarContentSelector, self.__pI))
            ofh.write("%s" % "\n".join(htmlContentList))

            ofh.write("%s\n" % ht.getPageTrailer())
            ofh.close()
            st = os.stat(filePath)
            os.chmod(filePath, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            return True
        except Exception as e:
            logger.error("failed for %s", filePath)
            logger.exception("Failing with %s", str(e))
        return False


if __name__ == "__main__":
    pass
