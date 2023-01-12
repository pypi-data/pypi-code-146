import json

from .entities import *


class Workspace(object):
    def __init__(self, data):
        json_data = json.loads(data)

        self.bucket_id_map = self._bucket_id_map(json_data.get('buckets', []))
        self.experiment_key_map = self._experiment_key_map('AB_TEST', json_data.get('experiments', []))
        self.feature_flag_key_map = self._experiment_key_map('FEATURE_FLAG', json_data.get('featureFlags', []))
        self.event_type_key_map = self._event_type_key_map(json_data.get('events', []))
        self.segment_key_map = self._segment_key_map(json_data.get('segments', []))
        self._container_id_map = self._container_id_map(json_data.get('containers', []))
        self.parameter_configurations = self._parameter_configuration_id_map(
            json_data.get('parameterConfigurations', []))
        self.remote_config_parameters = self._remote_config_parameter_key_map(
            json_data.get('remoteConfigParameters', []))

    def get_experiment_or_none(self, experiment_key):
        return self.experiment_key_map.get(experiment_key)

    def get_feature_flag_or_none(self, feature_key):
        return self.feature_flag_key_map.get(feature_key)

    def get_bucket_or_none(self, bucket_id):
        return self.bucket_id_map.get(bucket_id)

    def get_event_type_or_none(self, event_key):
        return self.event_type_key_map.get(event_key)

    def get_segment_or_none(self, segment_key):
        return self.segment_key_map.get(segment_key)

    def get_container_or_none(self, container_id):
        return self._container_id_map.get(container_id)

    def get_parameter_configuration_or_none(self, parameter_configuration_id):
        return self.parameter_configurations.get(parameter_configuration_id)

    def get_remote_config_parameter_or_none(self, remote_config_parameter_key):
        return self.remote_config_parameters.get(remote_config_parameter_key)

    @staticmethod
    def _bucket_id_map(buckets_data):
        bucket_id_map = {}
        for bucket_data in buckets_data:
            slots = []

            for slot_data in bucket_data['slots']:
                slots.append(
                    Slot(
                        start_inclusive=slot_data['startInclusive'],
                        end_exclusive=slot_data['endExclusive'],
                        variation_id=slot_data['variationId']
                    )
                )

            bucket_id_map[bucket_data['id']] = Bucket(
                seed=bucket_data['seed'],
                slot_size=bucket_data['slotSize'],
                slots=slots
            )
        return bucket_id_map

    @staticmethod
    def _experiment_key_map(experiment_type, experiments_data):
        experiment_key_map = {}
        for experiment_data in experiments_data:
            experiment = Workspace._experiment(experiment_type, experiment_data)
            if experiment:
                experiment_key_map[experiment_data['key']] = experiment
        return experiment_key_map

    @staticmethod
    def _experiment(type, experiment_data):

        execution_data = experiment_data['execution']
        status = Workspace._experiment_status_or_none(execution_data['status'])
        if not status:
            return None

        variations = []
        for variation_data in experiment_data['variations']:
            variation = Variation(
                id=variation_data['id'],
                key=variation_data['key'],
                is_dropped=variation_data['status'] == 'DROPPED',
                parameter_configuration_id=variation_data.get('parameterConfigurationId')
            )
            variations.append(variation)

        user_overrides = {}
        for override_data in execution_data['userOverrides']:
            user_overrides[override_data['userId']] = override_data['variationId']

        return Experiment(
            id=experiment_data['id'],
            key=experiment_data['key'],
            type=type,
            identifier_type=experiment_data['identifierType'],
            status=status,
            version=experiment_data['version'],
            variations=variations,
            user_overrides=user_overrides,
            segment_overrides=Workspace._target_rules(execution_data.get('segmentOverrides', []),
                                                      TargetingTypes.IDENTIFIER),
            target_audiences=Workspace._targets(execution_data.get('targetAudiences', []), TargetingTypes.PROPERTY),
            target_rules=Workspace._target_rules(execution_data.get('targetRules', []), TargetingTypes.PROPERTY),
            default_rule=Workspace._target_action(execution_data['defaultRule']),
            container_id=experiment_data.get('containerId'),
            winner_variation_id=experiment_data.get('winnerVariationId')
        )

    @staticmethod
    def _experiment_status_or_none(execution_status):
        if execution_status == 'READY':
            return 'DRAFT'
        elif execution_status == 'RUNNING':
            return 'RUNNING'
        elif execution_status == 'PAUSED':
            return 'PAUSED'
        elif execution_status == 'STOPPED':
            return 'COMPLETED'
        else:
            return None

    @staticmethod
    def _target_or_none(target_data, targeting_type):
        conditions = []

        for condition_data in target_data['conditions']:
            condition = Workspace._condition_or_none(condition_data, targeting_type)
            if condition:
                conditions.append(condition)

        if not conditions:
            return None

        return Target(conditions)

    @staticmethod
    def _condition_or_none(condition_data, targeting_type):

        target_key = Workspace._target_key(condition_data['key'])

        if not targeting_type.supports(target_key.type):
            return None

        target_match = Workspace._target_match(condition_data['match'])

        return TargetCondition(
            key=target_key,
            match=target_match
        )

    @staticmethod
    def _target_key(target_key_data):
        return TargetKey(
            type=target_key_data['type'],
            name=target_key_data['name']
        )

    @staticmethod
    def _target_match(target_match_data):
        return TargetMatch(
            type=target_match_data['type'],
            operator=target_match_data['operator'],
            value_type=target_match_data['valueType'],
            values=target_match_data['values']
        )

    @staticmethod
    def _target_action(target_action_data):
        return TargetAction(
            type=target_action_data['type'],
            variation_id=target_action_data.get('variationId'),
            bucket_id=target_action_data.get('bucketId')
        )

    @staticmethod
    def _target_rule_or_none(target_rule_data, targeting_type):
        target = Workspace._target_or_none(target_rule_data['target'], targeting_type)
        if not target:
            return None

        action = Workspace._target_action(target_rule_data['action'])

        return TargetRule(
            target=target,
            action=action
        )

    @staticmethod
    def _targets(targets_data, targeting_type):
        targets = []
        for target_data in targets_data:
            target = Workspace._target_or_none(target_data, targeting_type)
            if not target:
                continue
            targets.append(target)
        return targets

    @staticmethod
    def _target_rules(target_rules_data, targeting_type):
        target_rules = []
        for target_rule_data in target_rules_data:
            target_rule = Workspace._target_rule_or_none(target_rule_data, targeting_type)
            if not target_rule:
                continue
            target_rules.append(target_rule)
        return target_rules

    @staticmethod
    def _event_type_key_map(event_types_data):
        event_type_key_map = {}
        for event_type_data in event_types_data:
            event_type_key_map[str(event_type_data['key'])] = EventType(event_type_data['id'],
                                                                        event_type_data['key'])
        return event_type_key_map

    @staticmethod
    def _segment_key_map(segments_data):
        _segment_key_map = {}
        for segment_data in segments_data:
            segment = Workspace._segment(segment_data)
            _segment_key_map[segment.key] = segment
        return _segment_key_map

    @staticmethod
    def _segment(segment_data):
        return Segment(
            id=segment_data['id'],
            key=segment_data['key'],
            type=segment_data['type'],
            targets=Workspace._targets(segment_data['targets'], TargetingTypes.SEGMENT)
        )

    @staticmethod
    def _container_id_map(containers_data):
        _container_id_map = {}
        for container_data in containers_data:
            container = Workspace._container(container_data)
            _container_id_map[container.id] = container
        return _container_id_map

    @staticmethod
    def _container(container_data):
        groups = []
        for container_group_data in container_data.get('groups', []):
            container_group = Workspace._container_group(container_group_data)
            groups.append(container_group)
        return Container(
            id=container_data['id'],
            bucket_id=container_data['bucketId'],
            groups=groups
        )

    @staticmethod
    def _container_group(container_group_data):
        return ContainerGroup(
            id=container_group_data['id'],
            experiments=container_group_data['experiments']
        )

    @staticmethod
    def _parameter_configuration_id_map(parameter_configurations_data):
        _parameter_configuration_id_map = {}
        for parameter_configuration_data in parameter_configurations_data:
            parameters = {}
            for parameter in parameter_configuration_data['parameters']:
                parameters[parameter['key']] = parameter['value']

            parameter_configuration = ParameterConfiguration(
                id=parameter_configuration_data['id'],
                parameters=parameters
            )
            _parameter_configuration_id_map[parameter_configuration.id] = parameter_configuration
        return _parameter_configuration_id_map

    @staticmethod
    def _remote_config_parameter_key_map(remote_config_parameters_data):
        _remote_config_parameter_key_map = {}
        for remote_config_parameter_data in remote_config_parameters_data:
            target_rules = []
            for target_rule_data in remote_config_parameter_data['targetRules']:
                target_rules.append(Workspace._remote_config_parameter_target_rule_or_none(target_rule_data, TargetingTypes.PROPERTY))

            default_value = Workspace._remote_config_parameter_value(remote_config_parameter_data['defaultValue'])

            remote_config_parameter = RemoteConfigParameter(
                id=remote_config_parameter_data['id'],
                key=remote_config_parameter_data['key'],
                type=remote_config_parameter_data['type'],
                identifier_type=remote_config_parameter_data['identifierType'],
                target_rules=target_rules,
                default_value=default_value
            )

            _remote_config_parameter_key_map[remote_config_parameter_data['key']] = remote_config_parameter
        return _remote_config_parameter_key_map

    @staticmethod
    def _remote_config_parameter_target_rule_or_none(target_rule_data, targeting_type):
        target = Workspace._target_or_none(target_rule_data['target'], targeting_type)
        if not target:
            return None

        return RemoteConfigTargetRule(
            key=target_rule_data['key'],
            name=target_rule_data['name'],
            target=target,
            bucket_id=target_rule_data['bucketId'],
            value=Workspace._remote_config_parameter_value(target_rule_data['value'])
        )

    @staticmethod
    def _remote_config_parameter_value(remote_config_parameter_value_data):
        return RemoteConfigParameterValue(
            id=remote_config_parameter_value_data['id'],
            raw_value=remote_config_parameter_value_data['value']
        )
