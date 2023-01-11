# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent.protect.rule.base_rule import BaseRule
from contrast.agent.protect.rule import ProtectionRule


class MalformedHeader(BaseRule):
    """
    Malformed Header Protection rule
    """

    RULE_NAME = "malformed-header"

    @property
    def mode(self):
        """
        Always block at perimeter
        """
        return ProtectionRule.BLOCK_AT_PERIMETER
