from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class PublishColumnConfigInfo(TcBaseObj):
    """
    'PublishColumnConfigInfo' structure represents the parameters required to publish the column configuration.
    
    :var clientId: A unique string supplied by the caller. This ID is used to identify return data elements and partial
    errors associated with this input structure.
    :var columnConfiguration: The Fnd0ColumnConfiguration object, that stores all preferences that needs to be created
    as site preferences.
    """
    clientId: str = ''
    columnConfiguration: BusinessObject = None
