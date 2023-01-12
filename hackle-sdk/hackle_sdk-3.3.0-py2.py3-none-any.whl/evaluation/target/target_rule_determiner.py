class TargetRuleDeterminer(object):
    def __init__(self, target_matcher):
        self.target_matcher = target_matcher

    def determine_target_rule_or_none(self, workspace, experiment, user):
        for rule in experiment.target_rules:
            if self.target_matcher.matches(rule.target, workspace, user):
                return rule

        return None
