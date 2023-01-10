from __future__ import annotations

from tcsoa.gen.BusinessObjects import ImanFile, Dataset
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LoadPlmdTicketReplaceOutput(TcBaseObj):
    """
    Output
    
    :var referenceCount: Number of files attached to the Dataset.
    :var ticket: The requested PLMD file transient ticket.
    :var datasetName: Dataset name.
    :var fileNameExt: List of file names extensions.
    :var fileNames: List of file names attached to the Dataset.
    """
    referenceCount: int = 0
    ticket: str = ''
    datasetName: str = ''
    fileNameExt: List[str] = ()
    fileNames: List[str] = ()


@dataclass
class LoadPlmdTicketReplaceResponse(TcBaseObj):
    """
    Response
    
    :var output: A map(Dataset, LoadPlmdTicketReplaceOutput) of input Dataset objects to the required Replace File
    information.
    :var serviceData: Updated Dataset, ImanFile objects and partial errors if any.
    """
    output: DatasetPlmdResponse = None
    serviceData: ServiceData = None


@dataclass
class DatashareManagerReplaceInfo(TcBaseObj):
    """
    Input information about the Dataset and file to be replaced.
    
    :var dataset: The Dataset object to which the referenced ImanFile objects(s) is to be uploaded to.
    :var imanFile: The ImanFile currently referenced by the Dataset. This named reference is intended to be replaced by
    the operation.
    :var namedReferenceName: The name of the reference type relation binding the Dataset to the ImanFile object file.
    This input is used to ensure that the right file is being replaced since Dataset named reference uniqueness is
    based on the named Reference name in addition to the ImanFile.
    :var absoluteFilePath: The absolute file path of the file being uploaded on the client host. This file Path is used
    to generate the "original File name". If empty, an internally generated name is used.
    """
    dataset: Dataset = None
    imanFile: ImanFile = None
    namedReferenceName: str = ''
    absoluteFilePath: str = ''


"""
Map of Dataset and LoadPlmdTicketReplaceOutput.
"""
DatasetPlmdResponse = Dict[Dataset, LoadPlmdTicketReplaceOutput]
