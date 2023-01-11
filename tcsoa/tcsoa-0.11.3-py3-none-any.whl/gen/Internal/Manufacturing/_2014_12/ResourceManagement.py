from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetVendorCatalogInfo2Response(TcBaseObj):
    """
    Contains a ServiceData object that may contain error descriptions, if any errors occurred, and a list of catalog
    information objects providing detailed information about Generic Tool Catalog vendor catalogs that are stored on
    the Teamcenter server.
    
    :var serviceData: The service data
    :var catalogInfo: The vendor catalog information
    """
    serviceData: ServiceData = None
    catalogInfo: List[CatalogInfo2] = ()


@dataclass
class CatalogInfo2(TcBaseObj):
    """
    The structure contains vendor catalog information 
    
    
    :var vendorName: The name of the tool vendor company providing the catalog
    :var vendorAcronym: An acronym for the tool vendor providing the catalog, usually consisting of two or three
    characters 
    :var gtcHierarchyVersion: The Generic Tool Catalog version number, in the format:VR, for example "V1R7"
    :var gtcPackageId: A unique identifier for this Generic Tool Catalog package
    :var vendorCatalogVersion: The version of the catalog
    :var vendorCatalogLanguage: The language of the catalog
    :var vendorCatalogDescription: A long description of the catalog
    :var vendorCatalogShortDescription: A short description of the catalog
    :var vendorCatalogId: A unique ID for the catalog
    :var vendorCatalogRootClassId: The ID of the catalog's root class in the Generic Tool Catalog's Classification
    hierarchy when the catalog gets imported, typically the concatenation of the vendor's acronym and "_GTC"
    :var vendorCatalogRootDir: The root directory where the tool vendor catalog is stored on the Teamcenter server
    :var gtcPackageCreationDate: The creation date of the Generic Tool Catalog package, in the format yyyymmdd_hhmmss
    """
    vendorName: str = ''
    vendorAcronym: str = ''
    gtcHierarchyVersion: str = ''
    gtcPackageId: str = ''
    vendorCatalogVersion: str = ''
    vendorCatalogLanguage: str = ''
    vendorCatalogDescription: str = ''
    vendorCatalogShortDescription: str = ''
    vendorCatalogId: str = ''
    vendorCatalogRootClassId: str = ''
    vendorCatalogRootDir: str = ''
    gtcPackageCreationDate: str = ''
