from botocore.exceptions import ClientError

from aws_recommendation_a12.utils import *


# Generate the recommendation for enable s3 bucket keys
def enable_s3_bucket_keys(self) -> list:
    """
    :param self:
    :return:
    """
    logger.info(" ---Inside s3 :: enable_s3_bucket_keys()")

    recommendation = []

    client = self.session.client('s3')

    try:
        response = client.list_buckets()
    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied':
            logger.info('---------S3 read access denied----------')
            temp = {
                'Service Name': 'S3',
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
        else:
            temp = {
                'Service Name': 'S3',
                'Id': e.response['Error']['Code'],
                'Recommendation': e.response['Error']['Code'],
                'Description': e.response['Error']['Code'],
                'Metadata': {
                    e.response['Error']['Code']
                },
                'Recommendation Reason': {
                    e.response['Error']['Code']
                },
                'Risk': 'Low',
                'Savings': None
            }
            recommendation.append(temp)
        return recommendation

    for bucket in response['Buckets']:
        try:
            res = client.get_bucket_encryption(
                Bucket=bucket['Name']
            )
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                logger.info('---------S3 read access denied----------')
                temp = {
                    'Service Name': 'S3',
                    'Id': bucket['Name'],
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
            continue
        for rule in res['ServerSideEncryptionConfiguration']['Rules']:
            if rule['ApplyServerSideEncryptionByDefault']['SSEAlgorithm'] == 'aws:kms' and rule['BucketKeyEnabled']:
                temp = {
                    'Service Name': 'S3',
                    'Id': bucket['Name'],
                    'Recommendation': 'Enable s3 bucket keys',
                    'Description': 'Enable s3 bucket keys instead of KMS keys to optimize the aws cost',
                    'Metadata':{

                    },
                    'Recommendation Reason': {
                        # 'Average CPU Datapoints(7 days)': [float('{:.2f}'.format(x)) for x in tmp_lst_cpu]
                        'reason': 'KMS keys are used for encryption'
                    },
                    'Risk': 'Low',
                    'Savings': None
                }
                recommendation.append(temp)

    return recommendation


# Generate the recommendation for bucket versioning enabled
def s3_bucket_versioning_enabled(self):
    """
    :param self:
    :return dict: details of s3 bucket versioning enabled compliance.py
    """
    logger.info(" ---Inside s3 :: s3_bucket_versioning_enabled()")

    recommendation = []

    client = self.session.client('s3')
    try:
        response = client.list_buckets()
    except ClientError as e:
        if e.response['Error']['Code'] == 'AccessDenied':
            logger.info('---------S3 read access denied----------')
            temp = {
                'Service Name': 'S3',
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
        else:
            temp = {
                'Service Name': 'S3',
                'Id': e.response['Error']['Code'],
                'Recommendation': e.response['Error']['Code'],
                'Description': e.response['Error']['Code'],
                'Metadata': {
                    e.response['Error']['Code']
                },
                'Recommendation Reason': {
                    e.response['Error']['Code']
                },
                'Risk': 'Low',
                'Savings': None
            }
            recommendation.append(temp)
        return recommendation

    for bucket in response['Buckets']:
        bucket_name = bucket['Name']

        try:
            resp = client.get_bucket_versioning(
                Bucket=bucket_name,
            )
            status = resp['Status']
        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                logger.info('---------S3 read access denied----------')
                temp = {
                    'Service Name': 'S3',
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
            temp = {
                'Service Name': 'S3',
                'Id': bucket['Name'],
                'Recommendation': 'Enable S3 bucket versioning',
                'Description': 'Enable s3 bucket versioning',
                'Metadata': {

                },
                'Recommendation Reason': {
                    'reason': 'Bucket versioning is not enabled'
                },
                'Risk': 'Low',
                'Savings': None
            }
            recommendation.append(temp)
            continue
        except KeyError:
            temp = {
                'Service Name': 'S3',
                'Id': bucket['Name'],
                'Recommendation': 'Enable S3 bucket versioning',
                'Description': 'Enable s3 bucket versioning',
                'Metadata': {

                },
                'Recommendation Reason': {
                    'reason': 'Bucket versioning is not enabled'
                },
                'Risk': 'Low',
                'Savings': None
            }
            recommendation.append(temp)
            continue

        if not status == 'Enabled':
            temp = {
                'Service Name': 'S3',
                'Id': bucket['Name'],
                'Recommendation': 'Enable S3 bucket versioning',
                'Description': 'Enable s3 bucket versioning',
                'Metadata': {

                },
                'Recommendation Reason': {
                    'reason': 'Bucket versioning is not enabled'
                },
                'Risk': 'Low',
                'Savings': None
            }
            recommendation.append(temp)

    return recommendation


#Generate the recommendation for s3 lifecycle enabled
def s3_bucket_lifecycle_configuration(self)-> list:
    """
    :param self:
    :return dict: details of s3 bucket versioning enabled compliance.py
    """
    logger.info(" ---Inside s3 :: s3_bucket_lifecycle_configuration()")

    recommendation = []

    client = self.session.client('s3')
    try:
        response = client.list_buckets()

    except ClientError as e:
        print(e)
        if e.response['Error']['Code'] == 'AccessDenied':
            logger.info('---------S3 read access denied----------')
            temp = {
                'Service Name': 'S3',
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
        else:
            temp = {
                'Service Name': 'S3',
                'Id': e.response['Error']['Code'],
                'Recommendation': e.response['Error']['Code'],
                'Description': e.response['Error']['Code'],
                'Metadata': {
                    e.response['Error']['Code']
                },
                'Recommendation Reason': {
                    e.response['Error']['Code']
                },
                'Risk': 'Low',
                'Savings': None
            }
            recommendation.append(temp)
        return recommendation

    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        # print(bucket_name)
        try:
            resp = client.get_bucket_lifecycle_configuration(
                Bucket=bucket_name,
            )
            # print(resp)
            flag = False
            for rule in resp['Rules']:
                if rule['Status'] == 'Enabled':
                    flag = flag or True
                else:
                    flag = flag or False

            if not flag:
                temp = {
                    'Service Name': 'S3',
                    'Id': bucket['Name'],
                    'Recommendation': 'Add lifecycle rules to the bucket',
                    'Description': 'Add lifecycle rules to the bucket',
                    'Metadata': {

                    },
                    'Recommendation Reason': {
                        'reason': 'lifecycle rules are not there for s3 bucket'
                    },
                    'Risk': 'Low',
                    'Savings': None
                }
                recommendation.append(temp)

        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                logger.info('---------S3 read access denied----------')
                temp = {
                    'Service Name': 'S3',
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
            temp = {
                'Service Name': 'S3',
                'Id': bucket['Name'],
                'Recommendation': 'Add lifecycle rules to the bucket',
                'Description': 'Add lifecycle rules to the bucket',
                'Metadata': {

                },
                'Recommendation Reason': {
                    'reason': 'lifecycle rules are not there for s3 bucket'
                },
                'Risk': 'Low',
                'Savings': None
            }
            recommendation.append(temp)

    return recommendation