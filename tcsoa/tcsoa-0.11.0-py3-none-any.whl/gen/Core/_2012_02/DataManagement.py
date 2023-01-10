from __future__ import annotations

from tcsoa.gen.Core._2008_06.DataManagement import CreateInput
from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject, Folder
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BulkCreIn(TcBaseObj):
    """
    Input for bulk create operation including unique client identifier.
    
    :var clientId: client id Unique client identifier.
    :var quantity: Number of instances of each type for creation.For Asp0Aspect objects,'CreateInput' needs to be
    populated with the number of Asp0Aspect objects to be created hence quantity should be passed as 1.
    :var folder: Containing folder for the newly created items.
    :var data: Input data for create operation.
    """
    clientId: str = ''
    quantity: int = 0
    folder: Folder = None
    data: CreateInput = None


@dataclass
class ValidationResponse(TcBaseObj):
    """
    Return structure for 'createConnections' operation
    
    :var validationResult: A map of type <'std::string ,bool'> indicating if the ID is valid. The key is clientId from
    'CreateIn'.  The value is true if the id is valid, otherwise id is invalid.
    :var serviceData: Service data
    """
    validationResult: ValidationResult = None
    serviceData: ServiceData = None


@dataclass
class WhereUsedConfigParameters(TcBaseObj):
    """
    Additional Configuration Parameters required for 'whereUsed' search. For example 'tagMap' to specify the
    RevisionRule with revision_rule as a key, 'boolMap' to specify 'whereUsedPreciseFlag' with whereUsedPreciseFlag as
    a key, and 'intMap' to specify number of levels with numLevels as a key.
    
    :var stringMap: String Input parameters ( std::string, std::string )
    :var doubleMap: Double Input parameters ( std::string, double )
    :var intMap: int Input parameters ( std::string, int )
    :var boolMap: bool Input parameters ( std::string, bool )
    :var dateMap: Date Input parameters ( std::string, Teamcenter::DateTime )
    :var tagMap: Object Input parameters   ( std::string, BusinessObjectRef ( Teamcenter::BusinessObject ) )
    :var floatMap: Float Input Parameters ( std::string, float )
    """
    stringMap: WUStringMap = None
    doubleMap: WUDoubleMap = None
    intMap: WUIntMap = None
    boolMap: WUBoolMap = None
    dateMap: WUDateMap = None
    tagMap: WUTagMap = None
    floatMap: WUFloatMap = None


@dataclass
class WhereUsedInputData(TcBaseObj):
    """
    Input data for 'whereUsed' search contains the target object to perform search along with the configuration
    parameters.
    
    :var inputObject: Target object to do 'whereUsed' search
    :var useLocalParams: Flag to decide which config paramerters to be used, local or common
    :var inputParams: Additional Configuration Parameters required for 'whereUsed' search
    :var clientId: Client ID to uniquely idnetify this input data
    """
    inputObject: WorkspaceObject = None
    useLocalParams: bool = False
    inputParams: WhereUsedConfigParameters = None
    clientId: str = ''


@dataclass
class WhereUsedOutputData(TcBaseObj):
    """
    This structure contains output information of Where Used Call.
    
    :var inputObject: Input object
    :var info: List of where used result objects
    :var clientId: Client ID of input object which this output object is for
    """
    inputObject: WorkspaceObject = None
    info: List[WhereUsedParentInfo] = ()
    clientId: str = ''


@dataclass
class WhereUsedParentInfo(TcBaseObj):
    """
    Generic Parent Info Structure
    
    :var parentObject: Parent Workspace Object
    :var level: levet at which parent is found
    """
    parentObject: WorkspaceObject = None
    level: int = 0


@dataclass
class WhereUsedResponse(TcBaseObj):
    """
    'WhereUsedResponse' object contains list of  'WhereUsedOutputData' structure. This structure contains list of
    ItemRevision objects which are result of 'whereUsed' search.
    
    :var output: List of 'WhereUsedOutputData' structures
    :var serviceData: Standard 'ServiceData' Member
    """
    output: List[WhereUsedOutputData] = ()
    serviceData: ServiceData = None


"""
A map of type bool indicating if the ID is valid. The key is clientId from 'CreateIn'. The value is of type bool.  True if id is valid, otherise id is invalid
"""
ValidationResult = Dict[str, bool]


"""
Map of bool property names to values ('string, bool').
"""
WUBoolMap = Dict[str, bool]


"""
Map of DateTime property names to values '(string, DateTime').
"""
WUDateMap = Dict[str, datetime]


"""
Map of double property names to values ('string, double').
"""
WUDoubleMap = Dict[str, float]


"""
Map of float property names to values ('string, float').
"""
WUFloatMap = Dict[str, float]


"""
Map of int property names to values ('string, in').
"""
WUIntMap = Dict[str, int]


"""
Map of sting property names to values '(string, string').
"""
WUStringMap = Dict[str, str]


"""
 Map of BusinessObject property names to values ('string, BusinessObject').
"""
WUTagMap = Dict[str, BusinessObject]
