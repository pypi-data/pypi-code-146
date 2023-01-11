##
# File:    DictionaryItemCoverage.py
# Author:  jdw
# Date:    28-Oct-2020
# Version: 0.001
#
# Updates:
##
"""
Class providing data item coverage statistics.

"""
__docformat__ = "restructuredtext en"
__author__ = "John Westbrook"
__email__ = "jwest@rcsb.rutgers.edu"
__license__ = "Apache 2,0"

import logging
import os

from rcsb.utils.io.MarshalUtil import MarshalUtil

logger = logging.getLogger(__name__)


HERE = os.path.abspath(os.path.dirname(__file__))
TOPDIR = os.path.dirname(os.path.dirname(HERE))


class DictionaryItemCoverage(object):
    """Methods providing item coverage statistics for PDB archive and chemical reference data files."""

    def __init__(self, coverageDirPath):
        #
        # Paths to data files with coverage statistics -
        #
        self.__pathArchiveItemCounts = os.path.join(coverageDirPath, "scan-pdbx-item-coverage.tdd")
        self.__pathPrdItemCounts = os.path.join(coverageDirPath, "scan-bird-item-coverage.tdd")
        self.__pathCcItemCounts = os.path.join(coverageDirPath, "scan-chem_comp-item-coverage.tdd")
        self.__pathFamilyPrdItemCounts = os.path.join(coverageDirPath, "scan-bird_family-item-coverage.tdd")
        #

    def getItemCoverage(self, deliveryType="archive"):
        """Return a dictionary of usage counts for each data item for the input delivery type.

        deliveryTypes = [ 'archive', 'cc', 'prd', 'family']
        """
        if deliveryType in ["archive"]:
            return self.__getItemCounts(self.__pathArchiveItemCounts)
        elif deliveryType in ["cc"]:
            return self.__getItemCounts(self.__pathCcItemCounts)
        elif deliveryType in ["prd", "bird"]:
            return self.__getItemCounts(self.__pathPrdItemCounts)
        elif deliveryType in ["family", "bird-family"]:
            return self.__getItemCounts(self.__pathFamilyPrdItemCounts)
        else:
            return {}

    def __getItemCounts(self, itemCoverageFilePath):
        #
        mU = MarshalUtil()
        rowList = mU.doImport(itemCoverageFilePath, fmt="tdd", rowFormat="list")
        itemCountD = {}
        for row in rowList:
            itemCountD[row[0]] = int(row[1])
        #
        return itemCountD
