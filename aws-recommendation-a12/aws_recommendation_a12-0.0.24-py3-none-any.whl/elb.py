from botocore.exceptions import ClientError

from aws_recommendation_a12.utils import *


# Generate the recommendation for idle elastic load balancer
def idle_elastic_load_balancer(self):
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside elb :: idle_elastic_load_balancer()")

    recommendation = []
    regions = self.session.get_available_regions('elbv2')

    for region in regions:
        try:
            client = self.session.client('elbv2', region_name=region)
            marker = ''
            while True:
                if marker == '':
                    response = client.describe_load_balancers()
                else:
                    response = client.describe_load_balancers(
                        Marker=marker
                    )
                for lb in response['LoadBalancers']:
                    datapoints = get_metrics_stats(
                        self,
                        region=region,
                        namespace='AWS/EC2',
                        dimensions=[
                            {
                                'Name': 'LoadBalancerName',
                                'Value': lb['LoadBalancerName']
                            }
                        ],
                        metric_name='RequestCount',
                        stats=['Sum'],
                        unit=None
                    )
                    sum_request_count = 0
                    for datapoint in datapoints['Datapoints']:
                        sum_request_count = sum_request_count + datapoint['Sum']

                    recommend_flag = True
                    if sum_request_count >= 100:
                        recommend_flag = False

                    if recommend_flag:
                        tags_response = client.describe_tags(
                            ResourceArns=[
                                lb['LoadBalancerArn']
                            ]
                        )
                        try:
                            for tag in tags_response['TagDescriptions'][0]['Tags']:
                                if 'Role' in tag['Key']:
                                    recommend_flag = False
                        except TypeError:
                            pass
                        if recommend_flag:
                            temp = {
                                'Service Name': 'Elastic load balacer',
                                'Id': lb['LoadBalancerName'],
                                'Recommendation': 'Terminate Elastic Load Balancer',
                                'Description': 'The selected Elastic Load Balancer can be safely removed from the AWS account to reduce the ELB monthly costs.',
                                'Metadata': {
                                    'Region': region,
                                    'Type': lb['Type'],
                                    'Tags': tags_response['TagDescriptions'][0]['Tags'],
                                },
                                'Recommendation Reason': {
                                    'reason': "Load balancer is idle"
                                },
                                'Risk': 'High',
                                'Savings': None
                            }
                            recommendation.append(temp)

                try:
                    marker = response['NextMarker']
                    if marker == '':
                        break
                except KeyError:
                    break

        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied' or e.response['Error']['Code'] == 'AccessDeniedException':
                logger.info('---------ELB read access denied----------')
                temp = {
                    'Service Name': 'ELB',
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


# Generates the recommendation for unused elastic load balancer
def unused_elb(self) -> list:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside elb :: unused_elb()")

    recommendation = []
    regions = self.session.get_available_regions('elb')

    for region in regions:
        try:
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
                    try:
                        instances = response['Instances']
                    except KeyError:
                        temp = {
                            'Service Name': 'Elastic load balacer',
                            'Id': lb['LoadBalancerName'],
                            'Recommendation': 'Remove Unused ELB',
                            'Description': 'Identify unused Elastic Load Balancers, and delete them to help lower the cost of your monthly AWS bill.',
                            'Metadata': {
                                'Region': region,
                                # 'Type': lb['Type'],
                            },
                            'Recommendation Reason': {
                                'reason': 'The load balancer has 0 instances behind it'
                            },
                            'Risk': 'High',
                            'Savings': None
                        }
                        recommendation.append(temp)

                try:
                    marker = response['NextMarker']
                    if marker == '':
                        break
                except KeyError:
                    break

        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied' or e.response['Error']['Code'] == 'AccessDeniedException':
                logger.info('---------ELB read access denied----------')
                temp = {
                    'Service Name': 'ELB',
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
            logger.warning("Something went wrong with the region {}: {}".format(region, e))

    return recommendation