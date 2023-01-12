import abc

from six import add_metaclass

from hackle.decision import DecisionReason
from hackle.evaluation.evaluator import Evaluation


@add_metaclass(abc.ABCMeta)
class FlowEvaluator(object):

    @abc.abstractmethod
    def evaluate(self, workspace, experiment, user, default_variation_key, next_flow):
        pass


class OverrideEvaluator(FlowEvaluator):

    def __init__(self, override_resolver):
        self.override_resolver = override_resolver

    def evaluate(self, workspace, experiment, user, default_variation_key, next_flow):
        overridden_variation = self.override_resolver.resolve_or_none(workspace, experiment, user)

        if overridden_variation:
            if experiment.type == 'AB_TEST':
                return Evaluation.with_variation(workspace, overridden_variation, DecisionReason.OVERRIDDEN)
            elif experiment.type == 'FEATURE_FLAG':
                return Evaluation.with_variation(workspace, overridden_variation,
                                                 DecisionReason.INDIVIDUAL_TARGET_MATCH)
            else:
                raise Exception('experiment type [{}]'.format(experiment.type))
        else:
            return next_flow.evaluate(workspace, experiment, user, default_variation_key)


class DraftEvaluator(FlowEvaluator):
    def evaluate(self, workspace, experiment, user, default_variation_key, next_flow):
        if experiment.status == 'DRAFT':
            return Evaluation.of(workspace, experiment, default_variation_key, DecisionReason.EXPERIMENT_DRAFT)
        else:
            return next_flow.evaluate(workspace, experiment, user, default_variation_key)


class PausedEvaluator(FlowEvaluator):
    def evaluate(self, workspace, experiment, user, default_variation_key, next_flow):
        if experiment.status == 'PAUSED':
            if experiment.type == 'AB_TEST':
                return Evaluation.of(workspace, experiment, default_variation_key, DecisionReason.EXPERIMENT_PAUSED)
            elif experiment.type == 'FEATURE_FLAG':
                return Evaluation.of(workspace, experiment, default_variation_key, DecisionReason.FEATURE_FLAG_INACTIVE)
            else:
                raise Exception('experiment type [{}]'.format(experiment.type))
        else:
            return next_flow.evaluate(workspace, experiment, user, default_variation_key)


class CompletedEvaluator(FlowEvaluator):
    def evaluate(self, workspace, experiment, user, default_variation_key, next_flow):
        if experiment.status == 'COMPLETED':
            return Evaluation.with_variation(workspace, experiment.winner_variation,
                                             DecisionReason.EXPERIMENT_COMPLETED)
        else:
            return next_flow.evaluate(workspace, experiment, user, default_variation_key)


class ExperimentTargetEvaluator(FlowEvaluator):

    def __init__(self, experiment_target_determiner):
        self.experiment_target_determiner = experiment_target_determiner

    def evaluate(self, workspace, experiment, user, default_variation_key, next_flow):
        if experiment.type != 'AB_TEST':
            raise Exception('experiment type must be AB_TEST [{}]'.format(experiment.id))

        is_user_in_experiment_target = self.experiment_target_determiner.is_user_in_experiment_target(workspace,
                                                                                                      experiment, user)
        if is_user_in_experiment_target:
            return next_flow.evaluate(workspace, experiment, user, default_variation_key)
        else:
            return Evaluation.of(workspace, experiment, default_variation_key, DecisionReason.NOT_IN_EXPERIMENT_TARGET)


class TrafficAllocateEvaluator(FlowEvaluator):

    def __init__(self, action_resolver):
        self.action_resolver = action_resolver

    def evaluate(self, workspace, experiment, user, default_variation_key, next_flow):
        if experiment.status != 'RUNNING':
            raise Exception('experiment status must be RUNNING [{}]'.format(experiment.id))

        if experiment.type != 'AB_TEST':
            raise Exception('experiment type must be AB_TEST [{}]'.format(experiment.id))

        variation = self.action_resolver.resolve_or_none(experiment.default_rule, workspace, experiment, user)
        if not variation:
            return Evaluation.of(workspace, experiment, default_variation_key, DecisionReason.TRAFFIC_NOT_ALLOCATED)

        if variation.is_dropped:
            return Evaluation.of(workspace, experiment, default_variation_key, DecisionReason.VARIATION_DROPPED)

        return Evaluation.with_variation(workspace, variation, DecisionReason.TRAFFIC_ALLOCATED)


class TargetRuleEvaluator(FlowEvaluator):

    def __init__(self, target_rule_determiner, action_resolver):
        self.target_rule_determiner = target_rule_determiner
        self.action_resolver = action_resolver

    def evaluate(self, workspace, experiment, user, default_variation_key, next_flow):
        if experiment.status != 'RUNNING':
            raise Exception('experiment status must be RUNNING [{}]'.format(experiment.id))

        if experiment.type != 'FEATURE_FLAG':
            raise Exception('experiment type must be FEATURE_FLAG [{}]'.format(experiment.id))

        if user.identifiers.get(experiment.identifier_type) is None:
            return next_flow.evaluate(workspace, experiment, user, default_variation_key)

        target_rule = self.target_rule_determiner.determine_target_rule_or_none(workspace, experiment, user)
        if target_rule is None:
            return next_flow.evaluate(workspace, experiment, user, default_variation_key)

        variation = self.action_resolver.resolve_or_none(target_rule.action, workspace, experiment, user)
        if not variation:
            raise Exception('FeatureFlag must decide the variation [{}]'.format(experiment.id))

        return Evaluation.with_variation(workspace, variation, DecisionReason.TARGET_RULE_MATCH)


class DefaultRuleEvaluator(FlowEvaluator):

    def __init__(self, action_resolver):
        self.action_resolver = action_resolver

    def evaluate(self, workspace, experiment, user, default_variation_key, next_flow):
        if experiment.status != 'RUNNING':
            raise Exception('experiment status must be RUNNING [{}]'.format(experiment.id))

        if experiment.type != 'FEATURE_FLAG':
            raise Exception('experiment type must be FEATURE_FLAG [{}]'.format(experiment.id))

        if user.identifiers.get(experiment.identifier_type) is None:
            return Evaluation.of(workspace, experiment, default_variation_key, DecisionReason.DEFAULT_RULE)

        variation = self.action_resolver.resolve_or_none(experiment.default_rule, workspace, experiment, user)
        if not variation:
            raise Exception('FeatureFlag must decide the variation [{}]'.format(experiment.id))

        return Evaluation.with_variation(workspace, variation, DecisionReason.DEFAULT_RULE)


class ContainerEvaluator(FlowEvaluator):

    def __init__(self, container_resolver):
        self.container_resolver = container_resolver

    def evaluate(self, workspace, experiment, user, default_variation_key, next_flow):
        container_id = experiment.container_id
        if container_id is None:
            return next_flow.evaluate(workspace, experiment, user, default_variation_key)

        container = workspace.get_container_or_none(container_id)
        if container is None:
            raise Exception('Container[{}]'.format(container_id))

        bucket = workspace.get_bucket_or_none(container.bucket_id)
        if bucket is None:
            raise Exception('Bucket[{}]'.format(container.bucket_id))

        is_user_in_container_group = self.container_resolver.is_user_in_container_group(container, bucket, experiment,
                                                                                        user)
        if is_user_in_container_group:
            return next_flow.evaluate(workspace, experiment, user, default_variation_key)
        else:
            return Evaluation.of(workspace, experiment, default_variation_key,
                                 DecisionReason.NOT_IN_MUTUAL_EXCLUSION_EXPERIMENT)


class IdentifierEvaluator(FlowEvaluator):
    def evaluate(self, workspace, experiment, user, default_variation_key, next_flow):
        if user.identifiers.get(experiment.identifier_type) is not None:
            return next_flow.evaluate(workspace, experiment, user, default_variation_key)
        else:
            return Evaluation.of(workspace, experiment, default_variation_key, DecisionReason.IDENTIFIER_NOT_FOUND)
