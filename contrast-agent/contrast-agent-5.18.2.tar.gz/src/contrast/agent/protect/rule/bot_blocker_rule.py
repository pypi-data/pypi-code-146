# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from contrast.agent import agent_lib
from contrast.agent.protect.rule.base_rule import BaseRule


class BotBlocker(BaseRule):

    RULE_NAME = "bot-blocker"
    BITMASK_VALUE = agent_lib.CONSTANTS.RuleType.get(RULE_NAME)
