class RemoteConfigTargetRuleDeterminer(object):
    def __init__(self, target_matcher, bucketer):
        self.target_matcher = target_matcher
        self.bucketer = bucketer

    def determine_target_rule_or_none(self, workspace, remote_config_parameter, user):
        for rule in remote_config_parameter.target_rules:
            if self.matches(rule.target, rule.bucket_id, workspace, remote_config_parameter, user):
                return rule
        return None

    def matches(self, target_rule, bucket_id, workspace, remote_config_parameter, user):
        if not self.target_matcher.matches(target_rule, workspace, user):
            return False

        identifier = user.identifiers.get(remote_config_parameter.identifier_type)

        if identifier is None:
            return False

        bucket = workspace.get_bucket_or_none(bucket_id)
        if bucket is None:
            raise Exception('bucket[{}]'.format(bucket_id))

        slot = self.bucketer.bucketing(bucket, identifier)
        if slot is None:
            return False

        return True
