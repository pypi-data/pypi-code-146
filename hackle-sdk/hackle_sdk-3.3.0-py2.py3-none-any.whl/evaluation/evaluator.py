from hackle.commons.validator import is_string, is_number, is_bool
from hackle.decision import DecisionReason


class Evaluation(object):
    def __init__(self, variation_id, variation_key, reason, config=None):
        self.variation_id = variation_id
        self.variation_key = variation_key
        self.reason = reason
        self.config = config

    def __eq__(self, o):
        if isinstance(o, self.__class__):
            return self.__dict__ == o.__dict__
        else:
            return False

    def __str__(self):
        return 'Evaluation(variation_id={}, variation_key={}, reason={}, config={})'.format(self.variation_id,
                                                                                            self.variation_key,
                                                                                            self.reason,
                                                                                            self.config)

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def with_variation(workspace, variation, reason):
        parameter_configuration_id = variation.parameter_configuration_id
        if parameter_configuration_id is None:
            return Evaluation(variation_id=variation.id, variation_key=variation.key, reason=reason, config=None)

        parameter_configuration = workspace.get_parameter_configuration_or_none(parameter_configuration_id)
        if parameter_configuration is None:
            raise Exception('ParameterConfiguration[{}]'.format(parameter_configuration_id))

        return Evaluation(variation_id=variation.id, variation_key=variation.key, reason=reason,
                          config=parameter_configuration)

    @staticmethod
    def of(workspace, experiment, variation_key, reason):
        variation = experiment.get_variation_by_key_or_none(variation_key)
        if variation is None:
            return Evaluation(variation_id=None, variation_key=variation_key, reason=reason, config=None)
        else:
            return Evaluation.with_variation(workspace, variation, reason)


class RemoteConfigEvaluation(object):
    def __init__(self, value_id, value, reason, properties):
        self.value_id = value_id
        self.value = value
        self.reason = reason
        self.properties = properties


class Evaluator(object):

    def __init__(self, evaluation_flow_factory):
        self.evaluation_flow_factory = evaluation_flow_factory

    def evaluate(self, workspace, experiment, user, default_variation_key):
        evaluation_flow = self.evaluation_flow_factory.get_evaluation_flow(experiment.type)
        return evaluation_flow.evaluate(workspace, experiment, user, default_variation_key)

    def remote_config_evaluate(self, workspace, parameter, user, required_type, default_value):
        properties = {'requestValueType': required_type, 'requestDefaultValue': default_value}

        identifier = user.identifiers.get(parameter.identifier_type)
        if identifier is None:
            return RemoteConfigEvaluation(value_id=None, value=default_value,
                                          reason=DecisionReason.IDENTIFIER_NOT_FOUND, properties=properties)

        target_rule_determiner = self.evaluation_flow_factory.remote_config_parameter_target_rule_determiner
        target_rule = target_rule_determiner.determine_target_rule_or_none(workspace, parameter, user)

        if target_rule is not None:
            properties['targetRuleKey'] = target_rule.key
            properties['targetRuleName'] = target_rule.name
            return self._remote_config_evaluate(target_rule.value, DecisionReason.TARGET_RULE_MATCH, required_type,
                                                default_value, properties)

        return self._remote_config_evaluate(parameter.default_value, DecisionReason.DEFAULT_RULE, required_type,
                                            default_value, properties)

    def _remote_config_evaluate(self, parameter_value, reason, required_type, default_value, properties):
        if required_type == 'NULL':
            properties["returnValue"] = parameter_value.raw_value
            return RemoteConfigEvaluation(value_id=parameter_value.id, value=parameter_value.raw_value, reason=reason,
                                          properties=properties)

        is_valid_value = self._is_valid_type(parameter_value.raw_value, required_type)

        if is_valid_value:
            properties["returnValue"] = parameter_value.raw_value
            return RemoteConfigEvaluation(value_id=parameter_value.id, value=parameter_value.raw_value, reason=reason,
                                          properties=properties)
        else:
            properties["returnValue"] = default_value
            return RemoteConfigEvaluation(value_id=None, value=default_value, reason=DecisionReason.TYPE_MISMATCH,
                                          properties=properties)

    def _is_valid_type(self, value, required_type):
        if required_type == 'STRING':
            return is_string(value)
        elif required_type == 'NUMBER':
            return is_number(value)
        elif required_type == 'BOOLEAN':
            return is_bool(value)
        else:
            return False
