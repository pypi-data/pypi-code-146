from hackle import logger as _logging
from hackle.evaluation.action.action_resolver import ActionResolver
from hackle.evaluation.bucket.bucketer import Bucketer
from hackle.evaluation.container.container_resolver import ContainerResolver
from hackle.evaluation.flow.evaluation_flow import EvaluationFlow
from hackle.evaluation.flow.flow_evaluator import *
from hackle.evaluation.match.condition_matcher import ConditionMatcherFactory
from hackle.evaluation.match.target_matcher import TargetMatcher
from hackle.evaluation.target.experiment_target_determiner import ExperimentTargetDeterminer
from hackle.evaluation.target.override_resolver import OverrideResolver
from hackle.evaluation.target.remote_config_target_rule_determiner import RemoteConfigTargetRuleDeterminer
from hackle.evaluation.target.target_rule_determiner import TargetRuleDeterminer


class EvaluationFlowFactory(object):

    def __init__(self, logger=None):
        self.logger = _logging.adapt_logger(logger or _logging.NoOpLogger())

        bucketer = Bucketer()
        target_matcher = TargetMatcher(ConditionMatcherFactory())
        action_resolver = ActionResolver(bucketer, self.logger)
        override_resolver = OverrideResolver(target_matcher, action_resolver)
        container_resolver = ContainerResolver(bucketer)

        self.ab_test_flow = EvaluationFlow.of(
            OverrideEvaluator(override_resolver),
            IdentifierEvaluator(),
            ContainerEvaluator(container_resolver),
            ExperimentTargetEvaluator(ExperimentTargetDeterminer(target_matcher)),
            DraftEvaluator(),
            PausedEvaluator(),
            CompletedEvaluator(),
            TrafficAllocateEvaluator(action_resolver)
        )

        self.feature_flag_flow = EvaluationFlow.of(
            DraftEvaluator(),
            PausedEvaluator(),
            CompletedEvaluator(),
            OverrideEvaluator(override_resolver),
            IdentifierEvaluator(),
            TargetRuleEvaluator(TargetRuleDeterminer(target_matcher), action_resolver),
            DefaultRuleEvaluator(action_resolver)
        )

        self.remote_config_parameter_target_rule_determiner = RemoteConfigTargetRuleDeterminer(target_matcher, bucketer)

    def get_evaluation_flow(self, experiment_type):
        if experiment_type == 'AB_TEST':
            return self.ab_test_flow
        elif experiment_type == 'FEATURE_FLAG':
            return self.feature_flag_flow
        else:
            raise Exception('Unsupported type [{}]'.format(experiment_type))
