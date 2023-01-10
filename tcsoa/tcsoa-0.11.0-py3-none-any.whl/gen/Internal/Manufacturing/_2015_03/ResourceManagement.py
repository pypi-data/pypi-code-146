from __future__ import annotations

from typing import List
from tcsoa.gen.Manufacturing._2013_12.ResourceManagement import RMFileTicket
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GtcPackageImportResult(TcBaseObj):
    """
    Information related to importing a product from a GTC Package.
    
    
    :var status: The resulting status of an attempt to perform a GTC package import. 
    If the status value is 0, the import step succeeded. If it is not 0, the import step failed. 
    The details why the import failed are described in the report.
    
    :var icoId: The Classification Object ID of the imported product.
    
    :var icoUid: The Unique ID of the Classification Object of the imported product.
    :var wsoUid: The Unique ID of the workspace object of the imported product.
    
    :var classId: The ID of the class of the product's classifying Classification Object.
    
    :var report: A list of reports containing information, warnings, and errors related to importing the product.
    """
    status: int = 0
    icoId: str = ''
    icoUid: str = ''
    wsoUid: str = ''
    classId: str = ''
    report: List[str] = ()


@dataclass
class ImportStep3DModels2Response(TcBaseObj):
    """
    Information related to importing 3D model data from a GTC package.
    
    :var serviceData: Service data that can contain error descriptions.
    
    :var importStep3DModelResults: Information related to importing 3D model data from a GTC Package.
    
    """
    serviceData: ServiceData = None
    importStep3DModelResults: List[GtcPackageImportResult] = ()


@dataclass
class ImportStepP21Files3Response(TcBaseObj):
    """
    Information related to importing the products from STEP Part 21 files.
    
    :var serviceData: Service data that can contain error descriptions.
    
    :var logFileTicket: The File Management Service's (FMS) ticket for the STEP Part 21 import log file.
    
    :var importStepP21ProductResults: A list of information related to importing the products from STEP Part 21 files.
    """
    serviceData: ServiceData = None
    logFileTicket: RMFileTicket = None
    importStepP21ProductResults: List[GtcPackageImportResult] = ()


@dataclass
class MapClassificationObjectResponse(TcBaseObj):
    """
    Information related to mapping ICOs from one Classification class to another.
    
    :var serviceData: Service data that can contain error descriptions.
    
    :var targetIcoUid: The Teamcenter unique ID of the target ICO that the source ICO was mapped to.
    :var targetWsoUid: The Teamcenter unique ID of the target workspace object that the source ICO was mapped to.
    """
    serviceData: ServiceData = None
    targetIcoUid: str = ''
    targetWsoUid: str = ''


@dataclass
class UnzipGtcPackageResponse(TcBaseObj):
    """
    Information related to GTC package that was unzipped on the Teamcenter server.
    
    :var serviceData: Service data that can contain error descriptions.
    
    :var gtcPackageServerDirectory: The relative server-sided directory (based on the TC_DATA directory) where the GTC
    package was unzipped into.
    """
    serviceData: ServiceData = None
    gtcPackageServerDirectory: str = ''
