'''
# AWS::DevOpsGuru Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as devopsguru
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

from .._jsii import *

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnNotificationChannel(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_devopsguru.CfnNotificationChannel",
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
        from monocdk import aws_devopsguru as devopsguru
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        config: typing.Union[typing.Union["CfnNotificationChannel.NotificationChannelConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    ) -> None:
        '''Create a new ``AWS::DevOpsGuru::NotificationChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param config: A ``NotificationChannelConfig`` object that contains information about configured notification channels.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bbae86d41aea0585a2eaac6a3f32b425ad2b816c314e4927e6d332ea05e0718)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnNotificationChannelProps(config=config)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ea7ea5eb95d96b8eb193b06dd64026d9f9a83e37899a0ba9cddc0f3e8a5311b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20f24c5c030821c4f9ecfe0a0bcfa9ddba48a65227d8add919d7653a31cef6b0)
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
    ) -> typing.Union["CfnNotificationChannel.NotificationChannelConfigProperty", _IResolvable_a771d0ef]:
        '''A ``NotificationChannelConfig`` object that contains information about configured notification channels.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-notificationchannel.html#cfn-devopsguru-notificationchannel-config
        '''
        return typing.cast(typing.Union["CfnNotificationChannel.NotificationChannelConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "config"))

    @config.setter
    def config(
        self,
        value: typing.Union["CfnNotificationChannel.NotificationChannelConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e84d1c63356a2e4ecaa15ce344db06ba4489b4a93d8dbccf8c07e87a7478044c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "config", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_devopsguru.CfnNotificationChannel.NotificationChannelConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"filters": "filters", "sns": "sns"},
    )
    class NotificationChannelConfigProperty:
        def __init__(
            self,
            *,
            filters: typing.Optional[typing.Union[typing.Union["CfnNotificationChannel.NotificationFilterConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            sns: typing.Optional[typing.Union[typing.Union["CfnNotificationChannel.SnsChannelConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_devopsguru as devopsguru
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__cc2e4465e46488b2716def351bbeba471b6d8a5e1a62e3e239c5b03ba7415eb8)
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
        ) -> typing.Optional[typing.Union["CfnNotificationChannel.NotificationFilterConfigProperty", _IResolvable_a771d0ef]]:
            '''The filter configurations for the Amazon SNS notification topic you use with DevOps Guru.

            If you do not provide filter configurations, the default configurations are to receive notifications for all message types of ``High`` or ``Medium`` severity.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-notificationchannelconfig.html#cfn-devopsguru-notificationchannel-notificationchannelconfig-filters
            '''
            result = self._values.get("filters")
            return typing.cast(typing.Optional[typing.Union["CfnNotificationChannel.NotificationFilterConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def sns(
            self,
        ) -> typing.Optional[typing.Union["CfnNotificationChannel.SnsChannelConfigProperty", _IResolvable_a771d0ef]]:
            '''Information about a notification channel configured in DevOps Guru to send notifications when insights are created.

            If you use an Amazon SNS topic in another account, you must attach a policy to it that grants DevOps Guru permission to it notifications. DevOps Guru adds the required policy on your behalf to send notifications using Amazon SNS in your account. DevOps Guru only supports standard SNS topics. For more information, see `Permissions for cross account Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-required-permissions.html>`_ .

            If you use an Amazon SNS topic in another account, you must attach a policy to it that grants DevOps Guru permission to it notifications. DevOps Guru adds the required policy on your behalf to send notifications using Amazon SNS in your account. For more information, see Permissions for cross account Amazon SNS topics.

            If you use an Amazon SNS topic that is encrypted by an AWS Key Management Service customer-managed key (CMK), then you must add permissions to the CMK. For more information, see `Permissions for AWS KMS–encrypted Amazon SNS topics <https://docs.aws.amazon.com/devops-guru/latest/userguide/sns-kms-permissions.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-notificationchannel-notificationchannelconfig.html#cfn-devopsguru-notificationchannel-notificationchannelconfig-sns
            '''
            result = self._values.get("sns")
            return typing.cast(typing.Optional[typing.Union["CfnNotificationChannel.SnsChannelConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NotificationChannelConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_devopsguru.CfnNotificationChannel.NotificationFilterConfigProperty",
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
                from monocdk import aws_devopsguru as devopsguru
                
                notification_filter_config_property = devopsguru.CfnNotificationChannel.NotificationFilterConfigProperty(
                    message_types=["messageTypes"],
                    severities=["severities"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0eadc6342bf29b81b3c4f49e62e8640c7432ca8a1d8538b22ce4a1ab5b8a64e2)
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
        jsii_type="monocdk.aws_devopsguru.CfnNotificationChannel.SnsChannelConfigProperty",
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
                from monocdk import aws_devopsguru as devopsguru
                
                sns_channel_config_property = devopsguru.CfnNotificationChannel.SnsChannelConfigProperty(
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f5f139d98dbcda10edbce11503dcdf35927f5e8c13cf9f8ca30f3a5f61b8632e)
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
    jsii_type="monocdk.aws_devopsguru.CfnNotificationChannelProps",
    jsii_struct_bases=[],
    name_mapping={"config": "config"},
)
class CfnNotificationChannelProps:
    def __init__(
        self,
        *,
        config: typing.Union[typing.Union[CfnNotificationChannel.NotificationChannelConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    ) -> None:
        '''Properties for defining a ``CfnNotificationChannel``.

        :param config: A ``NotificationChannelConfig`` object that contains information about configured notification channels.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-notificationchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_devopsguru as devopsguru
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__825c99d4860b79e84c4ad8c59225b5332d749b8b390f25892a772cfac4c80e57)
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config": config,
        }

    @builtins.property
    def config(
        self,
    ) -> typing.Union[CfnNotificationChannel.NotificationChannelConfigProperty, _IResolvable_a771d0ef]:
        '''A ``NotificationChannelConfig`` object that contains information about configured notification channels.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-notificationchannel.html#cfn-devopsguru-notificationchannel-config
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast(typing.Union[CfnNotificationChannel.NotificationChannelConfigProperty, _IResolvable_a771d0ef], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNotificationChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResourceCollection(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_devopsguru.CfnResourceCollection",
):
    '''A CloudFormation ``AWS::DevOpsGuru::ResourceCollection``.

    A collection of AWS resources supported by DevOps Guru. The one type of AWS resource collection supported is AWS CloudFormation stacks. DevOps Guru can be configured to analyze only the AWS resources that are defined in the stacks.

    :cloudformationResource: AWS::DevOpsGuru::ResourceCollection
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-resourcecollection.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_devopsguru as devopsguru
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        resource_collection_filter: typing.Union[typing.Union["CfnResourceCollection.ResourceCollectionFilterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    ) -> None:
        '''Create a new ``AWS::DevOpsGuru::ResourceCollection``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resource_collection_filter: Information about a filter used to specify which AWS resources are analyzed for anomalous behavior by DevOps Guru.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92b566b8728cdd7da1ab03e907718915745eb33e37ea5c6f13988bfdb660976e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourceCollectionProps(
            resource_collection_filter=resource_collection_filter
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0abcbd5733a8abfee13439dd6dbaa9548ae6dd3e2788abf49e50803c6c2959a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4ed90def3e7ff6d4f509b6b23e9f918f563f3a24ec43f34c9661c4e70f7f05ab)
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
    ) -> typing.Union["CfnResourceCollection.ResourceCollectionFilterProperty", _IResolvable_a771d0ef]:
        '''Information about a filter used to specify which AWS resources are analyzed for anomalous behavior by DevOps Guru.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-resourcecollection.html#cfn-devopsguru-resourcecollection-resourcecollectionfilter
        '''
        return typing.cast(typing.Union["CfnResourceCollection.ResourceCollectionFilterProperty", _IResolvable_a771d0ef], jsii.get(self, "resourceCollectionFilter"))

    @resource_collection_filter.setter
    def resource_collection_filter(
        self,
        value: typing.Union["CfnResourceCollection.ResourceCollectionFilterProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca9d09dd9877ebd9f704d1335fab78d85e95cf71aaa96cd16d95118e4fb2f384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceCollectionFilter", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_devopsguru.CfnResourceCollection.CloudFormationCollectionFilterProperty",
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
                from monocdk import aws_devopsguru as devopsguru
                
                cloud_formation_collection_filter_property = devopsguru.CfnResourceCollection.CloudFormationCollectionFilterProperty(
                    stack_names=["stackNames"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f2fd64417a4fd2babbce47418aede0e3f2a208489de9d718f2be06d1e73c8109)
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
        jsii_type="monocdk.aws_devopsguru.CfnResourceCollection.ResourceCollectionFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"cloud_formation": "cloudFormation", "tags": "tags"},
    )
    class ResourceCollectionFilterProperty:
        def __init__(
            self,
            *,
            cloud_formation: typing.Optional[typing.Union[typing.Union["CfnResourceCollection.CloudFormationCollectionFilterProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_devopsguru as devopsguru
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__26ce2195a03e357ce0d7eab3dcc2d79b39fad0f050b647c2fd29bb609058428d)
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
        ) -> typing.Optional[typing.Union["CfnResourceCollection.CloudFormationCollectionFilterProperty", _IResolvable_a771d0ef]]:
            '''Information about AWS CloudFormation stacks.

            You can use up to 500 stacks to specify which AWS resources in your account to analyze. For more information, see `Stacks <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/stacks.html>`_ in the *AWS CloudFormation User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-devopsguru-resourcecollection-resourcecollectionfilter.html#cfn-devopsguru-resourcecollection-resourcecollectionfilter-cloudformation
            '''
            result = self._values.get("cloud_formation")
            return typing.cast(typing.Optional[typing.Union["CfnResourceCollection.CloudFormationCollectionFilterProperty", _IResolvable_a771d0ef]], result)

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
        jsii_type="monocdk.aws_devopsguru.CfnResourceCollection.TagCollectionProperty",
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
                from monocdk import aws_devopsguru as devopsguru
                
                tag_collection_property = devopsguru.CfnResourceCollection.TagCollectionProperty(
                    app_boundary_key="appBoundaryKey",
                    tag_values=["tagValues"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5d043840d679162311996828816928681ccdfe21a5601477831044baa1c58f76)
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
    jsii_type="monocdk.aws_devopsguru.CfnResourceCollectionProps",
    jsii_struct_bases=[],
    name_mapping={"resource_collection_filter": "resourceCollectionFilter"},
)
class CfnResourceCollectionProps:
    def __init__(
        self,
        *,
        resource_collection_filter: typing.Union[typing.Union[CfnResourceCollection.ResourceCollectionFilterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    ) -> None:
        '''Properties for defining a ``CfnResourceCollection``.

        :param resource_collection_filter: Information about a filter used to specify which AWS resources are analyzed for anomalous behavior by DevOps Guru.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-resourcecollection.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_devopsguru as devopsguru
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__60acb637b5dfb79b47738099f3f1b32e08a7c7c1c41f680b6a35c9693bc8381a)
            check_type(argname="argument resource_collection_filter", value=resource_collection_filter, expected_type=type_hints["resource_collection_filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_collection_filter": resource_collection_filter,
        }

    @builtins.property
    def resource_collection_filter(
        self,
    ) -> typing.Union[CfnResourceCollection.ResourceCollectionFilterProperty, _IResolvable_a771d0ef]:
        '''Information about a filter used to specify which AWS resources are analyzed for anomalous behavior by DevOps Guru.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-devopsguru-resourcecollection.html#cfn-devopsguru-resourcecollection-resourcecollectionfilter
        '''
        result = self._values.get("resource_collection_filter")
        assert result is not None, "Required property 'resource_collection_filter' is missing"
        return typing.cast(typing.Union[CfnResourceCollection.ResourceCollectionFilterProperty, _IResolvable_a771d0ef], result)

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

def _typecheckingstub__8bbae86d41aea0585a2eaac6a3f32b425ad2b816c314e4927e6d332ea05e0718(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    config: typing.Union[typing.Union[CfnNotificationChannel.NotificationChannelConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ea7ea5eb95d96b8eb193b06dd64026d9f9a83e37899a0ba9cddc0f3e8a5311b(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20f24c5c030821c4f9ecfe0a0bcfa9ddba48a65227d8add919d7653a31cef6b0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e84d1c63356a2e4ecaa15ce344db06ba4489b4a93d8dbccf8c07e87a7478044c(
    value: typing.Union[CfnNotificationChannel.NotificationChannelConfigProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc2e4465e46488b2716def351bbeba471b6d8a5e1a62e3e239c5b03ba7415eb8(
    *,
    filters: typing.Optional[typing.Union[typing.Union[CfnNotificationChannel.NotificationFilterConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    sns: typing.Optional[typing.Union[typing.Union[CfnNotificationChannel.SnsChannelConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eadc6342bf29b81b3c4f49e62e8640c7432ca8a1d8538b22ce4a1ab5b8a64e2(
    *,
    message_types: typing.Optional[typing.Sequence[builtins.str]] = None,
    severities: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f139d98dbcda10edbce11503dcdf35927f5e8c13cf9f8ca30f3a5f61b8632e(
    *,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__825c99d4860b79e84c4ad8c59225b5332d749b8b390f25892a772cfac4c80e57(
    *,
    config: typing.Union[typing.Union[CfnNotificationChannel.NotificationChannelConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92b566b8728cdd7da1ab03e907718915745eb33e37ea5c6f13988bfdb660976e(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    resource_collection_filter: typing.Union[typing.Union[CfnResourceCollection.ResourceCollectionFilterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0abcbd5733a8abfee13439dd6dbaa9548ae6dd3e2788abf49e50803c6c2959a4(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ed90def3e7ff6d4f509b6b23e9f918f563f3a24ec43f34c9661c4e70f7f05ab(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca9d09dd9877ebd9f704d1335fab78d85e95cf71aaa96cd16d95118e4fb2f384(
    value: typing.Union[CfnResourceCollection.ResourceCollectionFilterProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2fd64417a4fd2babbce47418aede0e3f2a208489de9d718f2be06d1e73c8109(
    *,
    stack_names: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ce2195a03e357ce0d7eab3dcc2d79b39fad0f050b647c2fd29bb609058428d(
    *,
    cloud_formation: typing.Optional[typing.Union[typing.Union[CfnResourceCollection.CloudFormationCollectionFilterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnResourceCollection.TagCollectionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d043840d679162311996828816928681ccdfe21a5601477831044baa1c58f76(
    *,
    app_boundary_key: typing.Optional[builtins.str] = None,
    tag_values: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60acb637b5dfb79b47738099f3f1b32e08a7c7c1c41f680b6a35c9693bc8381a(
    *,
    resource_collection_filter: typing.Union[typing.Union[CfnResourceCollection.ResourceCollectionFilterProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass
