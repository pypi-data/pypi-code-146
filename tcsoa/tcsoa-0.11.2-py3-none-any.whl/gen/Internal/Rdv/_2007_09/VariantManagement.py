from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, NamedVariantExpression
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetVariantExprAllDataResponse(TcBaseObj):
    """
    This structure contains the XO chart related information and the 'ServiceData' object.
    
    :var nveData: An object containing all the NVEs information and their XO chart data related information.
    :var serviceData: An object of ServiceData which contains any exceptions if occurred during creation of XO chart
    data.
    """
    nveData: VariantExprAllData = None
    serviceData: ServiceData = None


@dataclass
class VariantExprAllData(TcBaseObj):
    """
    This structure contains all the NVEs information and their XO chart data related information.
    
    :var varExprXOData: An object containing information required to display the XO chart
    :var codeDescData: List of VariantExprCodeDescData structure
    """
    varExprXOData: VariantExprXOChartData = None
    codeDescData: List[VariantExprCodeDescData] = ()


@dataclass
class VariantExprCodeDescData(TcBaseObj):
    """
    This structure is used to store the NVE related information like NVE object reference, name and description.
    
    :var nve: The NVE object
    :var code: Name of the Named Variant Expression
    :var desc: Description of the NamedVariantExpression
    """
    nve: NamedVariantExpression = None
    code: str = ''
    desc: str = ''


@dataclass
class VariantExprXOChartData(TcBaseObj):
    """
    This structure contains the XO chart information such as table header strings, number of rows and columns.
    
    :var noOfColHeaders: Number of column header to display in the UI
    :var colHeaderExprs: list of col header expressions
    :var noOfRows: Number of rows to display in the UI
    :var noOfCols: Number of columns in the UI
    :var noOfTableChars: Number of table characters
    :var tableChars: The octal string representation of the table char bytes
    :var colHeaderExprStrs: Values for the column headers. Format of value will be like option name=value ex. Color=Blue
    """
    noOfColHeaders: int = 0
    colHeaderExprs: List[BusinessObject] = ()
    noOfRows: int = 0
    noOfCols: int = 0
    noOfTableChars: int = 0
    tableChars: str = ''
    colHeaderExprStrs: List[str] = ()
