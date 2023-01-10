from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExtensionAttachmentTypeDetails(TcBaseObj):
    """
    ExtensionAttachmentTypeDetails represents a list of AttachmentTypeDetailElement for each extension name.
    
    :var extensionName: Extension name that needs to be compared.
    An extension name is the ID of a "serverExtension" registered in Accountability Check&rsquo;s plugin.xml. It can be
    located in com.teamcenter.rac.cme.accountabilitycheck.relations package. The server extension for Attachments is
    "Mfg0dataset_form".
    :var attachmentTypesDetails: A list of details of each attachment type.
    """
    extensionName: str = ''
    attachmentTypesDetails: List[AttachmentTypeDetailElement] = ()


@dataclass
class AttachmentComparisonDetailsResponse(TcBaseObj):
    """
    AttachmentComparisonDetailsResponse represents a list of AttachmentTypeDetails element and ServiceData.
    
    :var details: A list of AttachmentType detail elements - one for each input equivalent set.
    :var serviceData: Object that captures any partial errors.
    """
    details: List[AttachmentTypeDetail] = ()
    serviceData: ServiceData = None


@dataclass
class AttachmentDetail(TcBaseObj):
    """
    AttachmentDetail holds a set of attachments&rsquo; tag and match type information for each line in input equivalent
    set.
    
    :var attachments: For each BOMLine in input equivalent set holds the attachment objects. Attachments can be both
    Dataset and Form objects.
    :var matchType: To indicate the type of match between attachments.
    Probable values can only be from the set {0, 1, 2} which represents the set {"Full Match", "Source Modified",
    "Target Modified"} respectively.
    """
    attachments: List[BusinessObject] = ()
    matchType: int = 0


@dataclass
class AttachmentTypeDetail(TcBaseObj):
    """
    AttachmentTypeDetail pairs the ExtensionAttachmentTypeDetails element and a list of equivalent BOMLines with an
    index.
    
    :var index: Index of the input equivalent set for which these details were calculated.
    :var equivalentLines: A list of all equivalent lines in the input equivalent set (all equivalent sources in
    sequence and then all targets in sequence) of MEProcess,  MEOp and MEWorkarea for which attachments are to be
    compared.
    :var attachmentExtDetails: A list of attachment type details of this equivalent set.
    """
    index: int = 0
    equivalentLines: List[BusinessObject] = ()
    attachmentExtDetails: List[ExtensionAttachmentTypeDetails] = ()


@dataclass
class AttachmentTypeDetailElement(TcBaseObj):
    """
    AttachmentTypeDetailElement contains a list of all the attachments for a particular attachment relation type.
    
    :var attachmentRelType: The relation type of attachment (Cps0LBRel, IMAN_SPECIFICATION, Cps0RobotProgRel etc.)
    :var attachmentsDetails: A list of details of the attachment for each line in input equivalent set.
    """
    attachmentRelType: BusinessObject = None
    attachmentsDetails: List[AttachmentDetail] = ()
