from .decision import RemoteConfigDecision, DecisionReason
from .commons import validator
from .model import HackleRemoteConfig


class HackleRemoteConfigImpl(HackleRemoteConfig):
    def __init__(self, user, internal_client, hackle_user_resolver):
        self.user = user
        self.internal_client = internal_client
        self.hackle_user_resolver = hackle_user_resolver

    def get(self, key, default=None):
        if validator.is_string(default):
            parameter_value = self.__get(key, 'STRING', default).value
        elif validator.is_number(default):
            parameter_value = self.__get(key, 'NUMBER', default).value
        elif validator.is_bool(default):
            parameter_value = self.__get(key, 'BOOLEAN', default).value
        elif default is None:
            parameter_value = self.__get(key, 'NULL', default).value
        else:
            parameter_value = self.__get(key, 'UNKNOWN', default).value

        return parameter_value

    def __get(self, key, required_type, default):
        hackle_user = self.hackle_user_resolver.resolve_or_none(self.user)

        if hackle_user is None:
            return RemoteConfigDecision(default, DecisionReason.INVALID_INPUT)

        if key is None:
            return RemoteConfigDecision(default, DecisionReason.INVALID_INPUT)

        return self.internal_client.remote_config(hackle_user, key, required_type, default)
