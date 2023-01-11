from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BusinessObject, NamedVariantExpression, MEAppearancePathNode, BOMWindow, Item
from enum import Enum
from typing import List
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcBaseObj
from dataclasses import dataclass


@dataclass
class GetABandABEInputInfo(TcBaseObj):
    """
    The 'GetABandABEInputInfo' structure represents the full set of inputs required for the operation
    'getApnComponents'(..).
    
    :var gcid: Specifies the generic component ID of the ABE to be searched.
    :var topArchTag: Specifies the top level Architecture Breakdown object.
    :var bomWindow: Specifies the BOMWindow object of parent architecture.
    """
    gcid: str = ''
    topArchTag: Item = None
    bomWindow: BOMWindow = None


@dataclass
class GetABandABEResponse(TcBaseObj):
    """
    The 'GetABandABEResponse' structure represents the response for the operation 'getApnComponents'(..) and has the
    reference to 'CompMeapnGcidAndDesc' object containing the generic component ID, description and MEAPN of the
    component. If there is any exception during the operation it will be added to the 'ServiceData' object and returned
    as a partial error.
    
    :var compsApnAndGcid: Reference to 'CompMeapnGcidAndDesc' object containing the generic component ID, description
    and MEAPN of the component.
    :var serviceData: An object of 'ServiceData' which contains updated data model objects and/or error objects with
    error messages.
    """
    compsApnAndGcid: List[CompMeapnGcidAndDesc] = ()
    serviceData: ServiceData = None


@dataclass
class GetAbeBomlineChildComponentsResponse(TcBaseObj):
    """
    This structure contains list of 'CompMeapnAndBomLine' and 'ServiceData'.
    
    :var componentsApnAndBomLines: It contains the list of 'CompMeapnAndBomLine' objects.
    
    :var serviceData: The 'ServiceData' containing full/partial errors.
    """
    componentsApnAndBomLines: List[CompMeapnAndBomLine] = ()
    serviceData: ServiceData = None


@dataclass
class GetAbeChildComponentsInputInfo(TcBaseObj):
    """
    This structure contains reference to Architecture Breakdown, BOMWindow and parent MEAppearancePathNode whose child
    MEAppearancePathNode objects needs to be retrieved.
    
    :var topLevelItem: Reference to Architecture Breakdown item, which is the topline in Architecture Breakdown
    Structure. If this reference is not supplied then operation will fail.
    
    :var meApn: MEAPN of parent whose child MEAPNs are to be retrieved. This is a mandatory parameter.
    
    :var bomWindow: Specifies the BOMWindow object of parent architecture. If it is not supplied then operation will
    fail.
    """
    topLevelItem: Item = None
    meApn: MEAppearancePathNode = None
    bomWindow: BOMWindow = None


@dataclass
class GetAbeMeapnChildComponentsResponse(TcBaseObj):
    """
    The 'GetAbeMeapnChildComponentsResponse' structure represents the response from the operation
    'getArchbreakdownMeapnChildComponents'(..) and has the reference to 'CompMeapnGcidAndDesc' objects containing the
    generic component ID, description and MEAPN of the child components. If there is any exception during the operation
    it will be added to the 'ServiceData' object and returned as a partial error.
    
    :var componentsApnAndGcid: Reference to 'CompMeapnGcidAndDesc' object containing the generic component ID,
    description and MEAPN of the component.
    :var serviceData: An object of 'ServiceData', returned as response for retrieving information on APNs, GCUID and
    description of child components, which contains updated data model objects and/or error objects with error messages.
    """
    componentsApnAndGcid: List[CompMeapnGcidAndDesc] = ()
    serviceData: ServiceData = None


@dataclass
class MetaExprTokens(TcBaseObj):
    """
    This structure contains the list of 'NVEMetaToken'. 'NVEMetaToken' represents a Token.
    
    :var tokens: Contains the list of 'NVEMetaToken'. 'NVEMetaToken' represents a token.
    """
    tokens: List[NVEMetaToken] = ()


@dataclass
class NVEMetaExpressionResponse(TcBaseObj):
    """
    This structure contains the list of MetaExprTokens and ServiceData.
    
    :var metaExprs: Contains the list of MetaExprTokens.
    :var serviceData: The ServiceData containing list of full/partial errors.
    """
    metaExprs: List[MetaExprTokens] = ()
    serviceData: ServiceData = None


@dataclass
class NVEMetaToken(TcBaseObj):
    """
    This structure represents a token.
    
    :var tokenType: It can take following values 
    -     tokenNull
    -     tokenAnd
    -     tokenOr
    -     tokenNot
    -     tokenBra
    -     tokenKet
    -     tokenNVE
    
    
    :var nveRef: Represents a NVE.
    """
    tokenType: TokenType = None
    nveRef: NVEReference = None


@dataclass
class NVEReference(TcBaseObj):
    """
    Structure representing a NamedVariantExpression (NVE). If 'TokenType' is not 'tokenNVE' then 'nveName' and 'nve'
    would be null.
    
    :var nveType: Type of NamedVariantExpression. It can take following values:
    -     nveAuthorized
    -     nveSplitting
    -     nveMandatorySplit
    
    
    :var nveName: Name of NVE. If 'TokenType' is not 'tokenNVE' then this field will be null.
    
    :var nve: Reference to the NVE object. If 'TokenType' is not 'tokenNVE' then this field will be null.
    """
    nveType: NVEType = None
    nveName: str = ''
    nve: NamedVariantExpression = None


@dataclass
class ValidateNVEMetaExprResponse(TcBaseObj):
    """
    This structure contains the list of 'XOChartData' and 'ServiceData' objects.
    
    :var xoCharts: List of the 'XOChartData' of NamedVariantExpression.
    :var serviceData: The 'ServiceData' containing full/partial errors.
    """
    xoCharts: List[XOChartData] = ()
    serviceData: ServiceData = None


@dataclass
class XOChartData(TcBaseObj):
    """
    This structure contains the XO chart information of the NamedVariantExpressions.
    
    :var noOfRows: Number of rows in the XO chart.
    :var noOfColumns: Number of column in the XO chart.
    :var colHeaderExprStrs: Name of the column header of the Expression in XO chart. 
    Example Color=BLUE.
    
    :var tableChars: The values for each cell in the XO chart. Each column can take  value as 1 (X)  or 0 (O).
    """
    noOfRows: int = 0
    noOfColumns: int = 0
    colHeaderExprStrs: List[str] = ()
    tableChars: List[int] = ()


@dataclass
class CompMeapnAndBomLine(TcBaseObj):
    """
    This structure contains MEAppearancePathNode and BOMLine.
    
    :var childMeapn: MEAppearancePathNode of child component.
    :var bomLine: BOMLine of the child component.
    """
    childMeapn: MEAppearancePathNode = None
    bomLine: BOMLine = None


@dataclass
class CompMeapnGcidAndDesc(TcBaseObj):
    """
    This structure contains the component information like generic component ID (gcid), component description and MEAPN.
    
    :var gcid: Specifies GCUID of child component.
    :var desc: Specifies description of child component.
    :var childMeapn: Specifies MEAPN of child component.
    """
    gcid: str = ''
    desc: str = ''
    childMeapn: MEAppearancePathNode = None


@dataclass
class AddDesignToProductResponse(TcBaseObj):
    """
    The 'AddDesignToProductResponse' structure represents the response for the operation 'addDesignToProduct'(..)
    containing the new PSOccurrence, Occurrence Type and Service data. If there is any exception during addition of
    part solutions it will be added to the 'ServiceData' object and returned as a partial error.
    
    :var newOcc: A collection of the occurrences created.
    :var newOccType: A collection of types of the corresponding occurrences created.
    :var serviceData: An object of 'ServiceData' which contains updated data model objects and/or error objects with
    error messages
    """
    newOcc: List[BusinessObject] = ()
    newOccType: List[BusinessObject] = ()
    serviceData: ServiceData = None


class NVEType(Enum):
    """
    Enumeration to classify NVE.
    """
    nveAuthorized = 'nveAuthorized'
    nveSplitting = 'nveSplitting'
    nveMandatorySplit = 'nveMandatorySplit'


class TokenType(Enum):
    """
    Enumeration to classify the Token.
    """
    tokenNull = 'tokenNull'
    tokenAnd = 'tokenAnd'
    tokenOr = 'tokenOr'
    tokenNot = 'tokenNot'
    tokenBra = 'tokenBra'
    tokenKet = 'tokenKet'
    tokenNVE = 'tokenNVE'
