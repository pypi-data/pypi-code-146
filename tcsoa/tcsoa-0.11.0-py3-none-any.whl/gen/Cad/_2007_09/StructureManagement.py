from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from enum import Enum
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class VariantCondInfo(TcBaseObj):
    """
    Contains the information related to classic variant condition.
    
    :var optionName: Refers to the classic variant option name.
    :var itemId: Refers to item id where classic variant option is defined.
    :var joinOperator: Refers to 'VariantOperator'.  Legal values are: 'AND', 'OR', 'OPEN_BRACKET' and 'CLOSE_BRACKET'.
    :var compOperator: Refers to 'ComparisonOperator'.  Legal values are: 'EQ', 'NEQ', 'LT', 'GT', 'GTEQ' and 'LTEQ'.
    :var value: Refers to classic variant option value.
    """
    optionName: str = ''
    itemId: str = ''
    joinOperator: VariantOperator = None
    compOperator: ComparisonOperator = None
    value: str = ''


@dataclass
class CreateOrUpdateVariantCondInput(TcBaseObj):
    """
    Contains the input for create/update variant condition associated with a BOMLine object.
    
    :var clientId: Identifier that helps the client to track the object(s) created.
    :var operation: Refers to 'Operation' which refers to the operation type. Legal values are: 'Create' and 'Update'.
    :var bomLine: Refers to BOMLine object on which variant condition has been defined.
    :var variantCondInfo: Refers to a list of 'VariantCondInfo' struct, and contains the information needed to
    create/update a variant condition.
    """
    clientId: str = ''
    operation: Operation = None
    bomLine: BOMLine = None
    variantCondInfo: List[VariantCondInfo] = ()


class ComparisonOperator(Enum):
    """
    Contains comparison operator. Legal values are:' EQ, NEQ, LT, GT, GTEQ' and 'LTEQ'.
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


class VariantOperator(Enum):
    """
    Contains the join operator type. Legal values are: 'AND', 'OR, OPEN_BRACKET' and 'CLOSE_BRACKET'.
    """
    AND = 'AND'
    OR = 'OR'
    OPEN_BRACKET = 'OPEN_BRACKET'
    CLOSE_BRACKET = 'CLOSE_BRACKET'
