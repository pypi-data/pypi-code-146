from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, VariantRule
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetProductStructureIdResponse(TcBaseObj):
    """
    This structure contains the information about the structure ID used to determine the product structure information
    from the catalogue of product structure information maintained in the VDS. The configuration that need to be
    applied on that product structure to configure it is also returned via this response.
    
    :var psIdInfos: A list of ProductStructureIdInfo containing the id of  product structure information and the
    configuration that need to be applied.
    :var serviceData: ServiceData by which the partial errors are communicated to the client.
    """
    psIdInfos: List[ProductStructureIdInfo] = ()
    serviceData: ServiceData = None


@dataclass
class ProductAndConfigInfo(TcBaseObj):
    """
    This structure contains product and the associated configuration for which the product structure information id is
    to be determined. The configuration information can either be passed in a detailed format or as recipe object.
    
    :var product: The product which is indexed. IThe supported object types can either be a  BOMViewRevision or
    Cpd0CollaborativeDesign.
    :var revisionRule: The RevisionRule configuration applied on the product structure.
    :var effectivityInfos: A list of effectivity information for which the product structure was configured.
    :var variantInfos: A list of VariantRule objects applied on the product structure.
    """
    product: BusinessObject = None
    revisionRule: BusinessObject = None
    effectivityInfos: List[EffectivityInfo] = ()
    variantInfos: List[VariantRuleInfo] = ()


@dataclass
class ProductStructureIdInfo(TcBaseObj):
    """
    This structure contains the id of the product structure and the configuration information that need to be applied
    to the product structure.
    
    :var clientId: A clientId passed by the client in order to map the input to the corresponding output in the
    response.
    :var productStrutureIdentifier: The structure ID  for the indexed product structure data. This identifier
    corresponds to the product id indexed in the VDS (and passed in the .mmp file).
    :var productAndConfig: The configuration that needs to be applied on the  product structure.
    :var revRuleInfo: The list of RevRuleInfo containing revision rule information to be used for solver library inside
    VDS.
    """
    clientId: str = ''
    productStrutureIdentifier: str = ''
    productAndConfig: ProductAndConfigInfo = None
    revRuleInfo: List[RevRuleInfo] = ()


@dataclass
class ProductStructureIdInput(TcBaseObj):
    """
    This structure contains product and the associated configuration for which the product structure information id is
    to be determined. The configuration information can either be passed in a detailed format or as recipe object.
    
    :var clientId: A clientId passed by the client in order to map the input to the corresponding output in the
    response.
    :var recipeObject: The object that contains the configuration recipe. The supported types are
    Awb0ProductContextInfo or a VisStructureContext object.
    :var productAndConfig: The product and configuration information for which the structure id has to be determined.
    """
    clientId: str = ''
    recipeObject: BusinessObject = None
    productAndConfig: ProductAndConfigInfo = None


@dataclass
class RevRuleInfo(TcBaseObj):
    """
    This structure contains revision rule entry names, effectivity expression, variant expression and revision rule
    date.
    
    :var revRuleEntryNames: A list of revision rule entry names. The revision rule entry clause names will be used by
    VDS for configuration solve.
    :var effectivityExpr: Effectivity boolean expression string. For eg. "Unit  >= 1 &amp;&amp; Unit < 100". This
    expression will be used by VDS for effectivity solve and is an internal syntax. The client does not parse the
    string. It should instead pass this to VDS to filer the node using this effectivity expression..
    :var variantExpr: Variant  boolean expression string. For eg. "Color = Red &amp;&amp;  Fuel=Petrol". This
    expression will be used by VDS for variant solve  and is an internal syntax. The client does not parse the string.
    It should instead pass this to VDS to filer the node using this variant expression.
    :var revRuleDate: Revision rule Date.
    :var context: String value which differentiates whether it&rsquo;s client or partition revision rule. Valid values
    are: "ClientRevRule" or "PartitionRevRule".
    """
    revRuleEntryNames: List[str] = ()
    effectivityExpr: str = ''
    variantExpr: str = ''
    revRuleDate: datetime = None
    context: str = ''


@dataclass
class VariantRuleInfo(TcBaseObj):
    """
    This structure contains  VariantRule objects that were applied for configuration and the object to which the
    VariantRule is associated through GRM relation.
    
    :var variantRule: VariantRule object applied for configuration.
    :var variantRuleOwningObject: The object to which the VariantRule is associated through ImanRelation . The
    variantRuleOwningObject is the object chosen when the user is selecting a configuration that needs to be applied.
    The user could use any relation filter while specifying it but it is typically specification, reference or
    manifestation relation.
    """
    variantRule: VariantRule = None
    variantRuleOwningObject: BusinessObject = None


@dataclass
class EffectivityInfo(TcBaseObj):
    """
    This structure contains  information about the effectivity configuration.
    
    :var effectivityUnitNo: Effective unit number. Use value of  -1 if unit effectivity is not to be considered for
    configuration.
    :var effectivityDate: Effective date configuration information.
    :var endItem: Effective  end item. Supported object types are:  ItemRevision
    """
    effectivityUnitNo: int = 0
    effectivityDate: datetime = None
    endItem: BusinessObject = None
