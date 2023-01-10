from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ReportDefinition
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GenerateReportsCriteria2(TcBaseObj):
    """
    The criteria object needed to generate report.
    
    :var clientId: The client identifier for routing purposes (required).
    :var rdTag: The Report Definition ID.
    :var datasetCtxUID: The uid for the context Dataset.
    :var datasetCtxObj: The Dataset context ID.
    :var relationName: The relation name to be used.
    :var datasetType: The Dataset type to be used.
    :var reportOptionsNames: A list of strings containing the Names in a series of Name/Value pairs used to specify
    additional criteria (optional).
    :var reportOptionsValues: A list of strings containing the Names in a series of Name/Value pairs used to specify
    additional criteria (optional).
    :var reportName: Designates the name of the report given the rdTag is not supplied.
    :var stylesheetTag: The report style ID (optional).
    :var stylesheetName: The name of the report style if known
    :var contextObjects: A list of ID's representing context object(s) (required for item reports).
    :var contextObjectUIDs: A list of uids representing context objects.
    :var datasetName: The name of containing DataSet (optional).
    :var criteriaNames: A list of strings containing the Names in a series of Name/Value pairs used to specify criteria
    for saved queries(optional).
    :var criteriaValues: A list of strings containing the Values in a series of Name/Value pairs used to specify
    criteria for saved queries(optional).
    """
    clientId: str = ''
    rdTag: ReportDefinition = None
    datasetCtxUID: str = ''
    datasetCtxObj: BusinessObject = None
    relationName: str = ''
    datasetType: str = ''
    reportOptionsNames: List[str] = ()
    reportOptionsValues: List[str] = ()
    reportName: str = ''
    stylesheetTag: BusinessObject = None
    stylesheetName: str = ''
    contextObjects: List[BusinessObject] = ()
    contextObjectUIDs: List[str] = ()
    datasetName: str = ''
    criteriaNames: List[str] = ()
    criteriaValues: List[str] = ()
