from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, Fnd0ApprSchCriteriaScpAttr, Fnd0ApprSchCriteriaFormAttr, SearchStructureContext
from tcsoa.gen.Rdv._2010_09.ContextManagement import StructureCntxtObjectInfo, CreateSCOInputInfo
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetICSClassNamesResponse(TcBaseObj):
    """
    This structure contains the ICS class names and error, if any, in 'ServiceData' object.
    
    :var icsClassNames: ICS Class names for the corresponding     ApprSearchCriteriaInClass objects provided     in
    input paramter.
    :var serviceData: Contains any exceptions if occurred while getting the class name of InClass Search Criteria
    object.
    """
    icsClassNames: List[str] = ()
    serviceData: ServiceData = None


@dataclass
class UpdateSearchSCOInputInfo(TcBaseObj):
    """
    This structure contains the Search Structure Context Object, the 'StructureCntxtObjectInfo' object containing
    information to be updated, a flag to indicate if results should be stored or not and the scope bomlines.
    
    :var srchSCO: Search Structure Context Object that needs to be updated. This SCO object will be updated with the
    modified values.
    
    :var scoInfo: Object of 'StructureCntxtObjectInfo' structure. It internally holds all the details related to the
    search criteria and search results.
    :var resultStored: Describes whether the results are stored or not.
    :var nodes: It is a vector of all the scope bomlines used.
    """
    srchSCO: SearchStructureContext = None
    scoInfo: StructureCntxtObjectInfo = None
    resultStored: bool = False
    nodes: List[BusinessObject] = ()


@dataclass
class UpdateSearchSCOResponse(TcBaseObj):
    """
    This structure contains the list of updated SearchStructureContext object and error, if any, in 'ServiceData'
    object.
    
    :var srchSCO: Vector of object of SearchStructureContext updated with the supplied inputs.
    :var serviceData: Contains any exception that occurred during updating the SearchSCO.
    """
    srchSCO: List[SearchStructureContext] = ()
    serviceData: ServiceData = None


@dataclass
class CreateFormAttrSearchCriteriaInputInfo(TcBaseObj):
    """
    Specifies the full set of inputs required to create the Form Search Criteria object.
    
    :var relationtype: Type name of Relation with which Form is attached to an Item/Item Revision. (For example:
    References). The valid relation types can be fetched from BMIDE: Open BMIDE->Go to Business Objects View->Search
    for ImanRelation->Expand ImanRelation. The name of any object listed as child of ImanRelation, can be supplied.
    :var parentType: Boolean value indicating type of parent (true if the parent type is Item and false if the parent
    type is Item Revision)
    :var formType: Type name of Form being used for the search. The valid form type can be fetched from BMIDE: Open
    BMIDE->Go to Business Objects View->Search for Form. The name of any object listed as child of 'Form' can be
    supplied.
    :var logicalOpr: Logical operator. The only valid operator currently supported is 'AND'.
    :var propertyName: Name of the selected property on the form used for the search.
    :var mathOpr: Operator used for comparison. List of valid operators: 
    - 'EQ' - Equal
    - 'NE' - Not Equal
    - 'GT' - Greater Than
    - 'GE' - Greater Than or Equal
    - 'LT' - Less Than
    - 'LE' - Less Than or Equal
    - 'LIKE'
    - 'NOT LIKE'
    
    
    :var propertyType: Name of the type of property. The valid string values for this member are: 
    - 'BooleanType' - For Boolean Property
    - 'DateType' - For Date Property
    - 'IntegerType' - For Integer Property
    - 'StringType' - For String Property
    - 'DoubleType' - For Double Property
    - 'TagType' - For Tag Property
    
    
    :var values: List of string values used for the search. Each value specified here would be an appropriate value for
    the property specified in 'propertyName' parameter. These     values are passed in string format and converted back
    to their original format based on the 'propertyType' parameter specified above.
    """
    relationtype: str = ''
    parentType: bool = False
    formType: str = ''
    logicalOpr: str = ''
    propertyName: str = ''
    mathOpr: str = ''
    propertyType: str = ''
    values: List[str] = ()


@dataclass
class CreateFormAttrSearchCriteriaResponse(TcBaseObj):
    """
    Contains the list of newly created Fnd0ApprSchCriteriaFormAttr objects and 'ServiceData' object
    
    :var formAttrSchCriteria: List of newly created Fnd0ApprSchCriteriaFormAttr objects.
    :var serviceData: An object of 'ServiceData' which contains any exceptions if occurred during creation of Form
    attribute object.
    """
    formAttrSchCriteria: List[Fnd0ApprSchCriteriaFormAttr] = ()
    serviceData: ServiceData = None


@dataclass
class CreateSearchCriteriaScopeInfo(TcBaseObj):
    """
    This structure is used to store the list of scope BOMLine objects and the Apprearance Goup objects.
    
    :var nodes: List of all the scope BOMLine objects. If the search is performed on occurrence group object then this
    list will be empty.
    
    :var collections: It is a vector of BusinessObjects. If search is performed on one or more Occurrence group BOMLine
    objects then this list should have those occurrence group objects.
    """
    nodes: List[BusinessObject] = ()
    collections: List[BusinessObject] = ()


@dataclass
class CreateSearchCriteriaScpResponse(TcBaseObj):
    """
    This structure is used to store information about the newly created Fnd0ApprSchCriteriaScpAttr objects and
    'ServiceData' object after execution of the operation 'createSearchCriteriaScope'.
    
    :var searchCriteriaScpObjects: The list of objects of Fnd0ApprSchCriteriaScpAttr created by the
    'createSearchCriteriaScope' action.
    :var serviceData: An object of 'ServiceData' which contains any exceptions if occurred during the creation of Scope
    Search Criteria object
    """
    searchCriteriaScpObjects: List[Fnd0ApprSchCriteriaScpAttr] = ()
    serviceData: ServiceData = None


@dataclass
class CreateSearchSCOInputInfo(TcBaseObj):
    """
    This structure is used to store additional information about a SCO object such as the availability of results,
    option to specify if SCO is shared or not.
    
    :var scoInputInfo: It is an object of 'CreateSCOInputInfo' structure which contains name, description, search
    criteria information.
    :var resultStored: Specifies whether results are stored or not in the SearchSCO.
    :var isShared: Specifies whether the SearchSCO object will be shared with other users or not.
    :var nodes: List of all the scope bomlines used to store additional information in the SearchSCO.
    """
    scoInputInfo: CreateSCOInputInfo = None
    resultStored: bool = False
    isShared: bool = False
    nodes: List[BusinessObject] = ()


@dataclass
class CreateSearchSCOResponse(TcBaseObj):
    """
    The CreateSearchSCOResponse structure represents search structure context object created and the service data.
    
    :var srchSCO: The vector of objects of SearchStructureContext created by the 'createSearchSCO' action
    
    :var serviceData: An object of 'ServiceData' which contains any exceptions if occurred during creation of SearchSCO
    """
    srchSCO: List[SearchStructureContext] = ()
    serviceData: ServiceData = None
