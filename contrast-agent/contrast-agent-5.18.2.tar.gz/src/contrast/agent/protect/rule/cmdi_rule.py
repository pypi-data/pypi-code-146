# -*- coding: utf-8 -*-
# Copyright © 2023 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import os
import re


import contrast
from contrast.agent import agent_lib
from contrast.agent.agent_lib import get_index_of_chained_cmd
from contrast.agent.agent_lib import does_command_contain_dangerous_path
from contrast.agent.protect.rule.base_rule import BaseRule
from contrast.agent.protect.rule.cmd_injection.cmd_injection_rep_mixin import (
    CommandInjectionREPMixin,
)
from contrast.api.dtm_pb2 import HttpRequest
from contrast.api.user_input import UserInput
from contrast.utils.exceptions.security_exception import SecurityException
from contrast.utils.string_utils import index_of_any


class CmdInjection(BaseRule, CommandInjectionREPMixin):
    """
    Command Injection Protection rule
    """

    RULE_NAME = "cmd-injection"
    BITMASK_VALUE = agent_lib.CONSTANTS.RuleType.get(RULE_NAME)

    BIN_SH_C = "/bin/sh-c"

    CHAIN = ["&", ";", "|", ">", "<"]

    START_IDX = "start_idx"
    END_IDX = "end_idx"

    def find_attack(self, candidate_string=None, **kwargs):
        command_string = str(candidate_string) if candidate_string else None

        attack = super().find_attack(command_string, **kwargs)

        if not attack and command_string:
            evaluations_for_rule = self.evaluations_for_rule()
            return self.find_probable_attack(
                command_string, evaluations_for_rule, **kwargs
            )

        return attack

    def in_new_process(self):
        """
        Compare current pid to context pid
        """
        current_pid = os.getpid()

        original_pid = self.settings.pid

        return current_pid != original_pid

    def is_chained_command(self, command):
        """
        A command is chained if it is piped, backgrounded, or appended
        """
        if self.settings.config.is_agent_lib_enabled:
            return get_index_of_chained_cmd(command) != -1

        return index_of_any(command, self.CHAIN) != -1

    def does_contain_dangerous_path(self, command):
        if self.settings.config.is_agent_lib_enabled:
            return does_command_contain_dangerous_path(command) == 1

        return False

    def find_probable_attack(self, command_string, evaluations_for_rule, **kwargs):
        """
        Search through the attack string for a command that may have been executed
        """
        if not self.is_chained_command(
            command_string
        ) and not self.does_contain_dangerous_path(command_string):
            return None

        attack = None
        most_likely = None

        for evaluation in evaluations_for_rule:
            if not self.is_chained_command(
                evaluation.value
            ) and not self.does_contain_dangerous_path(evaluation.value):
                continue

            most_likely = evaluation
            break

        attack = self.build_attack_with_match(
            command_string, most_likely, attack, **kwargs
        )

        if not attack:
            return None

        self.log_rule_matched(most_likely, self.mode, command_string)

        return attack

    def build_sample(self, evaluation, command, **kwargs):
        sample = self.build_base_sample(evaluation)

        if command is not None:
            sample.details["command"] = command

        if self.START_IDX in kwargs or self.END_IDX in kwargs:
            sample.details["startIndex"] = kwargs.get(self.START_IDX, 0)
            sample.details["endIndex"] = kwargs.get(self.END_IDX, 0)
        elif command is not None:
            search_value = evaluation.value

            match = re.search(search_value, command, re.IGNORECASE)

            if match:
                sample.details["startIndex"] = match.start()
                sample.details["endIndex"] = match.end()

        return sample

    def infilter_kwargs(self, user_input, patch_policy):
        return dict(method=patch_policy.method_name, original_command=user_input)

    def skip_protect_analysis(self, user_input, args, kwargs):
        """
        cmdi rule supports list user input as well as str and bytes
        Do not skip protect analysis if user input is a  populated list
        """
        if isinstance(user_input, list) and user_input:
            return False

        return super().skip_protect_analysis(user_input, args, kwargs)

    def convert_input(self, user_input):
        if isinstance(user_input, list):
            user_input = " ".join(user_input)

        return super().convert_input(user_input)

    def infilter(self, match_string, **kwargs):
        context = contrast.CS__CONTEXT_TRACKER.current()

        if self.in_new_process():
            from contrast.agent.request_context import RequestContext

            context = RequestContext(context.environ)

        original_command = kwargs.get("original_command", "")

        if self.is_detect_parameter_command_backdoors_enabled:
            self.detect_command_backdoor(context, original_command)

        evaluations_for_rule = self.evaluations_for_rule()

        if not evaluations_for_rule:
            return

        if self.is_detect_chained_commands_enabled:
            evaluation = evaluations_for_rule[0]
            self.detect_command_chaining(original_command, evaluation)

        if self.settings.config.is_agent_lib_enabled:
            evaluation = evaluations_for_rule[0]
            self.detect_dangerous_path(original_command, evaluation)

        super().infilter(match_string, **kwargs)

    def detect_command_backdoor(self, context, command):
        """
        If we detect the user is supplying OS commands from a parameter
        then we'll block it. This is a common pattern from web shells
        and contrived applications.
        """
        parameter_key, parameter_value = self.find_matching_parameter(
            context, command
        ) or (None, None)
        if parameter_key and parameter_value:
            self.report_command_backdoor(command, parameter_key, parameter_value)

            raise SecurityException(self, "Command from input detected")

    def detect_command_chaining(self, command, evaluation):
        """
        If we detected an attack inbound but we didn't see it in the command
        we still might want to fuzzy match on chained attacks.
        """
        if self.settings.config.is_agent_lib_enabled:
            index = get_index_of_chained_cmd(command)
        else:
            index = self.get_first_command_chain_index(command)

        if index != -1:
            self.report_chained_injection(evaluation, command, index)

            if self.is_blocked():
                raise SecurityException(self, "Command chaining detected")

    def detect_dangerous_path(self, command, evaluation):
        is_dangerous_path_detected = does_command_contain_dangerous_path(command)

        if is_dangerous_path_detected == 1:
            self.report_dangerous_path(evaluation, command)

            if self.is_blocked():
                raise SecurityException(self, "Dangerous path detected")

    def find_matching_parameter(self, context, command):
        request = context.request

        if request and isinstance(command, str):
            normalized_command = self._normalize_str(command)

            parameters = request.params.dict_of_lists()

            for parameter_key, parameter_values in parameters.items():
                param = self._get_param_in_command(parameter_values, normalized_command)
                if param:
                    return parameter_key, param

        return None

    def _get_param_in_command(self, parameter_values, normalized_command):
        for param in parameter_values:
            if param and len(param) >= 2:
                normalized_param_value = self._normalize_str(param)

                if (
                    normalized_command == normalized_param_value
                    or normalized_command.startswith(self.BIN_SH_C)
                    or normalized_command.endswith(normalized_param_value)
                ):
                    return param

        return None

    def _normalize_str(self, string):
        return re.sub("\\s+", "", string).lower()

    def report_command_backdoor(self, command, parameter_key, parameter_value):
        evaluations_for_rule = self.evaluations_for_rule()
        if evaluations_for_rule:
            evaluation = evaluations_for_rule[0]
            evaluation.attack_count += 1
        else:
            evaluation = None

        sample = self.create_backdoor_command_sample(
            evaluation, command, parameter_key, parameter_value
        )

        attack = self.build_base_attack()

        attack.add_sample(sample)

        attack.set_response(self.response_from_mode(self.mode))

        self.log_rule_matched(evaluation, attack.response, parameter_value)

        self._append_to_context(attack)

    def report_chained_injection(self, evaluation, command, offset):
        start_idx = offset
        end_idx = len(command) - 1

        attack = self.build_or_append_attack(evaluation, candidate_string=command)

        result = self.build_attack_with_match(
            command, evaluation, attack, start_idx=start_idx, end_idx=end_idx
        )

        self._append_to_context(result)

    def report_dangerous_path(self, evaluation, command):
        attack = self.build_or_append_attack(evaluation, candidate_string=command)

        result = self.build_attack_with_match(command, evaluation, attack)

        self._append_to_context(result)

    def create_backdoor_command_sample(
        self, evaluation, command, parameter_key, parameter_value
    ):

        sample = self.build_base_sample(evaluation)
        user_input = UserInput(
            input_type=UserInput.PARAMETER_VALUE,
            key=parameter_key,
            value=parameter_value,
            matcher_ids=[self.REP_DETECT_PARAMETER_COMMAND_BACKDOORS_ID],
            document_type=HttpRequest.NORMAL,
        )
        sample.set_user_input(user_input)

        start_index = 0
        end_index = 0
        boundary_overrun_idx = 0
        input_boundary_idx = 0

        if self.settings.config.is_agent_lib_enabled:
            agent_lib_evaluation = agent_lib.check_cmd_injection_query(
                0, len(user_input.value), user_input.value
            )
            if bool(agent_lib_evaluation):
                start_index = agent_lib_evaluation.start_index
                end_index = agent_lib_evaluation.end_index
                boundary_overrun_idx = agent_lib_evaluation.boundary_overrun_index
                input_boundary_idx = agent_lib_evaluation.input_boundary_index

        sample.details["command"] = command
        sample.details["startIndex"] = start_index
        sample.details["endIndex"] = end_index
        sample.details["boundary_overrun_idx"] = boundary_overrun_idx
        sample.details["input_boundary_idx"] = input_boundary_idx

        return sample
