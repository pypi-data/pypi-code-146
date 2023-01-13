"""
security_control_4.py
"""

import os, re, sys, time, logging, logging.config

import datetime

import botocore.errorfactory
import botocore.exceptions
import pytz
from dateutil.relativedelta import relativedelta

from .utils import *

global logger
logging.basicConfig(level=logging.INFO)

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# LOG_CONF_PATH = os.path.join(BASE_DIR, '..', 'logging.conf')
# LOG_FILE_PATH = os.path.join(BASE_DIR, '..', 'logs',
#                              'cis_automation_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log')
# logging.config.fileConfig(LOG_CONF_PATH, defaults={'logfilename': LOG_FILE_PATH})
logger = logging.getLogger('simpleLogger')


# ---Security---


def control_5_1_cloudtrail_bucket_mfa_delete_enabled(self, cloudtrails):
    logger.info(" ---Inside security_control_5 :: control_5_1_cloudtrail_bucket_mfa_delete_enabled()---")
    """Summary
    
    Args:
        cloudtrails (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.1"
    description = "Ensure CloudTrail bucket MFA delete is enabled"
    scored = True

    try:
        for region, trails in cloudtrails.items():
            for trail in trails:
                s3_bucket = trail['S3BucketName']
                client = self.session.client('s3')
                try:
                    resp = client.get_bucket_versioning(
                        Bucket=s3_bucket,
                    )
                    status = resp['Status']

                    if not status == 'Enabled':
                        result = "Not Compliant"
                        failReason = "Either bucket versioning is not enabled or configuration not found"
                        offenders.append(s3_bucket)
                except KeyError:
                    result = "Not Compliant"
                    failReason = "Either bucket versioning is not enabled or configuration not found"
                    offenders.append(s3_bucket)
                    continue
                except botocore.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == 'AccessDenied':
                        result = "Not Compliant"
                        failReason = "S3 access denied"
                        offenders.append(trail)
                    elif e.response['Error']['Code'] == 'NoSuchBucket':
                        result = "Not Compliant"
                        failReason = "Cloudtrail bucket {} not found".format(s3_bucket)
                        offenders.append(trail)

    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# 5.2 Ensure that the existing IAM policies are attached only to groups and roles
def control_5_2_ensure_existing_iam_policies_attached_to_groups_and_roles(self):
    logger.info(
        "---Inside security_control_5 :: "
        "control_5_2_control_5_2_ensure_existing_iam_policies_attached_to_groups_and_roles()---")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.2"
    description = "Ensure existing iam policies attached to groups and roles only"
    scored = True

    client = self.session.client('iam')
    marker = ''
    while True:
        if marker == '':
            response = client.list_users()
        else:
            response = client.list_users(
                Marker=marker
            )
        for user in response['Users']:
            attached_policies = client.list_attached_user_policies(
                UserName=user['UserName']
            )
            if len(attached_policies['AttachedPolicies']) > 0:
                result = "Not Compliant"
                failReason = "Policies are attached to the user"
                offenders.append(user['UserName'])

        try:
            marker = response['Marker']
            if marker == '':
                break
        except KeyError:
            break

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# 5.3 Ensure that all your IAM user access keys are rotated every month
def control_5_3_ensure_access_keys_are_rotated_30_days(self):
    logger.info(" ---Inside security_control_5 :: control_5_3_ensure_access_keys_are_rotated_30_days---")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.3"
    description = "Ensure that all your IAM user access keys are rotated every month"
    scored = True

    datetime_30_days_ago = datetime.now() - relativedelta(months=1)
    timezone = pytz.timezone("UTC")
    datetime_30_days_ago = timezone.localize(datetime_30_days_ago)

    client = self.session.client('iam')
    marker = ''
    while True:
        if marker == '':
            response = client.list_users()
        else:
            response = client.list_users(
                Marker=marker
            )
        for user in response['Users']:
            access_keys = client.list_access_keys(
                UserName=user['UserName']
            )
            for key in access_keys['AccessKeyMetadata']:
                if key['CreateDate'] < datetime_30_days_ago:
                    result = "Not Compliant"
                    offenders.append(key['UserName'])
                    failReason = 'Key is not rotated since 1 month or older'

        try:
            marker = response['Marker']
            if marker == '':
                break
        except KeyError:
            break

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# 5.4 Ensure that your AWS IAM users are using a strong password policy to define password requirements
def control_5_4_ensure_strict_password_policy(self):
    logger.info(" ---Inside security_control_5 :: control_5_4_ensure_strict_password_policy()---")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.4"
    description = "Ensure that your AWS IAM users are using a strong password policy"
    scored = True

    client = self.session.client('iam')
    try:
        response = client.get_account_password_policy()
    except botocore.exceptions.ClientError as e:
        result = "Not Compliant"
        failReason = "No strict password policy is implemented"

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# 5.5 Check for any publicly accessible CloudTrail trail log buckets
def control_5_5_publicly_accessible_cloudtrail_buckets(self, cloudtrails):
    logger.info(" ---Inside security_control_5 :: control_5_5_publicly_accessible_cloudtrail_buckets")
    """Summary
    
    Args:
        cloudtrails (TYPE): Description

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.5"
    description = "Publicly accessible cloudtrail buckets"
    scored = True

    try:
        for region, trails in cloudtrails.items():
            for trail in trails:
                s3_bucket = trail['S3BucketName']
                client = self.session.client('s3')
                try:
                    resp = client.get_bucket_acl(
                        Bucket=s3_bucket,
                    )
                    for grant in resp['Grants']:
                        uri = grant['Grantee']['URI']
                        if 'AllUsers' in uri or 'AuthenticatedUsers' in uri:
                            result = "Not Compliant"
                            failReason = 'Cloudtrail bucket is publicly accessible'
                            offenders.append(trail['Name'])
                except KeyError:
                    result = "Not Compliant"
                    failReason = 'Cloudtrail bucket is publicly accessible'
                    offenders.append(trail['Name'])
                except botocore.exceptions.ClientError as e:
                    if e.response['Error']['Code'] == 'AccessDenied':
                        result = "Not Compliant"
                        failReason = "S3 access denied"
                        offenders.append(trail)
                    elif e.response['Error']['Code'] == 'NoSuchBucket':
                        result = "Not Compliant"
                        failReason = "Cloudtrail bucket {} not found".format(s3_bucket)
                        offenders.append(trail)

    except AttributeError as e:
        logger.error(" No details found for CloudTrail!!! ")

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# 5.6 Ensure that all your Amazon Elastic Block Store (EBS) volumes are encrypted
def control_5_6_ebs_encrypted(self, regions: list) -> dict:
    logger.info(" ---Inside security_control_5 :: control_5_6_ebs_encrypted()")

    """Summary
    
    Args:
        regions TYPE: list

    Returns:
        TYPE: dict
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.6"
    description = "EBS encrypted"
    scored = True

    for region in regions:
        client = self.session.client('ec2', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_volumes()
            else:
                response = client.describe_volumes(
                    NextToken=marker
                )
            for volume in response['Volumes']:
                encrypted = volume['Encrypted']
                if not encrypted:
                    result = "Not Compliant"
                    offenders.append(volume['VolumeId'])
                    failReason = "Volume is not encrypted"

            try:
                marker = response['NextToken']
                if marker == '':
                    break
            except KeyError:
                break

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# 5.7 Ensure that your Amazon EC2 default security groups restrict all inbound public traffic
def control_5_7_default_security_group_unrestricted(self, regions: list) -> dict:
    logger.info(" ---Inside security_control_5 :: control_5_7_default_security_group_unrestricted()")

    """Summary
    
    Args:
        regions TYPE: list

    Returns:
        TYPE: dict
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.7"
    description = "Default Security Group Unrestricted"
    scored = True

    for region in regions:
        client = self.session.client('ec2', region_name=region)

        marker = ''
        while True:
            if marker == '':
                response = client.describe_security_groups(
                    Filters=[
                        {
                            'Name': 'group-name',
                            'Values': ['default']
                        }
                    ]
                )
            else:
                response = client.describe_security_groups(
                    Filters=[
                        {
                            'Name': 'group-name',
                            'Values': ['default']
                        }
                    ],
                    NextToken=marker
                )

            for sg in response['SecurityGroups']:
                flag = True
                for perm in sg['IpPermissions']:
                    for ip_range in perm['IpRanges']:
                        cidr = ip_range['CidrIp']
                        if cidr == '0.0.0.0/0':
                            flag = False
                            result = "Not Compliant"
                            offenders.append(sg['GroupName'])
                            failReason = "default security group has open ports for anywhere"

                        if not flag:
                            break
                    if not flag:
                        break

            try:
                marker = response['NextToken']
                if marker == '':
                    break
            except KeyError:
                break

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# 5.8 Ensure that your Amazon Classic Load Balancer listeners are using a secure protocol (HTTPS or SSL)
def control_5_8_elb_listener_security(self, regions: list) -> dict:
    logger.info(" ---Inside security_control_5 :: control_5_8_elb_listener_security()")

    """Summary
    
    Args:
        regions TYPE: list

    Returns:
        TYPE: dict
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.8"
    description = "ELB Listener Security"
    scored = True

    for region in regions:
        client = self.session.client('elb', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_load_balancers()
            else:
                response = client.describe_load_balancers(
                    Marker=marker
                )
            for lb in response['LoadBalancerDescriptions']:
                flag = True
                if len(lb['ListenerDescriptions']) > 0:
                    for listener in lb['ListenerDescriptions']:
                        protocol = listener['Listener']['Protocol']
                        if protocol == 'HTTPS' or protocol == 'SSL':
                            pass
                        else:
                            flag = False
                            result = "Not Compliant"
                            failReason = 'Load balancer listeners are not using secure protocol (HTTPS or SSL)'
                            offenders.append(lb['LoadBalancerName'])
                        if not flag:
                            break

                else:
                    result = "Not Compliant"
                    failReason = 'Load balancer listeners are not using secure protocol (HTTPS or SSL)'
                    offenders.append(lb['LoadBalancerName'])

            try:
                marker = response['NextMarker']
                if marker == '':
                    break
            except KeyError:
                break

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# 5.10 Ensure that your RDS database instances are encrypted
def control_5_10_rds_encryption_enabled(self, regions: list) -> dict:
    logger.info(" ---Inside security_control_5 :: control_5_10_rds_encryption_enabled()")

    """Summary
    
    Args:
        regions TYPE: list

    Returns:
        TYPE: dict
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.10"
    description = "Rds encryption enabled"
    scored = True

    for region in regions:
        client = self.session.client('rds', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_db_instances()
            else:
                response = client.describe_db_instances(
                    Marker=marker
                )
            for instance in response['DBInstances']:
                encrypted = instance['StorageEncrypted']
                if not encrypted:
                    result = "Not Compliant"
                    offenders.append(instance['DBInstanceIdentifier'])
                    failReason = 'DB instance is not encrypted'

            try:
                marker = response['Marker']
                if marker == '':
                    break
            except KeyError:
                break

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# 5.12 Check for any public facing RDS database instances provisioned in your AWS account
def control_5_12_rds_publicly_accessible(self, regions: list) -> dict:
    logger.info(" ---Inside security_control_5 :: control_5_12_rds_publicly_accessible()")

    """Summary
    
    Args:
        regions TYPE: list

    Returns:
        TYPE: dict
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.12"
    description = "Rds Publicly Accessible"
    scored = True

    for region in regions:
        client = self.session.client('rds', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_db_instances()
            else:
                response = client.describe_db_instances(
                    Marker=marker
                )

            for instance in response['DBInstances']:
                public = instance['PubliclyAccessible']
                if public:
                    result = "Not Compliant"
                    offenders.append(instance['DBInstanceIdentifier'])
                    failReason = 'DB Instance is publicly accessible'

            try:
                marker = response['Marker']
                if marker == '':
                    break
            except KeyError:
                break

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# control 5.13 Ensure Redshift clusters are not publicly accessible to minimise security risks
def control_5_13_redshift_cluster_publicly_accessible(self, regions: list) -> dict:
    logger.info(" ---Inside security_control_5 :: control_5_13_redshift_cluster_publicly_accessible")

    """Summary
    
    Args:
        regions TYPE: list

    Returns:
        TYPE: dict
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.13"
    description = "Redshift cluster publicly accessible"
    scored = True

    for region in regions:
        client = self.session.client('redshift', region_name=region)

        marker = ''
        while True:
            if marker == '':
                response = client.describe_clusters()
            else:
                response = client.desceibe_clusters(
                    Marker=marker
                )
            for cluster in response['Clusters']:
                public = cluster['PubliclyAccessible']
                if public:
                    result = "Not Compliant"
                    failReason = 'Redshift cluster is publicly accessible'
                    offenders.append(cluster['ClusterIdentifier'])

            try:
                marker = response['Marker']
                if marker == '':
                    break
            except KeyError:
                break

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# control 5.14 Ensure that your AWS AMIs are not publicly shared with the other AWS accounts
def control_5_14_publicly_shared_ami(self, regions: list) -> dict:
    logger.info(" ---Inside security_control_5 :: control_5_14_publicly_shared_ami()")

    """Summary
    
    Args:
        regions TYPE: list

    Returns:
        TYPE: dict
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.14"
    description = "Publicly shared AMI"
    scored = True

    for region in regions:
        client = self.session.client('ec2', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_images(
                    Owners=['self']
                )
            else:
                response = client.describe_images(
                    Owners=['self'],
                    NextToken=marker
                )
            for image in response['Images']:
                public = image['Public']
                if public:
                    result = "Not Compliant"
                    offenders.append(image['ImageId'])
                    failReason = "Image is publicly accessible"

            try:
                marker = response['NextToken']
                if marker == '':
                    break
            except KeyError:
                break

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# control 5.15 Identify any unnecessary IAM SSH public keys
def control_5_15_unnecessary_ssh_public_keys(self) -> dict:
    logger.info(" ---Inside security_control_5 :: control_5_15_unnecessary_ssh_public_keys()---")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.15"
    description = "Unnecessary SSH Public Keys"
    scored = True

    client = self.session.client('iam')

    marker = ''
    while True:
        if marker == '':
            response = client.list_users()
        else:
            response = client.list_users(
                Marker=marker
            )
        for user in response['Users']:
            ssh_keys = client.list_ssh_public_keys(
                UserName=user['UserName']
            )
            count_active = 0
            for key in ssh_keys['SSHPublicKeys']:
                if key['Status'] == 'Active':
                    count_active - count_active + 1

                if count_active > 1:
                    result = "Not Compliant"
                    failReason = "more than 1 ssh key are in active state"
                    offenders.append(user['UserName'])

        try:
            marker = response['Marker']
            if marker == '':
                break
        except KeyError:
            break

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# control 5.16 Ensure that your Amazon CloudFront distributions are using a security policy with minimum TLSv1.2 or
# TLSv1.3 and appropriate security ciphers for HTTPS viewer connections
def control_5_16_cloudfront_security_policy(self) -> dict:
    logger.info(" ---Inside security_control_5 :: control_5_16_cloudfront_security_policy()---")

    """Summary

    Returns:
        TYPE: dict
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.16"
    description = "Amazon CloudFront distributions are using a security policy"
    scored = True

    client = self.session.client('cloudfront')

    protocol_not_recommended = [
        'TLSv1',
        'TLSv1_2016',
        'TLSv1.1_2016',
        'TLSv1.2_2018',
        'TLSv1.2_2019'
    ]

    marker = ''
    while True:
        if marker == '':
            response = client.list_distributions()
        else:
            response = client.list_distributions(
                Marker=marker
            )
        try:
            for distribution in response['DistributionList']['Items']:
                protocol = distribution['ViewerCertificate']['MinimumProtocolVersion']

                if protocol in protocol_not_recommended:
                    result = "Not Compliant"
                    offenders.append(distribution['Id'])
                    failReason = "Amazon Cloudfrontt distribution is not using an improved security policy that enforces TLS version 1.2 or 1.3 as the minimum protocol version"

            try:
                marker = response['DistributionList']['NextMarker']
                if marker == '':
                    break
            except KeyError:
                break
        except KeyError:
            break

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# control 5.17 Ensure that all the parameter groups associated with your Amazon Redshift clusters have the
# require_ssl parameter enabled
def control_5_17_redshift_parameter_group_require_ssl(self, regions: list) -> dict:
    logger.info(" ---Inside security_control_5 :: control_5_17_redshift_parameter_group_require_ssl()---")

    """Summary
    
    Args:
        regions TYPE: list

    Returns:
        TYPE: dict
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.17"
    description = "Redshift Parameter Group Require SSL"
    scored = True

    for region in regions:
        client = self.session.client('redshift', region_name=region)

        marker = ''
        while True:
            if marker == '':
                response = client.describe_clusters()
            else:
                response = client.describe_clusters(
                    Marker=marker
                )
            for cluster in response['Clusters']:
                for param_group in cluster['ClusterParameterGroups']:
                    m = ''
                    while True:
                        if m == '':
                            parameters_desc = client.describe_cluster_parameters(
                                ParameterGroupName=param_group['ParameterGroupName']
                            )
                        else:
                            parameters_desc = client.describe_cluster_parameters(
                                ParameterGroupName=param_group['ParameterGroupName'],
                                Marker=m
                            )
                        for param in parameters_desc['Parameters']:
                            if param['ParameterName'] == 'require_ssl' and not param['ParameterValue']:
                                result = "Not Compliant"
                                failReason = "Require SSL parameter is set to False"
                                offenders.append(cluster['ClusterIdentifier'])
                                break
                        try:
                            m = parameters_desc['Marker']
                            if m == '':
                                break
                        except:
                            break

            try:
                marker = response['Marker']
                if marker == '':
                    break
            except KeyError:
                break

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# 5.18 Ensure that all your IAM SSH public keys are rotated every 45 days
def control_5_18_ssh_public_keys_rotated_45_days(self) -> dict:
    logger.info(" ---Inside security_control_5 :: control_5_18_ssh_public_keys_rotated_45_days---")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.18"
    description = "SSH public keys rotated 45 days"
    scored = True

    datetime_45_days_ago = datetime.now() - relativedelta(days=45)
    timezone = pytz.timezone("UTC")
    datetime_45_days_ago = timezone.localize(datetime_45_days_ago)

    client = self.session.client('iam')
    marker = ''
    while True:
        if marker == '':
            response = client.list_users()
        else:
            response = client.list_users(
                Marker=marker
            )
        for user in response['Users']:
            ssh_keys = client.list_ssh_public_keys(
                UserName=user['UserName']
            )
            for key in ssh_keys['SSHPublicKeys']:
                upload_date = key['UploadDate']
                if upload_date < datetime_45_days_ago:
                    result = "Not Compliant"
                    failReason = "SSH keys are not rotated within 45 days"
                    offenders.append(user['UserName'])

        try:
            marker = response['Marker']
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


# 5.19 Ensure that your Amazon IAM users are either being used for API access or for management console access
def control_5_19_multi_mode_access(self) -> dict:
    logger.info(" ---Inside security_control_5 :: control_5_19_multi_mode_access()---")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.19"
    description = "Multi Mode access disabled"
    scored = True

    client = self.session.client('iam')
    marker = ''
    while True:
        if marker == '':
            response = client.list_users()
        else:
            response = client.list_users(
                Marker=marker
            )
        for user in response['Users']:
            access_keys = client.list_access_keys(
                UserName=user['UserName']
            )
            try:
                login_profile = client.get_login_profile(
                    UserName=user['UserName']
                )
                if len(access_keys['AccessKeyMetadata']) > 0:
                    result = "Not Compliant"
                    offenders.append(user['UserName'])
                    failReason = "User have access keys as well as console password"

            except botocore.exceptions.ClientError as e:
                pass

        try:
            marker = response['Marker']
            if marker == '':
                break
        except KeyError:
            break

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }


# control 5.20 reduce no. of IAM groups
def control_5_20_number_of_iam_groups(self) -> dict:
    logger.info(" ---Inside security_control_5 :: control_5_20_number_of_iam_groupss---")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "5.20"
    description = ""
    scored = True

    client = self.session.client('iam')
    count = 0
    marker = ''
    while True:
        if marker == '':
            response = client.list_groups()
        else:
            response = client.list_groups(
                Marker=marker
            )
        count = count + len(response['Groups'])

        try:
            marker = response['Marker']
            if marker == '':
                break
        except KeyError:
            break

    description = "AWS account has {} IAM groups".format(str(count))

    return {
        'Result': result,
        'failReason': failReason,
        'Offenders': offenders,
        'ScoredControl': scored,
        'Description': description,
        'ControlId': control
    }
