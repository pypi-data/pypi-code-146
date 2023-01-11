from __future__ import annotations

from typing import List
from tcsoa.gen.Internal.ActiveWorkspaceVis._2015_03.MassiveModelVisualization import ProductAndConfigInfo
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ProductStructureIdInfo2(TcBaseObj):
    """
    This structure contains the id of the product structure and the configuration information that need to be applied
    to the product structure.
    
    :var clientId: A clientId passed by the client in order to map the input to the corresponding output in the
    response.
    :var productStrutureIdentifier: The identifier to identify the product structure information. This identifier
    corresponds to the product id in the product structure(mmp file).
    :var productAndConfig: The configuration that need to be applied on the product structure.
    :var clientRevRuleInfo: The client revision rule information to be used for solver library inside VDS.
    :var partitionRevRuleInfo: The Partition revision rule information to be used for solver library inside VDS.
    """
    clientId: str = ''
    productStrutureIdentifier: str = ''
    productAndConfig: ProductAndConfigInfo = None
    clientRevRuleInfo: RevRuleInfo = None
    partitionRevRuleInfo: RevRuleInfo = None


@dataclass
class RevRuleInfo(TcBaseObj):
    """
    This structure contains names of revision rule entry names, effectivity expression, variant expression and revision
    rule date.
    
    :var revRuleEntryNames: A list of revision rule entry names.
    :var effectivityExpr: Effectivity expression string.
    :var variantExpr: Variant expression string.
    :var revRuleDate: Revision rule Date.
    """
    revRuleEntryNames: List[str] = ()
    effectivityExpr: str = ''
    variantExpr: str = ''
    revRuleDate: datetime = None


@dataclass
class GetProductStructureIdResponse2(TcBaseObj):
    """
    This structure contains the information about the product structure information identifier which can be used to
    determine the product structure information from the catalogue of product structure information maintained at the
    client. The configuration that need to be applied on that product structure information is also returned via this
    response.
    
    :var psIdInfos: A list of product and configuration for which the product structure information are indexed.
    :var serviceData: ServiceData by which the partial errors are communicated to the client.
    """
    psIdInfos: List[ProductStructureIdInfo2] = ()
    serviceData: ServiceData = None
