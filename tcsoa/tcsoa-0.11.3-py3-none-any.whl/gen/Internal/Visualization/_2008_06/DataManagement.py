from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ImanFile, ImanRelation, Dataset, Item, ItemRevision
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class FormInfo(TcBaseObj):
    """
    Input structure for createTwoDSnapshot
    
    :var name: Identifier that helps the client to track the object created.
    :var description: Description of form.
    :var formType: Type of form, typically set to "Vis_Snapshot_2D_Form".
    :var attributesMap: List of key value pairs that make up the forms data.
    :var saveDB: Whether data should be saved, typicaly set true.
    """
    name: str = ''
    description: str = ''
    formType: str = ''
    attributesMap: StringArrayMap = None
    saveDB: bool = False


@dataclass
class GRMRelationOutput(TcBaseObj):
    """
    This structure holds the association information between the created markup Dataset and the launched Teamcenter
    object on which markups were created.
    
    :var relation: A Teamcenter object referencing relation information between the created markup Dataset and the
    launched Teamcenter object on which markups were created.
    e.g., VisStructureContext, Datasets like DirectModel
    :var propertiesInfo: A map of key value pairs representing the attributes assigned to the relation connecting the
    created markup Dataset to the launched Teamcenter object by the client application.
    """
    relation: ImanRelation = None
    propertiesInfo: KeyValueMap = None


@dataclass
class GetLatestFileReadTicketsInfo(TcBaseObj):
    """
    This structure is used to find the latest version of the named reference to the specified Dataset.
    
    :var clientId: Identifier that helps the client track the object
    :var dataset: Dataset owning the named reference object.
    :var namedRef: The IMANFile named reference.
    :var originalFilename: The original filename. This is used to search for the latest named reference in the Dataset.
    """
    clientId: str = ''
    dataset: Dataset = None
    namedRef: ImanFile = None
    originalFilename: str = ''


@dataclass
class GetLatestFileReadTicketsOutput(TcBaseObj):
    """
    Output structure to hold the data returned from getLatestFileReadTickets
    
    :var clientId: Identifier that helps the client track the object. This is the same 'clientId' from the input data.
    :var namedRefUID: The UID of the resolved IMANFile named reference.
    :var originalFilename: The original filename. This is the original filename of the resolved named reference.
    :var readTicket: The read ticket for the IMANFile in the latest Dataset.
    """
    clientId: str = ''
    namedRefUID: str = ''
    originalFilename: str = ''
    readTicket: str = ''


@dataclass
class GetLatestFileReadTicketsResponse(TcBaseObj):
    """
    This structure holds the data returned from the 'getLatestFileReadTickets'.
    
    :var getLatestFileReadTicketsOutput: A vector containing the latest Dataset versions and the associated IMANFile
    including the read file ticket.
    :var serviceData: Standard 'ServiceData' member
    """
    getLatestFileReadTicketsOutput: List[GetLatestFileReadTicketsOutput] = ()
    serviceData: ServiceData = None


@dataclass
class IdInfo(TcBaseObj):
    """
    This structure holds the information about the objects that will be launched to the viewer.
    
    :var id: A required parameter that references the object to be launched. If needed, launched object will be
    resolved by the server to a launch able object.
    :var item: An optional object reference of the Item containing launch able object. If this is not known, the server
    will attempt to identify the parent if it can.
    :var itemRev: An optional object reference of the ItemRevision containing launchable object. If this is not known,
    the server will attempt to identify if it can.
    :var operation: An optional parameter references the type of launch action. This controls the action the viewer
    will perform when it opens the object. The actions supported are one of following: 'Open', 'Insert', 'Merge' or
    'Interop'.  'Open' will open the object in a new window.  'Insert' will insert the object into the current window
    that has focus.  'Merge' will attempt to merge a pruned product structure with one that is already open if it can. 
    'Interop' will present a dialog that lets the user select the launch action.
    :var idAdditionalInfo: An optional parameter referencing the additional information of launched objects in form of
    key/value pairs (if any).
    """
    id: BusinessObject = None
    item: Item = None
    itemRev: ItemRevision = None
    operation: str = ''
    idAdditionalInfo: KeyValueMap = None


@dataclass
class MarkupInput(TcBaseObj):
    """
    This structure holds the information related to creation of the markup Dataset , association information of the
    markup Dataset to the rest of the Teamcenter objects and the list of the files to be uploaded in the markup Dataset.
    
    :var clientId: (Required) Unique Identifier defined by user to track for each markup Dataset creation request.
    :var attachToLocation: (Optional) Teamcenter object reference where the created markup Dataset is referenced.
    :var createDatasetInfo: (Required) An object of type 'DatasetInfo' struct, containing markup Dataset creation
    information.
    :var baseObjInfo: (Required) An object of type 'BaseObjInfo' struct containing information of Teamcenter launched
    object on which markups are created and will be connected to the created markup Dataset.
    :var uploadData: (Required) A vector of objects of type 'NamedRefUploadOrUpdateInfo' struct where each object
    contains information specific to the file that will be uploaded to the markup Dataset.
    """
    clientId: str = ''
    attachToLocation: BusinessObject = None
    createDatasetInfo: DatasetInfo = None
    baseObjInfo: BaseObjInfo = None
    uploadData: List[NamedRefUploadOrUpdateInfo] = ()


@dataclass
class MarkupOutput(TcBaseObj):
    """
    This structure holds the information related to creation of the markup Dataset, association information of the
    markup Dataset to the rest of the Teamcenter objects and the list of the files uploaded in the markup Dataset.
    
    :var markupDatset: A Teamcenter object referencing the created markup Dataset.
    :var references: A vector of object of type 'NamedRefsInDataset' struct, each object containing information about
    the successfully uploaded files in the markup Dataset.
    :var attachRelation: A Teamcenter object referencing relation information between the created markup Dataset and
    the Teamcenter object in which it is referenced.
    :var relation: An object of type relation struct, containing information about the Teamcenter objects that the
    created markup Dataset is connected to.
    """
    markupDatset: Dataset = None
    references: List[NamedRefsInDataset] = ()
    attachRelation: ImanRelation = None
    relation: GRMRelationOutput = None


@dataclass
class MarkupResponse(TcBaseObj):
    """
    This structure is used to return information from the 'createMarkup' operation. This structure holds information
    about 'serviceData' (containing information about successfully created markup Dataset and if any updated Teamcenter
    object. It may also contain information if any of the failure to commit the files to the Dataset.  In case of
    failure to create session Dataset altogether, error messages are associated to 'clientId' identifier and are added
    to the error stack).  'MarkupOutputMap', contains information mapping the 'clientId' identifier to successfully
    created markup Dataset along with the list of named references in the created markup Dataset, and the Teamcenter
    objects it is connected to.
    
    :var markupInfo: A map associating the unique clientId identifier with the 'MarkupOutput' struct.
    :var serviceData: Created Dataset will be returned in the 'ServiceData'. Any failure will be returned with error
    message in the 'ServiceData' list of partial errors.
    """
    markupInfo: MarkupOutputMap = None
    serviceData: ServiceData = None


@dataclass
class MarkupUpdateInput(TcBaseObj):
    """
    This structure holds the information about the updated markup Dataset, (if any) association information of the
    markup Dataset to the Teamcenter object  (VisStructureContext), and the list of the files to be uploaded in the
    markup Dataset.
    
    :var clientId: (Required)  Unique Identifier defined by user to track for each markup Dataset creation request.
    :var markupDataset: (Required)  Teamcenter object referencing markup Dataset that needs to be updated.
    :var baseObjInfo: (Optional) Objects of type 'BaseObjInfo' struct containing information of Teamcenter object
    (VisStructureContext), on which markups are created and connected to the markup Dataset.
    
    NOTE: This parameter is relevant when markups are updated against VisStructureContext. 
    
    :var uploadData: (Required)  A vector of objects of type 'NamedRefUploadOrUpdateInfo' struct where each object
    contains information specific to the file that will be uploaded to the markup Dataset.
    """
    clientId: str = ''
    markupDataset: Dataset = None
    baseObjInfo: BaseObjInfo = None
    uploadData: List[NamedRefUploadOrUpdateInfo] = ()


@dataclass
class MarkupUpdateOutput(TcBaseObj):
    """
    This structure holds the information related of the updated markup Dataset, association information of the markup
    Dataset to the VisStructureContext and the list of the files uploaded in the markup Dataset.
    
    :var markupDatset: A Teamcenter object referencing the updated markup Dataset
    :var references: A vector of object of type 'NamedRefsInDataset' struct, each object containing information about
    the successfully uploaded files in the markup Dataset.
    :var relation: An object of type 'relation' struct, containing information about the VisStructureContext that the
    updated markup Dataset is connected to.
    """
    markupDatset: Dataset = None
    references: List[NamedRefsInDataset] = ()
    relation: GRMRelationOutput = None


@dataclass
class MarkupUpdateResponse(TcBaseObj):
    """
    This structure is used to return information from the 'updateMarkup' operation. This structure holds information
    about 'serviceData' (containing information about successfully updated markup Dataset. It may also contain
    information if any of the failure to commit the file to the Dataset. In case of failure to update Dataset
    altogether, error messages are associated to 'clientId' identifier and are added to the error stack).
    'MarkupUpdateOutputMap', contains information mapping the 'clientId' identifier to successfully updated markup
    Dataset along with the list of named references in the updated markup Dataset, and the Teamcenter object
    (VisStructureContext) it is connected to.
    
    :var markupInfo: A map associating the unique 'clientId' identifier with the 'MarkupUpdateOutput' struct.
    :var serviceData: Updated Dataset will be returned in the 'serviceData'. Any failure will be returned with error
    message in the 'serviceData' list of partial errors.
    """
    markupInfo: MarkupUpdateOutputMap = None
    serviceData: ServiceData = None


@dataclass
class MetaDataStampTicketsResponse(TcBaseObj):
    """
    Structure used for 'getMetaDataStamp' response.
    
    :var tickets: A vector of FMS transient file ticket corresponding to the ids in the input data.
    :var serviceData: Failures will be returned in the 'Servicedata', with the error message in the 'ServiceData' list
    of partial errors.
    """
    tickets: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class NamedRefUploadOrUpdateInfo(TcBaseObj):
    """
    This structure holds the information related to the files to be uploaded in the created markup Dataset.
    
    :var clientFileId: (Required) Unique Identifier defined by user to track each files that needs to be uploaded in
    the markup Dataset.
    :var fileState: (Required) State of the file at the time of upload. Options allowed are 'NEW', 'UPDATE', 'DELETE',
    'RENAME', 'RENAME_UPDATE'.
    
    e.g.  If creating then it will be the 'NEW'. If updating Dataset files the state will be either 'UPDATE', 'DELETE',
    'RENAME' or 'RENAME_UPDATE'.
    :var fileName: (Required) The name of file to be uploaded in the markup Dataset. Filename with extension needs to
    be provided.
    :var refName: (Required) Named reference of the file e.g. Markup.
    :var fileTicket: (Required) FMS write ticket of the file to be used at the time of commit.
    :var newObject: (Optional) Teamcenter IMANFile object reference to be added in the created markup Dataset. 
    
    Example scenarios where the parameter is relevant:
    - Adding a file reference from another Dataset.
    - Updating the IMANFile object existing in the Dataset, referenced by 'existingObject' parameter, with the new
    IMANFile object, referenced by 'newObject' parameter in Dataset.
    
    
    :var existingObject: (Optional) Teamcenter IMANFile object reference in the created markup Dataset.
    
    Example scenarios where the parameter is relevant:
    - Updating existing IMANFile Object referenced by 'existingObject' parameter with the new IMANFile object
    referenced by 'newObject' parameter in Dataset.  
    - Deleting the existing IMANFile object referenced by 'existingObject' parameter.
    
    """
    clientFileId: str = ''
    fileState: str = ''
    fileName: str = ''
    refName: str = ''
    fileTicket: str = ''
    newObject: BusinessObject = None
    existingObject: BusinessObject = None


@dataclass
class NamedRefsInDataset(TcBaseObj):
    """
    This structure holds the information related to the list of the files to be uploaded in the markup Dataset.
    
    :var clientFileId: Unique Identifier defined by user to track each file that was successfully uploaded to the
    markup Dataset.
    
    Note: This identifier is provided by 'NamedRefUploadOrUpdateInfo' structure.
    
    :var uploadedFile: Uploaded Teamcenter IMANFile object reference in the markup Dataset.
    :var uploadedFilename: Uploaded Teamcenter IMANFile object filename in the markup Dataset.
    :var uploadedFileRefNames: Uploaded Teamcenter IMANFile object reference name in the markup Dataset e.g. Markup.
    """
    clientFileId: str = ''
    uploadedFile: ImanFile = None
    uploadedFilename: str = ''
    uploadedFileRefNames: str = ''


@dataclass
class BaseObjInfo(TcBaseObj):
    """
    This structure holds the information related to Teamcenter launched object on which markup Dataset is created and
    connected to.
    
    :var baseObj: (Required) The object referencing Teamcenter objects like Dataset or VisStructureContext on which
    markup Dataset is created and connected to.
    :var propertiesInfo: (Optional) A map of key value pairs to assign the properties to the relation connecting the
    created markup Dataset to the launched Teamcenter object.
    
    NOTE: This parameter is relevant when creating a markup Dataset against a VisStructureContext. 
    """
    baseObj: BusinessObject = None
    propertiesInfo: KeyValueMap = None


@dataclass
class SaveSessionOutput(TcBaseObj):
    """
    This structure holds the information related to the session file to be uploaded in the session Dataset.
    
    :var sessionModelDataset: Teamcenter object referencing updated Vis_Session Dataset.
    :var reference: An object of type 'NamedRefsInDataset' struct, containing information about the successfully
    uploaded session file in the Vis_Session Dataset.
    """
    sessionModelDataset: Dataset = None
    reference: NamedRefsInDataset = None


@dataclass
class SaveSessionResponse(TcBaseObj):
    """
    This structure is used to return information from the 'saveSession' operation. This structure holds information
    about 'serviceData' and 'SessionToSessionModelMap'.  The 'serviceData' contains information about successfully
    updated session Dataset. It may also contain information if any on a failure to commit the file to the Dataset. In
    case of failure to update session Dataset, error messages are associated to 'clientId' identifier and are added to
    the error stack. The map, 'SessionToSessionModelMap', contains information mapping 'clientId' identifier to
    successfully updated session Dataset along with the information corresponding to the file uploaded in the session
    Dataset.
    
    :var sessionToSessionModelInfo: A map associating the unique 'clientId' identifier with the 'SaveSessionOutput'
    struct.
    :var serviceData: Updated session Dataset will be returned in the 'serviceData'. Any failure will be returned with
    error message in the 'serviceData' list of partial errors.
    """
    sessionToSessionModelInfo: SessionToSessionModelMap = None
    serviceData: ServiceData = None


@dataclass
class ServerInfo(TcBaseObj):
    """
    This structure holds the basic information for Teamcenter Visualization to connect to the server.
    
    :var protocol: A required parameter referencing the protocol type for connection to the server. Use http for
    standard 4 tier connections, and iiop for 2 tier deployments.
    :var hostpath: A required parameter referencing the URL to connect to the server.
    :var servermode: A required parameter referencing the server mode that controls how the connection to the server is
    made: 2 for two tier. 4 for four tier.
    :var serverAdditionalInfo: An optional parameter referencing the additional information of server in form of
    key/value pairs (if any).
    """
    protocol: str = ''
    hostpath: str = ''
    servermode: int = 0
    serverAdditionalInfo: KeyValueMap = None


@dataclass
class SessionInfo(TcBaseObj):
    """
    This structure holds the information about the session information of the client application from where the launch
    operation was initiated.
    
    :var sessionDescriminator: Client/Server session discriminator to connect to existing specified session.  This
    allows the viewer application to share an existing server process session with the client that initiated the
    launch. If this is not specified, the viewer will present a login prompt.
    :var sessionAdditionalInfo: An optional parameter referencing the additional information of the session in form of
    key/value pairs (if any).
    """
    sessionDescriminator: str = ''
    sessionAdditionalInfo: KeyValueMap = None


@dataclass
class SessionModelInput(TcBaseObj):
    """
    This structure holds the information related to creation of the markup Dataset , association information of the
    markup Dataset to the rest of the Teamcenter objects and the list of the files to be uploaded in the markup Dataset.
    
    :var clientId: (Required) Unique Identifier defined by user to track each session (Vis_Session) Dataset creation
    request.
    :var attachToLocation: (Optional) Teamcenter object reference where the created session Dataset is referenced.
    :var createDatasetInfo: (Required) An object of type 'DatasetInfo' struct, containing session Dataset creation
    information.
    :var sessionModelBaseObjs: (Required) A vector of type 'BaseObjInfo' struct where each object contains information
    of Teamcenter launched object, on which session is created. These objects are then connected to the created session
    Dataset via relations.
    :var uploadData: (Required) A vector of objects of type 'NamedRefUploadOrUpdateInfo' struct where each object
    contains information specific to the file that will be uploaded to the markup Dataset.
    """
    clientId: str = ''
    attachToLocation: BusinessObject = None
    createDatasetInfo: DatasetInfo = None
    sessionModelBaseObjs: List[BaseObjInfo] = ()
    uploadData: List[NamedRefUploadOrUpdateInfo] = ()


@dataclass
class SessionModelOutput(TcBaseObj):
    """
    This structure holds the information related to creation of the session Dataset , association information of the
    session Dataset to the rest of the Teamcenter objects and the list of the files uploaded in the session Dataset.
    
    :var sessionModelDatset: A Teamcenter object referencing the created Vis_Session  Dataset.
    :var references: A vector of objects of type 'NamedRefsInDataset' struct, each object containing information about
    the successfully uploaded files in the session Dataset.
    :var attachRelation: A Teamcenter object referencing relation information between the created markup Dataset and
    the Teamcenter object in which it is referenced.
    :var relations: A vector of objects of type 'GRMRelationOutput' struct, containing information about the Teamcenter
    objects that the created session Dataset is connected to.
    """
    sessionModelDatset: Dataset = None
    references: List[NamedRefsInDataset] = ()
    attachRelation: ImanRelation = None
    relations: List[GRMRelationOutput] = ()


@dataclass
class SessionModelResponse(TcBaseObj):
    """
    This structure is used to return information from the 'createSessionModel' operation. This structure holds
    information about 'serviceData' (containing information about successfully created session Dataset and if any
    updated Teamcenter object. It may also contain information if any of the failure to commit the files to the
    Dataset. In case of failure to create session Dataset altogether, error messages are associated to 'clientId'
    identifier and are added to the error stack). 'SessionModelOutputMap', contains information mapping 'clientId'
    identifier to successfully created session Dataset along with the list of named references in the created session
    Dataset, and the Teamcenter objects it is connected to.
    
    :var sessionModelInfo: A map associating the unique 'clientId' identifier with the 'SessionModelOutput' struct.
    :var serviceData: Created session Dataset will be returned in the 'serviceData'. Any failure will be returned with
    error message in the 'serviceData' list of partial errors.
    """
    sessionModelInfo: SessionModelOutputMap = None
    serviceData: ServiceData = None


@dataclass
class SessionModelUpdateOutput(TcBaseObj):
    """
    This structure holds the information related to updated session Dataset, association information of the session
    Dataset to the rest of the Teamcenter objects and the list of the files uploaded in the session Dataset.
    
    :var sessionModelDataset: A Teamcenter object referencing the updated  Vis_Session  Dataset.
    :var references: A vector of objects of type 'NamedRefsInDataset' struct, each object containing information about
    the successfully uploaded files in the session Dataset.
    :var relations: A vector of objects of type 'GRMRelationOutput' struct, containing association information between
    the input the Teamcenter objects and the updated session Dataset.
    """
    sessionModelDataset: Dataset = None
    references: List[NamedRefsInDataset] = ()
    relations: List[GRMRelationOutput] = ()


@dataclass
class SessionModelUpdateResponse(TcBaseObj):
    """
    This structure is used to return information from the 'updateSessionModel' operation. This structure holds
    information about 'serviceData' (containing information about successfully updated session Dataset.  It may also
    contain information if any of the failure to commit the file to the Dataset. In case of failure to update session
    Dataset altogether, error messages are associated to 'clientId' identifier and are added to the error stack).
    'SessionModelUpdateOutputMap' contains information mapping 'clientId' identifier to successfully updated session
    Dataset along with the information corresponding to the file uploaded in the session Dataset and updated relation
    of the session Dataset to the input Teamcenter objects.
    
    :var sessionModelInfo: A map associating the unique 'clientId' identifier with the 'SessionModelUpdateOutput'
    struct.
    :var serviceData: Updated session Dataset will be returned in the 'serviceData'. Any failure will be returned with
    error message in the 'serviceData' list of partial errors.
    """
    sessionModelInfo: SessionModelUpdateOutputMap = None
    serviceData: ServiceData = None


@dataclass
class TwoDSnapshotInput(TcBaseObj):
    """
    Input structure for create snapshot datasets operation
    
    :var clientId: Identifier that helps the client to track the object created, optional.
    :var sourceItemRev: Name of the source item revision to which snapshot dataset will be attached.  This represents
    the ItemRevision that owns the base image.
    :var createDatasetInfo: A structure containing information about the Vis_Snapshot_2D_View_Data dataset including
    tool to open the dataset, dataset type, name, and description. The datasetType should be set to
    "Vis_Snapshot_2D_View_Data".
    :var namedRefInfo: A vector of structures each containing information about a named reference.  Should include the
    markups, viewport xml file, thumbnail, and asset image files along with the object references to the base image
    dataset and the source ItemRevision objects.
    :var createFormInfo: A structure containing information about form attribute information.
    """
    clientId: str = ''
    sourceItemRev: ItemRevision = None
    createDatasetInfo: DatasetInfo = None
    namedRefInfo: List[NamedRefUploadOrUpdateInfo] = ()
    createFormInfo: FormInfo = None


@dataclass
class UpdateSessionModelWithSessionInput(TcBaseObj):
    """
    This structure holds the information of Vis_Session Dataset that will be updated with the session file.
    
    :var clientId: (Required) Unique Identifier defined by user to track each session (Vis_Session) Dataset that will
    be updated.
    :var sessionModelDataset: (Required) Teamcenter object referencing Vis_Session Dataset that needs to be updated.
    :var uploadSessionFile: (Required) An object of type 'NamedRefUploadOrUpdateInfo' struct, containing information of
    the session file that will be uploaded into the Vis_Session Dataset.
    """
    clientId: str = ''
    sessionModelDataset: Dataset = None
    uploadSessionFile: NamedRefUploadOrUpdateInfo = None


@dataclass
class UpdateSesssionModel(TcBaseObj):
    """
    This structure holds the information about the updated session Dataset, (if any) association information of the
    session Dataset to the Teamcenter object (VisStructureContext), and the list of the files to be uploaded in the
    session Dataset.
    
    :var clientId: (Required) Unique Identifier defined by user to track for each markup Dataset creation request.
    :var sessionModelDataset: (Required) Teamcenter object referencing session Dataset that needs to be updated.
    :var sessionModelBaseObjs: (Optional) A vector of objects of type 'BaseObjInfo' struct , each containing
    information of Teamcenter objects included in session and connected to the session Dataset.
    
    NOTE: This parameter may be relevant when session contains new references.
    
    :var uploadData: (Required) A vector of objects of type 'NamedRefUploadOrUpdateInfo' struct where each object
    contains information specific to the file that will be uploaded to the session Dataset.
    """
    clientId: str = ''
    sessionModelDataset: Dataset = None
    sessionModelBaseObjs: List[BaseObjInfo] = ()
    uploadData: List[NamedRefUploadOrUpdateInfo] = ()


@dataclass
class UpdateTwoDSnapshotInput(TcBaseObj):
    """
    Input structure for update snapshot dataset operation
    
    :var clientId: Identifier that helps the client to track the object created, optional.
    :var snapshotDataset: A structure containing information about the Vis_Snapshot_2D_View_Data dataset such as type,
    name, and description.  The datasetType should be set to "Vis_Snapshot_2D_View_Data".
    :var namedRefInfo: A vector of structures  each containing information about named references.  Same structure used
    by the createTwoDSnapshot service.  Should include the markup layers, viewport xml file, thumbnail, and asset image
    files along with the object references to the base image dataset and the source ItemRevision objects.
    """
    clientId: str = ''
    snapshotDataset: Dataset = None
    namedRefInfo: List[NamedRefUploadOrUpdateInfo] = ()


@dataclass
class UpdateTwoDSnapshotOutput(TcBaseObj):
    """
    Output structure for update 2D Snapshot operation
    
    :var snapshotDataset: Dataset object reference that was created.
    :var references: List of named references associated with dataset.
    """
    snapshotDataset: Dataset = None
    references: List[NamedRefsInDataset] = ()


@dataclass
class UpdateTwoDSnapshotResponse(TcBaseObj):
    """
    Return structure for update 2DSnapshot operation
    
    :var updateSnapshotInfo: A map containing client ids and output structure as key/value pairs.
    :var serviceData: The Service Data containing the error information.
    """
    updateSnapshotInfo: UpdateTwoDSnapshotOutputMap = None
    serviceData: ServiceData = None


@dataclass
class UserAgentDataInfo(TcBaseObj):
    """
    This structure holds the information about the client application that initiated the launch.
    
    :var userApplication: An optional parameter referencing the client who initiates the launch.
    :var userAppVersion: An optional parameter referencing the version of the client that initiated launch.
    :var userAdditionalInfo: An optional parameter referencing the additional information of client application in form
    of key/value pair (if any).
    """
    userApplication: str = ''
    userAppVersion: str = ''
    userAdditionalInfo: KeyValueMap = None


@dataclass
class VVITicketsResponse(TcBaseObj):
    """
    Used to return information from the 'createLaunchFile' operation. The structure holds the 'serviceData' object and
    a FMS transient read ticket corresponding to the launch file (VVI or VFZ).
    
    :var ticket: The FMS transient read ticket of the launch file (VVI or VFZ) generated for the objects that can be
    launched. The file will be placed in the transient file volume and the caller will need to download it from there
    with the ticket sent by the service.
    :var serviceData: SOA Framework object containing error information. In cases where objects cannot be launched,
    error message, codes will be mapped to respective object id in the list of partial errors.
    """
    ticket: str = ''
    serviceData: ServiceData = None


@dataclass
class CreateTwoDSnapshotOutput(TcBaseObj):
    """
    Output structure for create 2D Snapshot operation
    
    :var dataset: Dataset object that was created.
    :var form: The form attached to the snapshot dataset.
    :var references: List of named references associated with dataset.
    :var attachRelation: The datasets relation VisItemRevCreatedSnapshot2D that attached the 2D snapshot to to the 
    parent ItemRevision object.
    """
    dataset: Dataset = None
    form: BusinessObject = None
    references: List[NamedRefsInDataset] = ()
    attachRelation: ImanRelation = None


@dataclass
class CreateTwoDSnapshotResponse(TcBaseObj):
    """
    Return structure for create 2DSnapshot operation
    
    :var snapshotOutput: A map containing client ids and output structure as key/value pairs.
    :var serviceData: The Service Data containing the error information.
    """
    snapshotOutput: CreateTwoDSnapshotOutputMap = None
    serviceData: ServiceData = None


@dataclass
class DatasetInfo(TcBaseObj):
    """
    This structure holds the information related to creation of the markup Dataset.
    
    :var tool: (Required) The name of the tool used to open the created markup Dataset.
    :var datasetType: (Required) The Dataset type of the markup Dataset to be created.
    :var datasetName: (Required) The name provided by the client application to the markup Dataset.
    :var datasetDesc: (Optional) The description provided by the client application to be associated to the markup
    Dataset.
    """
    tool: str = ''
    datasetType: str = ''
    datasetName: str = ''
    datasetDesc: str = ''


"""
CreateTwoDSnapshotOutputMap
"""
CreateTwoDSnapshotOutputMap = Dict[str, CreateTwoDSnapshotOutput]


"""
KeyValueMap
"""
KeyValueMap = Dict[str, str]


"""
MarkupOutputMap
"""
MarkupOutputMap = Dict[str, MarkupOutput]


"""
MarkupUpdateOutputMap
"""
MarkupUpdateOutputMap = Dict[str, MarkupUpdateOutput]


"""
SessionModelOutputMap
"""
SessionModelOutputMap = Dict[str, SessionModelOutput]


"""
SessionModelUpdateOutputMap
"""
SessionModelUpdateOutputMap = Dict[str, SessionModelUpdateOutput]


"""
SessionToSessionModelMap
"""
SessionToSessionModelMap = Dict[str, SaveSessionOutput]


"""
StringArrayMap
"""
StringArrayMap = Dict[str, List[str]]


"""
UpdateTwoDSnapshotOutputMap
"""
UpdateTwoDSnapshotOutputMap = Dict[str, UpdateTwoDSnapshotOutput]
