import json
import os

import boto3

from dynamodb import Table

def handler(event, context):

    FIRELENS_IMAGE_MAP = {
        'us-east-1': '906394416424.dkr.ecr.us-east-1.amazonaws.com/aws-for-fluent-bit:latest',
        'us-east-2': '906394416424.dkr.ecr.us-east-2.amazonaws.com/aws-for-fluent-bit:latest',
        'us-west-1': '906394416424.dkr.ecr.us-west-1.amazonaws.com/aws-for-fluent-bit:latest',
        'us-west-2': '906394416424.dkr.ecr.us-west-2.amazonaws.com/aws-for-fluent-bit:latest',
        'ap-east-1': '449074385750.dkr.ecr.ap-east-1.amazonaws.com/aws-for-fluent-bit:latest',
        'ap-south-1': '906394416424.dkr.ecr.ap-south-1.amazonaws.com/aws-for-fluent-bit:latest',
        'ap-northeast-2': '906394416424.dkr.ecr.ap-northeast-2.amazonaws.com/aws-for-fluent-bit:latest',
        'ap-southeast-1': '906394416424.dkr.ecr.ap-southeast-1.amazonaws.com/aws-for-fluent-bit:latest',
        'ap-southeast-2': '906394416424.dkr.ecr.ap-southeast-2.amazonaws.com/aws-for-fluent-bit:latest',
        'ap-northeast-1': '906394416424.dkr.ecr.ap-northeast-1.amazonaws.com/aws-for-fluent-bit:latest',
        'ca-central-1': '906394416424.dkr.ecr.ca-central-1.amazonaws.com/aws-for-fluent-bit:latest',
        'eu-central-1': '906394416424.dkr.ecr.eu-central-1.amazonaws.com/aws-for-fluent-bit:latest',
        'eu-west-1': '906394416424.dkr.ecr.eu-west-1.amazonaws.com/aws-for-fluent-bit:latest',
        'eu-west-2': '906394416424.dkr.ecr.eu-west-2.amazonaws.com/aws-for-fluent-bit:latest',
        'eu-west-3': '906394416424.dkr.ecr.eu-west-3.amazonaws.com/aws-for-fluent-bit:latest',
        'eu-north-1': '906394416424.dkr.ecr.eu-north-1.amazonaws.com/aws-for-fluent-bit:latest',
        'me-south-1': '741863432321.dkr.ecr.me-south-1.amazonaws.com/aws-for-fluent-bit:latest',
        'sa-east-1': '906394416424.dkr.ecr.sa-east-1.amazonaws.com/aws-for-fluent-bit:latest',
        'gov-east-1': '161423150738.dkr.ecr.us-gov-east-1.amazonaws.com/aws-for-fluent-bit:latest',
        'gov-west-1': '161423150738.dkr.ecr.us-gov-west-1.amazonaws.com/aws-for-fluent-bit:latest',
        'cn-north-1': '128054284489.dkr.ecr.cn-north-1.amazonaws.com.cn/aws-for-fluent-bit:latest',
        'cn-northwest-1': '128054284489.dkr.ecr.cn-northwest-1.amazonaws.com.cn/aws-for-fluent-bit:latest',
    }

    client = boto3.client('ecs')

    table = Table('REGISTRY_TABLE_NAME')

    # {
    #     "version": "0",
    #     "id": "13cde686-328b-6117-af20-0e5566167482",
    #     "detail-type": "ECR Image Action",
    #     "source": "aws.ecr",
    #     "account": "123456789012",
    #     "time": "2019-11-16T01:54:34Z",
    #     "region": "us-west-2",
    #     "resources": [],
    #     "detail": {
    #         "result": "SUCCESS",
    #         "repository-name": "my-repo",
    #         "image-digest": "sha256:7f5b2640fe6fb4f46592dfd3410c4a79dac4f89e4782432e0378abcd1234",
    #         "action-type": "PUSH",
    #         "image-tag": "latest"
    #     }
    # }

    for record in event['Records']:

        event = json.loads(record['body'])

        response = client.register_task_definition(
            family=event['detail']['image-tag'],
            taskRoleArn='arn:aws:iam::417984092495:role/ECSTaskRole',
            executionRoleArn='arn:aws:iam::417984092495:role/ECSExecutionRole',
            networkMode='awsvpc',
            containerDefinitions=[
                {
                    'name': 'task',
                    'image': f'{event["account"]}.dkr.ecr.{event["region"]}.amazonaws.com/{event["detail"]["repository-name"]}:{event["detail"]["image-tag"]}',
                    'cpu': 2048,
                    'memory': 4096,
                    'memoryReservation': 4046,
                    'essential': True,
                    'dependsOn': [
                        {
                            'containerName': 'logrouter',
                            'condition': 'START'
                        },
                    ],
                    'startTimeout': 30,
                    'stopTimeout': 30,
                    'privileged': False,
                    'logConfiguration': {
                        'logDriver': 'awsfirelens',
                        'options': {
                            'Name': 'firehose',
                            'region': event['region'],
                            'delivery_stream': os.getenv('LOG_STREAM_NAME'),
                        },
                    },
                },
                {
                    'name': 'logrouter',
                    'image': FIRELENS_IMAGE_MAP.get(event['region']),
                    'firelensConfiguration': {
                        'type': 'fluentbit',
                        'options': {
                            'config-file-type': 'file',
                            'config-file-value': '/fluent-bit/configs/parse-json.conf',
                        },
                    },
                    'essential': True,
                    'memoryReservation': 50,
                    'logConfiguration': {
                        'logDriver': 'awslogs',
                        'options': {
                            'awslogs-group': '/harbour/ecs/firelens',
                            'awslogs-region': os.getenv('AWS_REGION'),
                            'awslogs-create-group': 'true',
                            'awslogs-stream-prefix': 'task'
                        },
                    },
                },
            ],
            requiresCompatibilities=['EC2', 'FARGATE'],
            cpu="2048",
            memory="4096"
        )

        table.update(
            event['detail']['image-tag'],
            {
                'definition': {
                    'arn': response['taskDefinition']['taskDefinitionArn'],
                    'family': response['taskDefinition']['family'],
                    'revision': response['taskDefinition']['revision'],
                    'roles': {
                        'task': response['taskDefinition']['taskRoleArn'],
                        'execution': response['taskDefinition']['executionRoleArn'],
                    },
                    'requirements': [r['name'] for r in response['taskDefinition']['requiresAttributes']],
                    'compatibilities': response['taskDefinition']['compatibilities'],
                    'cpu': response['taskDefinition']['cpu'],
                    'memory': response['taskDefinition']['memory'],
                },
            },
        )
