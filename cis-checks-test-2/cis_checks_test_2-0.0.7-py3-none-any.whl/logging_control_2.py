"""
	logging_control_2.py
"""

import os, re, sys, time, logging, logging.config
from datetime import datetime

import boto3
import botocore.errorfactory
import botocore.exceptions
from botocore.exceptions import NoCredentialsError

global logger
logging.basicConfig(level=logging.INFO)

from cis_checks_test_2.utils import *

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# LOG_CONF_PATH = os.path.join( BASE_DIR,'..', 'logging.conf')
# LOG_FILE_PATH = os.path.join(BASE_DIR, '..', 'logs', 'cis_automation_'+ datetime.now().strftime('%Y-%m-%d_%H-%M-%S')+ '.log')
# logging.config.fileConfig(LOG_CONF_PATH, defaults={'logfilename': LOG_FILE_PATH})
logger = logging.getLogger('simpleLogger')


# --- 2 Logging ---

# 2.1 Ensure CloudTrail is enabled in all regions (Scored)
def control_2_1_ensure_cloud_trail_all_regions(self, cloudtrails):
    logger.info(" ---Inside logging_control_2 :: control_2_1_ensure_cloud_trail_all_regions()--- ")
    """Summary

    Args:
        cloudtrails (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = False
    failReason = ""
    offenders = []
    control = "2.1"
    description = "Ensure CloudTrail is enabled in all regions"
    scored = True
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                if o['IsMultiRegionTrail']:
                    client = self.session.client('cloudtrail', region_name=m)
                    response = client.get_trail_status(
                        Name=o['TrailARN']
                    )
                    if response['IsLogging'] is True:
                        result = True
                        break
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")

    if result is False:
        failReason = "No enabled multi region trails found"
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 2.2 Ensure CloudTrail log file validation is enabled (Scored)
def control_2_2_ensure_cloudtrail_validation(self, cloudtrails):
    logger.info(" ---Inside logging_control_2 :: control_2_2_ensure_cloudtrail_validation()--- ")
    """Summary

    Args:
        cloudtrails (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "2.2"
    description = "Ensure CloudTrail log file validation is enabled"
    scored = True
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                if o['LogFileValidationEnabled'] is False:
                    result = False
                    failReason = "CloudTrails without log file validation discovered"
                    offenders.append(str(o['TrailARN']))
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")

    offenders = set(offenders)
    offenders = list(offenders)
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 2.3 Ensure the S3 bucket CloudTrail logs to is not publicly accessible (Scored)
def control_2_3_ensure_cloudtrail_bucket_not_public(self, cloudtrails):
    logger.info(" ---Inside logging_control_2 :: control_2_3_ensure_cloudtrail_bucket_not_public()--- ")
    """Summary

    Args:
        cloudtrails (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "2.3"
    description = "Ensure the S3 bucket CloudTrail logs to is not publicly accessible"
    scored = True
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                #  We only want to check cases where there is a bucket
                if "S3BucketName" in str(o):
                    try:
                        response = S3_CLIENT.get_bucket_acl(Bucket=o['S3BucketName'])
                        for p in response['Grants']:
                            # logger.info("Grantee is " + str(p['Grantee']))
                            if re.search(r'(global/AllUsers|global/AuthenticatedUsers)', str(p['Grantee'])):
                                result = False
                                offenders.append(str(o['TrailARN']) + ":PublicBucket")
                                if "Publically" not in failReason:
                                    failReason = failReason + "Publically accessible CloudTrail bucket discovered."
                    except Exception as e:
                        result = False
                        if "AccessDenied" in str(e):
                            offenders.append(str(o['TrailARN']) + ":AccessDenied")
                            if "Missing" not in failReason:
                                failReason = "Missing permissions to verify bucket ACL. " + failReason
                        elif "NoSuchBucket" in str(e):
                            offenders.append(str(o['TrailARN']) + ":NoBucket")
                            if "Trailbucket" not in failReason:
                                failReason = "Trailbucket doesn't exist. " + failReason
                        else:
                            offenders.append(str(o['TrailARN']) + ":CannotVerify")
                            if "Cannot" not in failReason:
                                failReason = "Cannot verify bucket ACL. " + failReason
                else:
                    result = False
                    offenders.append(str(o['TrailARN']) + "NoS3Logging")
                    failReason = "Cloudtrail not configured to log to S3. " + failReason
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")

    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 2.4 Ensure CloudTrail trails are integrated with CloudWatch Logs (Scored)
def control_2_4_ensure_cloudtrail_cloudwatch_logs_integration(self, cloudtrails):
    logger.info(" ---Inside logging_control_2 :: control_2_4_ensure_cloudtrail_cloudwatch_logs_integration()--- ")
    """Summary

    Args:
        cloudtrails (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "2.4"
    description = "Ensure CloudTrail trails are integrated with CloudWatch Logs"
    scored = True
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                try:
                    if "arn:aws:logs" in o['CloudWatchLogsLogGroupArn']:
                        pass
                    else:
                        result = False
                        failReason = "CloudTrails without CloudWatch Logs discovered"
                        offenders.append(str(o['TrailARN']))
                except:
                    result = False
                    failReason = "CloudTrails without CloudWatch Logs discovered"
                    offenders.append(str(o['TrailARN']))
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")

    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 2.5 Ensure AWS Config is enabled in all regions (Scored)
def control_2_5_ensure_config_all_regions(self, regions):
    logger.info(" ---Inside logging_control_2 :: control_2_5_ensure_config_all_regions()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "2.5"
    description = "Ensure AWS Config is enabled in all regions"
    scored = True
    globalConfigCapture = False  # Only one region needs to capture global events
    try:
        for n in regions:
            configClient = self.session.client('config', region_name=n)
            response = configClient.describe_configuration_recorder_status()
            # Get recording status
            try:
                if not response['ConfigurationRecordersStatus'][0]['recording'] is True:
                    result = False
                    failReason = "Config not enabled in all regions, not capturing all/global events or delivery channel errors"
                    offenders.append(str(n) + ":NotRecording")
            except:
                result = False
                failReason = "Config not enabled in all regions, not capturing all/global events or delivery channel errors"
                offenders.append(str(n) + ":NotRecording")

            # Verify that each region is capturing all events
            response = configClient.describe_configuration_recorders()
            try:
                if not response['ConfigurationRecorders'][0]['recordingGroup']['allSupported'] is True:
                    result = False
                    failReason = "Config not enabled in all regions, not capturing all/global events or delivery channel errors"
                    offenders.append(str(n) + ":NotAllEvents")
            except:
                pass  # This indicates that Config is disabled in the region and will be captured above.

            # Check if region is capturing global events. Fail is verified later since only one region needs to capture them.
            try:
                if response['ConfigurationRecorders'][0]['recordingGroup']['includeGlobalResourceTypes'] is True:
                    globalConfigCapture = True
            except:
                pass

            # Verify the delivery channels
            response = configClient.describe_delivery_channel_status()
            try:
                if response['DeliveryChannelsStatus'][0]['configHistoryDeliveryInfo']['lastStatus'] != "SUCCESS":
                    result = False
                    failReason = "Config not enabled in all regions, not capturing all/global events or delivery channel errors"
                    offenders.append(str(n) + ":S3orSNSDelivery")
            except:
                pass  # Will be captured by earlier rule
            try:
                if response['DeliveryChannelsStatus'][0]['configStreamDeliveryInfo']['lastStatus'] != "SUCCESS":
                    result = False
                    failReason = "Config not enabled in all regions, not capturing all/global events or delivery channel errors"
                    offenders.append(str(n) + ":SNSDelivery")
            except:
                pass  # Will be captured by earlier rule
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")

    # Verify that global events is captured by any region
    if globalConfigCapture is False:
        result = False
        failReason = "Config not enabled in all regions, not capturing all/global events or delivery channel errors"
        offenders.append("Global:NotRecording")
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 2.6 Ensure S3 bucket access logging is enabled on the CloudTrail S3 bucket (Scored)
def control_2_6_ensure_cloudtrail_bucket_logging(self, cloudtrails):
    logger.info(" ---Inside logging_control_2 :: control_2_6_ensure_cloudtrail_bucket_logging()--- ")
    """Summary

    Args:
        cloudtrails (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "2.6"
    description = "Ensure S3 bucket access logging is enabled on the CloudTrail S3 bucket"
    scored = True
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                # it is possible to have a cloudtrail configured with a nonexistant bucket
                try:
                    response = S3_CLIENT.get_bucket_logging(Bucket=o['S3BucketName'])
                except:
                    result = False
                    failReason = "Cloudtrail not configured to log to S3. "
                    offenders.append(str(o['TrailARN']))
                try:
                    if response['LoggingEnabled']:
                        pass
                except:
                    result = False
                    failReason = failReason + "CloudTrail S3 bucket without logging discovered"
                    offenders.append("Trail:" + str(o['TrailARN']) + " - S3Bucket:" + str(o['S3BucketName']))
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")

    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 2.7 Ensure CloudTrail logs are encrypted at rest using KMS CMKs (Scored)
def control_2_7_ensure_cloudtrail_encryption_kms(self, cloudtrails):
    logger.info(" ---Inside logging_control_2 :: control_2_7_ensure_cloudtrail_encryption_kms()--- ")
    """Summary

    Args:
        cloudtrails (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "2.7"
    description = "Ensure CloudTrail logs are encrypted at rest using KMS CMKs"
    scored = True
    try:
        for m, n in cloudtrails.iteritems():
            for o in n:
                try:
                    if o['KmsKeyId']:
                        pass
                except:
                    result = False
                    failReason = "CloudTrail not using KMS CMK for encryption discovered"
                    offenders.append("Trail:" + str(o['TrailARN']))
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")

    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 2.8 Ensure rotation for customer created CMKs is enabled (Scored)
def control_2_8_ensure_kms_cmk_rotation(self, regions):
    logger.info(" ---Inside logging_control_2 :: control_2_8_ensure_kms_cmk_rotation()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "2.8"
    description = "Ensure rotation for customer created CMKs is enabled"
    scored = True
    try:
        for n in regions:
            kms_client = self.session.client('kms', region_name=n)
            paginator = kms_client.get_paginator('list_keys')
            response_iterator = paginator.paginate()
            for page in response_iterator:
                for n in page['Keys']:
                    try:
                        rotationStatus = kms_client.get_key_rotation_status(KeyId=n['KeyId'])
                        if rotationStatus['KeyRotationEnabled'] is False:
                            keyDescription = kms_client.describe_key(KeyId=n['KeyId'])
                            if "Default master key that protects my" not in str(
                                    keyDescription['KeyMetadata']['Description']):  # Ignore service keys
                                result = False
                                failReason = "KMS CMK rotation not enabled"
                                offenders.append("Key:" + str(keyDescription['KeyMetadata']['Arn']))
                    except:
                        pass  # Ignore keys without permission, for example ACM key
    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")

    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}
