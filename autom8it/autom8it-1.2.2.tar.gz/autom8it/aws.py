import datetime
import pytz
import boto3
import logging
from time import sleep
from autom8it import Log
from autom8it import AutomationTask

UTC = pytz.UTC

for log_name in ['boto', 'boto3', 'botocore', 's3transfer', 'urllib3']:
    logging.getLogger(log_name).setLevel(logging.WARNING)


class DeregisterTarget(AutomationTask):

    TARGET_GROUP_ARN_KEY = 'target_group_arn'
    TARGET_ID_KEY = 'target_id'
    PORT_KEY = 'port'

    aws_client = boto3.client('elbv2')

    def __init__(self, task_data: dict):
        super().__init__(task_data=task_data, check_done_interval=10)

    @property
    def validation_schema(self) -> dict:
        return {
            self.TARGET_GROUP_ARN_KEY: {
                'required': True,
                'type': 'string'
            },
            self.TARGET_ID_KEY: {
                'required': True,
                'type': 'string'
            },
            self.PORT_KEY: {
                'required': True,
                'type': 'integer'
            }
        }

    @property
    def task_type(self) -> str:
        return 'Deregister target'

    def do(self):
        target_group_desc = self.aws_client.deregister_targets(
            TargetGroupArn=self.get_task_attribute(self.TARGET_GROUP_ARN_KEY),
            Targets=[{
                'Id': self.get_task_attribute(self.TARGET_ID_KEY),
                'Port': self.get_task_attribute(self.PORT_KEY)
            }],
        )
        return target_group_desc

    def is_done(self) -> bool:
        target_id = self.get_task_attribute(self.TARGET_ID_KEY)
        target_group_desc = self.aws_client.describe_target_health(
            TargetGroupArn=self.get_task_attribute(self.TARGET_GROUP_ARN_KEY)
        )
        for target in target_group_desc['TargetHealthDescriptions']:
            if target['Target']['Id'] == target_id:
                Log.debug(f"Target {target_id} state: {target['TargetHealth']['State']}")
                return False

        return True


class RegisterTarget(DeregisterTarget):

    def __init__(self, task_data: dict):
        super().__init__(task_data=task_data)

    @property
    def task_type(self) -> str:
        return 'Register target'

    def do(self):
        target_group_desc = self.aws_client.register_targets(
            TargetGroupArn=self.get_task_attribute(self.TARGET_GROUP_ARN_KEY),
            Targets=[{
                'Id': self.get_task_attribute(self.TARGET_ID_KEY),
                'Port': self.get_task_attribute(self.PORT_KEY, 80)
            }],
        )
        return target_group_desc

    def is_done(self) -> bool:
        target_id = self.get_task_attribute(self.TARGET_ID_KEY)
        target_group_desc = self.aws_client.describe_target_health(
            TargetGroupArn=self.get_task_attribute(self.TARGET_GROUP_ARN_KEY)
        )
        for target in target_group_desc['TargetHealthDescriptions']:
            if target['Target']['Id'] == target_id:
                target_state = target['TargetHealth']['State']
                Log.debug(f"Target {target_id} state: {target_state}")
                if target_state in ['healthy']:
                    return True

        return False


class StopEC2Instance(AutomationTask):

    INSTANCE_ID_KEY = 'instance_id'

    @property
    def validation_schema(self) -> dict:
        return {
            self.INSTANCE_ID_KEY: {
                'required': True,
                'type': 'string'
            },
        }

    aws_client = boto3.client('ec2')

    def __init__(self, task_data: dict):
        super().__init__(task_data=task_data)

    @property
    def task_type(self) -> str:
        return 'Stop EC2 instance'

    def do(self):
        return self.aws_client.stop_instances(
            InstanceIds=[self.get_task_attribute(self.INSTANCE_ID_KEY)],
        )

    def is_done(self) -> bool:
        return self.is_state_equals(requested_state='stopped')

    def is_state_equals(self, requested_state: str) -> bool:
        instance_id = self.get_task_attribute(self.INSTANCE_ID_KEY)
        desc = self.aws_client.describe_instance_status(
            InstanceIds=[instance_id],
        )
        for data in desc['InstanceStatuses']:
            if data['InstanceId'] == instance_id:
                state = data['InstanceState']['Name']
                Log.debug(f"Instance {instance_id} state: {state}")
                if state in [requested_state]:
                    return True

        return False


class StartEC2Instance(StopEC2Instance):

    def __init__(self, task_data: dict):
        super().__init__(task_data=task_data)

    @property
    def task_type(self) -> str:
        return 'Start EC2 instance'

    def do(self):
        return self.aws_client.start_instances(
            InstanceIds=[self.get_task_attribute(self.INSTANCE_ID_KEY)],
        )

    def is_done(self) -> bool:
        return self.is_state_equals(requested_state='running')


class RebootEC2Instance(StopEC2Instance):

    def __init__(self, task_data: dict):
        super().__init__(task_data=task_data)

    @property
    def task_type(self) -> str:
        return 'Start EC2 instance'

    def do(self):
        resp = self.aws_client.reboot_instances(
            InstanceIds=[self.get_task_attribute(self.INSTANCE_ID_KEY)],
        )
        sleep(90.0)
        return resp

    def is_done(self) -> bool:
        return self.is_state_equals(requested_state='running')


class VerifyECSServicesCount(AutomationTask):

    CLUSTER_KEY = 'cluster'
    SERVICES_KEY = 'services'
    SERVICE_RUNNING_COUNT_KEY = 'runningCount'
    SERVICE_DESIRED_COUNT_KEY = 'desiredCount'

    @property
    def validation_schema(self) -> dict:
        return {
            self.CLUSTER_KEY: {
                'required': True,
                'type': 'string'
            },
            self.SERVICES_KEY: {
                'required': True,
                'type': 'list'
            },
        }

    ecs_client = boto3.client('ecs')

    def __init__(self, task_data: dict):
        super().__init__(task_data=task_data)

    @property
    def task_type(self) -> str:
        return 'Verify ECS services count'

    def describe_services(self) -> dict:
        return self.ecs_client.describe_services(
            cluster=self.get_task_attribute(self.CLUSTER_KEY),
            services=self.get_task_attribute(self.SERVICES_KEY),
        )

    def do(self):
        return 'OK'

    def is_done(self) -> bool:
        desc = self.describe_services()
        for service in desc[self.SERVICES_KEY]:
            desired_count = service[self.SERVICE_DESIRED_COUNT_KEY]
            running_count = service[self.SERVICE_RUNNING_COUNT_KEY]
            if desired_count != running_count:
                Log.debug(
                    f"Service {service['serviceName']} is not ready, "
                    f"desired count is {desired_count} but running count is {running_count}."
                )
                return False
        return True


class UpdateServicesWithLastRevision(VerifyECSServicesCount):

    def __init__(self, task_data: dict):
        super().__init__(task_data=task_data)

    @property
    def task_type(self) -> str:
        return 'Update ECS services with last revision'

    def do(self):
        result = []
        for service in self.get_task_attribute(self.SERVICES_KEY):

            desc = self.ecs_client.update_service(
                cluster=self.get_task_attribute(self.CLUSTER_KEY),
                service=service,
                taskDefinition=self._get_task_definition_family(service=service)
            )
            result.append(desc)

        return result

    def _get_task_definition_family(self, service: str) -> str:
        desc = self.ecs_client.describe_services(
            cluster=self.get_task_attribute(self.CLUSTER_KEY),
            services=[service]
        )
        services_desc = desc['services']
        Log.debug(f'Services description: {services_desc}')
        if len(services_desc) == 1:
            return services_desc[0]['taskDefinition'].split('/')[1].split(':')[0]
        else:
            raise ValueError(f'Expected only one service, got {len(services_desc)}.')

    def is_done(self) -> bool:
        return True


class ChangeTaskDefinitionContainerImage(AutomationTask):

    TASK_DEFINITION_KEY = 'task_definition'
    IMAGE_KEY = 'image'
    CONTAINER_DEFINITIONS_KEY = 'containerDefinitions'

    @property
    def validation_schema(self) -> dict:
        return {
            self.TASK_DEFINITION_KEY: {
                'required': True,
                'type': 'string'
            },
            self.IMAGE_KEY: {
                'type': 'string'
            }
        }

    aws_ecs_client = boto3.client('ecs')
    aws_ecr_client = boto3.client('ecr')

    def __init__(self, task_data: dict):
        super().__init__(task_data=task_data)

    @property
    def task_type(self) -> str:
        return 'Create ECS Task Definition revision'

    def do(self):
        desc = self.aws_ecs_client.describe_task_definition(
            taskDefinition=self.get_task_attribute(self.TASK_DEFINITION_KEY)
        )
        Log.debug(f'Task definition description: {desc}')
        container_definitions = desc['taskDefinition'][self.CONTAINER_DEFINITIONS_KEY]
        for container_def in container_definitions:
            image_uri = self.get_task_attribute(self.IMAGE_KEY, default=None)
            if image_uri is None:
                image_uri = self.get_last_image_tag(
                    repository=self.get_repository_name(image_uri=container_def[self.IMAGE_KEY])
                )
            if ':' not in image_uri:
                image_uri = f"{container_def[self.IMAGE_KEY].split(':')[0]}:{image_uri}"
            container_def[self.IMAGE_KEY] = image_uri

        task_definition_desc = desc.get('taskDefinition', {})

        result = self.aws_ecs_client.register_task_definition(
            family=self.get_task_attribute(self.TASK_DEFINITION_KEY),
            containerDefinitions=container_definitions,
            taskRoleArn=task_definition_desc.get('taskRoleArn', ''),
            executionRoleArn=task_definition_desc.get('executionRoleArn', ''),
            networkMode=task_definition_desc.get('networkMode'),
            volumes=task_definition_desc.get('volumes', []),
            placementConstraints=task_definition_desc.get('placementConstraints', []),
            requiresCompatibilities=task_definition_desc.get('requiresCompatibilities', [])
        )

        return result

    def is_done(self) -> bool:
        return True

    @staticmethod
    def get_repository_name(image_uri: str) -> str:
        """
        Example: 112358132134.dkr.ecr.us-east-2.amazonaws.com/my-repo:1.10.21-tag
        Will return my-repo
        :param image_uri:
        :return:
        """
        return image_uri.split('/')[1].split(':')[0]

    @staticmethod
    def get_last_image_tag(repository: str) -> str:
        result = ChangeTaskDefinitionContainerImage.aws_ecr_client.describe_images(
            repositoryName=repository
        )
        images = {image['imageTags'][0]: image['imagePushedAt'] for image in result['imageDetails']}
        last_date = datetime.datetime(year=1970, month=1, day=1).replace(tzinfo=UTC)
        last_tag = None
        for tag, date in images.items():
            date = date.replace(tzinfo=UTC)
            if date > last_date:
                last_date = date
                last_tag = tag
        return last_tag


class StopServicesAndWaitUntilStarts(VerifyECSServicesCount):

    def __init__(self, task_data: dict):
        super().__init__(task_data=task_data)

    @property
    def task_type(self) -> str:
        return 'Stop all task of ECS services wait until they starts again'

    def stop_tasks(self, tasks_arn: list):
        for task_arn in tasks_arn:
            self.ecs_client.stop_task(
                cluster=self.get_task_attribute(self.CLUSTER_KEY),
                task=task_arn,
                reason=f'Stopping service by Autom8it ({self.__class__.__name__})'
            )

    def do(self):
        result = []
        for service in self.get_task_attribute(self.SERVICES_KEY):

            desc = self.ecs_client.list_tasks(
                cluster=self.get_task_attribute(self.CLUSTER_KEY),
                serviceName=service,
                desiredStatus='RUNNING',
            )
            tasks_arn = desc.get('taskArns', [])
            self.stop_tasks(tasks_arn=tasks_arn)
            result.append(tasks_arn)

        return result
