from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AattachmentsCreated(TcBaseObj):
    """
    Details about created attachment.
    
    :var sourceLine: The BOMLine for which attachment line is created. This is same as the incoming source line.
    :var createdObject: The newly created dataset or the form.
    :var attachmentLine: The newly created attachment line.
    :var writeFileTicket: The FMS write-file-ticket of the file.
    """
    sourceLine: BusinessObject = None
    createdObject: BusinessObject = None
    attachmentLine: BusinessObject = None
    writeFileTicket: str = ''


@dataclass
class AttachmentLines(TcBaseObj):
    """
    Information about the attachments of a BOMLine.
    
    :var serviceData: The service data containing partial errors. The following partial error may be returned.
    - 253148: No attachment lines found for the  line.
    
    
    :var attachmentsInfo: The map of the BOMLine and a structure holding the information about its attachments.
    """
    serviceData: ServiceData = None
    attachmentsInfo: AttachmentInfoMap = None


@dataclass
class AttachmentResponse(TcBaseObj):
    """
    The response.
    
    :var attchments: The list of the structure "attachmentsCreated" specifying the details about created attachment.
    :var serviceData: Service data containing partial errors.
    """
    attchments: List[AattachmentsCreated] = ()
    serviceData: ServiceData = None


@dataclass
class AttachmentWindowInfo(TcBaseObj):
    """
    The information of the attachment window.
    
    :var attachmentWindow: Attachment window of type CfgAttachmentWindow.
    :var attachmentLines: The list of CfgAttachmentLine objects representing the attachment lines in the attachment
    window. This first member of the list will always be the top line of the attachment window.
    """
    attachmentWindow: BusinessObject = None
    attachmentLines: List[BusinessObject] = ()


@dataclass
class AttachmentsInput(TcBaseObj):
    """
    The input contains a BOMLine object for which attachment lines are required.
    The input contains the list of CfgAttachmentWindow objects too.
    If the attachment window list is not empty, the given line is set as top line of all the attachment windows in the
    list and its attachments are fetched.
    
    If the list is empty, a new attachment window is created for the incoming line.
    
    :var line: The BOMLine objects for which attachment lines are required.
    :var attachmentWindowsList: The list of attachment window of type CfgAttachmentWindow.
    This list may be empty and in that case a new attachment window is created for the given BOMLine. If the list is
    not empty, the given BOMLine is set as the top line of all the attachment windows in the list.
    """
    line: BusinessObject = None
    attachmentWindowsList: List[BusinessObject] = ()


@dataclass
class CreateAttachmentsInput(TcBaseObj):
    """
    The structure related to attachment line information.
    
    :var sourceLine: The BOMLine or its subtype for which attachment is to be created. Example of subtypes are
    Mfg0BvrProcess, Mfg0BvrOperation, MfgoBvrPlantBOP etc.
    :var targetObject: The attachment line object under which the new attachment is to be created, e.g.,  top
    attachment line, pseudo folder etc.
    :var importFileType: Type of import file. It can be either Text or Binary.
    Ignored if importFilePath is blank.
    Ignored if the objectType is specified as Form.
    :var namedRefType: Type of named reference of the dataset. For example JT, Text ext.
    Ignored if the objectType is specified as Form.
    :var namedRefSubType: Sub type of named ref. Can be blank.
    Ignored if the objectType is specified as Form.
    :var relation: The name of the relation between dataset/form and ItemRevision.
    A default relation will be used if this is blank.
    :var saveForm: To save form or not. Ignored if the objectType is specified as Dataset.
    :var dsContainer: The object to which dataset is attached. If Null then Dataset is attached to the ItemRevision. 
    Ignored if the objectType is specified as Form.
    :var objectType: Specifies the type of object to be created for the attachment line. It can have two values
    - Dataset
    - Form
    
    
    :var name: Name.
    :var description: Description
    :var type: Specific type of the dataset or the form. For example Direct Model, Text, ArcWeld Attribut Form Time Way
    Plan Location Form etc. This cannot be blank.
    :var datasetID: Dataset ID. This can be blank. In that case the dataset with default id is created.
    Ignored if the objectType is specified as Form.
    :var datasetRev: Dataset revision. This can be blank. In that case the dataset with default revision is created.
    Ignored if the objectType is specified as Form.
    :var toolUsed: Name of tool to be used to open the dataset. For example Text Editor.
    Ignored if the objectType is specified as Form.
    :var importFilePath: Full path of the file to be imported with the dataset. Can be blank.
    Ignored if the objectType is specified as Form.
    """
    sourceLine: BusinessObject = None
    targetObject: BusinessObject = None
    importFileType: str = ''
    namedRefType: str = ''
    namedRefSubType: str = ''
    relation: str = ''
    saveForm: bool = False
    dsContainer: BusinessObject = None
    objectType: str = ''
    name: str = ''
    description: str = ''
    type: str = ''
    datasetID: str = ''
    datasetRev: str = ''
    toolUsed: str = ''
    importFilePath: str = ''


"""
The map of the BOMLine and a structure holding the information about its attachments.
"""
AttachmentInfoMap = Dict[BusinessObject, AttachmentWindowInfo]
