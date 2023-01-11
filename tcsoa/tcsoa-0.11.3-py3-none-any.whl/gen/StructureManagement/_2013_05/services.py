from __future__ import annotations

from tcsoa.gen.StructureManagement._2013_05.VariantManagement import BOMVariantRuleContents, SetBOMVariantRulesResponse, BOMVariantRulesResponse, SetBOMVariantRuleData, GetBOMVariantRuleInput, InputBOMLinesSet, ApplyBOMVariantRulesResponse, GetVariantExpressionsMatchInfoResponse
from tcsoa.gen.StructureManagement._2013_05.StructureVerification import AttributeGroupAndFormComparisonResponse, ConnectedObjectsComparisonResponse
from tcsoa.gen.BusinessObjects import BOMWindow
from tcsoa.gen.StructureManagement._2012_02.StructureVerification import EquivalentLines
from typing import List
from tcsoa.gen.StructureManagement._2013_05.IncrementalChange import ObjectsICEInfo
from tcsoa.gen.Server import ServiceData
from tcsoa.base import TcService


class VariantManagementService(TcService):

    @classmethod
    def getVariantExpressionsMatchInfo(cls, inputBOMLinesSets: List[InputBOMLinesSet]) -> GetVariantExpressionsMatchInfoResponse:
        """
        This operation calculates and returns the rolledup variant expressions and rolledUp clause lists for the input
        rollUpBomLines. For the nonRolledUpBomLines, BOMLine variant conditions and clause lists will be returned. . If
        doCompare parameter is set as true, then this operation compares the equivalent lines based on the variant
        conditions and sets the isDifferent variable accordingly. The lines in input rollUpBomLines, will be compared
        using the rolled up variants and the lines in the nonRollUpBomLines list will be compared using variant
        conditions. All the lines in one InputBOMLinesSet will be compared with each other till a difference is found.
        """
        return cls.execute_soa_method(
            method_name='getVariantExpressionsMatchInfo',
            library='StructureManagement',
            service_date='2013_05',
            service_name='VariantManagement',
            params={'inputBOMLinesSets': inputBOMLinesSets},
            response_cls=GetVariantExpressionsMatchInfoResponse,
        )

    @classmethod
    def setBOMVariantRules(cls, setBOMVariantRuleInput: List[SetBOMVariantRuleData]) -> SetBOMVariantRulesResponse:
        """
        This operation set the input variant rule to the window and returns the list of variant rule and respective
        window.
        
        Use cases:
        This operation should be used when user want to set values of the option on variant rule.
        
        Exceptions:
        >This operation may raise a Teamcenter::Soa::Server::ServiceException wrapping around following Teamcenter
        errors:
        
        46001 Invalid  input is received from input structure SetBOMVariantRuleData
        """
        return cls.execute_soa_method(
            method_name='setBOMVariantRules',
            library='StructureManagement',
            service_date='2013_05',
            service_name='VariantManagement',
            params={'setBOMVariantRuleInput': setBOMVariantRuleInput},
            response_cls=SetBOMVariantRulesResponse,
        )

    @classmethod
    def applyBOMVariantRules(cls, window: BOMWindow, rules: List[BOMVariantRuleContents]) -> ApplyBOMVariantRulesResponse:
        """
        The applyBOMVariantRules operation applies either given BOM variant rules or Saved Variant Rules to the window.
        BOM Variant rules that contain options having multiple values can be applied to the window. Output will be the
        window and list of BOM variant rules and Saved Variant Rules have been applied to the window.
        
        Use cases:
        This operation will be used when BOM variant rules or Saved Variant Rules needs to be applied on the window.
        
        Exceptions:
        >This operation may raise a Teamcenter::Soa::Server::ServiceException wrapping around following Teamcenter
        errors:
        - 46001 Invalid input  is received from input structure BomVariantRuleContents.
        - 214507 Single variant rule cannot be applied if window is in Overlay mode. Multiple variant rule is expected.
        - 214555 Only provide either BOM Variant Rules or Saved Variant Rules.
        
        """
        return cls.execute_soa_method(
            method_name='applyBOMVariantRules',
            library='StructureManagement',
            service_date='2013_05',
            service_name='VariantManagement',
            params={'window': window, 'rules': rules},
            response_cls=ApplyBOMVariantRulesResponse,
        )

    @classmethod
    def getBOMVariantRules(cls, variantRuleInput: List[GetBOMVariantRuleInput]) -> BOMVariantRulesResponse:
        """
        This operation takes list of window and its identifier and returns variant rules and saved variant rules
        associated with the window. As part of input in this operation user can provide saved variant rule along with
        saved variant rule action mode. This action indicates add, remove, update or override actions related to saved
        variant rule. There could be multiple variant rules, associated with window. List of these rules will be
        returned as the output. It also returns list of option and list of values associated with each option.  A flag
        in the value list indicates, if window is configured with the particular option value.  There could be multiple
        values associated with a single option and there could be multiple saved variant rules associated with a window.
        
        Use cases:
        This operation should be used when user wants to get variant rules associated with window. User may also use it
        to set , unset, override or update saved variant rule based on the window mode
        
        Exceptions:
        >This operation may raise a Teamcenter::Soa::Server::ServiceException wrapping around following Teamcenter
        errors.
        - 46001     Invalid input is received from input structure GetBomVariantRuleInput 
        - 214508   Overlay requires at least two variant rules to be loaded.   You cannot remove input variant rule.
        - 214509   Input Variant rule is invalid for the current bom window mode.
        - 214510   For the input svrActionMode, input saved variant rules are invalid. 
        
        """
        return cls.execute_soa_method(
            method_name='getBOMVariantRules',
            library='StructureManagement',
            service_date='2013_05',
            service_name='VariantManagement',
            params={'variantRuleInput': variantRuleInput},
            response_cls=BOMVariantRulesResponse,
        )


class IncrementalChangeService(TcService):

    @classmethod
    def removeIncrementalChanges(cls, listOfObjects: List[ObjectsICEInfo]) -> ServiceData:
        """
        This operation deletes the list of Incremental Change Elements (ICE) on the given BOMLine or the MECfgLine.
        """
        return cls.execute_soa_method(
            method_name='removeIncrementalChanges',
            library='StructureManagement',
            service_date='2013_05',
            service_name='IncrementalChange',
            params={'listOfObjects': listOfObjects},
            response_cls=ServiceData,
        )


class StructureVerificationService(TcService):

    @classmethod
    def getAttributeGroupsAndFormsComparisonDetails(cls, equivalentObjects: List[EquivalentLines], attributeGroupsNames: List[str]) -> AttributeGroupAndFormComparisonResponse:
        """
        This operation returns the details of differences between the supplied Attribute Groups for the supplied
        equivalent objects (that can be Cpd0DesignElement, Cpd0DesignFeature, or BOMLine objects). For each supplied
        attribute group the operation returns the list of its attributes, the attributes values for each supplied
        source and target, and the result of comparing each attribute on all supplied sources and targets.
        """
        return cls.execute_soa_method(
            method_name='getAttributeGroupsAndFormsComparisonDetails',
            library='StructureManagement',
            service_date='2013_05',
            service_name='StructureVerification',
            params={'equivalentObjects': equivalentObjects, 'attributeGroupsNames': attributeGroupsNames},
            response_cls=AttributeGroupAndFormComparisonResponse,
        )

    @classmethod
    def getConnectedObjectsComparisonDetails(cls, equivalentObjects: List[EquivalentLines]) -> ConnectedObjectsComparisonResponse:
        """
        This operation returns the details of any differences between connected objects (that can be either BOMLines or
        Cpd0DesignElements) for the supplied equivalent objects (that can be either BOMLines or Cpd0DesignFeatures).
        The operation takes the source and target and compares their connected objects. The source and target connected
        objects are returned by this operation in the form of a table that is created by the output structures.
        """
        return cls.execute_soa_method(
            method_name='getConnectedObjectsComparisonDetails',
            library='StructureManagement',
            service_date='2013_05',
            service_name='StructureVerification',
            params={'equivalentObjects': equivalentObjects},
            response_cls=ConnectedObjectsComparisonResponse,
        )
