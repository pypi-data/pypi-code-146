from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetActivitiesComparisonDetailsResponse(TcBaseObj):
    """
    Return the list of activities detail elements and service data for partial errors.
    
    :var details: for each input equivalent set holds the details of activities
    :var serviceData: to capture partial errors
    """
    details: List[ActivitiesDetails] = ()
    serviceData: ServiceData = None


@dataclass
class PartialMatchCriteria2(TcBaseObj):
    """
    a structure to capture generic Partial Match criteria
    
    :var intMap: map of string to vector or integers.
    :var dblMap: map of string to vector of doubles.
    :var strMap: map of string to vector of strings.
    :var objMap: map of string to vector of objects.
    :var dateMap: map of string to vector of dates
    """
    intMap: StringToIntVectorMap2 = None
    dblMap: StringToDblVectorMap2 = None
    strMap: StringToStrVectorMap2 = None
    objMap: StringToObjVectorMap2 = None
    dateMap: StringToDateVectorMap2 = None


@dataclass
class ToolRequirementComparisonData(TcBaseObj):
    """
    Specifies a data of the tool requirements.
    The fieldName specifies the data it represents such as TR description, Classification search class etc. 
    The Values specifies the data of source and target tool requirement combined. The first few data of Values
    corresponds to the source tool requirement followed by the target tool requirement. The vector size of Values is
    equal to the summation of vector size of source and target tool requirements input vector.
    The flag represents whether the data are different.
    
    :var fieldName: Specifies the field of tool requirement such as NAME, DESCRIPTION, SEARCHCLASS and SEARCHATTRIBUTE.
    NAME represents the name of the tool requirement.
     DESCRIPTION represents the tool requirement description.
     SEARCHCLASS represents the search class of the tool requirement.
    SEARCHATTRIBUTE represents one of the search attribute of classification search.
    :var values: Specifies the data of source and target tool requirement for the given field. The first few elements
    correspond to the source tool requirement followed by target tool requirement.
    :var isDifferent: For a field, specifies the flag indicating whether the data of source and target tool requirement
    is same. For multiple source and target tool requirement, if any two data are different then the flag is set to
    true.
    """
    fieldName: str = ''
    values: List[str] = ()
    isDifferent: bool = False


@dataclass
class ToolRequirementComparisonResult(TcBaseObj):
    """
    Specifies the comparison result of source and target tool requirements.
    
    :var comparisonData: Specifies the comparison data of all the fields of tool requirement. 
    The first element of the vector specifies the name of the tool requirement and will have NAME as fieldName.
    The second element of the vector specifies the description of tool requirement and will have DESCRIPTION as
    fieldName.
    If the search criteria is defined, the third element of the vector specifies the search class of tool requirement
    and will have SEARCHCLASS fieldName.
    If the search criteria is defined then the subsequent elements specifies the search attributes of the tool
    requirement. The elements will have SEARCHaTTRIBUTE as fieldName. The vector may have multiple elements with this
    fieldName.
    :var serviceData: Service data will hold warnings and errors, if any.
    """
    comparisonData: List[ToolRequirementComparisonData] = ()
    serviceData: ServiceData = None


@dataclass
class ActivitiesDetails(TcBaseObj):
    """
    details of activities for one equivalent set
    
    :var index: position in the input equivalentObjects vector
    :var details: details of all the activity tree for each operation in the equivalentLines vector
    :var equivalentLines: all sources of equivalent set in sequence and then all targets in sequence
    """
    index: int = 0
    details: ActivityDetailsElement = None
    equivalentLines: List[BusinessObject] = ()


@dataclass
class ActivityDetailsElement(TcBaseObj):
    """
    recursive structure that represents one row in the activities tree (one activity across all the input lines)
    
    :var isDifferent: result of comparison of this activity
    :var children: size of the vector will match the number of children that this activity has
    :var activities: size of the vector will match the size of equivalentLines vector
    """
    isDifferent: bool = False
    children: List[ActivityDetailsElement] = ()
    activities: List[BusinessObject] = ()


@dataclass
class EquivalentLines2(TcBaseObj):
    """
    Lines from a Source Window and a Target Window that are equivalent. For example - having the same ID in Context or
    other criteria.
    
    :var eqvSrcLines: set of source bomlines that are equivalent based on some criteria like ID in context.
    :var eqvTargetLines: set of target bomlines (not the same window as source lines) that are equivalent in a manner
    consistent with the source lines
    """
    eqvSrcLines: List[BusinessObject] = ()
    eqvTargetLines: List[BusinessObject] = ()


"""
a map of string to vector of dates
"""
StringToDateVectorMap2 = Dict[str, List[datetime]]


"""
String to vector of doubles map.
"""
StringToDblVectorMap2 = Dict[str, List[float]]


"""
map of string to vector of integers.
"""
StringToIntVectorMap2 = Dict[str, List[int]]


"""
a map of string to vector of objects.
"""
StringToObjVectorMap2 = Dict[str, List[BusinessObject]]


"""
a map of String to vector of strings.
"""
StringToStrVectorMap2 = Dict[str, List[str]]
