from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ExpandAndSearchOutput(TcBaseObj):
    """
    ExpandAndSearchOutput contains the result BOMLine with the satisfied search condition indexes.
    
    :var resultLine: The result BOMLine. 
    :var satisfiedConditions: The indexes of search conditions satisfied by result line. Index will start from 0.
    """
    resultLine: BOMLine = None
    satisfiedConditions: List[int] = ()


@dataclass
class ExpandAndSearchResponse(TcBaseObj):
    """
     This structure provides output for the expandAndSearch operation. ExpandAndSearchResponse contains the list of a
    structure which contains result BOMLine with the satisfied search condition indexes.
    
    :var outputLines: Structure with result BOMLine with the satisfied search condition indexes.
    :var serviceData: The service data.
    """
    outputLines: List[ExpandAndSearchOutput] = ()
    serviceData: ServiceData = None


@dataclass
class SearchCondition(TcBaseObj):
    """
    Search condition contains the information of search criteria. This will form a condion as "bl_item_item_id =
    000016" where bl_item_item_id is a property and 000016 is input value given by a user for search. User can combine
    more than one conditions with logical operator 'AND' and 'OR' like "bl_item_item_id = 000016 AND
    bl_level_starting_0 != 4 AND bl_is_precise == false" . 
    
    Allowed relational operators:
    =       Use this operator for wild card search. This operator will do a wild card search for given value,       no
    need to give a '*'.
    ==  Use this operator to search exact match of search value
    !=      Use this operator to search other values except search value
    >      Use this operator to search greater value than search value
    >=  Use this operator to search greater and equal value than search value
    <      Use this operator to search lesser value than search value
    <=  Use this operator to search lesser and equal value than search value
    
    Note: Comparison will be done on the basis of BOMLine property type only.
    
    
    :var logicalOperator: The logical operator for combining multiple search conditions. Only 'AND' and 'OR' can be
    used for combining the multiple conditions.
    :var propertyName: The property name to use for search.
    :var relationalOperator: The relational operator to use for search value comparison.
    :var inputValue: The property value to use for search.
    """
    logicalOperator: str = ''
    propertyName: str = ''
    relationalOperator: str = ''
    inputValue: str = ''
