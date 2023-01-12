"""
	iam_control_1.py
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
# --- Control Parameters ---

# Control 1.18 - IAM manager and master role names <Not implemented yet, under review>
IAM_MASTER = "iam_master"
IAM_MANAGER = "iam_manager"
IAM_MASTER_POLICY = "iam_master_policy"
IAM_MANAGER_POLICY = "iam_manager_policy"

# Control 1.1 - Days allowed since use of root account.
CONTROL_1_1_DAYS = 0


# --- Global ---
# def __init__(self):
#     IAM_CLIENT = self.session.client('iam')
#     S3_CLIENT = self.session.client('iam')

# --- 1 Identity and Access Management ---

# 1.1 Avoid the use of the "root" account (Scored)
def control_1_1_root_use(self, credreport):
    logger.info(" ---Inside iam_control_1 :: control_1_1_root_use()--- ")
    """Summary

    Args:
        credreport (TYPE): Description

    Returns:
        TYPE: Description
    """

    result = True
    failReason = ""
    offenders = []
    control = "1.1"
    description = "Avoid the use of the root account"
    scored = True
    if "Fail" in credreport:  # Report failure in control
        sys.exit(credreport)
    # Check if root is used in the last 24h
    now = time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime(time.time()))
    frm = "%Y-%m-%dT%H:%M:%S+00:00"

    try:
        # logger.info(credreport[0])
        pwdDelta = (datetime.strptime(now, frm) - datetime.strptime(credreport[0]['password_last_used'], frm))
        if (pwdDelta.days == CONTROL_1_1_DAYS) & (pwdDelta.seconds > 0):  # Used within last 24h
            failReason = "Used within 24h"
            result = False
    except:
        if credreport[0]['password_last_used'] == "N/A" or "no_information":
            pass
        else:
            logger.error(" Something went wrong")

    try:
        key1Delta = (datetime.strptime(now, frm) - datetime.strptime(credreport[0]['access_key_1_last_used_date'], frm))
        if (key1Delta.days == CONTROL_1_1_DAYS) & (key1Delta.seconds > 0):  # Used within last 24h
            failReason = "Used within 24h"
            result = False
    except:
        if credreport[0]['access_key_1_last_used_date'] == "N/A" or "no_information":
            pass
        else:
            logger.error("Something went wrong")
    try:
        key2Delta = datetime.strptime(now, frm) - datetime.strptime(credreport[0]['access_key_2_last_used_date'], frm)
        if (key2Delta.days == CONTROL_1_1_DAYS) & (key2Delta.seconds > 0):  # Used within last 24h
            failReason = "Used within 24h"
            result = False
    except:
        if credreport[0]['access_key_2_last_used_date'] == "N/A" or "no_information":
            pass
        else:
            logger.error("Something went wrong")
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.2 Ensure multi-factor authentication (MFA) is enabled for all IAM users that have a console password (Scored)
def control_1_2_mfa_on_password_enabled_iam(self, credreport):
    logger.info(" ---Inside iam_control_1 :: control_1_2_mfa_on_password_enabled_iam()--- ")
    """Summary

    Args:
        credreport (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.2"
    description = "Ensure multi-factor authentication (MFA) is enabled for all IAM users that have a console password"
    scored = True
    for i in range(len(credreport)):
        # Verify if the user have a password configured
        if credreport[i]['password_enabled'] == "true":
            # Verify if password users have MFA assigned
            if credreport[i]['mfa_active'] == "false":
                result = False
                failReason = "No MFA on users with password. "
                offenders.append(str(credreport[i]['arn']))
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.3 Ensure credentials unused for 90 days or greater are disabled (Scored)
def control_1_3_unused_credentials(self, credreport):
    logger.info(" ---Inside iam_control_1 :: control_1_3_unused_credentials()--- ")
    """Summary

    Args:
        credreport (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.3"
    description = "Ensure credentials unused for 90 days or greater are disabled"
    scored = True
    # Get current time
    now = time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime(time.time()))
    frm = "%Y-%m-%dT%H:%M:%S+00:00"

    # Look for unused credentails
    for i in range(len(credreport)):
        if credreport[i]['password_enabled'] == "true":
            try:
                delta = datetime.strptime(now, frm) - datetime.strptime(credreport[i]['password_last_used'], frm)
                # Verify password have been used in the last 90 days
                if delta.days > 90:
                    result = False
                    failReason = "Credentials unused > 90 days detected. "
                    offenders.append(str(credreport[i]['arn']) + ":password")
            except:
                pass  # Never used
        if credreport[i]['access_key_1_active'] == "true":
            try:
                delta = datetime.strptime(now, frm) - datetime.strptime(credreport[i]['access_key_1_last_used_date'],
                                                                        frm)
                # Verify password have been used in the last 90 days
                if delta.days > 90:
                    result = False
                    failReason = "Credentials unused > 90 days detected. "
                    offenders.append(str(credreport[i]['arn']) + ":key1")
            except:
                pass
        if credreport[i]['access_key_2_active'] == "true":
            try:
                delta = datetime.strptime(now, frm) - datetime.strptime(credreport[i]['access_key_2_last_used_date'],
                                                                        frm)
                # Verify password have been used in the last 90 days
                if delta.days > 90:
                    result = False
                    failReason = "Credentials unused > 90 days detected. "
                    offenders.append(str(credreport[i]['arn']) + ":key2")
            except:
                # Never used
                pass
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.4 Ensure access keys are rotated every 90 days or less (Scored)
def control_1_4_rotated_keys(self, credreport):
    logger.info(" ---Inside iam_control_1 :: control_1_4_rotated_keys()--- ")
    """Summary

    Args:
        credreport (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.4"
    description = "Ensure access keys are rotated every 90 days or less"
    scored = True
    # Get current time
    now = time.strftime('%Y-%m-%dT%H:%M:%S+00:00', time.gmtime(time.time()))
    frm = "%Y-%m-%dT%H:%M:%S+00:00"

    # Look for unused credentails
    for i in range(len(credreport)):
        if credreport[i]['access_key_1_active'] == "true":
            try:
                delta = datetime.strptime(now, frm) - datetime.strptime(credreport[i]['access_key_1_last_rotated'], frm)
                # Verify keys have rotated in the last 90 days
                if delta.days > 90:
                    result = False
                    failReason = "Key rotation >90 days or not used since rotation"
                    offenders.append(str(credreport[i]['arn']) + ":unrotated key1")
            except:
                pass
            try:
                last_used_datetime = datetime.strptime(credreport[i]['access_key_1_last_used_date'], frm)
                last_rotated_datetime = datetime.strptime(credreport[i]['access_key_1_last_rotated'], frm)
                # Verify keys have been used since rotation.
                if last_used_datetime < last_rotated_datetime:
                    result = False
                    failReason = "Key rotation >90 days or not used since rotation"
                    offenders.append(str(credreport[i]['arn']) + ":unused key1")
            except:
                pass
        if credreport[i]['access_key_2_active'] == "true":
            try:
                delta = datetime.strptime(now, frm) - datetime.strptime(credreport[i]['access_key_2_last_rotated'], frm)
                # Verify keys have rotated in the last 90 days
                if delta.days > 90:
                    result = False
                    failReason = "Key rotation >90 days or not used since rotation"
                    offenders.append(str(credreport[i]['arn']) + ":unrotated key2")
            except:
                pass
            try:
                last_used_datetime = datetime.strptime(credreport[i]['access_key_2_last_used_date'], frm)
                last_rotated_datetime = datetime.strptime(credreport[i]['access_key_2_last_rotated'], frm)
                # Verify keys have been used since rotation.
                if last_used_datetime < last_rotated_datetime:
                    result = False
                    failReason = "Key rotation >90 days or not used since rotation"
                    offenders.append(str(credreport[i]['arn']) + ":unused key2")
            except:
                pass
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.5 Ensure IAM password policy requires at least one uppercase letter (Scored)
def control_1_5_password_policy_uppercase(self, passwordpolicy):
    logger.info(" ---Inside iam_control_1 :: control_1_5_password_policy_uppercase()--- ")
    """Summary

    Args:
        passwordpolicy (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.5"
    description = "Ensure IAM password policy requires at least one uppercase letter"
    scored = True
    if passwordpolicy is False:
        result = False
        failReason = "Account does not have a IAM password policy."
    else:
        if passwordpolicy['RequireUppercaseCharacters'] is False:
            result = False
            failReason = "Password policy does not require at least one uppercase letter"
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.6 Ensure IAM password policy requires at least one lowercase letter (Scored)
def control_1_6_password_policy_lowercase(self, passwordpolicy):
    logger.info(" ---Inside iam_control_1 :: control_1_6_password_policy_lowercase()--- ")
    """Summary

    Args:
        passwordpolicy (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.6"
    description = "Ensure IAM password policy requires at least one lowercase letter"
    scored = True
    if passwordpolicy is False:
        result = False
        failReason = "Account does not have a IAM password policy."
    else:
        if passwordpolicy['RequireLowercaseCharacters'] is False:
            result = False
            failReason = "Password policy does not require at least one uppercase letter"
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.7 Ensure IAM password policy requires at least one symbol (Scored)
def control_1_7_password_policy_symbol(self, passwordpolicy):
    logger.info(" ---Inside iam_control_1 :: control_1_7_password_policy_symbol()--- ")
    """Summary

    Args:
        passwordpolicy (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.7"
    description = "Ensure IAM password policy requires at least one symbol"
    scored = True
    if passwordpolicy is False:
        result = False
        failReason = "Account does not have a IAM password policy."
    else:
        if passwordpolicy['RequireSymbols'] is False:
            result = False
            failReason = "Password policy does not require at least one symbol"
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.8 Ensure IAM password policy requires at least one number (Scored)
def control_1_8_password_policy_number(self, passwordpolicy):
    logger.info(" ---Inside iam_control_1 :: control_1_8_password_policy_number()--- ")
    """Summary

    Args:
        passwordpolicy (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.8"
    description = "Ensure IAM password policy requires at least one number"
    scored = True
    if passwordpolicy is False:
        result = False
        failReason = "Account does not have a IAM password policy."
    else:
        if passwordpolicy['RequireNumbers'] is False:
            result = False
            failReason = "Password policy does not require at least one number"
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.9 Ensure IAM password policy requires minimum length of 14 or greater (Scored)
def control_1_9_password_policy_length(self, passwordpolicy):
    logger.info(" ---Inside iam_control_1 :: control_1_9_password_policy_length()--- ")
    """Summary

    Args:
        passwordpolicy (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.9"
    description = "Ensure IAM password policy requires minimum length of 14 or greater"
    scored = True
    if passwordpolicy is False:
        result = False
        failReason = "Account does not have a IAM password policy."
    else:
        if passwordpolicy['MinimumPasswordLength'] < 14:
            result = False
            failReason = "Password policy does not require at least 14 characters"
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.10 Ensure IAM password policy prevents password reuse (Scored)
def control_1_10_password_policy_reuse(self, passwordpolicy):
    logger.info(" ---Inside iam_control_1 :: control_1_10_password_policy_reuse()--- ")
    """Summary

    Args:
        passwordpolicy (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.10"
    description = "Ensure IAM password policy prevents password reuse"
    scored = True
    if passwordpolicy is False:
        result = False
        failReason = "Account does not have a IAM password policy."
    else:
        try:
            if passwordpolicy['PasswordReusePrevention'] == 24:
                pass
            else:
                result = False
                failReason = "Password policy does not prevent reusing last 24 passwords"
        except:
            result = False
            failReason = "Password policy does not prevent reusing last 24 passwords"
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.11 Ensure IAM password policy expires passwords within 90 days or less (Scored)
def control_1_11_password_policy_expire(self, passwordpolicy):
    logger.info(" ---Inside iam_control_1 :: control_1_11_password_policy_expire()--- ")
    """Summary

    Args:
        passwordpolicy (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.11"
    description = "Ensure IAM password policy expires passwords within 90 days or less"
    scored = True
    if passwordpolicy is False:
        result = False
        failReason = "Account does not have a IAM password policy."
    else:
        if passwordpolicy['ExpirePasswords'] is True:
            if 0 < passwordpolicy['MaxPasswordAge'] > 90:
                result = False
                failReason = "Password policy does not expire passwords after 90 days or less"
        else:
            result = False
            failReason = "Password policy does not expire passwords after 90 days or less"
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.12 Ensure no root account access key exists (Scored)
def control_1_12_root_key_exists(self, credreport):
    logger.info(" ---Inside iam_control_1 :: control_1_12_root_key_exists()--- ")
    """Summary

    Args:
        credreport (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.12"
    description = "Ensure no root account access key exists"
    scored = True
    if (credreport[0]['access_key_1_active'] == "true") or (credreport[0]['access_key_2_active'] == "true"):
        result = False
        failReason = "Root have active access keys"
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.13 Ensure MFA is enabled for the "root" account (Scored)
def control_1_13_root_mfa_enabled(self, ):
    logger.info(" ---Inside iam_control_1 :: control_1_13_root_mfa_enabled()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.13"
    description = "Ensure MFA is enabled for the root account"
    scored = True
    # global IAM_CLIENT
    response = self.session.client('iam').get_account_summary()
    if response['SummaryMap']['AccountMFAEnabled'] != 1:
        result = False
        failReason = "Root account not using MFA"
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.14 Ensure hardware MFA is enabled for the "root" account (Scored)
def control_1_14_root_hardware_mfa_enabled(self, ):
    logger.info(" ---Inside iam_control_1 :: control_1_14_root_hardware_mfa_enabled()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.14"
    description = "Ensure hardware MFA is enabled for the root account"
    scored = True
    # global IAM_CLIENT
    # First verify that root is using MFA (avoiding false positive)
    response = self.session.client('iam').get_account_summary()
    if response['SummaryMap']['AccountMFAEnabled'] == 1:
        paginator = self.session.client('iam').get_paginator('list_virtual_mfa_devices')
        response_iterator = paginator.paginate(
            AssignmentStatus='Any',
        )
        pagedResult = []
        for page in response_iterator:
            for n in page['VirtualMFADevices']:
                pagedResult.append(n)
        if "mfa/root-account-mfa-device" in str(pagedResult):
            failReason = "Root account not using hardware MFA"
            result = False
    else:
        result = False
        failReason = "Root account not using MFA"
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.15 Ensure security questions are registered in the AWS account (Not Scored/Manual)
def control_1_15_security_questions_registered(self, ):
    logger.info(" ---Inside iam_control_1 :: control_1_15_security_questions_registered()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Manual"
    failReason = ""
    offenders = []
    control = "1.15"
    description = "Ensure security questions are registered in the AWS account, please verify manually"
    scored = False
    failReason = "Control not implemented using API, please verify manually"
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.16 Ensure IAM policies are attached only to groups or roles (Scored)
def control_1_16_no_policies_on_iam_users(self, ):
    logger.info(" ---Inside iam_control_1 :: control_1_16_no_policies_on_iam_users()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.16"
    description = "Ensure IAM policies are attached only to groups or roles"
    scored = True
    # global IAM_CLIENT
    paginator = self.session.client('iam').get_paginator('list_users')
    response_iterator = paginator.paginate()
    pagedResult = []
    for page in response_iterator:
        for n in page['Users']:
            pagedResult.append(n)
    offenders = []
    for n in pagedResult:
        policies = self.session.client('iam').list_user_policies(
            UserName=n['UserName'],
            MaxItems=1
        )
        if policies['PolicyNames'] != []:
            result = False
            failReason = "IAM user have inline policy attached"
            offenders.append(str(n['Arn']))
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.17 Enable detailed billing (Scored)
def control_1_17_detailed_billing_enabled(self, ):
    logger.info(" ---Inside iam_control_1 :: control_1_17_detailed_billing_enabled()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Manual"
    failReason = ""
    offenders = []
    control = "1.17"
    description = "Enable detailed billing, please verify manually"
    scored = True
    failReason = "Control not implemented using API, please verify manually"
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.18 Ensure IAM Master and IAM Manager roles are active (Scored)
def control_1_18_ensure_iam_master_and_manager_roles(self, ):
    logger.info(" ---Inside iam_control_1 :: control_1_18_ensure_iam_master_and_manager_roles()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "True"
    failReason = "No IAM Master or IAM Manager role created"
    offenders = []
    control = "1.18"
    description = "Ensure IAM Master and IAM Manager roles are active. Control under review/investigation"
    scored = True
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.19 Maintain current contact details (Scored)
def control_1_19_maintain_current_contact_details(self, ):
    logger.info(" ---Inside iam_control_1 :: control_1_19_maintain_current_contact_details()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Manual"
    failReason = ""
    offenders = []
    control = "1.19"
    description = "Maintain current contact details, please verify manually"
    scored = True
    failReason = "Control not implemented using API, please verify manually"
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.20 Ensure security contact information is registered (Scored)
def control_1_20_ensure_security_contact_details(self, ):
    logger.info(" ---Inside iam_control_1 :: control_1_20_ensure_security_contact_details()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Manual"
    failReason = ""
    offenders = []
    control = "1.20"
    description = "Ensure security contact information is registered, please verify manually"
    scored = True
    failReason = "Control not implemented using API, please verify manually"
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.21 Ensure IAM instance roles are used for AWS resource access from instances (Scored)
def control_1_21_ensure_iam_instance_roles_used(self, ):
    logger.info(" ---Inside iam_control_1 :: control_1_21_ensure_iam_instance_roles_used()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.21"
    description = "Ensure IAM instance roles are used for AWS resource access from instances, application code is not audited"
    scored = True
    failReason = "Instance not assigned IAM role for EC2"
    client = self.session.client('ec2', region_name='us-east-1')
    response = client.describe_instances()
    offenders = []
    for n, _ in enumerate(response['Reservations']):
        try:
            if response['Reservations'][n]['Instances'][0]['IamInstanceProfile']:
                pass
        except:
            result = False
            offenders.append(str(response['Reservations'][n]['Instances'][0]['InstanceId']))
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.22 Ensure a support role has been created to manage incidents with AWS Support (Scored)
def control_1_22_ensure_incident_management_roles(self, ):
    logger.info(" ---Inside iam_control_1 :: control_1_22_ensure_incident_management_roles()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.22"
    description = "Ensure a support role has been created to manage incidents with AWS Support"
    scored = True
    offenders = []
    # global IAM_CLIENT
    try:
        response = self.session.client('iam').list_entities_for_policy(
            PolicyArn='arn:aws:iam::aws:policy/AWSSupportAccess'
        )
        if (len(response['PolicyGroups']) + len(response['PolicyUsers']) + len(response['PolicyRoles'])) == 0:
            result = False
            failReason = "No user, group or role assigned AWSSupportAccess"
    except:
        result = False
        failReason = "AWSSupportAccess policy not created"
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.23 Do not setup access keys during initial user setup for all IAM users that have a console password (Not Scored)
def control_1_23_no_active_initial_access_keys_with_iam_user(self, credreport):
    logger.info(" ---Inside iam_control_1 :: control_1_23_no_active_initial_access_keys_with_iam_user()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.23"
    description = "Do not setup access keys during initial user setup for all IAM users that have a console password"
    scored = False
    offenders = []
    # global IAM_CLIENT
    for n, _ in enumerate(credreport):
        if (credreport[n]['access_key_1_active'] or credreport[n]['access_key_2_active'] == 'true') and n > 0:
            try:
                response = self.session.client('iam').list_access_keys(UserName=str(credreport[n]['user']))
                for m in response['AccessKeyMetadata']:
                    if re.sub(r"\s", "T", str(m['CreateDate'])) == credreport[n]['user_creation_time']:
                        result = False
                        failReason = "Users with keys created at user creation time found"
                        offenders.append(str(credreport[n]['arn']) + ":" + str(m['AccessKeyId']))
            except botocore.exceptions.ClientError as error:
                if error.response['Error']['Code'] == 'NoSuchEntityException':
                    logger.error(f" AccessKey credentails not found for user: {str(credreport[n]['user'])}")
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.24  Ensure IAM policies that allow full "*:*" administrative privileges are not created (Scored)
def control_1_24_no_overly_permissive_policies(self, ):
    logger.info(" ---Inside iam_control_1 :: control_1_24_no_overly_permissive_policies()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.24"
    description = "Ensure IAM policies that allow full administrative privileges are not created"
    scored = True
    offenders = []
    # global IAM_CLIENT
    paginator = self.session.client('iam').get_paginator('list_policies')
    response_iterator = paginator.paginate(
        Scope='Local',
        OnlyAttached=False,
    )
    pagedResult = []
    for page in response_iterator:
        for n in page['Policies']:
            pagedResult.append(n)
    for m in pagedResult:
        policy = self.session.client('iam').get_policy_version(
            PolicyArn=m['Arn'],
            VersionId=m['DefaultVersionId']
        )

        statements = []
        # a policy may contain a single statement, a single statement in an array, or multiple statements in an array
        if isinstance(policy['PolicyVersion']['Document']['Statement'], list):
            for statement in policy['PolicyVersion']['Document']['Statement']:
                statements.append(statement)
        else:
            statements.append(policy['PolicyVersion']['Document']['Statement'])

        for n in statements:
            # a policy statement has to contain either an Action or a NotAction
            if 'Action' in n.keys() and n['Effect'] == 'Allow':
                if ("'*'" in str(n['Action']) or str(n['Action']) == "*") and (
                        "'*'" in str(n['Resource']) or str(n['Resource']) == "*"):
                    result = False
                    failReason = "Found full administrative policy"
                    offenders.append(str(m['Arn']))
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 1.25 Ensure MFA is enable to delete cloudtrail buckets
def control_1_25_require_mfa_to_delete_cloudtrail_buckets(self, regions: list) -> dict:
    # returns the list trails
    def list_trails(region) -> dict:
        # trails_lst = []
        trails_lst_with_bucket = {}
        client = self.session.client('cloudtrail', region_name=region)

        response = client.describe_trails(
            trailNameList=[],
            includeShadowTrails=False
        )
        for trail in response['trailList']:
            trails_lst_with_bucket[trail['Name']] = trail['S3BucketName']

        return trails_lst_with_bucket

    logger.info(" ---Inside iam_control_1 :: control_1_25_require_mfa_to_delete_cloudtrail_buckets")

    """Summary
    
    Returns:
        TYPE: dict
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.25"
    description = "Require MFA to delete cloudtrail buckets"
    scored = True
    for n in regions:
        trails = list_trails(n)
        client = self.session.client('s3')
        for trail, bucket in trails.items():
            response = client.get_bucket_versioning(
                Bucket=bucket
            )
            try:
                if response['MFADelete'] == 'Disabled':
                    result = False
                    failReason = "Found cloudtrail s3 bucket with MFA delete disabled"
                    offenders.append(trail)
            except KeyError:
                result = False
                failReason = "Found cloudtrail s3 bucket with MFA delete disabled"
                offenders.append(trail)

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# 1.26 Ensure expired ssl and tls certificate are not in use
def control_1_26_dont_use_expired_ssl_tls_certificate(self, regions: list) -> dict:
    logger.info(" ---Inside iam_control_1 :: control_1_26_dont_use_expired_ssl_tls_certificate")

    """Summary
    
    Returns:
        TYPE: dict
    """
    result = True
    failReason = ""
    offenders = []
    control = "1.26"
    description = "Don't use expired ssl/tls certificate"
    scored = True

    for region in regions:
        client = self.session.client('acm', region_name=region)
        marker = ''
        while True:
            if marker == '' or marker is None:
                response = client.list_certificates(
                    CertificateStatuses=['EXPIRED']
                )
            else:
                response = client.list_certificates(
                    CertificateStatuses=['EXPIRED'],
                    NextToken=marker
                )

            for certificate in response['CertificateSummaryList']:
                try:
                    if certificate['InUse']:
                        result = False
                        failReason = "Found expired SSL/TLS certificate which is in use"
                        offenders.append(certificate['CertificateArn'])
                except KeyError:
                    pass

            try:
                marker = response['NextToken']
                if marker == '':
                    break
            except:
                break

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }
