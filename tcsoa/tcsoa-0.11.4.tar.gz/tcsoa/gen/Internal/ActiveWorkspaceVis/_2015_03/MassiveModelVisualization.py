from __future__ import annotations

from tcsoa.gen.BusinessObjects import BusinessObject, ImanFile, VariantRule
from typing import Dict, List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass
from datetime import datetime


@dataclass
class EffectivityInfo(TcBaseObj):
    """
    This structure contains  information about the effectivity configuration.
    Note: If effectivityUnitNo is not to be considered then -1 has to be passed as the default value. Value  0 is
    considered as  a valid effectivity unit number.
    
    :var effectivityUnitNo: Effective unit number.
    :var effectivityDate: Effective date configuration information.
    :var endItem: Effective end item.
    """
    effectivityUnitNo: int = 0
    effectivityDate: datetime = None
    endItem: BusinessObject = None


@dataclass
class GetIndexedProductsResponse(TcBaseObj):
    """
    This structure contains the list of product and configuration for which the product structure information is
    indexed.
    
    :var indexedProductAndConfigInfos: A list of product and configuration for which the product structure information
    are indexed.
    :var serviceData: ServiceData in which the partial errors are communicated to the client.
    """
    indexedProductAndConfigInfos: List[IndexedProductOutput] = ()
    serviceData: ServiceData = None


@dataclass
class OccsGroupedByProperty(TcBaseObj):
    """
    A structure that contains a list of PFUIDs, grouped by the property names and values.
    
    :var internalPropertyName: The internal name of the property.
    :var groupedPfuidsMap: A map (string, list of strings) containing a list of 'propertyGroupID' for each PFUID. For
    multi-valued properties, a single PFUID may be associated with multiple 'propertyGroupIDs'.
    :var unmatchedPfuidList: List of unmatched pfuids.
    """
    internalPropertyName: str = ''
    groupedPfuidsMap: PfuidToPropertyGroupIdMap = None
    unmatchedPfuidList: List[str] = ()


@dataclass
class OccsGroupedByPropertyResponse(TcBaseObj):
    """
    A structure that contains a list of PFUIDs, grouped by the property names and values.
    
    :var groupedOccList: List of 'OccGroupedByProperty' information.
    :var serviceData: The service data through which errors are communicated to the client.
    """
    groupedOccList: List[OccsGroupedByProperty] = ()
    serviceData: ServiceData = None


@dataclass
class ProductAndConfigInfo(TcBaseObj):
    """
    This structure contains product and the associated configuration for which the product structure information is
    indexed.
    
    :var product: The product which is indexed. It could be an ItemRevision.
    :var revisionRule: The RevisionRule configuration applied on the product structure.
    :var effectivityInfos: A list of effectivity information for which the product structure was configured.
    :var variantRuleInfos: A list of VariantRule applied on the product structure.
    """
    product: BusinessObject = None
    revisionRule: BusinessObject = None
    effectivityInfos: List[EffectivityInfo] = ()
    variantRuleInfos: List[VariantRuleInfo] = ()


@dataclass
class ProductAndConfigInfoInput(TcBaseObj):
    """
    This structure contains product and the associated configuration for which the product structure information file
    has to be retrieved. In case the client always needs a full structure then the deltaIdentifier can be passed as
    empty in which case the complete structure file along with any delta product structure files will be returned.
    The product information for which the product structure information has to be retrieved can be provided using the
    recipeObject or the productConfigInfo.recipeObject if provided would take precedence over productConfigInfo.
    
    
    :var clientId: A clientId passed by the client in order to map the input to the corresponding output in the
    response.
    :var deltaIdentifier: Delta identifier to identify mark point from which the next set of delta need to be retrieved.
    :var recipeObject: The BusinessObject that contains the information about the product and the configuration. For
    example it could be Awb0ProductContextInfo or VisStructureContext.
    :var productConfigInfo: The product and the configuration information for which the product structure is being
    retrieved.
    """
    clientId: str = ''
    deltaIdentifier: str = ''
    recipeObject: BusinessObject = None
    productConfigInfo: ProductAndConfigInfo = None


@dataclass
class ProductStructureFileInfo(TcBaseObj):
    """
    This structure contains the read ticket to a file containing the complete product structure information at some
    point in time and a set of read tickets to files containing the delta product structure information. The order of
    deltaStructureFileReadTickets is the order in which the delta files has to be merged with the complete file to make
    the product structure information current.
    
    :var clientId: A clientId passed by the client in order to map the input to the corresponding output in the
    response.
    :var fullStructureFileReadTicket: Read ticket to file that contains the full product structure at some point in
    time.
    :var deltaStructureFileReadTickets: Read tickets to file containing delta product structure information since the
    complete product structure file was generated.
    :var nextDeltaIdentifierToken: A delta token that need to be used for identifying  the next set of delta product
    structure file since this request.
    """
    clientId: str = ''
    fullStructureFileReadTicket: str = ''
    deltaStructureFileReadTickets: List[str] = ()
    nextDeltaIdentifierToken: str = ''


@dataclass
class ProductStructureIdInfo(TcBaseObj):
    """
    This structure contains the id of the product structure and the configuration information that need to be applied
    to the product structure.
    
    :var clientId: A clientId passed by the client in order to map the input to the corresponding output in the
    response.
    :var productStrutureIdentifier: The identifier to identify the product structure information. This identifier
    corresponds to the product id in the product structure(mmp file).
    :var productAndConfig: The configuration that need to be applied on the  product structure.
    """
    clientId: str = ''
    productStrutureIdentifier: str = ''
    productAndConfig: ProductAndConfigInfo = None


@dataclass
class ProductStructureIdInput(TcBaseObj):
    """
    This structure contains product and the associated configuration for which the product structure information id is
    to be determined. The configuration information can either be passed in a detailed format or as recipe object.
    
    :var clientId: A clientId passed by the client in order to map the input to the corresponding output in the
    response.
    :var recipeObject: The object that contains the configuration recipe. It could be something like
    Awb0ProductContextInfo or VisStructureContext.
    :var productAndConfig: The product and configuration information for which the structure id has to be determined.
    """
    clientId: str = ''
    recipeObject: BusinessObject = None
    productAndConfig: ProductAndConfigInfo = None


@dataclass
class PropertyGroupingValue(TcBaseObj):
    """
    A structure containing start and end values for a specific property. The end value is used for range comparisons if
    populated.
    
    :var propertyGroupID: Unique Identifier used by client to identify the group. The id will allow to associate the
    input to the output. This allows multiple types or ranges share the same color.
    
    :var startValue: String representation of the value for the property. For ranges, this is the start value for the
    range. If the client code is dealing with specific value types (int, double, etc.) the client code can use the
    appropriate client APIs to convert values to a string representation e.g Property::toFloatString,
    Property::toIntString, Property::toDateString, etc. On the server side, they can be converted back to the
    appropriate value types using the corresponding APIs e.g Property::parseFloat, Property::parseInt,
    Property::parseDate, etc.
    :var endValue: String representation of the end value for the property. This is optional and is populated only for
    ranges. It represents the end value of the range. See the startValue description for how the client  and server
    code can convert from and to the specific value types.
    """
    propertyGroupID: str = ''
    startValue: str = ''
    endValue: str = ''


@dataclass
class GetProductStructureIdResponse(TcBaseObj):
    """
    This structure contains the information about the product structure information identifier which can be used to
    determine the product structure information from the catalogue of product structure information maintained at the
    client. The configuration that need to be applied on that product structure information is also returned via this
    response.
    
    :var psIdInfos: A list of product and configuration for which the product structure information are indexed. 
    :var serviceData: ServiceData by which the partial errors are communicated to the client.
    """
    psIdInfos: List[ProductStructureIdInfo] = ()
    serviceData: ServiceData = None


@dataclass
class UpdateCollectionInput(TcBaseObj):
    """
    This structure contains  information about the file that need to be associated to the Awv0MMPDeltaCollection
    identified by the deltaCollectionIdentifier.
    
    :var deltaCollectionIdentifier: The string used to uniquely identify the Awv0MMPDeltaCollection instance. This is
    an uid of of Awb0BOMIndexAdminData instance in cases of Active Content Experience(ACE). In other non ACE usecases
    this is the string by which the Awb0ProductStructureProvider identifies the Awv0MMPDeltaCollection instance. 
    :var productStructureFile: The file that need to be associated to the Awv0MMPDeltaCollection dataset.
    :var isFull: If true, the file being supplied represents the complete product structure information. If false the
    file being supplied represents the delta product structure information.
    """
    deltaCollectionIdentifier: str = ''
    productStructureFile: ImanFile = None
    isFull: bool = False


@dataclass
class VariantRuleInfo(TcBaseObj):
    """
    This structure contains VariantRule object that was applied for configuration and the object to which the
    VariantRule is associated through GRM relation.
    
    :var variantRule: The VariantRule  applied for configuration.
    :var variantRuleOwningObject: The object to which the VariantRule is associated via ImanRelation.
    """
    variantRule: VariantRule = None
    variantRuleOwningObject: BusinessObject = None


@dataclass
class GetStructureFilesResponse(TcBaseObj):
    """
    This structure contains the information about the files containing product structure information that make up a
    complete product structure.
    
    :var productStructureFileInfos: A list of ProductStructureFileInfo containing the read ticket to the complete and
    or delta product structure files.
    :var serviceData: ServiceData by which the partial errors are communicated to the client.
    """
    productStructureFileInfos: List[ProductStructureFileInfo] = ()
    serviceData: ServiceData = None


@dataclass
class GroupOccsByPropertyInput(TcBaseObj):
    """
    A structure containing an internal property name, a list of 'PFUIDs 'that are to be grouped based upon
    'PropertyGroupingValue'.
    
    :var internalPropertyName: The internal name of the property based on whose values the occurrences are to be
    grouped.
    :var pfuidList: List of pfuid by which the product structure line can be identified in ACE Index Bom.
    :var propertyValues: List of 'PropertyGroupingValue' information corresponding to the property.
    """
    internalPropertyName: str = ''
    pfuidList: List[str] = ()
    propertyValues: List[PropertyGroupingValue] = ()


@dataclass
class IndexedProductOutput(TcBaseObj):
    """
    This structure contains the product, associated configuration information along with an identifier that is used to
    indentify this product and configuration in a catalogue of structure files.
    
    :var productConfigInfo: The product and the configuration information.
    :var productStructureIdentifier: An identifier to identify this product and configuration. The structure files for
    this product and configuration can be identified by this identifier.
    """
    productConfigInfo: ProductAndConfigInfo = None
    productStructureIdentifier: str = ''


"""
A map containing a list of 'propertyGroupID' for each PFUID. For multi-valued properties, a single PFUID may be associated with multiple 'propertyGroupIDs'. The id will allow to associate the input to the output. This allows multiple types or ranges share the same color.

"""
PfuidToPropertyGroupIdMap = Dict[str, List[str]]
