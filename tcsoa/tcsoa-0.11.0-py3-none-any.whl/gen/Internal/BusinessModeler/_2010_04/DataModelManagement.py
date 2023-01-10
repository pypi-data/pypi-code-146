from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TemplateFileInput(TcBaseObj):
    """
    Holds the template information for the 'getTemplateFiles' operation
    
    :var templateDirectory: A directory containing the template related file.
    :var templateFile: A template related file.
    """
    templateDirectory: str = ''
    templateFile: str = ''


@dataclass
class TemplateFileOutput(TcBaseObj):
    """
    Holds output data for a given template related file.
    
    :var templateDirectory: A directory containing template related files.
    :var templateFile: A template related file.
    :var templateFileTicket: This ticket is for the file 'templateFile' located at 'templateDirectory' on server.
    :var timestamp: The datetime stamp of the template related file.
    """
    templateDirectory: str = ''
    templateFile: str = ''
    templateFileTicket: str = ''
    timestamp: datetime = None


@dataclass
class TemplateFilesResponse(TcBaseObj):
    """
    Holds the response data of the 'getTemplateFiles' operation.
    
    :var outputs: A list of 'TemplateFileOutput' structures that contain the set of template data retrieved for each
    specified input 'TemplateFileInput'.
    :var serviceData: Status of the operation. Partial error may include following error codes
    - 216012 : Input directory not found
    
    """
    outputs: List[TemplateFileOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ChangedTemplateFileInput(TcBaseObj):
    """
    Input data for a given template related file.
    
    :var templateDirectory: A directory in Teamcenter Server installation containing the template related file. All
    template files are stored in $TC_DATA\model directory.
    :var templateFile: A template related file.
    :var timestamp: The datetime stamp of the templateFile to use for comparison with the datetime stamp of that same
    file in the OS.
    """
    templateDirectory: str = ''
    templateFile: str = ''
    timestamp: datetime = None


@dataclass
class DataModelDeploymentInput(TcBaseObj):
    """
    'DataModelDeploymentInput' structure represents parameters required for deploying data model.
    
    :var deploymentFileTicket: FMS ticket for a data model XML file of a type specified by 'deploymentFileType'.
    
    :var deploymentFileType: The type of file. The type can be '0, 1 or 2'. The value '0' is for template file, '1' is
    for template dependency file and '2' is for template language file.
    """
    deploymentFileTicket: str = ''
    deploymentFileType: int = 0
