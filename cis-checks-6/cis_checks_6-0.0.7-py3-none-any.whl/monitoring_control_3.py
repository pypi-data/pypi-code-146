"""
	monitoring_control_3.py
"""

import os, re, sys, time, logging, logging.config
from datetime import datetime

import boto3
import botocore.errorfactory
import botocore.exceptions
from botocore.exceptions import NoCredentialsError

global logger
logging.basicConfig(level=logging.INFO)

from cis_checks_6.utils import *

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# LOG_CONF_PATH = os.path.join( BASE_DIR,'..', 'logging.conf')
# LOG_FILE_PATH = os.path.join(BASE_DIR, '..', 'logs', 'cis_automation_'+ datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+ '.log')
# logging.config.fileConfig(LOG_CONF_PATH, defaults={'logfilename': LOG_FILE_PATH})
logger = logging.getLogger('simpleLogger')

# --- 3 Monitoring ---

# 3.1 Ensure a log metric filter and alarm exist for unauthorized API calls (Scored)
def control_3_1_ensure_log_metric_filter_unauthorized_api_calls(self, cloudtrails):
    logger.info(" ---Inside monitoring_control_3 :: control_3_1_ensure_log_metric_filter_unauthorized_api_calls()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = False
    failReason = ""
    offenders = []
    control = "3.1"
    description = "Ensure log metric filter unauthorized api calls"
    scored = True
    failReason = "Incorrect log metric alerts for unauthorized_api_calls"
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                try:
                    if o['CloudWatchLogsLogGroupArn']:
                        group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                        client = self.session.client('logs', region_name=m)
                        filters = client.describe_metric_filters(
                            logGroupName=group
                        )
                        for p in filters['metricFilters']:
                            patterns = ["\$\.errorCode\s*=\s*\"?\*UnauthorizedOperation(\"|\)|\s)", "\$\.errorCode\s*=\s*\"?AccessDenied\*(\"|\)|\s)"]
                            if find_in_string(patterns, str(p['filterPattern'])):
                                cwclient = self.session.client('cloudwatch', region_name=m)
                                response = cwclient.describe_alarms_for_metric(
                                    MetricName=p['metricTransformations'][0]['metricName'],
                                    Namespace=p['metricTransformations'][0]['metricNamespace']
                                )
                                snsClient = self.session.client('sns', region_name=m)
                                subscribers = snsClient.list_subscriptions_by_topic(
                                    TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                    #  Pagination not used since only 1 subscriber required
                                )
                                if not len(subscribers['Subscriptions']) == 0:
                                    result = True
                except:
                    pass
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored, 'Description': description, 'ControlId': control}


# 3.2 Ensure a log metric filter and alarm exist for Management Console sign-in without MFA (Scored)
def control_3_2_ensure_log_metric_filter_console_signin_no_mfa(self, cloudtrails):
    logger.info(" ---Inside monitoring_control_3 :: control_3_2_ensure_log_metric_filter_console_signin_no_mfa()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = False
    failReason = ""
    offenders = []
    control = "3.2"
    description = "Ensure a log metric filter and alarm exist for Management Console sign-in without MFA"
    scored = True
    failReason = "Incorrect log metric alerts for management console signin without MFA"
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                try:
                    if o['CloudWatchLogsLogGroupArn']:
                        group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                        client = self.session.client('logs', region_name=m)
                        filters = client.describe_metric_filters(
                            logGroupName=group
                        )
                        for p in filters['metricFilters']:
                            patterns = ["\$\.eventName\s*=\s*\"?ConsoleLogin(\"|\)|\s)", "\$\.additionalEventData\.MFAUsed\s*\!=\s*\"?Yes"]
                            if find_in_string(patterns, str(p['filterPattern'])):
                                cwclient = self.session.client('cloudwatch', region_name=m)
                                response = cwclient.describe_alarms_for_metric(
                                    MetricName=p['metricTransformations'][0]['metricName'],
                                    Namespace=p['metricTransformations'][0]['metricNamespace']
                                )
                                snsClient = self.session.client('sns', region_name=m)
                                subscribers = snsClient.list_subscriptions_by_topic(
                                    TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                    #  Pagination not used since only 1 subscriber required
                                )
                                if not len(subscribers['Subscriptions']) == 0:
                                    result = True
                except:
                    pass
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored, 'Description': description, 'ControlId': control}


# 3.3 Ensure a log metric filter and alarm exist for usage of "root" account (Scored)
def control_3_3_ensure_log_metric_filter_root_usage(self, cloudtrails):
    logger.info(" ---Inside monitoring_control_3 :: control_3_3_ensure_log_metric_filter_root_usage()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = False
    failReason = ""
    offenders = []
    control = "3.3"
    description = "Ensure a log metric filter and alarm exist for root usage"
    scored = True
    failReason = "Incorrect log metric alerts for root usage"
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                try:
                    if o['CloudWatchLogsLogGroupArn']:
                        group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                        client = self.session.client('logs', region_name=m)
                        filters = client.describe_metric_filters(
                            logGroupName=group
                        )
                        for p in filters['metricFilters']:
                            patterns = ["\$\.userIdentity\.type\s*=\s*\"?Root", "\$\.userIdentity\.invokedBy\s*NOT\s*EXISTS", "\$\.eventType\s*\!=\s*\"?AwsServiceEvent(\"|\)|\s)"]
                            if find_in_string(patterns, str(p['filterPattern'])):
                                cwclient = self.session.client('cloudwatch', region_name=m)
                                response = cwclient.describe_alarms_for_metric(
                                    MetricName=p['metricTransformations'][0]['metricName'],
                                    Namespace=p['metricTransformations'][0]['metricNamespace']
                                )
                                snsClient = self.session.client('sns', region_name=m)
                                subscribers = snsClient.list_subscriptions_by_topic(
                                    TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                    #  Pagination not used since only 1 subscriber required
                                )
                                if not len(subscribers['Subscriptions']) == 0:
                                    result = True
                except:
                    pass
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored, 'Description': description, 'ControlId': control}


# 3.4 Ensure a log metric filter and alarm exist for IAM policy changes  (Scored)
def control_3_4_ensure_log_metric_iam_policy_change(self, cloudtrails):
    logger.info(" ---Inside monitoring_control_3 :: control_3_4_ensure_log_metric_iam_policy_change()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = False
    failReason = ""
    offenders = []
    control = "3.4"
    description = "Ensure a log metric filter and alarm exist for IAM changes"
    scored = True
    failReason = "Incorrect log metric alerts for IAM policy changes"
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                try:
                    if o['CloudWatchLogsLogGroupArn']:
                        group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                        client = self.session.client('logs', region_name=m)
                        filters = client.describe_metric_filters(
                            logGroupName=group
                        )
                        for p in filters['metricFilters']:
                            patterns = ["\$\.eventName\s*=\s*\"?DeleteGroupPolicy(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeleteRolePolicy(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeleteUserPolicy(\"|\)|\s)", "\$\.eventName\s*=\s*\"?PutGroupPolicy(\"|\)|\s)", "\$\.eventName\s*=\s*\"?PutRolePolicy(\"|\)|\s)", "\$\.eventName\s*=\s*\"?PutUserPolicy(\"|\)|\s)", "\$\.eventName\s*=\s*\"?CreatePolicy(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeletePolicy(\"|\)|\s)", "\$\.eventName\s*=\s*\"?CreatePolicyVersion(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeletePolicyVersion(\"|\)|\s)", "\$\.eventName\s*=\s*\"?AttachRolePolicy(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DetachRolePolicy(\"|\)|\s)", "\$\.eventName\s*=\s*\"?AttachUserPolicy(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DetachUserPolicy(\"|\)|\s)", "\$\.eventName\s*=\s*\"?AttachGroupPolicy(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DetachGroupPolicy(\"|\)|\s)"]
                            if find_in_string(patterns, str(p['filterPattern'])):
                                cwclient = self.session.client('cloudwatch', region_name=m)
                                response = cwclient.describe_alarms_for_metric(
                                    MetricName=p['metricTransformations'][0]['metricName'],
                                    Namespace=p['metricTransformations'][0]['metricNamespace']
                                )
                                snsClient = self.session.client('sns', region_name=m)
                                subscribers = snsClient.list_subscriptions_by_topic(
                                    TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                    #  Pagination not used since only 1 subscriber required
                                )
                                if not len(subscribers['Subscriptions']) == 0:
                                    result = True
                except:
                    pass
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored, 'Description': description, 'ControlId': control}


# 3.5 Ensure a log metric filter and alarm exist for CloudTrail configuration changes (Scored)
def control_3_5_ensure_log_metric_cloudtrail_configuration_changes(self, cloudtrails):
    logger.info(" ---Inside monitoring_control_3 :: control_3_5_ensure_log_metric_cloudtrail_configuration_changes()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = False
    failReason = ""
    offenders = []
    control = "3.5"
    description = "Ensure a log metric filter and alarm exist for CloudTrail configuration changes"
    scored = True
    failReason = "Incorrect log metric alerts for CloudTrail configuration changes"
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                try:
                    if o['CloudWatchLogsLogGroupArn']:
                        group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                        client = self.session.client('logs', region_name=m)
                        filters = client.describe_metric_filters(
                            logGroupName=group
                        )
                        for p in filters['metricFilters']:
                            patterns = ["\$\.eventName\s*=\s*\"?CreateTrail(\"|\)|\s)", "\$\.eventName\s*=\s*\"?UpdateTrail(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeleteTrail(\"|\)|\s)", "\$\.eventName\s*=\s*\"?StartLogging(\"|\)|\s)", "\$\.eventName\s*=\s*\"?StopLogging(\"|\)|\s)"]
                            if find_in_string(patterns, str(p['filterPattern'])):
                                cwclient = self.session.client('cloudwatch', region_name=m)
                                response = cwclient.describe_alarms_for_metric(
                                    MetricName=p['metricTransformations'][0]['metricName'],
                                    Namespace=p['metricTransformations'][0]['metricNamespace']
                                )
                                snsClient = self.session.client('sns', region_name=m)
                                subscribers = snsClient.list_subscriptions_by_topic(
                                    TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                    #  Pagination not used since only 1 subscriber required
                                )
                                if not len(subscribers['Subscriptions']) == 0:
                                    result = True
                except:
                    pass
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored, 'Description': description, 'ControlId': control}


# 3.6 Ensure a log metric filter and alarm exist for AWS Management Console authentication failures (Scored)
def control_3_6_ensure_log_metric_console_auth_failures(self, cloudtrails):
    logger.info(" ---Inside monitoring_control_3 :: control_3_6_ensure_log_metric_console_auth_failures()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = False
    failReason = ""
    offenders = []
    control = "3.6"
    description = "Ensure a log metric filter and alarm exist for console auth failures"
    scored = True
    failReason = "Ensure a log metric filter and alarm exist for console auth failures"
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                try:
                    if o['CloudWatchLogsLogGroupArn']:
                        group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                        client = self.session.client('logs', region_name=m)
                        filters = client.describe_metric_filters(
                            logGroupName=group
                        )
                        for p in filters['metricFilters']:
                            patterns = ["\$\.eventName\s*=\s*\"?ConsoleLogin(\"|\)|\s)", "\$\.errorMessage\s*=\s*\"?Failed authentication(\"|\)|\s)"]
                            if find_in_string(patterns, str(p['filterPattern'])):
                                cwclient = self.session.client('cloudwatch', region_name=m)
                                response = cwclient.describe_alarms_for_metric(
                                    MetricName=p['metricTransformations'][0]['metricName'],
                                    Namespace=p['metricTransformations'][0]['metricNamespace']
                                )
                                snsClient = self.session.client('sns', region_name=m)
                                subscribers = snsClient.list_subscriptions_by_topic(
                                    TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                    #  Pagination not used since only 1 subscriber required
                                )
                                if not len(subscribers['Subscriptions']) == 0:
                                    result = True
                except:
                    pass
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored, 'Description': description, 'ControlId': control}


# 3.7 Ensure a log metric filter and alarm exist for disabling or scheduled deletion of customer created CMKs (Scored)
def control_3_7_ensure_log_metric_disabling_scheduled_delete_of_kms_cmk(self, cloudtrails):
    logger.info(" ---Inside monitoring_control_3 :: control_3_7_ensure_log_metric_disabling_scheduled_delete_of_kms_cmk()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = False
    failReason = ""
    offenders = []
    control = "3.7"
    description = "Ensure a log metric filter and alarm exist for disabling or scheduling deletion of KMS CMK"
    scored = True
    failReason = "Ensure a log metric filter and alarm exist for disabling or scheduling deletion of KMS CMK"
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                try:
                    if o['CloudWatchLogsLogGroupArn']:
                        group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                        client = self.session.client('logs', region_name=m)
                        filters = client.describe_metric_filters(
                            logGroupName=group
                        )
                        for p in filters['metricFilters']:
                            patterns = ["\$\.eventSource\s*=\s*\"?kms\.amazonaws\.com(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DisableKey(\"|\)|\s)", "\$\.eventName\s*=\s*\"?ScheduleKeyDeletion(\"|\)|\s)"]
                            if find_in_string(patterns, str(p['filterPattern'])):
                                cwclient = self.session.client('cloudwatch', region_name=m)
                                response = cwclient.describe_alarms_for_metric(
                                    MetricName=p['metricTransformations'][0]['metricName'],
                                    Namespace=p['metricTransformations'][0]['metricNamespace']
                                )
                                snsClient = self.session.client('sns', region_name=m)
                                subscribers = snsClient.list_subscriptions_by_topic(
                                    TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                    #  Pagination not used since only 1 subscriber required
                                )
                                if not len(subscribers['Subscriptions']) == 0:
                                    result = True
                except:
                    pass
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored, 'Description': description, 'ControlId': control}


# 3.8 Ensure a log metric filter and alarm exist for S3 bucket policy changes (Scored)
def control_3_8_ensure_log_metric_s3_bucket_policy_changes(self, cloudtrails):
    logger.info(" ---Inside monitoring_control_3 :: control_3_8_ensure_log_metric_s3_bucket_policy_changes()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = False
    failReason = ""
    offenders = []
    control = "3.8"
    description = "Ensure a log metric filter and alarm exist for S3 bucket policy changes"
    scored = True
    failReason = "Ensure a log metric filter and alarm exist for S3 bucket policy changes"
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                try:
                    if o['CloudWatchLogsLogGroupArn']:
                        group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                        client = self.session.client('logs', region_name=m)
                        filters = client.describe_metric_filters(
                            logGroupName=group
                        )
                        for p in filters['metricFilters']:
                            patterns = ["\$\.eventSource\s*=\s*\"?s3\.amazonaws\.com(\"|\)|\s)", "\$\.eventName\s*=\s*\"?PutBucketAcl(\"|\)|\s)", "\$\.eventName\s*=\s*\"?PutBucketPolicy(\"|\)|\s)", "\$\.eventName\s*=\s*\"?PutBucketCors(\"|\)|\s)", "\$\.eventName\s*=\s*\"?PutBucketLifecycle(\"|\)|\s)", "\$\.eventName\s*=\s*\"?PutBucketReplication(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeleteBucketPolicy(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeleteBucketCors(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeleteBucketLifecycle(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeleteBucketReplication(\"|\)|\s)"]
                            if find_in_string(patterns, str(p['filterPattern'])):
                                cwclient = self.session.client('cloudwatch', region_name=m)
                                response = cwclient.describe_alarms_for_metric(
                                    MetricName=p['metricTransformations'][0]['metricName'],
                                    Namespace=p['metricTransformations'][0]['metricNamespace']
                                )
                                snsClient = self.session.client('sns', region_name=m)
                                subscribers = snsClient.list_subscriptions_by_topic(
                                    TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                    #  Pagination not used since only 1 subscriber required
                                )
                                if not len(subscribers['Subscriptions']) == 0:
                                    result = True
                except:
                    pass
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored, 'Description': description, 'ControlId': control}


# 3.9 Ensure a log metric filter and alarm exist for AWS Config configuration changes (Scored)
def control_3_9_ensure_log_metric_config_configuration_changes(self, cloudtrails):
    logger.info(" ---Inside monitoring_control_3 :: control_3_9_ensure_log_metric_config_configuration_changes()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = False
    failReason = ""
    offenders = []
    control = "3.9"
    description = "Ensure a log metric filter and alarm exist for for AWS Config configuration changes"
    scored = True
    failReason = "Ensure a log metric filter and alarm exist for for AWS Config configuration changes"
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                try:
                    if o['CloudWatchLogsLogGroupArn']:
                        group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                        client = self.session.client('logs', region_name=m)
                        filters = client.describe_metric_filters(
                            logGroupName=group
                        )
                        for p in filters['metricFilters']:
                            patterns = ["\$\.eventSource\s*=\s*\"?config\.amazonaws\.com(\"|\)|\s)", "\$\.eventName\s*=\s*\"?StopConfigurationRecorder(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeleteDeliveryChannel(\"|\)|\s)", "\$\.eventName\s*=\s*\"?PutDeliveryChannel(\"|\)|\s)", "\$\.eventName\s*=\s*\"?PutConfigurationRecorder(\"|\)|\s)"]
                            if find_in_string(patterns, str(p['filterPattern'])):
                                cwclient = self.session.client('cloudwatch', region_name=m)
                                response = cwclient.describe_alarms_for_metric(
                                    MetricName=p['metricTransformations'][0]['metricName'],
                                    Namespace=p['metricTransformations'][0]['metricNamespace']
                                )
                                snsClient = self.session.client('sns', region_name=m)
                                subscribers = snsClient.list_subscriptions_by_topic(
                                    TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                    #  Pagination not used since only 1 subscriber required
                                )
                                if not len(subscribers['Subscriptions']) == 0:
                                    result = True
                except:
                    pass
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored, 'Description': description, 'ControlId': control}


# 3.10 Ensure a log metric filter and alarm exist for security group changes (Scored)
def control_3_10_ensure_log_metric_security_group_changes(self, cloudtrails):
    logger.info(" ---Inside monitoring_control_3 :: control_3_10_ensure_log_metric_security_group_changes()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = False
    failReason = ""
    offenders = []
    control = "3.10"
    description = "Ensure a log metric filter and alarm exist for security group changes"
    scored = True
    failReason = "Ensure a log metric filter and alarm exist for security group changes"
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                try:
                    if o['CloudWatchLogsLogGroupArn']:
                        group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                        client = self.session.client('logs', region_name=m)
                        filters = client.describe_metric_filters(
                            logGroupName=group
                        )
                        for p in filters['metricFilters']:
                            patterns = ["\$\.eventName\s*=\s*\"?AuthorizeSecurityGroupIngress(\"|\)|\s)", "\$\.eventName\s*=\s*\"?AuthorizeSecurityGroupEgress(\"|\)|\s)", "\$\.eventName\s*=\s*\"?RevokeSecurityGroupIngress(\"|\)|\s)", "\$\.eventName\s*=\s*\"?RevokeSecurityGroupEgress(\"|\)|\s)", "\$\.eventName\s*=\s*\"?CreateSecurityGroup(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeleteSecurityGroup(\"|\)|\s)"]
                            if find_in_string(patterns, str(p['filterPattern'])):
                                cwclient = self.session.client('cloudwatch', region_name=m)
                                response = cwclient.describe_alarms_for_metric(
                                    MetricName=p['metricTransformations'][0]['metricName'],
                                    Namespace=p['metricTransformations'][0]['metricNamespace']
                                )
                                snsClient = self.session.client('sns', region_name=m)
                                subscribers = snsClient.list_subscriptions_by_topic(
                                    TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                    #  Pagination not used since only 1 subscriber required
                                )
                                if not len(subscribers['Subscriptions']) == 0:
                                    result = True
                except:
                    pass
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored, 'Description': description, 'ControlId': control}


# 3.11 Ensure a log metric filter and alarm exist for changes to Network Access Control Lists (NACL) (Scored)
def control_3_11_ensure_log_metric_nacl(self, cloudtrails):
    logger.info(" ---Inside monitoring_control_3 :: control_3_11_ensure_log_metric_nacl()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = False
    failReason = ""
    offenders = []
    control = "3.11"
    description = "Ensure a log metric filter and alarm exist for changes to Network Access Control Lists (NACL)"
    scored = True
    failReason = "Ensure a log metric filter and alarm exist for changes to Network Access Control Lists (NACL)"
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                try:
                    if o['CloudWatchLogsLogGroupArn']:
                        group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                        client = self.session.client('logs', region_name=m)
                        filters = client.describe_metric_filters(
                            logGroupName=group
                        )
                        for p in filters['metricFilters']:
                            patterns = ["\$\.eventName\s*=\s*\"?CreateNetworkAcl(\"|\)|\s)", "\$\.eventName\s*=\s*\"?CreateNetworkAclEntry(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeleteNetworkAcl(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeleteNetworkAclEntry(\"|\)|\s)", "\$\.eventName\s*=\s*\"?ReplaceNetworkAclEntry(\"|\)|\s)", "\$\.eventName\s*=\s*\"?ReplaceNetworkAclAssociation(\"|\)|\s)"]
                            if find_in_string(patterns, str(p['filterPattern'])):
                                cwclient = self.session.client('cloudwatch', region_name=m)
                                response = cwclient.describe_alarms_for_metric(
                                    MetricName=p['metricTransformations'][0]['metricName'],
                                    Namespace=p['metricTransformations'][0]['metricNamespace']
                                )
                                snsClient = self.session.client('sns', region_name=m)
                                subscribers = snsClient.list_subscriptions_by_topic(
                                    TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                    #  Pagination not used since only 1 subscriber required
                                )
                                if not len(subscribers['Subscriptions']) == 0:
                                    result = True
                except:
                    pass
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored, 'Description': description, 'ControlId': control}


# 3.12 Ensure a log metric filter and alarm exist for changes to network gateways (Scored)
def control_3_12_ensure_log_metric_changes_to_network_gateways(self, cloudtrails):
    logger.info(" ---Inside monitoring_control_3 :: control_3_12_ensure_log_metric_changes_to_network_gateways()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = False
    failReason = ""
    offenders = []
    control = "3.12"
    description = "Ensure a log metric filter and alarm exist for changes to network gateways"
    scored = True
    failReason = "Ensure a log metric filter and alarm exist for changes to network gateways"
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                try:
                    if o['CloudWatchLogsLogGroupArn']:
                        group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                        client = self.session.client('logs', region_name=m)
                        filters = client.describe_metric_filters(
                            logGroupName=group
                        )
                        for p in filters['metricFilters']:
                            patterns = ["\$\.eventName\s*=\s*\"?CreateCustomerGateway(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeleteCustomerGateway(\"|\)|\s)", "\$\.eventName\s*=\s*\"?AttachInternetGateway(\"|\)|\s)", "\$\.eventName\s*=\s*\"?CreateInternetGateway(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeleteInternetGateway(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DetachInternetGateway(\"|\)|\s)"]
                            if find_in_string(patterns, str(p['filterPattern'])):
                                cwclient = self.session.client('cloudwatch', region_name=m)
                                response = cwclient.describe_alarms_for_metric(
                                    MetricName=p['metricTransformations'][0]['metricName'],
                                    Namespace=p['metricTransformations'][0]['metricNamespace']
                                )
                                snsClient = self.session.client('sns', region_name=m)
                                subscribers = snsClient.list_subscriptions_by_topic(
                                    TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                    #  Pagination not used since only 1 subscriber required
                                )
                                if not len(subscribers['Subscriptions']) == 0:
                                    result = True
                except:
                    pass
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored, 'Description': description, 'ControlId': control}


# 3.13 Ensure a log metric filter and alarm exist for route table changes (Scored)
def control_3_13_ensure_log_metric_changes_to_route_tables(self, cloudtrails):
    logger.info(" ---Inside monitoring_control_3 :: control_3_13_ensure_log_metric_changes_to_route_tables()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = False
    failReason = ""
    offenders = []
    control = "3.13"
    description = "Ensure a log metric filter and alarm exist for route table changes"
    scored = True
    failReason = "Ensure a log metric filter and alarm exist for route table changes"
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                try:
                    if o['CloudWatchLogsLogGroupArn']:
                        group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                        client = self.session.client('logs', region_name=m)
                        filters = client.describe_metric_filters(
                            logGroupName=group
                        )
                        for p in filters['metricFilters']:
                            patterns = ["\$\.eventName\s*=\s*\"?CreateRoute(\"|\)|\s)", "\$\.eventName\s*=\s*\"?CreateRouteTable(\"|\)|\s)", "\$\.eventName\s*=\s*\"?ReplaceRoute(\"|\)|\s)", "\$\.eventName\s*=\s*\"?ReplaceRouteTableAssociation(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeleteRouteTable(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeleteRoute(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DisassociateRouteTable(\"|\)|\s)"]
                            if find_in_string(patterns, str(p['filterPattern'])):
                                cwclient = self.session.client('cloudwatch', region_name=m)
                                response = cwclient.describe_alarms_for_metric(
                                    MetricName=p['metricTransformations'][0]['metricName'],
                                    Namespace=p['metricTransformations'][0]['metricNamespace']
                                )
                                snsClient = self.session.client('sns', region_name=m)
                                subscribers = snsClient.list_subscriptions_by_topic(
                                    TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                    #  Pagination not used since only 1 subscriber required
                                )
                                if not len(subscribers['Subscriptions']) == 0:
                                    result = True
                except:
                    pass
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored, 'Description': description, 'ControlId': control}


# 3.14 Ensure a log metric filter and alarm exist for VPC changes (Scored)
def control_3_14_ensure_log_metric_changes_to_vpc(self, cloudtrails):
    logger.info(" ---Inside monitoring_control_3 :: control_3_14_ensure_log_metric_changes_to_vpc()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = False
    failReason = ""
    offenders = []
    control = "3.14"
    description = "Ensure a log metric filter and alarm exist for VPC changes"
    scored = True
    failReason = "Ensure a log metric filter and alarm exist for VPC changes"
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                try:
                    if o['CloudWatchLogsLogGroupArn']:
                        group = re.search('log-group:(.+?):', o['CloudWatchLogsLogGroupArn']).group(1)
                        client = self.session.client('logs', region_name=m)
                        filters = client.describe_metric_filters(
                            logGroupName=group
                        )
                        for p in filters['metricFilters']:
                            patterns = ["\$\.eventName\s*=\s*\"?CreateVpc(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeleteVpc(\"|\)|\s)", "\$\.eventName\s*=\s*\"?ModifyVpcAttribute(\"|\)|\s)", "\$\.eventName\s*=\s*\"?AcceptVpcPeeringConnection(\"|\)|\s)", "\$\.eventName\s*=\s*\"?CreateVpcPeeringConnection(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DeleteVpcPeeringConnection(\"|\)|\s)", "\$\.eventName\s*=\s*\"?RejectVpcPeeringConnection(\"|\)|\s)", "\$\.eventName\s*=\s*\"?AttachClassicLinkVpc(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DetachClassicLinkVpc(\"|\)|\s)", "\$\.eventName\s*=\s*\"?DisableVpcClassicLink(\"|\)|\s)", "\$\.eventName\s*=\s*\"?EnableVpcClassicLink(\"|\)|\s)"]
                            if find_in_string(patterns, str(p['filterPattern'])):
                                cwclient = self.session.client('cloudwatch', region_name=m)
                                response = cwclient.describe_alarms_for_metric(
                                    MetricName=p['metricTransformations'][0]['metricName'],
                                    Namespace=p['metricTransformations'][0]['metricNamespace']
                                )
                                snsClient = self.session.client('sns', region_name=m)
                                subscribers = snsClient.list_subscriptions_by_topic(
                                    TopicArn=response['MetricAlarms'][0]['AlarmActions'][0]
                                    #  Pagination not used since only 1 subscriber required
                                )
                                if not len(subscribers['Subscriptions']) == 0:
                                    result = True
                except:
                    pass
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored, 'Description': description, 'ControlId': control}


# 3.15 Ensure appropriate subscribers to each SNS topic (Not Scored)
def control_3_15_verify_sns_subscribers(self, ):
    logger.info(" ---Inside monitoring_control_3 :: control_3_15_verify_sns_subscribers()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Manual"
    failReason = ""
    offenders = []
    control = "3.15"
    description = "Ensure appropriate subscribers to each SNS topic, please verify manually"
    scored = False
    failReason = "Control not implemented using API, please verify manually"
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored, 'Description': description, 'ControlId': control}


# 3.16 Ensure redshift audit logging is enabled
def control_3_16_ensure_redshift_audit_logging_enabled(self, regions: list) -> dict:
    logger.info(" ---Inside monitoring_control_3 :: control_3_16_ensure_redshift_audit_logging_enabled")

    """Summary
    
    Returns:
        TYPE: dict
    """
    result = True
    failReason = ""
    offenders = []
    control = "3.16"
    description = "Ensure audit logging is enabled in all redshift clusters"
    scored = True
    for n in regions:
        clusters = list_redshift_clusters(self, n)
        client = self.session.client('redshift', region_name=n)

        for cluster in clusters:
            response = client.describe_logging_status(
                ClusterIdentifier=cluster
            )
            if not response['AccessLog']['Enabled']:
                result = False
                failReason = "Found Redshift cluster with audit logging disabled"
                offenders.append(cluster)

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# 3.17 Ensure ELB access logs are enabled
def control_3_17_ensure_elb_access_logs_enabled(self, regions: list) -> dict:
    logger.info(" ---Inside monitoring_control_3 :: control_3_17_ensure_elb_access_logging_enabled")

    """Summary
    
    Returns:
        TYPE: dict
    """
    result = True
    failReason = ""
    offenders = []
    control = "3.17"
    description = "Ensure access logging is enabled in all load balancers"
    scored = True
    for n in regions:
        elb_lst = list_elb(self, n)
        client = self.session.client('elb', region_name=n)

        for elb in elb_lst:
            response = client.describe_load_balancer_attributes(
                LoadBalancerName=elb
            )
            try:
                if not response['AccessLog']['Enabled']:
                    result = False
                    failReason = "Found load balancer with access logging disabled"
                    offenders.append(elb)
            except KeyError:
                result = False
                failReason = "Found load balancer with access logging disabled"
                offenders.append(elb)
    
    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }
