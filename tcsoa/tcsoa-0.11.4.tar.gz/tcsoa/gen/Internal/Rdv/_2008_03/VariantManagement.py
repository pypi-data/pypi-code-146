from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetValidoverlayBomlineResponse(TcBaseObj):
    """
    The 'GetValidoverlayBomlineResponse' structure contains the configured and unconfigured BOMLine objects after the
    VOO operation and the 'ServiceData'.
    
    :var validoverlayBomlines: vector of 'ConfigbomlinesInfoForValidoverlay' objects
    :var serviceData: An object of 'ServiceData' which contains any PartialErrors if occurred during execution of the
    VOO or effectivity date filtering
    """
    validoverlayBomlines: List[ConfigbomlinesInfoForValidoverlay] = ()
    serviceData: ServiceData = None


@dataclass
class BomlinesInfoForValidoverlay(TcBaseObj):
    """
    The 'BomlinesInfoForValidoverlay' data structure contains background BOMLine objects on which VOO needs to be
    applied along with other parameters to configure the VOO operation
    
    :var showUnconfiguredVariant: Flag to specify whether unconfigured BOMLine objects need to be displayed
    :var showUnconfiguredBydate: Flag to specify whether the effectivity date based filtering needs to be applied. true
    value means it should be skipped.
    :var variantRuleTag: List of VariantRule tag, for each variant rule
    :var backgrndBomlines: List of background BOMLine objects for which VOO needs to be applied.
    """
    showUnconfiguredVariant: bool = False
    showUnconfiguredBydate: bool = False
    variantRuleTag: List[BusinessObject] = ()
    backgrndBomlines: List[BusinessObject] = ()


@dataclass
class ConfigbomlinesInfoForValidoverlay(TcBaseObj):
    """
    The 'ConfigbomlinesInfoForValidoverlay' structure contains lists of configured and unconfigured BOMLine objects,
    after the VOO filtering operation is completed.
    
    :var backgrndBomlines: List of configured BOMLine objects
    :var unconfiguredBomlines: List of unconfigured BOMLine objects post the filtering
    """
    backgrndBomlines: List[BusinessObject] = ()
    unconfiguredBomlines: List[BusinessObject] = ()
