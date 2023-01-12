from boto3 import session
from cis_checks_test_3 import utils
from cis_checks_test_3.security_control_5 import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

__author__ = 'Dheeraj Banodha'
__version__ = '0.0.7'


class aws_client:
    def __init__(self, **kwargs):
        """
        @param str aws_access_key_id: AWS Access Key ID
        @param str aws_secret_access_key: AWS Secret Access Key
        """

        if 'aws_access_key_id' in kwargs.keys() and 'aws_secret_access_key' in kwargs.keys():
            self.session = session.Session(
                aws_access_key_id=kwargs['aws_access_key_id'],
                aws_secret_access_key=kwargs['aws_secret_access_key'],
            )
        elif 'profile_name' in kwargs.keys():
            self.session = session.Session(profile_name=kwargs['profile_name'])

    from .security_control_5 import control_5_1_cloudtrail_bucket_mfa_delete_enabled, \
        control_5_2_ensure_existing_iam_policies_attached_to_groups_and_roles, \
        control_5_3_ensure_access_keys_are_rotated_30_days, control_5_4_ensure_strict_password_policy, \
        control_5_5_publicly_accessible_cloudtrail_buckets, control_5_6_ebs_encrypted, control_5_7_default_security_group_unrestricted, control_5_8_elb_listener_security, control_5_10_rds_encryption_enabled, control_5_12_rds_publicly_accessible, control_5_13_redshift_cluster_publicly_accessible, control_5_14_publicly_shared_ami, control_5_15_unnecessary_ssh_public_keys, control_5_16_cloudfront_security_policy, control_5_17_redshift_parameter_group_require_ssl, control_5_18_ssh_public_keys_rotated_45_days, control_5_19_multi_mode_access, control_5_20_number_of_iam_groups

    from .iam_control_1 import control_1_1_root_use, control_1_2_mfa_on_password_enabled_iam, control_1_3_unused_credentials, control_1_4_rotated_keys, control_1_5_password_policy_uppercase, control_1_6_password_policy_lowercase, control_1_7_password_policy_symbol, control_1_8_password_policy_number, control_1_9_password_policy_length, control_1_10_password_policy_reuse, control_1_11_password_policy_expire, control_1_12_root_key_exists, control_1_13_root_mfa_enabled, control_1_14_root_hardware_mfa_enabled, control_1_15_security_questions_registered, control_1_16_no_policies_on_iam_users, control_1_17_detailed_billing_enabled, control_1_18_ensure_iam_master_and_manager_roles, control_1_19_maintain_current_contact_details, control_1_20_ensure_security_contact_details, control_1_21_ensure_iam_instance_roles_used, control_1_22_ensure_incident_management_roles, control_1_23_no_active_initial_access_keys_with_iam_user, control_1_24_no_overly_permissive_policies, control_1_25_require_mfa_to_delete_cloudtrail_buckets, control_1_26_dont_use_expired_ssl_tls_certificate

    from .logging_control_2 import control_2_1_ensure_cloud_trail_all_regions, control_2_2_ensure_cloudtrail_validation, control_2_3_ensure_cloudtrail_bucket_not_public, control_2_4_ensure_cloudtrail_cloudwatch_logs_integration, control_2_5_ensure_config_all_regions, control_2_6_ensure_cloudtrail_bucket_logging, control_2_7_ensure_cloudtrail_encryption_kms, control_2_8_ensure_kms_cmk_rotation

    from .monitoring_control_3 import control_3_1_ensure_log_metric_filter_unauthorized_api_calls, control_3_2_ensure_log_metric_filter_console_signin_no_mfa, control_3_3_ensure_log_metric_filter_root_usage, control_3_4_ensure_log_metric_iam_policy_change, control_3_5_ensure_log_metric_cloudtrail_configuration_changes, control_3_6_ensure_log_metric_console_auth_failures, control_3_7_ensure_log_metric_disabling_scheduled_delete_of_kms_cmk, control_3_8_ensure_log_metric_s3_bucket_policy_changes, control_3_9_ensure_log_metric_config_configuration_changes, control_3_10_ensure_log_metric_security_group_changes, control_3_11_ensure_log_metric_nacl, control_3_12_ensure_log_metric_changes_to_network_gateways, control_3_13_ensure_log_metric_changes_to_route_tables, control_3_14_ensure_log_metric_changes_to_vpc, control_3_15_verify_sns_subscribers, control_3_16_ensure_redshift_audit_logging_enabled, control_3_17_ensure_elb_access_logs_enabled

    from .networking_control_4 import control_4_1_ensure_ssh_not_open_to_world, control_4_2_ensure_rdp_not_open_to_world, control_4_2_ensure_20_not_open_to_world, control_4_2_ensure_21_not_open_to_world, control_4_2_ensure_3306_not_open_to_world, control_4_2_ensure_4333_not_open_to_world, control_4_3_ensure_flow_logs_enabled_on_all_vpc, control_4_4_ensure_default_security_groups_restricts_traffic, control_4_5_ensure_route_tables_are_least_access, control_4_6_ensure_sg_dont_have_large_range_of_ports_open, control_4_7_use_https_for_cloudfront_distribution

    from .utils import get_cloudtrails, get_regions, get_account_password_policy, get_cred_report, get_account_number

    # consolidate compliance.py details
    def get_compliance(self) -> list:
        """
        :return list: consolidated list  of compliance.py checks
        """
        logger.info(" ---Inside get_compliance()")

        regions = self.get_regions()
        cloudtrails = self.get_cloudtrails(regions)
        credsreport = self.get_cred_report()
        password_policy = self.get_account_password_policy()

        compliance = [
            self.control_1_1_root_use(credsreport),
            self.control_1_2_mfa_on_password_enabled_iam(credsreport),
            self.control_1_3_unused_credentials(credsreport),
            self.control_1_4_rotated_keys(credsreport),
            self.control_1_5_password_policy_uppercase(password_policy),
            self.control_1_6_password_policy_lowercase(password_policy),
            self.control_1_7_password_policy_symbol(password_policy),
            self.control_1_8_password_policy_number(password_policy),
            self.control_1_9_password_policy_length(password_policy),
            self.control_1_10_password_policy_reuse(password_policy),
            self.control_1_11_password_policy_expire(password_policy),
            self.control_1_12_root_key_exists(credsreport),
            self.control_1_13_root_mfa_enabled(),
            self.control_1_14_root_hardware_mfa_enabled(),
            self.control_1_15_security_questions_registered(),
            self.control_1_16_no_policies_on_iam_users(),
            self.control_1_17_detailed_billing_enabled(),
            self.control_1_18_ensure_iam_master_and_manager_roles(),
            self.control_1_19_maintain_current_contact_details(),
            self.control_1_20_ensure_security_contact_details(),
            self.control_1_21_ensure_iam_instance_roles_used(),
            self.control_1_22_ensure_incident_management_roles(),
            self.control_1_23_no_active_initial_access_keys_with_iam_user(credsreport),
            self.control_1_24_no_overly_permissive_policies(),
            # self.control_1_25_require_mfa_to_delete_cloudtrail_buckets(regions),
            # self.control_1_26_dont_use_expired_ssl_tls_certificate(regions),

            # self.control_2_1_ensure_cloud_trail_all_regions(cloudtrails),
            # self.control_2_2_ensure_cloudtrail_validation(cloudtrails),
            # self.control_2_3_ensure_cloudtrail_bucket_not_public(cloudtrails),
            # self.control_2_4_ensure_cloudtrail_cloudwatch_logs_integration(cloudtrails),
            # self.control_2_5_ensure_config_all_regions(regions),
            # self.control_2_6_ensure_cloudtrail_bucket_logging(cloudtrails),
            # self.control_2_7_ensure_cloudtrail_encryption_kms(cloudtrails),
            # self.control_2_8_ensure_kms_cmk_rotation(regions),
            #
            # self.control_3_1_ensure_log_metric_filter_unauthorized_api_calls(cloudtrails),
            # self.control_3_2_ensure_log_metric_filter_console_signin_no_mfa(cloudtrails),
            # self.control_3_3_ensure_log_metric_filter_root_usage(cloudtrails),
            # self.control_3_4_ensure_log_metric_iam_policy_change(cloudtrails),
            # self.control_3_5_ensure_log_metric_cloudtrail_configuration_changes(cloudtrails),
            # self.control_3_6_ensure_log_metric_console_auth_failures(cloudtrails),
            # self.control_3_7_ensure_log_metric_disabling_scheduled_delete_of_kms_cmk(cloudtrails),
            # self.control_3_8_ensure_log_metric_s3_bucket_policy_changes(cloudtrails),
            # self.control_3_9_ensure_log_metric_config_configuration_changes(cloudtrails),
            # self.control_3_10_ensure_log_metric_security_group_changes(cloudtrails),
            # self.control_3_11_ensure_log_metric_nacl(cloudtrails),
            # self.control_3_12_ensure_log_metric_changes_to_network_gateways(cloudtrails),
            # self.control_3_13_ensure_log_metric_changes_to_route_tables(cloudtrails),
            # self.control_3_14_ensure_log_metric_changes_to_vpc(cloudtrails),
            # self.control_3_15_verify_sns_subscribers(),
            # self.control_3_16_ensure_redshift_audit_logging_enabled(regions),
            # self.control_3_17_ensure_elb_access_logs_enabled(regions),
            #
            # self.control_4_1_ensure_ssh_not_open_to_world(regions),
            # self.control_4_2_ensure_4333_not_open_to_world(regions),
            # self.control_4_2_ensure_3306_not_open_to_world(regions),
            # self.control_4_2_ensure_21_not_open_to_world(regions),
            # self.control_4_2_ensure_20_not_open_to_world(regions),
            # self.control_4_2_ensure_rdp_not_open_to_world(regions),
            # self.control_4_3_ensure_flow_logs_enabled_on_all_vpc(regions),
            # self.control_4_4_ensure_default_security_groups_restricts_traffic(regions),
            # self.control_4_5_ensure_route_tables_are_least_access(regions),
            # self.control_4_6_ensure_sg_dont_have_large_range_of_ports_open(regions),
            # self.control_4_7_use_https_for_cloudfront_distribution(),
            #
            # self.control_5_1_cloudtrail_bucket_mfa_delete_enabled(cloudtrails),
            # self.control_5_2_ensure_existing_iam_policies_attached_to_groups_and_roles(),
            # self.control_5_3_ensure_access_keys_are_rotated_30_days(),
            # self.control_5_4_ensure_strict_password_policy(),
            # self.control_5_5_publicly_accessible_cloudtrail_buckets(cloudtrails),
            # self.control_5_6_ebs_encrypted(regions),
            # self.control_5_7_default_security_group_unrestricted(regions),
            # self.control_5_8_elb_listener_security(regions),
            # self.control_5_10_rds_encryption_enabled(regions),
            # self.control_5_12_rds_publicly_accessible(regions),
            # self.control_5_13_redshift_cluster_publicly_accessible(regions),
            # self.control_5_14_publicly_shared_ami(regions),
            # self.control_5_15_unnecessary_ssh_public_keys(),
            # self.control_5_16_cloudfront_security_policy(),
            # self.control_5_17_redshift_parameter_group_require_ssl(regions),
            # self.control_5_18_ssh_public_keys_rotated_45_days(),
            # self.control_5_19_multi_mode_access(),
            # self.control_5_20_number_of_iam_groups()
        ]

        return compliance
