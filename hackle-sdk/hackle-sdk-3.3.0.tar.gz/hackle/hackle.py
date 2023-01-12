from . import exceptions as hackle_exceptions
from . import logger as _logging
from .commons import utils
from .commons import validator
from .decision import ExperimentDecision, DecisionReason, FeatureFlagDecision
from .evaluation.evaluator import Evaluator
from .evaluation.flow.evaluation_flow_factory import EvaluationFlowFactory
from .event.event_dispatcher import EventDispatcher
from .event.event_processor import BatchEventProcessor
from .internal_client import InternalClient
from .remote_config import HackleRemoteConfigImpl
from .user.hackle_user_resolver import HackleUserResolver
from .workspace_fetcher import WorkspaceFetcher


def __singleton(cls):
    instance = [None]

    def wrapper(*args, **kwargs):
        if instance[0] is None:
            instance[0] = cls(*args, **kwargs)
        return instance[0]

    return wrapper


@__singleton
class Client(object):
    def __init__(self, sdk_key=None, logger=None, timeout=None):
        if sdk_key is None:
            raise hackle_exceptions.RequiredParameterException('sdk_key must not be empty.')

        self.logger = _logging.adapt_logger(logger or _logging.NoOpLogger())

        self.internal_client = InternalClient(
            evaluator=Evaluator(EvaluationFlowFactory(self.logger)),
            workspace_fetcher=WorkspaceFetcher(sdk_key, logger=self.logger, timeout=timeout),
            event_processor=BatchEventProcessor(sdk_key, EventDispatcher(), self.logger),
            logger=self.logger
        )

        self.hackle_user_resolver = HackleUserResolver(logger)

    def close(self):
        self.internal_client.close()

    def __exit__(self):
        self.close()

    def variation(self, experiment_key, user, default_variation='A'):
        """
        Decide the variation to expose to the user for experiment.

        This method return the "A" if:
            - The experiment key is invalid
            - The experiment has not started yet
            - The user is not allocated to the experiment
            - The decided variation has been dropped

        :param int experiment_key: the unique key of the experiment.
        :param hackle.model.User or hackle.model.HackleUser user: the user to participate in the experiment.
        :param str default_variation: the default variation of the experiment.

        :return: the decided variation for the user, or the default variation.
        """
        return self.variation_detail(experiment_key, user, default_variation).variation

    def variation_detail(self, experiment_key, user, default_variation='A'):
        """
        Decide the variation to expose to the user for experiment, and returns an object that
        describes the way the variation was decided.

        :param int experiment_key: the unique key of the experiment.
        :param hackle.model.User or hackle.model.HackleUser user: the user to participate in the experiment.
        :param str default_variation: the default variation of the experiment.

        :return: a object describing the result
        """
        try:
            if not validator.is_non_zero_and_empty_int(experiment_key):
                self.logger.error('Experiment Key must not be empty. : {}'.format(experiment_key))
                return ExperimentDecision(default_variation, DecisionReason.INVALID_INPUT)

            hackle_user = self.hackle_user_resolver.resolve_or_none(user)
            if hackle_user is None:
                return ExperimentDecision(default_variation, DecisionReason.INVALID_INPUT)

            return self.internal_client.experiment(experiment_key, hackle_user, default_variation)
        except Exception as e:
            self.logger.error(
                "Unexpected error while deciding variation of experiment[{}]: {}".format(experiment_key, str(e)))
            return ExperimentDecision(default_variation, DecisionReason.EXCEPTION)

    def is_feature_on(self, feature_key, user):
        """
        Decide whether the feature is turned on to the user.

        :param int feature_key: the unique key of the feature.
        :param hackle.model.User or hackle.model.HackleUser user: the user to participate in the experiment.
        :return: True if the feature is on
                  False if the feature is off
        """
        return self.feature_flag_detail(feature_key, user).is_on

    def feature_flag_detail(self, feature_key, user):
        """
        Decide whether the feature is turned on to the user, and returns an object that
        describes the way the value was decided.

        :param int feature_key: the unique key of the feature.
        :param hackle.model.User or hackle.model.HackleUser user: the user to participate in the experiment.

        :return: a object describing the result
        """
        try:

            if not validator.is_non_zero_and_empty_int(feature_key):
                self.logger.error('Experiment Key must not be empty. : {}'.format(feature_key))
                return FeatureFlagDecision(False, DecisionReason.INVALID_INPUT)

            hackle_user = self.hackle_user_resolver.resolve_or_none(user)
            if hackle_user is None:
                return FeatureFlagDecision(False, DecisionReason.INVALID_INPUT)

            return self.internal_client.feature_flag(feature_key, hackle_user)
        except Exception as e:
            self.logger.error("Unexpected error while deciding feature flag[{}]: {}".format(feature_key, str(e)))
            return FeatureFlagDecision(False, DecisionReason.EXCEPTION)

    def track(self, event, user):
        """
        Records the event performed by the user with additional numeric value.

        :param hackle.model.Event event: the unique key of the event. MUST NOT be null.
        :param hackle.model.User or hackle.model.HackleUser user: the user to participate in the experiment.
        """
        try:
            if not validator.is_valid_event(event):
                self.logger.error('Event is not valid. Event must be hackle.model.event and event.id\'s type must be '
                                  'string_types. value\'s type must be numeric. '
                                  ': {}'.format(event))
                return

            if not validator.is_valid_properties(event.properties):
                self.logger.warning(
                    'Event properties is not valid. Event properties must be not dic types and items types must be string_types, number, bool.'
                    ': {}'.format(event.properties))
                event.properties = utils.filter_properties(event.properties)

            hackle_user = self.hackle_user_resolver.resolve_or_none(user)
            if hackle_user is None:
                return

            self.internal_client.track_event(event, hackle_user)
        except Exception as e:
            self.logger.error('Unexpected error while tracking event: {}'.format(str(e)))

    def remote_config(self, user):
        """
        Returns a instance of Hackle Remote Config.

        :param hackle.model.User or hackle.model.HackleUser user: the identifier of user.
        """
        return HackleRemoteConfigImpl(user, self.internal_client, self.hackle_user_resolver)
