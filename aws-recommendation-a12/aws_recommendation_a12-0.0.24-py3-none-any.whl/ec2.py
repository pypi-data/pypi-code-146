import botocore
import pytz
from botocore.exceptions import ClientError

from aws_recommendation_a12.utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# Generates recommendation to delete idle instances
def delete_or_downsize_instance_recommendation(self) -> list:
    logger.info(" ---Inside delete_or_downsize_instance_recommendation()")

    recommendation = []
    regions = self.session.get_available_regions('ec2')

    # iterating through all the available regions
    for region in regions:
        try:
            instance_lst = list_instances(self, region)

            for instance in instance_lst:
                response_cpu = get_metrics_stats(self, region, "AWS/EC2", [{'Name': 'InstanceId', 'Value': instance['InstanceId']}])
                # response_mem = get_metics_stats(session, region, "AWS/EC2", {'Name': 'InstanceId', 'Value': instance},
                # metric_name=) response_net_in = get_metrics_stats(region, "AWS/EC2", [{'Name': 'InstanceId',
                # 'Value': instance}], metric_name='NetworkIn') response_net_out = get_metrics_stats(region, "AWS/EC2",
                # [{'Name': 'InstanceId', 'Value': instance}], metric_name='NetworkOut') # print(response_net_in) print(
                # response_net_out) for r in response_net_in['Datapoints']: print(r['Average'])

                tmp_lst_cpu = []

                for r in response_cpu['Datapoints']:
                    tmp_lst_cpu.append(r['Average'])

                if len(tmp_lst_cpu) >= 7:
                    if max(tmp_lst_cpu) < 3:
                        try:
                            tags = instance['Tags']
                        except KeyError:
                            tags = None
                        temp = {
                            'Service Name': 'EC2 Instance',
                            'Id': instance['InstanceId'],
                            'Recommendation': 'Delete idle compute instance',
                            'Description': 'The Delete idle compute instances recommendation indicates that some compute instances are unused. Deleting unused compute instances saves you from paying for instances that you are not using.',
                            'Metadata': {
                                'Region': region,
                                'Instance Type': instance['InstanceType'],
                                'Tags': tags,
                                'LaunchTime': instance['LaunchTime']
                            },
                            'Recommendation Reason': {
                                'Average CPU Datapoints(7 days)': [float('{:.2f}'.format(x)) for x in tmp_lst_cpu]
                            },
                            'Risk': 'High',
                            'Savings': None
                        }
                        recommendation.append(temp)
                    else:
                        avg = 0
                        for v in tmp_lst_cpu:
                            avg = avg + v
                        avg = avg / len(tmp_lst_cpu)

                        if avg < 5:
                            try:
                                tags = instance['Tags']
                            except KeyError:
                                tags = None
                            temp = {
                                'Service Name': 'EC2 Instance',
                                'Id': instance['InstanceId'],
                                'Recommendation': 'Downsize underutilized compute instances',
                                'Description': 'The Downsize underutilized compute instances recommendation indicates that some compute instances are bigger than needed. Implementing this recommendation saves you money without degrading performance.',
                                'Metadata': {
                                    'Region': region,
                                    'Instance Type': instance['InstanceType'],
                                    'Tags': tags,
                                    'LaunchTime': instance['LaunchTime']
                                },
                                'Recommendation Reason': {
                                    'Average CPU Datapoints(7 days)': [float('{:.2f}'.format(x)) for x in tmp_lst_cpu]
                                },
                                'Risk': 'High',
                                'Savings': None
                            }
                            recommendation.append(temp)

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'UnauthorizedOperation':
                logger.info('---------Ec2 read access denied----------')
                temp = {
                    'Service Name': 'EC2',
                    'Id': 'Access Denied',
                    'Recommendation': 'Access Denied',
                    'Description': 'Access Denied',
                    'Metadata': {
                        'Access Denied'
                    },
                    'Recommendation Reason': {
                        'Access Denied'
                    },
                    'Risk': 'High',
                    'Savings': None
                }
                recommendation.append(temp)
                return recommendation
            logger.info("Something wrong with the region {}: {}".format(region, e))

    return recommendation


# generates the recommendation to delete unattached volumes
def purge_unattached_vol_recommendation(self) -> list:
    logger.info(" ---Inside purge_unattached_vol_recommendation()")

    recommendation = []
    regions = self.session.get_available_regions('ec2')

    # iterating through all the available regions
    for region in regions:
        try:
            vol_data = {}
            client = self.session.client('ec2', region_name=region)
            marker = ''
            while True:
                response = client.describe_volumes(
                    MaxResults=500,
                    NextToken=marker
                )
                for item in response['Volumes']:
                    create_time = item['CreateTime']
                    datetime_4_weeks_ago = dt.datetime.now() - dt.timedelta(weeks=4)
                    timezone = pytz.timezone("UTC")
                    datetime_4_weeks_ago = timezone.localize(datetime_4_weeks_ago)

                    older = create_time <= datetime_4_weeks_ago
                    if older:
                        # vol_data[item['VolumeId']] = item['Attachments']
                        if len(item['Attachments']) == 0:
                            try:
                                tags = item['Tags']
                            except KeyError:
                                tags = None
                            temp = {
                                'Service Name': 'Volume',
                                'Id': item['VolumeId'],
                                'Recommendation': 'Purge unattached volume',
                                'Description': 'The Delete unattached volumes recommendation indicates that unattached volumes exists. Attaching or deleting unattached volumes reduces costs.',
                                'Metadata': {
                                    'Region': region,
                                    'Instance Type': item['VolumeType'],
                                    'Tags': tags,
                                    'CreateTime': item['CreateTime']
                                },
                                'Recommendation Reason': {
                                    'reason': 'This Volume is 4 weeks older and is not attached to any instance'
                                },
                                'Risk': 'Medium',
                                'Savings': None
                            }
                            recommendation.append(temp)
                try:
                    marker = response['NextToken']
                    if marker == '':
                        break
                except KeyError:
                    break

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'UnauthorizedOperation':
                logger.info('---------Ec2 read access denied----------')
                temp = {
                    'Service Name': 'EC2',
                    'Id': 'Access Denied',
                    'Recommendation': 'Access Denied',
                    'Description': 'Access Denied',
                    'Metadata': {
                        'Access Denied'
                    },
                    'Recommendation Reason': {
                        'Access Denied'
                    },
                    'Risk': 'Medium',
                    'Savings': None
                }
                recommendation.append(temp)
                return recommendation
            logger.info("Something wrong with the region {}: {}".format(region, e))

    return recommendation


# Generates the recommendation to purge the snapshots which are older than 8 weeks
def purge_8_weeks_older_snapshots(self) -> list:
    logger.info(" ---Inside purge_8_weeks_older_snapshots()")

    recommendation = []
    regions = self.session.get_available_regions('ec2')

    datetime_8_weeks_ago = dt.datetime.now() - dt.timedelta(weeks=8)
    timezone = pytz.timezone("UTC")
    datetime_8_weeks_ago = timezone.localize(datetime_8_weeks_ago)

    for region in regions:
        try:
            client = self.session.client('ec2', region_name=region)
            marker = ''
            while True:
                response = client.describe_snapshots(
                    MaxResults=1000,
                    OwnerIds=['self'],
                    NextToken=marker
                )
                for snapshot in response['Snapshots']:
                    start_time = snapshot['StartTime']
                    older = start_time <= datetime_8_weeks_ago

                    if older:
                        service_name = 'Snanshot'
                        r_id =  snapshot['SnapshotId']
                        recom = 'Purge 8 week older snapshot'
                        desc = 'The Delete 8 weeks older snapshot recommendation indicates that snapshots is older than 8 weeks exists. Deleting older snapshots reduces costs.'

                        try:
                            tags = snapshot['Tags']
                        except KeyError:
                            tags = None

                        metadata = {
                            'Region': region,
                            # 'StorageTier': snapshot['StorageTier'],
                            'Tags': tags,
                            'CreateTime': snapshot['StartTime']
                        }
                        reason = {
                            'This snapshot is 8 weeks older'
                        }
                        temp = {
                            'Service Name': service_name,
                            'Id': r_id,
                            'Recommendation': recom,
                            'Description': desc,
                            'Metadata': metadata,
                            'Recommendation Reason': reason,
                            'Risk': 'Low',
                            'Savings': None
                        }
                        recommendation.append(temp)

                try:
                    marker = response['NextToken']
                    if marker == '':
                        break
                except KeyError:
                    break
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'UnauthorizedOperation':
                logger.info('---------Ec2 read access denied----------')
                temp = {
                    'Service Name': 'EC2',
                    'Id': 'Access Denied',
                    'Recommendation': 'Access Denied',
                    'Description': 'Access Denied',
                    'Metadata': {
                        'Access Denied'
                    },
                    'Recommendation Reason': {
                        'Access Denied'
                    },
                    'Risk': 'Low',
                    'Savings': None
                }
                recommendation.append(temp)
                return recommendation
            logger.info("Something wrong with the region {}: {}".format(region, e))
    return recommendation


# Generates the recommendations fot amazon ec2 reserved instance lease expiration
def reserved_instance_lease_expiration(self) -> list:
    """

    :param self:
    :return list: list of recommendations for reserved instances for lease expiration
    """
    logger.info(' ---Inside ec2 :: reserved_instance_lease_expiration()')

    recommendation = []
    regions = self.session.get_available_regions('ec2')

    datetime_now = dt.datetime.utcnow()
    timezone = pytz.timezone("UTC")
    datetime_30_days_ago = timezone.localize(datetime_now - dt.timedelta(days=30))

    datetime_30_days_after = timezone.localize(datetime_now + dt.timedelta(days=30))

    for region in regions:
        try:
            client = self.session.client('ec2', region_name=region)
            response = client.describe_reserved_instances()

            for instance in response['ReservedInstances']:
                expiry_date = instance['End']
                if datetime_30_days_ago <= expiry_date <= datetime_30_days_after:
                    try:
                        tags = instance['Tags']
                    except KeyError:
                        tags = None
                    temp = {
                        'Service Name': 'EC2 Instance',
                        'Id': instance['ReservedInstancesId'],
                        'Recommendation': 'Consider purchasing a new reserved instance',
                        'Description': 'Checks for Amazon EC2 Reserved Instances that are scheduled to expire within the next 30 days, or have expired in the preceding 30 days.',
                        'Metadata': {
                            'Region': region,
                            'Zone': instance['AvailabilityZone'],
                            'Status': instance['State'],
                            'Instance Type': instance['InstanceType'],
                            'Tags': tags,
                            'Expiration Date': expiry_date
                        },
                        'Recommendation Reason': {
                            'Reason': 'The Instance is either expired within 30 days or will be expiring in next 30 days'
                        },
                        'Risk': 'High',
                        'Savings': None
                    }
                    recommendation.append(temp)

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'UnauthorizedOperation':
                logger.info('---------Ec2 read access denied----------')
                temp = {
                    'Service Name': 'EC2',
                    'Id': 'Access Denied',
                    'Recommendation': 'Access Denied',
                    'Description': 'Access Denied',
                    'Metadata': {
                        'Access Denied'
                    },
                    'Recommendation Reason': {
                        'Access Denied'
                    },
                    'Risk': 'High',
                    'Savings': None
                }
                recommendation.append(temp)
                return recommendation
            logger.error("Something went wrong with the region {}: {}".format(region, e))

    return recommendation


# Generated recommendations for unassociated elastic IP addresses
def unassociated_elastic_ip_addresses(self) -> list:
    """

    :param self:
    :return list: list of recommendations for unassociated elastic ip addresses
    """
    logger.info(" ---Inside ec2 :: unassociated_elastic_ip_addresses()")

    recommendation = []
    regions = self.session.get_available_regions('ec2')

    for region in regions:
        try:
            client = self.session.client('ec2', region_name=region)
            response = client.describe_addresses()

            for eip in response['Addresses']:
                try:
                    association = eip['AssociationId']
                except KeyError:
                    try:
                        tags = eip['Tags']
                    except KeyError:
                        tags = None
                    temp = {
                        'Service Name': 'EIP',
                        'Id': eip['AllocationId'],
                        'Recommendation': 'Associate the EIP with a running active instance, or release the unassociated EIP',
                        'Description': 'Checks for Elastic IP addresses (EIPs) that are not associated with a running Amazon Elastic Compute Cloud (Amazon EC2) instance.',
                        'Metadata': {
                            'Region': region,
                            'IP address': eip['PublicIp'],
                            'Tags': tags
                        },
                        'Recommendation Reason': {
                            'Reason': 'An allocated Elastic IP address (EIP) is not associated with a running Amazon EC2 instance'
                        },
                        'Risk': 'Low',
                        'Savings': '$3.65'
                    }
                    recommendation.append(temp)

        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == 'UnauthorizedOperation':
                logger.info('---------Ec2 read access denied----------')
                temp = {
                    'Service Name': 'EC2',
                    'Id': 'Access Denied',
                    'Recommendation': 'Access Denied',
                    'Description': 'Access Denied',
                    'Metadata': {
                        'Access Denied'
                    },
                    'Recommendation Reason': {
                        'Access Denied'
                    },
                    'Risk': 'Low',
                    'Savings': None
                }
                recommendation.append(temp)
                return recommendation
            logger.error("Something went wrong with the region {}: {}".format(region, e))

    return recommendation


# Generates the recommendations for unused AMI
def unused_ami(self) -> list:
    """
    :param self:
    :return:
    """
    logger.info(' ---Inside ec2 :: unused_ami()')

    recommendation = []
    regions = self.session.get_available_regions('ec2')

    for region in regions:
        try:
            client = self.session.client('ec2', region_name=region)

            marker = ''
            while True:
                if marker == '':
                    response_ami = client.describe_images(
                        Owners=['self']
                    )
                else:
                    response_ami = client.describe_images(
                        Owners=['self'],
                        NextToken=marker
                    )

                for image in response_ami['Images']:
                    response_ec2 = client.describe_instances(
                        Filters=[
                            {
                                'Name': 'image-id',
                                'Values': [image['ImageId']]
                            }
                        ]
                    )
                    if len(response_ec2['Reservations']) == 0:
                        try:
                            tags = image['Tags']
                        except KeyError:
                            tags = None
                            
                        temp = {
                            'Service Name': 'EC2 AMI',
                            'Id': image['ImageId'],
                            'Recommendation': 'Remove AMI',
                            'Description': 'Find any unused Amazon Machine Images available in your AWS account and remove them in order to lower the cost of your monthly AWS bill',
                            'Metadata': {
                                'Region': region,
                                'Public': image['Public'],
                                'ImageType': image['ImageType'],
                                'Tags': tags,
                            },
                            'Recommendation Reason': {
                                'Reason': 'AMI is not used anymore and can be safely removed'
                            },
                            'Risk': 'Low',
                            'Savings': None
                        }
                try:
                    marker = response_ami['NextToken']
                    if marker == '':
                        break
                except KeyError:
                    break

        except ClientError as e:
            if e.response['Error']['Code'] == 'UnauthorizedOperation':
                logger.info('---------EC2 read access denied----------')
                temp = {
                    'Service Name': 'EC2',
                    'Id': 'Access Denied',
                    'Recommendation': 'Access Denied',
                    'Description': 'Access Denied',
                    'Metadata': {
                        'Access Denied'
                    },
                    'Recommendation Reason': {
                        'Access Denied'
                    },
                    'Risk': 'Low',
                    'Savings': None
                }
                recommendation.append(temp)
                return recommendation
            logger.warning("Something went wrong with the region {}: {}".format(region, e))

    return recommendation