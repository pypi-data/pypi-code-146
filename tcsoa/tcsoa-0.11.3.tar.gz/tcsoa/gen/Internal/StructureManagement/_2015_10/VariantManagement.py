from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject
from typing import List
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class VariantConfigurationCriteria(TcBaseObj):
    """
    Formula or VariantRule that needs to be applied on the window.
    
    :var variantConfiguratorFormula: variant criteria derived from variant formula or from variant rule created using
    Product Configurator application or from user selections in Variant Configuration View, that needs to be applied on
    the window.
    :var savedVariantRules: List of saved variant rules created via Product Configurator application that needs to be
    applied on the window. In case of multiple saved variant rule,  they are ORed and then applied to the window. Only
    the VariantRule expressions are considered for configuration.
    """
    variantConfiguratorFormula: str = ''
    savedVariantRules: List[BusinessObject] = ()
