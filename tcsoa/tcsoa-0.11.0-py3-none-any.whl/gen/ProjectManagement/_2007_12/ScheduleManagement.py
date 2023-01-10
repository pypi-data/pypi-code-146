from __future__ import annotations

from typing import List
from tcsoa.gen.BusinessObjects import Schedule
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ItemDemand(TcBaseObj):
    """
    This represents the output structure to store the labor demand per resource.
    
    :var resourceId: Represents the resource id of an individual labor or resource.
    :var costs: Represents the per period cost of an individual resource.
    """
    resourceId: str = ''
    costs: List[PeriodCost] = ()


@dataclass
class PeriodCost(TcBaseObj):
    """
    This represents the output structure to store the cost vasule per period.
    
    :var periodNum: Represents the period number.
    :var cost: Represents the cost calculated per each period.
    """
    periodNum: int = 0
    cost: str = ''


@dataclass
class DemandProfileRequest(TcBaseObj):
    """
    This represents the input structure for calculating DemandProfile data for each schedule.
    
    :var schedule: Input schedule of which DemandProfile data will be calculated.
    :var startPeriod: Start of schedule Period to calculate data (MM-YYYY).
    :var endPeriod: End of schedule Period to calculate data (MM-YYYY).
    :var monthsInPeriod: Number of months in the period.
    :var currency: Currency to calculate the cost (ISO 4217). (Not currently used)
    """
    schedule: Schedule = None
    startPeriod: str = ''
    endPeriod: str = ''
    monthsInPeriod: int = 0
    currency: str = ''


@dataclass
class DemandProfileResponse(TcBaseObj):
    """
    This represents the output structure for calculated DemandProfile data for each shecule.
    
    :var schedule: Schedule loaded for DemandProfile data.
    :var activeBaseline: The active baseline of the schedule.
    :var laborDemand: Labor demand calculated for the schedule.
    :var capitalDemand: Capital Demand calculated for the schedule.
    :var expenseDemand: Expense Demand calculated for the schedule.
    :var currency: Currency used in the calculations (not currently used).
    """
    schedule: Schedule = None
    activeBaseline: Schedule = None
    laborDemand: List[ItemDemand] = ()
    capitalDemand: List[ItemDemand] = ()
    expenseDemand: List[ItemDemand] = ()
    currency: str = ''


@dataclass
class DemandProfileResponses(TcBaseObj):
    """
    This represents the DemandProfileResponses for a schedule.
    
    :var response: The Demand Profile Information of one schedule.
    :var data: The ServiceData.
    """
    response: List[DemandProfileResponse] = ()
    data: ServiceData = None
