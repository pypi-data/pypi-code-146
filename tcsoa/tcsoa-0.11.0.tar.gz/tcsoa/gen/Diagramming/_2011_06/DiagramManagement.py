from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Fnd0DiagramRevision, ImanRelation, TransferMode, Fnd0DiagramTmplRevision, Fnd0ShapeRelation
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetDiagramMembersInputInfo(TcBaseObj):
    """
    'GetDiagramMembersInputInfo' structure represents the parameters required to get specific types of members from the
    diagram.
    
    :var membershipType: The membership type.
    :var diagramRevision: The Diagram Revision object.
    :var selectedObject: The Diagram Root object.
    """
    membershipType: int = 0
    diagramRevision: Fnd0DiagramRevision = None
    selectedObject: BusinessObject = None


@dataclass
class GetDiagramMembersOutput(TcBaseObj):
    """
    'GetDiagramMembersOutput' structure represents the output parameters.
    
    :var diagramMembers: A list of structure which holds the primary object, the shape relation object, the persistent
    object, the type of the object and a Boolean to indicate if user has manually removed this object's shape from the
    diagram.
    :var relationsOnDiagram: A list of structure which holds the relation object, the shape relation object, the
    primary and secondary objects of the relation, the type of the relation object and a Boolean to indicate if user
    has manually removed this object's shape from the diagram.
    """
    diagramMembers: List[DiagramMembers] = ()
    relationsOnDiagram: List[RelationsOnDiagram] = ()


@dataclass
class GetDiagramMembersResponse(TcBaseObj):
    """
    'GetDiagramMembersResponse' structure represents the output of the get diagram members operation.
    
    :var outputs: A list of 'GetDiagramMembersOutput' structures.
    :var serviceData: ServiceData
    """
    outputs: List[GetDiagramMembersOutput] = ()
    serviceData: ServiceData = None


@dataclass
class OpenDiagramInputInfo(TcBaseObj):
    """
    'OpenDiagramInputInfo' structure represents the parameters required to open a diagram.
    
    :var selectedObject: The Teamcenter object for which a Visio diagram will be created, either a Workspace object or
    a BOM Line.
    :var diagramRevision: The Diagram revision object.
    """
    selectedObject: BusinessObject = None
    diagramRevision: Fnd0DiagramRevision = None


@dataclass
class OpenDiagramOutput(TcBaseObj):
    """
    OpenDiagramOutput structure represents the parameters as a result of opening a diagram.
    
    :var diagramTmplFileTickets: A list of FMS tickets to the diagram stencils files associated with the diagram
    template.
    :var diagMappingFileTicket: FMS ticket to the diagram's property map file associated with the diagram template.
    :var diagramFileTicket: FMS ticket to the diagram's vdx file which is stored in the transient volume.
    :var diagramMembers: A list of structure which holds the primary object, the shape relation object, the persistent
    object, the type of the object and a Boolean to indicate if user has manually removed this object's shape from the
    diagram.
    :var relationsOnDiagram: A list of structure which holds the relation object, the shape relation object, the
    primary and secondary objects of the relation, the type of the relation object and a Boolean to indicate if user
    has manually removed this object's shape from the diagram.
    :var objectUIDvsShapeID: The map of the UIDs of all the objects and the Visio unique ids of their corresponding
    shapes (string/string).
    :var appDomain: The Application Domain name of the diagram.
    :var startObject: The root object of the diagram.
    """
    diagramTmplFileTickets: List[str] = ()
    diagMappingFileTicket: str = ''
    diagramFileTicket: str = ''
    diagramMembers: List[DiagramMembers] = ()
    relationsOnDiagram: List[RelationsOnDiagram] = ()
    objectUIDvsShapeID: ObjectUIDVsShapeID = None
    appDomain: str = ''
    startObject: BusinessObject = None


@dataclass
class OpenDiagramResponse(TcBaseObj):
    """
    'OpenDiagramResponse' structure represents the output of the open diagram operation.
    
    :var openDiagOutput: A list of OpenDiagramOutput structures.
    :var serviceData: The Service Data.
    """
    openDiagOutput: List[OpenDiagramOutput] = ()
    serviceData: ServiceData = None


@dataclass
class RelationsOnDiagram(TcBaseObj):
    """
    'RelationsOnDiagram' structure holds the details of the relations shown on the diagram.
    
    :var relation: The relation object to be shown on the diagram.
    :var shapeRelation: The relation object, which holds the shape information of Visio shape.
    :var primaryObject: The primary object of the relation, required to show the relation between the members.
    :var secondaryObject: The secondary object of the relation, required to show the relation between the members.
    :var relationType: The TC type name of the relation object.
    :var isRelationMemberOmitted: If true, indicates that the relation shape was removed from the diagram by the user.
    Such shapes can be restored.
    """
    relation: ImanRelation = None
    shapeRelation: Fnd0ShapeRelation = None
    primaryObject: BusinessObject = None
    secondaryObject: BusinessObject = None
    relationType: str = ''
    isRelationMemberOmitted: bool = False


@dataclass
class SaveDiagramInputInfo(TcBaseObj):
    """
    'SaveDiagramInputInfo' structure represents the parameters required to save a diagram.
    
    :var diagFileTicket: FMS ticket to the diagram's .vdx file to be saved.
    :var diagImageFileTicket: FMS ticket to the diagram's preview image to be saved.
    :var diagramRevision: The diagram revision object.
    :var selectedObject: The Teamcenter business object.
    """
    diagFileTicket: str = ''
    diagImageFileTicket: str = ''
    diagramRevision: Fnd0DiagramRevision = None
    selectedObject: BusinessObject = None


@dataclass
class SaveDiagramOutput(TcBaseObj):
    """
    'SaveDiagramOutput' structure represents the output parameters as a result of saving a diagram.
    
    :var resultObjects: A list of Teamcenter objects, which appear on the diagram, for which shape relations are
    created during the saving of the diagram.
    """
    resultObjects: List[BusinessObject] = ()


@dataclass
class SaveDiagramResponse(TcBaseObj):
    """
    'SaveDiagramResponse' structure represents the output of the save diagram operation.
    
    :var saveDiagOutput: A list of SaveDiagramOutput structures.
    :var serviceData: The Service Data.
    """
    saveDiagOutput: List[SaveDiagramOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateDiagramInputInfo(TcBaseObj):
    """
    The parameters required to create a diagram.
    
    :var selectedObject: Teamcenter business object for which a Visio diagram will be created.
    :var openDiagram: If true, the created Visio diagram will be opened upon creation.
    :var propNamevsValueMap: A map of property names and values (string/string). Valid keys are Description, Name,
    templateName and ID.
    """
    selectedObject: BusinessObject = None
    openDiagram: bool = False
    propNamevsValueMap: PropNamevsPropValueMap = None


@dataclass
class CreateDiagramOutput(TcBaseObj):
    """
    'CreateDiagramOutput' structure represents the output parameters as a result of creating a diagram.
    
    :var diagramTmplFileTickets: A list of FMS tickets to the diagram stencils files associated with the diagram
    template.
    :var diagMappingFileTicket: The FMS ticket to the diagram's property map file associated with the diagram template.
    :var diagramRev: The newly created Diagram Revision object.
    :var diagramMembers: A list of diagram members, each element holds the primary object, the shape relation object,
    the persistent object, the type of the object and a Boolean to indicate if user has manually removed this object's
    shape from the diagram.
    :var relationsOnDiagram: A list of relations on the created diagram. Each element holds the relation object, the
    shape relation object, the primary and secondary objects of the relation, the type of the relation object and a
    Boolean to indicate if user has manually removed this object's shape from the diagram.
    :var appDomain: The Application Domain name of the diagram.
    """
    diagramTmplFileTickets: List[str] = ()
    diagMappingFileTicket: str = ''
    diagramRev: Fnd0DiagramRevision = None
    diagramMembers: List[DiagramMembers] = ()
    relationsOnDiagram: List[RelationsOnDiagram] = ()
    appDomain: str = ''


@dataclass
class CreateDiagramResponse(TcBaseObj):
    """
    'CreateDiagramResponse' structure represents the output of create diagram operation.
    
    :var createDiagOutput: A list of created diagrams
    :var serviceData: The Service Data.
    """
    createDiagOutput: List[CreateDiagramOutput] = ()
    serviceData: ServiceData = None


@dataclass
class CreateOrUpdateTemplateInputInfo(TcBaseObj):
    """
    CreateOrUpdateTemplateInputInfo structure represents the parameters required to create a diagram template.
    
    :var available: If true, the Diagram Template is available for use.
    :var tmplStencilFileTickets: A list of FMS tickets to the Diagram tool specific stencils or Template files.
    :var tmplMappingFileTicket: FMS ticket to the Property Map xml file.
    :var membershipRule: The Transfer mode, which will be used for traversing the structure for the diagram root object.
    :var relationRule: The Relation Rule which is the list of relations between the objects shown on the diagram.
    :var diagramTmplRev: The updated template object.
    :var propNamevsPropValueMap: A map of property names and values (string/string). Valid keys are Description, Name,
    templateName and ID.
    """
    available: bool = False
    tmplStencilFileTickets: List[str] = ()
    tmplMappingFileTicket: str = ''
    membershipRule: TransferMode = None
    relationRule: List[str] = ()
    diagramTmplRev: Fnd0DiagramTmplRevision = None
    propNamevsPropValueMap: PropNamevsPropValueMap = None


@dataclass
class CreateOrUpdateTemplateOuput(TcBaseObj):
    """
    'CreateOrUpdateTemplateOuput' structure represents the output parameters required for creating or updating a
    diagram template.
    
    :var diagramTmplRev: The created or updated  template object.
    """
    diagramTmplRev: Fnd0DiagramTmplRevision = None


@dataclass
class CreateOrUpdateTemplateResponse(TcBaseObj):
    """
    'CreateOrUpdateTemplateResponse' structure represents the list of 'CreateOrUpdateTemplateOuput' structures as a
    result of creating or updating a diagram template.
    
    :var outputs: A list of CreateOrUpdateTemplateOuput structures, which hold the information of created templates.
    :var serviceData: If true, the created Visio diagram will be opened on creation.
    """
    outputs: List[CreateOrUpdateTemplateOuput] = ()
    serviceData: ServiceData = None


@dataclass
class DiagramMembers(TcBaseObj):
    """
    'DiagramMembers' structure holds the details of the members shown on the diagram.
    
    :var primaryObject: The primary object of the shape shown on the diagram.
    :var shapeRelation: The relation object, which holds the shape information of Visio shape.
    :var persistentObject: The persistent object of the primary object shown on the diagram.
    :var objectTCTypeName: The TC type name of the object.
    :var isMemberOmitted: If true, indicates that the shape was removed from the diagram by the user. Such shapes can
    be restored.
    """
    primaryObject: BusinessObject = None
    shapeRelation: Fnd0ShapeRelation = None
    persistentObject: BusinessObject = None
    objectTCTypeName: str = ''
    isMemberOmitted: bool = False


"""
A Map that holds the collection of object UID for the object that appears on diagram as key vs the ID of the Shape that this object represent on diagram as value.
"""
ObjectUIDVsShapeID = Dict[str, int]


"""
This  map contains the property name and its value.
"""
PropNamevsPropValueMap = Dict[str, str]
