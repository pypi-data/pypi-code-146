from __future__ import annotations

from tcsoa.gen.BusinessObjects import Dataset
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class DigitalSignSaveInput(TcBaseObj):
    """
    The digitalSigningSave input structure.
    
    :var baseObj: The Dataset object that contains the named reference file to be signed.  This is required.
    :var signedFileTicket: The FMS file ticket for uploading the signed file.  This is required.
    :var createToolName: The tool name that is used to sign the file.  This is required.
    :var validSignature: If this is set to true, then the signature is valid; otherwise, it is not.  If the signing
    tool does not declare the signature is valid, then the base dataset will not be checkin.
    :var userNameWhoSign: The Teamcenter user name that completed the digitally sign operation.
    :var signTime: The timestamp of the digital signature in the signing tool.
    """
    baseObj: Dataset = None
    signedFileTicket: str = ''
    createToolName: str = ''
    validSignature: bool = False
    userNameWhoSign: str = ''
    signTime: str = ''


@dataclass
class DigtalSigningSaveResponse(TcBaseObj):
    """
    Digital signing save operation response
    
    :var basedDataset: If the Dataset is updated successfully, then the Dataset is returned.
    :var serviceData: The partial error list if there is any system errors.
    """
    basedDataset: Dataset = None
    serviceData: ServiceData = None
