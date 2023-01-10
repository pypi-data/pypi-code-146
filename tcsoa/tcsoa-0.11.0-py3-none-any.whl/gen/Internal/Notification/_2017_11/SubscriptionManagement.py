from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetSubscribablePropertiesResponse(TcBaseObj):
    """
    The response will include a set of subscribable properties for a set of input object types. Partial errors will be
    returned and wrapped in serviceData, if any are specified.
    
    :var criteriaProperties: A list of properties for each input object type
    :var serviceData: Service data with the partial error information
    """
    criteriaProperties: List[CriteriaPropertyStructure] = ()
    serviceData: ServiceData = None


@dataclass
class CriteriaPropertyStructure(TcBaseObj):
    """
    Contains object type and a list of subscribable properties internal names and display name pairs sorted by display
    names.
    
    :var subscribableObjectType: Subscribable object type for which the list of properties are configured.
    :var propInternalNames: List of property internal names of subscribable object types sorted by property&rsquo;s
    display names
    :var propDisplayNames: Sorted list of property display names of subscribable object type
    """
    subscribableObjectType: BusinessObject = None
    propInternalNames: List[str] = ()
    propDisplayNames: List[str] = ()
