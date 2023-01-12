class OverrideResolver(object):
    def __init__(self, target_matcher, action_resolver):
        self.target_matcher = target_matcher
        self.action_resolver = action_resolver

    def resolve_or_none(self, workspace, experiment, user):
        user_overridden_variation = self._resolve_user_override_or_none(experiment, user)
        if user_overridden_variation is not None:
            return user_overridden_variation

        return self._resolve_segment_override(workspace, experiment, user)

    def _resolve_user_override_or_none(self, experiment, user):
        identifier = user.identifiers.get(experiment.identifier_type)
        if identifier is None:
            return None

        overridden_variation_id = experiment.user_overrides.get(identifier)
        if overridden_variation_id is None:
            return None

        return experiment.get_variation_by_id_or_none(overridden_variation_id)

    def _resolve_segment_override(self, workspace, experiment, user):
        for overridden_rule in experiment.segment_overrides:
            if self.target_matcher.matches(overridden_rule.target, workspace, user):
                return self.action_resolver.resolve_or_none(overridden_rule.action, workspace, experiment, user)

        return None
