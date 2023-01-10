from __future__ import annotations

from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class SavedQueryProperties(TcBaseObj):
    """
    Contains properties of the saved query to be created.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify returned partial errors
    associated with this input structure.
    :var queryName: Name of the saved query to be created.
    :var queryDesc: Description of the saved query to be created, may be an empty string.
    :var queryClass: The storage class name of the business object type this query will find object instances of.
    :var queryClauses: Query clauses of the saved query to be created. To make sure the query clauses is  in correct
    formate, please use Export button in Query Builder to export the saved query into a XML file, pick up the string
    value of QueryClause element in the XML, replace all " with " to get the final string, the final query clauses
    string should be the same as seen in View Properties dialog. 
    """
    clientId: str = ''
    queryName: str = ''
    queryDesc: str = ''
    queryClass: str = ''
    queryClauses: str = ''
