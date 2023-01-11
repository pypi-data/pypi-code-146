'''
# AWS::DevOpsGuru Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_devopsguru as devopsguru
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for DevOpsGuru construct libraries](https://constructs.dev/search?q=devopsguru)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::DevOpsGuru resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DevOpsGuru.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::DevOpsGuru](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_DevOpsGuru.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
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

from ._jsii import *

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnNotificationChannel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-devopsguru.CfnNotificationChannel",
):
    '''A CloudFormation ``AWS::DevOpsGuru::NotificationChannel``.

    Adds a notification channel to DevOps Guru. A notification channel is used to notify you about important DevOps Guru events, such as when an insight is generated.

    If you use an Amazon SNS topic in another account, you must attach a policy to it that grants DevOps Guru permission to it notifications. DevOps Guru adds the required policy on your behalf to send notifications using Amazon SNS in your account. DevOps Guru only supports standard SNS topics. For more information, see `Permissions for cross account Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-required-permissions.html>`_ .

    If you use an Amazon SNS topic in another account, you must attach a policy to it that grants DevOps Guru permission to it notifications. DevOps Guru adds the required policy on your behalf to send notifications using Amazon SNS in your account. For more information, see Permissions for cross account Amazon SNS topics.

    If you use an Amazon SNS topic that is encrypted by an AWS Key Management Service customer-managed key (CMK), then you must add permissions to the CMK. For more information, see `Permissions for AWS KMS–encrypted Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-kms-permissions.html>`_ .

    :cloudformationResource: AWS::DevOpsGuru::NotificationChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-notificationchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_devopsguru as devopsguru
        
        cfn_notification_channel = devopsguru.CfnNotificationChannel(self, "MyCfnNotificationChannel",
            config=devopsguru.CfnNotificationChannel.NotificationChannelConfigProperty(
                filters=devopsguru.CfnNotificationChannel.NotificationFilterConfigProperty(
                    message_types=["messageTypes"],
                    severities=["severities"]
                ),
                sns=devopsguru.CfnNotificationChannel.SnsChannelConfigProperty(
                    topic_arn="topicArn"
                )
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        config: typing.Union[typing.Union["CfnNotificationChannel.NotificationChannelConfigProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        '''Create a new ``AWS::DevOpsGuru::NotificationChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param config: A ``NotificationChannelConfig`` object that contains information about configured notification channels.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31c06066b3003ff8d9da37ebb15bedfaff5076bf165ac95e12bdcbcb7c4f55ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnNotificationChannelProps(config=config)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3556039464b7fcc81d098e1c4222016d7db5822310db94a2fccb9b9d2badf9a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__dc968e7600659321ee24850469d8cac89549fc85a0245f40e0118f11d4c626b3)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the notification channel.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(
        self,
    ) -> typing.Union["CfnNotificationChannel.NotificationChannelConfigProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''A ``NotificationChannelConfig`` object that contains information about configured notification channels.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-notificationchannel.html#cfn-devopsguru-notificationchannel-config
        '''
        return typing.cast(typing.Union["CfnNotificationChannel.NotificationChannelConfigProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "config"))

    @config.setter
    def config(
        self,
        value: typing.Union["CfnNotificationChannel.NotificationChannelConfigProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adea638fa6ddda72a64100b4c225a01cf7eb8ee82ca03f38e132467d5f5e8b66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "config", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-devopsguru.CfnNotificationChannel.NotificationChannelConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"filters": "filters", "sns": "sns"},
    )
    class NotificationChannelConfigProperty:
        def __init__(
            self,
            *,
            filters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnNotificationChannel.NotificationFilterConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sns: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnNotificationChannel.SnsChannelConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about notification channels you have configured with DevOps Guru.

            The one supported notification channel is Amazon Simple Notification Service (Amazon SNS).

            :param filters: The filter configurations for the Amazon SNS notification topic you use with DevOps Guru. If you do not provide filter configurations, the default configurations are to receive notifications for all message types of ``High`` or ``Medium`` severity.
            :param sns: Information about a notification channel configured in DevOps Guru to send notifications when insights are created. If you use an Amazon SNS topic in another account, you must attach a policy to it that grants DevOps Guru permission to it notifications. DevOps Guru adds the required policy on your behalf to send notifications using Amazon SNS in your account. DevOps Guru only supports standard SNS topics. For more information, see `Permissions for cross account Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-required-permissions.html>`_ . If you use an Amazon SNS topic in another account, you must attach a policy to it that grants DevOps Guru permission to it notifications. DevOps Guru adds the required policy on your behalf to send notifications using Amazon SNS in your account. For more information, see Permissions for cross account Amazon SNS topics. If you use an Amazon SNS topic that is encrypted by an AWS Key Management Service customer-managed key (CMK), then you must add permissions to the CMK. For more information, see `Permissions for AWS KMS–encrypted Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-kms-permissions.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-notificationchannelconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_devopsguru as devopsguru
                
                notification_channel_config_property = devopsguru.CfnNotificationChannel.NotificationChannelConfigProperty(
                    filters=devopsguru.CfnNotificationChannel.NotificationFilterConfigProperty(
                        message_types=["messageTypes"],
                        severities=["severities"]
                    ),
                    sns=devopsguru.CfnNotificationChannel.SnsChannelConfigProperty(
                        topic_arn="topicArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c2a397ad906bf6ceb9c0961b03a2b27ceb560c56d23935b941945c2f2b122c9b)
                check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
                check_type(argname="argument sns", value=sns, expected_type=type_hints["sns"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if filters is not None:
                self._values["filters"] = filters
            if sns is not None:
                self._values["sns"] = sns

        @builtins.property
        def filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnNotificationChannel.NotificationFilterConfigProperty"]]:
            '''The filter configurations for the Amazon SNS notification topic you use with DevOps Guru.

            If you do not provide filter configurations, the default configurations are to receive notifications for all message types of ``High`` or ``Medium`` severity.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-notificationchannelconfig.html#cfn-devopsguru-notificationchannel-notificationchannelconfig-filters
            '''
            result = self._values.get("filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnNotificationChannel.NotificationFilterConfigProperty"]], result)

        @builtins.property
        def sns(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnNotificationChannel.SnsChannelConfigProperty"]]:
            '''Information about a notification channel configured in DevOps Guru to send notifications when insights are created.

            If you use an Amazon SNS topic in another account, you must attach a policy to it that grants DevOps Guru permission to it notifications. DevOps Guru adds the required policy on your behalf to send notifications using Amazon SNS in your account. DevOps Guru only supports standard SNS topics. For more information, see `Permissions for cross account Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-required-permissions.html>`_ .

            If you use an Amazon SNS topic in another account, you must attach a policy to it that grants DevOps Guru permission to it notifications. DevOps Guru adds the required policy on your behalf to send notifications using Amazon SNS in your account. For more information, see Permissions for cross account Amazon SNS topics.

            If you use an Amazon SNS topic that is encrypted by an AWS Key Management Service customer-managed key (CMK), then you must add permissions to the CMK. For more information, see `Permissions for AWS KMS–encrypted Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-kms-permissions.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-notificationchannelconfig.html#cfn-devopsguru-notificationchannel-notificationchannelconfig-sns
            '''
            result = self._values.get("sns")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnNotificationChannel.SnsChannelConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationChannelConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-devopsguru.CfnNotificationChannel.NotificationFilterConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"message_types": "messageTypes", "severities": "severities"},
    )
    class NotificationFilterConfigProperty:
        def __init__(
            self,
            *,
            message_types: typing.Optional[typing.Sequence[builtins.str]] = None,
            severities: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The filter configurations for the Amazon SNS notification topic you use with DevOps Guru.

            You can choose to specify which events or message types to receive notifications for. You can also choose to specify which severity levels to receive notifications for.

            :param message_types: The events that you want to receive notifications for. For example, you can choose to receive notifications only when the severity level is upgraded or a new insight is created.
            :param severities: The severity levels that you want to receive notifications for. For example, you can choose to receive notifications only for insights with ``HIGH`` and ``MEDIUM`` severity levels. For more information, see `Understanding insight severities <https://docs.aws.amazon.com/devops-guru/latest/userguide/working-with-insights.html#understanding-insights-severities>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-notificationfilterconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_devopsguru as devopsguru
                
                notification_filter_config_property = devopsguru.CfnNotificationChannel.NotificationFilterConfigProperty(
                    message_types=["messageTypes"],
                    severities=["severities"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3fe9953f715dcc692ab6a0f882bf21bc6692ce37437d1198c0789f8d11f8b29b)
                check_type(argname="argument message_types", value=message_types, expected_type=type_hints["message_types"])
                check_type(argname="argument severities", value=severities, expected_type=type_hints["severities"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if message_types is not None:
                self._values["message_types"] = message_types
            if severities is not None:
                self._values["severities"] = severities

        @builtins.property
        def message_types(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The events that you want to receive notifications for.

            For example, you can choose to receive notifications only when the severity level is upgraded or a new insight is created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-notificationfilterconfig.html#cfn-devopsguru-notificationchannel-notificationfilterconfig-messagetypes
            '''
            result = self._values.get("message_types")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def severities(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The severity levels that you want to receive notifications for.

            For example, you can choose to receive notifications only for insights with ``HIGH`` and ``MEDIUM`` severity levels. For more information, see `Understanding insight severities <https://docs.aws.amazon.com/devops-guru/latest/userguide/working-with-insights.html#understanding-insights-severities>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-notificationfilterconfig.html#cfn-devopsguru-notificationchannel-notificationfilterconfig-severities
            '''
            result = self._values.get("severities")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationFilterConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-devopsguru.CfnNotificationChannel.SnsChannelConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"topic_arn": "topicArn"},
    )
    class SnsChannelConfigProperty:
        def __init__(self, *, topic_arn: typing.Optional[builtins.str] = None) -> None:
            '''Contains the Amazon Resource Name (ARN) of an Amazon Simple Notification Service topic.

            If you use an Amazon SNS topic in another account, you must attach a policy to it that grants DevOps Guru permission to it notifications. DevOps Guru adds the required policy on your behalf to send notifications using Amazon SNS in your account. DevOps Guru only supports standard SNS topics. For more information, see `Permissions for cross account Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-required-permissions.html>`_ .

            If you use an Amazon SNS topic in another account, you must attach a policy to it that grants DevOps Guru permission to it notifications. DevOps Guru adds the required policy on your behalf to send notifications using Amazon SNS in your account. For more information, see Permissions for cross account Amazon SNS topics.

            If you use an Amazon SNS topic that is encrypted by an AWS Key Management Service customer-managed key (CMK), then you must add permissions to the CMK. For more information, see `Permissions for AWS KMS–encrypted Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-kms-permissions.html>`_ .

            :param topic_arn: The Amazon Resource Name (ARN) of an Amazon Simple Notification Service topic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-snschannelconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_devopsguru as devopsguru
                
                sns_channel_config_property = devopsguru.CfnNotificationChannel.SnsChannelConfigProperty(
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9208bd1ac08c3b5daea644bb8aebf000cb363880cf31dbf8ec45e1b067681abd)
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of an Amazon Simple Notification Service topic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-snschannelconfig.html#cfn-devopsguru-notificationchannel-snschannelconfig-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnsChannelConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-devopsguru.CfnNotificationChannelProps",
    jsii_struct_bases=[],
    name_mapping={"config": "config"},
)
class CfnNotificationChannelProps:
    def __init__(
        self,
        *,
        config: typing.Union[typing.Union[CfnNotificationChannel.NotificationChannelConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        '''Properties for defining a ``CfnNotificationChannel``.

        :param config: A ``NotificationChannelConfig`` object that contains information about configured notification channels.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-notificationchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_devopsguru as devopsguru
            
            cfn_notification_channel_props = devopsguru.CfnNotificationChannelProps(
                config=devopsguru.CfnNotificationChannel.NotificationChannelConfigProperty(
                    filters=devopsguru.CfnNotificationChannel.NotificationFilterConfigProperty(
                        message_types=["messageTypes"],
                        severities=["severities"]
                    ),
                    sns=devopsguru.CfnNotificationChannel.SnsChannelConfigProperty(
                        topic_arn="topicArn"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f24d8090b1d7fd688e1f7fc33b8a37697307799794cd2046962b894410692c2)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config": config,
        }

    @builtins.property
    def config(
        self,
    ) -> typing.Union[CfnNotificationChannel.NotificationChannelConfigProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''A ``NotificationChannelConfig`` object that contains information about configured notification channels.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-notificationchannel.html#cfn-devopsguru-notificationchannel-config
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast(typing.Union[CfnNotificationChannel.NotificationChannelConfigProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNotificationChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResourceCollection(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-devopsguru.CfnResourceCollection",
):
    '''A CloudFormation ``AWS::DevOpsGuru::ResourceCollection``.

    A collection of AWS resources supported by DevOps Guru. The one type of AWS resource collection supported is AWS CloudFormation stacks. DevOps Guru can be configured to analyze only the AWS resources that are defined in the stacks.

    :cloudformationResource: AWS::DevOpsGuru::ResourceCollection
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-resourcecollection.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_devopsguru as devopsguru
        
        cfn_resource_collection = devopsguru.CfnResourceCollection(self, "MyCfnResourceCollection",
            resource_collection_filter=devopsguru.CfnResourceCollection.ResourceCollectionFilterProperty(
                cloud_formation=devopsguru.CfnResourceCollection.CloudFormationCollectionFilterProperty(
                    stack_names=["stackNames"]
                ),
                tags=[devopsguru.CfnResourceCollection.TagCollectionProperty(
                    app_boundary_key="appBoundaryKey",
                    tag_values=["tagValues"]
                )]
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        resource_collection_filter: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceCollection.ResourceCollectionFilterProperty", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''Create a new ``AWS::DevOpsGuru::ResourceCollection``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resource_collection_filter: Information about a filter used to specify which AWS resources are analyzed for anomalous behavior by DevOps Guru.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f91868a5265bc126078ff5b3595cfb0e5f921298fef0a1403f76b945aa549420)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourceCollectionProps(
            resource_collection_filter=resource_collection_filter
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f1725787f9f67c725570a56df5f471201f28766a27f04bdf1f5455390e0e289)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d91dc8cefa404331e1f7e481fe62d663fc4d53fb2cf988d53589bf484503844)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrResourceCollectionType")
    def attr_resource_collection_type(self) -> builtins.str:
        '''The type of AWS resource collections to return.

        The one valid value is ``CLOUD_FORMATION`` for AWS CloudFormation stacks.

        :cloudformationAttribute: ResourceCollectionType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceCollectionType"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="resourceCollectionFilter")
    def resource_collection_filter(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceCollection.ResourceCollectionFilterProperty"]:
        '''Information about a filter used to specify which AWS resources are analyzed for anomalous behavior by DevOps Guru.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-resourcecollection.html#cfn-devopsguru-resourcecollection-resourcecollectionfilter
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceCollection.ResourceCollectionFilterProperty"], jsii.get(self, "resourceCollectionFilter"))

    @resource_collection_filter.setter
    def resource_collection_filter(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceCollection.ResourceCollectionFilterProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54febd8bfa98035bf9c56766e84d3c38b7f5656c5f0b31bfe4ebe8b1e4832529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceCollectionFilter", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-devopsguru.CfnResourceCollection.CloudFormationCollectionFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"stack_names": "stackNames"},
    )
    class CloudFormationCollectionFilterProperty:
        def __init__(
            self,
            *,
            stack_names: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Information about AWS CloudFormation stacks.

            You can use up to 500 stacks to specify which AWS resources in your account to analyze. For more information, see `Stacks <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacks.html>`_ in the *AWS CloudFormation User Guide* .

            :param stack_names: An array of CloudFormation stack names.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-cloudformationcollectionfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_devopsguru as devopsguru
                
                cloud_formation_collection_filter_property = devopsguru.CfnResourceCollection.CloudFormationCollectionFilterProperty(
                    stack_names=["stackNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0c60363e53e50cb43c392294b7f43d7936d431d2a83ca93a78dca8d08893635f)
                check_type(argname="argument stack_names", value=stack_names, expected_type=type_hints["stack_names"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if stack_names is not None:
                self._values["stack_names"] = stack_names

        @builtins.property
        def stack_names(self) -> typing.Optional[typing.List[builtins.str]]:
            '''An array of CloudFormation stack names.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-cloudformationcollectionfilter.html#cfn-devopsguru-resourcecollection-cloudformationcollectionfilter-stacknames
            '''
            result = self._values.get("stack_names")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudFormationCollectionFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-devopsguru.CfnResourceCollection.ResourceCollectionFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_formation": "cloudFormation", "tags": "tags"},
    )
    class ResourceCollectionFilterProperty:
        def __init__(
            self,
            *,
            cloud_formation: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResourceCollection.CloudFormationCollectionFilterProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tags: typing.Optional[typing.Sequence[typing.Union["CfnResourceCollection.TagCollectionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Information about a filter used to specify which AWS resources are analyzed for anomalous behavior by DevOps Guru.

            :param cloud_formation: Information about AWS CloudFormation stacks. You can use up to 500 stacks to specify which AWS resources in your account to analyze. For more information, see `Stacks <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacks.html>`_ in the *AWS CloudFormation User Guide* .
            :param tags: The AWS tags used to filter the resources in the resource collection. Tags help you identify and organize your AWS resources. Many AWS services support tagging, so you can assign the same tag to resources from different services to indicate that the resources are related. For example, you can assign the same tag to an Amazon DynamoDB table resource that you assign to an AWS Lambda function. For more information about using tags, see the `Tagging best practices <https://docs.aws.amazon.com/https://d1.awsstatic.com/whitepapers/aws-tagging-best-practices.pdf>`_ whitepaper. Each AWS tag has two parts. - A tag *key* (for example, ``CostCenter`` , ``Environment`` , ``Project`` , or ``Secret`` ). Tag *keys* are case-sensitive. - An optional field known as a tag *value* (for example, ``111122223333`` , ``Production`` , or a team name). Omitting the tag *value* is the same as using an empty string. Like tag *keys* , tag *values* are case-sensitive. Together these are known as *key* - *value* pairs. .. epigraph:: The string used for a *key* in a tag that you use to define your resource coverage must begin with the prefix ``Devops-guru-`` . The tag *key* might be ``DevOps-Guru-deployment-application`` or ``devops-guru-rds-application`` . When you create a *key* , the case of characters in the *key* can be whatever you choose. After you create a *key* , it is case-sensitive. For example, DevOps Guru works with a *key* named ``devops-guru-rds`` and a *key* named ``DevOps-Guru-RDS`` , and these act as two different *keys* . Possible *key* / *value* pairs in your application might be ``Devops-Guru-production-application/RDS`` or ``Devops-Guru-production-application/containers`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-resourcecollectionfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_devopsguru as devopsguru
                
                resource_collection_filter_property = devopsguru.CfnResourceCollection.ResourceCollectionFilterProperty(
                    cloud_formation=devopsguru.CfnResourceCollection.CloudFormationCollectionFilterProperty(
                        stack_names=["stackNames"]
                    ),
                    tags=[devopsguru.CfnResourceCollection.TagCollectionProperty(
                        app_boundary_key="appBoundaryKey",
                        tag_values=["tagValues"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04a7bb74cd38fa4c5bed22295950ff69859ebd6433f3fc8457fe57bf99428ec5)
                check_type(argname="argument cloud_formation", value=cloud_formation, expected_type=type_hints["cloud_formation"])
                check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cloud_formation is not None:
                self._values["cloud_formation"] = cloud_formation
            if tags is not None:
                self._values["tags"] = tags

        @builtins.property
        def cloud_formation(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceCollection.CloudFormationCollectionFilterProperty"]]:
            '''Information about AWS CloudFormation stacks.

            You can use up to 500 stacks to specify which AWS resources in your account to analyze. For more information, see `Stacks <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacks.html>`_ in the *AWS CloudFormation User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-resourcecollectionfilter.html#cfn-devopsguru-resourcecollection-resourcecollectionfilter-cloudformation
            '''
            result = self._values.get("cloud_formation")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResourceCollection.CloudFormationCollectionFilterProperty"]], result)

        @builtins.property
        def tags(
            self,
        ) -> typing.Optional[typing.List["CfnResourceCollection.TagCollectionProperty"]]:
            '''The AWS tags used to filter the resources in the resource collection.

            Tags help you identify and organize your AWS resources. Many AWS services support tagging, so you can assign the same tag to resources from different services to indicate that the resources are related. For example, you can assign the same tag to an Amazon DynamoDB table resource that you assign to an AWS Lambda function. For more information about using tags, see the `Tagging best practices <https://docs.aws.amazon.com/https://d1.awsstatic.com/whitepapers/aws-tagging-best-practices.pdf>`_ whitepaper.

            Each AWS tag has two parts.

            - A tag *key* (for example, ``CostCenter`` , ``Environment`` , ``Project`` , or ``Secret`` ). Tag *keys* are case-sensitive.
            - An optional field known as a tag *value* (for example, ``111122223333`` , ``Production`` , or a team name). Omitting the tag *value* is the same as using an empty string. Like tag *keys* , tag *values* are case-sensitive.

            Together these are known as *key* - *value* pairs.
            .. epigraph::

               The string used for a *key* in a tag that you use to define your resource coverage must begin with the prefix ``Devops-guru-`` . The tag *key* might be ``DevOps-Guru-deployment-application`` or ``devops-guru-rds-application`` . When you create a *key* , the case of characters in the *key* can be whatever you choose. After you create a *key* , it is case-sensitive. For example, DevOps Guru works with a *key* named ``devops-guru-rds`` and a *key* named ``DevOps-Guru-RDS`` , and these act as two different *keys* . Possible *key* / *value* pairs in your application might be ``Devops-Guru-production-application/RDS`` or ``Devops-Guru-production-application/containers`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-resourcecollectionfilter.html#cfn-devopsguru-resourcecollection-resourcecollectionfilter-tags
            '''
            result = self._values.get("tags")
            return typing.cast(typing.Optional[typing.List["CfnResourceCollection.TagCollectionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceCollectionFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-devopsguru.CfnResourceCollection.TagCollectionProperty",
        jsii_struct_bases=[],
        name_mapping={"app_boundary_key": "appBoundaryKey", "tag_values": "tagValues"},
    )
    class TagCollectionProperty:
        def __init__(
            self,
            *,
            app_boundary_key: typing.Optional[builtins.str] = None,
            tag_values: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A collection of AWS tags.

            Tags help you identify and organize your AWS resources. Many AWS services support tagging, so you can assign the same tag to resources from different services to indicate that the resources are related. For example, you can assign the same tag to an Amazon DynamoDB table resource that you assign to an AWS Lambda function. For more information about using tags, see the `Tagging best practices <https://docs.aws.amazon.com/https://d1.awsstatic.com/whitepapers/aws-tagging-best-practices.pdf>`_ whitepaper.

            Each AWS tag has two parts.

            - A tag *key* (for example, ``CostCenter`` , ``Environment`` , ``Project`` , or ``Secret`` ). Tag *keys* are case-sensitive.
            - An optional field known as a tag *value* (for example, ``111122223333`` , ``Production`` , or a team name). Omitting the tag *value* is the same as using an empty string. Like tag *keys* , tag *values* are case-sensitive.

            Together these are known as *key* - *value* pairs.
            .. epigraph::

               The string used for a *key* in a tag that you use to define your resource coverage must begin with the prefix ``Devops-guru-`` . The tag *key* might be ``DevOps-Guru-deployment-application`` or ``devops-guru-rds-application`` . When you create a *key* , the case of characters in the *key* can be whatever you choose. After you create a *key* , it is case-sensitive. For example, DevOps Guru works with a *key* named ``devops-guru-rds`` and a *key* named ``DevOps-Guru-RDS`` , and these act as two different *keys* . Possible *key* / *value* pairs in your application might be ``Devops-Guru-production-application/RDS`` or ``Devops-Guru-production-application/containers`` .

            :param app_boundary_key: An AWS tag *key* that is used to identify the AWS resources that DevOps Guru analyzes. All AWS resources in your account and Region tagged with this *key* make up your DevOps Guru application and analysis boundary. .. epigraph:: The string used for a *key* in a tag that you use to define your resource coverage must begin with the prefix ``Devops-guru-`` . The tag *key* might be ``DevOps-Guru-deployment-application`` or ``devops-guru-rds-application`` . When you create a *key* , the case of characters in the *key* can be whatever you choose. After you create a *key* , it is case-sensitive. For example, DevOps Guru works with a *key* named ``devops-guru-rds`` and a *key* named ``DevOps-Guru-RDS`` , and these act as two different *keys* . Possible *key* / *value* pairs in your application might be ``Devops-Guru-production-application/RDS`` or ``Devops-Guru-production-application/containers`` .
            :param tag_values: The values in an AWS tag collection. The tag's *value* is an optional field used to associate a string with the tag *key* (for example, ``111122223333`` , ``Production`` , or a team name). The *key* and *value* are the tag's *key* pair. Omitting the tag *value* is the same as using an empty string. Like tag *keys* , tag *values* are case-sensitive. You can specify a maximum of 256 characters for a tag value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-tagcollection.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_devopsguru as devopsguru
                
                tag_collection_property = devopsguru.CfnResourceCollection.TagCollectionProperty(
                    app_boundary_key="appBoundaryKey",
                    tag_values=["tagValues"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f24edc8b1b2d32174d71a3353f48cb92e72fe5fad6b1c1c984e8c56cdcdcfc27)
                check_type(argname="argument app_boundary_key", value=app_boundary_key, expected_type=type_hints["app_boundary_key"])
                check_type(argname="argument tag_values", value=tag_values, expected_type=type_hints["tag_values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if app_boundary_key is not None:
                self._values["app_boundary_key"] = app_boundary_key
            if tag_values is not None:
                self._values["tag_values"] = tag_values

        @builtins.property
        def app_boundary_key(self) -> typing.Optional[builtins.str]:
            '''An AWS tag *key* that is used to identify the AWS resources that DevOps Guru analyzes.

            All AWS resources in your account and Region tagged with this *key* make up your DevOps Guru application and analysis boundary.
            .. epigraph::

               The string used for a *key* in a tag that you use to define your resource coverage must begin with the prefix ``Devops-guru-`` . The tag *key* might be ``DevOps-Guru-deployment-application`` or ``devops-guru-rds-application`` . When you create a *key* , the case of characters in the *key* can be whatever you choose. After you create a *key* , it is case-sensitive. For example, DevOps Guru works with a *key* named ``devops-guru-rds`` and a *key* named ``DevOps-Guru-RDS`` , and these act as two different *keys* . Possible *key* / *value* pairs in your application might be ``Devops-Guru-production-application/RDS`` or ``Devops-Guru-production-application/containers`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-tagcollection.html#cfn-devopsguru-resourcecollection-tagcollection-appboundarykey
            '''
            result = self._values.get("app_boundary_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tag_values(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The values in an AWS tag collection.

            The tag's *value* is an optional field used to associate a string with the tag *key* (for example, ``111122223333`` , ``Production`` , or a team name). The *key* and *value* are the tag's *key* pair. Omitting the tag *value* is the same as using an empty string. Like tag *keys* , tag *values* are case-sensitive. You can specify a maximum of 256 characters for a tag value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-tagcollection.html#cfn-devopsguru-resourcecollection-tagcollection-tagvalues
            '''
            result = self._values.get("tag_values")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagCollectionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-devopsguru.CfnResourceCollectionProps",
    jsii_struct_bases=[],
    name_mapping={"resource_collection_filter": "resourceCollectionFilter"},
)
class CfnResourceCollectionProps:
    def __init__(
        self,
        *,
        resource_collection_filter: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceCollection.ResourceCollectionFilterProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''Properties for defining a ``CfnResourceCollection``.

        :param resource_collection_filter: Information about a filter used to specify which AWS resources are analyzed for anomalous behavior by DevOps Guru.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-resourcecollection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_devopsguru as devopsguru
            
            cfn_resource_collection_props = devopsguru.CfnResourceCollectionProps(
                resource_collection_filter=devopsguru.CfnResourceCollection.ResourceCollectionFilterProperty(
                    cloud_formation=devopsguru.CfnResourceCollection.CloudFormationCollectionFilterProperty(
                        stack_names=["stackNames"]
                    ),
                    tags=[devopsguru.CfnResourceCollection.TagCollectionProperty(
                        app_boundary_key="appBoundaryKey",
                        tag_values=["tagValues"]
                    )]
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40e3c7b5e00f6fb94be19c56f2748c8422d5677f0dc0777c6eb5761702c153a0)
            check_type(argname="argument resource_collection_filter", value=resource_collection_filter, expected_type=type_hints["resource_collection_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_collection_filter": resource_collection_filter,
        }

    @builtins.property
    def resource_collection_filter(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnResourceCollection.ResourceCollectionFilterProperty]:
        '''Information about a filter used to specify which AWS resources are analyzed for anomalous behavior by DevOps Guru.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-resourcecollection.html#cfn-devopsguru-resourcecollection-resourcecollectionfilter
        '''
        result = self._values.get("resource_collection_filter")
        assert result is not None, "Required property 'resource_collection_filter' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnResourceCollection.ResourceCollectionFilterProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceCollectionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnNotificationChannel",
    "CfnNotificationChannelProps",
    "CfnResourceCollection",
    "CfnResourceCollectionProps",
]

publication.publish()

def _typecheckingstub__31c06066b3003ff8d9da37ebb15bedfaff5076bf165ac95e12bdcbcb7c4f55ec(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    config: typing.Union[typing.Union[CfnNotificationChannel.NotificationChannelConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3556039464b7fcc81d098e1c4222016d7db5822310db94a2fccb9b9d2badf9a1(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc968e7600659321ee24850469d8cac89549fc85a0245f40e0118f11d4c626b3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adea638fa6ddda72a64100b4c225a01cf7eb8ee82ca03f38e132467d5f5e8b66(
    value: typing.Union[CfnNotificationChannel.NotificationChannelConfigProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2a397ad906bf6ceb9c0961b03a2b27ceb560c56d23935b941945c2f2b122c9b(
    *,
    filters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnNotificationChannel.NotificationFilterConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sns: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnNotificationChannel.SnsChannelConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe9953f715dcc692ab6a0f882bf21bc6692ce37437d1198c0789f8d11f8b29b(
    *,
    message_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    severities: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9208bd1ac08c3b5daea644bb8aebf000cb363880cf31dbf8ec45e1b067681abd(
    *,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f24d8090b1d7fd688e1f7fc33b8a37697307799794cd2046962b894410692c2(
    *,
    config: typing.Union[typing.Union[CfnNotificationChannel.NotificationChannelConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f91868a5265bc126078ff5b3595cfb0e5f921298fef0a1403f76b945aa549420(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    resource_collection_filter: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceCollection.ResourceCollectionFilterProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f1725787f9f67c725570a56df5f471201f28766a27f04bdf1f5455390e0e289(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d91dc8cefa404331e1f7e481fe62d663fc4d53fb2cf988d53589bf484503844(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54febd8bfa98035bf9c56766e84d3c38b7f5656c5f0b31bfe4ebe8b1e4832529(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnResourceCollection.ResourceCollectionFilterProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c60363e53e50cb43c392294b7f43d7936d431d2a83ca93a78dca8d08893635f(
    *,
    stack_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04a7bb74cd38fa4c5bed22295950ff69859ebd6433f3fc8457fe57bf99428ec5(
    *,
    cloud_formation: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceCollection.CloudFormationCollectionFilterProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnResourceCollection.TagCollectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f24edc8b1b2d32174d71a3353f48cb92e72fe5fad6b1c1c984e8c56cdcdcfc27(
    *,
    app_boundary_key: typing.Optional[builtins.str] = None,
    tag_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40e3c7b5e00f6fb94be19c56f2748c8422d5677f0dc0777c6eb5761702c153a0(
    *,
    resource_collection_filter: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResourceCollection.ResourceCollectionFilterProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass
