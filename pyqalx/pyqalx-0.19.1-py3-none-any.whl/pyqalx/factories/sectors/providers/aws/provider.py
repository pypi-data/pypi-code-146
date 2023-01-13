import logging
import os
from io import StringIO

import boto3
import requests
from botocore.exceptions import ClientError
from colorama import Fore
from troposphere import Tags

from pyqalx.core.errors import QalxFactoryError
from pyqalx.factories.sectors.providers.aws.stack import AWSStack
from pyqalx.factories.sectors.providers.provider import BaseProvider


class AWSProvider(BaseProvider):
    """
    A provider subclass that provides interaction with AWS
    """

    _type = "aws"

    FORE = Fore.YELLOW
    REGION_NAME_KEY = "region_name"
    PROFILE_NAME_KEY = "profile_name"
    CREATE_COMPLETE = "CREATE_COMPLETE"
    CREATE_FAILED = "CREATE_FAILED"
    ROLLBACK_IN_PROGRESS = "ROLLBACK_IN_PROGRESS"
    ROLLBACK_FAILED = "ROLLBACK_FAILED"
    ROLLBACK_COMPLETE = "ROLLBACK_COMPLETE"
    DELETE_IN_PROGRESS = "DELETE_IN_PROGRESS"
    DELETE_FAILED = "DELETE_FAILED"
    DELETE_COMPLETE = "DELETE_COMPLETE"

    @staticmethod
    def _identity_document():
        """
        Gets the identity document from the EC2 instance. Certain parameters
        can only be looked up from within the instance (i.e. the default region)
        """
        resp = requests.get(
            "http://169.254.169.254/latest/dynamic/instance-identity/document"
        )
        if resp.ok:
            return resp.json()
        else:
            raise QalxFactoryError(
                f"Error getting " f"identity document: {resp.reason}"
            )

    @staticmethod
    def _get_region():
        """
        Helper for getting the region for remote instances
        """
        return AWSProvider._identity_document()["region"]

    @staticmethod
    def default_profile_name():
        return boto3.session.Session().profile_name

    @staticmethod
    def default_region_name(validate, log):
        session = boto3.session.Session()
        if validate and session.region_name is None:
            # Ensure that when building the local machine has AWS configured
            # properly
            msg = (
                "Must configure the default"
                f" `region_name` for `{AWSProvider._type}`. "
                f"See https://docs.aws.amazon.com/cli/"
                f"latest/reference/configure/#examples"
            )
            AWSProvider._send_message(
                title="all", message=msg, level=logging.ERROR, log=log
            )
            raise QalxFactoryError(msg)
        return session.region_name or AWSProvider._get_region()

    @property
    def ERRORED_STATUSES(self):
        return [
            self.CREATE_FAILED,
            self.ROLLBACK_IN_PROGRESS,
            self.ROLLBACK_FAILED,
            self.ROLLBACK_COMPLETE,
            self.DELETE_IN_PROGRESS,
            self.DELETE_FAILED,
            self.DELETE_COMPLETE,
        ]

    @property
    def CREATED_STATUS(self):
        return self.CREATE_COMPLETE

    @property
    def DELETED_STATUSES(self):
        return [self.DELETE_COMPLETE, self.DELETE_FAILED]

    def _get_client(self, service_name="cloudformation"):
        session = boto3.session.Session(
            profile_name=self.profile_name, region_name=self.region_name
        )
        return session.client(service_name)

    @staticmethod
    def _update_termination_protection(client, enabled, stack_id):
        client.update_termination_protection(
            EnableTerminationProtection=enabled, StackName=stack_id
        )

    @staticmethod
    def _simulate_principal_policy(
        client, session, action_names, resource_arns
    ):
        """
        Helper for simulating the policy for the calling user
        :param session: An instance of ~boto3.session.Session
        :param action_names: A list of action names to simulate
        :param resource_arns: A list of resource arns to simulate
        :return: The response from boto3
        """
        caller_identity = session.client("sts").get_caller_identity()

        resp = client.simulate_principal_policy(
            PolicySourceArn=caller_identity["Arn"],
            ActionNames=action_names,
            ResourceArns=resource_arns,
        )
        return resp

    @staticmethod
    def validate_permissions(profile_name, region_name, log):
        """
        Validates that the calling user has permission to create the
        resources required for the stack
        """
        session = boto3.session.Session(
            profile_name=profile_name, region_name=region_name
        )
        # A list of tuples of <action_names>, <resource_arns> to check
        # the user permission for.
        policies = [
            (
                [
                    "cloudformation:CreateStack",
                    "cloudformation:DeleteStack",
                    "cloudformation:DescribeStacks",
                    "cloudformation:DescribeStackEvents",
                    "cloudformation:UpdateTerminationProtection",
                    "cloudwatch:PutMetricData",
                    "ec2:CreateTags",
                    "ec2:DescribeImages",
                    "ec2:DescribeInstances",
                    "ec2:TerminateInstances",
                    "secretsmanager:CreateSecret",
                    "secretsmanager:TagResource",
                    "ssm:AddTagsToResource",
                    "ssm:PutParameter",
                    "ssm:DeleteParameter",
                    "secretsmanager:DeleteSecret",
                ],
                ["*"],
            ),
            (
                [
                    "iam:AddRoleToInstanceProfile",
                    "iam:CreateInstanceProfile",
                    "iam:CreateRole",
                    "iam:DeleteInstanceProfile",
                    "iam:DeleteRole",
                    "iam:DeleteRolePolicy",
                    "iam:GetInstanceProfile",
                    "iam:GetRole",
                    "iam:GetRolePolicy",
                    "iam:PassRole",
                    "iam:PutRolePolicy",
                    "iam:TagRole",
                    "iam:RemoveRoleFromInstanceProfile",
                ],
                ["arn:aws:iam::*:instance-profile/*", "arn:aws:iam::*:role/*"],
            ),
            (
                ["ec2:RunInstances"],
                [
                    "arn:aws:ec2:*:*:security-group/*",
                    "arn:aws:ec2:*::image/*",
                    "arn:aws:ec2:*:*:instance/*",
                ],
            ),
            (
                [
                    "cloudwatch:EnableAlarmActions",
                    "cloudwatch:DeleteAlarms",
                    "cloudwatch:DisableAlarmActions",
                    "cloudwatch:PutMetricAlarm",
                ],
                ["arn:aws:cloudwatch:*:*:alarm:*"],
            ),
        ]

        results = []
        try:
            client = session.client("iam")
            for action_names, resource_arns in policies:
                resp = AWSProvider._simulate_principal_policy(
                    session=session,
                    client=client,
                    action_names=action_names,
                    resource_arns=resource_arns,
                )
                results += resp["EvaluationResults"]
        except ClientError as exc:
            # ClientError: Problem with calling AWS.  Possibly due to the user
            #              not having permission to `simulate_principal_policy
            AWSProvider._send_message(
                title="all", message=str(exc), level=logging.ERROR, log=log
            )
            raise QalxFactoryError(exc)
        missing_permissions = {}
        for result in results:
            decision = result["EvalDecision"]
            if decision != "allowed":
                missing_permissions[result["EvalActionName"]] = decision

        if missing_permissions:
            formatted_permissions = "\n ".join(
                [
                    f"{action} - {decision},"
                    for action, decision in missing_permissions.items()
                ]
            )

            msg = (
                f"Profile `{profile_name}` on region `{region_name}` is "
                f"missing the following permissions required to create"
                f" factories:\n {formatted_permissions}"
            )
            AWSProvider._send_message(
                title="all", message=msg, level=logging.ERROR, log=log
            )
            raise QalxFactoryError(msg)

    def _create_stack(self, stack):
        """
        Creates the Cloudformation Stack for the given template.  Uploads
        the stack as a file Item to allow us to take advantage of the larger
        file size allowed when using TemplateURL.  This item will be
        automatically deleted when the factory is deleted.
        :param stack:
        :return:
        """
        stack_name = self._stack_name()
        client = self._get_client()
        item = self.factory.session.item.add(
            source=StringIO(stack),
            file_name=self.factory._plan_name,
            meta=self.factory._metadata(self.factory.entity),
        )
        on_failure = (
            "DELETE"
            if self.factory._plan_debug._demolish_on_failure
            else "DO_NOTHING"
        )
        try:
            resp = client.create_stack(
                StackName=stack_name,
                TemplateURL=item.file.url,
                OnFailure=on_failure,
                EnableTerminationProtection=True,
                Capabilities=["CAPABILITY_NAMED_IAM"],
                Tags=Tags(*AWSStack(self)._resource_tags(stack_name)).to_dict(),
            )
        except ClientError as exc:
            # ClientError: There was some sort of issue when
            #              we tried to create the stack.  Record this error and
            #              the manager will ensure that any previous stack
            #              gets deleted.
            self._msg_user(str(exc), level=logging.ERROR)
            return
        self.stack_id = resp["StackId"]
        return self.stack_id

    def _describe_stack(self):
        client = self._get_client()
        try:
            resp = client.describe_stacks(StackName=self.stack_id)
        except ClientError:  # pragma: no cover
            # ClientError: The stack can't be found at all.
            #              This may be because it has been deleted
            return None
        return resp["Stacks"][0]["StackStatus"]

    def _describe_images(self, image_ids):
        """
        Gets the images for the given image_ids so that we can determine
        the platform of the image
        """
        client = self._get_client("ec2")
        try:
            resp = client.describe_images(
                Filters=[{"Name": "image-id", "Values": image_ids}]
            )["Images"]
        except ClientError as exc:
            # ClientError: Some issue communicating with AWS
            self._msg_user(str(exc), level=logging.ERROR)
            return None
        return resp

    @staticmethod
    def _paginated_response(client, list_method, list_key):
        """
        For the given boto3 client and list_method will continue querying AWS
        until `NextToken` is not on the response (meaning we are at the end
        of the pagination)

        :param client: An instance of ~boto3.client
        :param list_method:The list method to use to query AWS
        :param list_key:The key that the response data resides in
        :return:yields an individual response
        """
        # Can't do partial matching, so need them all.
        # Don't catch potential exceptions - this needs to error if
        # there is a problem so that the instance shuts down
        _list_method = getattr(client, list_method)
        parameters = _list_method()
        end = False
        while not end:
            for _p in parameters[list_key]:
                yield _p
            next_token = parameters.get("NextToken")
            if next_token:
                parameters = _list_method(NextToken=next_token)
            else:
                end = True

    def _set_environment_variable(
        self,
        instance_name,
        name,
        client,
        get_method,
        get_kwarg,
        get_key,
        response_key=None,
    ):
        """
        For the given client and get_method will query AWS and return the single
        object (if the name starts with the instance_name).  It will then save
        that as an environment variable
        :param name: The name of the object to lookup
        :param client: An instance of ~boto3.client
        :param get_method: The get method to use to query AWS
        :param get_kwarg: The argument to use when calling the get_method
        :param get_key:The key in the response that the value of the object
                       resides in
        :param response_key: Optional response key in case the returning object
                             is a nested dict
        """
        if name.startswith(instance_name):
            # Qalx parameters will start with the factory guid
            # Don't catch potential exceptions.  This needs to error so that
            # the instance shuts down.
            _variable = getattr(client, get_method)(**{get_kwarg: name})
            # Handle the response being a nested dict
            _variable = _variable.get(response_key, _variable)
            environment_variable_name = self.factory._environment_variable_key(
                name
            )
            os.environ[environment_variable_name] = _variable[get_key]

    def set_environment_variables(self, instance_name):
        """
        Gets ALL the SSM Parameters and Secrets from SecretsManager.
        Iterates through the pages and then sets the ones that start with the
        instance_name as environment variables.  The parameters/secrets are
        created on the Troposphere stack at factory build time.  Uses the
        permissions on the instance role.

        :param instance_name: The name of the instance that was used to create
        the parameters at stack creation.  As parameters are namespace as
        `<<instance_name>_PARAMETER` the name is required to ensure
        the correct parameter is loaded for the instance doing the bootstrapping
        """
        # Will use the role of the instance for permissions
        ssm = self._get_client("ssm")
        for parameter in self._paginated_response(
            client=ssm, list_method="describe_parameters", list_key="Parameters"
        ):
            self._set_environment_variable(
                instance_name=instance_name,
                name=parameter["Name"],
                client=ssm,
                get_method="get_parameter",
                get_kwarg="Name",
                get_key="Value",
                response_key="Parameter",
            )

        secretsmanager = self._get_client("secretsmanager")

        for secret in self._paginated_response(
            client=secretsmanager,
            list_method="list_secrets",
            list_key="SecretList",
        ):
            self._set_environment_variable(
                instance_name=instance_name,
                name=secret["Name"],
                client=secretsmanager,
                get_method="get_secret_value",
                get_kwarg="SecretId",
                get_key="SecretString",
            )

    def _delete_stack(self, stack_id):
        client = self._get_client()
        self._update_termination_protection(
            client=client, stack_id=stack_id, enabled=False
        )
        client.delete_stack(StackName=stack_id)
        return

    def _get_error_reason(self):
        client = self._get_client()
        reasons = []
        events = {"StackEvents": []}
        try:
            events = client.describe_stack_events(StackName=self.stack_id)
        except ClientError:
            # ClientError: Some sort of error (possibly permissions)
            #              when trying to find out what happened
            pass

        for event in events["StackEvents"]:
            if event["ResourceStatus"] == self.CREATE_FAILED:
                reasons.append(event["ResourceStatusReason"])
        return reasons or ["Unknown Error"]

    def _build_stack(self):
        """
        For the given sectors will build a YAML string - one for each
        profile_name/region intersection.  There may be multiple EC2 instances
        per stack if they need to share a profile/region.
        :param sectors: The sectors to create YAML stacks for
        :type sectors:dict
        :return: A dict of profile_name:region_name:yaml_string
        """
        troposphere = AWSStack(self)
        stack_as_yaml = troposphere.generate()
        return stack_as_yaml
