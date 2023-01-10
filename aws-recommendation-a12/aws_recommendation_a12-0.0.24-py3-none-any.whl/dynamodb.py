from botocore.exceptions import ClientError

from aws_recommendation_a12.utils import *


# generated the recommendations for unused dynamodb tables
def unused_dynamodb_tables(self) -> list:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside dynamodb :: unused_dynamodb_tables()")

    recommendation = []
    regions = self.session.get_available_regions('dynamodb')

    for region in regions:
        try:
            client = self.session.client('dynamodb', region_name=region)

            marker=''
            while True:
                if marker == '':
                    response = client.list_tables()
                else:
                    response = client.list_tables(
                        ExclusiveStartTableName=marker
                    )
                for table in response['TableNames']:
                    table_desc = client.describe_table(
                        TableName=table
                    )
                    if table_desc['Table']['ItemCount'] == 0:
                        temp = {
                            'Service Name': 'Dynamodb',
                            'Id': table,
                            'Recommendation': 'Remove Dynamodb table',
                            'Description': 'Identify any unused Amazon DynamoDB tables available within your AWS account and remove them to help lower the cost of your monthly AWS bill. A DynamoDB table is considered unused if it’s ItemCount parameter, which describes the number of items in the table, is equal to 0 (zero)',
                            'Metadata': {
                                'Region': region,
                                'TableStatus': table_desc['TableStatus']
                            },
                            'Recommendation Reason': {
                                'reason': "The ItemCount parameter value is 0, therefore the selected amazon dynamodb table is not currently in use and can be safely removed from your AWS Account"
                            },
                            'Risk': 'Medium',
                            'Savings': None
                        }
                        recommendation.append(temp)
                try:
                    marker = response['LastEvaluatedTableName']
                    if marker == '':
                        break
                except KeyError:
                    break
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied' or e.response['Error']['Code'] == 'AccessDeniedException':
                logger.warning(e)
                logger.info('---------Dynamodb read access denied----------')
                temp = {
                    'Service Name': 'DynamoDB',
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