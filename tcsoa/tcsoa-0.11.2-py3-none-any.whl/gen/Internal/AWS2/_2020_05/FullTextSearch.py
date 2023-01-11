from __future__ import annotations

from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class GetSearchSettingsInput(TcBaseObj):
    """
    Input structure for the getSearchSettings service which is used to set the inputs for which values are needed from
    server.
    
    This input structure uses a map to provide a way for the client to request specific display values for multiple
    preference in bulk. The Key for this map is the dynamic set of preference names to request display values for. The
    Value is the specific list of internal values to translate to display values.
    
    :var inputSettings: Input map(string, list<string>) for getting the search settings. Supported keys and values are
    (this set will be expanded in future releases)
    --------------------------------------------------------------------------------------------------
    Key                                                                   |                Values
    --------------------------------------------------------------------------------------------------
    AWC_Limited_Filter_Categories_Expanded |     List of internal property names  
                                                                          |     <type_name>.<property name>] Ex: 
                                                                          |     WorkspaceObject.object_type
    --------------------------------------------------------------------------------------------------
    Default_Quick_Access_Query                       |     Internal name of the quick access query
    --------------------------------------------------------------------------------------------------
    """
    inputSettings: StringVectorMap = None


@dataclass
class GetSearchSettingsResponse(TcBaseObj):
    """
    The input key and its corrosponding output values.
    
    :var outputValues: Output values map(string, list of<string>) that contain the input key and its corresponding
    outputs.
    ---------------------------------------------------------------------------------------------------
    Key                                                                     |       Values
    ---------------------------------------------------------------------------------------------------
    AWC_Limited_Filter_Categories_Expanded   |  A List of [display names of the properties] Ex: For 
                                                                            |  WorkspaceObject.object_type as input the
    output 
                                                                            |  would be "Type"
    ---------------------------------------------------------------------------------------------------
    Default_Quick_Access_Query                         |  Display name of the quick access query
    ---------------------------------------------------------------------------------------------------
    """
    outputValues: StringVectorMap = None


"""
A map of string to list of strings.
"""
StringVectorMap = Dict[str, List[str]]
