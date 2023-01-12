from __future__ import annotations

from tcsoa.gen.BusinessObjects import WorkspaceObject, ImanType, IdContext, Item, ItemRevision
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class IDContextOut(TcBaseObj):
    """
    The IDContextOut is list of  IdContext objects. It also contains the input object of type Item or ItemRevision.
    
    :var inputObj: Input object of type WorkspaceObject or null for which the list of IdContext objects are fetched.
    :var idContexts: A list of all IdContext objects found in the Teamcenter database.
    """
    inputObj: WorkspaceObject = None
    idContexts: List[IdContext] = ()


@dataclass
class IDContextOutput(TcBaseObj):
    """
    The IDContextOutput is list of IdContextOut objects. It also contains the instance of ServiceData for the operation.
    
    :var idContextOuts: A list of IdContextOut structures which holds the list of IdContext objects and input object of
    type WorkspaceObject or null.
    :var serviceData: Any partial errors encountered during this operation are returned in the list of partial errors
    of the ServiceData.
    """
    idContextOuts: List[IDContextOut] = ()
    serviceData: ServiceData = None


@dataclass
class IDDispRuleCreateIn(TcBaseObj):
    """
    The IDDispRuleCreateIn structure is used to hold the name of the ID Display Rule, list of ID Context objects and a
    flag whether to set the ID Display Rule being created as the default ID Display Rule.
    
    :var ruleName: Name of the ID Display Rule being created.
    :var idContexts: A list of input IdContext objects to be set with the IdDispRule object being created.
    :var useDefault: If true, the created IdDispRule object is set as the default ID Display Rule for the user;
    otherwise, the existing default ID Display Rule will remain the default.
    :var setCurrent: If true, the created IdDispRule object is set as the current ID Display Rule for the user;
    otherwise, the existing current ID Display Rule will remain the current.
    """
    ruleName: str = ''
    idContexts: List[IdContext] = ()
    useDefault: bool = False
    setCurrent: bool = False


@dataclass
class IdentifierTypesIn(TcBaseObj):
    """
    The IdentifierTypesIn structure is used to hold the input Item or ItemRevision object and the input IdContext
    object.
    
    :var inputItemOrRev: Input Item or ItemRevision object for which the Identifier type is being fetched.
    :var idContext: Input IdContext object used to fetch the Identifier type for the input Item or ItemRevision from
    the defined ID Display Rules.
    """
    inputItemOrRev: WorkspaceObject = None
    idContext: IdContext = None


@dataclass
class IdentifierTypesOut(TcBaseObj):
    """
    The IdentifierTypesOut is list of IdentifiersOut objects. It also contains the instance of ServiceData for the
    operation.
    
    :var identifiersOutput: A list of IdentifiersOut structures which holds list of Identifier types, object of type
    Item and list of ItemRevision objects, applicable for defining the Alternate IDs.
    :var serviceData: Any partial errors encountered during this operation are returned in the list of partial errors
    of the ServiceData.
    """
    identifiersOutput: List[IdentifiersOut] = ()
    serviceData: ServiceData = None


@dataclass
class IdentifiersOut(TcBaseObj):
    """
    The IdentifiersOut structure is used to hold the list of Identifier types, applicable object of type Item and list
    of ItemRevision objects, applicable for defining the Alternate IDs.
    
    :var inputItemOrRev: Input Item or ItemRevision object for which the Identifier type is being fetched.
    :var identifierTypes: A list of valid Identifier types which can be used to define the Alternate and Alias IDs of
    the input object.
    :var item: Item object of the given input ItemRevision for which Alternate IDs can be defined.
    :var revisions: A list containing all revisions of the input Item for which Alternate IDs can be defined.
    """
    inputItemOrRev: WorkspaceObject = None
    identifierTypes: List[ImanType] = ()
    item: Item = None
    revisions: List[ItemRevision] = ()
