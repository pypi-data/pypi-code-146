from __future__ import annotations

from tcsoa.gen.BusinessObjects import BOMLine, BOMWindow, BusinessObject, RevisionRule
from typing import List
from tcsoa.gen.Internal.Rdv._2009_01.VariantManagement import MetaExprTokens
from tcsoa.gen.Internal.Rdv._2009_05.VariantManagement import SearchResponse, SearchResults, NVEMetaExprTokensResponse
from tcsoa.base import TcService


class VariantManagementService(TcService):

    @classmethod
    def realignNVEMetaExpressionTokens(cls, metaExprs: List[MetaExprTokens]) -> NVEMetaExprTokensResponse:
        """
        This operation realigns the 'MetaExprTokens'. Meta expressions are used to balance the tree structure amongst
        the variant expressions and validate the input combination of Named Variant Expressions (NVEs). It creates the
        NVEMetaExpression object from 'MetaExprTokens' object and realigns it. The operation returns this realigned
        'MetaExprTokens' list along with 'ServiceData' object.
        
        
        Use cases:
        This operation can be used to realign the Named Variant Expression tokens to make sure that they do not equate
        to always false condition. Input parameter takes the list of MetaExprTokens those needs to be realigned.
        """
        return cls.execute_soa_method(
            method_name='realignNVEMetaExpressionTokens',
            library='Internal-Rdv',
            service_date='2009_05',
            service_name='VariantManagement',
            params={'metaExprs': metaExprs},
            response_cls=NVEMetaExprTokensResponse,
        )

    @classmethod
    def executeAdhocSearchWithOverlays(cls, datasetTag: BusinessObject, productRevTag: BusinessObject, bookMarkStringsToMatch: List[str], bomWindow: BOMWindow, targetBOMLine: List[BOMLine], vooFlag: bool, svrTag: BusinessObject) -> SearchResponse:
        """
        This method performs an Adhoc Search and Valid Overlays Only analysis on the search results, using the
        following input parameters:
        - datasetTag
        - productRevTag
        - bookMarkStringsToMatch
        - bomWindow
        - targetBOMLine
        - vooFlag
        - svrTag
        
        
        
        The datasetTag is a DirectModelAssembly dataset which contains the unconfigured structure information,
        generated using the BOMWriter. The unconfigured plmxml file, attached with the dataset, is parsed and processed
        to create a pruned plmxml file, containing the search result. This file can be opened in TcVis, in order to
        view the results. The method also performs Valid Overlays Only filtering, based on the target BOMLine objects
        and the Saved VariantRule object which are used to the effective variant condition is calculated, to perform
        the VOO filtering.
        This method is currently used by the Teamcenter Rich Client Adhoc DC application, to perform Adhoc Search and
        VOO filtering.
        
        Use cases:
        Use case1: Executing Adhoc Search along with Valid Overlays Only filter
        If the user wishes to execute Adhoc Search and filter the search results using valid overlays filter, then this
        operation is invoked. It uses the effective variant condition on the target BOMLine objects along with the
        Saved VariantRule to apply the filter.
        """
        return cls.execute_soa_method(
            method_name='executeAdhocSearchWithOverlays',
            library='Internal-Rdv',
            service_date='2009_05',
            service_name='VariantManagement',
            params={'datasetTag': datasetTag, 'productRevTag': productRevTag, 'bookMarkStringsToMatch': bookMarkStringsToMatch, 'bomWindow': bomWindow, 'targetBOMLine': targetBOMLine, 'vooFlag': vooFlag, 'svrTag': svrTag},
            response_cls=SearchResponse,
        )

    @classmethod
    def executeSearchWithOverlays(cls, bookMarkStringsToMatch: List[str], bomWindow: BOMWindow, revRule: RevisionRule, targetBOMLine: List[BOMLine], vooFlag: bool) -> SearchResults:
        """
        This method categorizes the input bookmark strings into Configured BOMLine objects that match the input
        strings, Unconfigured BOMLine objects that are not configured for the current variant rule or effective date,
        Unconfigurable BOMLine objects for which no revision configured for the current revision rule and Unconfigured
        VOO BOMLine objects that got unconfigured by applying the Valid Overlay Only (VOO) filter, using the different
        input parameters provided.
        The following inputs are required:
        - bookMarkStringsToMatch
        - bomWindow
        - revRule
        - targetBOMLine
        - vooFlag
        
        
        All the input parameters are mandatory.
        
        This method is used in QPL search (NX and JT based) and Appearance based search. As valid overlays filtering is
        in built in the cacheless search, this method is not required in cacheless search engine. The bookmark strings
        expected are different for different search engines.
        
        For NX based QPL search engine, the bookmark string is a BOMLine object string, that consists of an Occurrence
        Note UG ENTITY HANDLE value for BOMLine objects all the way to the top BOMLine for a particular BOMLine object.
        Example:
        ABC12345/001 view,
        DEF12345/001 view ( UG ENTITY HANDLE contains x38 ),
             GHI12345/001 ( UG ENTITY HANDLE contains x162E ),
        The bookmark string that corresponds to the leaf node BOMLine object is the bookmark string //56/5678, and the
        BOMLine object that will be returned is GHI12345/001.
        For a JT based QPL search engine, the bookmark string is a BOMLine object string which is a concatenation of
        the occurrence UIDs on the occurrence tree path, using the string representation.
        ABC12345/001 view,
        DEF12345/001 view ( Occurrence UID = g8_YK3Jyg9jhgD ),
             GHI12345/001 ( Occurrence UID = gMyopk3ag9jhgD ),
        The BOMLine object string that corresponds to the leaf node BOMLine object is //g8_YK3Jyg9jhgD/gMyopk3ag9jhgD,
        and the BOMLine object that will be returned is GHI12345/001.
        
        For an Appearance based search engine, the bookmark string is the concatenation of the UIDs of the appearance.
        
        Use cases:
        Use case 1: Applying valid overlays only filtering on the QPL/Appearance based search results. 
        If the user wishes to filter search results using valid overlays filter, then this operation is invoked. It
        uses the effective variant condition on the target lines provided to filter out the non matching BOMLine
        objects from the search results.
        """
        return cls.execute_soa_method(
            method_name='executeSearchWithOverlays',
            library='Internal-Rdv',
            service_date='2009_05',
            service_name='VariantManagement',
            params={'bookMarkStringsToMatch': bookMarkStringsToMatch, 'bomWindow': bomWindow, 'revRule': revRule, 'targetBOMLine': targetBOMLine, 'vooFlag': vooFlag},
            response_cls=SearchResults,
        )
