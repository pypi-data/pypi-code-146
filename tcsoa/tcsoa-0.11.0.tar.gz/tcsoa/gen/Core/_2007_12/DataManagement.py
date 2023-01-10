from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ImanType, IdContext, User, IdDispRule
from enum import Enum
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class AlternateIdentifiersInput(TcBaseObj):
    """
    Description of Alternate Identifiers to create.
    
    :var context: The IdContext to associate with the Alternate ID.
    :var identifierType: The Type of Alternate Identifier to create.
    :var mainObject: The Item to be associated with the Alternate ID.
    :var revObject: An ItemRevision to associate with the Alternate ID, optional.
    """
    context: IdContext = None
    identifierType: ImanType = None
    mainObject: IdentifierData = None
    revObject: IdentifierData = None


@dataclass
class GetContextAndIdentifiersResponse(TcBaseObj):
    """
    'GetContextAndIdentifierTypes' response
    
    :var contextAndIdentifierTypesMap: A map of context and identifier types for each requested ImanType
    (ImanType/'ContextAndIdentifierTypes')
    :var serviceData: Service data associated with the call
    """
    contextAndIdentifierTypesMap: ContextAndIdentifierTypesMap = None
    serviceData: ServiceData = None


@dataclass
class IdentifierData(TcBaseObj):
    """
    This structure contains information for Identifier data.
    
    :var identifiableObject: identifiableObject
    :var alternateId: alternateId
    :var additionalProps: additionalProps
    :var makeDefault: makeDefault
    """
    identifiableObject: BusinessObject = None
    alternateId: str = ''
    additionalProps: NameValueMap2 = None
    makeDefault: bool = False


@dataclass
class ListAlternateIdDisplayRulesInfo(TcBaseObj):
    """
    Input structure for 'ListAlternateIdDisplayRules' operation
    
    
    :var users: A list of users to return display rules for.
    :var currentUser: Flag to indicate display rules for current user.
    """
    users: List[User] = ()
    currentUser: bool = False


@dataclass
class ListAlternateIdDisplayRulesResponse(TcBaseObj):
    """
    Return structure 'ListAlternateIdDisplayRules'
    
    :var userDisplayRuleMaps: A list of maps of 'Teamcenter::UserImpl' to 'IdDisplayRules'.
    
    :var currentRuleInDB: The current rule in the database ( valid for current user only ).
    :var serviceData: 'ServiceData' associated with the call.
    """
    userDisplayRuleMaps: UserDisplayRuleMap = None
    currentRuleInDB: IdDispRule = None
    serviceData: ServiceData = None


@dataclass
class ValidateAlternateIdInput(TcBaseObj):
    """
    Input structure representing the alternate id to validate.
    
    :var clientId: Input 'clientId' to help the caller match the input to the output and identify error conditions.
    :var alternateId: The Item alternateId to be validated.
    :var alternateRevId: The ItemRevision alternate id to be validated.
    :var patternName: The name of the pattern for the alternate id. This is passed to the user exit
    'USER_validate_alt_id' for validation.
    :var context: The IdContext for the alternate id.
    :var identifierType: The ImanType for the Identifier.
    """
    clientId: str = ''
    alternateId: str = ''
    alternateRevId: str = ''
    patternName: str = ''
    context: IdContext = None
    identifierType: ImanType = None


@dataclass
class ValidateAlternateIdOutput(TcBaseObj):
    """
    This structure contains information for 'ValidateAlternateIdOutput'.
    
    :var clientId: Input 'clientId' to help the caller match the input to the output.
    :var modifiedAltId: Returned alternate id for the Item. This will be a modified id if the input id was invalid.
    :var modifiedAltRevId: Returned alternate id for the ItemRevision. This will be a modified id if the input id was
    invalid.
    :var validityId: Status of the validation for the alternate id for the Item. The values can be found in
    'Teamcenter::Soa::Core::_2007_12::DataManagement::ValidateIdsStatus'
    :var validityRevId: Status of the validation for the alternate id for the ItemRevision. The values can be found in
    'Teamcenter::Soa::Core::_2007_12::DataManagement::ValidateIdsStatus'
    """
    clientId: str = ''
    modifiedAltId: str = ''
    modifiedAltRevId: str = ''
    validityId: ValidateIdsStatus = None
    validityRevId: ValidateIdsStatus = None


@dataclass
class ValidateAlternateIdResponse(TcBaseObj):
    """
    Return structure containing a list of output corresponding to the input and the 'ServiceData'.
    
    :var output: List of 'ValidateAlternateIdOutput'.
    :var serviceData: The 'ServiceData' will contain the objects that are returned by the service call. Any partial
    errors will be mapped with input client id and error message in the 'ServiceData'.
    """
    output: List[ValidateAlternateIdOutput] = ()
    serviceData: ServiceData = None


@dataclass
class ContextAndIdentifierTypes(TcBaseObj):
    """
    This structure contains Context and Identifier Types.
    
    :var context: The IdContext
    :var identfierTypes: The list of ImanTypes that are valid for the IdContext
    """
    context: IdContext = None
    identfierTypes: List[ImanType] = ()


class ValidateIdsStatus(Enum):
    """
    A map of enum of the status for validating ids.
    """
    Valid = 'Valid'
    Invalid = 'Invalid'
    Modified = 'Modified'
    Override = 'Override'
    Duplicate = 'Duplicate'


"""
Map of name and values
"""
NameValueMap2 = Dict[str, List[str]]


"""
A map of user to 'IdDispRule'.
"""
UserDisplayRuleMap = Dict[User, List[IdDispRule]]


"""
Map of IManType to the list of 'ContextAndIdentifierTypes'.
"""
ContextAndIdentifierTypesMap = Dict[ImanType, List[ContextAndIdentifierTypes]]
