from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.gen.Core._2014_10.DataManagement import DeepCopyData
from typing import Dict, List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class ReviseIn(TcBaseObj):
    """
    This structure holds information about the target business object, property names and values and list of deep copy
    data that will be used for the Revise operation input.
    
    :var targetObject: The target business object being revised
    :var inputPropValues: A map (string/ list of strings) that holds input property values. Each value is a list of
    strings to support both single valued and multi valued properties of types. The calling client is responsible for
    converting the different property types (like integer, double, date, etc.) to a string using the appropriate to<
    type >String function (e.g. toIntString and toDateString) in the client framework's Property class.
    :var deepCopyDatas: A list of DeepCopyData objects attached to the target object.
    """
    targetObject: BusinessObject = None
    inputPropValues: PropertyValuesMap3 = None
    deepCopyDatas: List[DeepCopyData] = ()


@dataclass
class SaveAsIn(TcBaseObj):
    """
    This structure holds information about the target business object, property names and values and list of deep copy
    data that will be used for the SaveAs operation.
    
    :var targetObject: The target business object.
    :var inputPropValues: A map (string / list of strings) that holds input property values. Each value is a list of
    strings to support both single valued and multi valued properties of types. The calling client is responsible for
    converting the different property types (like integer, double, date, etc.) to a string using the appropriate to<
    type >String function (e.g. toIntString and toDateString) in the client framework's Property class.
    :var deepCopyDatas: DeepCopyData of the objects attached to the target object.
    """
    targetObject: BusinessObject = None
    inputPropValues: PropertyValuesMap3 = None
    deepCopyDatas: List[DeepCopyData] = ()


"""
This map is of property name (as key) and property values (as value) in string format. Each value is a list of strings to support both single valued and multi valued properties of types. It is used in SaveAsIn structure to hold the property name and values&rsquo; details of the target object. The calling client is responsible for converting the different property types (like integer, double, date, etc) to a string using the appropriate to< type >String function (e.g. toIntString and toDateString) in the client framework's Property class.
"""
PropertyValuesMap3 = Dict[str, List[str]]
