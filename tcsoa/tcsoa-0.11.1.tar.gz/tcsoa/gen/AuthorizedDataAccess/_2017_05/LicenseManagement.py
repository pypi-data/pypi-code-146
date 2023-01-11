from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, VariantRule, RevisionRule
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class LicenseAttachOrDetachInput(TcBaseObj):
    """
    A structure containing license to be attached or removed and propagation context information.
    
    :var attachLicenseDetails: Structure containing data for attach license operation.
    :var detachLicenseDetails: Structure containing data for detach license operation.
    :var contextInfo: A structure of PropagationConfigurationContext.
    :var processAsynchronously: Flag indicating if this operation needs to be processed in asynchronously. A value True
    means to process it asynchronously. If the value is not set or is set to False then processing happens
    synchronously in the same request.
    """
    attachLicenseDetails: LicenseInputDetails = None
    detachLicenseDetails: LicenseInputDetails = None
    contextInfo: PropagationConfigurationContext = None
    processAsynchronously: bool = False


@dataclass
class LicenseInputDetails(TcBaseObj):
    """
    A Structure containing list of selected licenses and objects with the ead paragraph if there is any.
    
    :var selectedLicenses: List of license IDs of ADA licenses. These are strings of each with a maximum of 128 bytes
    size.
    :var objects: List of WorkspaceObject business objects to be either attached or detached from selected list of
    Licenses
    :var eadParagraph: List of authorizing paragraphs for the licenses being attached to WorkspaceObject business
    objects. These are strings with a maximum of 80 bytes size. The size of eadParagraph vector should match the size
    of the selectedLicenses (each entry in eadParagraph maps to corresponding entry in selectedLicenses). If a
    paragraph entry is not applicable for a specific license (paragraph entries are applicable only for licenses of
    ITAR type), then that entry can be left blank. System will ignore any paragraph entry if it is not applicable for a
    license to be attached. This is an optional parameter.
    """
    selectedLicenses: List[str] = ()
    objects: List[BusinessObject] = ()
    eadParagraph: List[str] = ()


@dataclass
class PropagationConfigurationContext(TcBaseObj):
    """
    PropagationConfigurationContext contains data which can be applied to attach to projects and detach from license
    operation.
    
    :var selectedTopLevelObject: Selected top level object in context of ACE ( Active Content Expericence ), if this
    object is passed we will fetch variant rule and revision rule.
    :var variantRule: 
    The VariantRule in context of the assign to project  or attach to license operation.
    :var revisionRule: The RevisionRule associated with the assign to project or attach to license operation.
    :var typeOption: An integer indicating the type of Item or Item Revision, valid values are 0 for Item and 1 for
    Item Revision.
    :var depth: A number indicating how deep the traversal needs to be performed for a given structure, applicable only
    for structures.
    """
    selectedTopLevelObject: BusinessObject = None
    variantRule: VariantRule = None
    revisionRule: RevisionRule = None
    typeOption: int = 0
    depth: int = 0
