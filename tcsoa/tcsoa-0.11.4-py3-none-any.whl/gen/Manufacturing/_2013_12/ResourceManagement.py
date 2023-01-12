from __future__ import annotations

from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetStepP21FileCountsResponse(TcBaseObj):
    """
    The counts of available STEP P21 product files for the given classes will be returned.
    The following partial errors may be returned:
     - 71513 Invalid class ID
     - 300361 Assortment file cannot be found.
    
    :var serviceData: The service data
    :var countMap: A map of class IDs for which the counts are requested and its corresponding counts.
    """
    serviceData: ServiceData = None
    countMap: MapStringInt = None


@dataclass
class GetVendorCatalogInfoResponse(TcBaseObj):
    """
    A list of all vendor catalogs that are available on the Teamcenter server machine. Each catalog info object
    contains detailed information about each catalog like the name, acronamy, version, language and description.
    Additionally a unique catalog ID is returned that can be used to identify it lateron. The root class ID is the ID
    of the Classification main class for this specific vendor catalog, when it is imported. The root directory that is
    returned is the actual, full directory where the catalog is located. It can be used to start the import of the
    catalog hierarchy using the service operation importVendorCatalogHierarchy.
    Only valid catalogs will be returned. If there is a corrupt catalog (e.g., if one of the mandatory files or
    directories is missing), this catalog will not be returned in the list of catalogs. If one corrupt catalog is
    found, the system continues searching for other valid catalogs and returns all valid ones.
    The following partial errors may be returned:
     - 300300 The preference MRMGTCVendorCatalogRootDir is not defined.
     - 300301 The specified vendor catalog root directory does not exist.
     - 300302 No vendor catalog was found.
    
    
    
    :var serviceData: The service data
    :var catalogInfo: The vendor catalog information
    """
    serviceData: ServiceData = None
    catalogInfo: List[CatalogInfo] = ()


@dataclass
class ImportStepP21FilesResponse(TcBaseObj):
    """
    The importStepP21FilesResponse object that contains the logfile with additional data of the import. When there is a
    failure during the import, an error code will be returned as the part of the service data.
    Possible errors are:
     - 71513 Invalid class ID
     - 300361 Assortment file cannot be found
     - 300362 Mapping file cannot be found
     - 300363 STEP P21 file cannot be found
     - 300324 Invalid import options
     - 300364 Error importing STEP P21 files (details can be found in the import log file (file ticket))
    
    :var serviceData: The service data
    :var logFileTicket: Ticket of the import log file
    """
    serviceData: ServiceData = None
    logFileTicket: RMFileTicket = None


@dataclass
class ImportVendorCatalogHierarchyResponse(TcBaseObj):
    """
    This importVendorCatalogHierarchyResponse object that contains the logfile with additional data for the import.
    When there is a failure during the import, an error code will be returned as the part of the service data.
    
    Possible errors are:
     - 300301 Specified vendor catalog root directory does not exist
     - 300320 Transfer mode cannot be found
     - 300321 Invalid transfer mode tag
     - 300322 Transfer mode object does not exist
     - 300323 Vendor catalog hierarchy import file does not exist
     - 300324 Invalid import options
     - 300325 File ticket for PLMXML log file cannot be created
     - 300326 Error importing vendor catalog hierarchy (details can be found in the import log file (file ticket))
    
    
    
    :var serviceData: Service data that can contain error codes
    :var logFileTicket: Ticket of the import log file
    """
    serviceData: ServiceData = None
    logFileTicket: RMFileTicket = None


@dataclass
class RMFileTicket(TcBaseObj):
    """
    The file information of log file
    
    :var ticket: The FMS file ticket
    :var fileName: The original file name
    """
    ticket: str = ''
    fileName: str = ''


@dataclass
class CatalogInfo(TcBaseObj):
    """
    The structure contains vendor catalog information
    
    :var vendorName: Name of the vendor that provided the catalog
    :var vendorAcronym: Acronym of the vendor that provided the catalog
    :var vendorCatalogVersion: Version of the catalog
    :var vendorCatalogLanguage: Language of the catalog
    :var vendorCatalogDescription: Description of the catalog
    :var vendorCatalogShortDescription: Short description of the catalog
    :var vendorCatalogID: Unique ID of the catalog
    :var vendorCatalogRootClassID: Root class ID of the catalog
    :var vendorCatalogRootDir: Root directory of the catalog
    """
    vendorName: str = ''
    vendorAcronym: str = ''
    vendorCatalogVersion: str = ''
    vendorCatalogLanguage: str = ''
    vendorCatalogDescription: str = ''
    vendorCatalogShortDescription: str = ''
    vendorCatalogID: str = ''
    vendorCatalogRootClassID: str = ''
    vendorCatalogRootDir: str = ''


"""
Map String Int
"""
MapStringInt = Dict[str, int]
