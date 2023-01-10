from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RbfNameValue(TcBaseObj):
    """
    The name of the input or output column along with the data value on a application extension rule.
    
    :var name: The input or output column name from the application extension rule.
    :var value: The value of the named column.
    """
    name: str = ''
    value: RbfValue = None


@dataclass
class RbfValue(TcBaseObj):
    """
    The value for an input or output column on an Application Extension Rule.
    
    :var dataType: The type of data the structure is holding. It will have one of the following values: ' STRING,
    BOOLEAN, INTEGER, DOUBLE, FLOAT, DATE, or TAG'.
    :var stringValue: The 'STRING' value for the column.
    :var booleanValue: The 'BOOLEAN' value for the column.
    :var integerValue: The 'INTEGER' value for the column.
    :var doubleValue: The 'DOUBLE' value for the column.
    :var floatValue: The 'FLOAT' value for the column.
    :var dateValue: The 'DATE' value for the column.
    :var tagValue: The 'TAG' value for the column.
    """
    dataType: str = ''
    stringValue: str = ''
    booleanValue: bool = False
    integerValue: int = 0
    doubleValue: float = 0.0
    floatValue: float = 0.0
    dateValue: datetime = None
    tagValue: BusinessObject = None


@dataclass
class ExecuteRbfRulesResponse(TcBaseObj):
    """
    Holds the response for the 'executeRbfRules' operation.
    
    :var outputs: This is a set of output name/value pairs from the rules engine execution.
    :var serviceData: This contains the status of the operation.
    """
    outputs: List[RbfNameValue] = ()
    serviceData: ServiceData = None
