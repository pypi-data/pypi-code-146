'''
# AWS::Chatbot Construct Library

AWS Chatbot is an AWS service that enables DevOps and software development teams to use Slack chat rooms to monitor and respond to operational events in their AWS Cloud. AWS Chatbot processes AWS service notifications from Amazon Simple Notification Service (Amazon SNS), and forwards them to Slack chat rooms so teams can analyze and act on them immediately, regardless of location.

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as chatbot
import monocdk as sns
import monocdk as iam


slack_channel = chatbot.SlackChannelConfiguration(self, "MySlackChannel",
    slack_channel_configuration_name="YOUR_CHANNEL_NAME",
    slack_workspace_id="YOUR_SLACK_WORKSPACE_ID",
    slack_channel_id="YOUR_SLACK_CHANNEL_ID"
)

slack_channel.add_to_role_policy(iam.PolicyStatement(
    effect=iam.Effect.ALLOW,
    actions=["s3:GetObject"
    ],
    resources=["arn:aws:s3:::abc/xyz/123.txt"]
))

slack_channel.add_notification_topic(sns.Topic(self, "MyTopic"))
```

## Log Group

Slack channel configuration automatically create a log group with the name `/aws/chatbot/<configuration-name>` in `us-east-1` upon first execution with
log data set to never expire.

The `logRetention` property can be used to set a different expiration period. A log group will be created if not already exists.
If the log group already exists, it's expiration will be configured to the value specified in this construct (never expire, by default).

By default, CDK uses the AWS SDK retry options when interacting with the log group. The `logRetentionRetryOptions` property
allows you to customize the maximum number of retries and base backoff duration.

*Note* that, if `logRetention` is set, a [CloudFormation custom
resource](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cfn-customresource.html) is added
to the stack that pre-creates the log group as part of the stack deployment, if it already doesn't exist, and sets the
correct log retention period (never expire, by default).
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from .._jsii import *

import constructs as _constructs_77d1e7e8
from .. import (
    CfnResource as _CfnResource_e0a482dc,
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_cloudwatch import (
    Metric as _Metric_5b2b8e58,
    MetricOptions as _MetricOptions_1c185ae8,
    Unit as _Unit_113c79f9,
)
from ..aws_codestarnotifications import (
    INotificationRuleTarget as _INotificationRuleTarget_31f512df,
    NotificationRuleTargetConfig as _NotificationRuleTargetConfig_a582558e,
)
from ..aws_iam import (
    IGrantable as _IGrantable_4c5a91d1,
    IPrincipal as _IPrincipal_93b48231,
    IRole as _IRole_59af6f50,
    PolicyStatement as _PolicyStatement_296fe8a3,
)
from ..aws_logs import (
    LogRetentionRetryOptions as _LogRetentionRetryOptions_c6b3d73a,
    RetentionDays as _RetentionDays_6c560d31,
)
from ..aws_sns import ITopic as _ITopic_465e36b9


@jsii.implements(_IInspectable_82c04a63)
class CfnSlackChannelConfiguration(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_chatbot.CfnSlackChannelConfiguration",
):
    '''A CloudFormation ``AWS::Chatbot::SlackChannelConfiguration``.

    The ``AWS::Chatbot::SlackChannelConfiguration`` resource configures a Slack channel to allow users to use AWS Chatbot with AWS CloudFormation templates.

    This resource requires some setup to be done in the AWS Chatbot console. To provide the required Slack workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console, then copy and paste the workspace ID from the console. For more details, see steps 1-4 in `Setting Up AWS Chatbot with Slack <https://docs.aws.amazon.com/chatbot/latest/adminguide/setting-up.html#Setup_intro>`_ in the *AWS Chatbot User Guide* .

    :cloudformationResource: AWS::Chatbot::SlackChannelConfiguration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_chatbot as chatbot
        
        cfn_slack_channel_configuration = chatbot.CfnSlackChannelConfiguration(self, "MyCfnSlackChannelConfiguration",
            configuration_name="configurationName",
            iam_role_arn="iamRoleArn",
            slack_channel_id="slackChannelId",
            slack_workspace_id="slackWorkspaceId",
        
            # the properties below are optional
            guardrail_policies=["guardrailPolicies"],
            logging_level="loggingLevel",
            sns_topic_arns=["snsTopicArns"],
            user_role_required=False
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        configuration_name: builtins.str,
        iam_role_arn: builtins.str,
        slack_channel_id: builtins.str,
        slack_workspace_id: builtins.str,
        guardrail_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_level: typing.Optional[builtins.str] = None,
        sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_role_required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::Chatbot::SlackChannelConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param configuration_name: The name of the configuration.
        :param iam_role_arn: The ARN of the IAM role that defines the permissions for AWS Chatbot . This is a user-defined role that AWS Chatbot will assume. This is not the service-linked role. For more information, see `IAM Policies for AWS Chatbot <https://docs.aws.amazon.com/chatbot/latest/adminguide/chatbot-iam-policies.html>`_ .
        :param slack_channel_id: The ID of the Slack channel. To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link. The channel ID is the 9-character string at the end of the URL. For example, ``ABCBBLZZZ`` .
        :param slack_workspace_id: The ID of the Slack workspace authorized with AWS Chatbot . To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console. Then you can copy and paste the workspace ID from the console. For more details, see steps 1-4 in `Setting Up AWS Chatbot with Slack <https://docs.aws.amazon.com/chatbot/latest/adminguide/setting-up.html#Setup_intro>`_ in the *AWS Chatbot User Guide* .
        :param guardrail_policies: The list of IAM policy ARNs that are applied as channel guardrails. The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.
        :param logging_level: Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs. Logging levels include ``ERROR`` , ``INFO`` , or ``NONE`` .
        :param sns_topic_arns: The ARNs of the SNS topics that deliver notifications to AWS Chatbot .
        :param user_role_required: Enables use of a user role requirement in your chat configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd0412d8f818742b46d15eb194d87cac54799e66193cc8229e544b28e626b856)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSlackChannelConfigurationProps(
            configuration_name=configuration_name,
            iam_role_arn=iam_role_arn,
            slack_channel_id=slack_channel_id,
            slack_workspace_id=slack_workspace_id,
            guardrail_policies=guardrail_policies,
            logging_level=logging_level,
            sns_topic_arns=sns_topic_arns,
            user_role_required=user_role_required,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee73351f4d4f3368db9cfa57e5826dd093b9e531e3469733f483605f3a0d4b5)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4026dde0d321dad3e47e395f5715de904e213da903a7fcdde9ed75e6ee63f46e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="configurationName")
    def configuration_name(self) -> builtins.str:
        '''The name of the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-configurationname
        '''
        return typing.cast(builtins.str, jsii.get(self, "configurationName"))

    @configuration_name.setter
    def configuration_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c590fedf0abe8ef009317b609259c5f58fe4b3043f27a4f11add95019bd8d79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationName", value)

    @builtins.property
    @jsii.member(jsii_name="iamRoleArn")
    def iam_role_arn(self) -> builtins.str:
        '''The ARN of the IAM role that defines the permissions for AWS Chatbot .

        This is a user-defined role that AWS Chatbot will assume. This is not the service-linked role. For more information, see `IAM Policies for AWS Chatbot <https://docs.aws.amazon.com/chatbot/latest/adminguide/chatbot-iam-policies.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-iamrolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "iamRoleArn"))

    @iam_role_arn.setter
    def iam_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f359c90f82be9856c7adcc7d0bff8ba99d0ee4c26849035fbcaafd2cf4933ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="slackChannelId")
    def slack_channel_id(self) -> builtins.str:
        '''The ID of the Slack channel.

        To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link. The channel ID is the 9-character string at the end of the URL. For example, ``ABCBBLZZZ`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackchannelid
        '''
        return typing.cast(builtins.str, jsii.get(self, "slackChannelId"))

    @slack_channel_id.setter
    def slack_channel_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eaa8cb019aa5506fac10e297ae6d7331fd21e82b30676011beb4f62a6e684621)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slackChannelId", value)

    @builtins.property
    @jsii.member(jsii_name="slackWorkspaceId")
    def slack_workspace_id(self) -> builtins.str:
        '''The ID of the Slack workspace authorized with AWS Chatbot .

        To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console. Then you can copy and paste the workspace ID from the console. For more details, see steps 1-4 in `Setting Up AWS Chatbot with Slack <https://docs.aws.amazon.com/chatbot/latest/adminguide/setting-up.html#Setup_intro>`_ in the *AWS Chatbot User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackworkspaceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "slackWorkspaceId"))

    @slack_workspace_id.setter
    def slack_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc94f7cb95ac359119dc432843eb5b4bcd11d3d7467b565a01435edaba2fbfa6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "slackWorkspaceId", value)

    @builtins.property
    @jsii.member(jsii_name="guardrailPolicies")
    def guardrail_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of IAM policy ARNs that are applied as channel guardrails.

        The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-guardrailpolicies
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "guardrailPolicies"))

    @guardrail_policies.setter
    def guardrail_policies(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64429f2750f4405f0b4dcb28e5a5b948ac2acf7c4b483e1425ccc094bc771054)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guardrailPolicies", value)

    @builtins.property
    @jsii.member(jsii_name="loggingLevel")
    def logging_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs.

        Logging levels include ``ERROR`` , ``INFO`` , or ``NONE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-logginglevel
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "loggingLevel"))

    @logging_level.setter
    def logging_level(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c08d61dd4d0672bd65aa20807a196a2324ee36588f7a8003c0d0bf2a091e87c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingLevel", value)

    @builtins.property
    @jsii.member(jsii_name="snsTopicArns")
    def sns_topic_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARNs of the SNS topics that deliver notifications to AWS Chatbot .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-snstopicarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "snsTopicArns"))

    @sns_topic_arns.setter
    def sns_topic_arns(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c255630a2b443a1de133faed964ba20b03d128b859708fe81b498b3c971160)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snsTopicArns", value)

    @builtins.property
    @jsii.member(jsii_name="userRoleRequired")
    def user_role_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables use of a user role requirement in your chat configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-userrolerequired
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "userRoleRequired"))

    @user_role_required.setter
    def user_role_required(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c60b375f5901966ece93900df3a8255fa4d4dd5005e99edf64b7cf28e0c47caf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userRoleRequired", value)


@jsii.data_type(
    jsii_type="monocdk.aws_chatbot.CfnSlackChannelConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_name": "configurationName",
        "iam_role_arn": "iamRoleArn",
        "slack_channel_id": "slackChannelId",
        "slack_workspace_id": "slackWorkspaceId",
        "guardrail_policies": "guardrailPolicies",
        "logging_level": "loggingLevel",
        "sns_topic_arns": "snsTopicArns",
        "user_role_required": "userRoleRequired",
    },
)
class CfnSlackChannelConfigurationProps:
    def __init__(
        self,
        *,
        configuration_name: builtins.str,
        iam_role_arn: builtins.str,
        slack_channel_id: builtins.str,
        slack_workspace_id: builtins.str,
        guardrail_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
        logging_level: typing.Optional[builtins.str] = None,
        sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        user_role_required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSlackChannelConfiguration``.

        :param configuration_name: The name of the configuration.
        :param iam_role_arn: The ARN of the IAM role that defines the permissions for AWS Chatbot . This is a user-defined role that AWS Chatbot will assume. This is not the service-linked role. For more information, see `IAM Policies for AWS Chatbot <https://docs.aws.amazon.com/chatbot/latest/adminguide/chatbot-iam-policies.html>`_ .
        :param slack_channel_id: The ID of the Slack channel. To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link. The channel ID is the 9-character string at the end of the URL. For example, ``ABCBBLZZZ`` .
        :param slack_workspace_id: The ID of the Slack workspace authorized with AWS Chatbot . To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console. Then you can copy and paste the workspace ID from the console. For more details, see steps 1-4 in `Setting Up AWS Chatbot with Slack <https://docs.aws.amazon.com/chatbot/latest/adminguide/setting-up.html#Setup_intro>`_ in the *AWS Chatbot User Guide* .
        :param guardrail_policies: The list of IAM policy ARNs that are applied as channel guardrails. The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.
        :param logging_level: Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs. Logging levels include ``ERROR`` , ``INFO`` , or ``NONE`` .
        :param sns_topic_arns: The ARNs of the SNS topics that deliver notifications to AWS Chatbot .
        :param user_role_required: Enables use of a user role requirement in your chat configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_chatbot as chatbot
            
            cfn_slack_channel_configuration_props = chatbot.CfnSlackChannelConfigurationProps(
                configuration_name="configurationName",
                iam_role_arn="iamRoleArn",
                slack_channel_id="slackChannelId",
                slack_workspace_id="slackWorkspaceId",
            
                # the properties below are optional
                guardrail_policies=["guardrailPolicies"],
                logging_level="loggingLevel",
                sns_topic_arns=["snsTopicArns"],
                user_role_required=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4890d38518885f1c140a5326bc6c191c515f3a51b190eda3b677a610ce6eb9e5)
            check_type(argname="argument configuration_name", value=configuration_name, expected_type=type_hints["configuration_name"])
            check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            check_type(argname="argument slack_channel_id", value=slack_channel_id, expected_type=type_hints["slack_channel_id"])
            check_type(argname="argument slack_workspace_id", value=slack_workspace_id, expected_type=type_hints["slack_workspace_id"])
            check_type(argname="argument guardrail_policies", value=guardrail_policies, expected_type=type_hints["guardrail_policies"])
            check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
            check_type(argname="argument sns_topic_arns", value=sns_topic_arns, expected_type=type_hints["sns_topic_arns"])
            check_type(argname="argument user_role_required", value=user_role_required, expected_type=type_hints["user_role_required"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration_name": configuration_name,
            "iam_role_arn": iam_role_arn,
            "slack_channel_id": slack_channel_id,
            "slack_workspace_id": slack_workspace_id,
        }
        if guardrail_policies is not None:
            self._values["guardrail_policies"] = guardrail_policies
        if logging_level is not None:
            self._values["logging_level"] = logging_level
        if sns_topic_arns is not None:
            self._values["sns_topic_arns"] = sns_topic_arns
        if user_role_required is not None:
            self._values["user_role_required"] = user_role_required

    @builtins.property
    def configuration_name(self) -> builtins.str:
        '''The name of the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-configurationname
        '''
        result = self._values.get("configuration_name")
        assert result is not None, "Required property 'configuration_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def iam_role_arn(self) -> builtins.str:
        '''The ARN of the IAM role that defines the permissions for AWS Chatbot .

        This is a user-defined role that AWS Chatbot will assume. This is not the service-linked role. For more information, see `IAM Policies for AWS Chatbot <https://docs.aws.amazon.com/chatbot/latest/adminguide/chatbot-iam-policies.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-iamrolearn
        '''
        result = self._values.get("iam_role_arn")
        assert result is not None, "Required property 'iam_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slack_channel_id(self) -> builtins.str:
        '''The ID of the Slack channel.

        To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link. The channel ID is the 9-character string at the end of the URL. For example, ``ABCBBLZZZ`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackchannelid
        '''
        result = self._values.get("slack_channel_id")
        assert result is not None, "Required property 'slack_channel_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slack_workspace_id(self) -> builtins.str:
        '''The ID of the Slack workspace authorized with AWS Chatbot .

        To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console. Then you can copy and paste the workspace ID from the console. For more details, see steps 1-4 in `Setting Up AWS Chatbot with Slack <https://docs.aws.amazon.com/chatbot/latest/adminguide/setting-up.html#Setup_intro>`_ in the *AWS Chatbot User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-slackworkspaceid
        '''
        result = self._values.get("slack_workspace_id")
        assert result is not None, "Required property 'slack_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def guardrail_policies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of IAM policy ARNs that are applied as channel guardrails.

        The AWS managed 'AdministratorAccess' policy is applied as a default if this is not set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-guardrailpolicies
        '''
        result = self._values.get("guardrail_policies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def logging_level(self) -> typing.Optional[builtins.str]:
        '''Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs.

        Logging levels include ``ERROR`` , ``INFO`` , or ``NONE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-logginglevel
        '''
        result = self._values.get("logging_level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sns_topic_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The ARNs of the SNS topics that deliver notifications to AWS Chatbot .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-snstopicarns
        '''
        result = self._values.get("sns_topic_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def user_role_required(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables use of a user role requirement in your chat configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-chatbot-slackchannelconfiguration.html#cfn-chatbot-slackchannelconfiguration-userrolerequired
        '''
        result = self._values.get("user_role_required")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSlackChannelConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_chatbot.ISlackChannelConfiguration")
class ISlackChannelConfiguration(
    _IResource_8c1dbbbd,
    _IGrantable_4c5a91d1,
    _INotificationRuleTarget_31f512df,
    typing_extensions.Protocol,
):
    '''(experimental) Represents a Slack channel configuration.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationArn")
    def slack_channel_configuration_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Slack channel configuration In the form of arn:aws:chatbot:{region}:{account}:chat-configuration/slack-channel/{slackChannelName}.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationName")
    def slack_channel_configuration_name(self) -> builtins.str:
        '''(experimental) The name of Slack channel configuration.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The permission role of Slack channel configuration.

        :default: - A role will be created.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: _PolicyStatement_296fe8a3) -> None:
        '''(experimental) Adds a statement to the IAM role.

        :param statement: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Return the given named metric for this SlackChannelConfiguration.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        ...


class _ISlackChannelConfigurationProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
    jsii.proxy_for(_IGrantable_4c5a91d1), # type: ignore[misc]
    jsii.proxy_for(_INotificationRuleTarget_31f512df), # type: ignore[misc]
):
    '''(experimental) Represents a Slack channel configuration.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_chatbot.ISlackChannelConfiguration"

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationArn")
    def slack_channel_configuration_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Slack channel configuration In the form of arn:aws:chatbot:{region}:{account}:chat-configuration/slack-channel/{slackChannelName}.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "slackChannelConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationName")
    def slack_channel_configuration_name(self) -> builtins.str:
        '''(experimental) The name of Slack channel configuration.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "slackChannelConfigurationName"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The permission role of Slack channel configuration.

        :default: - A role will be created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.Optional[_IRole_59af6f50], jsii.get(self, "role"))

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: _PolicyStatement_296fe8a3) -> None:
        '''(experimental) Adds a statement to the IAM role.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29458baa00a3496fa8875b25454701b3f109dec008af03d28580229f90b0933d)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(None, jsii.invoke(self, "addToRolePolicy", [statement]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Return the given named metric for this SlackChannelConfiguration.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0e3831ef79c26734a4aa9c2e741cef5b5d58486046b61cf872e2838ef38d6eb)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metric", [metric_name, props]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISlackChannelConfiguration).__jsii_proxy_class__ = lambda : _ISlackChannelConfigurationProxy


@jsii.enum(jsii_type="monocdk.aws_chatbot.LoggingLevel")
class LoggingLevel(enum.Enum):
    '''(experimental) Logging levels include ERROR, INFO, or NONE.

    :stability: experimental
    '''

    ERROR = "ERROR"
    '''(experimental) ERROR.

    :stability: experimental
    '''
    INFO = "INFO"
    '''(experimental) INFO.

    :stability: experimental
    '''
    NONE = "NONE"
    '''(experimental) NONE.

    :stability: experimental
    '''


@jsii.implements(ISlackChannelConfiguration)
class SlackChannelConfiguration(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_chatbot.SlackChannelConfiguration",
):
    '''(experimental) A new Slack channel configuration.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as chatbot
        
        # project: codebuild.Project
        
        
        target = chatbot.SlackChannelConfiguration(self, "MySlackChannel",
            slack_channel_configuration_name="YOUR_CHANNEL_NAME",
            slack_workspace_id="YOUR_SLACK_WORKSPACE_ID",
            slack_channel_id="YOUR_SLACK_CHANNEL_ID"
        )
        
        rule = project.notify_on_build_succeeded("NotifyOnBuildSucceeded", target)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        slack_channel_configuration_name: builtins.str,
        slack_channel_id: builtins.str,
        slack_workspace_id: builtins.str,
        logging_level: typing.Optional[LoggingLevel] = None,
        log_retention: typing.Optional[_RetentionDays_6c560d31] = None,
        log_retention_retry_options: typing.Optional[typing.Union[_LogRetentionRetryOptions_c6b3d73a, typing.Dict[builtins.str, typing.Any]]] = None,
        log_retention_role: typing.Optional[_IRole_59af6f50] = None,
        notification_topics: typing.Optional[typing.Sequence[_ITopic_465e36b9]] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param slack_channel_configuration_name: (experimental) The name of Slack channel configuration.
        :param slack_channel_id: (experimental) The ID of the Slack channel. To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link. The channel ID is the 9-character string at the end of the URL. For example, ABCBBLZZZ.
        :param slack_workspace_id: (experimental) The ID of the Slack workspace authorized with AWS Chatbot. To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console. Then you can copy and paste the workspace ID from the console. For more details, see steps 1-4 in Setting Up AWS Chatbot with Slack in the AWS Chatbot User Guide.
        :param logging_level: (experimental) Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs. Default: LoggingLevel.NONE
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: (experimental) When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: (experimental) The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param notification_topics: (experimental) The SNS topics that deliver notifications to AWS Chatbot. Default: None
        :param role: (experimental) The permission role of Slack channel configuration. Default: - A role will be created.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2558412e17a6cae8d7e937245f5a4d89d66e1c8fed2e1f9a6351f2d7b5667d1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SlackChannelConfigurationProps(
            slack_channel_configuration_name=slack_channel_configuration_name,
            slack_channel_id=slack_channel_id,
            slack_workspace_id=slack_workspace_id,
            logging_level=logging_level,
            log_retention=log_retention,
            log_retention_retry_options=log_retention_retry_options,
            log_retention_role=log_retention_role,
            notification_topics=notification_topics,
            role=role,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromSlackChannelConfigurationArn")
    @builtins.classmethod
    def from_slack_channel_configuration_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        slack_channel_configuration_arn: builtins.str,
    ) -> ISlackChannelConfiguration:
        '''(experimental) Import an existing Slack channel configuration provided an ARN.

        :param scope: The parent creating construct.
        :param id: The construct's name.
        :param slack_channel_configuration_arn: configuration ARN (i.e. arn:aws:chatbot::1234567890:chat-configuration/slack-channel/my-slack).

        :return: a reference to the existing Slack channel configuration

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6887f1868e618b1cde129798dd05ca63d3f77b100a8893f4fc9b036def999f23)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument slack_channel_configuration_arn", value=slack_channel_configuration_arn, expected_type=type_hints["slack_channel_configuration_arn"])
        return typing.cast(ISlackChannelConfiguration, jsii.sinvoke(cls, "fromSlackChannelConfigurationArn", [scope, id, slack_channel_configuration_arn]))

    @jsii.member(jsii_name="metricAll")
    @builtins.classmethod
    def metric_all(
        cls,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Return the given named metric for All SlackChannelConfigurations.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ba4e917ea698b2065420506fc31058c04b5b3e9d203ee310d48f311a39b23a)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.sinvoke(cls, "metricAll", [metric_name, props]))

    @jsii.member(jsii_name="addNotificationTopic")
    def add_notification_topic(self, notification_topic: _ITopic_465e36b9) -> None:
        '''(experimental) Adds a SNS topic that deliver notifications to AWS Chatbot.

        :param notification_topic: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc47b68088cb84d284d28a44c3f8ff7f2799adc13026a5cfcd9362e0dbb23cad)
            check_type(argname="argument notification_topic", value=notification_topic, expected_type=type_hints["notification_topic"])
        return typing.cast(None, jsii.invoke(self, "addNotificationTopic", [notification_topic]))

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: _PolicyStatement_296fe8a3) -> None:
        '''(experimental) Adds extra permission to iam-role of Slack channel configuration.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69ca2e300e542a34f648ef554229c00bcaa08cb8226f508660a0d5f6e5421014)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(None, jsii.invoke(self, "addToRolePolicy", [statement]))

    @jsii.member(jsii_name="bindAsNotificationRuleTarget")
    def bind_as_notification_rule_target(
        self,
        _scope: _constructs_77d1e7e8.Construct,
    ) -> _NotificationRuleTargetConfig_a582558e:
        '''(experimental) Returns a target configuration for notification rule.

        :param _scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21856da15f42d0dbaff885d4829646782f76f94f0368773438273b2cf830796e)
            check_type(argname="argument _scope", value=_scope, expected_type=type_hints["_scope"])
        return typing.cast(_NotificationRuleTargetConfig_a582558e, jsii.invoke(self, "bindAsNotificationRuleTarget", [_scope]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Return the given named metric for this SlackChannelConfiguration.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__155ad06c49a63697e955d5b98660ab80e27a3e5de0c6b92d35fbe4d11748312c)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metric", [metric_name, props]))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_93b48231:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(_IPrincipal_93b48231, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationArn")
    def slack_channel_configuration_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Slack channel configuration In the form of arn:aws:chatbot:{region}:{account}:chat-configuration/slack-channel/{slackChannelName}.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "slackChannelConfigurationArn"))

    @builtins.property
    @jsii.member(jsii_name="slackChannelConfigurationName")
    def slack_channel_configuration_name(self) -> builtins.str:
        '''(experimental) The name of Slack channel configuration.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "slackChannelConfigurationName"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The permission role of Slack channel configuration.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IRole_59af6f50], jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="monocdk.aws_chatbot.SlackChannelConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "slack_channel_configuration_name": "slackChannelConfigurationName",
        "slack_channel_id": "slackChannelId",
        "slack_workspace_id": "slackWorkspaceId",
        "logging_level": "loggingLevel",
        "log_retention": "logRetention",
        "log_retention_retry_options": "logRetentionRetryOptions",
        "log_retention_role": "logRetentionRole",
        "notification_topics": "notificationTopics",
        "role": "role",
    },
)
class SlackChannelConfigurationProps:
    def __init__(
        self,
        *,
        slack_channel_configuration_name: builtins.str,
        slack_channel_id: builtins.str,
        slack_workspace_id: builtins.str,
        logging_level: typing.Optional[LoggingLevel] = None,
        log_retention: typing.Optional[_RetentionDays_6c560d31] = None,
        log_retention_retry_options: typing.Optional[typing.Union[_LogRetentionRetryOptions_c6b3d73a, typing.Dict[builtins.str, typing.Any]]] = None,
        log_retention_role: typing.Optional[_IRole_59af6f50] = None,
        notification_topics: typing.Optional[typing.Sequence[_ITopic_465e36b9]] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''(experimental) Properties for a new Slack channel configuration.

        :param slack_channel_configuration_name: (experimental) The name of Slack channel configuration.
        :param slack_channel_id: (experimental) The ID of the Slack channel. To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link. The channel ID is the 9-character string at the end of the URL. For example, ABCBBLZZZ.
        :param slack_workspace_id: (experimental) The ID of the Slack workspace authorized with AWS Chatbot. To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console. Then you can copy and paste the workspace ID from the console. For more details, see steps 1-4 in Setting Up AWS Chatbot with Slack in the AWS Chatbot User Guide.
        :param logging_level: (experimental) Specifies the logging level for this configuration. This property affects the log entries pushed to Amazon CloudWatch Logs. Default: LoggingLevel.NONE
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: (experimental) When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: (experimental) The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param notification_topics: (experimental) The SNS topics that deliver notifications to AWS Chatbot. Default: None
        :param role: (experimental) The permission role of Slack channel configuration. Default: - A role will be created.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as chatbot
            
            # project: codebuild.Project
            
            
            target = chatbot.SlackChannelConfiguration(self, "MySlackChannel",
                slack_channel_configuration_name="YOUR_CHANNEL_NAME",
                slack_workspace_id="YOUR_SLACK_WORKSPACE_ID",
                slack_channel_id="YOUR_SLACK_CHANNEL_ID"
            )
            
            rule = project.notify_on_build_succeeded("NotifyOnBuildSucceeded", target)
        '''
        if isinstance(log_retention_retry_options, dict):
            log_retention_retry_options = _LogRetentionRetryOptions_c6b3d73a(**log_retention_retry_options)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0ecb400e67a6ee4d0c9b907e9d4ae357d18e1db85a9e3e3fbb73e2a2be4ac36)
            check_type(argname="argument slack_channel_configuration_name", value=slack_channel_configuration_name, expected_type=type_hints["slack_channel_configuration_name"])
            check_type(argname="argument slack_channel_id", value=slack_channel_id, expected_type=type_hints["slack_channel_id"])
            check_type(argname="argument slack_workspace_id", value=slack_workspace_id, expected_type=type_hints["slack_workspace_id"])
            check_type(argname="argument logging_level", value=logging_level, expected_type=type_hints["logging_level"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument log_retention_retry_options", value=log_retention_retry_options, expected_type=type_hints["log_retention_retry_options"])
            check_type(argname="argument log_retention_role", value=log_retention_role, expected_type=type_hints["log_retention_role"])
            check_type(argname="argument notification_topics", value=notification_topics, expected_type=type_hints["notification_topics"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "slack_channel_configuration_name": slack_channel_configuration_name,
            "slack_channel_id": slack_channel_id,
            "slack_workspace_id": slack_workspace_id,
        }
        if logging_level is not None:
            self._values["logging_level"] = logging_level
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if log_retention_retry_options is not None:
            self._values["log_retention_retry_options"] = log_retention_retry_options
        if log_retention_role is not None:
            self._values["log_retention_role"] = log_retention_role
        if notification_topics is not None:
            self._values["notification_topics"] = notification_topics
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def slack_channel_configuration_name(self) -> builtins.str:
        '''(experimental) The name of Slack channel configuration.

        :stability: experimental
        '''
        result = self._values.get("slack_channel_configuration_name")
        assert result is not None, "Required property 'slack_channel_configuration_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slack_channel_id(self) -> builtins.str:
        '''(experimental) The ID of the Slack channel.

        To get the ID, open Slack, right click on the channel name in the left pane, then choose Copy Link.
        The channel ID is the 9-character string at the end of the URL. For example, ABCBBLZZZ.

        :stability: experimental
        '''
        result = self._values.get("slack_channel_id")
        assert result is not None, "Required property 'slack_channel_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def slack_workspace_id(self) -> builtins.str:
        '''(experimental) The ID of the Slack workspace authorized with AWS Chatbot.

        To get the workspace ID, you must perform the initial authorization flow with Slack in the AWS Chatbot console.
        Then you can copy and paste the workspace ID from the console.
        For more details, see steps 1-4 in Setting Up AWS Chatbot with Slack in the AWS Chatbot User Guide.

        :see: https://docs.aws.amazon.com/chatbot/latest/adminguide/setting-up.html#Setup_intro
        :stability: experimental
        '''
        result = self._values.get("slack_workspace_id")
        assert result is not None, "Required property 'slack_workspace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def logging_level(self) -> typing.Optional[LoggingLevel]:
        '''(experimental) Specifies the logging level for this configuration.

        This property affects the log entries pushed to Amazon CloudWatch Logs.

        :default: LoggingLevel.NONE

        :stability: experimental
        '''
        result = self._values.get("logging_level")
        return typing.cast(typing.Optional[LoggingLevel], result)

    @builtins.property
    def log_retention(self) -> typing.Optional[_RetentionDays_6c560d31]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.INFINITE

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_RetentionDays_6c560d31], result)

    @builtins.property
    def log_retention_retry_options(
        self,
    ) -> typing.Optional[_LogRetentionRetryOptions_c6b3d73a]:
        '''(experimental) When log retention is specified, a custom resource attempts to create the CloudWatch log group.

        These options control the retry policy when interacting with CloudWatch APIs.

        :default: - Default AWS SDK retry options.

        :stability: experimental
        '''
        result = self._values.get("log_retention_retry_options")
        return typing.cast(typing.Optional[_LogRetentionRetryOptions_c6b3d73a], result)

    @builtins.property
    def log_retention_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        :default: - A new role is created.

        :stability: experimental
        '''
        result = self._values.get("log_retention_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def notification_topics(self) -> typing.Optional[typing.List[_ITopic_465e36b9]]:
        '''(experimental) The SNS topics that deliver notifications to AWS Chatbot.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("notification_topics")
        return typing.cast(typing.Optional[typing.List[_ITopic_465e36b9]], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The permission role of Slack channel configuration.

        :default: - A role will be created.

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SlackChannelConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnSlackChannelConfiguration",
    "CfnSlackChannelConfigurationProps",
    "ISlackChannelConfiguration",
    "LoggingLevel",
    "SlackChannelConfiguration",
    "SlackChannelConfigurationProps",
]

publication.publish()

def _typecheckingstub__fd0412d8f818742b46d15eb194d87cac54799e66193cc8229e544b28e626b856(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    configuration_name: builtins.str,
    iam_role_arn: builtins.str,
    slack_channel_id: builtins.str,
    slack_workspace_id: builtins.str,
    guardrail_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_level: typing.Optional[builtins.str] = None,
    sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_role_required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee73351f4d4f3368db9cfa57e5826dd093b9e531e3469733f483605f3a0d4b5(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4026dde0d321dad3e47e395f5715de904e213da903a7fcdde9ed75e6ee63f46e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c590fedf0abe8ef009317b609259c5f58fe4b3043f27a4f11add95019bd8d79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f359c90f82be9856c7adcc7d0bff8ba99d0ee4c26849035fbcaafd2cf4933ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eaa8cb019aa5506fac10e297ae6d7331fd21e82b30676011beb4f62a6e684621(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc94f7cb95ac359119dc432843eb5b4bcd11d3d7467b565a01435edaba2fbfa6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64429f2750f4405f0b4dcb28e5a5b948ac2acf7c4b483e1425ccc094bc771054(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c08d61dd4d0672bd65aa20807a196a2324ee36588f7a8003c0d0bf2a091e87c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c255630a2b443a1de133faed964ba20b03d128b859708fe81b498b3c971160(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c60b375f5901966ece93900df3a8255fa4d4dd5005e99edf64b7cf28e0c47caf(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4890d38518885f1c140a5326bc6c191c515f3a51b190eda3b677a610ce6eb9e5(
    *,
    configuration_name: builtins.str,
    iam_role_arn: builtins.str,
    slack_channel_id: builtins.str,
    slack_workspace_id: builtins.str,
    guardrail_policies: typing.Optional[typing.Sequence[builtins.str]] = None,
    logging_level: typing.Optional[builtins.str] = None,
    sns_topic_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    user_role_required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29458baa00a3496fa8875b25454701b3f109dec008af03d28580229f90b0933d(
    statement: _PolicyStatement_296fe8a3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e3831ef79c26734a4aa9c2e741cef5b5d58486046b61cf872e2838ef38d6eb(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_Unit_113c79f9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2558412e17a6cae8d7e937245f5a4d89d66e1c8fed2e1f9a6351f2d7b5667d1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    slack_channel_configuration_name: builtins.str,
    slack_channel_id: builtins.str,
    slack_workspace_id: builtins.str,
    logging_level: typing.Optional[LoggingLevel] = None,
    log_retention: typing.Optional[_RetentionDays_6c560d31] = None,
    log_retention_retry_options: typing.Optional[typing.Union[_LogRetentionRetryOptions_c6b3d73a, typing.Dict[builtins.str, typing.Any]]] = None,
    log_retention_role: typing.Optional[_IRole_59af6f50] = None,
    notification_topics: typing.Optional[typing.Sequence[_ITopic_465e36b9]] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6887f1868e618b1cde129798dd05ca63d3f77b100a8893f4fc9b036def999f23(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    slack_channel_configuration_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ba4e917ea698b2065420506fc31058c04b5b3e9d203ee310d48f311a39b23a(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_Unit_113c79f9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc47b68088cb84d284d28a44c3f8ff7f2799adc13026a5cfcd9362e0dbb23cad(
    notification_topic: _ITopic_465e36b9,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69ca2e300e542a34f648ef554229c00bcaa08cb8226f508660a0d5f6e5421014(
    statement: _PolicyStatement_296fe8a3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21856da15f42d0dbaff885d4829646782f76f94f0368773438273b2cf830796e(
    _scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__155ad06c49a63697e955d5b98660ab80e27a3e5de0c6b92d35fbe4d11748312c(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_Unit_113c79f9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0ecb400e67a6ee4d0c9b907e9d4ae357d18e1db85a9e3e3fbb73e2a2be4ac36(
    *,
    slack_channel_configuration_name: builtins.str,
    slack_channel_id: builtins.str,
    slack_workspace_id: builtins.str,
    logging_level: typing.Optional[LoggingLevel] = None,
    log_retention: typing.Optional[_RetentionDays_6c560d31] = None,
    log_retention_retry_options: typing.Optional[typing.Union[_LogRetentionRetryOptions_c6b3d73a, typing.Dict[builtins.str, typing.Any]]] = None,
    log_retention_role: typing.Optional[_IRole_59af6f50] = None,
    notification_topics: typing.Optional[typing.Sequence[_ITopic_465e36b9]] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass
