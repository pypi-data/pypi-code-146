import os
from log_control_ao import Logger

logger = Logger(domain='vpc-ao', local=True)
vpc_token = os.environ.get('VPC_TOKEN', 'test')
vpc_ip = 'vpc-control-test-svc.system-service.svc.cluster.local'
vpc_port = 8080
