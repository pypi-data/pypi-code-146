from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, ImanFile
from typing import Dict, List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class CreateVisSCsFromBOMsInfo(TcBaseObj):
    """
    Input structure used for creating VisStrucutreContext objects based on the given BOMWindows and specific
    occurrences within those BOMWindows.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var occurrencesList: List of BOMLines representing the occurrences to be included in the structure recipe.
    :var staticStructureFile: IMANFile reference to the PLMXML static representation of the structure. If not supplied
    then the associated property of the VisStructureContext will not be set. [optional]
    :var createVisSCOptions: A list of options that are to be considered when creating VisStructureContext objects
    during the execution of this operation. This list of options is represented by a map of string option names to
    string option values. The values are represented as a list of strings. The size of this list is dependent on the
    particular option being defined.
    """
    clientId: str = ''
    occurrencesList: List[BOMLine] = ()
    staticStructureFile: ImanFile = None
    createVisSCOptions: StringKeyToStringVectorMap = None


"""
Map that contains option names and the corresponding option value(s).
"""
StringKeyToStringVectorMap = Dict[str, List[str]]
