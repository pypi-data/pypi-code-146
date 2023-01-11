from __future__ import annotations

from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from typing import Dict


@dataclass
class GetCurrentCountryPageInfoResponse(TcBaseObj):
    """
    The information used to populate the current country selection page.
    
    :var displayCountries: Map of key/value pairs (string, string) representing the selectable countries the user may
    choose when filling out the current country selection page.
    - Key is the ISO 3166-1 alpha-2 two letter country codes.
    - Value is the full country name.
    
    
    Examples: US &ndash; United States of America, GB &ndash; United Kingdom, and IN &ndash; India.
    :var extraInfoOut: Map of key/value pairs (string, string).
    - Key: initialCountry. The initial value displayed in the current country pick list. The format is ISO 3166-1
    alpha-2 two letter country. This is optional. The value may be the empty string.  
    - Key: confidentialityStatement. The agreement that the user must read when filling out the current country page.
    
    
    :var serviceData: ServiceData.
    """
    displayCountries: ExtraMappedInfo = None
    extraInfoOut: ExtraMappedInfo = None
    serviceData: ServiceData = None


"""
Map of information used to populate the current country page.
"""
ExtraMappedInfo = Dict[str, str]
