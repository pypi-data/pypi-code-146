from __future__ import annotations

from tcsoa.gen.BusinessObjects import Item, WorkspaceObject, ItemRevision
from typing import Dict, List
from tcsoa.gen.Internal.Visualization._2008_06.DataManagement import NamedRefsInDataset
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GatherBasedDatasetInfo(TcBaseObj):
    """
    Base dataset information.
    
    :var uid: the base Dataset object uid.   The base Dataset is the Dataset where the markup Datasets are related to.
    :var name: the base Dataset object name.
    :var additionalInfo: the additional information will have the followings: 
    RequestMode=VIEW or MARKUP
    PrintMode=PRINT or NOPRINT
    AccessMode=READ or WRITE
    Arguments=(empty)
    FilePath=(base file name, for example, MyFile.pdf)
    DataSegmentFileType=oai (if the file is a Microsoft office file) or file extension for other file type.
    DataSegment=(this contains all the above information, but all the information are in a single string. 
    Additionally, it also contains the server information: host path, SSO application id, and SSO loginURL)
    :var namedRefInfos: the list of base dataset named references.
    :var controlObj: the control object structure with uid, name, and any additional information.
    :var markupList: the list of the related markup structures that are related to the base Dataset.
    """
    uid: str = ''
    name: str = ''
    additionalInfo: GatherKeyValueMap = None
    namedRefInfos: List[NamedRefsInDataset] = ()
    controlObj: GatherMarkupControlObject = None
    markupList: List[GatherMarkupInfo] = ()


@dataclass
class GatherBasedDatasetTypeInfo(TcBaseObj):
    """
    Base dataset type information.
    
    :var relatedDatasets: the list of base Datasets of the same type.
    :var toolPreferences: the list of markup tool preferences.
    :var name: the Dataset type name.
    """
    relatedDatasets: List[GatherBasedDatasetInfo] = ()
    toolPreferences: List[str] = ()
    name: str = ''


@dataclass
class GatherBusinessDataInfo(TcBaseObj):
    """
    Item and ItemRevision information or Dataset type information or both.
    
    :var gatherItemInfo: the structure of Item and Item Revision information.
    :var gatherDatasetTypeInfos: the list of structures of the DatasetType and Datasets information.
    """
    gatherItemInfo: GatherItemInfo = None
    gatherDatasetTypeInfos: List[GatherBasedDatasetTypeInfo] = ()


@dataclass
class GatherInputInfo(TcBaseObj):
    """
    the input information.
    
    :var id: the id can be a WorkspaceObject, an Item, an Item Revision, a Dataset or a markup control object (a markup
    control object is any WorkspaceObject that has the business object Fnd0MarkupControlObject constant is defined as
    true, default is false).  The input id is required.  If empty, invalid object error is returned.
    :var item: the related Item to the input id above.  This can be empty.
    :var itemRev: the related Item Revision to the input id above.  This can be empty.
    :var controlObj: the related markup control object to the input id above.  This can be empty.
    :var idAdditionalInfo: the map of additional information in the form of key value pair strings.  This can be empty.
      Currently, the system only processes the input with key=MARKUPTOOL and value=(tool name).
    """
    id: WorkspaceObject = None
    item: Item = None
    itemRev: ItemRevision = None
    controlObj: WorkspaceObject = None
    idAdditionalInfo: GatherKeyValueMap = None


@dataclass
class GatherItemInfo(TcBaseObj):
    """
    Item and ItemRevision information.
    
    :var itemUid: the Item object uid.
    :var itemName: the Item object name.
    :var itemRevUid: the Item Revision object uid.
    :var itemRevName: the Item Revision object name.
    :var toolPreferences: the list of markup tool preferences.
    """
    itemUid: str = ''
    itemName: str = ''
    itemRevUid: str = ''
    itemRevName: str = ''
    toolPreferences: List[str] = ()


@dataclass
class GatherMarkupControlObject(TcBaseObj):
    """
    Markup control object information.
    
    :var uid: the control object uid.  A markup control object is any WorkspaceObject that has the Business Object
    Fnd0MarkupControlObject constant is defined as true, default is false.
    :var name: the control object name.
    :var additionalInfo: any additional information in the form of key value pair strings.  This is for future use.
    """
    uid: str = ''
    name: str = ''
    additionalInfo: GatherKeyValueMap = None


@dataclass
class GatherMarkupInfo(TcBaseObj):
    """
    Markup dataset information.
    
    :var uid: the markup Dataset object uid.
    :var name: the markup Dataset object name.
    :var additionalInfo: the additional information will have the followings: 
    MarkupFormat=(file extension, example: fdf)
    AccessMode=READ or WRITE
    CreatedOn=(yyyy mm dd.hh.mm.ss)
    :var namedRefInfos: the list of markup Dataset named references.
    """
    uid: str = ''
    name: str = ''
    additionalInfo: GatherKeyValueMap = None
    namedRefInfos: List[NamedRefsInDataset] = ()


@dataclass
class GatherResponse(TcBaseObj):
    """
    Gather markup return information.
    
    :var businessDataList: the list of the structures of the Item, DatasetType information.
    :var svcData: the service data that will have the failed objects and errors.
    """
    businessDataList: List[GatherBusinessDataInfo] = ()
    svcData: ServiceData = None


@dataclass
class GatherServerInfo(TcBaseObj):
    """
    Server information.
    
    :var protocol: the connection protocal to the server.  It can be http or iiop.
    :var hostPath: the host path.
    :var serverMode: the server mode character.  2 is for two tier.   4 is for four tier.
    :var useSso: if the client uses Single Sign On (SSO) environment to connect to the server, this is set to true,
    otherwise false.
    :var tccsEnvironment: the SSO environment name.
    :var ssoInfo: the structure of the SSO service url and id.
    :var additionalInfo: the map of additional information in the form of key value pair strings.  This is currently
    not used (future).
    """
    protocol: str = ''
    hostPath: str = ''
    serverMode: str = ''
    useSso: bool = False
    tccsEnvironment: str = ''
    ssoInfo: GatherSsoInfo = None
    additionalInfo: GatherKeyValueMap = None


@dataclass
class GatherSessionInfo(TcBaseObj):
    """
    Session information.
    
    :var sessionDescriminator: the Client Server session discriminator to connect to the existing specified session.
    :var sessionAdditionalInfo: the map of additional information in the form of key value pair strings.
    """
    sessionDescriminator: str = ''
    sessionAdditionalInfo: GatherKeyValueMap = None


@dataclass
class GatherSsoInfo(TcBaseObj):
    """
    Single Sign On (SSO) information.
    
    :var loginServiceUrl: the login service url.
    :var appId: the application id of the Teamcenter server in the SSO environment.
    """
    loginServiceUrl: str = ''
    appId: str = ''


@dataclass
class GatherUserAgentDataInfo(TcBaseObj):
    """
    User application information.
    
    :var userApplication: the client name that initiates the launch.
    :var userAppVersion: the version of the client.
    :var userAdditionalInfo: the map of additional information in the form of key value pair strings.  This is
    currently not used (future).
    """
    userApplication: str = ''
    userAppVersion: str = ''
    userAdditionalInfo: GatherKeyValueMap = None


"""
Key value map of string, string.
"""
GatherKeyValueMap = Dict[str, str]
