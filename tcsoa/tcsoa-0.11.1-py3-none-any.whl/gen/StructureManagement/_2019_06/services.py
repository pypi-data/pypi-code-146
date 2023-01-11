from __future__ import annotations

from tcsoa.gen.StructureManagement._2019_06.VariantManagement import BOMVariantRuleContents2, ApplyBOMVariantRulesResponse2, SetBOMVariantRulesResponse2, BOMVariantRulesResponse2, SetBOMVariantRuleData2
from tcsoa.gen.BusinessObjects import BOMWindow
from tcsoa.gen.StructureManagement._2013_05.VariantManagement import GetBOMVariantRuleInput
from typing import List
from tcsoa.base import TcService


class VariantManagementService(TcService):

    @classmethod
    def setBOMVariantRules2(cls, setBOMVariantRuleInput: List[SetBOMVariantRuleData2]) -> SetBOMVariantRulesResponse2:
        """
        This operation set the input variant rule to the window and returns the list of variant rule and respective
        window.
        
        Use cases:
        This operation should be used when user want to set values of the option on variant rule.
        
        Exceptions:
        >This operation may raise a Teamcenter::Soa::Server::ServiceException.
        &bull;    214515   The operation has encountered an internal error.
        """
        return cls.execute_soa_method(
            method_name='setBOMVariantRules2',
            library='StructureManagement',
            service_date='2019_06',
            service_name='VariantManagement',
            params={'setBOMVariantRuleInput': setBOMVariantRuleInput},
            response_cls=SetBOMVariantRulesResponse2,
        )

    @classmethod
    def applyBOMVariantRules2(cls, window: BOMWindow, rules: List[BOMVariantRuleContents2]) -> ApplyBOMVariantRulesResponse2:
        """
        The applyBOMVariantRules2 operation applies either given BOM variant rules or Saved Variant Rules to the
        window. BOM Variant rules that contain options having multiple values can be applied to the window. Output will
        be the window and list of BOM variant rules and Saved Variant Rules have been applied to the window.
        
        Use cases:
        This operation will be used when BOM variant rules or Saved Variant Rules needs to be applied on the window.
        
        Exceptions:
        >This operation may raise a Teamcenter::Soa::Server::ServiceException.
        &bull;    214515   The operation has encountered an internal error.
        """
        return cls.execute_soa_method(
            method_name='applyBOMVariantRules2',
            library='StructureManagement',
            service_date='2019_06',
            service_name='VariantManagement',
            params={'window': window, 'rules': rules},
            response_cls=ApplyBOMVariantRulesResponse2,
        )

    @classmethod
    def getBOMVariantRules2(cls, variantRuleInput: List[GetBOMVariantRuleInput]) -> BOMVariantRulesResponse2:
        """
        This operation takes list of windows and its identifier and returns variant rules and saved variant rules
        associated with the window. As part of input in this operation user can provide saved variant rule along with
        saved variant rule action mode. This action indicates add, remove, update or override actions related to the
        saved variant rule. There could be multiple variant rules, associated with window. List of these rules will be
        returned as the output. It also returns list of option and list of values associated with each option. A flag
        in the value list indicates, if window is configured with the particular option value. There could be multiple
        values associated with a single option and there could be multiple saved variant rules associated with a window.
        
        Use cases:
        This operation should be used when user wants to get variant rules associated with window. User may also use it
        to set, unset, override or update saved variant rule based on the window mode.
        
        Exceptions:
        >This operation may raise a Teamcenter::Soa::Server::ServiceException.
        &bull;    214515   The operation has encountered an internal error.
        """
        return cls.execute_soa_method(
            method_name='getBOMVariantRules2',
            library='StructureManagement',
            service_date='2019_06',
            service_name='VariantManagement',
            params={'variantRuleInput': variantRuleInput},
            response_cls=BOMVariantRulesResponse2,
        )
