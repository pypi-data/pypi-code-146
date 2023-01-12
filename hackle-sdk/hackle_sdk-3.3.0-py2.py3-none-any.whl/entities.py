class BaseEntity(object):
    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False


class Experiment(BaseEntity):

    def __init__(self, id, key, type, identifier_type, status, version, variations, user_overrides, segment_overrides,
                 target_audiences, target_rules, default_rule, container_id, winner_variation_id):
        self.id = id
        self.key = key
        self.type = type
        self.identifier_type = identifier_type
        self.status = status
        self.version = version
        self.variations = variations
        self.user_overrides = user_overrides
        self.segment_overrides = segment_overrides
        self.target_audiences = target_audiences
        self.target_rules = target_rules
        self.default_rule = default_rule
        self.container_id = container_id
        self.winner_variation = self.get_variation_by_id_or_none(winner_variation_id)

    def get_variation_by_id_or_none(self, variation_id):
        for variation in self.variations:
            if variation.id == variation_id:
                return variation
        return None

    def get_variation_by_key_or_none(self, variation_key):
        for variation in self.variations:
            if variation.key == variation_key:
                return variation
        return None


class Variation(BaseEntity):
    def __init__(self, id, key, is_dropped, parameter_configuration_id=None):
        self.id = id
        self.key = key
        self.is_dropped = is_dropped
        self.parameter_configuration_id = parameter_configuration_id


class Bucket(BaseEntity):
    def __init__(self, seed, slot_size, slots):
        self.seed = seed
        self.slot_size = slot_size
        self.slots = slots

    def get_slot_or_none(self, slot_number):
        for slot in self.slots:
            if slot.contains(slot_number):
                return slot
        return None


class Slot(BaseEntity):
    def __init__(self, start_inclusive, end_exclusive, variation_id):
        self.start_inclusive = start_inclusive
        self.end_exclusive = end_exclusive
        self.variation_id = variation_id

    def contains(self, slot_number):
        return (self.start_inclusive <= slot_number) and (slot_number < self.end_exclusive)


class EventType(BaseEntity):
    def __init__(self, id, key):
        self.id = id
        self.key = key


class Target(BaseEntity):
    def __init__(self, conditions):
        self.conditions = conditions


class TargetCondition(BaseEntity):
    def __init__(self, key, match):
        self.key = key
        self.match = match


class TargetKey(BaseEntity):
    def __init__(self, type, name):
        self.type = type
        self.name = name


class TargetMatch(BaseEntity):
    def __init__(self, type, operator, value_type, values):
        self.type = type
        self.operator = operator
        self.value_type = value_type
        self.values = values


class TargetAction(BaseEntity):
    def __init__(self, type, variation_id=None, bucket_id=None):
        self.type = type
        self.variation_id = variation_id
        self.bucket_id = bucket_id


class TargetRule(BaseEntity):
    def __init__(self, target, action):
        self.target = target
        self.action = action


class Segment(BaseEntity):
    def __init__(self, id, key, type, targets):
        self.id = id
        self.key = key
        self.type = type
        self.targets = targets


class TargetingType(object):

    def __init__(self, *supported_key_types):
        self.supported_key_types = supported_key_types

    def supports(self, target_key_type):
        return target_key_type in self.supported_key_types


class TargetingTypes(object):
    IDENTIFIER = TargetingType('SEGMENT')
    PROPERTY = TargetingType('SEGMENT', 'USER_PROPERTY', 'HACKLE_PROPERTY')
    SEGMENT = TargetingType('USER_ID', 'USER_PROPERTY', 'HACKLE_PROPERTY')


class Container(object):

    def __init__(self, id, bucket_id, groups):
        self.id = id
        self.bucket_id = bucket_id
        self.groups = groups

    def get_group_or_none(self, container_group_id):
        for group in self.groups:
            if group.id == container_group_id:
                return group
        return None


class ContainerGroup(object):
    def __init__(self, id, experiments):
        self.id = id
        self.experiments = experiments


class ParameterConfiguration(object):

    def __init__(self, id, parameters):
        self.id = id
        self.parameters = parameters

    def __str__(self):
        return 'ParameterConfiguration(id={}, parameters={})'.format(self.id, self.parameters)

    def get(self, key, default):
        parameter_value = self.parameters.get(key, default)
        if default is None:
            return parameter_value
        if type(parameter_value) != type(default):
            return default
        return parameter_value


class RemoteConfigParameter(object):

    def __init__(self, id, key, type, identifier_type, target_rules, default_value):
        self.id = id
        self.key = key
        self.type = type
        self.identifier_type = identifier_type
        self.target_rules = target_rules
        self.default_value = default_value

    def __str__(self):
        return 'RemoteConfigParameter(id={}, key={}, type={}, identifier_type={}, target_rules={}, default_value={})' \
            .format(self.id,
                    self.key,
                    self.type,
                    self.identifier_type,
                    self.target_rules,
                    self.default_value)


class RemoteConfigTargetRule(object):

    def __init__(self, key, name, target, bucket_id, value):
        self.key = key
        self.name = name
        self.target = target
        self.bucket_id = bucket_id
        self.value = value

    def __str__(self):
        return 'RemoteConfigTargetRule(key={}, name={}, target={}, bucket_id={}, value={})'.format(self.key,
                                                                                                   self.name,
                                                                                                   self.target,
                                                                                                   self.bucket_id,
                                                                                                   self.value)


class RemoteConfigParameterValue(object):
    def __init__(self, id, raw_value):
        self.id = id
        self.raw_value = raw_value

    def __str__(self):
        return 'RemoteConfigParameterValue(id={}, raw_value={})'.format(self.id, self.raw_value)
