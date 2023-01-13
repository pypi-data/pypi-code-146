"""
	networking_control_4.py
"""

import os, re, sys, time, logging, logging.config
from datetime import datetime

import boto3
import botocore.errorfactory
import botocore.exceptions
from botocore.exceptions import NoCredentialsError

global logger
logging.basicConfig(level=logging.INFO)

from cis_checks_10.utils import *

# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# LOG_CONF_PATH = os.path.join(BASE_DIR, '..', 'logging.conf')
# LOG_FILE_PATH = os.path.join(BASE_DIR, '..', 'logs',
#                              'cis_automation_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log')
# logging.config.fileConfig(LOG_CONF_PATH, defaults={'logfilename': LOG_FILE_PATH})
logger = logging.getLogger('simpleLogger')


# --- 4 Networking ---

# 4.1 Ensure no security groups allow ingress from 0.0.0.0/0 to port 22 (Scored)
def control_4_1_ensure_ssh_not_open_to_world(self, regions):
    logger.info(" ---Inside networking_control_4 :: control_4_1_ensure_ssh_not_open_to_world()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "4.1"
    description = "Ensure no security groups allow ingress from 0.0.0.0/0 to port 22"
    scored = True
    for n in regions:
        client = self.session.client('ec2', region_name=n)
        response = client.describe_security_groups()
        for m in response['SecurityGroups']:
            if "0.0.0.0/0" in str(m['IpPermissions']):
                for o in m['IpPermissions']:
                    try:
                        if int(o['FromPort']) <= 22 <= int(o['ToPort']) and '0.0.0.0/0' in str(o['IpRanges']):
                            result = "Not Compliant"
                            failReason = "Found Security Group with port 22 open to the world (0.0.0.0/0)"
                            offenders.append(str(m['GroupId']))
                    except:
                        if str(o['IpProtocol']) == "-1" and '0.0.0.0/0' in str(o['IpRanges']):
                            result = "Not Compliant"
                            failReason = "Found Security Group with port 22 open to the world (0.0.0.0/0)"
                            offenders.append(str(n) + " : " + str(m['GroupId']))
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 4.2 Ensure no security groups allow ingress from 0.0.0.0/0 to port 3389 (Scored)
def control_4_2_ensure_rdp_not_open_to_world(self, regions):
    logger.info(" ---Inside networking_control_4 :: control_4_2_ensure_rdp_not_open_to_world()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "4.2"
    description = "Ensure no security groups allow ingress from 0.0.0.0/0 to port 3389"
    scored = True
    for n in regions:
        client = self.session.client('ec2', region_name=n)
        response = client.describe_security_groups()
        for m in response['SecurityGroups']:
            if "0.0.0.0/0" in str(m['IpPermissions']):
                for o in m['IpPermissions']:
                    try:
                        if int(o['FromPort']) <= 3389 <= int(o['ToPort']) and '0.0.0.0/0' in str(o['IpRanges']):
                            result = "Not Compliant"
                            failReason = "Found Security Group with port 3389 open to the world (0.0.0.0/0)"
                            offenders.append(str(m['GroupId']))
                    except:
                        if str(o['IpProtocol']) == "-1" and '0.0.0.0/0' in str(o['IpRanges']):
                            result = "Not Compliant"
                            failReason = "Found Security Group with port 3389 open to the world (0.0.0.0/0)"
                            offenders.append(str(n) + " : " + str(m['GroupId']))
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


def control_4_2_ensure_20_not_open_to_world(self, regions):
    logger.info(" ---Inside networking_control_4 :: control_4_2_ensure_20_not_open_to_world()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "4.2"
    description = "Ensure no security groups allow ingress from 0.0.0.0/0 to port 20"
    scored = True
    for n in regions:
        client = self.session.client('ec2', region_name=n)
        response = client.describe_security_groups()
        for m in response['SecurityGroups']:
            if "0.0.0.0/0" in str(m['IpPermissions']):
                for o in m['IpPermissions']:
                    try:
                        if int(o['FromPort']) <= 20 <= int(o['ToPort']) and '0.0.0.0/0' in str(o['IpRanges']):
                            result = "Not Compliant"
                            failReason = "Found Security Group with port 20 open to the world (0.0.0.0/0)"
                            offenders.append(str(m['GroupId']))
                    except:
                        if str(o['IpProtocol']) == "-1" and '0.0.0.0/0' in str(o['IpRanges']):
                            result = "Not Compliant"
                            failReason = "Found Security Group with port 20 open to the world (0.0.0.0/0)"
                            offenders.append(str(n) + " : " + str(m['GroupId']))
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


def control_4_2_ensure_21_not_open_to_world(self, regions):
    logger.info(" ---Inside networking_control_4 :: control_4_2_ensure_21_not_open_to_world()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "4.2"
    description = "Ensure no security groups allow ingress from 0.0.0.0/0 to port 21"
    scored = True
    for n in regions:
        client = self.session.client('ec2', region_name=n)
        response = client.describe_security_groups()
        for m in response['SecurityGroups']:
            if "0.0.0.0/0" in str(m['IpPermissions']):
                for o in m['IpPermissions']:
                    try:
                        if int(o['FromPort']) <= 21 <= int(o['ToPort']) and '0.0.0.0/0' in str(o['IpRanges']):
                            result = "Not Compliant"
                            failReason = "Found Security Group with port 21 open to the world (0.0.0.0/0)"
                            offenders.append(str(m['GroupId']))
                    except:
                        if str(o['IpProtocol']) == "-1" and '0.0.0.0/0' in str(o['IpRanges']):
                            result = "Not Compliant"
                            failReason = "Found Security Group with port 21 open to the world (0.0.0.0/0)"
                            offenders.append(str(n) + " : " + str(m['GroupId']))
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


def control_4_2_ensure_3306_not_open_to_world(self, regions):
    logger.info(" ---Inside networking_control_4 :: control_4_2_ensure_3306_not_open_to_world()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "4.2"
    description = "Ensure no security groups allow ingress from 0.0.0.0/0 to port 3306"
    scored = True
    for n in regions:
        client = self.session.client('ec2', region_name=n)
        response = client.describe_security_groups()
        for m in response['SecurityGroups']:
            if "0.0.0.0/0" in str(m['IpPermissions']):
                for o in m['IpPermissions']:
                    try:
                        if int(o['FromPort']) <= 3306 <= int(o['ToPort']) and '0.0.0.0/0' in str(o['IpRanges']):
                            result = "Not Compliant"
                            failReason = "Found Security Group with port 3306 open to the world (0.0.0.0/0)"
                            offenders.append(str(m['GroupId']))
                    except:
                        if str(o['IpProtocol']) == "-1" and '0.0.0.0/0' in str(o['IpRanges']):
                            result = "Not Compliant"
                            failReason = "Found Security Group with port 3306 open to the world (0.0.0.0/0)"
                            offenders.append(str(n) + " : " + str(m['GroupId']))
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


def control_4_2_ensure_4333_not_open_to_world(self, regions):
    logger.info(" ---Inside networking_control_4 :: control_4_2_ensure_4333_not_open_to_world()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "4.2"
    description = "Ensure no security groups allow ingress from 0.0.0.0/0 to port 4333"
    scored = True
    for n in regions:
        client = self.session.client('ec2', region_name=n)
        response = client.describe_security_groups()
        for m in response['SecurityGroups']:
            if "0.0.0.0/0" in str(m['IpPermissions']):
                for o in m['IpPermissions']:
                    try:
                        if int(o['FromPort']) <= 4333 <= int(o['ToPort']) and '0.0.0.0/0' in str(o['IpRanges']):
                            result = "Not Compliant"
                            failReason = "Found Security Group with port 4333 open to the world (0.0.0.0/0)"
                            offenders.append(str(m['GroupId']))
                    except:
                        if str(o['IpProtocol']) == "-1" and '0.0.0.0/0' in str(o['IpRanges']):
                            result = "Not Compliant"
                            failReason = "Found Security Group with port 4333 open to the world (0.0.0.0/0)"
                            offenders.append(str(n) + " : " + str(m['GroupId']))
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 4.3 Ensure VPC flow logging is enabled in all VPCs (Scored)
def control_4_3_ensure_flow_logs_enabled_on_all_vpc(self, regions):
    logger.info(" ---Inside networking_control_4 :: control_4_3_ensure_flow_logs_enabled_on_all_vpc()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "4.3"
    description = "Ensure VPC flow logging is enabled in all VPCs"
    scored = True
    for n in regions:
        client = self.session.client('ec2', region_name=n)
        flowlogs = client.describe_flow_logs(
            #  No paginator support in boto atm.
        )
        activeLogs = []
        for m in flowlogs['FlowLogs']:
            if "vpc-" in str(m['ResourceId']):
                activeLogs.append(m['ResourceId'])
        vpcs = client.describe_vpcs(
            Filters=[
                {
                    'Name': 'state',
                    'Values': [
                        'available',
                    ]
                },
            ]
        )
        for m in vpcs['Vpcs']:
            if not str(m['VpcId']) in str(activeLogs):
                result = "Not Compliant"
                failReason = "VPC without active VPC Flow Logs found"
                offenders.append(str(n) + " : " + str(m['VpcId']))
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 4.4 Ensure the default security group of every VPC restricts all traffic (Scored)
def control_4_4_ensure_default_security_groups_restricts_traffic(self, regions):
    logger.info(" ---Inside networking_control_4 :: control_4_4_ensure_default_security_groups_restricts_traffic()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "4.4"
    description = "Ensure the default security group of every VPC restricts all traffic"
    scored = True
    for n in regions:
        client = self.session.client('ec2', region_name=n)
        response = client.describe_security_groups(
            Filters=[
                {
                    'Name': 'group-name',
                    'Values': [
                        'default',
                    ]
                },
            ]
        )
        for m in response['SecurityGroups']:
            if not (len(m['IpPermissions']) + len(m['IpPermissionsEgress'])) == 0:
                result = "Not Compliant"
                failReason = "Default security groups with ingress or egress rules discovered"
                offenders.append(str(n) + " : " + str(m['GroupId']))
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 4.5 Ensure routing tables for VPC peering are "least access" (Not Scored)
def control_4_5_ensure_route_tables_are_least_access(self, regions):
    logger.info(" ---Inside networking_control_4 :: control_4_5_ensure_route_tables_are_least_access()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "4.5"
    description = "Ensure routing tables for VPC peering are least access"
    scored = False
    for n in regions:
        client = self.session.client('ec2', region_name=n)
        response = client.describe_route_tables()
        for m in response['RouteTables']:
            for o in m['Routes']:
                try:
                    if o['VpcPeeringConnectionId']:
                        if int(str(o['DestinationCidrBlock']).split("/", 1)[1]) < 24:
                            result = "Not Compliant"
                            failReason = "Large CIDR block routed to peer discovered, please investigate"
                            offenders.append(str(n) + " : " + str(m['RouteTableId']))
                except:
                    pass
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 4.5 Ensure routing tables for VPC peering are "least access" (Not Scored)
def control_4_5_ensure_route_tables_are_least_access(self, regions):
    logger.info(" ---Inside networking_control_4 :: control_4_5_ensure_route_tables_are_least_access()--- ")
    """Summary

    Returns:
        TYPE: Description
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "4.5"
    description = "Ensure routing tables for VPC peering are least access"
    scored = False
    for n in regions:
        client = self.session.client('ec2', region_name=n)
        response = client.describe_route_tables()
        for m in response['RouteTables']:
            for o in m['Routes']:
                try:
                    if o['VpcPeeringConnectionId']:
                        if int(str(o['DestinationCidrBlock']).split("/", 1)[1]) < 24:
                            result = "Not Compliant"
                            failReason = "Large CIDR block routed to peer discovered, please investigate"
                            offenders.append(str(n) + " : " + str(m['RouteTableId']))
                except:
                    pass
    return {'Result': result, 'failReason': failReason, 'Offenders': offenders, 'ScoredControl': scored,
            'Description': description, 'ControlId': control}


# 4.6 ensure security group dont have large range of ports open
def control_4_6_ensure_sg_dont_have_large_range_of_ports_open(self, regions: list) -> dict:
    logger.info(" ---Inside networking_control_4 :: control_4_6_ensure_sg_dont_have_large_range_of_ports_open")

    """Summary
    
    Returns:
        TYPE: dict
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = "4.6"
    description = "Ensure security groups don't have large range of ports open"
    scored = True

    for region in regions:
        client = self.session.client('ec2', region_name=region)
        marker = ''
        while True:
            if marker == '' or marker is None:
                response = client.describe_security_groups()
            else:
                response = client.describe_security_groups(
                    NextToken=marker
                )
            for sg in response['SecurityGroups']:
                for port_range in sg['IpPermissions']:
                    try:
                        count = port_range['ToPort'] - port_range['FromPort']
                        if count > 1:
                            result = "Not Compliant"
                            failReason = "Found Security group with range of port open"
                            offenders.append(sg['GroupName'])
                            continue
                    except KeyError:
                        continue

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


# 4.7 Ensure use of https for cloudfront distributions
def control_4_7_use_https_for_cloudfront_distribution(self) -> dict:
    logger.info(" ---Inside networking_control_4 :: control_4_7_use_https_for_cloudfront_distribution")

    """Summary
    
    Returns:
        TYPE: dict
    """
    result = "Compliant"
    failReason = ""
    offenders = []
    control = '4.7'
    description = "Use https for cloudfront distributions"
    scored = True

    client = self.session.client('cloudfront')
    marker = ''
    while True:
        if marker == '' or marker == None:
            response = client.list_distributions()
        else:
            response = client.list_distributions(
                Marker=marker
            )
        try:
            for item in response['DistributionList']['Items']:
                protocol_policy = item['DefaultCacheBehavior']['ViewerProtocolPolicy']
                if protocol_policy == 'allow-all':
                    result = "Not Compliant"
                    failReason = "Found cloudfront distribution which accepts http also"
                    offenders.append(item['Id'])
                    continue

                try:
                    for cache_behaviour in item['CacheBehaviors']['Items']:
                        protocol_policy = cache_behaviour['ViewerProtocolPolicy']
                        if protocol_policy == 'allow-all':
                            result = "Not Compliant"
                            failReason = "Found cloudfront distribution which accepts http also"
                            offenders.append(item['Id'])
                            continue

                except KeyError:
                    pass
        except KeyError:
            break
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
