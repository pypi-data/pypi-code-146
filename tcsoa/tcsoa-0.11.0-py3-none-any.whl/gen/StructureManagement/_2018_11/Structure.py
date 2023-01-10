from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, WorkspaceObject
from typing import Dict, List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateGroupInput(TcBaseObj):
    """
    The structure represents all of the data necessary to create interchangeable groups.
    
    :var objectType: Type of the Interchangeable Group to be created, Substitute Group or Alternate Group.
    :var props: A map of Interchangeable Group properties names and initial values pairs (string, string). Multi-valued
    properties are represented with a comma separated string.
    :var sourceObjs: A list of occurences (Occurrence level) or a list of Item/ItemRevision objects (Global level) that
    needs to be all replaced together as a group by an interchangeable group.
    :var interChangeableObjs: A list of interchangeable parts to be associcated as an Interchangeable Group.
    """
    objectType: str = ''
    props: PropNameValuesMap = None
    sourceObjs: List[BusinessObject] = ()
    interChangeableObjs: List[WorkspaceObject] = ()


"""
Interchangeable Group properties and values. This map is of property name (as key) and property values (as value) in string format. Each value is a list of strings to support both single valued and multi valued properties of types. The calling client is responsible for converting the different property types (like integer, double, date, etc) to a string using the appropriate to< type >String function (e.g. toIntString and toDateString) in the client framework's Property class.
"""
PropNameValuesMap = Dict[str, str]
