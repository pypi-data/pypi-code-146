from aws_recommendation_a12 import ec2 as fn
from boto3 import session

__author__ = "Dheeraj Banodha"
__version__ = '0.0.24'

class aws_client:
    def __init__(self, **kwargs):
        if 'aws_access_key_id' in kwargs.keys() and 'aws_secret_access_key' in kwargs.keys():
            self.session = session.Session(
                aws_access_key_id=kwargs['aws_access_key_id'],
                aws_secret_access_key=kwargs['aws_secret_access_key'],
            )
        elif 'profile_name' in kwargs.keys():
            self.session = session.Session(profile_name=kwargs['profile_name'])

    from .recommendation import get_recommendations

    from .ec2 import delete_or_downsize_instance_recommendation, purge_unattached_vol_recommendation, purge_8_weeks_older_snapshots, reserved_instance_lease_expiration, unassociated_elastic_ip_addresses, unused_ami

    from .rds import downsize_underutilized_rds_recommendation, rds_idle_db_instances, rds_general_purpose_ssd

    from .ebs import idle_ebs_volumes, ebs_general_purpose_ssd, gp2_to_gp3, unused_ebs_volume

    from .cost_estimations import estimated_savings

    from .s3 import enable_s3_bucket_keys, s3_bucket_versioning_enabled,s3_bucket_lifecycle_configuration, s3_bucket_lifecycle_configuration

    from .elb import idle_elastic_load_balancer, unused_elb

    from .cloudwatch import log_group_retention_period_check

    from .dynamodb import unused_dynamodb_tables

    from .kms import unused_cmk





