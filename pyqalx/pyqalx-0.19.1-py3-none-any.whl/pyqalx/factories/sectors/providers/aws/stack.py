import json
from collections import defaultdict

import yaml
from troposphere import Tag, Tags, Template, Base64, Join, Ref, ssm, cloudwatch
from troposphere.ec2 import Instance
from troposphere.iam import Role, Policy, InstanceProfile
from troposphere.secretsmanager import Secret
from troposphere.cloudformation import WaitCondition, WaitConditionHandle

from pyqalx.__version__ import __version__
from pyqalx.config import UserConfig, BotConfig


class AWSStack:
    def __init__(self, provider):
        self.provider = provider
        self.factory_entity = self.provider.factory.entity
        self.stack = self.provider.stack
        self.template = Template(Description=self.provider._description)
        self.images = None
        self._secure_parameters = ["TOKEN"]

    @staticmethod
    def _add_tag(key, value):
        """
        Helper for adding a Tag to a resource
        :param key: The key for the tag
        :type key: str
        :param value: The value for the tag
        :type value: str
        :return:dict
        """
        return Tag(key, value)

    def _resource_tags(self, name):
        """
        Helper for common resource tags to use on resources created by
        the stack, as well as the stack itself
        """
        tags = [
            self._add_tag("Name", name),
            # This should be stored as a string on AWS not uuid.UUID
            self._add_tag("qalx-factory-guid", str(self.factory_entity.guid)),
            self._add_tag("qalx-factory-stage", self.provider.stage),
            self._add_tag("qalx-created-version", __version__),
            self._add_tag("qalx-factory-name", self.factory_entity.name),
            self._add_tag(
                "qalx-creating-aws-profile", self.provider.profile_name
            ),
        ]
        return tags

    def _tags(self, sector_name, suffix):
        name = self.provider._resource_name(sector_name, suffix)
        tags = self._resource_tags(name=name)
        return Tags(*tags)

    def _tags_as_dict(self, sector_name, suffix):
        """
        For AWS reasons some resources require the Tags to be a dict of
        {key:value} rather than a list of [{"Key": key, "Value": value}]
        """
        _tags = self._tags(sector_name, suffix).to_dict()
        tags = {}
        for tag in _tags:
            tags[tag["Key"]] = tag["Value"]
        return tags

    def _logical_id(self, sector_name, suffix):
        return (
            self.provider._resource_name(sector_name, suffix)
            .title()
            .replace("-", "")
        )

    def _get_instance_name(self):
        """
        The instance name only exists in the tags of the instance.
        It will always be there as the instance gets created before the
        secrets
        """
        ec2_instance = self.refs["instance"]
        for tag in ec2_instance.Tags.to_dict():
            if tag["Key"] == "Name":
                instance_name = tag["Value"]
                break
        return instance_name

    def _parameter_variable_name(self, name, key_prefix):
        """
        Parameter variables don't follow the same naming convention
        as normal resources.  Instead they should be in the format of
        "<instance_name>_<config prefix><variable name>".
        This enables easier lookup of the resource in order to set them
        as environment variables on the EC2 instance.  It also allows separate
        profiles to be used for different EC2 instances in the stack
        :param name:The name of the paramter variable we want to save
        :return: The full name of the parameter variable how it should exist
        on the EC2 instance
        """
        instance_name = self._get_instance_name()
        return f"{instance_name}_{key_prefix}{name.upper()}"

    def _parameter_description(self, name):
        return f"qalx {name.upper()} for {self._get_instance_name()}"

    def linux_user_data(self, sector_name):
        """
        The user data that enables a linux instance to be
        bootstrapped.
        :param sector_name:The name of the sector
        :return: troposphere template detailing the userdata
        """
        sector = self.provider.stack[sector_name]
        instance_name = self._get_instance_name()
        bootstrap_script = (
            f"sudo -u ec2-user bash -c "
            f"'. /home/ec2-user/pyqalx/pyqalx_factory_bootstrap.sh "
            f"--factory_guid {self.factory_entity.guid} "
            f"--sector_name {sector_name} "
            f"--profile_name {sector['profile_name']} "
            f"--region_name {sector['region_name']} "
            f"--instance_name {instance_name}'"
        )
        # A log file the bootstrap script writes to disk that is used to check
        # for success.
        bootstrap_log = "/tmp/bootstrap.log"
        return Base64(
            Join(
                "",
                [
                    # https://aws.amazon.com/premiumsupport/knowledge
                    #           -center/execute-user-data-ec2/
                    'Content-Type: multipart/mixed; boundary="//"\n',
                    "MIME-Version: 1.0\n\n",
                    "--//\n",
                    'Content-Type: text/cloud-config; charset="us-ascii"\n',
                    "MIME-Version: 1.0\n",
                    "Content-Transfer-Encoding: 7bit\n"
                    'Content-Disposition: attachment; filename="cloud-config.txt"\n\n'
                    "#cloud-config\n"
                    "cloud_final_modules:\n"
                    "- [scripts-user, always]\n\n"
                    "--//\n",
                    'Content-Type: text/x-shellscript; charset="us-ascii"\n',
                    "MIME-Version: 1.0\n"
                    "Content-Transfer-Encoding: 7bit\n"
                    'Content-Disposition: attachment; filename="userdata.txt"\n\n'
                    "#!/bin/bash\n",
                    # can't use cfn-init because cfn-init waits until spawned
                    # processes exit - which won't work for us because the bots
                    # will run indefinitely.
                    bootstrap_script,
                    "\n",
                    # Read the first char from the bootstrap script.  This
                    # will be 0 if success, or 1 if failure
                    f'/opt/aws/bin/cfn-signal -e "$(head -c 1 {bootstrap_log})" -r '
                    f'"$(<{bootstrap_log})" \'',
                    Ref(self.refs["wait_handle"]),
                    "'\n",
                    "-- //\n",
                ],
            )
        )

    def windows_user_data(self, sector_name):
        sector = self.provider.stack[sector_name]
        instance_name = self._get_instance_name()
        cmd = (
            "C:\\Users\\Administrator\\.venvs\\pyqalx\\Scripts\\pyqalx_"
            "factory_bootstrap.bat"
        )
        bootstrap_script = (
            f"{cmd} "
            f"--factory_guid {self.factory_entity.guid} "
            f"--sector_name {sector_name} "
            f"--profile_name {sector['profile_name']} "
            f"--region_name {sector['region_name']} "
            f"--instance_name {instance_name}"
        )

        return Base64(
            Join(
                "",
                [
                    "<script>",
                    "\n",
                    bootstrap_script,
                    "\n",
                    "</script>",
                    "\n",
                    "<powershell>",
                    "\n",
                    # A log file the bootstrap script writes to disk that is
                    # used to check for success.
                    "$logfile=Get-Content -Path C:\\Windows\\Temp\\bootstrap.log",
                    "\n",
                    "$errorcode=$logfile.SubString(0,1)",
                    "\n",
                    'cfn-signal -e "$errorcode" -r "$logfile" \'',
                    Ref(self.refs["wait_handle"]),
                    "'\n",
                    "</powershell>",
                    "\n",
                    "<persist>true</persist>",
                    "\n",
                ],
            )
        )

    def _get_platform(self, sector_name):
        """
        Works out the platform for the requested image required by the sector
        based on the ImageId.  If it is a linux image then the `Platform` key
        will not exist in the `self.images` response from AWS.
        :param sector_name:The name of the sector we are building the image for
        :return:The platform - either 'windows' or 'linux'.
        """
        sector_instance_id = self.stack[sector_name]["parameters"]["ImageId"]
        platform = None
        for image in self.images:
            if sector_instance_id == image["ImageId"]:
                # If this is a linux image the Platform key won't exist
                platform = image.get("Platform", "linux").lower()
        return platform

    def _get_user_data(self, sector_name):
        """
        Gets the user data based on the platform
        """
        platform = self._get_platform(sector_name)
        user_data = getattr(self, f"{platform}_user_data")(sector_name)
        return user_data

    def _ec2_instance_logical_id(self, sector_name):
        """
        Helper for determining the EC2 instance logical ID for a given
        sector
        :param sector_name:The name of the sector from the plan
        :return: The logical ID used in CF templates
        """
        return self._logical_id(sector_name, "instance")

    def _ec2_instance(self, sector_name):
        """
        Adds a single ec2 instance to the template.  There will be one EC2
        instance for each sector on the stack.  Creates a wait handle so that
        the instance can single to cloudformation when the bots have been
        bootstrapped (either success or failure)
        :param sector_name: The name of the sector.
        """
        suffix = "instance"
        instance_profile = self.refs["instance_profile"]
        logical_id = self._ec2_instance_logical_id(sector_name)
        wait_handle = WaitConditionHandle(
            self._logical_id(sector_name, "wait_condition_handle")
        )

        self.refs["wait_handle"] = wait_handle
        self.template.add_resource(wait_handle)
        instance = Instance(
            logical_id,
            IamInstanceProfile=instance_profile.InstanceProfileName,
            Tags=self._tags(sector_name, suffix),
            DependsOn=[self.refs["role"].title, instance_profile.title],
        )
        self.refs["instance"] = instance
        # user data needs the instance name, so set user data after the instance
        # resource is crated
        instance.UserData = self._get_user_data(sector_name)

        wait_condition = WaitCondition(
            self._logical_id(sector_name, "wait_condition"),
            DependsOn=[instance],
            Count=1,
            Handle=Ref(wait_handle),
            # Really long timeout to give time for windows instances to fully
            # boot up
            Timeout=1200,
        )
        self.template.add_resource(wait_condition)
        self.template.add_resource(instance)

    def _role_policies(self):
        """
        Updates the role with policies that limit the reading of
        secrets/parameters to just sector the role is attached to
        """
        instance_name = self._get_instance_name()
        self.refs["role"].Policies = [
            Policy(
                PolicyName="ReadSecretsManagerPolicy",
                PolicyDocument={
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Action": "secretsmanager:GetSecretValue",
                            "Resource": {
                                "Fn::Join": [
                                    "",
                                    [
                                        f"arn:aws:"
                                        f"secretsmanager:"
                                        f"{self.provider.region_name}:",
                                        {"Ref": "AWS::AccountId"},
                                        f":secret:{instance_name}*",
                                    ],
                                ]
                            },
                        },
                        {
                            "Effect": "Allow",
                            "Action": "secretsmanager:ListSecrets",
                            "Resource": "*",
                        },
                    ],
                },
            ),
            Policy(
                PolicyName="ReadSSMPolicy",
                PolicyDocument={
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Action": "ssm:GetParameter",
                            "Resource": {
                                "Fn::Join": [
                                    "",
                                    [
                                        f"arn:aws:"
                                        f"ssm:"
                                        f"{self.provider.region_name}:",
                                        {"Ref": "AWS::AccountId"},
                                        f":parameter/{instance_name}*",
                                    ],
                                ]
                            },
                        },
                        {
                            "Effect": "Allow",
                            "Action": "ssm:DescribeParameters",
                            "Resource": "*",
                        },
                    ],
                },
            ),
        ]

    def _role(self, sector_name):
        """
        The Role that this specific EC2 instance will have applied to it.
        Required so that the EC2 instance get obtain the configuration
        parameters from SSM and Secrets Manager.   There is one role
        per sector to ensure that sectors (EC2 instances) cannot get
        resources assigned to another sector
        """
        suffix = "role"
        role_name = self.provider._resource_name(sector_name, suffix)
        instance = Role(
            self._logical_id(sector_name, suffix),
            # role name is limited to 64 characters
            RoleName=role_name[0:64],
            Description="IAM role for qalx factory",
            AssumeRolePolicyDocument={
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"Service": ["ec2.amazonaws.com"]},
                        "Action": ["sts:AssumeRole"],
                    }
                ],
            },
            Tags=self._tags(sector_name, suffix),
        )
        self.template.add_resource(instance)
        self.refs["role"] = instance

    def _instance_profile(self, sector_name):
        """
        The instance profile for the role.  One instance profile is created per
        stack - namespaced to the AWS profile
        """
        suffix = "instanceprofile"
        instance = InstanceProfile(
            self._logical_id(sector_name, suffix),
            InstanceProfileName=self.provider._resource_name(
                sector_name, suffix
            ),
            Roles=[self.refs["role"].RoleName],
            DependsOn=[self.refs["role"].title],
        )
        self.template.add_resource(instance)
        self.refs["instance_profile"] = instance

    def _config_parameters(self, sector_name):
        """
        Creates entries in Secret Manager and SSM Parameter store for the
        provided configs specified on the sector
        :param sector_name: The name of the sector
        """
        user_config = UserConfig._load_inifile(
            self.provider.stack[sector_name]["user_profile"]
        )
        bot_config = BotConfig._load_inifile(
            self.provider.stack[sector_name]["bot_profile"]
        )
        configs = {UserConfig: user_config, BotConfig: bot_config}
        for Config, config in configs.items():
            for name, value in config.items():
                # Values must be a string.  The session Config
                # will handle converting to boolean as necessary.
                value = str(value)
                suffix = f"{Config.key_prefix.lower()}{name.lower()}"
                logical_id = self._logical_id(sector_name, suffix)
                description = self._parameter_description(name)
                parameter_name = self._parameter_variable_name(
                    name, Config.key_prefix
                )

                if value:
                    if name in self._secure_parameters:
                        # Ensure we only create secrets if there is a value
                        suffix = f"secretsmanager{suffix}"
                        instance = Secret(
                            logical_id,
                            Name=parameter_name,
                            SecretString=value,
                            Description=description,
                            Tags=self._tags(sector_name, suffix),
                        )
                        self.template.add_resource(instance)
                    else:
                        # TOKEN should not be stored in SSM as it isn't secure.
                        suffix = f"ssm{suffix}"

                        instance = ssm.Parameter(
                            logical_id,
                            Type="String",
                            Value=value,
                            Name=parameter_name,
                            Description=description,
                            # ...Tags for ssm.Parameter are a dict rather
                            # than a list
                            Tags=self._tags_as_dict(sector_name, suffix),
                        )
                        self.template.add_resource(instance)

    def _build_alarm(self, alarm_name, region_name):
        """
        Helper for building a specific alarm based on the alarm name
        """
        alarm = self.provider.factory.plan["factory"]["alarms"][alarm_name]
        template = {}

        for key, value in alarm.items():
            if key == "AlarmActions":
                # Alarm actions get built up from an enum
                action_value = []
                for action in value:
                    action_value.append(
                        f"arn:aws:automate:{region_name}:ec2:{action}"
                    )
                value = action_value
            template[key] = value
        return template

    def _alarms(self):
        """
        Builds all the Cloudwatch alarms for all the instances.  The same alarm
        is used for multiple instances if possible.
        """
        alarms = {}
        dimensions = defaultdict(list)
        depends_on = defaultdict(list)
        for sector_name, parameters in self.stack.items():
            alarm_name = parameters.get("alarm", None)
            ec2_instance_logical_id = self._ec2_instance_logical_id(sector_name)
            sector = self.provider.stack[sector_name]
            region = sector["region_name"]

            if alarm_name is not None:
                # There is an alarm on this sector, build the base alarm
                # template
                logical_id = self._logical_id(
                    f"{sector_name}-{alarm_name}", "alarm"
                )
                alarms[logical_id] = self._build_alarm(alarm_name, region)
                depends_on[logical_id].append(ec2_instance_logical_id)
                dimensions[logical_id].append(
                    {
                        "Name": "InstanceId",
                        "Value": Ref(ec2_instance_logical_id),
                    }
                )

        for logical_id, dimension in dimensions.items():
            metric_dimensions = [
                cloudwatch.MetricDimension().from_dict(d=d, title=logical_id)
                for d in dimension
            ]

            alarms[logical_id]["Dimensions"] = metric_dimensions
            alarms[logical_id]["DependsOn"] = depends_on[logical_id]

            instance = cloudwatch.Alarm(logical_id, **alarms[logical_id])
            self.template.add_resource(instance)

    def _image_ids(self):
        """
        Returns the imageIDs for the given sector.  There may be multiple
        EC2 instances for a given sector
        :return: List of image ids
        """
        image_ids = []
        for sector in self.stack.values():
            image_ids.append(sector["parameters"]["ImageId"])
        return image_ids

    def generate(self):
        self.images = self.provider._describe_images(self._image_ids())

        if self.images is None:
            # There was a problem describing images.  We can't build this
            # stack so return. The error message is shown to the user
            # in the _describe_images call
            return None

        found = [i["ImageId"] for i in self.images]
        missing = set(self._image_ids()) - set(found)
        if missing:
            # The imageIds in the plan don't exist on AWS
            self.provider._msg_user(
                f"Could not find the following ImageIds on "
                f'AWS: {", ".join(missing)}.'
            )
            return None

        for sector_name in self.stack.keys():
            self.refs = {}
            # Create one role & instance profile per sector.
            # This ensures that an instance cannot talk to resources
            # specified for another instance
            self._role(sector_name)
            self._instance_profile(sector_name)
            # Create one ec2 instance and associated parameters for each sector
            self._ec2_instance(sector_name)
            self._config_parameters(sector_name)
            self._role_policies()
        self._alarms()
        # The user supplies the raw parameters for the EC2 instances
        # so we need to insert them into the template directly
        template = self._insert_parameters()
        return yaml.safe_dump(template)

    def _insert_parameters(self):
        """
        Inserts the parameters from the sector directly into the EC2
        instance properties
        :return: The template as a dict
        """
        template = json.loads(self.template.to_json())
        for sector_name, parameters in self.stack.items():
            logical_id = self._logical_id(sector_name, "instance")

            template["Resources"][logical_id]["Properties"].update(
                parameters["parameters"]
            )
        return template
