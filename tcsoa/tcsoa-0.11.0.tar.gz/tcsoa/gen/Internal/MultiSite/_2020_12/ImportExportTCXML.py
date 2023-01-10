from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class MultisiteDashboardResponse(TcBaseObj):
    """
    Return structure for getMultisiteDashBoardData operation.
    
    :var dashboardData: A map (string, string) of report id and dashboard data in JSON format  for the report recipe
    provided  by the user. The Dashboard data help to track and analyze the critical errors and key data points to
    monitor the health of Multi-Site operation. The dashboardData map uses id as key and data as value as listed below
    - recipeId      A unique identifier used for collating the input and output Multisite dashboard data
    - data    The dashboard data is stored in JSON format and will be used for displaying stack charts, bar chart, line
    charts and tables in dashboard interface.
    
    
    :var serviceData:  The standard ServiceData return.
    """
    dashboardData: StrStrMap = None
    serviceData: ServiceData = None


@dataclass
class ReportRecipe(TcBaseObj):
    """
    Structure containing detailed input information for the generation of Multi-Site dashbaord reports.
    
    :var recipeId: A unique identifier used for collating the input and output Multisite dashboard data.
    :var reportType: Name of different types of reports that need to be generated on server side. The supported report
    types are:
    
    - ItemErrorsBySite &ndash; Report the errors occurred during Multi-Site import, export and synchronization
    operations categorized by Teamcenter site name.
    - ItemErrorsByErrorType &ndash; Report the errors occurred during Multi-Site import, export and synchronization
    operations on each site categorized by error type.
    - ItemInconsistentOwnership- Report the items across all Teamcenter sites in Multi-Site federation which has
    varying ownership.
    
    
    :var filters: A map (string, list of strings) of report recipe filter names and values used for the generation of
    desired report type. the supported report recipe filter names and values are:
    
    - siteNames:-  List of names of Teamcenter sites on which the report needs to be generated on server side.
    - dateRange:-    List of dates in the date range for which the historic data is gathered. The dates are specified
    in MM-DD-YYYY format.
    
    """
    recipeId: str = ''
    reportType: str = ''
    filters: StrVecMap = None


"""
Map of string array property names to value.
"""
StrStrMap = Dict[str, str]


"""
Map of string array property names to values.
"""
StrVecMap = Dict[str, List[str]]
