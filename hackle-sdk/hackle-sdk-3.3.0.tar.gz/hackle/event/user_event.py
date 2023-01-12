import abc
import time

from hackle.user.identifier_type import IdentifierType

ABC = abc.ABCMeta('ABC', (object,), {'__slots__': ()})


class UserEvent(ABC):
    def __init__(self, user):
        self.timestamp = self._get_time()
        self.userId = user.identifiers.get(IdentifierType.ID)
        self.identifiers = user.identifiers
        self.userProperties = user.properties

    # noinspection PyMethodMayBeStatic
    def _get_time(self):
        return int(round(time.time() * 1000))

    @staticmethod
    def exposure(experiment, user, evaluation):
        return ExposureEvent(user, experiment, evaluation)

    @staticmethod
    def track(event_type, event, user):
        return TrackEvent(user, event_type, event)

    @staticmethod
    def remote_config(parameter, user, evaluation):
        return RemoteConfigEvent(user, parameter, evaluation)


class ExposureEvent(UserEvent):
    def __init__(self, user, experiment, evaluation):
        super(ExposureEvent, self).__init__(user)
        self.experimentId = experiment.id
        self.experimentKey = experiment.key
        self.experimentType = experiment.type
        self.experimentVersion = experiment.version
        self.variationId = evaluation.variation_id
        self.variationKey = evaluation.variation_key
        self.decisionReason = evaluation.reason

        properties = {}
        if evaluation.config is not None:
            properties['$parameterConfigurationId'] = evaluation.config.id
        self.properties = properties


class TrackEvent(UserEvent):
    def __init__(self, user, event_type, event):
        super(TrackEvent, self).__init__(user)
        self.eventTypeId = event_type.id
        self.eventTypeKey = event_type.key
        self.value = event.value
        self.properties = event.properties


class RemoteConfigEvent(UserEvent):
    def __init__(self, user, parameter, evaluation):
        super(RemoteConfigEvent, self).__init__(user)
        self.parameterId = parameter.id
        self.parameterKey = parameter.key
        self.parameterType = parameter.type
        self.decisionReason = evaluation.reason
        self.valueId = evaluation.value_id
        self.properties = evaluation.properties
