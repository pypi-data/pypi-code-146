from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExtensionMountAttachTypeDetails(TcBaseObj):
    """
    ExtensionMountAttachTypeDetails represents a list of MountAttachDetailTypeElement for each extension name.
    
    :var extensionName: Extension name that needs to be compared.
    An extension name is the ID of a "serverExtension" registered in Accountability Check&rsquo;s plugin.xml. It can be
    located in com.teamcenter.rac.cme.accountabilitycheck.relations package. 
    The server extension for physical connection is "Mfg0MountAttach_Relation".
    :var mountAttachDetailTypes: A list of details of each physical attachment type.
    """
    extensionName: str = ''
    mountAttachDetailTypes: List[MountAttachDetailTypeElement] = ()


@dataclass
class MountAttachComparisonsResponse(TcBaseObj):
    """
    MountAttachComparisonDetailsResponse represents a list of MountAttachTypeDetail element and ServiceData.
    
    :var mountAttachTypeDetails: A list of MountAttachTypeDetail elements - one for each input equivalent set.
    :var serviceData: Object that captures any partial errors.
    """
    mountAttachTypeDetails: List[MountAttachTypeDetail] = ()
    serviceData: ServiceData = None


@dataclass
class MountAttachDetail(TcBaseObj):
    """
    MountAttachDetail holds a set of BOE objects connected using physical attachment relations and match type
    information for each BOMLine in the input equivalent set.
    
    :var attachments: For each BOMLine in input equivalent set holds the physical attachment objects. The physical
    attachments can be both tool and weld gun objects.
    :var matchType: To indicate the type of match between physical attachments. Values are from set {0, 1, 2} which
    represents set {"Full Match", "Source Modified", "Target Modified"} respectively.
    """
    attachments: List[BusinessObject] = ()
    matchType: int = 0


@dataclass
class MountAttachDetailTypeElement(TcBaseObj):
    """
    MountAttachDetailTypeElement contains a list of all the physical attachments for a particular attachment relation
    type.
    
    :var relationType: The relation type of physical attachment (Mfg0MEPhysicalAttachment, Mfg0MEMountToolToRobot).
    :var mountAttachDetails: A list of BOE objects connected using physical attachment relations and match type
    information for each BOMLine in the input equivalent set.
    """
    relationType: BusinessObject = None
    mountAttachDetails: List[MountAttachDetail] = ()


@dataclass
class MountAttachTypeDetail(TcBaseObj):
    """
    MountAttachTypeDetail pairs the ExtensionMountAttachTypeDetails element and a list of equivalent BOMLine objects
    with an index.
    
    :var index: Index of the extension in the input equivalent set for which these details were calculated. It
    represents the order in which the extensions are provided in the input equivalent set.
    :var equivalentLines: A list of all equivalent lines in the input equivalent set (all equivalent sources in
    sequence and then all targets in sequence) of MEWorkarea objects for which attachments are to be compared.
    :var mountAttachTypeExtensions: A list of physical attachment type details of this equivalent set.
    """
    index: int = 0
    equivalentLines: List[BusinessObject] = ()
    mountAttachTypeExtensions: List[ExtensionMountAttachTypeDetails] = ()
