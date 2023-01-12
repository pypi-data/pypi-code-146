from jsonpath_ng import parse
from .paginate import dms_paginate

#####################################

class describe_replication_instances(dms_paginate):
    def name(self): return __class__.__name__        
    def jsonpath_expression(self): return parse('ReplicationInstances[*]')

#####################################

class describe_replication_tasks(dms_paginate):
    def name(self): return __class__.__name__        
    def jsonpath_expression(self): return parse('ReplicationTasks[*]')

#####################################
