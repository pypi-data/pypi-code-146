from __future__ import annotations

from tcsoa.gen.Cad._2008_06.DataManagement import AttributeInfo
from tcsoa.gen.BusinessObjects import BusinessObject, ImanFile, WorkspaceObject, POM_object, Fnd0ModelViewPalette, Dataset, Fnd0ModelViewProxy
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GroupInfo(TcBaseObj):
    """
    A Model View Group to create or update and what Model View Proxies should be disclosed for that Group. It also
    allows each Group to be sequenced among the other Groups in the Palette.
    
    :var clientId: The use of this value is optional, but recommended.  It is used for mapping server errors and for
    correlating data in the response to the inputs.  The caller should populate a 'clientId' for each 'GroupInfo' with
    a value that is unique within the entire operation inputs.   The value is not interpreted or manipulated internally
    by the server
    :var boType: The type of group to create. Optional. If provided, must be a "Fnd0ModelViewGroup" or a valid sub-type
    of Fnd0ModelViewGroup. If not provided, "Fnd0ModelViewGroup" will be assumed as the type of the group to create.
    :var modelViewGroupForUpdate: Existing Model View Group (Fnd0ModelViewGroup or sub-type only) to be updated. If not
    given, a new Model View Group will be created and linked to the Model View Palette which was given as a Palette to
    create or update in the parent 'ModelViewPaletteInfo' input.
    :var attrListForGroup: A list of name-value pairs (string, list of strings) used to specify additional property
    data for the Model View Group.  All values are specified as strings, the caller is responsible for generating the
    correct string representation of each value passed.  For business objects use the UID value of the object.
    :var proxiesInGroup: An ordered list of Model View Proxies for the Group to contain. This is a complete list for
    this Model View Group.
    :var newOrderSequenceNumber: Optional hint for ordering Groups when not all Groups of a Palette are given. A 0
    'newOrderSequenceNumber' means to leave the Group in its current sequence order. Other valid sequence values are 1
    through the new total number of Group objects (e.g. the number of Groups after all Group creates and deletes for
    this Palette are completed.) If 'newOrderSequenceNumber' is 0 and this Group is newly created then it will be
    placed at the end of the existing Groups. No particular order is enforced among such zero-sequenced newly created
    Groups.
    """
    clientId: str = ''
    boType: str = ''
    modelViewGroupForUpdate: POM_object = None
    attrListForGroup: List[AttributeInfo] = ()
    proxiesInGroup: List[Fnd0ModelViewProxy] = ()
    newOrderSequenceNumber: List[int] = ()


@dataclass
class ModelViewPaletteInfo(TcBaseObj):
    """
    'ModelViewPaletteInfo' is used as input for creating, updating or deleting Model View Palette
    (Fnd0ModelViewPalette) and Model View Group (Fnd0ModelViewGroup) objects.  During update, 'boType' is left empty
    and the Model View Palette to update is given. Create or delete of a Model View Palette requires the user to have
    write access to the given 'disclosure'. Update of an existing Palette will only check write permission of the
    Palette itself.
    
    :var clientId: The use of this value is optional, but recommended.  It is used for mapping server errors and for
    correlating data in the response to the inputs.  The caller should populate a 'clientId' for each
    'ModelViewPaletteInfo' with a value that is unique within the input set and all input 'GroupInfo' for any input
    'ModelViewPaletteInfo'. The value is not interpreted or manipulated internally by the server.
    :var disclosure: The disclosure object (ItemRevision or Cpd0Workset) for which a Model View Palette is to be
    created, updated, or deleted. A value is optional. If not provided, any new Model View Palettes created will not be
    linked to any disclosure.
    :var boType: The business object type of a Model View Palette to be created. This value is optional for creating a
    new Model View Palette, and if provided must be Fnd0ModelViewPalette or a valid subtype of Fnd0ModelViewPalette. If
    no value is provided and no 'paletteToUpdate' is provided, then the 'boType' default value used is,
    "Fnd0ModelViewPalette." To update an existing Model View Palette, this value may be empty.
    :var paletteToUpdate: Required if an existing Palette (Fnd0ModelViewPalette) is being updated.
    :var attrListForPalette: A list of name-value pairs (string, list of strings) used to specify additional property
    data for the Model View Palette.  All values are specified as strings, the caller is responsible for generating the
    correct string representation of each value passed.  For business object, use the UID value of the object.
    :var groupsAndProxies: Details for new and existing Model View Groups (Fnd0ModelViewGroup) and their ordering and
    content.
    :var paletteIsComplete: If true, the existing list of Group objects (Fnd0ModelViewGroup) will be entirely replaced
    by the input Groups (within 'groupsAndProxies') and existing Groups in the Palette that are not in the
    'groupsAndProxies' content will be deleted (but not their Proxies). And if true, 'groupsToDelete' is ignored. If
    false, groups not in the 'groupsAndProxies' content are ignored, barring side-effects of requested re-ordering of
    Groups (see 'newOrderSequenceNumber' in 'groupsAndProxies').
    :var groupsToDelete: A list of Fnd0ModelViewGroup objects to delete and remove from the complete Palette
    (optional). List is ignored if 'paletteIsComplete' is true.
    :var deletePalette: If true, specifies that the existing Model View Palette (Fnd0ModelViewPalette) in
    'paletteToUpdate' should be deleted if possible. For update of an existing Model View Palette or creation of a new
    Palette, this value should be left at a default of false. All Model View Groups (Fnd0ModelViewGroup) objects in the
    deleted Palette will also be deleted but Proxies (Fnd0ModelViewProxy) referenced by the Model View Groups will be
    untouched.
    """
    clientId: str = ''
    disclosure: WorkspaceObject = None
    boType: str = ''
    paletteToUpdate: Fnd0ModelViewPalette = None
    attrListForPalette: List[AttributeInfo] = ()
    groupsAndProxies: List[GroupInfo] = ()
    paletteIsComplete: bool = False
    groupsToDelete: List[POM_object] = ()
    deletePalette: bool = False


@dataclass
class ModelViewProxyInfo(TcBaseObj):
    """
    An input for creating, updating or deleting model view proxy objects.  When creating a new model view
    proxy(Fnd0ModelViewProxy), the caller must specify the business object type ('boType') of the new model view proxy.
     During update, 'boType' is left empty and a reference to the model view proxy ('modelView') to be updated is
    specified.
    
    :var clientId: The use of this value is optional, but recommended.  It is used for mapping server errors and for
    correlating data in the response to the inputs.  The caller should populate a 'clientId' for each
    ModelViewProxyInfo with a value that is unique within the input set.   The value is not interpreted or manipulated
    internally by the server.
    :var modelView: The Fnd0ModelViewProxy to be updated.  A value is required for update or delete action cases,
    otherwise (create case) this value should be empty.
    :var boType: The business object type (its internal string name) of a model view proxy to be created.  This value
    is optional for creating a new model view proxy, and must be a Fnd0ModelViewProxy or subtype.  If no value is
    provided but also no modelView is provided, then the boType default value will be set to "Fnd0ModelViewProxy".  For
    update of an existing model view proxy, this value may be empty.
    :var deleteProxy: If true, specifies that this existing proxy should be deleted if possible. For update of an
    existing model view proxy or create of a new proxy, this value should be left at a default of false.
    :var owningModel: The owning object which manages the actual CAD model view for which the proxy is being created.
    This owning object will also control the lifecycle of the new proxy object. Required for creating a new model view
    proxy.  If an existing model view proxy is being updated, then this value may be empty.
    :var attrList: A list of name-value pairs (string, list of strings) used to specify additional property data for
    model view proxies.  All values are specified as strings, the caller is responsible for generating the correct
    string representation of each value passed.  For business object values, the UID of the object is used.
    :var thumbnailFile: The File to associate with the model view proxy to give a thumbnail of the model view. Value
    can be null.
    :var hiresImageFile: The File to associate with the model view proxy to give a higher resolution (versus the
    thumbnail) image of the model view. Value can be null.
    :var guardObjLastModifiedDate: If true, causes the update or delete of a model view proxy to check the proxy's last
    modified date to avoid data overwrite.
    :var objLastModifiedDateGuard: Modification date guard is used if 'guardObjLastModifiedDate' is set to true. Object
    update or delete will abort if the last modified date of the object is greater than 'objLastModifiedDateGuard'.
    """
    clientId: str = ''
    modelView: Fnd0ModelViewProxy = None
    boType: str = ''
    deleteProxy: bool = False
    owningModel: WorkspaceObject = None
    attrList: List[AttributeInfo] = ()
    thumbnailFile: ImanFile = None
    hiresImageFile: ImanFile = None
    guardObjLastModifiedDate: bool = False
    objLastModifiedDateGuard: datetime = None


@dataclass
class OwningModelAndCadLmd(TcBaseObj):
    """
    OwningModelAndCadLmd is used to identify when the CAD model views have last been modified. For each owning model
    object being passed in a OwningModelAndCadLmd input, all the owned model view proxies should be have their CAD last
    modified date synchronized to this date which is being provided.
    
    :var owningModel: The owning object which manages the actual CAD  model views which have a new date time. Required.
    :var cadLastModifiedDate: The date time at which at least some CAD model views have been most recently updated, and
    hence the date time to which the associated proxy objects should have their CAD last modified date set. Required.
    :var owningDataset: The owning dataset which manages the actual CAD  model views which have a new date time.
    Optional.
    """
    owningModel: WorkspaceObject = None
    cadLastModifiedDate: datetime = None
    owningDataset: Dataset = None


@dataclass
class CreateOrUpdateMVPaletteResponse(TcBaseObj):
    """
    The response contains a map of input caller specified 'clientId' values and the corresponding objects that were
    created or updated. The service data contains a list of added, updated, or deleted objects and it also contains a
    list of any errors which occurred within the call.
    
    :var clientIDMap: Map(string, Fnd0ModelViewPalette or Fnd0ModelViewGroup) of the various input 'clientId' to
    corresponding objects (Fnd0ModelViewPalette or Fnd0ModelViewGroup) that were created. Any input Info structures for
    which a 'clientId' wasn't provided will not have objects populated here but only within the 'serviceData'.
    :var serviceData: Contains a list of added, updated, or deleted objects.  Also contains list of any errors which
    occurred within the call.
    """
    clientIDMap: StringToBoMap = None
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateModelViewProxiesResponse(TcBaseObj):
    """
     The response contains a map of input caller specified client ID values and the corresponding objects that were
    created or updated. The service data contains a list of added, updated, or deleted objects and it also contains a
    list of any errors which occurred within the call.
    
    :var clientIDMap: Map (string, Fnd0ModelViewProxy) of the various input client IDs to corresponding objects
    (Fnd0ModelViewProxy) that were created.
    :var serviceData: Contains a list of added, updated, or deleted objects.  Also contains list of any errors which
    occurred within the call.
    """
    clientIDMap: StringToBoMap = None
    serviceData: ServiceData = None


"""
Generic map of a string to a business object.
"""
StringToBoMap = Dict[str, BusinessObject]
