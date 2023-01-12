from jsonpath_ng import parse
from .paginate import autoscaling_paginate

#####################################

class describe_auto_scaling_groups(autoscaling_paginate):
    def name(self): return __class__.__name__        
    def jsonpath_expression(self): return parse('AutoScalingGroups[*]')

#####################################

class describe_policies(autoscaling_paginate):
    def name(self): return __class__.__name__        
    def jsonpath_expression(self): return parse('ScalingPolicies[*]')

#####################################
