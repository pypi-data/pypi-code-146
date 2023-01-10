from __future__ import annotations

from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetDiagnosticInfoForAcctTablesResp(TcBaseObj):
    """
    The return data for getDiagnosticInfoForAcctTables operation.
    
    :var tableInfos: The list of table diagnostic information structures.
    :var serviceData: The service data that includes any partial errors.
    """
    tableInfos: List[TableDiagnosticInfo] = ()
    serviceData: ServiceData = None


@dataclass
class NameValuesInfo(TcBaseObj):
    """
    The information type name and information values structure.
    
    :var infoType: The information type name.
    :var infoValues: The list of information values.
    """
    infoType: str = ''
    infoValues: List[str] = ()


@dataclass
class TableDiagnosticInfo(TcBaseObj):
    """
    The table name and table information structure.
    
    :var tableName: The table name.
    :var tableInfos: The list of table information type name and values.
    """
    tableName: str = ''
    tableInfos: List[NameValuesInfo] = ()
