from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ApplySignaturesInputData(TcBaseObj):
    """
    This structure contains input parameters required for applyDigitalSignatures operation.    
    
    :var object: Target business object to which Digital Signature is to be applied.
    :var encryptedString: CMS (Cryptographic Message Syntax ) string.
    """
    object: BusinessObject = None
    encryptedString: str = ''


@dataclass
class GetSignatureMessagesOutput(TcBaseObj):
    """
    This structure contains computed signature message.
    
    :var targetObject: Target object for which signature message is computed.
    :var message: Signature message computed for the targetObject.
    """
    targetObject: BusinessObject = None
    message: str = ''


@dataclass
class GetSignatureMessagesResponse(TcBaseObj):
    """
    This structure contains the output parameters of the getSignatureMessages service operation.
    
    :var output: List of getSignatureMessagesOuput structures. 
    :var serviceData: ServiceData Containing list of partial errors and details of business objects for which signature
    message computation was not successful.
    """
    output: List[GetSignatureMessagesOutput] = ()
    serviceData: ServiceData = None


@dataclass
class VoidSignaturesInputData(TcBaseObj):
    """
    This structure contains input parameters required for voidDigitalSignatures operation.
    
    :var targetObject: business object on which digital signatures are to be voided.
    :var signatureobject: List of digital signature objects to be voided.
    :var comment: User comments (optional).
    """
    targetObject: BusinessObject = None
    signatureobject: List[BusinessObject] = ()
    comment: str = ''
