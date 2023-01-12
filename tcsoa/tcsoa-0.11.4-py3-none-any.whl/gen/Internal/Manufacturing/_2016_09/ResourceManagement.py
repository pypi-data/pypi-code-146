from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetVendorCatalogInfo3Response(TcBaseObj):
    """
    A list of catalog info objects that contain information about all valid vendor catalogs of the requested types that
    are available on the Teamcenter server machine.
    Each catalog info object from this list contains detailed information about the catalog (see below). It also
    contains a unique catalog ID that can be used to identify the catalog lateron. Its  root class ID identifies under
    which root class this vendor catalog will reside in Teamcenter's vendor catalog classification hierarchy once it is
    imported.
    The root directory information contains the absolute path of the directory where the catalog resides on the
    Teamcenter server. Only valid catalogs of the requested types will be returned. If a corrupted catalog is found,
    for example if it is missing mandatory files or directories, this catalog's information will not be returned in the
    list of catalog information objects. If this operation finds such corrupted catalogs, it continues searching for
    other valid catalogs and returns all valid catalogs of the requested types.
    
    :var serviceData: The service data.
    :var catalogInfo: A list of catalog infos.
    """
    serviceData: ServiceData = None
    catalogInfo: List[CatalogInfo3] = ()


@dataclass
class CatalogInfo3(TcBaseObj):
    """
    The structure contains vendor catalog information for GTC V1 and GTC V2.
    
    :var vendorName: The name of the tool vendor company providing the catalog.
    :var vendorAcronym: An acronym for the tool vendor providing the catalog, usually consisting of two or three
    characters.
    :var gtcHierarchyVersion: The Generic Tool Catalog version number. For GTC V1 packages the format is defined by
    "V<version>R<revision>", for example "V1R7"; for GTC V2 packages the format is for example "0.1.0".
    :var gtcPackageId: A unique identifier for this Generic Tool Catalog package.
    :var logoUrl: {GTC-V2 only} The filepath of the package logo.
    :var disclaimerText: {GTC-V2 only} The disclaimer text in the current Teamcenter language. If the disclaimer does
    not exist in the current language, the english text will be returned.
    :var gtcVersion: The version of this GTC package, for example "1" for V1 or "2" for V2.
    :var vendorHierarchyVersion: {GTC V2 only} The version of the GTC class hierarchy that is used in this package.
    :var downloadSecurity: {GTC V2 and online packages only} This value states if the tool vendor would like to set a
    control on package data release or not. Possible values are "yes" and "no". This is an optional value.
    :var onlineConnectionConfiguration: {GTC V2 and online packages only} This value is used for online data download
    only. It refers to a technical configuration file (an URL) that is provided by data senders who support online data
    download.
    :var vendorCatalogVersion: The version of the catalog.
    :var vendorCatalogLanguage: The language of the catalog.
    :var vendorCatalogDescription: A long description of the catalog. (For GTC V2 packages it is returned in the
    current Teamcenter server language.)
    :var vendorCatalogShortDescription: A short description of the catalog. (For GTC v2 packages it is returned in the
    current Teamcenter server language.)
    :var vendorCatalogId: A unique ID for the catalog.
    :var vendorCatalogRootClassId: The ID of the catalog's root class in the Generic Tool Catalog's Classification
    hierarchy when the catalog gets imported, typically the concatenation of the vendor's acronym and "#GTC" -> 
    "<vendorAcronym>#GTC".
    :var vendorCatalogRootDir: The root directory where the tool vendor catalog is stored on the Teamcenter server.
    :var gtcPackageCreationDate: The creation date of the Generic Tool Catalog package, in the format yyyymmdd_hhmmss.
    """
    vendorName: str = ''
    vendorAcronym: str = ''
    gtcHierarchyVersion: str = ''
    gtcPackageId: str = ''
    logoUrl: str = ''
    disclaimerText: str = ''
    gtcVersion: str = ''
    vendorHierarchyVersion: str = ''
    downloadSecurity: str = ''
    onlineConnectionConfiguration: str = ''
    vendorCatalogVersion: str = ''
    vendorCatalogLanguage: str = ''
    vendorCatalogDescription: str = ''
    vendorCatalogShortDescription: str = ''
    vendorCatalogId: str = ''
    vendorCatalogRootClassId: str = ''
    vendorCatalogRootDir: str = ''
    gtcPackageCreationDate: str = ''
