from __future__ import annotations

from tcsoa.gen.BusinessObjects import InstalledTemplates
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class SiteTemplateDeployInfoResponse(TcBaseObj):
    """
    The response data for the 'getSiteTemplateDeployInfo' operation.
    
    :var siteID: Site ID of the current database
    :var siteName: Site name of the current database
    :var serviceData: Status of the operation.
    :var templatesDeployInfo: list of 'InstalledTemplate' objects
    """
    siteID: str = ''
    siteName: str = ''
    serviceData: ServiceData = None
    templatesDeployInfo: List[InstalledTemplates] = ()


@dataclass
class DeployDataModelResponse(TcBaseObj):
    """
    This is the response that the service returns to the caller of the 'deployDataModel2'. It contains the info about
    the status of the operation, logfiles, the site and the related data.
    
    :var siteID: The site ID of the database to which the connection is established.
    
    :var siteName: The name of the database site to which connection is established.
    :var templateDeployInfo: the 'TemplateDeployInfo' object containing details from 'InstalledTemplates' table for the
    deployed template in the Database.
    :var serviceData: A 'ServiceData' structure containing the status of the operation execution
    :var logFileTickets: List of file tickets for the output log file(s) showing the results of the business model
    updater
    """
    siteID: str = ''
    siteName: str = ''
    templateDeployInfo: InstalledTemplates = None
    serviceData: ServiceData = None
    logFileTickets: List[str] = ()
