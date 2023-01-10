from botocore.exceptions import ClientError

from aws_recommendation_a12.utils import *


#Generate the recommendation for log groups with no retention period
def log_group_retention_period_check(self) -> list:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside log_group_retention_period_check()")

    recommendation = []

    regions = self.session.get_available_regions('logs')

    for region in regions:
        try:
            client = self.session.client('logs', region_name=region)

            marker = ''
            while True:
                if marker == '':
                    response = client.describe_log_groups()
                else:
                    response = client.describe_log_groups(
                        nextToken=marker
                    )
                for group in response['logGroups']:
                    try:
                        retention_period = group['retentionInDays']
                        if retention_period <= 0:
                            temp = {
                                'Service Name': 'CloudWatch logs',
                                'Id': group['logGroupName'],
                                'Recommendation': 'Add retention period in log group',
                                'Description': 'Enabling the retention period will reduce the aws costs',
                                'Metadata': {
                                    'creation time': group['creationTime'],
                                    'arn': group['arn']
                                },
                                'Recommendation Reason': {
                                    'reason': 'Retention period is not set on the log group'
                                },
                                'Risk': 'Medium',
                                'Savings': None
                            }
                            recommendation.append(temp)
                    except KeyError:
                        temp = {
                            'Service Name': 'CloudWatch logs',
                            'Id': group['logGroupName'],
                            'Recommendation': 'Add retention period in log group',
                            'Description': 'Enabling the retention period will reduce the aws costs',
                            'Metadata': {
                                'creation time': group['creationTime'],
                                'arn': group['arn']
                            },
                            'Recommendation Reason': {
                                'reason': 'Retention period is not set on the log group'
                            },
                            'Risk': 'Medium',
                            'Savings': None
                        }
                        recommendation.append(temp)

                try:
                    marker = response['nextToken']
                    if marker == '':
                        break
                except KeyError:
                    break

        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied' or e.response['Error']['Code'] == 'AccessDeniedException':
                logger.info('---------Cloudwatch read access denied----------')
                temp = {
                    'Service Name': 'Cloudwatch',
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
            logger.warning("Something went wrong with the region {}: {}".format(region, e))

    return recommendation