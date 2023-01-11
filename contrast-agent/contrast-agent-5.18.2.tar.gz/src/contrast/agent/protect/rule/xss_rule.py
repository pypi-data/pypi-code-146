# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent import agent_lib
from contrast.agent.protect.rule.base_rule import BaseRule
from contrast.agent.protect.rule import ProtectionRule


class Xss(BaseRule):
    """
    Cross Site Scripting Protection rule
    Currently only a prefilter / block at perimeter rule
    """

    RULE_NAME = "reflected-xss"
    BITMASK_VALUE = agent_lib.CONSTANTS.RuleType.get(RULE_NAME)

    @property
    def mode(self):
        """
        Always block at perimeter
        """
        mode = self.mode_from_settings()

        return (
            mode
            if mode in [ProtectionRule.NO_ACTION, ProtectionRule.MONITOR]
            else ProtectionRule.BLOCK_AT_PERIMETER
        )
