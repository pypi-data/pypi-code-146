from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject, RevisionRule, ItemRevision
from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetConfiguredItemRevisionInfo(TcBaseObj):
    """
    Contains the item/item revision object reference and revision rule object reference to find the configured
    itemRevision.
    
    :var object: object reference of the item / item revision
    :var revRule: Teamcenter::RevisionRuleImpl object reference
    """
    object: BusinessObject = None
    revRule: RevisionRule = None


@dataclass
class GetConfiguredItemRevisionOutput(TcBaseObj):
    """
    The response for the getConfiguredItemRevision operation.
    
    :var inputInfo: Member of type GetConfiguredItemRevisionInfo, copy of input data
    :var configuredItemRev: ItemRevision object reference found
    """
    inputInfo: GetConfiguredItemRevisionInfo = None
    configuredItemRev: ItemRevision = None


@dataclass
class GetConfiguredItemRevisionResponse(TcBaseObj):
    """
    The response for the getConfiguredItemRevision call.
    
    :var output: A List of type GetConfiguredItemRevisionOutput
    :var serviceData: The SOA framework object containing plain objects and error information.
    """
    output: List[GetConfiguredItemRevisionOutput] = ()
    serviceData: ServiceData = None


@dataclass
class VariantCondInfo(TcBaseObj):
    """
    Contains the information neede to create/update a variant condition.
    
    :var optionName: optionName
    :var joinOperator: joinOperator  Legal values are: 'AND', 'OR', 'OPEN_BRACKET' and 'CLOSE_BRACKET'.
    :var compOperator: compOperator. Legal values are: 'EQ', 'NEQ', 'LT', 'GT', 'GTEQ' and 'LTEQ'.
    :var value: value
    """
    optionName: str = ''
    joinOperator: VariantOperator = None
    compOperator: ComparisonOperator = None
    value: str = ''


@dataclass
class ClassicOptionInfo(TcBaseObj):
    """
    Contains the information about classic variant option.
    
    :var optionName: Refers to classic variant option name.
    :var optionDesc: Refers to classic variant option description.
    :var values: Refers to list of classic variant option values. This input is given for new or update scenarios.
    :var existingValues: Refers to list of existing classic variant option values.
    """
    optionName: str = ''
    optionDesc: str = ''
    values: List[str] = ()
    existingValues: List[str] = ()


@dataclass
class CreateOrUpdateVariantCondInput(TcBaseObj):
    """
    Contains the input for create/update variant condition associated with a BOMLine object.
    
    :var clientId: Identifier that helps the client to track the object(s) created.
    :var operation: This indicates the operation type which can be create or update variant condition. Legal values
    are: 'Create' and 'Update'.
    :var bomLine: Refers to BOMLine object on which variant condition has been defined.
    :var variantCondInfo: Refers to a list of 'VariantCondInfo' struct, and contains the information needed to
    create/update a variant condition.
    """
    clientId: str = ''
    operation: Operation = None
    bomLine: BOMLine = None
    variantCondInfo: List[VariantCondInfo] = ()


@dataclass
class CreateUpdateClassicOptionsInput(TcBaseObj):
    """
    Contains the input for creating or updating classic variant options associated with a BOMLine object.
    
    :var clientId: Refers to clientId attribute.
    :var operation: Refers to operation type, as defined in 'OptionOperation'. The operation could be 'CreateOption',
    'AddValue', 'RemoveValue' or 'ReplaceValue'.
    :var bomLine: Refers to BOMLine object on which classic variant options are created or updated.
    :var options: Refers to list of 'ClassicOptionInfo' structure which needs to be updated.
    """
    clientId: str = ''
    operation: OptionOperation = None
    bomLine: BOMLine = None
    options: List[ClassicOptionInfo] = ()


@dataclass
class DelClassicOptionsInput(TcBaseObj):
    """
    Contains the input for deleting variant condition associated with a BOMLine object.
    
    :var clientId: Identifier that helps the client to track the object(s) created.
    :var bomLine: Refers to BOMLine object on which classic variant options are defined, which needs to be deleted.
    :var optionNames: Refers to list of classic variant option names which are needs to be deleted.
    """
    clientId: str = ''
    bomLine: BOMLine = None
    optionNames: List[str] = ()


@dataclass
class DeleteVariantCondInput(TcBaseObj):
    """
    This contains the input for deleting variant condition associated with a BOMLine object.
    
    :var clientId: Identifier that helps the client to track the object(s) created.
    :var bomLine: Refers to BOMLine object on which variant conditions are defined, which needs to be deleted.
    """
    clientId: str = ''
    bomLine: BOMLine = None


class ComparisonOperator(Enum):
    """
    Contains comparison operator. Legal values are: 'EQ, NEQ, LT, GT, GTEQ' and 'LTEQ'.
    """
    EQ = 'EQ'
    NEQ = 'NEQ'
    LT = 'LT'
    GT = 'GT'
    GTEQ = 'GTEQ'
    LTEQ = 'LTEQ'


class Operation(Enum):
    """
    Contains the operation type. Legal values are: 'Create' and 'Update'.
    """
    Create = 'Create'
    Update = 'Update'


class OptionOperation(Enum):
    """
    The operations on variant option. Legal values 'are: CreateOption' ,'AddValue' ,'RemoveValue'  and 'ReplaceValue'.
    """
    CreateOption = 'CreateOption'
    AddValue = 'AddValue'
    RemoveValue = 'RemoveValue'
    ReplaceValue = 'ReplaceValue'


class VariantOperator(Enum):
    """
    Contains the join operator type. Legal values are: 'AND, OR '.
    """
    AND = 'AND'
    OR = 'OR'
