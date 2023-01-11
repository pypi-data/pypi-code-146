'''
# Amazon Simple Email Service Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

![cdk-constructs: Stable](https://img.shields.io/badge/cdk--constructs-stable-success.svg?style=for-the-badge)

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Email receiving

Create a receipt rule set with rules and actions (actions can be found in the
`@aws-cdk/aws-ses-actions` package):

```python
import aws_cdk.aws_s3 as s3
import aws_cdk.aws_ses_actions as actions


bucket = s3.Bucket(self, "Bucket")
topic = sns.Topic(self, "Topic")

ses.ReceiptRuleSet(self, "RuleSet",
    rules=[ses.ReceiptRuleOptions(
        recipients=["hello@aws.com"],
        actions=[
            actions.AddHeader(
                name="X-Special-Header",
                value="aws"
            ),
            actions.S3(
                bucket=bucket,
                object_key_prefix="emails/",
                topic=topic
            )
        ]
    ), ses.ReceiptRuleOptions(
        recipients=["aws.com"],
        actions=[
            actions.Sns(
                topic=topic
            )
        ]
    )
    ]
)
```

Alternatively, rules can be added to a rule set:

```python
rule_set = ses.ReceiptRuleSet(self, "RuleSet")

aws_rule = rule_set.add_rule("Aws",
    recipients=["aws.com"]
)
```

And actions to rules:

```python
import aws_cdk.aws_ses_actions as actions

# aws_rule: ses.ReceiptRule
# topic: sns.Topic

aws_rule.add_action(actions.Sns(
    topic=topic
))
```

When using `addRule`, the new rule is added after the last added rule unless `after` is specified.

### Drop spams

A rule to drop spam can be added by setting `dropSpam` to `true`:

```python
ses.ReceiptRuleSet(self, "RuleSet",
    drop_spam=True
)
```

This will add a rule at the top of the rule set with a Lambda action that stops processing messages that have at least one spam indicator. See [Lambda Function Examples](https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-lambda-example-functions.html).

## Receipt filter

Create a receipt filter:

```python
ses.ReceiptFilter(self, "Filter",
    ip="1.2.3.4/16"
)
```

An allow list filter is also available:

```python
ses.AllowListReceiptFilter(self, "AllowList",
    ips=["10.0.0.0/16", "1.2.3.4/16"
    ]
)
```

This will first create a block all filter and then create allow filters for the listed ip addresses.
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
import constructs as _constructs_77d1e7e8


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.AddHeaderActionConfig",
    jsii_struct_bases=[],
    name_mapping={"header_name": "headerName", "header_value": "headerValue"},
)
class AddHeaderActionConfig:
    def __init__(
        self,
        *,
        header_name: builtins.str,
        header_value: builtins.str,
    ) -> None:
        '''AddHeaderAction configuration.

        :param header_name: The name of the header that you want to add to the incoming message.
        :param header_value: The content that you want to include in the header.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            add_header_action_config = ses.AddHeaderActionConfig(
                header_name="headerName",
                header_value="headerValue"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__348a080a2f9682288c131b7b71880fef0517d3ca56a388ed41b5b2343ce2cfc3)
            check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
            check_type(argname="argument header_value", value=header_value, expected_type=type_hints["header_value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "header_name": header_name,
            "header_value": header_value,
        }

    @builtins.property
    def header_name(self) -> builtins.str:
        '''The name of the header that you want to add to the incoming message.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-addheaderaction.html#cfn-ses-receiptrule-addheaderaction-headername
        '''
        result = self._values.get("header_name")
        assert result is not None, "Required property 'header_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def header_value(self) -> builtins.str:
        '''The content that you want to include in the header.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-addheaderaction.html#cfn-ses-receiptrule-addheaderaction-headervalue
        '''
        result = self._values.get("header_value")
        assert result is not None, "Required property 'header_value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddHeaderActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AllowListReceiptFilter(
    _aws_cdk_core_f4b25747.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses.AllowListReceiptFilter",
):
    '''An allow list receipt filter.

    :exampleMetadata: infused

    Example::

        ses.AllowListReceiptFilter(self, "AllowList",
            ips=["10.0.0.0/16", "1.2.3.4/16"
            ]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        ips: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ips: A list of ip addresses or ranges to allow list.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__621fd3b2b69149194b2a6bae8af9c37eeda6172f68e30f3a366cb20b31126e25)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AllowListReceiptFilterProps(ips=ips)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.AllowListReceiptFilterProps",
    jsii_struct_bases=[],
    name_mapping={"ips": "ips"},
)
class AllowListReceiptFilterProps:
    def __init__(self, *, ips: typing.Sequence[builtins.str]) -> None:
        '''Construction properties for am AllowListReceiptFilter.

        :param ips: A list of ip addresses or ranges to allow list.

        :exampleMetadata: infused

        Example::

            ses.AllowListReceiptFilter(self, "AllowList",
                ips=["10.0.0.0/16", "1.2.3.4/16"
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cbcffdabd4f85ca883574c4195eee526fdaa455bd68055fa01abd49020e41f5)
            check_type(argname="argument ips", value=ips, expected_type=type_hints["ips"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ips": ips,
        }

    @builtins.property
    def ips(self) -> typing.List[builtins.str]:
        '''A list of ip addresses or ranges to allow list.'''
        result = self._values.get("ips")
        assert result is not None, "Required property 'ips' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AllowListReceiptFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.BounceActionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "message": "message",
        "sender": "sender",
        "smtp_reply_code": "smtpReplyCode",
        "status_code": "statusCode",
        "topic_arn": "topicArn",
    },
)
class BounceActionConfig:
    def __init__(
        self,
        *,
        message: builtins.str,
        sender: builtins.str,
        smtp_reply_code: builtins.str,
        status_code: typing.Optional[builtins.str] = None,
        topic_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''BoundAction configuration.

        :param message: Human-readable text to include in the bounce message.
        :param sender: The email address of the sender of the bounced email. This is the address that the bounce message is sent from.
        :param smtp_reply_code: The SMTP reply code, as defined by RFC 5321.
        :param status_code: The SMTP enhanced status code, as defined by RFC 3463. Default: - No status code.
        :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the bounce action is taken. Default: - No notification is sent to SNS.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            bounce_action_config = ses.BounceActionConfig(
                message="message",
                sender="sender",
                smtp_reply_code="smtpReplyCode",
            
                # the properties below are optional
                status_code="statusCode",
                topic_arn="topicArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f847dea812065f41d89ef8714a33298b916a69d8d4a316128580a5528706e36e)
            check_type(argname="argument message", value=message, expected_type=type_hints["message"])
            check_type(argname="argument sender", value=sender, expected_type=type_hints["sender"])
            check_type(argname="argument smtp_reply_code", value=smtp_reply_code, expected_type=type_hints["smtp_reply_code"])
            check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "message": message,
            "sender": sender,
            "smtp_reply_code": smtp_reply_code,
        }
        if status_code is not None:
            self._values["status_code"] = status_code
        if topic_arn is not None:
            self._values["topic_arn"] = topic_arn

    @builtins.property
    def message(self) -> builtins.str:
        '''Human-readable text to include in the bounce message.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-message
        '''
        result = self._values.get("message")
        assert result is not None, "Required property 'message' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sender(self) -> builtins.str:
        '''The email address of the sender of the bounced email.

        This is the address that the bounce message is sent from.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-sender
        '''
        result = self._values.get("sender")
        assert result is not None, "Required property 'sender' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def smtp_reply_code(self) -> builtins.str:
        '''The SMTP reply code, as defined by RFC 5321.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-smtpreplycode
        '''
        result = self._values.get("smtp_reply_code")
        assert result is not None, "Required property 'smtp_reply_code' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def status_code(self) -> typing.Optional[builtins.str]:
        '''The SMTP enhanced status code, as defined by RFC 3463.

        :default: - No status code.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-statuscode
        '''
        result = self._values.get("status_code")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the bounce action is taken.

        :default: - No notification is sent to SNS.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-topicarn
        '''
        result = self._values.get("topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BounceActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnConfigurationSet(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses.CfnConfigurationSet",
):
    '''A CloudFormation ``AWS::SES::ConfigurationSet``.

    Configuration sets let you create groups of rules that you can apply to the emails you send using Amazon SES. For more information about using configuration sets, see `Using Amazon SES Configuration Sets <https://docs.aws.amazon.com/ses/latest/dg/using-configuration-sets.html>`_ in the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/>`_ .
    .. epigraph::

       *Required permissions:*

       To apply any of the resource options, you will need to have the corresponding AWS Identity and Access Management (IAM) SES API v2 permissions:

       - ``ses:GetConfigurationSet``
       - (This permission is replacing the v1 *ses:DescribeConfigurationSet* permission which will not work with these v2 resource options.)
       - ``ses:PutConfigurationSetDeliveryOptions``
       - ``ses:PutConfigurationSetReputationOptions``
       - ``ses:PutConfigurationSetSendingOptions``
       - ``ses:PutConfigurationSetSuppressionOptions``
       - ``ses:PutConfigurationSetTrackingOptions``

    :cloudformationResource: AWS::SES::ConfigurationSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ses as ses
        
        cfn_configuration_set = ses.CfnConfigurationSet(self, "MyCfnConfigurationSet",
            delivery_options=ses.CfnConfigurationSet.DeliveryOptionsProperty(
                sending_pool_name="sendingPoolName",
                tls_policy="tlsPolicy"
            ),
            name="name",
            reputation_options=ses.CfnConfigurationSet.ReputationOptionsProperty(
                reputation_metrics_enabled=False
            ),
            sending_options=ses.CfnConfigurationSet.SendingOptionsProperty(
                sending_enabled=False
            ),
            suppression_options=ses.CfnConfigurationSet.SuppressionOptionsProperty(
                suppressed_reasons=["suppressedReasons"]
            ),
            tracking_options=ses.CfnConfigurationSet.TrackingOptionsProperty(
                custom_redirect_domain="customRedirectDomain"
            ),
            vdm_options=ses.CfnConfigurationSet.VdmOptionsProperty(
                dashboard_options=ses.CfnConfigurationSet.DashboardOptionsProperty(
                    engagement_metrics="engagementMetrics"
                ),
                guardian_options=ses.CfnConfigurationSet.GuardianOptionsProperty(
                    optimized_shared_delivery="optimizedSharedDelivery"
                )
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        delivery_options: typing.Optional[typing.Union[typing.Union["CfnConfigurationSet.DeliveryOptionsProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        reputation_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfigurationSet.ReputationOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        sending_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfigurationSet.SendingOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        suppression_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfigurationSet.SuppressionOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tracking_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfigurationSet.TrackingOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        vdm_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfigurationSet.VdmOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::SES::ConfigurationSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param delivery_options: Specifies whether messages that use the configuration set are required to use Transport Layer Security (TLS).
        :param name: The name of the configuration set. The name must meet the following requirements:. - Contain only letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-). - Contain 64 characters or fewer.
        :param reputation_options: An object that represents the reputation settings for the configuration set.
        :param sending_options: An object that defines whether or not Amazon SES can send email that you send using the configuration set.
        :param suppression_options: An object that contains information about the suppression list preferences for your account.
        :param tracking_options: The name of the custom open and click tracking domain associated with the configuration set.
        :param vdm_options: The Virtual Deliverability Manager (VDM) options that apply to the configuration set.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13bb44c4317522a7d6ce5dee4a2200eb13cf7dfccfdbfa15df9ba7d50ec75bd1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConfigurationSetProps(
            delivery_options=delivery_options,
            name=name,
            reputation_options=reputation_options,
            sending_options=sending_options,
            suppression_options=suppression_options,
            tracking_options=tracking_options,
            vdm_options=vdm_options,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63ed92a00925569033d102d0f89dd0683aa8605fca8dbbda1aa15f5c8f52e540)
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
            type_hints = typing.get_type_hints(_typecheckingstub__68f9412d7545d61e9c7a1fc0e5c70c73156f9b93bdb00b36af94a3192bb9cdc0)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="deliveryOptions")
    def delivery_options(
        self,
    ) -> typing.Optional[typing.Union["CfnConfigurationSet.DeliveryOptionsProperty", _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether messages that use the configuration set are required to use Transport Layer Security (TLS).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-deliveryoptions
        '''
        return typing.cast(typing.Optional[typing.Union["CfnConfigurationSet.DeliveryOptionsProperty", _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "deliveryOptions"))

    @delivery_options.setter
    def delivery_options(
        self,
        value: typing.Optional[typing.Union["CfnConfigurationSet.DeliveryOptionsProperty", _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef0d1934fafb466d58818e69e36e9e4b6064f66ef66048e445022da948e81ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deliveryOptions", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the configuration set. The name must meet the following requirements:.

        - Contain only letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-).
        - Contain 64 characters or fewer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49743c3fce7e5e543b82086f63966eb171b6e470ce7f6b177f2c832eb37618a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="reputationOptions")
    def reputation_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.ReputationOptionsProperty"]]:
        '''An object that represents the reputation settings for the configuration set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-reputationoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.ReputationOptionsProperty"]], jsii.get(self, "reputationOptions"))

    @reputation_options.setter
    def reputation_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.ReputationOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a79ec05d54ce608b4f0ab49d74f3f54d5f0f0ad6e916fcb7b8b0a751b9e08e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reputationOptions", value)

    @builtins.property
    @jsii.member(jsii_name="sendingOptions")
    def sending_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.SendingOptionsProperty"]]:
        '''An object that defines whether or not Amazon SES can send email that you send using the configuration set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-sendingoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.SendingOptionsProperty"]], jsii.get(self, "sendingOptions"))

    @sending_options.setter
    def sending_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.SendingOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b964b196b027647457be83679b2ee4615c64b70cbf051a0e16758c9591dcb1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sendingOptions", value)

    @builtins.property
    @jsii.member(jsii_name="suppressionOptions")
    def suppression_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.SuppressionOptionsProperty"]]:
        '''An object that contains information about the suppression list preferences for your account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-suppressionoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.SuppressionOptionsProperty"]], jsii.get(self, "suppressionOptions"))

    @suppression_options.setter
    def suppression_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.SuppressionOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49ed583322df351368c001a1b1c1270a762c297dca9b1c8c36f9f75037025a9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "suppressionOptions", value)

    @builtins.property
    @jsii.member(jsii_name="trackingOptions")
    def tracking_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.TrackingOptionsProperty"]]:
        '''The name of the custom open and click tracking domain associated with the configuration set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-trackingoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.TrackingOptionsProperty"]], jsii.get(self, "trackingOptions"))

    @tracking_options.setter
    def tracking_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.TrackingOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43461cc53c702a41eb4d9ef79ad4df5865d056628bea9fbb9c617d1252a38f2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trackingOptions", value)

    @builtins.property
    @jsii.member(jsii_name="vdmOptions")
    def vdm_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.VdmOptionsProperty"]]:
        '''The Virtual Deliverability Manager (VDM) options that apply to the configuration set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-vdmoptions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.VdmOptionsProperty"]], jsii.get(self, "vdmOptions"))

    @vdm_options.setter
    def vdm_options(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.VdmOptionsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d104f1f3b29060fba6959555e511139222657ff331fcff77faa6c7b17ca1018)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vdmOptions", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnConfigurationSet.DashboardOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"engagement_metrics": "engagementMetrics"},
    )
    class DashboardOptionsProperty:
        def __init__(self, *, engagement_metrics: builtins.str) -> None:
            '''Settings for your VDM configuration as applicable to the Dashboard.

            :param engagement_metrics: Specifies the status of your VDM engagement metrics collection. Can be one of the following:. - ``ENABLED`` – Amazon SES enables engagement metrics for the configuration set. - ``DISABLED`` – Amazon SES disables engagement metrics for the configuration set.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-dashboardoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                dashboard_options_property = ses.CfnConfigurationSet.DashboardOptionsProperty(
                    engagement_metrics="engagementMetrics"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a4201dce85f3f4e41450d83b2ff8ccccae9d14f1be24abe8292fd1bb249cff03)
                check_type(argname="argument engagement_metrics", value=engagement_metrics, expected_type=type_hints["engagement_metrics"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "engagement_metrics": engagement_metrics,
            }

        @builtins.property
        def engagement_metrics(self) -> builtins.str:
            '''Specifies the status of your VDM engagement metrics collection. Can be one of the following:.

            - ``ENABLED`` – Amazon SES enables engagement metrics for the configuration set.
            - ``DISABLED`` – Amazon SES disables engagement metrics for the configuration set.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-dashboardoptions.html#cfn-ses-configurationset-dashboardoptions-engagementmetrics
            '''
            result = self._values.get("engagement_metrics")
            assert result is not None, "Required property 'engagement_metrics' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashboardOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnConfigurationSet.DeliveryOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "sending_pool_name": "sendingPoolName",
            "tls_policy": "tlsPolicy",
        },
    )
    class DeliveryOptionsProperty:
        def __init__(
            self,
            *,
            sending_pool_name: typing.Optional[builtins.str] = None,
            tls_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies whether messages that use the configuration set are required to use Transport Layer Security (TLS).

            :param sending_pool_name: The name of the dedicated IP pool to associate with the configuration set.
            :param tls_policy: Specifies whether messages that use the configuration set are required to use Transport Layer Security (TLS). If the value is ``REQUIRE`` , messages are only delivered if a TLS connection can be established. If the value is ``OPTIONAL`` , messages can be delivered in plain text if a TLS connection can't be established. Valid Values: ``REQUIRE | OPTIONAL``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-deliveryoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                delivery_options_property = ses.CfnConfigurationSet.DeliveryOptionsProperty(
                    sending_pool_name="sendingPoolName",
                    tls_policy="tlsPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5da9615e44a9aea922d9ae0fa9b864fc1bdfd670ef6fc69b7b8ca02893560a15)
                check_type(argname="argument sending_pool_name", value=sending_pool_name, expected_type=type_hints["sending_pool_name"])
                check_type(argname="argument tls_policy", value=tls_policy, expected_type=type_hints["tls_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sending_pool_name is not None:
                self._values["sending_pool_name"] = sending_pool_name
            if tls_policy is not None:
                self._values["tls_policy"] = tls_policy

        @builtins.property
        def sending_pool_name(self) -> typing.Optional[builtins.str]:
            '''The name of the dedicated IP pool to associate with the configuration set.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-deliveryoptions.html#cfn-ses-configurationset-deliveryoptions-sendingpoolname
            '''
            result = self._values.get("sending_pool_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def tls_policy(self) -> typing.Optional[builtins.str]:
            '''Specifies whether messages that use the configuration set are required to use Transport Layer Security (TLS).

            If the value is ``REQUIRE`` , messages are only delivered if a TLS connection can be established. If the value is ``OPTIONAL`` , messages can be delivered in plain text if a TLS connection can't be established.

            Valid Values: ``REQUIRE | OPTIONAL``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-deliveryoptions.html#cfn-ses-configurationset-deliveryoptions-tlspolicy
            '''
            result = self._values.get("tls_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeliveryOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnConfigurationSet.GuardianOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"optimized_shared_delivery": "optimizedSharedDelivery"},
    )
    class GuardianOptionsProperty:
        def __init__(self, *, optimized_shared_delivery: builtins.str) -> None:
            '''Settings for your VDM configuration as applicable to the Guardian.

            :param optimized_shared_delivery: Specifies the status of your VDM optimized shared delivery. Can be one of the following:. - ``ENABLED`` – Amazon SES enables optimized shared delivery for the configuration set. - ``DISABLED`` – Amazon SES disables optimized shared delivery for the configuration set.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-guardianoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                guardian_options_property = ses.CfnConfigurationSet.GuardianOptionsProperty(
                    optimized_shared_delivery="optimizedSharedDelivery"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f7d26d6faf60057c4d500cd3ed1bd1fbebdcca7b98cdab5484730d44796e2d2d)
                check_type(argname="argument optimized_shared_delivery", value=optimized_shared_delivery, expected_type=type_hints["optimized_shared_delivery"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "optimized_shared_delivery": optimized_shared_delivery,
            }

        @builtins.property
        def optimized_shared_delivery(self) -> builtins.str:
            '''Specifies the status of your VDM optimized shared delivery. Can be one of the following:.

            - ``ENABLED`` – Amazon SES enables optimized shared delivery for the configuration set.
            - ``DISABLED`` – Amazon SES disables optimized shared delivery for the configuration set.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-guardianoptions.html#cfn-ses-configurationset-guardianoptions-optimizedshareddelivery
            '''
            result = self._values.get("optimized_shared_delivery")
            assert result is not None, "Required property 'optimized_shared_delivery' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GuardianOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnConfigurationSet.ReputationOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"reputation_metrics_enabled": "reputationMetricsEnabled"},
    )
    class ReputationOptionsProperty:
        def __init__(
            self,
            *,
            reputation_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Contains information about the reputation settings for a configuration set.

            :param reputation_metrics_enabled: Describes whether or not Amazon SES publishes reputation metrics for the configuration set, such as bounce and complaint rates, to Amazon CloudWatch. If the value is ``true`` , reputation metrics are published. If the value is ``false`` , reputation metrics are not published. The default value is ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-reputationoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                reputation_options_property = ses.CfnConfigurationSet.ReputationOptionsProperty(
                    reputation_metrics_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fee151174424c629aa606a17d41bd5f922500b13883f167ec5d37c2fff7dec3d)
                check_type(argname="argument reputation_metrics_enabled", value=reputation_metrics_enabled, expected_type=type_hints["reputation_metrics_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if reputation_metrics_enabled is not None:
                self._values["reputation_metrics_enabled"] = reputation_metrics_enabled

        @builtins.property
        def reputation_metrics_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Describes whether or not Amazon SES publishes reputation metrics for the configuration set, such as bounce and complaint rates, to Amazon CloudWatch.

            If the value is ``true`` , reputation metrics are published. If the value is ``false`` , reputation metrics are not published. The default value is ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-reputationoptions.html#cfn-ses-configurationset-reputationoptions-reputationmetricsenabled
            '''
            result = self._values.get("reputation_metrics_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReputationOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnConfigurationSet.SendingOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"sending_enabled": "sendingEnabled"},
    )
    class SendingOptionsProperty:
        def __init__(
            self,
            *,
            sending_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Used to enable or disable email sending for messages that use this configuration set in the current AWS Region.

            :param sending_enabled: If ``true`` , email sending is enabled for the configuration set. If ``false`` , email sending is disabled for the configuration set.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-sendingoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                sending_options_property = ses.CfnConfigurationSet.SendingOptionsProperty(
                    sending_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1a5c23cb2ccbd3036c589b7bfc323dd1e87316f23cb614e0dc83fa84833acc99)
                check_type(argname="argument sending_enabled", value=sending_enabled, expected_type=type_hints["sending_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if sending_enabled is not None:
                self._values["sending_enabled"] = sending_enabled

        @builtins.property
        def sending_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''If ``true`` , email sending is enabled for the configuration set.

            If ``false`` , email sending is disabled for the configuration set.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-sendingoptions.html#cfn-ses-configurationset-sendingoptions-sendingenabled
            '''
            result = self._values.get("sending_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SendingOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnConfigurationSet.SuppressionOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"suppressed_reasons": "suppressedReasons"},
    )
    class SuppressionOptionsProperty:
        def __init__(
            self,
            *,
            suppressed_reasons: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''An object that contains information about the suppression list preferences for your account.

            :param suppressed_reasons: A list that contains the reasons that email addresses are automatically added to the suppression list for your account. This list can contain any or all of the following: - ``COMPLAINT`` – Amazon SES adds an email address to the suppression list for your account when a message sent to that address results in a complaint. - ``BOUNCE`` – Amazon SES adds an email address to the suppression list for your account when a message sent to that address results in a hard bounce.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-suppressionoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                suppression_options_property = ses.CfnConfigurationSet.SuppressionOptionsProperty(
                    suppressed_reasons=["suppressedReasons"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2ee545a15706684e2048616f818fd4b36c1b08d8f01c6c927469bde9fad70683)
                check_type(argname="argument suppressed_reasons", value=suppressed_reasons, expected_type=type_hints["suppressed_reasons"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if suppressed_reasons is not None:
                self._values["suppressed_reasons"] = suppressed_reasons

        @builtins.property
        def suppressed_reasons(self) -> typing.Optional[typing.List[builtins.str]]:
            '''A list that contains the reasons that email addresses are automatically added to the suppression list for your account.

            This list can contain any or all of the following:

            - ``COMPLAINT`` – Amazon SES adds an email address to the suppression list for your account when a message sent to that address results in a complaint.
            - ``BOUNCE`` – Amazon SES adds an email address to the suppression list for your account when a message sent to that address results in a hard bounce.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-suppressionoptions.html#cfn-ses-configurationset-suppressionoptions-suppressedreasons
            '''
            result = self._values.get("suppressed_reasons")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SuppressionOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnConfigurationSet.TrackingOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"custom_redirect_domain": "customRedirectDomain"},
    )
    class TrackingOptionsProperty:
        def __init__(
            self,
            *,
            custom_redirect_domain: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A domain that is used to redirect email recipients to an Amazon SES-operated domain.

            This domain captures open and click events generated by Amazon SES emails.

            For more information, see `Configuring Custom Domains to Handle Open and Click Tracking <https://docs.aws.amazon.com/ses/latest/dg/configure-custom-open-click-domains.html>`_ in the *Amazon SES Developer Guide* .

            :param custom_redirect_domain: The custom subdomain that is used to redirect email recipients to the Amazon SES event tracking domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-trackingoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                tracking_options_property = ses.CfnConfigurationSet.TrackingOptionsProperty(
                    custom_redirect_domain="customRedirectDomain"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6abf6e56bc382300f76ed3f7f64fdc609cad611358fb341a37f082d6dee43566)
                check_type(argname="argument custom_redirect_domain", value=custom_redirect_domain, expected_type=type_hints["custom_redirect_domain"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if custom_redirect_domain is not None:
                self._values["custom_redirect_domain"] = custom_redirect_domain

        @builtins.property
        def custom_redirect_domain(self) -> typing.Optional[builtins.str]:
            '''The custom subdomain that is used to redirect email recipients to the Amazon SES event tracking domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-trackingoptions.html#cfn-ses-configurationset-trackingoptions-customredirectdomain
            '''
            result = self._values.get("custom_redirect_domain")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrackingOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnConfigurationSet.VdmOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dashboard_options": "dashboardOptions",
            "guardian_options": "guardianOptions",
        },
    )
    class VdmOptionsProperty:
        def __init__(
            self,
            *,
            dashboard_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfigurationSet.DashboardOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            guardian_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfigurationSet.GuardianOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The Virtual Deliverability Manager (VDM) options that apply to a configuration set.

            :param dashboard_options: Settings for your VDM configuration as applicable to the Dashboard.
            :param guardian_options: Settings for your VDM configuration as applicable to the Guardian.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-vdmoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                vdm_options_property = ses.CfnConfigurationSet.VdmOptionsProperty(
                    dashboard_options=ses.CfnConfigurationSet.DashboardOptionsProperty(
                        engagement_metrics="engagementMetrics"
                    ),
                    guardian_options=ses.CfnConfigurationSet.GuardianOptionsProperty(
                        optimized_shared_delivery="optimizedSharedDelivery"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fc57adf947a48650c66bba0d0eb06fe8b1f18083936744d343fc26f217b08e11)
                check_type(argname="argument dashboard_options", value=dashboard_options, expected_type=type_hints["dashboard_options"])
                check_type(argname="argument guardian_options", value=guardian_options, expected_type=type_hints["guardian_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dashboard_options is not None:
                self._values["dashboard_options"] = dashboard_options
            if guardian_options is not None:
                self._values["guardian_options"] = guardian_options

        @builtins.property
        def dashboard_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.DashboardOptionsProperty"]]:
            '''Settings for your VDM configuration as applicable to the Dashboard.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-vdmoptions.html#cfn-ses-configurationset-vdmoptions-dashboardoptions
            '''
            result = self._values.get("dashboard_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.DashboardOptionsProperty"]], result)

        @builtins.property
        def guardian_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.GuardianOptionsProperty"]]:
            '''Settings for your VDM configuration as applicable to the Guardian.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationset-vdmoptions.html#cfn-ses-configurationset-vdmoptions-guardianoptions
            '''
            result = self._values.get("guardian_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSet.GuardianOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VdmOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnConfigurationSetEventDestination(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestination",
):
    '''A CloudFormation ``AWS::SES::ConfigurationSetEventDestination``.

    Specifies a configuration set event destination. An event destination is an AWS service that Amazon SES publishes email sending events to. When you specify an event destination, you provide one, and only one, destination. You can send event data to Amazon CloudWatch, Amazon Kinesis Data Firehose, or Amazon Simple Notification Service (Amazon SNS).

    :cloudformationResource: AWS::SES::ConfigurationSetEventDestination
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationseteventdestination.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ses as ses
        
        cfn_configuration_set_event_destination = ses.CfnConfigurationSetEventDestination(self, "MyCfnConfigurationSetEventDestination",
            configuration_set_name="configurationSetName",
            event_destination=ses.CfnConfigurationSetEventDestination.EventDestinationProperty(
                matching_event_types=["matchingEventTypes"],
        
                # the properties below are optional
                cloud_watch_destination=ses.CfnConfigurationSetEventDestination.CloudWatchDestinationProperty(
                    dimension_configurations=[ses.CfnConfigurationSetEventDestination.DimensionConfigurationProperty(
                        default_dimension_value="defaultDimensionValue",
                        dimension_name="dimensionName",
                        dimension_value_source="dimensionValueSource"
                    )]
                ),
                enabled=False,
                kinesis_firehose_destination=ses.CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty(
                    delivery_stream_arn="deliveryStreamArn",
                    iam_role_arn="iamRoleArn"
                ),
                name="name",
                sns_destination=ses.CfnConfigurationSetEventDestination.SnsDestinationProperty(
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
        configuration_set_name: builtins.str,
        event_destination: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfigurationSetEventDestination.EventDestinationProperty", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''Create a new ``AWS::SES::ConfigurationSetEventDestination``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param configuration_set_name: The name of the configuration set that contains the event destination.
        :param event_destination: The event destination object.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a49f6f5e7a15af6e2ff6c54e820b52a709f0013fadf4e0b326438252999177e8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConfigurationSetEventDestinationProps(
            configuration_set_name=configuration_set_name,
            event_destination=event_destination,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75c27f598cfff52c463542bfe637e1036c1d83c4d4b7b3ec9591610afde4bfaf)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf800f6aff4772c8e683753a8251964ddd1e4a9fcb97b025a55f8edc43f470bf)
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
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="configurationSetName")
    def configuration_set_name(self) -> builtins.str:
        '''The name of the configuration set that contains the event destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationseteventdestination.html#cfn-ses-configurationseteventdestination-configurationsetname
        '''
        return typing.cast(builtins.str, jsii.get(self, "configurationSetName"))

    @configuration_set_name.setter
    def configuration_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a4539d5fe86a724cf11a76ef829e6f6fda15da137b662ef661e0c85367b014)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationSetName", value)

    @builtins.property
    @jsii.member(jsii_name="eventDestination")
    def event_destination(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSetEventDestination.EventDestinationProperty"]:
        '''The event destination object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationseteventdestination.html#cfn-ses-configurationseteventdestination-eventdestination
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSetEventDestination.EventDestinationProperty"], jsii.get(self, "eventDestination"))

    @event_destination.setter
    def event_destination(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSetEventDestination.EventDestinationProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b4784f2ab1f3d60a68bd553763c7ce7a511fd77fad7066d5dcd37bb10f69c85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventDestination", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestination.CloudWatchDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"dimension_configurations": "dimensionConfigurations"},
    )
    class CloudWatchDestinationProperty:
        def __init__(
            self,
            *,
            dimension_configurations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfigurationSetEventDestination.DimensionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Contains information associated with an Amazon CloudWatch event destination to which email sending events are published.

            Event destinations, such as Amazon CloudWatch, are associated with configuration sets, which enable you to publish email sending events. For information about using configuration sets, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/monitor-sending-activity.html>`_ .

            :param dimension_configurations: A list of dimensions upon which to categorize your emails when you publish email sending events to Amazon CloudWatch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-cloudwatchdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                cloud_watch_destination_property = ses.CfnConfigurationSetEventDestination.CloudWatchDestinationProperty(
                    dimension_configurations=[ses.CfnConfigurationSetEventDestination.DimensionConfigurationProperty(
                        default_dimension_value="defaultDimensionValue",
                        dimension_name="dimensionName",
                        dimension_value_source="dimensionValueSource"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__780f585a1e7280214ab83b3a59f4355c9225141a917ddf40525cf5724f53ea76)
                check_type(argname="argument dimension_configurations", value=dimension_configurations, expected_type=type_hints["dimension_configurations"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dimension_configurations is not None:
                self._values["dimension_configurations"] = dimension_configurations

        @builtins.property
        def dimension_configurations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSetEventDestination.DimensionConfigurationProperty"]]]]:
            '''A list of dimensions upon which to categorize your emails when you publish email sending events to Amazon CloudWatch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-cloudwatchdestination.html#cfn-ses-configurationseteventdestination-cloudwatchdestination-dimensionconfigurations
            '''
            result = self._values.get("dimension_configurations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSetEventDestination.DimensionConfigurationProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestination.DimensionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_dimension_value": "defaultDimensionValue",
            "dimension_name": "dimensionName",
            "dimension_value_source": "dimensionValueSource",
        },
    )
    class DimensionConfigurationProperty:
        def __init__(
            self,
            *,
            default_dimension_value: builtins.str,
            dimension_name: builtins.str,
            dimension_value_source: builtins.str,
        ) -> None:
            '''Contains the dimension configuration to use when you publish email sending events to Amazon CloudWatch.

            For information about publishing email sending events to Amazon CloudWatch, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/monitor-sending-activity.html>`_ .

            :param default_dimension_value: The default value of the dimension that is published to Amazon CloudWatch if you do not provide the value of the dimension when you send an email. The default value must meet the following requirements: - Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), dashes (-), at signs (@), or periods (.). - Contain 256 characters or fewer.
            :param dimension_name: The name of an Amazon CloudWatch dimension associated with an email sending metric. The name must meet the following requirements: - Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), dashes (-), or colons (:). - Contain 256 characters or fewer.
            :param dimension_value_source: The place where Amazon SES finds the value of a dimension to publish to Amazon CloudWatch. To use the message tags that you specify using an ``X-SES-MESSAGE-TAGS`` header or a parameter to the ``SendEmail`` / ``SendRawEmail`` API, specify ``messageTag`` . To use your own email headers, specify ``emailHeader`` . To put a custom tag on any link included in your email, specify ``linkTag`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-dimensionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                dimension_configuration_property = ses.CfnConfigurationSetEventDestination.DimensionConfigurationProperty(
                    default_dimension_value="defaultDimensionValue",
                    dimension_name="dimensionName",
                    dimension_value_source="dimensionValueSource"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5ac68ff7c8ca01431429158705d6b1b9c57672959fd9ff59651fea4c6d036e09)
                check_type(argname="argument default_dimension_value", value=default_dimension_value, expected_type=type_hints["default_dimension_value"])
                check_type(argname="argument dimension_name", value=dimension_name, expected_type=type_hints["dimension_name"])
                check_type(argname="argument dimension_value_source", value=dimension_value_source, expected_type=type_hints["dimension_value_source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "default_dimension_value": default_dimension_value,
                "dimension_name": dimension_name,
                "dimension_value_source": dimension_value_source,
            }

        @builtins.property
        def default_dimension_value(self) -> builtins.str:
            '''The default value of the dimension that is published to Amazon CloudWatch if you do not provide the value of the dimension when you send an email.

            The default value must meet the following requirements:

            - Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), dashes (-), at signs (@), or periods (.).
            - Contain 256 characters or fewer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-dimensionconfiguration.html#cfn-ses-configurationseteventdestination-dimensionconfiguration-defaultdimensionvalue
            '''
            result = self._values.get("default_dimension_value")
            assert result is not None, "Required property 'default_dimension_value' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def dimension_name(self) -> builtins.str:
            '''The name of an Amazon CloudWatch dimension associated with an email sending metric.

            The name must meet the following requirements:

            - Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), dashes (-), or colons (:).
            - Contain 256 characters or fewer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-dimensionconfiguration.html#cfn-ses-configurationseteventdestination-dimensionconfiguration-dimensionname
            '''
            result = self._values.get("dimension_name")
            assert result is not None, "Required property 'dimension_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def dimension_value_source(self) -> builtins.str:
            '''The place where Amazon SES finds the value of a dimension to publish to Amazon CloudWatch.

            To use the message tags that you specify using an ``X-SES-MESSAGE-TAGS`` header or a parameter to the ``SendEmail`` / ``SendRawEmail`` API, specify ``messageTag`` . To use your own email headers, specify ``emailHeader`` . To put a custom tag on any link included in your email, specify ``linkTag`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-dimensionconfiguration.html#cfn-ses-configurationseteventdestination-dimensionconfiguration-dimensionvaluesource
            '''
            result = self._values.get("dimension_value_source")
            assert result is not None, "Required property 'dimension_value_source' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestination.EventDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "matching_event_types": "matchingEventTypes",
            "cloud_watch_destination": "cloudWatchDestination",
            "enabled": "enabled",
            "kinesis_firehose_destination": "kinesisFirehoseDestination",
            "name": "name",
            "sns_destination": "snsDestination",
        },
    )
    class EventDestinationProperty:
        def __init__(
            self,
            *,
            matching_event_types: typing.Sequence[builtins.str],
            cloud_watch_destination: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfigurationSetEventDestination.CloudWatchDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            kinesis_firehose_destination: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            name: typing.Optional[builtins.str] = None,
            sns_destination: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfigurationSetEventDestination.SnsDestinationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains information about an event destination.

            .. epigraph::

               When you create or update an event destination, you must provide one, and only one, destination. The destination can be Amazon CloudWatch, Amazon Kinesis Firehose or Amazon Simple Notification Service (Amazon SNS).

            Event destinations are associated with configuration sets, which enable you to publish email sending events to Amazon CloudWatch, Amazon Kinesis Firehose, or Amazon Simple Notification Service (Amazon SNS). For information about using configuration sets, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/monitor-sending-activity.html>`_ .

            :param matching_event_types: The type of email sending events to publish to the event destination. - ``send`` - The send request was successful and SES will attempt to deliver the message to the recipient’s mail server. (If account-level or global suppression is being used, SES will still count it as a send, but delivery is suppressed.) - ``reject`` - SES accepted the email, but determined that it contained a virus and didn’t attempt to deliver it to the recipient’s mail server. - ``bounce`` - ( *Hard bounce* ) The recipient's mail server permanently rejected the email. ( *Soft bounces* are only included when SES fails to deliver the email after retrying for a period of time.) - ``complaint`` - The email was successfully delivered to the recipient’s mail server, but the recipient marked it as spam. - ``delivery`` - SES successfully delivered the email to the recipient's mail server. - ``open`` - The recipient received the message and opened it in their email client. - ``click`` - The recipient clicked one or more links in the email. - ``renderingFailure`` - The email wasn't sent because of a template rendering issue. This event type can occur when template data is missing, or when there is a mismatch between template parameters and data. (This event type only occurs when you send email using the ```SendTemplatedEmail`` <https://docs.aws.amazon.com/ses/latest/APIReference/API_SendTemplatedEmail.html>`_ or ```SendBulkTemplatedEmail`` <https://docs.aws.amazon.com/ses/latest/APIReference/API_SendBulkTemplatedEmail.html>`_ API operations.) - ``deliveryDelay`` - The email couldn't be delivered to the recipient’s mail server because a temporary issue occurred. Delivery delays can occur, for example, when the recipient's inbox is full, or when the receiving email server experiences a transient issue. - ``subscription`` - The email was successfully delivered, but the recipient updated their subscription preferences by clicking on an *unsubscribe* link as part of your `subscription management <https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html>`_ .
            :param cloud_watch_destination: An object that contains the names, default values, and sources of the dimensions associated with an Amazon CloudWatch event destination.
            :param enabled: Sets whether Amazon SES publishes events to this destination when you send an email with the associated configuration set. Set to ``true`` to enable publishing to this destination; set to ``false`` to prevent publishing to this destination. The default value is ``false`` .
            :param kinesis_firehose_destination: An object that contains the delivery stream ARN and the IAM role ARN associated with an Amazon Kinesis Firehose event destination.
            :param name: The name of the event destination. The name must meet the following requirements:. - Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-). - Contain 64 characters or fewer.
            :param sns_destination: An object that contains the topic ARN associated with an Amazon Simple Notification Service (Amazon SNS) event destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                event_destination_property = ses.CfnConfigurationSetEventDestination.EventDestinationProperty(
                    matching_event_types=["matchingEventTypes"],
                
                    # the properties below are optional
                    cloud_watch_destination=ses.CfnConfigurationSetEventDestination.CloudWatchDestinationProperty(
                        dimension_configurations=[ses.CfnConfigurationSetEventDestination.DimensionConfigurationProperty(
                            default_dimension_value="defaultDimensionValue",
                            dimension_name="dimensionName",
                            dimension_value_source="dimensionValueSource"
                        )]
                    ),
                    enabled=False,
                    kinesis_firehose_destination=ses.CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty(
                        delivery_stream_arn="deliveryStreamArn",
                        iam_role_arn="iamRoleArn"
                    ),
                    name="name",
                    sns_destination=ses.CfnConfigurationSetEventDestination.SnsDestinationProperty(
                        topic_arn="topicArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__491d2c903338d5c9011c8332967a088e9a705bdb1595304ad304871f7ba18087)
                check_type(argname="argument matching_event_types", value=matching_event_types, expected_type=type_hints["matching_event_types"])
                check_type(argname="argument cloud_watch_destination", value=cloud_watch_destination, expected_type=type_hints["cloud_watch_destination"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument kinesis_firehose_destination", value=kinesis_firehose_destination, expected_type=type_hints["kinesis_firehose_destination"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument sns_destination", value=sns_destination, expected_type=type_hints["sns_destination"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "matching_event_types": matching_event_types,
            }
            if cloud_watch_destination is not None:
                self._values["cloud_watch_destination"] = cloud_watch_destination
            if enabled is not None:
                self._values["enabled"] = enabled
            if kinesis_firehose_destination is not None:
                self._values["kinesis_firehose_destination"] = kinesis_firehose_destination
            if name is not None:
                self._values["name"] = name
            if sns_destination is not None:
                self._values["sns_destination"] = sns_destination

        @builtins.property
        def matching_event_types(self) -> typing.List[builtins.str]:
            '''The type of email sending events to publish to the event destination.

            - ``send`` - The send request was successful and SES will attempt to deliver the message to the recipient’s mail server. (If account-level or global suppression is being used, SES will still count it as a send, but delivery is suppressed.)
            - ``reject`` - SES accepted the email, but determined that it contained a virus and didn’t attempt to deliver it to the recipient’s mail server.
            - ``bounce`` - ( *Hard bounce* ) The recipient's mail server permanently rejected the email. ( *Soft bounces* are only included when SES fails to deliver the email after retrying for a period of time.)
            - ``complaint`` - The email was successfully delivered to the recipient’s mail server, but the recipient marked it as spam.
            - ``delivery`` - SES successfully delivered the email to the recipient's mail server.
            - ``open`` - The recipient received the message and opened it in their email client.
            - ``click`` - The recipient clicked one or more links in the email.
            - ``renderingFailure`` - The email wasn't sent because of a template rendering issue. This event type can occur when template data is missing, or when there is a mismatch between template parameters and data. (This event type only occurs when you send email using the ```SendTemplatedEmail`` <https://docs.aws.amazon.com/ses/latest/APIReference/API_SendTemplatedEmail.html>`_ or ```SendBulkTemplatedEmail`` <https://docs.aws.amazon.com/ses/latest/APIReference/API_SendBulkTemplatedEmail.html>`_ API operations.)
            - ``deliveryDelay`` - The email couldn't be delivered to the recipient’s mail server because a temporary issue occurred. Delivery delays can occur, for example, when the recipient's inbox is full, or when the receiving email server experiences a transient issue.
            - ``subscription`` - The email was successfully delivered, but the recipient updated their subscription preferences by clicking on an *unsubscribe* link as part of your `subscription management <https://docs.aws.amazon.com/ses/latest/dg/sending-email-subscription-management.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-matchingeventtypes
            '''
            result = self._values.get("matching_event_types")
            assert result is not None, "Required property 'matching_event_types' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def cloud_watch_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSetEventDestination.CloudWatchDestinationProperty"]]:
            '''An object that contains the names, default values, and sources of the dimensions associated with an Amazon CloudWatch event destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-cloudwatchdestination
            '''
            result = self._values.get("cloud_watch_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSetEventDestination.CloudWatchDestinationProperty"]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Sets whether Amazon SES publishes events to this destination when you send an email with the associated configuration set.

            Set to ``true`` to enable publishing to this destination; set to ``false`` to prevent publishing to this destination. The default value is ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def kinesis_firehose_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty"]]:
            '''An object that contains the delivery stream ARN and the IAM role ARN associated with an Amazon Kinesis Firehose event destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-kinesisfirehosedestination
            '''
            result = self._values.get("kinesis_firehose_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty"]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the event destination. The name must meet the following requirements:.

            - Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-).
            - Contain 64 characters or fewer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sns_destination(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSetEventDestination.SnsDestinationProperty"]]:
            '''An object that contains the topic ARN associated with an Amazon Simple Notification Service (Amazon SNS) event destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-snsdestination
            '''
            result = self._values.get("sns_destination")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationSetEventDestination.SnsDestinationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EventDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delivery_stream_arn": "deliveryStreamArn",
            "iam_role_arn": "iamRoleArn",
        },
    )
    class KinesisFirehoseDestinationProperty:
        def __init__(
            self,
            *,
            delivery_stream_arn: builtins.str,
            iam_role_arn: builtins.str,
        ) -> None:
            '''Contains the delivery stream ARN and the IAM role ARN associated with an Amazon Kinesis Firehose event destination.

            Event destinations, such as Amazon Kinesis Firehose, are associated with configuration sets, which enable you to publish email sending events. For information about using configuration sets, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/monitor-sending-activity.html>`_ .

            :param delivery_stream_arn: The ARN of the Amazon Kinesis Firehose stream that email sending events should be published to.
            :param iam_role_arn: The ARN of the IAM role under which Amazon SES publishes email sending events to the Amazon Kinesis Firehose stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-kinesisfirehosedestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                kinesis_firehose_destination_property = ses.CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty(
                    delivery_stream_arn="deliveryStreamArn",
                    iam_role_arn="iamRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c61081ffc519bd7ddb306b39b258359d44cf4540fd9a43e46cbc9b6cb9f22171)
                check_type(argname="argument delivery_stream_arn", value=delivery_stream_arn, expected_type=type_hints["delivery_stream_arn"])
                check_type(argname="argument iam_role_arn", value=iam_role_arn, expected_type=type_hints["iam_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "delivery_stream_arn": delivery_stream_arn,
                "iam_role_arn": iam_role_arn,
            }

        @builtins.property
        def delivery_stream_arn(self) -> builtins.str:
            '''The ARN of the Amazon Kinesis Firehose stream that email sending events should be published to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-kinesisfirehosedestination.html#cfn-ses-configurationseteventdestination-kinesisfirehosedestination-deliverystreamarn
            '''
            result = self._values.get("delivery_stream_arn")
            assert result is not None, "Required property 'delivery_stream_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def iam_role_arn(self) -> builtins.str:
            '''The ARN of the IAM role under which Amazon SES publishes email sending events to the Amazon Kinesis Firehose stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-kinesisfirehosedestination.html#cfn-ses-configurationseteventdestination-kinesisfirehosedestination-iamrolearn
            '''
            result = self._values.get("iam_role_arn")
            assert result is not None, "Required property 'iam_role_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "KinesisFirehoseDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestination.SnsDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={"topic_arn": "topicArn"},
    )
    class SnsDestinationProperty:
        def __init__(self, *, topic_arn: builtins.str) -> None:
            '''Contains the topic ARN associated with an Amazon Simple Notification Service (Amazon SNS) event destination.

            Event destinations, such as Amazon SNS, are associated with configuration sets, which enable you to publish email sending events. For information about using configuration sets, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/monitor-sending-activity.html>`_ .

            :param topic_arn: The ARN of the Amazon SNS topic for email sending events. You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ Amazon SNS operation. For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-snsdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                sns_destination_property = ses.CfnConfigurationSetEventDestination.SnsDestinationProperty(
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4845e2a6ad7322cffecc37f1f2e066e3ca0641082a1573e34566115f9b75e11d)
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "topic_arn": topic_arn,
            }

        @builtins.property
        def topic_arn(self) -> builtins.str:
            '''The ARN of the Amazon SNS topic for email sending events.

            You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ Amazon SNS operation.

            For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-snsdestination.html#cfn-ses-configurationseteventdestination-snsdestination-topicarn
            '''
            result = self._values.get("topic_arn")
            assert result is not None, "Required property 'topic_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SnsDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestinationProps",
    jsii_struct_bases=[],
    name_mapping={
        "configuration_set_name": "configurationSetName",
        "event_destination": "eventDestination",
    },
)
class CfnConfigurationSetEventDestinationProps:
    def __init__(
        self,
        *,
        configuration_set_name: builtins.str,
        event_destination: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSetEventDestination.EventDestinationProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''Properties for defining a ``CfnConfigurationSetEventDestination``.

        :param configuration_set_name: The name of the configuration set that contains the event destination.
        :param event_destination: The event destination object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationseteventdestination.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            cfn_configuration_set_event_destination_props = ses.CfnConfigurationSetEventDestinationProps(
                configuration_set_name="configurationSetName",
                event_destination=ses.CfnConfigurationSetEventDestination.EventDestinationProperty(
                    matching_event_types=["matchingEventTypes"],
            
                    # the properties below are optional
                    cloud_watch_destination=ses.CfnConfigurationSetEventDestination.CloudWatchDestinationProperty(
                        dimension_configurations=[ses.CfnConfigurationSetEventDestination.DimensionConfigurationProperty(
                            default_dimension_value="defaultDimensionValue",
                            dimension_name="dimensionName",
                            dimension_value_source="dimensionValueSource"
                        )]
                    ),
                    enabled=False,
                    kinesis_firehose_destination=ses.CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty(
                        delivery_stream_arn="deliveryStreamArn",
                        iam_role_arn="iamRoleArn"
                    ),
                    name="name",
                    sns_destination=ses.CfnConfigurationSetEventDestination.SnsDestinationProperty(
                        topic_arn="topicArn"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46d5160911dad5335a3bbf8ff0d91591b2c913fd423fa5f2f4c80837d87309aa)
            check_type(argname="argument configuration_set_name", value=configuration_set_name, expected_type=type_hints["configuration_set_name"])
            check_type(argname="argument event_destination", value=event_destination, expected_type=type_hints["event_destination"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "configuration_set_name": configuration_set_name,
            "event_destination": event_destination,
        }

    @builtins.property
    def configuration_set_name(self) -> builtins.str:
        '''The name of the configuration set that contains the event destination.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationseteventdestination.html#cfn-ses-configurationseteventdestination-configurationsetname
        '''
        result = self._values.get("configuration_set_name")
        assert result is not None, "Required property 'configuration_set_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def event_destination(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSetEventDestination.EventDestinationProperty]:
        '''The event destination object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationseteventdestination.html#cfn-ses-configurationseteventdestination-eventdestination
        '''
        result = self._values.get("event_destination")
        assert result is not None, "Required property 'event_destination' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSetEventDestination.EventDestinationProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationSetEventDestinationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetProps",
    jsii_struct_bases=[],
    name_mapping={
        "delivery_options": "deliveryOptions",
        "name": "name",
        "reputation_options": "reputationOptions",
        "sending_options": "sendingOptions",
        "suppression_options": "suppressionOptions",
        "tracking_options": "trackingOptions",
        "vdm_options": "vdmOptions",
    },
)
class CfnConfigurationSetProps:
    def __init__(
        self,
        *,
        delivery_options: typing.Optional[typing.Union[typing.Union[CfnConfigurationSet.DeliveryOptionsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        name: typing.Optional[builtins.str] = None,
        reputation_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSet.ReputationOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        sending_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSet.SendingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        suppression_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSet.SuppressionOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tracking_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSet.TrackingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        vdm_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSet.VdmOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnConfigurationSet``.

        :param delivery_options: Specifies whether messages that use the configuration set are required to use Transport Layer Security (TLS).
        :param name: The name of the configuration set. The name must meet the following requirements:. - Contain only letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-). - Contain 64 characters or fewer.
        :param reputation_options: An object that represents the reputation settings for the configuration set.
        :param sending_options: An object that defines whether or not Amazon SES can send email that you send using the configuration set.
        :param suppression_options: An object that contains information about the suppression list preferences for your account.
        :param tracking_options: The name of the custom open and click tracking domain associated with the configuration set.
        :param vdm_options: The Virtual Deliverability Manager (VDM) options that apply to the configuration set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            cfn_configuration_set_props = ses.CfnConfigurationSetProps(
                delivery_options=ses.CfnConfigurationSet.DeliveryOptionsProperty(
                    sending_pool_name="sendingPoolName",
                    tls_policy="tlsPolicy"
                ),
                name="name",
                reputation_options=ses.CfnConfigurationSet.ReputationOptionsProperty(
                    reputation_metrics_enabled=False
                ),
                sending_options=ses.CfnConfigurationSet.SendingOptionsProperty(
                    sending_enabled=False
                ),
                suppression_options=ses.CfnConfigurationSet.SuppressionOptionsProperty(
                    suppressed_reasons=["suppressedReasons"]
                ),
                tracking_options=ses.CfnConfigurationSet.TrackingOptionsProperty(
                    custom_redirect_domain="customRedirectDomain"
                ),
                vdm_options=ses.CfnConfigurationSet.VdmOptionsProperty(
                    dashboard_options=ses.CfnConfigurationSet.DashboardOptionsProperty(
                        engagement_metrics="engagementMetrics"
                    ),
                    guardian_options=ses.CfnConfigurationSet.GuardianOptionsProperty(
                        optimized_shared_delivery="optimizedSharedDelivery"
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3a4c788b1b4cd57a037e5e54db330a83c2c90dda72509059ba1185e6129b18d)
            check_type(argname="argument delivery_options", value=delivery_options, expected_type=type_hints["delivery_options"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument reputation_options", value=reputation_options, expected_type=type_hints["reputation_options"])
            check_type(argname="argument sending_options", value=sending_options, expected_type=type_hints["sending_options"])
            check_type(argname="argument suppression_options", value=suppression_options, expected_type=type_hints["suppression_options"])
            check_type(argname="argument tracking_options", value=tracking_options, expected_type=type_hints["tracking_options"])
            check_type(argname="argument vdm_options", value=vdm_options, expected_type=type_hints["vdm_options"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if delivery_options is not None:
            self._values["delivery_options"] = delivery_options
        if name is not None:
            self._values["name"] = name
        if reputation_options is not None:
            self._values["reputation_options"] = reputation_options
        if sending_options is not None:
            self._values["sending_options"] = sending_options
        if suppression_options is not None:
            self._values["suppression_options"] = suppression_options
        if tracking_options is not None:
            self._values["tracking_options"] = tracking_options
        if vdm_options is not None:
            self._values["vdm_options"] = vdm_options

    @builtins.property
    def delivery_options(
        self,
    ) -> typing.Optional[typing.Union[CfnConfigurationSet.DeliveryOptionsProperty, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether messages that use the configuration set are required to use Transport Layer Security (TLS).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-deliveryoptions
        '''
        result = self._values.get("delivery_options")
        return typing.cast(typing.Optional[typing.Union[CfnConfigurationSet.DeliveryOptionsProperty, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the configuration set. The name must meet the following requirements:.

        - Contain only letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-).
        - Contain 64 characters or fewer.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def reputation_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSet.ReputationOptionsProperty]]:
        '''An object that represents the reputation settings for the configuration set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-reputationoptions
        '''
        result = self._values.get("reputation_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSet.ReputationOptionsProperty]], result)

    @builtins.property
    def sending_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSet.SendingOptionsProperty]]:
        '''An object that defines whether or not Amazon SES can send email that you send using the configuration set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-sendingoptions
        '''
        result = self._values.get("sending_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSet.SendingOptionsProperty]], result)

    @builtins.property
    def suppression_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSet.SuppressionOptionsProperty]]:
        '''An object that contains information about the suppression list preferences for your account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-suppressionoptions
        '''
        result = self._values.get("suppression_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSet.SuppressionOptionsProperty]], result)

    @builtins.property
    def tracking_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSet.TrackingOptionsProperty]]:
        '''The name of the custom open and click tracking domain associated with the configuration set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-trackingoptions
        '''
        result = self._values.get("tracking_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSet.TrackingOptionsProperty]], result)

    @builtins.property
    def vdm_options(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSet.VdmOptionsProperty]]:
        '''The Virtual Deliverability Manager (VDM) options that apply to the configuration set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-vdmoptions
        '''
        result = self._values.get("vdm_options")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSet.VdmOptionsProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnContactList(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses.CfnContactList",
):
    '''A CloudFormation ``AWS::SES::ContactList``.

    A list that contains contacts that have subscribed to a particular topic or topics.

    :cloudformationResource: AWS::SES::ContactList
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-contactlist.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ses as ses
        
        cfn_contact_list = ses.CfnContactList(self, "MyCfnContactList",
            contact_list_name="contactListName",
            description="description",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            topics=[ses.CfnContactList.TopicProperty(
                default_subscription_status="defaultSubscriptionStatus",
                display_name="displayName",
                topic_name="topicName",
        
                # the properties below are optional
                description="description"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        contact_list_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        topics: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnContactList.TopicProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::SES::ContactList``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param contact_list_name: The name of the contact list.
        :param description: A description of what the contact list is about.
        :param tags: The tags associated with a contact list.
        :param topics: An interest group, theme, or label within a list. A contact list can have multiple topics.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d41d40c7650ac85127d792fb4544c5491814b232a136ef2d4611f0e326fe2a4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnContactListProps(
            contact_list_name=contact_list_name,
            description=description,
            tags=tags,
            topics=topics,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4aeef0171480641fb2ad55c2ee030c27ae5f04ccd64bcbec193eecd02de8a36e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__61f34a97c26868e8ff0a40b8c1795deb2566ac2a8fb35011f7505b85c4bcfab5)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags associated with a contact list.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-contactlist.html#cfn-ses-contactlist-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="contactListName")
    def contact_list_name(self) -> typing.Optional[builtins.str]:
        '''The name of the contact list.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-contactlist.html#cfn-ses-contactlist-contactlistname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "contactListName"))

    @contact_list_name.setter
    def contact_list_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739da882089c70a3956a0a56974f2c6b70c22e3dc60db1f3ad1b835a6a0b2ef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactListName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of what the contact list is about.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-contactlist.html#cfn-ses-contactlist-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__787467977eb6be3f2e0d9027c3300ab4d17303343bf64aa66b7a780776fe90d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="topics")
    def topics(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnContactList.TopicProperty"]]]]:
        '''An interest group, theme, or label within a list.

        A contact list can have multiple topics.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-contactlist.html#cfn-ses-contactlist-topics
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnContactList.TopicProperty"]]]], jsii.get(self, "topics"))

    @topics.setter
    def topics(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnContactList.TopicProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88be175e59547757c7fb365d8693776a486b4dc7eeea3c04cbf5039c52d61f9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "topics", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnContactList.TopicProperty",
        jsii_struct_bases=[],
        name_mapping={
            "default_subscription_status": "defaultSubscriptionStatus",
            "display_name": "displayName",
            "topic_name": "topicName",
            "description": "description",
        },
    )
    class TopicProperty:
        def __init__(
            self,
            *,
            default_subscription_status: builtins.str,
            display_name: builtins.str,
            topic_name: builtins.str,
            description: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An interest group, theme, or label within a list.

            Lists can have multiple topics.

            :param default_subscription_status: The default subscription status to be applied to a contact if the contact has not noted their preference for subscribing to a topic.
            :param display_name: The name of the topic the contact will see.
            :param topic_name: The name of the topic.
            :param description: A description of what the topic is about, which the contact will see.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-contactlist-topic.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                topic_property = ses.CfnContactList.TopicProperty(
                    default_subscription_status="defaultSubscriptionStatus",
                    display_name="displayName",
                    topic_name="topicName",
                
                    # the properties below are optional
                    description="description"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f5f535996f8706e019992cccc74f2fa2a24f8722b6e340100c254e24e878ae81)
                check_type(argname="argument default_subscription_status", value=default_subscription_status, expected_type=type_hints["default_subscription_status"])
                check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
                check_type(argname="argument topic_name", value=topic_name, expected_type=type_hints["topic_name"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "default_subscription_status": default_subscription_status,
                "display_name": display_name,
                "topic_name": topic_name,
            }
            if description is not None:
                self._values["description"] = description

        @builtins.property
        def default_subscription_status(self) -> builtins.str:
            '''The default subscription status to be applied to a contact if the contact has not noted their preference for subscribing to a topic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-contactlist-topic.html#cfn-ses-contactlist-topic-defaultsubscriptionstatus
            '''
            result = self._values.get("default_subscription_status")
            assert result is not None, "Required property 'default_subscription_status' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def display_name(self) -> builtins.str:
            '''The name of the topic the contact will see.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-contactlist-topic.html#cfn-ses-contactlist-topic-displayname
            '''
            result = self._values.get("display_name")
            assert result is not None, "Required property 'display_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def topic_name(self) -> builtins.str:
            '''The name of the topic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-contactlist-topic.html#cfn-ses-contactlist-topic-topicname
            '''
            result = self._values.get("topic_name")
            assert result is not None, "Required property 'topic_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of what the topic is about, which the contact will see.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-contactlist-topic.html#cfn-ses-contactlist-topic-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TopicProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.CfnContactListProps",
    jsii_struct_bases=[],
    name_mapping={
        "contact_list_name": "contactListName",
        "description": "description",
        "tags": "tags",
        "topics": "topics",
    },
)
class CfnContactListProps:
    def __init__(
        self,
        *,
        contact_list_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        topics: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnContactList.TopicProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnContactList``.

        :param contact_list_name: The name of the contact list.
        :param description: A description of what the contact list is about.
        :param tags: The tags associated with a contact list.
        :param topics: An interest group, theme, or label within a list. A contact list can have multiple topics.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-contactlist.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            cfn_contact_list_props = ses.CfnContactListProps(
                contact_list_name="contactListName",
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                topics=[ses.CfnContactList.TopicProperty(
                    default_subscription_status="defaultSubscriptionStatus",
                    display_name="displayName",
                    topic_name="topicName",
            
                    # the properties below are optional
                    description="description"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0798ff904789fade03f62047b94c93c4052247f33073f39e2b52b964e35a0fd2)
            check_type(argname="argument contact_list_name", value=contact_list_name, expected_type=type_hints["contact_list_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument topics", value=topics, expected_type=type_hints["topics"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if contact_list_name is not None:
            self._values["contact_list_name"] = contact_list_name
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags
        if topics is not None:
            self._values["topics"] = topics

    @builtins.property
    def contact_list_name(self) -> typing.Optional[builtins.str]:
        '''The name of the contact list.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-contactlist.html#cfn-ses-contactlist-contactlistname
        '''
        result = self._values.get("contact_list_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of what the contact list is about.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-contactlist.html#cfn-ses-contactlist-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags associated with a contact list.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-contactlist.html#cfn-ses-contactlist-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def topics(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnContactList.TopicProperty]]]]:
        '''An interest group, theme, or label within a list.

        A contact list can have multiple topics.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-contactlist.html#cfn-ses-contactlist-topics
        '''
        result = self._values.get("topics")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnContactList.TopicProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnContactListProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDedicatedIpPool(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses.CfnDedicatedIpPool",
):
    '''A CloudFormation ``AWS::SES::DedicatedIpPool``.

    Create a new pool of dedicated IP addresses. A pool can include one or more dedicated IP addresses that are associated with your AWS account . You can associate a pool with a configuration set. When you send an email that uses that configuration set, the message is sent from one of the addresses in the associated pool.
    .. epigraph::

       You can't delete dedicated IP pools that have a ``STANDARD`` scaling mode and one or more dedicated IP addresses. This constraint doesn't apply to dedicated IP pools that have a ``MANAGED`` scaling mode.

    :cloudformationResource: AWS::SES::DedicatedIpPool
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-dedicatedippool.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ses as ses
        
        cfn_dedicated_ip_pool = ses.CfnDedicatedIpPool(self, "MyCfnDedicatedIpPool",
            pool_name="poolName",
            scaling_mode="scalingMode"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        pool_name: typing.Optional[builtins.str] = None,
        scaling_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::SES::DedicatedIpPool``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param pool_name: The name of the dedicated IP pool that the IP address is associated with.
        :param scaling_mode: The type of scaling mode. The following options are available: - ``STANDARD`` - The customer controls which IPs are part of the dedicated IP pool. - ``MANAGED`` - The reputation and number of IPs is automatically managed by Amazon SES . The ``STANDARD`` option is selected by default if no value is specified.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01af3bfed322607c1c6648ea9f2d2b04e87efd5e451c84e9e5f60736f25d0547)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDedicatedIpPoolProps(pool_name=pool_name, scaling_mode=scaling_mode)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45cd6570bc5b3254cdb9efd25822e51284336d1e1b926b5dbb4d56816c471112)
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
            type_hints = typing.get_type_hints(_typecheckingstub__720ab9d7a5ca4c5272c5b8c1d2022ddf71a5032e9cb40f6eff12cf520938be5c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="poolName")
    def pool_name(self) -> typing.Optional[builtins.str]:
        '''The name of the dedicated IP pool that the IP address is associated with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-dedicatedippool.html#cfn-ses-dedicatedippool-poolname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "poolName"))

    @pool_name.setter
    def pool_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09abfb4bce0f3ed5afdb8a3da3d7cbb23048256da78540f62d19b6c8581d005a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "poolName", value)

    @builtins.property
    @jsii.member(jsii_name="scalingMode")
    def scaling_mode(self) -> typing.Optional[builtins.str]:
        '''The type of scaling mode.

        The following options are available:

        - ``STANDARD`` - The customer controls which IPs are part of the dedicated IP pool.
        - ``MANAGED`` - The reputation and number of IPs is automatically managed by Amazon SES .

        The ``STANDARD`` option is selected by default if no value is specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-dedicatedippool.html#cfn-ses-dedicatedippool-scalingmode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "scalingMode"))

    @scaling_mode.setter
    def scaling_mode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc232e0d76a02e680328b8a52c42d03a442cdf0ac60808542f4dee66a6265a79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scalingMode", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.CfnDedicatedIpPoolProps",
    jsii_struct_bases=[],
    name_mapping={"pool_name": "poolName", "scaling_mode": "scalingMode"},
)
class CfnDedicatedIpPoolProps:
    def __init__(
        self,
        *,
        pool_name: typing.Optional[builtins.str] = None,
        scaling_mode: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnDedicatedIpPool``.

        :param pool_name: The name of the dedicated IP pool that the IP address is associated with.
        :param scaling_mode: The type of scaling mode. The following options are available: - ``STANDARD`` - The customer controls which IPs are part of the dedicated IP pool. - ``MANAGED`` - The reputation and number of IPs is automatically managed by Amazon SES . The ``STANDARD`` option is selected by default if no value is specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-dedicatedippool.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            cfn_dedicated_ip_pool_props = ses.CfnDedicatedIpPoolProps(
                pool_name="poolName",
                scaling_mode="scalingMode"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__520d61be5c4902b43b0e1ead0425bcca3b6e7db1618de509d22353689b058f63)
            check_type(argname="argument pool_name", value=pool_name, expected_type=type_hints["pool_name"])
            check_type(argname="argument scaling_mode", value=scaling_mode, expected_type=type_hints["scaling_mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if pool_name is not None:
            self._values["pool_name"] = pool_name
        if scaling_mode is not None:
            self._values["scaling_mode"] = scaling_mode

    @builtins.property
    def pool_name(self) -> typing.Optional[builtins.str]:
        '''The name of the dedicated IP pool that the IP address is associated with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-dedicatedippool.html#cfn-ses-dedicatedippool-poolname
        '''
        result = self._values.get("pool_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scaling_mode(self) -> typing.Optional[builtins.str]:
        '''The type of scaling mode.

        The following options are available:

        - ``STANDARD`` - The customer controls which IPs are part of the dedicated IP pool.
        - ``MANAGED`` - The reputation and number of IPs is automatically managed by Amazon SES .

        The ``STANDARD`` option is selected by default if no value is specified.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-dedicatedippool.html#cfn-ses-dedicatedippool-scalingmode
        '''
        result = self._values.get("scaling_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDedicatedIpPoolProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnEmailIdentity(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses.CfnEmailIdentity",
):
    '''A CloudFormation ``AWS::SES::EmailIdentity``.

    Specifies an identity for using within SES. An identity is an email address or domain that you use when you send email. Before you can use an identity to send email, you first have to verify it. By verifying an identity, you demonstrate that you're the owner of the identity, and that you've given Amazon SES API v2 permission to send email from the identity.

    When you verify an email address, SES sends an email to the address. Your email address is verified as soon as you follow the link in the verification email. When you verify a domain without specifying the DkimSigningAttributes properties, OR only the NextSigningKeyLength property of DkimSigningAttributes, this resource provides a set of CNAME token names and values (DkimDNSTokenName1, DkimDNSTokenValue1, DkimDNSTokenName2, DkimDNSTokenValue2, DkimDNSTokenName3, DkimDNSTokenValue3) as outputs. You can then add these to the DNS configuration for your domain. Your domain is verified when Amazon SES detects these records in the DNS configuration for your domain. This verification method is known as Easy DKIM.

    Alternatively, you can perform the verification process by providing your own public-private key pair. This verification method is known as Bring Your Own DKIM (BYODKIM). To use BYODKIM, your resource must include DkimSigningAttributes properties DomainSigningSelector and DomainSigningPrivateKey. When you specify this object, you provide a selector (DomainSigningSelector) (a component of the DNS record name that identifies the public key to use for DKIM authentication) and a private key (DomainSigningPrivateKey).

    Additionally, you can associate an existing configuration set with the email identity that you're verifying.

    :cloudformationResource: AWS::SES::EmailIdentity
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ses as ses
        
        cfn_email_identity = ses.CfnEmailIdentity(self, "MyCfnEmailIdentity",
            email_identity="emailIdentity",
        
            # the properties below are optional
            configuration_set_attributes=ses.CfnEmailIdentity.ConfigurationSetAttributesProperty(
                configuration_set_name="configurationSetName"
            ),
            dkim_attributes=ses.CfnEmailIdentity.DkimAttributesProperty(
                signing_enabled=False
            ),
            dkim_signing_attributes=ses.CfnEmailIdentity.DkimSigningAttributesProperty(
                domain_signing_private_key="domainSigningPrivateKey",
                domain_signing_selector="domainSigningSelector",
                next_signing_key_length="nextSigningKeyLength"
            ),
            feedback_attributes=ses.CfnEmailIdentity.FeedbackAttributesProperty(
                email_forwarding_enabled=False
            ),
            mail_from_attributes=ses.CfnEmailIdentity.MailFromAttributesProperty(
                behavior_on_mx_failure="behaviorOnMxFailure",
                mail_from_domain="mailFromDomain"
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        email_identity: builtins.str,
        configuration_set_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEmailIdentity.ConfigurationSetAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        dkim_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEmailIdentity.DkimAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        dkim_signing_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEmailIdentity.DkimSigningAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        feedback_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEmailIdentity.FeedbackAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        mail_from_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEmailIdentity.MailFromAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::SES::EmailIdentity``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param email_identity: The email address or domain to verify.
        :param configuration_set_attributes: Used to associate a configuration set with an email identity.
        :param dkim_attributes: An object that contains information about the DKIM attributes for the identity.
        :param dkim_signing_attributes: If your request includes this object, Amazon SES configures the identity to use Bring Your Own DKIM (BYODKIM) for DKIM authentication purposes, or, configures the key length to be used for `Easy DKIM <https://docs.aws.amazon.com/ses/latest/dg/send-email-authentication-dkim-easy.html>`_ .
        :param feedback_attributes: Used to enable or disable feedback forwarding for an identity.
        :param mail_from_attributes: Used to enable or disable the custom Mail-From domain configuration for an email identity.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92fb9f941d507a6aaad3a1156f5369cccc785c22e6001b3af9d8fc6ff5196774)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEmailIdentityProps(
            email_identity=email_identity,
            configuration_set_attributes=configuration_set_attributes,
            dkim_attributes=dkim_attributes,
            dkim_signing_attributes=dkim_signing_attributes,
            feedback_attributes=feedback_attributes,
            mail_from_attributes=mail_from_attributes,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07e34ed2ae4e3aeaba51c9ca9d43061a0be5a74a33c984a6b1a869b16c90acb0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d436f9ed4a6719e0c9d1f60877b7035a85ea0ba0ee5c11327829227b6f0d5dba)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDkimDnsTokenName1")
    def attr_dkim_dns_token_name1(self) -> builtins.str:
        '''The host name for the first token that you have to add to the DNS configuration for your domain.

        :cloudformationAttribute: DkimDNSTokenName1
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDkimDnsTokenName1"))

    @builtins.property
    @jsii.member(jsii_name="attrDkimDnsTokenName2")
    def attr_dkim_dns_token_name2(self) -> builtins.str:
        '''The host name for the second token that you have to add to the DNS configuration for your domain.

        :cloudformationAttribute: DkimDNSTokenName2
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDkimDnsTokenName2"))

    @builtins.property
    @jsii.member(jsii_name="attrDkimDnsTokenName3")
    def attr_dkim_dns_token_name3(self) -> builtins.str:
        '''The host name for the third token that you have to add to the DNS configuration for your domain.

        :cloudformationAttribute: DkimDNSTokenName3
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDkimDnsTokenName3"))

    @builtins.property
    @jsii.member(jsii_name="attrDkimDnsTokenValue1")
    def attr_dkim_dns_token_value1(self) -> builtins.str:
        '''The record value for the first token that you have to add to the DNS configuration for your domain.

        :cloudformationAttribute: DkimDNSTokenValue1
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDkimDnsTokenValue1"))

    @builtins.property
    @jsii.member(jsii_name="attrDkimDnsTokenValue2")
    def attr_dkim_dns_token_value2(self) -> builtins.str:
        '''The record value for the second token that you have to add to the DNS configuration for your domain.

        :cloudformationAttribute: DkimDNSTokenValue2
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDkimDnsTokenValue2"))

    @builtins.property
    @jsii.member(jsii_name="attrDkimDnsTokenValue3")
    def attr_dkim_dns_token_value3(self) -> builtins.str:
        '''The record value for the third token that you have to add to the DNS configuration for your domain.

        :cloudformationAttribute: DkimDNSTokenValue3
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDkimDnsTokenValue3"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="emailIdentity")
    def email_identity(self) -> builtins.str:
        '''The email address or domain to verify.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-emailidentity
        '''
        return typing.cast(builtins.str, jsii.get(self, "emailIdentity"))

    @email_identity.setter
    def email_identity(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56c426b12a9bce7afd8cabc2804d134f62f4352e3fce2b14ee81daa0b4ad73f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "emailIdentity", value)

    @builtins.property
    @jsii.member(jsii_name="configurationSetAttributes")
    def configuration_set_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEmailIdentity.ConfigurationSetAttributesProperty"]]:
        '''Used to associate a configuration set with an email identity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-configurationsetattributes
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEmailIdentity.ConfigurationSetAttributesProperty"]], jsii.get(self, "configurationSetAttributes"))

    @configuration_set_attributes.setter
    def configuration_set_attributes(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEmailIdentity.ConfigurationSetAttributesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f961ad3e66f2f73a6f436a2db83842b86857257439c62f2e515810a0756cb9bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationSetAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="dkimAttributes")
    def dkim_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEmailIdentity.DkimAttributesProperty"]]:
        '''An object that contains information about the DKIM attributes for the identity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-dkimattributes
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEmailIdentity.DkimAttributesProperty"]], jsii.get(self, "dkimAttributes"))

    @dkim_attributes.setter
    def dkim_attributes(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEmailIdentity.DkimAttributesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5b6c1d1905bf652627534f1e2e5fad5f23df15c8766e388ab3642403e37bb8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dkimAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="dkimSigningAttributes")
    def dkim_signing_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEmailIdentity.DkimSigningAttributesProperty"]]:
        '''If your request includes this object, Amazon SES configures the identity to use Bring Your Own DKIM (BYODKIM) for DKIM authentication purposes, or, configures the key length to be used for `Easy DKIM <https://docs.aws.amazon.com/ses/latest/dg/send-email-authentication-dkim-easy.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-dkimsigningattributes
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEmailIdentity.DkimSigningAttributesProperty"]], jsii.get(self, "dkimSigningAttributes"))

    @dkim_signing_attributes.setter
    def dkim_signing_attributes(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEmailIdentity.DkimSigningAttributesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf37d00117a480dcbb019c54de9fb105bf3131b66dc129b250c74a6f8fd48e6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dkimSigningAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="feedbackAttributes")
    def feedback_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEmailIdentity.FeedbackAttributesProperty"]]:
        '''Used to enable or disable feedback forwarding for an identity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-feedbackattributes
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEmailIdentity.FeedbackAttributesProperty"]], jsii.get(self, "feedbackAttributes"))

    @feedback_attributes.setter
    def feedback_attributes(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEmailIdentity.FeedbackAttributesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a10e564656a1b907c1a252e0d6d9f7edacc7e6fd08c33e149793438ebd700b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "feedbackAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="mailFromAttributes")
    def mail_from_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEmailIdentity.MailFromAttributesProperty"]]:
        '''Used to enable or disable the custom Mail-From domain configuration for an email identity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-mailfromattributes
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEmailIdentity.MailFromAttributesProperty"]], jsii.get(self, "mailFromAttributes"))

    @mail_from_attributes.setter
    def mail_from_attributes(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEmailIdentity.MailFromAttributesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee019766d081441b8f5888505a746be1db3301c73f5dd14054ec7af5e15f035)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mailFromAttributes", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnEmailIdentity.ConfigurationSetAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"configuration_set_name": "configurationSetName"},
    )
    class ConfigurationSetAttributesProperty:
        def __init__(
            self,
            *,
            configuration_set_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Used to associate a configuration set with an email identity.

            :param configuration_set_name: The configuration set to associate with an email identity.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-configurationsetattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                configuration_set_attributes_property = ses.CfnEmailIdentity.ConfigurationSetAttributesProperty(
                    configuration_set_name="configurationSetName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__de468812f19ffde625b8ed88668e2896b995244823d7f3eb37d31f6942e593ce)
                check_type(argname="argument configuration_set_name", value=configuration_set_name, expected_type=type_hints["configuration_set_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if configuration_set_name is not None:
                self._values["configuration_set_name"] = configuration_set_name

        @builtins.property
        def configuration_set_name(self) -> typing.Optional[builtins.str]:
            '''The configuration set to associate with an email identity.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-configurationsetattributes.html#cfn-ses-emailidentity-configurationsetattributes-configurationsetname
            '''
            result = self._values.get("configuration_set_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationSetAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnEmailIdentity.DkimAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"signing_enabled": "signingEnabled"},
    )
    class DkimAttributesProperty:
        def __init__(
            self,
            *,
            signing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Used to enable or disable DKIM authentication for an email identity.

            :param signing_enabled: Sets the DKIM signing configuration for the identity. When you set this value ``true`` , then the messages that are sent from the identity are signed using DKIM. If you set this value to ``false`` , your messages are sent without DKIM signing.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-dkimattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                dkim_attributes_property = ses.CfnEmailIdentity.DkimAttributesProperty(
                    signing_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8e365aa286b283628ffbc4b67d87160115af4aff1375faf68282e7bab4b60f6b)
                check_type(argname="argument signing_enabled", value=signing_enabled, expected_type=type_hints["signing_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if signing_enabled is not None:
                self._values["signing_enabled"] = signing_enabled

        @builtins.property
        def signing_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Sets the DKIM signing configuration for the identity.

            When you set this value ``true`` , then the messages that are sent from the identity are signed using DKIM. If you set this value to ``false`` , your messages are sent without DKIM signing.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-dkimattributes.html#cfn-ses-emailidentity-dkimattributes-signingenabled
            '''
            result = self._values.get("signing_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DkimAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnEmailIdentity.DkimSigningAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "domain_signing_private_key": "domainSigningPrivateKey",
            "domain_signing_selector": "domainSigningSelector",
            "next_signing_key_length": "nextSigningKeyLength",
        },
    )
    class DkimSigningAttributesProperty:
        def __init__(
            self,
            *,
            domain_signing_private_key: typing.Optional[builtins.str] = None,
            domain_signing_selector: typing.Optional[builtins.str] = None,
            next_signing_key_length: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Used to configure or change the DKIM authentication settings for an email domain identity.

            You can use this operation to do any of the following:

            - Update the signing attributes for an identity that uses Bring Your Own DKIM (BYODKIM).
            - Update the key length that should be used for Easy DKIM.
            - Change from using no DKIM authentication to using Easy DKIM.
            - Change from using no DKIM authentication to using BYODKIM.
            - Change from using Easy DKIM to using BYODKIM.
            - Change from using BYODKIM to using Easy DKIM.

            :param domain_signing_private_key: [Bring Your Own DKIM] A private key that's used to generate a DKIM signature. The private key must use 1024 or 2048-bit RSA encryption, and must be encoded using base64 encoding. .. epigraph:: Rather than embedding sensitive information directly in your CFN templates, we recommend you use dynamic parameters in the stack template to reference sensitive information that is stored and managed outside of CFN, such as in the AWS Systems Manager Parameter Store or AWS Secrets Manager. For more information, see the `Do not embed credentials in your templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html#creds>`_ best practice.
            :param domain_signing_selector: [Bring Your Own DKIM] A string that's used to identify a public key in the DNS configuration for a domain.
            :param next_signing_key_length: [Easy DKIM] The key length of the future DKIM key pair to be generated. This can be changed at most once per day. Valid Values: ``RSA_1024_BIT | RSA_2048_BIT``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-dkimsigningattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                dkim_signing_attributes_property = ses.CfnEmailIdentity.DkimSigningAttributesProperty(
                    domain_signing_private_key="domainSigningPrivateKey",
                    domain_signing_selector="domainSigningSelector",
                    next_signing_key_length="nextSigningKeyLength"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1d1a313fff0747a5e39535795a8149a34edcefde533d0a34fa6a0747b71c81dd)
                check_type(argname="argument domain_signing_private_key", value=domain_signing_private_key, expected_type=type_hints["domain_signing_private_key"])
                check_type(argname="argument domain_signing_selector", value=domain_signing_selector, expected_type=type_hints["domain_signing_selector"])
                check_type(argname="argument next_signing_key_length", value=next_signing_key_length, expected_type=type_hints["next_signing_key_length"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_signing_private_key is not None:
                self._values["domain_signing_private_key"] = domain_signing_private_key
            if domain_signing_selector is not None:
                self._values["domain_signing_selector"] = domain_signing_selector
            if next_signing_key_length is not None:
                self._values["next_signing_key_length"] = next_signing_key_length

        @builtins.property
        def domain_signing_private_key(self) -> typing.Optional[builtins.str]:
            '''[Bring Your Own DKIM] A private key that's used to generate a DKIM signature.

            The private key must use 1024 or 2048-bit RSA encryption, and must be encoded using base64 encoding.
            .. epigraph::

               Rather than embedding sensitive information directly in your CFN templates, we recommend you use dynamic parameters in the stack template to reference sensitive information that is stored and managed outside of CFN, such as in the AWS Systems Manager Parameter Store or AWS Secrets Manager.

               For more information, see the `Do not embed credentials in your templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/best-practices.html#creds>`_ best practice.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-dkimsigningattributes.html#cfn-ses-emailidentity-dkimsigningattributes-domainsigningprivatekey
            '''
            result = self._values.get("domain_signing_private_key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def domain_signing_selector(self) -> typing.Optional[builtins.str]:
            '''[Bring Your Own DKIM] A string that's used to identify a public key in the DNS configuration for a domain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-dkimsigningattributes.html#cfn-ses-emailidentity-dkimsigningattributes-domainsigningselector
            '''
            result = self._values.get("domain_signing_selector")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def next_signing_key_length(self) -> typing.Optional[builtins.str]:
            '''[Easy DKIM] The key length of the future DKIM key pair to be generated.

            This can be changed at most once per day.

            Valid Values: ``RSA_1024_BIT | RSA_2048_BIT``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-dkimsigningattributes.html#cfn-ses-emailidentity-dkimsigningattributes-nextsigningkeylength
            '''
            result = self._values.get("next_signing_key_length")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DkimSigningAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnEmailIdentity.FeedbackAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"email_forwarding_enabled": "emailForwardingEnabled"},
    )
    class FeedbackAttributesProperty:
        def __init__(
            self,
            *,
            email_forwarding_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Used to enable or disable feedback forwarding for an identity.

            This setting determines what happens when an identity is used to send an email that results in a bounce or complaint event.

            :param email_forwarding_enabled: Sets the feedback forwarding configuration for the identity. If the value is ``true`` , you receive email notifications when bounce or complaint events occur. These notifications are sent to the address that you specified in the ``Return-Path`` header of the original email. You're required to have a method of tracking bounces and complaints. If you haven't set up another mechanism for receiving bounce or complaint notifications (for example, by setting up an event destination), you receive an email notification when these events occur (even if this setting is disabled).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-feedbackattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                feedback_attributes_property = ses.CfnEmailIdentity.FeedbackAttributesProperty(
                    email_forwarding_enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__415a5e5714e4c7499571025e863f54b06d548076362600b1ccdb46d327495647)
                check_type(argname="argument email_forwarding_enabled", value=email_forwarding_enabled, expected_type=type_hints["email_forwarding_enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email_forwarding_enabled is not None:
                self._values["email_forwarding_enabled"] = email_forwarding_enabled

        @builtins.property
        def email_forwarding_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Sets the feedback forwarding configuration for the identity.

            If the value is ``true`` , you receive email notifications when bounce or complaint events occur. These notifications are sent to the address that you specified in the ``Return-Path`` header of the original email.

            You're required to have a method of tracking bounces and complaints. If you haven't set up another mechanism for receiving bounce or complaint notifications (for example, by setting up an event destination), you receive an email notification when these events occur (even if this setting is disabled).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-feedbackattributes.html#cfn-ses-emailidentity-feedbackattributes-emailforwardingenabled
            '''
            result = self._values.get("email_forwarding_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FeedbackAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnEmailIdentity.MailFromAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "behavior_on_mx_failure": "behaviorOnMxFailure",
            "mail_from_domain": "mailFromDomain",
        },
    )
    class MailFromAttributesProperty:
        def __init__(
            self,
            *,
            behavior_on_mx_failure: typing.Optional[builtins.str] = None,
            mail_from_domain: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Used to enable or disable the custom Mail-From domain configuration for an email identity.

            :param behavior_on_mx_failure: The action to take if the required MX record isn't found when you send an email. When you set this value to ``USE_DEFAULT_VALUE`` , the mail is sent using *amazonses.com* as the MAIL FROM domain. When you set this value to ``REJECT_MESSAGE`` , the Amazon SES API v2 returns a ``MailFromDomainNotVerified`` error, and doesn't attempt to deliver the email. These behaviors are taken when the custom MAIL FROM domain configuration is in the ``Pending`` , ``Failed`` , and ``TemporaryFailure`` states. Valid Values: ``USE_DEFAULT_VALUE | REJECT_MESSAGE``
            :param mail_from_domain: The custom MAIL FROM domain that you want the verified identity to use. The MAIL FROM domain must meet the following criteria: - It has to be a subdomain of the verified identity. - It can't be used to receive email. - It can't be used in a "From" address if the MAIL FROM domain is a destination for feedback forwarding emails.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-mailfromattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                mail_from_attributes_property = ses.CfnEmailIdentity.MailFromAttributesProperty(
                    behavior_on_mx_failure="behaviorOnMxFailure",
                    mail_from_domain="mailFromDomain"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__04c1b2dc7466a7a1c93c65f19c736343d00f475535c09c4245b43bb21d05eeb7)
                check_type(argname="argument behavior_on_mx_failure", value=behavior_on_mx_failure, expected_type=type_hints["behavior_on_mx_failure"])
                check_type(argname="argument mail_from_domain", value=mail_from_domain, expected_type=type_hints["mail_from_domain"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if behavior_on_mx_failure is not None:
                self._values["behavior_on_mx_failure"] = behavior_on_mx_failure
            if mail_from_domain is not None:
                self._values["mail_from_domain"] = mail_from_domain

        @builtins.property
        def behavior_on_mx_failure(self) -> typing.Optional[builtins.str]:
            '''The action to take if the required MX record isn't found when you send an email.

            When you set this value to ``USE_DEFAULT_VALUE`` , the mail is sent using *amazonses.com* as the MAIL FROM domain. When you set this value to ``REJECT_MESSAGE`` , the Amazon SES API v2 returns a ``MailFromDomainNotVerified`` error, and doesn't attempt to deliver the email.

            These behaviors are taken when the custom MAIL FROM domain configuration is in the ``Pending`` , ``Failed`` , and ``TemporaryFailure`` states.

            Valid Values: ``USE_DEFAULT_VALUE | REJECT_MESSAGE``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-mailfromattributes.html#cfn-ses-emailidentity-mailfromattributes-behavioronmxfailure
            '''
            result = self._values.get("behavior_on_mx_failure")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def mail_from_domain(self) -> typing.Optional[builtins.str]:
            '''The custom MAIL FROM domain that you want the verified identity to use.

            The MAIL FROM domain must meet the following criteria:

            - It has to be a subdomain of the verified identity.
            - It can't be used to receive email.
            - It can't be used in a "From" address if the MAIL FROM domain is a destination for feedback forwarding emails.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-emailidentity-mailfromattributes.html#cfn-ses-emailidentity-mailfromattributes-mailfromdomain
            '''
            result = self._values.get("mail_from_domain")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MailFromAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.CfnEmailIdentityProps",
    jsii_struct_bases=[],
    name_mapping={
        "email_identity": "emailIdentity",
        "configuration_set_attributes": "configurationSetAttributes",
        "dkim_attributes": "dkimAttributes",
        "dkim_signing_attributes": "dkimSigningAttributes",
        "feedback_attributes": "feedbackAttributes",
        "mail_from_attributes": "mailFromAttributes",
    },
)
class CfnEmailIdentityProps:
    def __init__(
        self,
        *,
        email_identity: builtins.str,
        configuration_set_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEmailIdentity.ConfigurationSetAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        dkim_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEmailIdentity.DkimAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        dkim_signing_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEmailIdentity.DkimSigningAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        feedback_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEmailIdentity.FeedbackAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        mail_from_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEmailIdentity.MailFromAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnEmailIdentity``.

        :param email_identity: The email address or domain to verify.
        :param configuration_set_attributes: Used to associate a configuration set with an email identity.
        :param dkim_attributes: An object that contains information about the DKIM attributes for the identity.
        :param dkim_signing_attributes: If your request includes this object, Amazon SES configures the identity to use Bring Your Own DKIM (BYODKIM) for DKIM authentication purposes, or, configures the key length to be used for `Easy DKIM <https://docs.aws.amazon.com/ses/latest/dg/send-email-authentication-dkim-easy.html>`_ .
        :param feedback_attributes: Used to enable or disable feedback forwarding for an identity.
        :param mail_from_attributes: Used to enable or disable the custom Mail-From domain configuration for an email identity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            cfn_email_identity_props = ses.CfnEmailIdentityProps(
                email_identity="emailIdentity",
            
                # the properties below are optional
                configuration_set_attributes=ses.CfnEmailIdentity.ConfigurationSetAttributesProperty(
                    configuration_set_name="configurationSetName"
                ),
                dkim_attributes=ses.CfnEmailIdentity.DkimAttributesProperty(
                    signing_enabled=False
                ),
                dkim_signing_attributes=ses.CfnEmailIdentity.DkimSigningAttributesProperty(
                    domain_signing_private_key="domainSigningPrivateKey",
                    domain_signing_selector="domainSigningSelector",
                    next_signing_key_length="nextSigningKeyLength"
                ),
                feedback_attributes=ses.CfnEmailIdentity.FeedbackAttributesProperty(
                    email_forwarding_enabled=False
                ),
                mail_from_attributes=ses.CfnEmailIdentity.MailFromAttributesProperty(
                    behavior_on_mx_failure="behaviorOnMxFailure",
                    mail_from_domain="mailFromDomain"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3e26635d9a29bd70d081bd12ae2f76d68303c184568003c88e9d459ac641b18)
            check_type(argname="argument email_identity", value=email_identity, expected_type=type_hints["email_identity"])
            check_type(argname="argument configuration_set_attributes", value=configuration_set_attributes, expected_type=type_hints["configuration_set_attributes"])
            check_type(argname="argument dkim_attributes", value=dkim_attributes, expected_type=type_hints["dkim_attributes"])
            check_type(argname="argument dkim_signing_attributes", value=dkim_signing_attributes, expected_type=type_hints["dkim_signing_attributes"])
            check_type(argname="argument feedback_attributes", value=feedback_attributes, expected_type=type_hints["feedback_attributes"])
            check_type(argname="argument mail_from_attributes", value=mail_from_attributes, expected_type=type_hints["mail_from_attributes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "email_identity": email_identity,
        }
        if configuration_set_attributes is not None:
            self._values["configuration_set_attributes"] = configuration_set_attributes
        if dkim_attributes is not None:
            self._values["dkim_attributes"] = dkim_attributes
        if dkim_signing_attributes is not None:
            self._values["dkim_signing_attributes"] = dkim_signing_attributes
        if feedback_attributes is not None:
            self._values["feedback_attributes"] = feedback_attributes
        if mail_from_attributes is not None:
            self._values["mail_from_attributes"] = mail_from_attributes

    @builtins.property
    def email_identity(self) -> builtins.str:
        '''The email address or domain to verify.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-emailidentity
        '''
        result = self._values.get("email_identity")
        assert result is not None, "Required property 'email_identity' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration_set_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEmailIdentity.ConfigurationSetAttributesProperty]]:
        '''Used to associate a configuration set with an email identity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-configurationsetattributes
        '''
        result = self._values.get("configuration_set_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEmailIdentity.ConfigurationSetAttributesProperty]], result)

    @builtins.property
    def dkim_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEmailIdentity.DkimAttributesProperty]]:
        '''An object that contains information about the DKIM attributes for the identity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-dkimattributes
        '''
        result = self._values.get("dkim_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEmailIdentity.DkimAttributesProperty]], result)

    @builtins.property
    def dkim_signing_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEmailIdentity.DkimSigningAttributesProperty]]:
        '''If your request includes this object, Amazon SES configures the identity to use Bring Your Own DKIM (BYODKIM) for DKIM authentication purposes, or, configures the key length to be used for `Easy DKIM <https://docs.aws.amazon.com/ses/latest/dg/send-email-authentication-dkim-easy.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-dkimsigningattributes
        '''
        result = self._values.get("dkim_signing_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEmailIdentity.DkimSigningAttributesProperty]], result)

    @builtins.property
    def feedback_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEmailIdentity.FeedbackAttributesProperty]]:
        '''Used to enable or disable feedback forwarding for an identity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-feedbackattributes
        '''
        result = self._values.get("feedback_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEmailIdentity.FeedbackAttributesProperty]], result)

    @builtins.property
    def mail_from_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEmailIdentity.MailFromAttributesProperty]]:
        '''Used to enable or disable the custom Mail-From domain configuration for an email identity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-emailidentity.html#cfn-ses-emailidentity-mailfromattributes
        '''
        result = self._values.get("mail_from_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEmailIdentity.MailFromAttributesProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEmailIdentityProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnReceiptFilter(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses.CfnReceiptFilter",
):
    '''A CloudFormation ``AWS::SES::ReceiptFilter``.

    Specify a new IP address filter. You use IP address filters when you receive email with Amazon SES.

    :cloudformationResource: AWS::SES::ReceiptFilter
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptfilter.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ses as ses
        
        cfn_receipt_filter = ses.CfnReceiptFilter(self, "MyCfnReceiptFilter",
            filter=ses.CfnReceiptFilter.FilterProperty(
                ip_filter=ses.CfnReceiptFilter.IpFilterProperty(
                    cidr="cidr",
                    policy="policy"
                ),
        
                # the properties below are optional
                name="name"
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        filter: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnReceiptFilter.FilterProperty", typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''Create a new ``AWS::SES::ReceiptFilter``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param filter: A data structure that describes the IP address filter to create, which consists of a name, an IP address range, and whether to allow or block mail from it.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05c2f1065db49ca19b225de3364838487829cc571fc76ebe5bacaa324a37a651)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnReceiptFilterProps(filter=filter)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39fb038b4f58e87d7653c5e341b14ee5cae1c4cdc23f52e4644c438bc9c12299)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d52466eff2ed506c217a7eacd465a0c7a4d7bb043832b04fffbb91b68baab4c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="filter")
    def filter(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptFilter.FilterProperty"]:
        '''A data structure that describes the IP address filter to create, which consists of a name, an IP address range, and whether to allow or block mail from it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptfilter.html#cfn-ses-receiptfilter-filter
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptFilter.FilterProperty"], jsii.get(self, "filter"))

    @filter.setter
    def filter(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptFilter.FilterProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d27d05e2b153099f7a40e474c17cd4bdcbd045f367dd459dce48138be373fd3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "filter", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnReceiptFilter.FilterProperty",
        jsii_struct_bases=[],
        name_mapping={"ip_filter": "ipFilter", "name": "name"},
    )
    class FilterProperty:
        def __init__(
            self,
            *,
            ip_filter: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnReceiptFilter.IpFilterProperty", typing.Dict[builtins.str, typing.Any]]],
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies an IP address filter.

            :param ip_filter: A structure that provides the IP addresses to block or allow, and whether to block or allow incoming mail from them.
            :param name: The name of the IP address filter. The name must meet the following requirements:. - Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-). - Start and end with a letter or number. - Contain 64 characters or fewer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-filter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                filter_property = ses.CfnReceiptFilter.FilterProperty(
                    ip_filter=ses.CfnReceiptFilter.IpFilterProperty(
                        cidr="cidr",
                        policy="policy"
                    ),
                
                    # the properties below are optional
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ef85abf22811dcf652326f6c8dd2c2056dc7d3f8c8065ecd40169113f1766e99)
                check_type(argname="argument ip_filter", value=ip_filter, expected_type=type_hints["ip_filter"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "ip_filter": ip_filter,
            }
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def ip_filter(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptFilter.IpFilterProperty"]:
            '''A structure that provides the IP addresses to block or allow, and whether to block or allow incoming mail from them.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-filter.html#cfn-ses-receiptfilter-filter-ipfilter
            '''
            result = self._values.get("ip_filter")
            assert result is not None, "Required property 'ip_filter' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptFilter.IpFilterProperty"], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the IP address filter. The name must meet the following requirements:.

            - Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), or dashes (-).
            - Start and end with a letter or number.
            - Contain 64 characters or fewer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-filter.html#cfn-ses-receiptfilter-filter-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnReceiptFilter.IpFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"cidr": "cidr", "policy": "policy"},
    )
    class IpFilterProperty:
        def __init__(self, *, cidr: builtins.str, policy: builtins.str) -> None:
            '''A receipt IP address filter enables you to specify whether to accept or reject mail originating from an IP address or range of IP addresses.

            For information about setting up IP address filters, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-ip-filtering-console-walkthrough.html>`_ .

            :param cidr: A single IP address or a range of IP addresses to block or allow, specified in Classless Inter-Domain Routing (CIDR) notation. An example of a single email address is 10.0.0.1. An example of a range of IP addresses is 10.0.0.1/24. For more information about CIDR notation, see `RFC 2317 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc2317>`_ .
            :param policy: Indicates whether to block or allow incoming mail from the specified IP addresses.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-ipfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                ip_filter_property = ses.CfnReceiptFilter.IpFilterProperty(
                    cidr="cidr",
                    policy="policy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e8c700d36d7f8266aa0fc65c9b6465de201aca33b6ac28dfd5b4b78d533e21d)
                check_type(argname="argument cidr", value=cidr, expected_type=type_hints["cidr"])
                check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cidr": cidr,
                "policy": policy,
            }

        @builtins.property
        def cidr(self) -> builtins.str:
            '''A single IP address or a range of IP addresses to block or allow, specified in Classless Inter-Domain Routing (CIDR) notation.

            An example of a single email address is 10.0.0.1. An example of a range of IP addresses is 10.0.0.1/24. For more information about CIDR notation, see `RFC 2317 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc2317>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-ipfilter.html#cfn-ses-receiptfilter-ipfilter-cidr
            '''
            result = self._values.get("cidr")
            assert result is not None, "Required property 'cidr' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def policy(self) -> builtins.str:
            '''Indicates whether to block or allow incoming mail from the specified IP addresses.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-ipfilter.html#cfn-ses-receiptfilter-ipfilter-policy
            '''
            result = self._values.get("policy")
            assert result is not None, "Required property 'policy' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IpFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.CfnReceiptFilterProps",
    jsii_struct_bases=[],
    name_mapping={"filter": "filter"},
)
class CfnReceiptFilterProps:
    def __init__(
        self,
        *,
        filter: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReceiptFilter.FilterProperty, typing.Dict[builtins.str, typing.Any]]],
    ) -> None:
        '''Properties for defining a ``CfnReceiptFilter``.

        :param filter: A data structure that describes the IP address filter to create, which consists of a name, an IP address range, and whether to allow or block mail from it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptfilter.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            cfn_receipt_filter_props = ses.CfnReceiptFilterProps(
                filter=ses.CfnReceiptFilter.FilterProperty(
                    ip_filter=ses.CfnReceiptFilter.IpFilterProperty(
                        cidr="cidr",
                        policy="policy"
                    ),
            
                    # the properties below are optional
                    name="name"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29474d88053c830ad11781445403eec9d50949a6d5546f79697e31fd3c6e11a5)
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "filter": filter,
        }

    @builtins.property
    def filter(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnReceiptFilter.FilterProperty]:
        '''A data structure that describes the IP address filter to create, which consists of a name, an IP address range, and whether to allow or block mail from it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptfilter.html#cfn-ses-receiptfilter-filter
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnReceiptFilter.FilterProperty], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReceiptFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnReceiptRule(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses.CfnReceiptRule",
):
    '''A CloudFormation ``AWS::SES::ReceiptRule``.

    Specifies a receipt rule.

    :cloudformationResource: AWS::SES::ReceiptRule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ses as ses
        
        cfn_receipt_rule = ses.CfnReceiptRule(self, "MyCfnReceiptRule",
            rule=ses.CfnReceiptRule.RuleProperty(
                actions=[ses.CfnReceiptRule.ActionProperty(
                    add_header_action=ses.CfnReceiptRule.AddHeaderActionProperty(
                        header_name="headerName",
                        header_value="headerValue"
                    ),
                    bounce_action=ses.CfnReceiptRule.BounceActionProperty(
                        message="message",
                        sender="sender",
                        smtp_reply_code="smtpReplyCode",
        
                        # the properties below are optional
                        status_code="statusCode",
                        topic_arn="topicArn"
                    ),
                    lambda_action=ses.CfnReceiptRule.LambdaActionProperty(
                        function_arn="functionArn",
        
                        # the properties below are optional
                        invocation_type="invocationType",
                        topic_arn="topicArn"
                    ),
                    s3_action=ses.CfnReceiptRule.S3ActionProperty(
                        bucket_name="bucketName",
        
                        # the properties below are optional
                        kms_key_arn="kmsKeyArn",
                        object_key_prefix="objectKeyPrefix",
                        topic_arn="topicArn"
                    ),
                    sns_action=ses.CfnReceiptRule.SNSActionProperty(
                        encoding="encoding",
                        topic_arn="topicArn"
                    ),
                    stop_action=ses.CfnReceiptRule.StopActionProperty(
                        scope="scope",
        
                        # the properties below are optional
                        topic_arn="topicArn"
                    ),
                    workmail_action=ses.CfnReceiptRule.WorkmailActionProperty(
                        organization_arn="organizationArn",
        
                        # the properties below are optional
                        topic_arn="topicArn"
                    )
                )],
                enabled=False,
                name="name",
                recipients=["recipients"],
                scan_enabled=False,
                tls_policy="tlsPolicy"
            ),
            rule_set_name="ruleSetName",
        
            # the properties below are optional
            after="after"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        rule: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnReceiptRule.RuleProperty", typing.Dict[builtins.str, typing.Any]]],
        rule_set_name: builtins.str,
        after: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::SES::ReceiptRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param rule: A data structure that contains the specified rule's name, actions, recipients, domains, enabled status, scan status, and TLS policy.
        :param rule_set_name: The name of the rule set where the receipt rule is added.
        :param after: The name of an existing rule after which the new rule is placed. If this parameter is null, the new rule is inserted at the beginning of the rule list.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdeb50f3f81bada0d11b4dc5376bfe771b34f7860802a9e68cb8d547e857a21d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnReceiptRuleProps(
            rule=rule, rule_set_name=rule_set_name, after=after
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82f85e94bb3707ef022f954c96416e9286e1f65da69502a142ac7d2534ae0a9a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f31984613cd495e566c4142b7054eeea557ea4b11c894112bf6d2db95799c36c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.RuleProperty"]:
        '''A data structure that contains the specified rule's name, actions, recipients, domains, enabled status, scan status, and TLS policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html#cfn-ses-receiptrule-rule
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.RuleProperty"], jsii.get(self, "rule"))

    @rule.setter
    def rule(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.RuleProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60310f384dc7e1ad3b0ff906100871ab80d0ebb1cbba5382a100f3f56c1b43f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rule", value)

    @builtins.property
    @jsii.member(jsii_name="ruleSetName")
    def rule_set_name(self) -> builtins.str:
        '''The name of the rule set where the receipt rule is added.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html#cfn-ses-receiptrule-rulesetname
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleSetName"))

    @rule_set_name.setter
    def rule_set_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c259135681ea9a0e2d2f49ba97265f2838f60ff72076584fada2e549689c964)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleSetName", value)

    @builtins.property
    @jsii.member(jsii_name="after")
    def after(self) -> typing.Optional[builtins.str]:
        '''The name of an existing rule after which the new rule is placed.

        If this parameter is null, the new rule is inserted at the beginning of the rule list.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html#cfn-ses-receiptrule-after
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "after"))

    @after.setter
    def after(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f140fe9f0405c85b2f9efb527ac561f53ef8fd7717c7c6b99858d1af620278f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "after", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_header_action": "addHeaderAction",
            "bounce_action": "bounceAction",
            "lambda_action": "lambdaAction",
            "s3_action": "s3Action",
            "sns_action": "snsAction",
            "stop_action": "stopAction",
            "workmail_action": "workmailAction",
        },
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            add_header_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnReceiptRule.AddHeaderActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            bounce_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnReceiptRule.BounceActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            lambda_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnReceiptRule.LambdaActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnReceiptRule.S3ActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            sns_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnReceiptRule.SNSActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            stop_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnReceiptRule.StopActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            workmail_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnReceiptRule.WorkmailActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''An action that Amazon SES can take when it receives an email on behalf of one or more email addresses or domains that you own.

            An instance of this data type can represent only one action.

            For information about setting up receipt rules, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-receipt-rules-console-walkthrough.html>`_ .

            :param add_header_action: Adds a header to the received email.
            :param bounce_action: Rejects the received email by returning a bounce response to the sender and, optionally, publishes a notification to Amazon Simple Notification Service (Amazon SNS).
            :param lambda_action: Calls an AWS Lambda function, and optionally, publishes a notification to Amazon SNS.
            :param s3_action: Saves the received message to an Amazon Simple Storage Service (Amazon S3) bucket and, optionally, publishes a notification to Amazon SNS.
            :param sns_action: Publishes the email content within a notification to Amazon SNS.
            :param stop_action: Terminates the evaluation of the receipt rule set and optionally publishes a notification to Amazon SNS.
            :param workmail_action: Calls Amazon WorkMail and, optionally, publishes a notification to Amazon Amazon SNS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                action_property = ses.CfnReceiptRule.ActionProperty(
                    add_header_action=ses.CfnReceiptRule.AddHeaderActionProperty(
                        header_name="headerName",
                        header_value="headerValue"
                    ),
                    bounce_action=ses.CfnReceiptRule.BounceActionProperty(
                        message="message",
                        sender="sender",
                        smtp_reply_code="smtpReplyCode",
                
                        # the properties below are optional
                        status_code="statusCode",
                        topic_arn="topicArn"
                    ),
                    lambda_action=ses.CfnReceiptRule.LambdaActionProperty(
                        function_arn="functionArn",
                
                        # the properties below are optional
                        invocation_type="invocationType",
                        topic_arn="topicArn"
                    ),
                    s3_action=ses.CfnReceiptRule.S3ActionProperty(
                        bucket_name="bucketName",
                
                        # the properties below are optional
                        kms_key_arn="kmsKeyArn",
                        object_key_prefix="objectKeyPrefix",
                        topic_arn="topicArn"
                    ),
                    sns_action=ses.CfnReceiptRule.SNSActionProperty(
                        encoding="encoding",
                        topic_arn="topicArn"
                    ),
                    stop_action=ses.CfnReceiptRule.StopActionProperty(
                        scope="scope",
                
                        # the properties below are optional
                        topic_arn="topicArn"
                    ),
                    workmail_action=ses.CfnReceiptRule.WorkmailActionProperty(
                        organization_arn="organizationArn",
                
                        # the properties below are optional
                        topic_arn="topicArn"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ead34a7d8bb1152d74a37e0378dccfecd1284762b94ea8dc9aaa10c6d45995ea)
                check_type(argname="argument add_header_action", value=add_header_action, expected_type=type_hints["add_header_action"])
                check_type(argname="argument bounce_action", value=bounce_action, expected_type=type_hints["bounce_action"])
                check_type(argname="argument lambda_action", value=lambda_action, expected_type=type_hints["lambda_action"])
                check_type(argname="argument s3_action", value=s3_action, expected_type=type_hints["s3_action"])
                check_type(argname="argument sns_action", value=sns_action, expected_type=type_hints["sns_action"])
                check_type(argname="argument stop_action", value=stop_action, expected_type=type_hints["stop_action"])
                check_type(argname="argument workmail_action", value=workmail_action, expected_type=type_hints["workmail_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if add_header_action is not None:
                self._values["add_header_action"] = add_header_action
            if bounce_action is not None:
                self._values["bounce_action"] = bounce_action
            if lambda_action is not None:
                self._values["lambda_action"] = lambda_action
            if s3_action is not None:
                self._values["s3_action"] = s3_action
            if sns_action is not None:
                self._values["sns_action"] = sns_action
            if stop_action is not None:
                self._values["stop_action"] = stop_action
            if workmail_action is not None:
                self._values["workmail_action"] = workmail_action

        @builtins.property
        def add_header_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.AddHeaderActionProperty"]]:
            '''Adds a header to the received email.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-addheaderaction
            '''
            result = self._values.get("add_header_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.AddHeaderActionProperty"]], result)

        @builtins.property
        def bounce_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.BounceActionProperty"]]:
            '''Rejects the received email by returning a bounce response to the sender and, optionally, publishes a notification to Amazon Simple Notification Service (Amazon SNS).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-bounceaction
            '''
            result = self._values.get("bounce_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.BounceActionProperty"]], result)

        @builtins.property
        def lambda_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.LambdaActionProperty"]]:
            '''Calls an AWS Lambda function, and optionally, publishes a notification to Amazon SNS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-lambdaaction
            '''
            result = self._values.get("lambda_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.LambdaActionProperty"]], result)

        @builtins.property
        def s3_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.S3ActionProperty"]]:
            '''Saves the received message to an Amazon Simple Storage Service (Amazon S3) bucket and, optionally, publishes a notification to Amazon SNS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-s3action
            '''
            result = self._values.get("s3_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.S3ActionProperty"]], result)

        @builtins.property
        def sns_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.SNSActionProperty"]]:
            '''Publishes the email content within a notification to Amazon SNS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-snsaction
            '''
            result = self._values.get("sns_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.SNSActionProperty"]], result)

        @builtins.property
        def stop_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.StopActionProperty"]]:
            '''Terminates the evaluation of the receipt rule set and optionally publishes a notification to Amazon SNS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-stopaction
            '''
            result = self._values.get("stop_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.StopActionProperty"]], result)

        @builtins.property
        def workmail_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.WorkmailActionProperty"]]:
            '''Calls Amazon WorkMail and, optionally, publishes a notification to Amazon Amazon SNS.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-workmailaction
            '''
            result = self._values.get("workmail_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.WorkmailActionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.AddHeaderActionProperty",
        jsii_struct_bases=[],
        name_mapping={"header_name": "headerName", "header_value": "headerValue"},
    )
    class AddHeaderActionProperty:
        def __init__(
            self,
            *,
            header_name: builtins.str,
            header_value: builtins.str,
        ) -> None:
            '''When included in a receipt rule, this action adds a header to the received email.

            For information about adding a header using a receipt rule, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-action-add-header.html>`_ .

            :param header_name: The name of the header to add to the incoming message. The name must contain at least one character, and can contain up to 50 characters. It consists of alphanumeric (a–z, A–Z, 0–9) characters and dashes.
            :param header_value: The content to include in the header. This value can contain up to 2048 characters. It can't contain newline ( ``\\n`` ) or carriage return ( ``\\r`` ) characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-addheaderaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                add_header_action_property = ses.CfnReceiptRule.AddHeaderActionProperty(
                    header_name="headerName",
                    header_value="headerValue"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__79a146577e59cdc7eeb9344fd4d6d0c00f4a66542172c4e23804856be51d3788)
                check_type(argname="argument header_name", value=header_name, expected_type=type_hints["header_name"])
                check_type(argname="argument header_value", value=header_value, expected_type=type_hints["header_value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "header_name": header_name,
                "header_value": header_value,
            }

        @builtins.property
        def header_name(self) -> builtins.str:
            '''The name of the header to add to the incoming message.

            The name must contain at least one character, and can contain up to 50 characters. It consists of alphanumeric (a–z, A–Z, 0–9) characters and dashes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-addheaderaction.html#cfn-ses-receiptrule-addheaderaction-headername
            '''
            result = self._values.get("header_name")
            assert result is not None, "Required property 'header_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def header_value(self) -> builtins.str:
            '''The content to include in the header.

            This value can contain up to 2048 characters. It can't contain newline ( ``\\n`` ) or carriage return ( ``\\r`` ) characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-addheaderaction.html#cfn-ses-receiptrule-addheaderaction-headervalue
            '''
            result = self._values.get("header_value")
            assert result is not None, "Required property 'header_value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AddHeaderActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.BounceActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "message": "message",
            "sender": "sender",
            "smtp_reply_code": "smtpReplyCode",
            "status_code": "statusCode",
            "topic_arn": "topicArn",
        },
    )
    class BounceActionProperty:
        def __init__(
            self,
            *,
            message: builtins.str,
            sender: builtins.str,
            smtp_reply_code: builtins.str,
            status_code: typing.Optional[builtins.str] = None,
            topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When included in a receipt rule, this action rejects the received email by returning a bounce response to the sender and, optionally, publishes a notification to Amazon Simple Notification Service (Amazon SNS).

            For information about sending a bounce message in response to a received email, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-action-bounce.html>`_ .

            :param message: Human-readable text to include in the bounce message.
            :param sender: The email address of the sender of the bounced email. This is the address from which the bounce message is sent.
            :param smtp_reply_code: The SMTP reply code, as defined by `RFC 5321 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc5321>`_ .
            :param status_code: The SMTP enhanced status code, as defined by `RFC 3463 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc3463>`_ .
            :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the bounce action is taken. You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS. For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                bounce_action_property = ses.CfnReceiptRule.BounceActionProperty(
                    message="message",
                    sender="sender",
                    smtp_reply_code="smtpReplyCode",
                
                    # the properties below are optional
                    status_code="statusCode",
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4968c069223b8dbfd25efbd33e5a25c5ed23b2ad1e45757f7bd4c2f94931772d)
                check_type(argname="argument message", value=message, expected_type=type_hints["message"])
                check_type(argname="argument sender", value=sender, expected_type=type_hints["sender"])
                check_type(argname="argument smtp_reply_code", value=smtp_reply_code, expected_type=type_hints["smtp_reply_code"])
                check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "message": message,
                "sender": sender,
                "smtp_reply_code": smtp_reply_code,
            }
            if status_code is not None:
                self._values["status_code"] = status_code
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def message(self) -> builtins.str:
            '''Human-readable text to include in the bounce message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-message
            '''
            result = self._values.get("message")
            assert result is not None, "Required property 'message' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def sender(self) -> builtins.str:
            '''The email address of the sender of the bounced email.

            This is the address from which the bounce message is sent.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-sender
            '''
            result = self._values.get("sender")
            assert result is not None, "Required property 'sender' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def smtp_reply_code(self) -> builtins.str:
            '''The SMTP reply code, as defined by `RFC 5321 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc5321>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-smtpreplycode
            '''
            result = self._values.get("smtp_reply_code")
            assert result is not None, "Required property 'smtp_reply_code' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def status_code(self) -> typing.Optional[builtins.str]:
            '''The SMTP enhanced status code, as defined by `RFC 3463 <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc3463>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-statuscode
            '''
            result = self._values.get("status_code")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the bounce action is taken.

            You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS.

            For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BounceActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.LambdaActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "function_arn": "functionArn",
            "invocation_type": "invocationType",
            "topic_arn": "topicArn",
        },
    )
    class LambdaActionProperty:
        def __init__(
            self,
            *,
            function_arn: builtins.str,
            invocation_type: typing.Optional[builtins.str] = None,
            topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When included in a receipt rule, this action calls an AWS Lambda function and, optionally, publishes a notification to Amazon Simple Notification Service (Amazon SNS).

            To enable Amazon SES to call your AWS Lambda function or to publish to an Amazon SNS topic of another account, Amazon SES must have permission to access those resources. For information about giving permissions, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-permissions.html>`_ .

            For information about using AWS Lambda actions in receipt rules, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-action-lambda.html>`_ .

            :param function_arn: The Amazon Resource Name (ARN) of the AWS Lambda function. An example of an AWS Lambda function ARN is ``arn:aws:lambda:us-west-2:account-id:function:MyFunction`` . For more information about AWS Lambda, see the `AWS Lambda Developer Guide <https://docs.aws.amazon.com/lambda/latest/dg/welcome.html>`_ .
            :param invocation_type: The invocation type of the AWS Lambda function. An invocation type of ``RequestResponse`` means that the execution of the function immediately results in a response, and a value of ``Event`` means that the function is invoked asynchronously. The default value is ``Event`` . For information about AWS Lambda invocation types, see the `AWS Lambda Developer Guide <https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html>`_ . .. epigraph:: There is a 30-second timeout on ``RequestResponse`` invocations. You should use ``Event`` invocation in most cases. Use ``RequestResponse`` only to make a mail flow decision, such as whether to stop the receipt rule or the receipt rule set.
            :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the Lambda action is executed. You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS. For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-lambdaaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                lambda_action_property = ses.CfnReceiptRule.LambdaActionProperty(
                    function_arn="functionArn",
                
                    # the properties below are optional
                    invocation_type="invocationType",
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7f43f93e4d1c2ce69c8deca1e9f8fc1d02d5072221eb7202d439838815dc27db)
                check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
                check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "function_arn": function_arn,
            }
            if invocation_type is not None:
                self._values["invocation_type"] = invocation_type
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def function_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the AWS Lambda function.

            An example of an AWS Lambda function ARN is ``arn:aws:lambda:us-west-2:account-id:function:MyFunction`` . For more information about AWS Lambda, see the `AWS Lambda Developer Guide <https://docs.aws.amazon.com/lambda/latest/dg/welcome.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-lambdaaction.html#cfn-ses-receiptrule-lambdaaction-functionarn
            '''
            result = self._values.get("function_arn")
            assert result is not None, "Required property 'function_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def invocation_type(self) -> typing.Optional[builtins.str]:
            '''The invocation type of the AWS Lambda function.

            An invocation type of ``RequestResponse`` means that the execution of the function immediately results in a response, and a value of ``Event`` means that the function is invoked asynchronously. The default value is ``Event`` . For information about AWS Lambda invocation types, see the `AWS Lambda Developer Guide <https://docs.aws.amazon.com/lambda/latest/dg/API_Invoke.html>`_ .
            .. epigraph::

               There is a 30-second timeout on ``RequestResponse`` invocations. You should use ``Event`` invocation in most cases. Use ``RequestResponse`` only to make a mail flow decision, such as whether to stop the receipt rule or the receipt rule set.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-lambdaaction.html#cfn-ses-receiptrule-lambdaaction-invocationtype
            '''
            result = self._values.get("invocation_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the Lambda action is executed.

            You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS.

            For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-lambdaaction.html#cfn-ses-receiptrule-lambdaaction-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.RuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "actions": "actions",
            "enabled": "enabled",
            "name": "name",
            "recipients": "recipients",
            "scan_enabled": "scanEnabled",
            "tls_policy": "tlsPolicy",
        },
    )
    class RuleProperty:
        def __init__(
            self,
            *,
            actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnReceiptRule.ActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            name: typing.Optional[builtins.str] = None,
            recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
            scan_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            tls_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Receipt rules enable you to specify which actions Amazon SES should take when it receives mail on behalf of one or more email addresses or domains that you own.

            Each receipt rule defines a set of email addresses or domains that it applies to. If the email addresses or domains match at least one recipient address of the message, Amazon SES executes all of the receipt rule's actions on the message.

            For information about setting up receipt rules, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-receipt-rules-console-walkthrough.html>`_ .

            :param actions: An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule.
            :param enabled: If ``true`` , the receipt rule is active. The default value is ``false`` .
            :param name: The name of the receipt rule. The name must meet the following requirements:. - Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), dashes (-), or periods (.). - Start and end with a letter or number. - Contain 64 characters or fewer.
            :param recipients: The recipient domains and email addresses that the receipt rule applies to. If this field is not specified, this rule matches all recipients on all verified domains.
            :param scan_enabled: If ``true`` , then messages that this receipt rule applies to are scanned for spam and viruses. The default value is ``false`` .
            :param tls_policy: Specifies whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS). If this parameter is set to ``Require`` , Amazon SES bounces emails that are not received over TLS. The default is ``Optional`` . Valid Values: ``Require | Optional``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                rule_property = ses.CfnReceiptRule.RuleProperty(
                    actions=[ses.CfnReceiptRule.ActionProperty(
                        add_header_action=ses.CfnReceiptRule.AddHeaderActionProperty(
                            header_name="headerName",
                            header_value="headerValue"
                        ),
                        bounce_action=ses.CfnReceiptRule.BounceActionProperty(
                            message="message",
                            sender="sender",
                            smtp_reply_code="smtpReplyCode",
                
                            # the properties below are optional
                            status_code="statusCode",
                            topic_arn="topicArn"
                        ),
                        lambda_action=ses.CfnReceiptRule.LambdaActionProperty(
                            function_arn="functionArn",
                
                            # the properties below are optional
                            invocation_type="invocationType",
                            topic_arn="topicArn"
                        ),
                        s3_action=ses.CfnReceiptRule.S3ActionProperty(
                            bucket_name="bucketName",
                
                            # the properties below are optional
                            kms_key_arn="kmsKeyArn",
                            object_key_prefix="objectKeyPrefix",
                            topic_arn="topicArn"
                        ),
                        sns_action=ses.CfnReceiptRule.SNSActionProperty(
                            encoding="encoding",
                            topic_arn="topicArn"
                        ),
                        stop_action=ses.CfnReceiptRule.StopActionProperty(
                            scope="scope",
                
                            # the properties below are optional
                            topic_arn="topicArn"
                        ),
                        workmail_action=ses.CfnReceiptRule.WorkmailActionProperty(
                            organization_arn="organizationArn",
                
                            # the properties below are optional
                            topic_arn="topicArn"
                        )
                    )],
                    enabled=False,
                    name="name",
                    recipients=["recipients"],
                    scan_enabled=False,
                    tls_policy="tlsPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__44983645286f8cbdb286ef6ed092191a41032a973ed7e0b43bfb53b1141e9c54)
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument recipients", value=recipients, expected_type=type_hints["recipients"])
                check_type(argname="argument scan_enabled", value=scan_enabled, expected_type=type_hints["scan_enabled"])
                check_type(argname="argument tls_policy", value=tls_policy, expected_type=type_hints["tls_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if actions is not None:
                self._values["actions"] = actions
            if enabled is not None:
                self._values["enabled"] = enabled
            if name is not None:
                self._values["name"] = name
            if recipients is not None:
                self._values["recipients"] = recipients
            if scan_enabled is not None:
                self._values["scan_enabled"] = scan_enabled
            if tls_policy is not None:
                self._values["tls_policy"] = tls_policy

        @builtins.property
        def actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.ActionProperty"]]]]:
            '''An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-actions
            '''
            result = self._values.get("actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnReceiptRule.ActionProperty"]]]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''If ``true`` , the receipt rule is active.

            The default value is ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the receipt rule. The name must meet the following requirements:.

            - Contain only ASCII letters (a-z, A-Z), numbers (0-9), underscores (_), dashes (-), or periods (.).
            - Start and end with a letter or number.
            - Contain 64 characters or fewer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def recipients(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The recipient domains and email addresses that the receipt rule applies to.

            If this field is not specified, this rule matches all recipients on all verified domains.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-recipients
            '''
            result = self._values.get("recipients")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def scan_enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''If ``true`` , then messages that this receipt rule applies to are scanned for spam and viruses.

            The default value is ``false`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-scanenabled
            '''
            result = self._values.get("scan_enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def tls_policy(self) -> typing.Optional[builtins.str]:
            '''Specifies whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS).

            If this parameter is set to ``Require`` , Amazon SES bounces emails that are not received over TLS. The default is ``Optional`` .

            Valid Values: ``Require | Optional``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-tlspolicy
            '''
            result = self._values.get("tls_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.S3ActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_name": "bucketName",
            "kms_key_arn": "kmsKeyArn",
            "object_key_prefix": "objectKeyPrefix",
            "topic_arn": "topicArn",
        },
    )
    class S3ActionProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            kms_key_arn: typing.Optional[builtins.str] = None,
            object_key_prefix: typing.Optional[builtins.str] = None,
            topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When included in a receipt rule, this action saves the received message to an Amazon Simple Storage Service (Amazon S3) bucket and, optionally, publishes a notification to Amazon Simple Notification Service (Amazon SNS).

            To enable Amazon SES to write emails to your Amazon S3 bucket, use an AWS KMS key to encrypt your emails, or publish to an Amazon SNS topic of another account, Amazon SES must have permission to access those resources. For information about granting permissions, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-permissions.html>`_ .
            .. epigraph::

               When you save your emails to an Amazon S3 bucket, the maximum email size (including headers) is 30 MB. Emails larger than that bounces.

            For information about specifying Amazon S3 actions in receipt rules, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-action-s3.html>`_ .

            :param bucket_name: The name of the Amazon S3 bucket for incoming email.
            :param kms_key_arn: The customer master key that Amazon SES should use to encrypt your emails before saving them to the Amazon S3 bucket. You can use the default master key or a custom master key that you created in AWS KMS as follows: - To use the default master key, provide an ARN in the form of ``arn:aws:kms:REGION:ACCOUNT-ID-WITHOUT-HYPHENS:alias/aws/ses`` . For example, if your AWS account ID is 123456789012 and you want to use the default master key in the US West (Oregon) Region, the ARN of the default master key would be ``arn:aws:kms:us-west-2:123456789012:alias/aws/ses`` . If you use the default master key, you don't need to perform any extra steps to give Amazon SES permission to use the key. - To use a custom master key that you created in AWS KMS, provide the ARN of the master key and ensure that you add a statement to your key's policy to give Amazon SES permission to use it. For more information about giving permissions, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-permissions.html>`_ . For more information about key policies, see the `AWS KMS Developer Guide <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html>`_ . If you do not specify a master key, Amazon SES does not encrypt your emails. .. epigraph:: Your mail is encrypted by Amazon SES using the Amazon S3 encryption client before the mail is submitted to Amazon S3 for storage. It is not encrypted using Amazon S3 server-side encryption. This means that you must use the Amazon S3 encryption client to decrypt the email after retrieving it from Amazon S3, as the service has no access to use your AWS KMS keys for decryption. This encryption client is currently available with the `AWS SDK for Java <https://docs.aws.amazon.com/sdk-for-java/>`_ and `AWS SDK for Ruby <https://docs.aws.amazon.com/sdk-for-ruby/>`_ only. For more information about client-side encryption using AWS KMS master keys, see the `Amazon S3 Developer Guide <https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingClientSideEncryption.html>`_ .
            :param object_key_prefix: The key prefix of the Amazon S3 bucket. The key prefix is similar to a directory name that enables you to store similar data under the same directory in a bucket.
            :param topic_arn: The ARN of the Amazon SNS topic to notify when the message is saved to the Amazon S3 bucket. You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS. For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                s3_action_property = ses.CfnReceiptRule.S3ActionProperty(
                    bucket_name="bucketName",
                
                    # the properties below are optional
                    kms_key_arn="kmsKeyArn",
                    object_key_prefix="objectKeyPrefix",
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ffad8fea384dd0c7624b0693273ee36d7bb0b3beb516dd6d0b3ca0507f5b409d)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
                check_type(argname="argument object_key_prefix", value=object_key_prefix, expected_type=type_hints["object_key_prefix"])
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
            }
            if kms_key_arn is not None:
                self._values["kms_key_arn"] = kms_key_arn
            if object_key_prefix is not None:
                self._values["object_key_prefix"] = object_key_prefix
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''The name of the Amazon S3 bucket for incoming email.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html#cfn-ses-receiptrule-s3action-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def kms_key_arn(self) -> typing.Optional[builtins.str]:
            '''The customer master key that Amazon SES should use to encrypt your emails before saving them to the Amazon S3 bucket.

            You can use the default master key or a custom master key that you created in AWS KMS as follows:

            - To use the default master key, provide an ARN in the form of ``arn:aws:kms:REGION:ACCOUNT-ID-WITHOUT-HYPHENS:alias/aws/ses`` . For example, if your AWS account ID is 123456789012 and you want to use the default master key in the US West (Oregon) Region, the ARN of the default master key would be ``arn:aws:kms:us-west-2:123456789012:alias/aws/ses`` . If you use the default master key, you don't need to perform any extra steps to give Amazon SES permission to use the key.
            - To use a custom master key that you created in AWS KMS, provide the ARN of the master key and ensure that you add a statement to your key's policy to give Amazon SES permission to use it. For more information about giving permissions, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-permissions.html>`_ .

            For more information about key policies, see the `AWS KMS Developer Guide <https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html>`_ . If you do not specify a master key, Amazon SES does not encrypt your emails.
            .. epigraph::

               Your mail is encrypted by Amazon SES using the Amazon S3 encryption client before the mail is submitted to Amazon S3 for storage. It is not encrypted using Amazon S3 server-side encryption. This means that you must use the Amazon S3 encryption client to decrypt the email after retrieving it from Amazon S3, as the service has no access to use your AWS KMS keys for decryption. This encryption client is currently available with the `AWS SDK for Java <https://docs.aws.amazon.com/sdk-for-java/>`_ and `AWS SDK for Ruby <https://docs.aws.amazon.com/sdk-for-ruby/>`_ only. For more information about client-side encryption using AWS KMS master keys, see the `Amazon S3 Developer Guide <https://docs.aws.amazon.com/AmazonS3/latest/dev/UsingClientSideEncryption.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html#cfn-ses-receiptrule-s3action-kmskeyarn
            '''
            result = self._values.get("kms_key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def object_key_prefix(self) -> typing.Optional[builtins.str]:
            '''The key prefix of the Amazon S3 bucket.

            The key prefix is similar to a directory name that enables you to store similar data under the same directory in a bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html#cfn-ses-receiptrule-s3action-objectkeyprefix
            '''
            result = self._values.get("object_key_prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Amazon SNS topic to notify when the message is saved to the Amazon S3 bucket.

            You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS.

            For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html#cfn-ses-receiptrule-s3action-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.SNSActionProperty",
        jsii_struct_bases=[],
        name_mapping={"encoding": "encoding", "topic_arn": "topicArn"},
    )
    class SNSActionProperty:
        def __init__(
            self,
            *,
            encoding: typing.Optional[builtins.str] = None,
            topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When included in a receipt rule, this action publishes a notification to Amazon Simple Notification Service (Amazon SNS).

            This action includes a complete copy of the email content in the Amazon SNS notifications. Amazon SNS notifications for all other actions simply provide information about the email. They do not include the email content itself.

            If you own the Amazon SNS topic, you don't need to do anything to give Amazon SES permission to publish emails to it. However, if you don't own the Amazon SNS topic, you need to attach a policy to the topic to give Amazon SES permissions to access it. For information about giving permissions, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-permissions.html>`_ .
            .. epigraph::

               You can only publish emails that are 150 KB or less (including the header) to Amazon SNS. Larger emails bounce. If you anticipate emails larger than 150 KB, use the S3 action instead.

            For information about using a receipt rule to publish an Amazon SNS notification, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-action-sns.html>`_ .

            :param encoding: The encoding to use for the email within the Amazon SNS notification. UTF-8 is easier to use, but may not preserve all special characters when a message was encoded with a different encoding format. Base64 preserves all special characters. The default value is UTF-8.
            :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to notify. You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS. For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-snsaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                s_nSAction_property = ses.CfnReceiptRule.SNSActionProperty(
                    encoding="encoding",
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e774b238b52714bf99eb38772dd49314b558f5a78f6cad33a8b666dcc5f9d18a)
                check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if encoding is not None:
                self._values["encoding"] = encoding
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def encoding(self) -> typing.Optional[builtins.str]:
            '''The encoding to use for the email within the Amazon SNS notification.

            UTF-8 is easier to use, but may not preserve all special characters when a message was encoded with a different encoding format. Base64 preserves all special characters. The default value is UTF-8.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-snsaction.html#cfn-ses-receiptrule-snsaction-encoding
            '''
            result = self._values.get("encoding")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SNS topic to notify.

            You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS.

            For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-snsaction.html#cfn-ses-receiptrule-snsaction-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SNSActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.StopActionProperty",
        jsii_struct_bases=[],
        name_mapping={"scope": "scope", "topic_arn": "topicArn"},
    )
    class StopActionProperty:
        def __init__(
            self,
            *,
            scope: builtins.str,
            topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When included in a receipt rule, this action terminates the evaluation of the receipt rule set and, optionally, publishes a notification to Amazon Simple Notification Service (Amazon SNS).

            For information about setting a stop action in a receipt rule, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-action-stop.html>`_ .

            :param scope: The scope of the StopAction. The only acceptable value is ``RuleSet`` .
            :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the stop action is taken. You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ Amazon SNS operation. For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-stopaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                stop_action_property = ses.CfnReceiptRule.StopActionProperty(
                    scope="scope",
                
                    # the properties below are optional
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5164570f6613f6deba8cc3127b441841cf7aa01b75c8e6ea9bd5b0a6a0ff436b)
                check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "scope": scope,
            }
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def scope(self) -> builtins.str:
            '''The scope of the StopAction.

            The only acceptable value is ``RuleSet`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-stopaction.html#cfn-ses-receiptrule-stopaction-scope
            '''
            result = self._values.get("scope")
            assert result is not None, "Required property 'scope' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the stop action is taken.

            You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ Amazon SNS operation.

            For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-stopaction.html#cfn-ses-receiptrule-stopaction-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StopActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.WorkmailActionProperty",
        jsii_struct_bases=[],
        name_mapping={"organization_arn": "organizationArn", "topic_arn": "topicArn"},
    )
    class WorkmailActionProperty:
        def __init__(
            self,
            *,
            organization_arn: builtins.str,
            topic_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''When included in a receipt rule, this action calls Amazon WorkMail and, optionally, publishes a notification to Amazon Simple Notification Service (Amazon SNS).

            It usually isn't necessary to set this up manually, because Amazon WorkMail adds the rule automatically during its setup procedure.

            For information using a receipt rule to call Amazon WorkMail, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-action-workmail.html>`_ .

            :param organization_arn: The Amazon Resource Name (ARN) of the Amazon WorkMail organization. Amazon WorkMail ARNs use the following format:. ``arn:aws:workmail:<region>:<awsAccountId>:organization/<workmailOrganizationId>`` You can find the ID of your organization by using the `ListOrganizations <https://docs.aws.amazon.com/workmail/latest/APIReference/API_ListOrganizations.html>`_ operation in Amazon WorkMail. Amazon WorkMail organization IDs begin with " ``m-`` ", followed by a string of alphanumeric characters. For information about Amazon WorkMail organizations, see the `Amazon WorkMail Administrator Guide <https://docs.aws.amazon.com/workmail/latest/adminguide/organizations_overview.html>`_ .
            :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the WorkMail action is called. You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS. For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-workmailaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                workmail_action_property = ses.CfnReceiptRule.WorkmailActionProperty(
                    organization_arn="organizationArn",
                
                    # the properties below are optional
                    topic_arn="topicArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eabf0dba6adad414bc7330c34b82e3cd1d896b65fced49928d373478bbc1268b)
                check_type(argname="argument organization_arn", value=organization_arn, expected_type=type_hints["organization_arn"])
                check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "organization_arn": organization_arn,
            }
            if topic_arn is not None:
                self._values["topic_arn"] = topic_arn

        @builtins.property
        def organization_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the Amazon WorkMail organization. Amazon WorkMail ARNs use the following format:.

            ``arn:aws:workmail:<region>:<awsAccountId>:organization/<workmailOrganizationId>``

            You can find the ID of your organization by using the `ListOrganizations <https://docs.aws.amazon.com/workmail/latest/APIReference/API_ListOrganizations.html>`_ operation in Amazon WorkMail. Amazon WorkMail organization IDs begin with " ``m-`` ", followed by a string of alphanumeric characters.

            For information about Amazon WorkMail organizations, see the `Amazon WorkMail Administrator Guide <https://docs.aws.amazon.com/workmail/latest/adminguide/organizations_overview.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-workmailaction.html#cfn-ses-receiptrule-workmailaction-organizationarn
            '''
            result = self._values.get("organization_arn")
            assert result is not None, "Required property 'organization_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def topic_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the WorkMail action is called.

            You can find the ARN of a topic by using the `ListTopics <https://docs.aws.amazon.com/sns/latest/api/API_ListTopics.html>`_ operation in Amazon SNS.

            For more information about Amazon SNS topics, see the `Amazon SNS Developer Guide <https://docs.aws.amazon.com/sns/latest/dg/CreateTopic.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-workmailaction.html#cfn-ses-receiptrule-workmailaction-topicarn
            '''
            result = self._values.get("topic_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkmailActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.CfnReceiptRuleProps",
    jsii_struct_bases=[],
    name_mapping={"rule": "rule", "rule_set_name": "ruleSetName", "after": "after"},
)
class CfnReceiptRuleProps:
    def __init__(
        self,
        *,
        rule: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReceiptRule.RuleProperty, typing.Dict[builtins.str, typing.Any]]],
        rule_set_name: builtins.str,
        after: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnReceiptRule``.

        :param rule: A data structure that contains the specified rule's name, actions, recipients, domains, enabled status, scan status, and TLS policy.
        :param rule_set_name: The name of the rule set where the receipt rule is added.
        :param after: The name of an existing rule after which the new rule is placed. If this parameter is null, the new rule is inserted at the beginning of the rule list.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            cfn_receipt_rule_props = ses.CfnReceiptRuleProps(
                rule=ses.CfnReceiptRule.RuleProperty(
                    actions=[ses.CfnReceiptRule.ActionProperty(
                        add_header_action=ses.CfnReceiptRule.AddHeaderActionProperty(
                            header_name="headerName",
                            header_value="headerValue"
                        ),
                        bounce_action=ses.CfnReceiptRule.BounceActionProperty(
                            message="message",
                            sender="sender",
                            smtp_reply_code="smtpReplyCode",
            
                            # the properties below are optional
                            status_code="statusCode",
                            topic_arn="topicArn"
                        ),
                        lambda_action=ses.CfnReceiptRule.LambdaActionProperty(
                            function_arn="functionArn",
            
                            # the properties below are optional
                            invocation_type="invocationType",
                            topic_arn="topicArn"
                        ),
                        s3_action=ses.CfnReceiptRule.S3ActionProperty(
                            bucket_name="bucketName",
            
                            # the properties below are optional
                            kms_key_arn="kmsKeyArn",
                            object_key_prefix="objectKeyPrefix",
                            topic_arn="topicArn"
                        ),
                        sns_action=ses.CfnReceiptRule.SNSActionProperty(
                            encoding="encoding",
                            topic_arn="topicArn"
                        ),
                        stop_action=ses.CfnReceiptRule.StopActionProperty(
                            scope="scope",
            
                            # the properties below are optional
                            topic_arn="topicArn"
                        ),
                        workmail_action=ses.CfnReceiptRule.WorkmailActionProperty(
                            organization_arn="organizationArn",
            
                            # the properties below are optional
                            topic_arn="topicArn"
                        )
                    )],
                    enabled=False,
                    name="name",
                    recipients=["recipients"],
                    scan_enabled=False,
                    tls_policy="tlsPolicy"
                ),
                rule_set_name="ruleSetName",
            
                # the properties below are optional
                after="after"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e11141ac3c676d1083540c831b2a1ed266163b8787a6e0a1725f0fa366178d2)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
            check_type(argname="argument rule_set_name", value=rule_set_name, expected_type=type_hints["rule_set_name"])
            check_type(argname="argument after", value=after, expected_type=type_hints["after"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule": rule,
            "rule_set_name": rule_set_name,
        }
        if after is not None:
            self._values["after"] = after

    @builtins.property
    def rule(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnReceiptRule.RuleProperty]:
        '''A data structure that contains the specified rule's name, actions, recipients, domains, enabled status, scan status, and TLS policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html#cfn-ses-receiptrule-rule
        '''
        result = self._values.get("rule")
        assert result is not None, "Required property 'rule' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnReceiptRule.RuleProperty], result)

    @builtins.property
    def rule_set_name(self) -> builtins.str:
        '''The name of the rule set where the receipt rule is added.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html#cfn-ses-receiptrule-rulesetname
        '''
        result = self._values.get("rule_set_name")
        assert result is not None, "Required property 'rule_set_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def after(self) -> typing.Optional[builtins.str]:
        '''The name of an existing rule after which the new rule is placed.

        If this parameter is null, the new rule is inserted at the beginning of the rule list.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html#cfn-ses-receiptrule-after
        '''
        result = self._values.get("after")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReceiptRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnReceiptRuleSet(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses.CfnReceiptRuleSet",
):
    '''A CloudFormation ``AWS::SES::ReceiptRuleSet``.

    Creates an empty receipt rule set.

    For information about setting up receipt rule sets, see the `Amazon SES Developer Guide <https://docs.aws.amazon.com/ses/latest/dg/receiving-email-concepts.html#receiving-email-concepts-rules>`_ .

    You can execute this operation no more than once per second.

    :cloudformationResource: AWS::SES::ReceiptRuleSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptruleset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ses as ses
        
        cfn_receipt_rule_set = ses.CfnReceiptRuleSet(self, "MyCfnReceiptRuleSet",
            rule_set_name="ruleSetName"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        rule_set_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::SES::ReceiptRuleSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param rule_set_name: The name of the receipt rule set to reorder.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b60388d81c9ac8b18b3c7ba204e70888d5dac3e36d4ced53f619b4f906a63c4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnReceiptRuleSetProps(rule_set_name=rule_set_name)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34b4d7fbd860d19ad136d51164a501b2c540790d4f40fa5ba8b7e350ed9f119f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0cd5871c5543371d6e49166af6535cd7c03b8592f833ac872d640e0f59127c1e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="ruleSetName")
    def rule_set_name(self) -> typing.Optional[builtins.str]:
        '''The name of the receipt rule set to reorder.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptruleset.html#cfn-ses-receiptruleset-rulesetname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ruleSetName"))

    @rule_set_name.setter
    def rule_set_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1daf1d4b9fdf178960223360ba7544e83ac2a879ed96ad2f411c4acdf6f7c22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleSetName", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.CfnReceiptRuleSetProps",
    jsii_struct_bases=[],
    name_mapping={"rule_set_name": "ruleSetName"},
)
class CfnReceiptRuleSetProps:
    def __init__(self, *, rule_set_name: typing.Optional[builtins.str] = None) -> None:
        '''Properties for defining a ``CfnReceiptRuleSet``.

        :param rule_set_name: The name of the receipt rule set to reorder.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptruleset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            cfn_receipt_rule_set_props = ses.CfnReceiptRuleSetProps(
                rule_set_name="ruleSetName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea57eaf42e698570a3b692f5689ccf537a93cf78b1c13400d6364a205ccc4826)
            check_type(argname="argument rule_set_name", value=rule_set_name, expected_type=type_hints["rule_set_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if rule_set_name is not None:
            self._values["rule_set_name"] = rule_set_name

    @builtins.property
    def rule_set_name(self) -> typing.Optional[builtins.str]:
        '''The name of the receipt rule set to reorder.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptruleset.html#cfn-ses-receiptruleset-rulesetname
        '''
        result = self._values.get("rule_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnReceiptRuleSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnTemplate(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses.CfnTemplate",
):
    '''A CloudFormation ``AWS::SES::Template``.

    Specifies an email template. Email templates enable you to send personalized email to one or more destinations in a single API operation.

    :cloudformationResource: AWS::SES::Template
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-template.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ses as ses
        
        cfn_template = ses.CfnTemplate(self, "MyCfnTemplate",
            template=ses.CfnTemplate.TemplateProperty(
                subject_part="subjectPart",
        
                # the properties below are optional
                html_part="htmlPart",
                template_name="templateName",
                text_part="textPart"
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTemplate.TemplateProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::SES::Template``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param template: The content of the email, composed of a subject line and either an HTML part or a text-only part.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3a4f7388ccce3e291d0c0c559d8a920274ba31fd8e65d0d88c4ea7631e6ffd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTemplateProps(template=template)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b109e5f165d7688120de74e50ee871dd73322f6fd5168ab015b1839e89bc57f9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__40a0f178f4ce74b5f638fcd9f6a35916e7ae6b9c57df03304ae5563b25740c69)
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
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="template")
    def template(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTemplate.TemplateProperty"]]:
        '''The content of the email, composed of a subject line and either an HTML part or a text-only part.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-template.html#cfn-ses-template-template
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTemplate.TemplateProperty"]], jsii.get(self, "template"))

    @template.setter
    def template(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTemplate.TemplateProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__00a00804b717b4b2c5a4d93aba12c147de4cc82fdde21bd37fa92286baed0578)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "template", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnTemplate.TemplateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "subject_part": "subjectPart",
            "html_part": "htmlPart",
            "template_name": "templateName",
            "text_part": "textPart",
        },
    )
    class TemplateProperty:
        def __init__(
            self,
            *,
            subject_part: builtins.str,
            html_part: typing.Optional[builtins.str] = None,
            template_name: typing.Optional[builtins.str] = None,
            text_part: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The content of the email, composed of a subject line and either an HTML part or a text-only part.

            :param subject_part: The subject line of the email.
            :param html_part: The HTML body of the email.
            :param template_name: The name of the template.
            :param text_part: The email body that is visible to recipients whose email clients do not display HTML content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-template-template.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                template_property = ses.CfnTemplate.TemplateProperty(
                    subject_part="subjectPart",
                
                    # the properties below are optional
                    html_part="htmlPart",
                    template_name="templateName",
                    text_part="textPart"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__522c0fb2f6ff5ffc3f6b2d8d7b1864301ce56b2b85274e34956f81acb7d7b591)
                check_type(argname="argument subject_part", value=subject_part, expected_type=type_hints["subject_part"])
                check_type(argname="argument html_part", value=html_part, expected_type=type_hints["html_part"])
                check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
                check_type(argname="argument text_part", value=text_part, expected_type=type_hints["text_part"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "subject_part": subject_part,
            }
            if html_part is not None:
                self._values["html_part"] = html_part
            if template_name is not None:
                self._values["template_name"] = template_name
            if text_part is not None:
                self._values["text_part"] = text_part

        @builtins.property
        def subject_part(self) -> builtins.str:
            '''The subject line of the email.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-template-template.html#cfn-ses-template-template-subjectpart
            '''
            result = self._values.get("subject_part")
            assert result is not None, "Required property 'subject_part' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def html_part(self) -> typing.Optional[builtins.str]:
            '''The HTML body of the email.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-template-template.html#cfn-ses-template-template-htmlpart
            '''
            result = self._values.get("html_part")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def template_name(self) -> typing.Optional[builtins.str]:
            '''The name of the template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-template-template.html#cfn-ses-template-template-templatename
            '''
            result = self._values.get("template_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def text_part(self) -> typing.Optional[builtins.str]:
            '''The email body that is visible to recipients whose email clients do not display HTML content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-template-template.html#cfn-ses-template-template-textpart
            '''
            result = self._values.get("text_part")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TemplateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.CfnTemplateProps",
    jsii_struct_bases=[],
    name_mapping={"template": "template"},
)
class CfnTemplateProps:
    def __init__(
        self,
        *,
        template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTemplate.TemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnTemplate``.

        :param template: The content of the email, composed of a subject line and either an HTML part or a text-only part.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-template.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            cfn_template_props = ses.CfnTemplateProps(
                template=ses.CfnTemplate.TemplateProperty(
                    subject_part="subjectPart",
            
                    # the properties below are optional
                    html_part="htmlPart",
                    template_name="templateName",
                    text_part="textPart"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0241297bf0f761e563c87ebe7b83402ee63a9269d5d880d3e49386d678184181)
            check_type(argname="argument template", value=template, expected_type=type_hints["template"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if template is not None:
            self._values["template"] = template

    @builtins.property
    def template(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTemplate.TemplateProperty]]:
        '''The content of the email, composed of a subject line and either an HTML part or a text-only part.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-template.html#cfn-ses-template-template
        '''
        result = self._values.get("template")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTemplate.TemplateProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnVdmAttributes(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses.CfnVdmAttributes",
):
    '''A CloudFormation ``AWS::SES::VdmAttributes``.

    The Virtual Deliverability Manager (VDM) attributes that apply to your Amazon SES account.

    :cloudformationResource: AWS::SES::VdmAttributes
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-vdmattributes.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ses as ses
        
        cfn_vdm_attributes = ses.CfnVdmAttributes(self, "MyCfnVdmAttributes",
            dashboard_attributes=ses.CfnVdmAttributes.DashboardAttributesProperty(
                engagement_metrics="engagementMetrics"
            ),
            guardian_attributes=ses.CfnVdmAttributes.GuardianAttributesProperty(
                optimized_shared_delivery="optimizedSharedDelivery"
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        dashboard_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnVdmAttributes.DashboardAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        guardian_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnVdmAttributes.GuardianAttributesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::SES::VdmAttributes``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param dashboard_attributes: Specifies additional settings for your VDM configuration as applicable to the Dashboard.
        :param guardian_attributes: Specifies additional settings for your VDM configuration as applicable to the Guardian.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__707bc5deeb197b1f1aae5f3d96c5f19ed175c44435c08f11aaa70b33d1975da5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnVdmAttributesProps(
            dashboard_attributes=dashboard_attributes,
            guardian_attributes=guardian_attributes,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb36fd8a1f2b75c804cd7812035b3fa649e82558f02f00585d5198cf4c59cdc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aef819d717ed35f9acf106570bc1a94656e7e2aa226543cdb3e6e3957f5eb12c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrVdmAttributesResourceId")
    def attr_vdm_attributes_resource_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: VdmAttributesResourceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVdmAttributesResourceId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="dashboardAttributes")
    def dashboard_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVdmAttributes.DashboardAttributesProperty"]]:
        '''Specifies additional settings for your VDM configuration as applicable to the Dashboard.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-vdmattributes.html#cfn-ses-vdmattributes-dashboardattributes
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVdmAttributes.DashboardAttributesProperty"]], jsii.get(self, "dashboardAttributes"))

    @dashboard_attributes.setter
    def dashboard_attributes(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVdmAttributes.DashboardAttributesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb94dd05d1a51277a022d21e5d15a42e98ce1be2534cfd0a3b015e3eaebb7f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dashboardAttributes", value)

    @builtins.property
    @jsii.member(jsii_name="guardianAttributes")
    def guardian_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVdmAttributes.GuardianAttributesProperty"]]:
        '''Specifies additional settings for your VDM configuration as applicable to the Guardian.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-vdmattributes.html#cfn-ses-vdmattributes-guardianattributes
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVdmAttributes.GuardianAttributesProperty"]], jsii.get(self, "guardianAttributes"))

    @guardian_attributes.setter
    def guardian_attributes(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnVdmAttributes.GuardianAttributesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f11ad9bebb9eef5ced0eb65c2eab345ea4ca50426f1900d2d6dffd2d03cfffd3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "guardianAttributes", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnVdmAttributes.DashboardAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"engagement_metrics": "engagementMetrics"},
    )
    class DashboardAttributesProperty:
        def __init__(
            self,
            *,
            engagement_metrics: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings for your VDM configuration as applicable to the Dashboard.

            :param engagement_metrics: Specifies the status of your VDM engagement metrics collection. Can be one of the following:. - ``ENABLED`` – Amazon SES enables engagement metrics for your account. - ``DISABLED`` – Amazon SES disables engagement metrics for your account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-vdmattributes-dashboardattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                dashboard_attributes_property = ses.CfnVdmAttributes.DashboardAttributesProperty(
                    engagement_metrics="engagementMetrics"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__df5ae1a6abb8489623c92ecdaccd214bfb56d0c6a2d87c7b5063e5a9ca52a346)
                check_type(argname="argument engagement_metrics", value=engagement_metrics, expected_type=type_hints["engagement_metrics"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if engagement_metrics is not None:
                self._values["engagement_metrics"] = engagement_metrics

        @builtins.property
        def engagement_metrics(self) -> typing.Optional[builtins.str]:
            '''Specifies the status of your VDM engagement metrics collection. Can be one of the following:.

            - ``ENABLED`` – Amazon SES enables engagement metrics for your account.
            - ``DISABLED`` – Amazon SES disables engagement metrics for your account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-vdmattributes-dashboardattributes.html#cfn-ses-vdmattributes-dashboardattributes-engagementmetrics
            '''
            result = self._values.get("engagement_metrics")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DashboardAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ses.CfnVdmAttributes.GuardianAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={"optimized_shared_delivery": "optimizedSharedDelivery"},
    )
    class GuardianAttributesProperty:
        def __init__(
            self,
            *,
            optimized_shared_delivery: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Settings for your VDM configuration as applicable to the Guardian.

            :param optimized_shared_delivery: Specifies the status of your VDM optimized shared delivery. Can be one of the following:. - ``ENABLED`` – Amazon SES enables optimized shared delivery for your account. - ``DISABLED`` – Amazon SES disables optimized shared delivery for your account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-vdmattributes-guardianattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ses as ses
                
                guardian_attributes_property = ses.CfnVdmAttributes.GuardianAttributesProperty(
                    optimized_shared_delivery="optimizedSharedDelivery"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee246be618e93926f991c6ddc0764630f78726234365bcd4a40e10efc63abf2c)
                check_type(argname="argument optimized_shared_delivery", value=optimized_shared_delivery, expected_type=type_hints["optimized_shared_delivery"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if optimized_shared_delivery is not None:
                self._values["optimized_shared_delivery"] = optimized_shared_delivery

        @builtins.property
        def optimized_shared_delivery(self) -> typing.Optional[builtins.str]:
            '''Specifies the status of your VDM optimized shared delivery. Can be one of the following:.

            - ``ENABLED`` – Amazon SES enables optimized shared delivery for your account.
            - ``DISABLED`` – Amazon SES disables optimized shared delivery for your account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-vdmattributes-guardianattributes.html#cfn-ses-vdmattributes-guardianattributes-optimizedshareddelivery
            '''
            result = self._values.get("optimized_shared_delivery")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "GuardianAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.CfnVdmAttributesProps",
    jsii_struct_bases=[],
    name_mapping={
        "dashboard_attributes": "dashboardAttributes",
        "guardian_attributes": "guardianAttributes",
    },
)
class CfnVdmAttributesProps:
    def __init__(
        self,
        *,
        dashboard_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVdmAttributes.DashboardAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        guardian_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVdmAttributes.GuardianAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnVdmAttributes``.

        :param dashboard_attributes: Specifies additional settings for your VDM configuration as applicable to the Dashboard.
        :param guardian_attributes: Specifies additional settings for your VDM configuration as applicable to the Guardian.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-vdmattributes.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            cfn_vdm_attributes_props = ses.CfnVdmAttributesProps(
                dashboard_attributes=ses.CfnVdmAttributes.DashboardAttributesProperty(
                    engagement_metrics="engagementMetrics"
                ),
                guardian_attributes=ses.CfnVdmAttributes.GuardianAttributesProperty(
                    optimized_shared_delivery="optimizedSharedDelivery"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fd73f238043bea9c9e6be5f4f5b95e2251356dbfda24e734f8faccb01ff113b)
            check_type(argname="argument dashboard_attributes", value=dashboard_attributes, expected_type=type_hints["dashboard_attributes"])
            check_type(argname="argument guardian_attributes", value=guardian_attributes, expected_type=type_hints["guardian_attributes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dashboard_attributes is not None:
            self._values["dashboard_attributes"] = dashboard_attributes
        if guardian_attributes is not None:
            self._values["guardian_attributes"] = guardian_attributes

    @builtins.property
    def dashboard_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVdmAttributes.DashboardAttributesProperty]]:
        '''Specifies additional settings for your VDM configuration as applicable to the Dashboard.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-vdmattributes.html#cfn-ses-vdmattributes-dashboardattributes
        '''
        result = self._values.get("dashboard_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVdmAttributes.DashboardAttributesProperty]], result)

    @builtins.property
    def guardian_attributes(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVdmAttributes.GuardianAttributesProperty]]:
        '''Specifies additional settings for your VDM configuration as applicable to the Guardian.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-vdmattributes.html#cfn-ses-vdmattributes-guardianattributes
        '''
        result = self._values.get("guardian_attributes")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVdmAttributes.GuardianAttributesProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVdmAttributesProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DropSpamReceiptRule(
    _aws_cdk_core_f4b25747.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses.DropSpamReceiptRule",
):
    '''A rule added at the top of the rule set to drop spam/virus.

    :see: https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-lambda-example-functions.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ses as ses
        
        # receipt_rule: ses.ReceiptRule
        # receipt_rule_action: ses.IReceiptRuleAction
        # receipt_rule_set: ses.ReceiptRuleSet
        
        drop_spam_receipt_rule = ses.DropSpamReceiptRule(self, "MyDropSpamReceiptRule",
            rule_set=receipt_rule_set,
        
            # the properties below are optional
            actions=[receipt_rule_action],
            after=receipt_rule,
            enabled=False,
            receipt_rule_name="receiptRuleName",
            recipients=["recipients"],
            scan_enabled=False,
            tls_policy=ses.TlsPolicy.OPTIONAL
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        rule_set: "IReceiptRuleSet",
        actions: typing.Optional[typing.Sequence["IReceiptRuleAction"]] = None,
        after: typing.Optional["IReceiptRule"] = None,
        enabled: typing.Optional[builtins.bool] = None,
        receipt_rule_name: typing.Optional[builtins.str] = None,
        recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
        scan_enabled: typing.Optional[builtins.bool] = None,
        tls_policy: typing.Optional["TlsPolicy"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param rule_set: The name of the rule set that the receipt rule will be added to.
        :param actions: An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule. Default: - No actions.
        :param after: An existing rule after which the new rule will be placed. Default: - The new rule is inserted at the beginning of the rule list.
        :param enabled: Whether the rule is active. Default: true
        :param receipt_rule_name: The name for the rule. Default: - A CloudFormation generated name.
        :param recipients: The recipient domains and email addresses that the receipt rule applies to. Default: - Match all recipients under all verified domains.
        :param scan_enabled: Whether to scan for spam and viruses. Default: false
        :param tls_policy: Whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS). Default: - Optional which will not check for TLS.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f5ee6a4101857bbf89bdd19f4a458990d101d06b7d375ba27e1402a60ab1467)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DropSpamReceiptRuleProps(
            rule_set=rule_set,
            actions=actions,
            after=after,
            enabled=enabled,
            receipt_rule_name=receipt_rule_name,
            recipients=recipients,
            scan_enabled=scan_enabled,
            tls_policy=tls_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "ReceiptRule":
        return typing.cast("ReceiptRule", jsii.get(self, "rule"))


@jsii.interface(jsii_type="@aws-cdk/aws-ses.IReceiptRule")
class IReceiptRule(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''A receipt rule.'''

    @builtins.property
    @jsii.member(jsii_name="receiptRuleName")
    def receipt_rule_name(self) -> builtins.str:
        '''The name of the receipt rule.

        :attribute: true
        '''
        ...


class _IReceiptRuleProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''A receipt rule.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ses.IReceiptRule"

    @builtins.property
    @jsii.member(jsii_name="receiptRuleName")
    def receipt_rule_name(self) -> builtins.str:
        '''The name of the receipt rule.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "receiptRuleName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IReceiptRule).__jsii_proxy_class__ = lambda : _IReceiptRuleProxy


@jsii.interface(jsii_type="@aws-cdk/aws-ses.IReceiptRuleAction")
class IReceiptRuleAction(typing_extensions.Protocol):
    '''An abstract action for a receipt rule.'''

    @jsii.member(jsii_name="bind")
    def bind(self, receipt_rule: IReceiptRule) -> "ReceiptRuleActionConfig":
        '''Returns the receipt rule action specification.

        :param receipt_rule: -
        '''
        ...


class _IReceiptRuleActionProxy:
    '''An abstract action for a receipt rule.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ses.IReceiptRuleAction"

    @jsii.member(jsii_name="bind")
    def bind(self, receipt_rule: IReceiptRule) -> "ReceiptRuleActionConfig":
        '''Returns the receipt rule action specification.

        :param receipt_rule: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62cdc71a3506ecb7cb76a11a036a2de86f68b6dc6cbdab946396888a9353d6e8)
            check_type(argname="argument receipt_rule", value=receipt_rule, expected_type=type_hints["receipt_rule"])
        return typing.cast("ReceiptRuleActionConfig", jsii.invoke(self, "bind", [receipt_rule]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IReceiptRuleAction).__jsii_proxy_class__ = lambda : _IReceiptRuleActionProxy


@jsii.interface(jsii_type="@aws-cdk/aws-ses.IReceiptRuleSet")
class IReceiptRuleSet(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''A receipt rule set.'''

    @builtins.property
    @jsii.member(jsii_name="receiptRuleSetName")
    def receipt_rule_set_name(self) -> builtins.str:
        '''The receipt rule set name.

        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addRule")
    def add_rule(
        self,
        id: builtins.str,
        *,
        actions: typing.Optional[typing.Sequence[IReceiptRuleAction]] = None,
        after: typing.Optional[IReceiptRule] = None,
        enabled: typing.Optional[builtins.bool] = None,
        receipt_rule_name: typing.Optional[builtins.str] = None,
        recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
        scan_enabled: typing.Optional[builtins.bool] = None,
        tls_policy: typing.Optional["TlsPolicy"] = None,
    ) -> "ReceiptRule":
        '''Adds a new receipt rule in this rule set.

        The new rule is added after
        the last added rule unless ``after`` is specified.

        :param id: -
        :param actions: An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule. Default: - No actions.
        :param after: An existing rule after which the new rule will be placed. Default: - The new rule is inserted at the beginning of the rule list.
        :param enabled: Whether the rule is active. Default: true
        :param receipt_rule_name: The name for the rule. Default: - A CloudFormation generated name.
        :param recipients: The recipient domains and email addresses that the receipt rule applies to. Default: - Match all recipients under all verified domains.
        :param scan_enabled: Whether to scan for spam and viruses. Default: false
        :param tls_policy: Whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS). Default: - Optional which will not check for TLS.
        '''
        ...


class _IReceiptRuleSetProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''A receipt rule set.'''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ses.IReceiptRuleSet"

    @builtins.property
    @jsii.member(jsii_name="receiptRuleSetName")
    def receipt_rule_set_name(self) -> builtins.str:
        '''The receipt rule set name.

        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "receiptRuleSetName"))

    @jsii.member(jsii_name="addRule")
    def add_rule(
        self,
        id: builtins.str,
        *,
        actions: typing.Optional[typing.Sequence[IReceiptRuleAction]] = None,
        after: typing.Optional[IReceiptRule] = None,
        enabled: typing.Optional[builtins.bool] = None,
        receipt_rule_name: typing.Optional[builtins.str] = None,
        recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
        scan_enabled: typing.Optional[builtins.bool] = None,
        tls_policy: typing.Optional["TlsPolicy"] = None,
    ) -> "ReceiptRule":
        '''Adds a new receipt rule in this rule set.

        The new rule is added after
        the last added rule unless ``after`` is specified.

        :param id: -
        :param actions: An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule. Default: - No actions.
        :param after: An existing rule after which the new rule will be placed. Default: - The new rule is inserted at the beginning of the rule list.
        :param enabled: Whether the rule is active. Default: true
        :param receipt_rule_name: The name for the rule. Default: - A CloudFormation generated name.
        :param recipients: The recipient domains and email addresses that the receipt rule applies to. Default: - Match all recipients under all verified domains.
        :param scan_enabled: Whether to scan for spam and viruses. Default: false
        :param tls_policy: Whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS). Default: - Optional which will not check for TLS.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b6eff382a474c81b9a627d228768afa664eaf696238bc60888b8b50abd7bc45)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = ReceiptRuleOptions(
            actions=actions,
            after=after,
            enabled=enabled,
            receipt_rule_name=receipt_rule_name,
            recipients=recipients,
            scan_enabled=scan_enabled,
            tls_policy=tls_policy,
        )

        return typing.cast("ReceiptRule", jsii.invoke(self, "addRule", [id, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IReceiptRuleSet).__jsii_proxy_class__ = lambda : _IReceiptRuleSetProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.LambdaActionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "function_arn": "functionArn",
        "invocation_type": "invocationType",
        "topic_arn": "topicArn",
    },
)
class LambdaActionConfig:
    def __init__(
        self,
        *,
        function_arn: builtins.str,
        invocation_type: typing.Optional[builtins.str] = None,
        topic_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''LambdaAction configuration.

        :param function_arn: The Amazon Resource Name (ARN) of the AWS Lambda function.
        :param invocation_type: The invocation type of the AWS Lambda function. Default: 'Event'
        :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the Lambda action is executed. Default: - No notification is sent to SNS.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            lambda_action_config = ses.LambdaActionConfig(
                function_arn="functionArn",
            
                # the properties below are optional
                invocation_type="invocationType",
                topic_arn="topicArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__788da92ccb3c920ddd9805afa846fdbb5b00ab9a2dd073950a7661d3c4b06ebb)
            check_type(argname="argument function_arn", value=function_arn, expected_type=type_hints["function_arn"])
            check_type(argname="argument invocation_type", value=invocation_type, expected_type=type_hints["invocation_type"])
            check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "function_arn": function_arn,
        }
        if invocation_type is not None:
            self._values["invocation_type"] = invocation_type
        if topic_arn is not None:
            self._values["topic_arn"] = topic_arn

    @builtins.property
    def function_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the AWS Lambda function.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-lambdaaction.html#cfn-ses-receiptrule-lambdaaction-functionarn
        '''
        result = self._values.get("function_arn")
        assert result is not None, "Required property 'function_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def invocation_type(self) -> typing.Optional[builtins.str]:
        '''The invocation type of the AWS Lambda function.

        :default: 'Event'

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-lambdaaction.html#cfn-ses-receiptrule-lambdaaction-invocationtype
        '''
        result = self._values.get("invocation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the Lambda action is executed.

        :default: - No notification is sent to SNS.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-lambdaaction.html#cfn-ses-receiptrule-lambdaaction-topicarn
        '''
        result = self._values.get("topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LambdaActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ReceiptFilter(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses.ReceiptFilter",
):
    '''A receipt filter.

    When instantiated without props, it creates a
    block all receipt filter.

    :exampleMetadata: infused

    Example::

        ses.ReceiptFilter(self, "Filter",
            ip="1.2.3.4/16"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        ip: typing.Optional[builtins.str] = None,
        policy: typing.Optional["ReceiptFilterPolicy"] = None,
        receipt_filter_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ip: The ip address or range to filter. Default: 0.0.0.0/0
        :param policy: The policy for the filter. Default: Block
        :param receipt_filter_name: The name for the receipt filter. Default: a CloudFormation generated name
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f69afaebba485366a9d84283d36b4483eb2c5b1349288debba873a1bed0000c0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ReceiptFilterProps(
            ip=ip, policy=policy, receipt_filter_name=receipt_filter_name
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.enum(jsii_type="@aws-cdk/aws-ses.ReceiptFilterPolicy")
class ReceiptFilterPolicy(enum.Enum):
    '''The policy for the receipt filter.'''

    ALLOW = "ALLOW"
    '''Allow the ip address or range.'''
    BLOCK = "BLOCK"
    '''Block the ip address or range.'''


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.ReceiptFilterProps",
    jsii_struct_bases=[],
    name_mapping={
        "ip": "ip",
        "policy": "policy",
        "receipt_filter_name": "receiptFilterName",
    },
)
class ReceiptFilterProps:
    def __init__(
        self,
        *,
        ip: typing.Optional[builtins.str] = None,
        policy: typing.Optional[ReceiptFilterPolicy] = None,
        receipt_filter_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Construction properties for a ReceiptFilter.

        :param ip: The ip address or range to filter. Default: 0.0.0.0/0
        :param policy: The policy for the filter. Default: Block
        :param receipt_filter_name: The name for the receipt filter. Default: a CloudFormation generated name

        :exampleMetadata: infused

        Example::

            ses.ReceiptFilter(self, "Filter",
                ip="1.2.3.4/16"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c4332f9b243b79549c5166db9dc6b46b79fd2b1392d30d9a4c2a6894e618ab5)
            check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument receipt_filter_name", value=receipt_filter_name, expected_type=type_hints["receipt_filter_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if ip is not None:
            self._values["ip"] = ip
        if policy is not None:
            self._values["policy"] = policy
        if receipt_filter_name is not None:
            self._values["receipt_filter_name"] = receipt_filter_name

    @builtins.property
    def ip(self) -> typing.Optional[builtins.str]:
        '''The ip address or range to filter.

        :default: 0.0.0.0/0
        '''
        result = self._values.get("ip")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy(self) -> typing.Optional[ReceiptFilterPolicy]:
        '''The policy for the filter.

        :default: Block
        '''
        result = self._values.get("policy")
        return typing.cast(typing.Optional[ReceiptFilterPolicy], result)

    @builtins.property
    def receipt_filter_name(self) -> typing.Optional[builtins.str]:
        '''The name for the receipt filter.

        :default: a CloudFormation generated name
        '''
        result = self._values.get("receipt_filter_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReceiptFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IReceiptRule)
class ReceiptRule(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses.ReceiptRule",
):
    '''A new receipt rule.

    :exampleMetadata: infused

    Example::

        rule_set = ses.ReceiptRuleSet(self, "RuleSet")
        
        aws_rule = rule_set.add_rule("Aws",
            recipients=["aws.com"]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        rule_set: IReceiptRuleSet,
        actions: typing.Optional[typing.Sequence[IReceiptRuleAction]] = None,
        after: typing.Optional[IReceiptRule] = None,
        enabled: typing.Optional[builtins.bool] = None,
        receipt_rule_name: typing.Optional[builtins.str] = None,
        recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
        scan_enabled: typing.Optional[builtins.bool] = None,
        tls_policy: typing.Optional["TlsPolicy"] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param rule_set: The name of the rule set that the receipt rule will be added to.
        :param actions: An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule. Default: - No actions.
        :param after: An existing rule after which the new rule will be placed. Default: - The new rule is inserted at the beginning of the rule list.
        :param enabled: Whether the rule is active. Default: true
        :param receipt_rule_name: The name for the rule. Default: - A CloudFormation generated name.
        :param recipients: The recipient domains and email addresses that the receipt rule applies to. Default: - Match all recipients under all verified domains.
        :param scan_enabled: Whether to scan for spam and viruses. Default: false
        :param tls_policy: Whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS). Default: - Optional which will not check for TLS.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f09fc324eb67895ced753f10973ac3d15c83cdc8fa4982d3f930362a7d78eb22)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ReceiptRuleProps(
            rule_set=rule_set,
            actions=actions,
            after=after,
            enabled=enabled,
            receipt_rule_name=receipt_rule_name,
            recipients=recipients,
            scan_enabled=scan_enabled,
            tls_policy=tls_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromReceiptRuleName")
    @builtins.classmethod
    def from_receipt_rule_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        receipt_rule_name: builtins.str,
    ) -> IReceiptRule:
        '''
        :param scope: -
        :param id: -
        :param receipt_rule_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a489f8830d33373a4a4eee8722cc60408037ac38edb882ee2702b8e29af4ecb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument receipt_rule_name", value=receipt_rule_name, expected_type=type_hints["receipt_rule_name"])
        return typing.cast(IReceiptRule, jsii.sinvoke(cls, "fromReceiptRuleName", [scope, id, receipt_rule_name]))

    @jsii.member(jsii_name="addAction")
    def add_action(self, action: IReceiptRuleAction) -> None:
        '''Adds an action to this receipt rule.

        :param action: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b402316972bc07642c4a9948941e066d7bf61cfa2423303457530278f6924e1)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
        return typing.cast(None, jsii.invoke(self, "addAction", [action]))

    @builtins.property
    @jsii.member(jsii_name="receiptRuleName")
    def receipt_rule_name(self) -> builtins.str:
        '''The name of the receipt rule.'''
        return typing.cast(builtins.str, jsii.get(self, "receiptRuleName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.ReceiptRuleActionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "add_header_action": "addHeaderAction",
        "bounce_action": "bounceAction",
        "lambda_action": "lambdaAction",
        "s3_action": "s3Action",
        "sns_action": "snsAction",
        "stop_action": "stopAction",
        "workmail_action": "workmailAction",
    },
)
class ReceiptRuleActionConfig:
    def __init__(
        self,
        *,
        add_header_action: typing.Optional[typing.Union[AddHeaderActionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        bounce_action: typing.Optional[typing.Union[BounceActionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        lambda_action: typing.Optional[typing.Union[LambdaActionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
        s3_action: typing.Optional[typing.Union["S3ActionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        sns_action: typing.Optional[typing.Union["SNSActionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        stop_action: typing.Optional[typing.Union["StopActionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
        workmail_action: typing.Optional[typing.Union["WorkmailActionConfig", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''Properties for a receipt rule action.

        :param add_header_action: Adds a header to the received email.
        :param bounce_action: Rejects the received email by returning a bounce response to the sender and, optionally, publishes a notification to Amazon SNS.
        :param lambda_action: Calls an AWS Lambda function, and optionally, publishes a notification to Amazon SNS.
        :param s3_action: Saves the received message to an Amazon S3 bucket and, optionally, publishes a notification to Amazon SNS.
        :param sns_action: Publishes the email content within a notification to Amazon SNS.
        :param stop_action: Terminates the evaluation of the receipt rule set and optionally publishes a notification to Amazon SNS.
        :param workmail_action: Calls Amazon WorkMail and, optionally, publishes a notification to Amazon SNS.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            receipt_rule_action_config = ses.ReceiptRuleActionConfig(
                add_header_action=ses.AddHeaderActionConfig(
                    header_name="headerName",
                    header_value="headerValue"
                ),
                bounce_action=ses.BounceActionConfig(
                    message="message",
                    sender="sender",
                    smtp_reply_code="smtpReplyCode",
            
                    # the properties below are optional
                    status_code="statusCode",
                    topic_arn="topicArn"
                ),
                lambda_action=ses.LambdaActionConfig(
                    function_arn="functionArn",
            
                    # the properties below are optional
                    invocation_type="invocationType",
                    topic_arn="topicArn"
                ),
                s3_action=ses.S3ActionConfig(
                    bucket_name="bucketName",
            
                    # the properties below are optional
                    kms_key_arn="kmsKeyArn",
                    object_key_prefix="objectKeyPrefix",
                    topic_arn="topicArn"
                ),
                sns_action=ses.SNSActionConfig(
                    encoding="encoding",
                    topic_arn="topicArn"
                ),
                stop_action=ses.StopActionConfig(
                    scope="scope",
            
                    # the properties below are optional
                    topic_arn="topicArn"
                ),
                workmail_action=ses.WorkmailActionConfig(
                    organization_arn="organizationArn",
            
                    # the properties below are optional
                    topic_arn="topicArn"
                )
            )
        '''
        if isinstance(add_header_action, dict):
            add_header_action = AddHeaderActionConfig(**add_header_action)
        if isinstance(bounce_action, dict):
            bounce_action = BounceActionConfig(**bounce_action)
        if isinstance(lambda_action, dict):
            lambda_action = LambdaActionConfig(**lambda_action)
        if isinstance(s3_action, dict):
            s3_action = S3ActionConfig(**s3_action)
        if isinstance(sns_action, dict):
            sns_action = SNSActionConfig(**sns_action)
        if isinstance(stop_action, dict):
            stop_action = StopActionConfig(**stop_action)
        if isinstance(workmail_action, dict):
            workmail_action = WorkmailActionConfig(**workmail_action)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4129e43f7dd2d7df99dcce640a8dc8554a0b5229fafe7d47439e3664dd8d7d1)
            check_type(argname="argument add_header_action", value=add_header_action, expected_type=type_hints["add_header_action"])
            check_type(argname="argument bounce_action", value=bounce_action, expected_type=type_hints["bounce_action"])
            check_type(argname="argument lambda_action", value=lambda_action, expected_type=type_hints["lambda_action"])
            check_type(argname="argument s3_action", value=s3_action, expected_type=type_hints["s3_action"])
            check_type(argname="argument sns_action", value=sns_action, expected_type=type_hints["sns_action"])
            check_type(argname="argument stop_action", value=stop_action, expected_type=type_hints["stop_action"])
            check_type(argname="argument workmail_action", value=workmail_action, expected_type=type_hints["workmail_action"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_header_action is not None:
            self._values["add_header_action"] = add_header_action
        if bounce_action is not None:
            self._values["bounce_action"] = bounce_action
        if lambda_action is not None:
            self._values["lambda_action"] = lambda_action
        if s3_action is not None:
            self._values["s3_action"] = s3_action
        if sns_action is not None:
            self._values["sns_action"] = sns_action
        if stop_action is not None:
            self._values["stop_action"] = stop_action
        if workmail_action is not None:
            self._values["workmail_action"] = workmail_action

    @builtins.property
    def add_header_action(self) -> typing.Optional[AddHeaderActionConfig]:
        '''Adds a header to the received email.'''
        result = self._values.get("add_header_action")
        return typing.cast(typing.Optional[AddHeaderActionConfig], result)

    @builtins.property
    def bounce_action(self) -> typing.Optional[BounceActionConfig]:
        '''Rejects the received email by returning a bounce response to the sender and, optionally, publishes a notification to Amazon SNS.'''
        result = self._values.get("bounce_action")
        return typing.cast(typing.Optional[BounceActionConfig], result)

    @builtins.property
    def lambda_action(self) -> typing.Optional[LambdaActionConfig]:
        '''Calls an AWS Lambda function, and optionally, publishes a notification to Amazon SNS.'''
        result = self._values.get("lambda_action")
        return typing.cast(typing.Optional[LambdaActionConfig], result)

    @builtins.property
    def s3_action(self) -> typing.Optional["S3ActionConfig"]:
        '''Saves the received message to an Amazon S3 bucket and, optionally, publishes a notification to Amazon SNS.'''
        result = self._values.get("s3_action")
        return typing.cast(typing.Optional["S3ActionConfig"], result)

    @builtins.property
    def sns_action(self) -> typing.Optional["SNSActionConfig"]:
        '''Publishes the email content within a notification to Amazon SNS.'''
        result = self._values.get("sns_action")
        return typing.cast(typing.Optional["SNSActionConfig"], result)

    @builtins.property
    def stop_action(self) -> typing.Optional["StopActionConfig"]:
        '''Terminates the evaluation of the receipt rule set and optionally publishes a notification to Amazon SNS.'''
        result = self._values.get("stop_action")
        return typing.cast(typing.Optional["StopActionConfig"], result)

    @builtins.property
    def workmail_action(self) -> typing.Optional["WorkmailActionConfig"]:
        '''Calls Amazon WorkMail and, optionally, publishes a notification to Amazon SNS.'''
        result = self._values.get("workmail_action")
        return typing.cast(typing.Optional["WorkmailActionConfig"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReceiptRuleActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.ReceiptRuleOptions",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "after": "after",
        "enabled": "enabled",
        "receipt_rule_name": "receiptRuleName",
        "recipients": "recipients",
        "scan_enabled": "scanEnabled",
        "tls_policy": "tlsPolicy",
    },
)
class ReceiptRuleOptions:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[IReceiptRuleAction]] = None,
        after: typing.Optional[IReceiptRule] = None,
        enabled: typing.Optional[builtins.bool] = None,
        receipt_rule_name: typing.Optional[builtins.str] = None,
        recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
        scan_enabled: typing.Optional[builtins.bool] = None,
        tls_policy: typing.Optional["TlsPolicy"] = None,
    ) -> None:
        '''Options to add a receipt rule to a receipt rule set.

        :param actions: An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule. Default: - No actions.
        :param after: An existing rule after which the new rule will be placed. Default: - The new rule is inserted at the beginning of the rule list.
        :param enabled: Whether the rule is active. Default: true
        :param receipt_rule_name: The name for the rule. Default: - A CloudFormation generated name.
        :param recipients: The recipient domains and email addresses that the receipt rule applies to. Default: - Match all recipients under all verified domains.
        :param scan_enabled: Whether to scan for spam and viruses. Default: false
        :param tls_policy: Whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS). Default: - Optional which will not check for TLS.

        :exampleMetadata: infused

        Example::

            rule_set = ses.ReceiptRuleSet(self, "RuleSet")
            
            aws_rule = rule_set.add_rule("Aws",
                recipients=["aws.com"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66eea3ac6fc7a11054cff3fa7a66f99ea44e5e1e4d3ef7a5712ba6dfc81d6faf)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument after", value=after, expected_type=type_hints["after"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument receipt_rule_name", value=receipt_rule_name, expected_type=type_hints["receipt_rule_name"])
            check_type(argname="argument recipients", value=recipients, expected_type=type_hints["recipients"])
            check_type(argname="argument scan_enabled", value=scan_enabled, expected_type=type_hints["scan_enabled"])
            check_type(argname="argument tls_policy", value=tls_policy, expected_type=type_hints["tls_policy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if after is not None:
            self._values["after"] = after
        if enabled is not None:
            self._values["enabled"] = enabled
        if receipt_rule_name is not None:
            self._values["receipt_rule_name"] = receipt_rule_name
        if recipients is not None:
            self._values["recipients"] = recipients
        if scan_enabled is not None:
            self._values["scan_enabled"] = scan_enabled
        if tls_policy is not None:
            self._values["tls_policy"] = tls_policy

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[IReceiptRuleAction]]:
        '''An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule.

        :default: - No actions.
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[IReceiptRuleAction]], result)

    @builtins.property
    def after(self) -> typing.Optional[IReceiptRule]:
        '''An existing rule after which the new rule will be placed.

        :default: - The new rule is inserted at the beginning of the rule list.
        '''
        result = self._values.get("after")
        return typing.cast(typing.Optional[IReceiptRule], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Whether the rule is active.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def receipt_rule_name(self) -> typing.Optional[builtins.str]:
        '''The name for the rule.

        :default: - A CloudFormation generated name.
        '''
        result = self._values.get("receipt_rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The recipient domains and email addresses that the receipt rule applies to.

        :default: - Match all recipients under all verified domains.
        '''
        result = self._values.get("recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def scan_enabled(self) -> typing.Optional[builtins.bool]:
        '''Whether to scan for spam and viruses.

        :default: false
        '''
        result = self._values.get("scan_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tls_policy(self) -> typing.Optional["TlsPolicy"]:
        '''Whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS).

        :default: - Optional which will not check for TLS.
        '''
        result = self._values.get("tls_policy")
        return typing.cast(typing.Optional["TlsPolicy"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReceiptRuleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.ReceiptRuleProps",
    jsii_struct_bases=[ReceiptRuleOptions],
    name_mapping={
        "actions": "actions",
        "after": "after",
        "enabled": "enabled",
        "receipt_rule_name": "receiptRuleName",
        "recipients": "recipients",
        "scan_enabled": "scanEnabled",
        "tls_policy": "tlsPolicy",
        "rule_set": "ruleSet",
    },
)
class ReceiptRuleProps(ReceiptRuleOptions):
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[IReceiptRuleAction]] = None,
        after: typing.Optional[IReceiptRule] = None,
        enabled: typing.Optional[builtins.bool] = None,
        receipt_rule_name: typing.Optional[builtins.str] = None,
        recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
        scan_enabled: typing.Optional[builtins.bool] = None,
        tls_policy: typing.Optional["TlsPolicy"] = None,
        rule_set: IReceiptRuleSet,
    ) -> None:
        '''Construction properties for a ReceiptRule.

        :param actions: An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule. Default: - No actions.
        :param after: An existing rule after which the new rule will be placed. Default: - The new rule is inserted at the beginning of the rule list.
        :param enabled: Whether the rule is active. Default: true
        :param receipt_rule_name: The name for the rule. Default: - A CloudFormation generated name.
        :param recipients: The recipient domains and email addresses that the receipt rule applies to. Default: - Match all recipients under all verified domains.
        :param scan_enabled: Whether to scan for spam and viruses. Default: false
        :param tls_policy: Whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS). Default: - Optional which will not check for TLS.
        :param rule_set: The name of the rule set that the receipt rule will be added to.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            # receipt_rule: ses.ReceiptRule
            # receipt_rule_action: ses.IReceiptRuleAction
            # receipt_rule_set: ses.ReceiptRuleSet
            
            receipt_rule_props = ses.ReceiptRuleProps(
                rule_set=receipt_rule_set,
            
                # the properties below are optional
                actions=[receipt_rule_action],
                after=receipt_rule,
                enabled=False,
                receipt_rule_name="receiptRuleName",
                recipients=["recipients"],
                scan_enabled=False,
                tls_policy=ses.TlsPolicy.OPTIONAL
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22331a230e5d3dcb99e74c746c989f50d4a3e405e65ddccedce57fa6f16a9363)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument after", value=after, expected_type=type_hints["after"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument receipt_rule_name", value=receipt_rule_name, expected_type=type_hints["receipt_rule_name"])
            check_type(argname="argument recipients", value=recipients, expected_type=type_hints["recipients"])
            check_type(argname="argument scan_enabled", value=scan_enabled, expected_type=type_hints["scan_enabled"])
            check_type(argname="argument tls_policy", value=tls_policy, expected_type=type_hints["tls_policy"])
            check_type(argname="argument rule_set", value=rule_set, expected_type=type_hints["rule_set"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_set": rule_set,
        }
        if actions is not None:
            self._values["actions"] = actions
        if after is not None:
            self._values["after"] = after
        if enabled is not None:
            self._values["enabled"] = enabled
        if receipt_rule_name is not None:
            self._values["receipt_rule_name"] = receipt_rule_name
        if recipients is not None:
            self._values["recipients"] = recipients
        if scan_enabled is not None:
            self._values["scan_enabled"] = scan_enabled
        if tls_policy is not None:
            self._values["tls_policy"] = tls_policy

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[IReceiptRuleAction]]:
        '''An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule.

        :default: - No actions.
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[IReceiptRuleAction]], result)

    @builtins.property
    def after(self) -> typing.Optional[IReceiptRule]:
        '''An existing rule after which the new rule will be placed.

        :default: - The new rule is inserted at the beginning of the rule list.
        '''
        result = self._values.get("after")
        return typing.cast(typing.Optional[IReceiptRule], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Whether the rule is active.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def receipt_rule_name(self) -> typing.Optional[builtins.str]:
        '''The name for the rule.

        :default: - A CloudFormation generated name.
        '''
        result = self._values.get("receipt_rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The recipient domains and email addresses that the receipt rule applies to.

        :default: - Match all recipients under all verified domains.
        '''
        result = self._values.get("recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def scan_enabled(self) -> typing.Optional[builtins.bool]:
        '''Whether to scan for spam and viruses.

        :default: false
        '''
        result = self._values.get("scan_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tls_policy(self) -> typing.Optional["TlsPolicy"]:
        '''Whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS).

        :default: - Optional which will not check for TLS.
        '''
        result = self._values.get("tls_policy")
        return typing.cast(typing.Optional["TlsPolicy"], result)

    @builtins.property
    def rule_set(self) -> IReceiptRuleSet:
        '''The name of the rule set that the receipt rule will be added to.'''
        result = self._values.get("rule_set")
        assert result is not None, "Required property 'rule_set' is missing"
        return typing.cast(IReceiptRuleSet, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReceiptRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IReceiptRuleSet)
class ReceiptRuleSet(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses.ReceiptRuleSet",
):
    '''A new receipt rule set.

    :exampleMetadata: infused

    Example::

        rule_set = ses.ReceiptRuleSet(self, "RuleSet")
        
        aws_rule = rule_set.add_rule("Aws",
            recipients=["aws.com"]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        drop_spam: typing.Optional[builtins.bool] = None,
        receipt_rule_set_name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Sequence[typing.Union[ReceiptRuleOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param drop_spam: Whether to add a first rule to stop processing messages that have at least one spam indicator. Default: false
        :param receipt_rule_set_name: The name for the receipt rule set. Default: - A CloudFormation generated name.
        :param rules: The list of rules to add to this rule set. Rules are added in the same order as they appear in the list. Default: - No rules are added to the rule set.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28ad0f3e07f029d665c1c2b58fdb133cd56129cc935855ed630938946830f11b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ReceiptRuleSetProps(
            drop_spam=drop_spam,
            receipt_rule_set_name=receipt_rule_set_name,
            rules=rules,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromReceiptRuleSetName")
    @builtins.classmethod
    def from_receipt_rule_set_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        receipt_rule_set_name: builtins.str,
    ) -> IReceiptRuleSet:
        '''Import an exported receipt rule set.

        :param scope: -
        :param id: -
        :param receipt_rule_set_name: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d32bda755a5c3882e6d40011a51e10aa7c4ab1dbff4de2f5e4f31ad948255af)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument receipt_rule_set_name", value=receipt_rule_set_name, expected_type=type_hints["receipt_rule_set_name"])
        return typing.cast(IReceiptRuleSet, jsii.sinvoke(cls, "fromReceiptRuleSetName", [scope, id, receipt_rule_set_name]))

    @jsii.member(jsii_name="addDropSpamRule")
    def _add_drop_spam_rule(self) -> None:
        '''Adds a drop spam rule.'''
        return typing.cast(None, jsii.invoke(self, "addDropSpamRule", []))

    @jsii.member(jsii_name="addRule")
    def add_rule(
        self,
        id: builtins.str,
        *,
        actions: typing.Optional[typing.Sequence[IReceiptRuleAction]] = None,
        after: typing.Optional[IReceiptRule] = None,
        enabled: typing.Optional[builtins.bool] = None,
        receipt_rule_name: typing.Optional[builtins.str] = None,
        recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
        scan_enabled: typing.Optional[builtins.bool] = None,
        tls_policy: typing.Optional["TlsPolicy"] = None,
    ) -> ReceiptRule:
        '''Adds a new receipt rule in this rule set.

        The new rule is added after
        the last added rule unless ``after`` is specified.

        :param id: -
        :param actions: An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule. Default: - No actions.
        :param after: An existing rule after which the new rule will be placed. Default: - The new rule is inserted at the beginning of the rule list.
        :param enabled: Whether the rule is active. Default: true
        :param receipt_rule_name: The name for the rule. Default: - A CloudFormation generated name.
        :param recipients: The recipient domains and email addresses that the receipt rule applies to. Default: - Match all recipients under all verified domains.
        :param scan_enabled: Whether to scan for spam and viruses. Default: false
        :param tls_policy: Whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS). Default: - Optional which will not check for TLS.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21cca4f2550bc241a4c6b481b1e16fe34cdca13118be943d145899e6902eb815)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = ReceiptRuleOptions(
            actions=actions,
            after=after,
            enabled=enabled,
            receipt_rule_name=receipt_rule_name,
            recipients=recipients,
            scan_enabled=scan_enabled,
            tls_policy=tls_policy,
        )

        return typing.cast(ReceiptRule, jsii.invoke(self, "addRule", [id, options]))

    @builtins.property
    @jsii.member(jsii_name="receiptRuleSetName")
    def receipt_rule_set_name(self) -> builtins.str:
        '''The receipt rule set name.'''
        return typing.cast(builtins.str, jsii.get(self, "receiptRuleSetName"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.ReceiptRuleSetProps",
    jsii_struct_bases=[],
    name_mapping={
        "drop_spam": "dropSpam",
        "receipt_rule_set_name": "receiptRuleSetName",
        "rules": "rules",
    },
)
class ReceiptRuleSetProps:
    def __init__(
        self,
        *,
        drop_spam: typing.Optional[builtins.bool] = None,
        receipt_rule_set_name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Sequence[typing.Union[ReceiptRuleOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Construction properties for a ReceiptRuleSet.

        :param drop_spam: Whether to add a first rule to stop processing messages that have at least one spam indicator. Default: false
        :param receipt_rule_set_name: The name for the receipt rule set. Default: - A CloudFormation generated name.
        :param rules: The list of rules to add to this rule set. Rules are added in the same order as they appear in the list. Default: - No rules are added to the rule set.

        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_s3 as s3
            import aws_cdk.aws_ses_actions as actions
            
            
            bucket = s3.Bucket(self, "Bucket")
            topic = sns.Topic(self, "Topic")
            
            ses.ReceiptRuleSet(self, "RuleSet",
                rules=[ses.ReceiptRuleOptions(
                    recipients=["hello@aws.com"],
                    actions=[
                        actions.AddHeader(
                            name="X-Special-Header",
                            value="aws"
                        ),
                        actions.S3(
                            bucket=bucket,
                            object_key_prefix="emails/",
                            topic=topic
                        )
                    ]
                ), ses.ReceiptRuleOptions(
                    recipients=["aws.com"],
                    actions=[
                        actions.Sns(
                            topic=topic
                        )
                    ]
                )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe60713f6f1db793e4f84c75e3b684d03f32ab586a08d75d38f50abe8d80396e)
            check_type(argname="argument drop_spam", value=drop_spam, expected_type=type_hints["drop_spam"])
            check_type(argname="argument receipt_rule_set_name", value=receipt_rule_set_name, expected_type=type_hints["receipt_rule_set_name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if drop_spam is not None:
            self._values["drop_spam"] = drop_spam
        if receipt_rule_set_name is not None:
            self._values["receipt_rule_set_name"] = receipt_rule_set_name
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def drop_spam(self) -> typing.Optional[builtins.bool]:
        '''Whether to add a first rule to stop processing messages that have at least one spam indicator.

        :default: false
        '''
        result = self._values.get("drop_spam")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def receipt_rule_set_name(self) -> typing.Optional[builtins.str]:
        '''The name for the receipt rule set.

        :default: - A CloudFormation generated name.
        '''
        result = self._values.get("receipt_rule_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.List[ReceiptRuleOptions]]:
        '''The list of rules to add to this rule set.

        Rules are added in the same
        order as they appear in the list.

        :default: - No rules are added to the rule set.
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List[ReceiptRuleOptions]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReceiptRuleSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.S3ActionConfig",
    jsii_struct_bases=[],
    name_mapping={
        "bucket_name": "bucketName",
        "kms_key_arn": "kmsKeyArn",
        "object_key_prefix": "objectKeyPrefix",
        "topic_arn": "topicArn",
    },
)
class S3ActionConfig:
    def __init__(
        self,
        *,
        bucket_name: builtins.str,
        kms_key_arn: typing.Optional[builtins.str] = None,
        object_key_prefix: typing.Optional[builtins.str] = None,
        topic_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''S3Action configuration.

        :param bucket_name: The name of the Amazon S3 bucket that you want to send incoming mail to.
        :param kms_key_arn: The customer master key that Amazon SES should use to encrypt your emails before saving them to the Amazon S3 bucket. Default: - Emails are not encrypted.
        :param object_key_prefix: The key prefix of the Amazon S3 bucket. Default: - No prefix.
        :param topic_arn: The ARN of the Amazon SNS topic to notify when the message is saved to the Amazon S3 bucket. Default: - No notification is sent to SNS.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            s3_action_config = ses.S3ActionConfig(
                bucket_name="bucketName",
            
                # the properties below are optional
                kms_key_arn="kmsKeyArn",
                object_key_prefix="objectKeyPrefix",
                topic_arn="topicArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5346e521fb0405ab945200e222a5586641f5f95495fc17b82c5174bb0640f25d)
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument kms_key_arn", value=kms_key_arn, expected_type=type_hints["kms_key_arn"])
            check_type(argname="argument object_key_prefix", value=object_key_prefix, expected_type=type_hints["object_key_prefix"])
            check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
        }
        if kms_key_arn is not None:
            self._values["kms_key_arn"] = kms_key_arn
        if object_key_prefix is not None:
            self._values["object_key_prefix"] = object_key_prefix
        if topic_arn is not None:
            self._values["topic_arn"] = topic_arn

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''The name of the Amazon S3 bucket that you want to send incoming mail to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html#cfn-ses-receiptrule-s3action-bucketname
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def kms_key_arn(self) -> typing.Optional[builtins.str]:
        '''The customer master key that Amazon SES should use to encrypt your emails before saving them to the Amazon S3 bucket.

        :default: - Emails are not encrypted.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html#cfn-ses-receiptrule-s3action-kmskeyarn
        '''
        result = self._values.get("kms_key_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def object_key_prefix(self) -> typing.Optional[builtins.str]:
        '''The key prefix of the Amazon S3 bucket.

        :default: - No prefix.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html#cfn-ses-receiptrule-s3action-objectkeyprefix
        '''
        result = self._values.get("object_key_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the Amazon SNS topic to notify when the message is saved to the Amazon S3 bucket.

        :default: - No notification is sent to SNS.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html#cfn-ses-receiptrule-s3action-topicarn
        '''
        result = self._values.get("topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3ActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.SNSActionConfig",
    jsii_struct_bases=[],
    name_mapping={"encoding": "encoding", "topic_arn": "topicArn"},
)
class SNSActionConfig:
    def __init__(
        self,
        *,
        encoding: typing.Optional[builtins.str] = None,
        topic_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''SNSAction configuration.

        :param encoding: The encoding to use for the email within the Amazon SNS notification. Default: 'UTF-8'
        :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to notify. Default: - No notification is sent to SNS.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            s_nSAction_config = ses.SNSActionConfig(
                encoding="encoding",
                topic_arn="topicArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88eb53ffdfee3dba7153a2b2cbe2a2b29d2b054f50662db3320156366c6900df)
            check_type(argname="argument encoding", value=encoding, expected_type=type_hints["encoding"])
            check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if encoding is not None:
            self._values["encoding"] = encoding
        if topic_arn is not None:
            self._values["topic_arn"] = topic_arn

    @builtins.property
    def encoding(self) -> typing.Optional[builtins.str]:
        '''The encoding to use for the email within the Amazon SNS notification.

        :default: 'UTF-8'

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-snsaction.html#cfn-ses-receiptrule-snsaction-encoding
        '''
        result = self._values.get("encoding")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon SNS topic to notify.

        :default: - No notification is sent to SNS.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-snsaction.html#cfn-ses-receiptrule-snsaction-topicarn
        '''
        result = self._values.get("topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SNSActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.StopActionConfig",
    jsii_struct_bases=[],
    name_mapping={"scope": "scope", "topic_arn": "topicArn"},
)
class StopActionConfig:
    def __init__(
        self,
        *,
        scope: builtins.str,
        topic_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''StopAction configuration.

        :param scope: The scope of the StopAction. The only acceptable value is RuleSet.
        :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the stop action is taken. Default: - No notification is sent to SNS.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            stop_action_config = ses.StopActionConfig(
                scope="scope",
            
                # the properties below are optional
                topic_arn="topicArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ef8ee892ef97594b95783fa2b84d8c95ab339f9f99ce516b23fbcd69e768a4f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "scope": scope,
        }
        if topic_arn is not None:
            self._values["topic_arn"] = topic_arn

    @builtins.property
    def scope(self) -> builtins.str:
        '''The scope of the StopAction.

        The only acceptable value is RuleSet.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-stopaction.html#cfn-ses-receiptrule-stopaction-scope
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the stop action is taken.

        :default: - No notification is sent to SNS.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-stopaction.html#cfn-ses-receiptrule-stopaction-topicarn
        '''
        result = self._values.get("topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StopActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-ses.TlsPolicy")
class TlsPolicy(enum.Enum):
    '''The type of TLS policy for a receipt rule.'''

    OPTIONAL = "OPTIONAL"
    '''Do not check for TLS.'''
    REQUIRE = "REQUIRE"
    '''Bounce emails that are not received over TLS.'''


class WhiteListReceiptFilter(
    AllowListReceiptFilter,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ses.WhiteListReceiptFilter",
):
    '''(deprecated) An allow list receipt filter.

    :deprecated: use ``AllowListReceiptFilter``

    :stability: deprecated
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ses as ses
        
        white_list_receipt_filter = ses.WhiteListReceiptFilter(self, "MyWhiteListReceiptFilter",
            ips=["ips"]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        ips: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param ips: A list of ip addresses or ranges to allow list.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8cc0d7f732dd0e75362b80532f23b2fd6c2e7239e7ae96db736a87a18648eb2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WhiteListReceiptFilterProps(ips=ips)

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.WhiteListReceiptFilterProps",
    jsii_struct_bases=[AllowListReceiptFilterProps],
    name_mapping={"ips": "ips"},
)
class WhiteListReceiptFilterProps(AllowListReceiptFilterProps):
    def __init__(self, *, ips: typing.Sequence[builtins.str]) -> None:
        '''(deprecated) Construction properties for a WhiteListReceiptFilter.

        :param ips: A list of ip addresses or ranges to allow list.

        :deprecated: use ``AllowListReceiptFilterProps``

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            white_list_receipt_filter_props = ses.WhiteListReceiptFilterProps(
                ips=["ips"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eeae95d61dd573d24fa913d1af465357923652cc571faae61673f0504912a5b)
            check_type(argname="argument ips", value=ips, expected_type=type_hints["ips"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ips": ips,
        }

    @builtins.property
    def ips(self) -> typing.List[builtins.str]:
        '''A list of ip addresses or ranges to allow list.'''
        result = self._values.get("ips")
        assert result is not None, "Required property 'ips' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WhiteListReceiptFilterProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.WorkmailActionConfig",
    jsii_struct_bases=[],
    name_mapping={"organization_arn": "organizationArn", "topic_arn": "topicArn"},
)
class WorkmailActionConfig:
    def __init__(
        self,
        *,
        organization_arn: builtins.str,
        topic_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''WorkmailAction configuration.

        :param organization_arn: The Amazon Resource Name (ARN) of the Amazon WorkMail organization.
        :param topic_arn: The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the WorkMail action is called. Default: - No notification is sent to SNS.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            workmail_action_config = ses.WorkmailActionConfig(
                organization_arn="organizationArn",
            
                # the properties below are optional
                topic_arn="topicArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0362b09858aa19ad4b560eaab9f5f45f016a9fe86b9d22b49aaafd3be97d57e6)
            check_type(argname="argument organization_arn", value=organization_arn, expected_type=type_hints["organization_arn"])
            check_type(argname="argument topic_arn", value=topic_arn, expected_type=type_hints["topic_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "organization_arn": organization_arn,
        }
        if topic_arn is not None:
            self._values["topic_arn"] = topic_arn

    @builtins.property
    def organization_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon WorkMail organization.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-workmailaction.html#cfn-ses-receiptrule-workmailaction-organizationarn
        '''
        result = self._values.get("organization_arn")
        assert result is not None, "Required property 'organization_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def topic_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the Amazon SNS topic to notify when the WorkMail action is called.

        :default: - No notification is sent to SNS.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-workmailaction.html#cfn-ses-receiptrule-workmailaction-topicarn
        '''
        result = self._values.get("topic_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkmailActionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ses.DropSpamReceiptRuleProps",
    jsii_struct_bases=[ReceiptRuleProps],
    name_mapping={
        "actions": "actions",
        "after": "after",
        "enabled": "enabled",
        "receipt_rule_name": "receiptRuleName",
        "recipients": "recipients",
        "scan_enabled": "scanEnabled",
        "tls_policy": "tlsPolicy",
        "rule_set": "ruleSet",
    },
)
class DropSpamReceiptRuleProps(ReceiptRuleProps):
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[IReceiptRuleAction]] = None,
        after: typing.Optional[IReceiptRule] = None,
        enabled: typing.Optional[builtins.bool] = None,
        receipt_rule_name: typing.Optional[builtins.str] = None,
        recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
        scan_enabled: typing.Optional[builtins.bool] = None,
        tls_policy: typing.Optional[TlsPolicy] = None,
        rule_set: IReceiptRuleSet,
    ) -> None:
        '''
        :param actions: An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule. Default: - No actions.
        :param after: An existing rule after which the new rule will be placed. Default: - The new rule is inserted at the beginning of the rule list.
        :param enabled: Whether the rule is active. Default: true
        :param receipt_rule_name: The name for the rule. Default: - A CloudFormation generated name.
        :param recipients: The recipient domains and email addresses that the receipt rule applies to. Default: - Match all recipients under all verified domains.
        :param scan_enabled: Whether to scan for spam and viruses. Default: false
        :param tls_policy: Whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS). Default: - Optional which will not check for TLS.
        :param rule_set: The name of the rule set that the receipt rule will be added to.

        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ses as ses
            
            # receipt_rule: ses.ReceiptRule
            # receipt_rule_action: ses.IReceiptRuleAction
            # receipt_rule_set: ses.ReceiptRuleSet
            
            drop_spam_receipt_rule_props = ses.DropSpamReceiptRuleProps(
                rule_set=receipt_rule_set,
            
                # the properties below are optional
                actions=[receipt_rule_action],
                after=receipt_rule,
                enabled=False,
                receipt_rule_name="receiptRuleName",
                recipients=["recipients"],
                scan_enabled=False,
                tls_policy=ses.TlsPolicy.OPTIONAL
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__040416e5e85b8b6efea40b26f9845395df834451bac0b29f36262918b9e5af97)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument after", value=after, expected_type=type_hints["after"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument receipt_rule_name", value=receipt_rule_name, expected_type=type_hints["receipt_rule_name"])
            check_type(argname="argument recipients", value=recipients, expected_type=type_hints["recipients"])
            check_type(argname="argument scan_enabled", value=scan_enabled, expected_type=type_hints["scan_enabled"])
            check_type(argname="argument tls_policy", value=tls_policy, expected_type=type_hints["tls_policy"])
            check_type(argname="argument rule_set", value=rule_set, expected_type=type_hints["rule_set"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "rule_set": rule_set,
        }
        if actions is not None:
            self._values["actions"] = actions
        if after is not None:
            self._values["after"] = after
        if enabled is not None:
            self._values["enabled"] = enabled
        if receipt_rule_name is not None:
            self._values["receipt_rule_name"] = receipt_rule_name
        if recipients is not None:
            self._values["recipients"] = recipients
        if scan_enabled is not None:
            self._values["scan_enabled"] = scan_enabled
        if tls_policy is not None:
            self._values["tls_policy"] = tls_policy

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[IReceiptRuleAction]]:
        '''An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule.

        :default: - No actions.
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[IReceiptRuleAction]], result)

    @builtins.property
    def after(self) -> typing.Optional[IReceiptRule]:
        '''An existing rule after which the new rule will be placed.

        :default: - The new rule is inserted at the beginning of the rule list.
        '''
        result = self._values.get("after")
        return typing.cast(typing.Optional[IReceiptRule], result)

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''Whether the rule is active.

        :default: true
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def receipt_rule_name(self) -> typing.Optional[builtins.str]:
        '''The name for the rule.

        :default: - A CloudFormation generated name.
        '''
        result = self._values.get("receipt_rule_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recipients(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The recipient domains and email addresses that the receipt rule applies to.

        :default: - Match all recipients under all verified domains.
        '''
        result = self._values.get("recipients")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def scan_enabled(self) -> typing.Optional[builtins.bool]:
        '''Whether to scan for spam and viruses.

        :default: false
        '''
        result = self._values.get("scan_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def tls_policy(self) -> typing.Optional[TlsPolicy]:
        '''Whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS).

        :default: - Optional which will not check for TLS.
        '''
        result = self._values.get("tls_policy")
        return typing.cast(typing.Optional[TlsPolicy], result)

    @builtins.property
    def rule_set(self) -> IReceiptRuleSet:
        '''The name of the rule set that the receipt rule will be added to.'''
        result = self._values.get("rule_set")
        assert result is not None, "Required property 'rule_set' is missing"
        return typing.cast(IReceiptRuleSet, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DropSpamReceiptRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddHeaderActionConfig",
    "AllowListReceiptFilter",
    "AllowListReceiptFilterProps",
    "BounceActionConfig",
    "CfnConfigurationSet",
    "CfnConfigurationSetEventDestination",
    "CfnConfigurationSetEventDestinationProps",
    "CfnConfigurationSetProps",
    "CfnContactList",
    "CfnContactListProps",
    "CfnDedicatedIpPool",
    "CfnDedicatedIpPoolProps",
    "CfnEmailIdentity",
    "CfnEmailIdentityProps",
    "CfnReceiptFilter",
    "CfnReceiptFilterProps",
    "CfnReceiptRule",
    "CfnReceiptRuleProps",
    "CfnReceiptRuleSet",
    "CfnReceiptRuleSetProps",
    "CfnTemplate",
    "CfnTemplateProps",
    "CfnVdmAttributes",
    "CfnVdmAttributesProps",
    "DropSpamReceiptRule",
    "DropSpamReceiptRuleProps",
    "IReceiptRule",
    "IReceiptRuleAction",
    "IReceiptRuleSet",
    "LambdaActionConfig",
    "ReceiptFilter",
    "ReceiptFilterPolicy",
    "ReceiptFilterProps",
    "ReceiptRule",
    "ReceiptRuleActionConfig",
    "ReceiptRuleOptions",
    "ReceiptRuleProps",
    "ReceiptRuleSet",
    "ReceiptRuleSetProps",
    "S3ActionConfig",
    "SNSActionConfig",
    "StopActionConfig",
    "TlsPolicy",
    "WhiteListReceiptFilter",
    "WhiteListReceiptFilterProps",
    "WorkmailActionConfig",
]

publication.publish()

def _typecheckingstub__348a080a2f9682288c131b7b71880fef0517d3ca56a388ed41b5b2343ce2cfc3(
    *,
    header_name: builtins.str,
    header_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__621fd3b2b69149194b2a6bae8af9c37eeda6172f68e30f3a366cb20b31126e25(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ips: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cbcffdabd4f85ca883574c4195eee526fdaa455bd68055fa01abd49020e41f5(
    *,
    ips: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f847dea812065f41d89ef8714a33298b916a69d8d4a316128580a5528706e36e(
    *,
    message: builtins.str,
    sender: builtins.str,
    smtp_reply_code: builtins.str,
    status_code: typing.Optional[builtins.str] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13bb44c4317522a7d6ce5dee4a2200eb13cf7dfccfdbfa15df9ba7d50ec75bd1(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    delivery_options: typing.Optional[typing.Union[typing.Union[CfnConfigurationSet.DeliveryOptionsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    reputation_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSet.ReputationOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sending_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSet.SendingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    suppression_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSet.SuppressionOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tracking_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSet.TrackingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vdm_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSet.VdmOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63ed92a00925569033d102d0f89dd0683aa8605fca8dbbda1aa15f5c8f52e540(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68f9412d7545d61e9c7a1fc0e5c70c73156f9b93bdb00b36af94a3192bb9cdc0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef0d1934fafb466d58818e69e36e9e4b6064f66ef66048e445022da948e81ac(
    value: typing.Optional[typing.Union[CfnConfigurationSet.DeliveryOptionsProperty, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49743c3fce7e5e543b82086f63966eb171b6e470ce7f6b177f2c832eb37618a5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a79ec05d54ce608b4f0ab49d74f3f54d5f0f0ad6e916fcb7b8b0a751b9e08e6(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSet.ReputationOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b964b196b027647457be83679b2ee4615c64b70cbf051a0e16758c9591dcb1f(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSet.SendingOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ed583322df351368c001a1b1c1270a762c297dca9b1c8c36f9f75037025a9a(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSet.SuppressionOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43461cc53c702a41eb4d9ef79ad4df5865d056628bea9fbb9c617d1252a38f2c(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSet.TrackingOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d104f1f3b29060fba6959555e511139222657ff331fcff77faa6c7b17ca1018(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSet.VdmOptionsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4201dce85f3f4e41450d83b2ff8ccccae9d14f1be24abe8292fd1bb249cff03(
    *,
    engagement_metrics: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5da9615e44a9aea922d9ae0fa9b864fc1bdfd670ef6fc69b7b8ca02893560a15(
    *,
    sending_pool_name: typing.Optional[builtins.str] = None,
    tls_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d26d6faf60057c4d500cd3ed1bd1fbebdcca7b98cdab5484730d44796e2d2d(
    *,
    optimized_shared_delivery: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fee151174424c629aa606a17d41bd5f922500b13883f167ec5d37c2fff7dec3d(
    *,
    reputation_metrics_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5c23cb2ccbd3036c589b7bfc323dd1e87316f23cb614e0dc83fa84833acc99(
    *,
    sending_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ee545a15706684e2048616f818fd4b36c1b08d8f01c6c927469bde9fad70683(
    *,
    suppressed_reasons: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6abf6e56bc382300f76ed3f7f64fdc609cad611358fb341a37f082d6dee43566(
    *,
    custom_redirect_domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc57adf947a48650c66bba0d0eb06fe8b1f18083936744d343fc26f217b08e11(
    *,
    dashboard_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSet.DashboardOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    guardian_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSet.GuardianOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a49f6f5e7a15af6e2ff6c54e820b52a709f0013fadf4e0b326438252999177e8(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    configuration_set_name: builtins.str,
    event_destination: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSetEventDestination.EventDestinationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c27f598cfff52c463542bfe637e1036c1d83c4d4b7b3ec9591610afde4bfaf(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf800f6aff4772c8e683753a8251964ddd1e4a9fcb97b025a55f8edc43f470bf(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a4539d5fe86a724cf11a76ef829e6f6fda15da137b662ef661e0c85367b014(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b4784f2ab1f3d60a68bd553763c7ce7a511fd77fad7066d5dcd37bb10f69c85(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationSetEventDestination.EventDestinationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__780f585a1e7280214ab83b3a59f4355c9225141a917ddf40525cf5724f53ea76(
    *,
    dimension_configurations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSetEventDestination.DimensionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ac68ff7c8ca01431429158705d6b1b9c57672959fd9ff59651fea4c6d036e09(
    *,
    default_dimension_value: builtins.str,
    dimension_name: builtins.str,
    dimension_value_source: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__491d2c903338d5c9011c8332967a088e9a705bdb1595304ad304871f7ba18087(
    *,
    matching_event_types: typing.Sequence[builtins.str],
    cloud_watch_destination: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSetEventDestination.CloudWatchDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    kinesis_firehose_destination: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    sns_destination: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSetEventDestination.SnsDestinationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c61081ffc519bd7ddb306b39b258359d44cf4540fd9a43e46cbc9b6cb9f22171(
    *,
    delivery_stream_arn: builtins.str,
    iam_role_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4845e2a6ad7322cffecc37f1f2e066e3ca0641082a1573e34566115f9b75e11d(
    *,
    topic_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46d5160911dad5335a3bbf8ff0d91591b2c913fd423fa5f2f4c80837d87309aa(
    *,
    configuration_set_name: builtins.str,
    event_destination: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSetEventDestination.EventDestinationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3a4c788b1b4cd57a037e5e54db330a83c2c90dda72509059ba1185e6129b18d(
    *,
    delivery_options: typing.Optional[typing.Union[typing.Union[CfnConfigurationSet.DeliveryOptionsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    reputation_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSet.ReputationOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sending_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSet.SendingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    suppression_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSet.SuppressionOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tracking_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSet.TrackingOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    vdm_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationSet.VdmOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d41d40c7650ac85127d792fb4544c5491814b232a136ef2d4611f0e326fe2a4(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    contact_list_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    topics: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnContactList.TopicProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4aeef0171480641fb2ad55c2ee030c27ae5f04ccd64bcbec193eecd02de8a36e(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61f34a97c26868e8ff0a40b8c1795deb2566ac2a8fb35011f7505b85c4bcfab5(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739da882089c70a3956a0a56974f2c6b70c22e3dc60db1f3ad1b835a6a0b2ef8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__787467977eb6be3f2e0d9027c3300ab4d17303343bf64aa66b7a780776fe90d3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88be175e59547757c7fb365d8693776a486b4dc7eeea3c04cbf5039c52d61f9b(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnContactList.TopicProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5f535996f8706e019992cccc74f2fa2a24f8722b6e340100c254e24e878ae81(
    *,
    default_subscription_status: builtins.str,
    display_name: builtins.str,
    topic_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0798ff904789fade03f62047b94c93c4052247f33073f39e2b52b964e35a0fd2(
    *,
    contact_list_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    topics: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnContactList.TopicProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01af3bfed322607c1c6648ea9f2d2b04e87efd5e451c84e9e5f60736f25d0547(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    pool_name: typing.Optional[builtins.str] = None,
    scaling_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45cd6570bc5b3254cdb9efd25822e51284336d1e1b926b5dbb4d56816c471112(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720ab9d7a5ca4c5272c5b8c1d2022ddf71a5032e9cb40f6eff12cf520938be5c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09abfb4bce0f3ed5afdb8a3da3d7cbb23048256da78540f62d19b6c8581d005a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc232e0d76a02e680328b8a52c42d03a442cdf0ac60808542f4dee66a6265a79(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__520d61be5c4902b43b0e1ead0425bcca3b6e7db1618de509d22353689b058f63(
    *,
    pool_name: typing.Optional[builtins.str] = None,
    scaling_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92fb9f941d507a6aaad3a1156f5369cccc785c22e6001b3af9d8fc6ff5196774(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    email_identity: builtins.str,
    configuration_set_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEmailIdentity.ConfigurationSetAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dkim_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEmailIdentity.DkimAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dkim_signing_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEmailIdentity.DkimSigningAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    feedback_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEmailIdentity.FeedbackAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mail_from_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEmailIdentity.MailFromAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07e34ed2ae4e3aeaba51c9ca9d43061a0be5a74a33c984a6b1a869b16c90acb0(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d436f9ed4a6719e0c9d1f60877b7035a85ea0ba0ee5c11327829227b6f0d5dba(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c426b12a9bce7afd8cabc2804d134f62f4352e3fce2b14ee81daa0b4ad73f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f961ad3e66f2f73a6f436a2db83842b86857257439c62f2e515810a0756cb9bb(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEmailIdentity.ConfigurationSetAttributesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5b6c1d1905bf652627534f1e2e5fad5f23df15c8766e388ab3642403e37bb8c(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEmailIdentity.DkimAttributesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf37d00117a480dcbb019c54de9fb105bf3131b66dc129b250c74a6f8fd48e6f(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEmailIdentity.DkimSigningAttributesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a10e564656a1b907c1a252e0d6d9f7edacc7e6fd08c33e149793438ebd700b(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEmailIdentity.FeedbackAttributesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee019766d081441b8f5888505a746be1db3301c73f5dd14054ec7af5e15f035(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEmailIdentity.MailFromAttributesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de468812f19ffde625b8ed88668e2896b995244823d7f3eb37d31f6942e593ce(
    *,
    configuration_set_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e365aa286b283628ffbc4b67d87160115af4aff1375faf68282e7bab4b60f6b(
    *,
    signing_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d1a313fff0747a5e39535795a8149a34edcefde533d0a34fa6a0747b71c81dd(
    *,
    domain_signing_private_key: typing.Optional[builtins.str] = None,
    domain_signing_selector: typing.Optional[builtins.str] = None,
    next_signing_key_length: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__415a5e5714e4c7499571025e863f54b06d548076362600b1ccdb46d327495647(
    *,
    email_forwarding_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c1b2dc7466a7a1c93c65f19c736343d00f475535c09c4245b43bb21d05eeb7(
    *,
    behavior_on_mx_failure: typing.Optional[builtins.str] = None,
    mail_from_domain: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e26635d9a29bd70d081bd12ae2f76d68303c184568003c88e9d459ac641b18(
    *,
    email_identity: builtins.str,
    configuration_set_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEmailIdentity.ConfigurationSetAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dkim_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEmailIdentity.DkimAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dkim_signing_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEmailIdentity.DkimSigningAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    feedback_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEmailIdentity.FeedbackAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mail_from_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEmailIdentity.MailFromAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05c2f1065db49ca19b225de3364838487829cc571fc76ebe5bacaa324a37a651(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    filter: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReceiptFilter.FilterProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39fb038b4f58e87d7653c5e341b14ee5cae1c4cdc23f52e4644c438bc9c12299(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d52466eff2ed506c217a7eacd465a0c7a4d7bb043832b04fffbb91b68baab4c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d27d05e2b153099f7a40e474c17cd4bdcbd045f367dd459dce48138be373fd3a(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnReceiptFilter.FilterProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef85abf22811dcf652326f6c8dd2c2056dc7d3f8c8065ecd40169113f1766e99(
    *,
    ip_filter: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReceiptFilter.IpFilterProperty, typing.Dict[builtins.str, typing.Any]]],
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8c700d36d7f8266aa0fc65c9b6465de201aca33b6ac28dfd5b4b78d533e21d(
    *,
    cidr: builtins.str,
    policy: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29474d88053c830ad11781445403eec9d50949a6d5546f79697e31fd3c6e11a5(
    *,
    filter: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReceiptFilter.FilterProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdeb50f3f81bada0d11b4dc5376bfe771b34f7860802a9e68cb8d547e857a21d(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    rule: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReceiptRule.RuleProperty, typing.Dict[builtins.str, typing.Any]]],
    rule_set_name: builtins.str,
    after: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82f85e94bb3707ef022f954c96416e9286e1f65da69502a142ac7d2534ae0a9a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f31984613cd495e566c4142b7054eeea557ea4b11c894112bf6d2db95799c36c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60310f384dc7e1ad3b0ff906100871ab80d0ebb1cbba5382a100f3f56c1b43f3(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnReceiptRule.RuleProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c259135681ea9a0e2d2f49ba97265f2838f60ff72076584fada2e549689c964(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f140fe9f0405c85b2f9efb527ac561f53ef8fd7717c7c6b99858d1af620278f3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ead34a7d8bb1152d74a37e0378dccfecd1284762b94ea8dc9aaa10c6d45995ea(
    *,
    add_header_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReceiptRule.AddHeaderActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    bounce_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReceiptRule.BounceActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    lambda_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReceiptRule.LambdaActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReceiptRule.S3ActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    sns_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReceiptRule.SNSActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stop_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReceiptRule.StopActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    workmail_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReceiptRule.WorkmailActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79a146577e59cdc7eeb9344fd4d6d0c00f4a66542172c4e23804856be51d3788(
    *,
    header_name: builtins.str,
    header_value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4968c069223b8dbfd25efbd33e5a25c5ed23b2ad1e45757f7bd4c2f94931772d(
    *,
    message: builtins.str,
    sender: builtins.str,
    smtp_reply_code: builtins.str,
    status_code: typing.Optional[builtins.str] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f43f93e4d1c2ce69c8deca1e9f8fc1d02d5072221eb7202d439838815dc27db(
    *,
    function_arn: builtins.str,
    invocation_type: typing.Optional[builtins.str] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44983645286f8cbdb286ef6ed092191a41032a973ed7e0b43bfb53b1141e9c54(
    *,
    actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReceiptRule.ActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    name: typing.Optional[builtins.str] = None,
    recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    scan_enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    tls_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ffad8fea384dd0c7624b0693273ee36d7bb0b3beb516dd6d0b3ca0507f5b409d(
    *,
    bucket_name: builtins.str,
    kms_key_arn: typing.Optional[builtins.str] = None,
    object_key_prefix: typing.Optional[builtins.str] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e774b238b52714bf99eb38772dd49314b558f5a78f6cad33a8b666dcc5f9d18a(
    *,
    encoding: typing.Optional[builtins.str] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5164570f6613f6deba8cc3127b441841cf7aa01b75c8e6ea9bd5b0a6a0ff436b(
    *,
    scope: builtins.str,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eabf0dba6adad414bc7330c34b82e3cd1d896b65fced49928d373478bbc1268b(
    *,
    organization_arn: builtins.str,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e11141ac3c676d1083540c831b2a1ed266163b8787a6e0a1725f0fa366178d2(
    *,
    rule: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnReceiptRule.RuleProperty, typing.Dict[builtins.str, typing.Any]]],
    rule_set_name: builtins.str,
    after: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b60388d81c9ac8b18b3c7ba204e70888d5dac3e36d4ced53f619b4f906a63c4(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    rule_set_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34b4d7fbd860d19ad136d51164a501b2c540790d4f40fa5ba8b7e350ed9f119f(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd5871c5543371d6e49166af6535cd7c03b8592f833ac872d640e0f59127c1e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1daf1d4b9fdf178960223360ba7544e83ac2a879ed96ad2f411c4acdf6f7c22(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea57eaf42e698570a3b692f5689ccf537a93cf78b1c13400d6364a205ccc4826(
    *,
    rule_set_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3a4f7388ccce3e291d0c0c559d8a920274ba31fd8e65d0d88c4ea7631e6ffd(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTemplate.TemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b109e5f165d7688120de74e50ee871dd73322f6fd5168ab015b1839e89bc57f9(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40a0f178f4ce74b5f638fcd9f6a35916e7ae6b9c57df03304ae5563b25740c69(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__00a00804b717b4b2c5a4d93aba12c147de4cc82fdde21bd37fa92286baed0578(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTemplate.TemplateProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__522c0fb2f6ff5ffc3f6b2d8d7b1864301ce56b2b85274e34956f81acb7d7b591(
    *,
    subject_part: builtins.str,
    html_part: typing.Optional[builtins.str] = None,
    template_name: typing.Optional[builtins.str] = None,
    text_part: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0241297bf0f761e563c87ebe7b83402ee63a9269d5d880d3e49386d678184181(
    *,
    template: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTemplate.TemplateProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__707bc5deeb197b1f1aae5f3d96c5f19ed175c44435c08f11aaa70b33d1975da5(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    dashboard_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVdmAttributes.DashboardAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    guardian_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVdmAttributes.GuardianAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb36fd8a1f2b75c804cd7812035b3fa649e82558f02f00585d5198cf4c59cdc(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aef819d717ed35f9acf106570bc1a94656e7e2aa226543cdb3e6e3957f5eb12c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb94dd05d1a51277a022d21e5d15a42e98ce1be2534cfd0a3b015e3eaebb7f3(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVdmAttributes.DashboardAttributesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f11ad9bebb9eef5ced0eb65c2eab345ea4ca50426f1900d2d6dffd2d03cfffd3(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnVdmAttributes.GuardianAttributesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5ae1a6abb8489623c92ecdaccd214bfb56d0c6a2d87c7b5063e5a9ca52a346(
    *,
    engagement_metrics: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee246be618e93926f991c6ddc0764630f78726234365bcd4a40e10efc63abf2c(
    *,
    optimized_shared_delivery: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd73f238043bea9c9e6be5f4f5b95e2251356dbfda24e734f8faccb01ff113b(
    *,
    dashboard_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVdmAttributes.DashboardAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    guardian_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnVdmAttributes.GuardianAttributesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f5ee6a4101857bbf89bdd19f4a458990d101d06b7d375ba27e1402a60ab1467(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    rule_set: IReceiptRuleSet,
    actions: typing.Optional[typing.Sequence[IReceiptRuleAction]] = None,
    after: typing.Optional[IReceiptRule] = None,
    enabled: typing.Optional[builtins.bool] = None,
    receipt_rule_name: typing.Optional[builtins.str] = None,
    recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    scan_enabled: typing.Optional[builtins.bool] = None,
    tls_policy: typing.Optional[TlsPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62cdc71a3506ecb7cb76a11a036a2de86f68b6dc6cbdab946396888a9353d6e8(
    receipt_rule: IReceiptRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b6eff382a474c81b9a627d228768afa664eaf696238bc60888b8b50abd7bc45(
    id: builtins.str,
    *,
    actions: typing.Optional[typing.Sequence[IReceiptRuleAction]] = None,
    after: typing.Optional[IReceiptRule] = None,
    enabled: typing.Optional[builtins.bool] = None,
    receipt_rule_name: typing.Optional[builtins.str] = None,
    recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    scan_enabled: typing.Optional[builtins.bool] = None,
    tls_policy: typing.Optional[TlsPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__788da92ccb3c920ddd9805afa846fdbb5b00ab9a2dd073950a7661d3c4b06ebb(
    *,
    function_arn: builtins.str,
    invocation_type: typing.Optional[builtins.str] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f69afaebba485366a9d84283d36b4483eb2c5b1349288debba873a1bed0000c0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ip: typing.Optional[builtins.str] = None,
    policy: typing.Optional[ReceiptFilterPolicy] = None,
    receipt_filter_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c4332f9b243b79549c5166db9dc6b46b79fd2b1392d30d9a4c2a6894e618ab5(
    *,
    ip: typing.Optional[builtins.str] = None,
    policy: typing.Optional[ReceiptFilterPolicy] = None,
    receipt_filter_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f09fc324eb67895ced753f10973ac3d15c83cdc8fa4982d3f930362a7d78eb22(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    rule_set: IReceiptRuleSet,
    actions: typing.Optional[typing.Sequence[IReceiptRuleAction]] = None,
    after: typing.Optional[IReceiptRule] = None,
    enabled: typing.Optional[builtins.bool] = None,
    receipt_rule_name: typing.Optional[builtins.str] = None,
    recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    scan_enabled: typing.Optional[builtins.bool] = None,
    tls_policy: typing.Optional[TlsPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a489f8830d33373a4a4eee8722cc60408037ac38edb882ee2702b8e29af4ecb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    receipt_rule_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b402316972bc07642c4a9948941e066d7bf61cfa2423303457530278f6924e1(
    action: IReceiptRuleAction,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4129e43f7dd2d7df99dcce640a8dc8554a0b5229fafe7d47439e3664dd8d7d1(
    *,
    add_header_action: typing.Optional[typing.Union[AddHeaderActionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    bounce_action: typing.Optional[typing.Union[BounceActionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    lambda_action: typing.Optional[typing.Union[LambdaActionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    s3_action: typing.Optional[typing.Union[S3ActionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    sns_action: typing.Optional[typing.Union[SNSActionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    stop_action: typing.Optional[typing.Union[StopActionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
    workmail_action: typing.Optional[typing.Union[WorkmailActionConfig, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66eea3ac6fc7a11054cff3fa7a66f99ea44e5e1e4d3ef7a5712ba6dfc81d6faf(
    *,
    actions: typing.Optional[typing.Sequence[IReceiptRuleAction]] = None,
    after: typing.Optional[IReceiptRule] = None,
    enabled: typing.Optional[builtins.bool] = None,
    receipt_rule_name: typing.Optional[builtins.str] = None,
    recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    scan_enabled: typing.Optional[builtins.bool] = None,
    tls_policy: typing.Optional[TlsPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22331a230e5d3dcb99e74c746c989f50d4a3e405e65ddccedce57fa6f16a9363(
    *,
    actions: typing.Optional[typing.Sequence[IReceiptRuleAction]] = None,
    after: typing.Optional[IReceiptRule] = None,
    enabled: typing.Optional[builtins.bool] = None,
    receipt_rule_name: typing.Optional[builtins.str] = None,
    recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    scan_enabled: typing.Optional[builtins.bool] = None,
    tls_policy: typing.Optional[TlsPolicy] = None,
    rule_set: IReceiptRuleSet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28ad0f3e07f029d665c1c2b58fdb133cd56129cc935855ed630938946830f11b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    drop_spam: typing.Optional[builtins.bool] = None,
    receipt_rule_set_name: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[ReceiptRuleOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d32bda755a5c3882e6d40011a51e10aa7c4ab1dbff4de2f5e4f31ad948255af(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    receipt_rule_set_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21cca4f2550bc241a4c6b481b1e16fe34cdca13118be943d145899e6902eb815(
    id: builtins.str,
    *,
    actions: typing.Optional[typing.Sequence[IReceiptRuleAction]] = None,
    after: typing.Optional[IReceiptRule] = None,
    enabled: typing.Optional[builtins.bool] = None,
    receipt_rule_name: typing.Optional[builtins.str] = None,
    recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    scan_enabled: typing.Optional[builtins.bool] = None,
    tls_policy: typing.Optional[TlsPolicy] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe60713f6f1db793e4f84c75e3b684d03f32ab586a08d75d38f50abe8d80396e(
    *,
    drop_spam: typing.Optional[builtins.bool] = None,
    receipt_rule_set_name: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[ReceiptRuleOptions, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5346e521fb0405ab945200e222a5586641f5f95495fc17b82c5174bb0640f25d(
    *,
    bucket_name: builtins.str,
    kms_key_arn: typing.Optional[builtins.str] = None,
    object_key_prefix: typing.Optional[builtins.str] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88eb53ffdfee3dba7153a2b2cbe2a2b29d2b054f50662db3320156366c6900df(
    *,
    encoding: typing.Optional[builtins.str] = None,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ef8ee892ef97594b95783fa2b84d8c95ab339f9f99ce516b23fbcd69e768a4f(
    *,
    scope: builtins.str,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8cc0d7f732dd0e75362b80532f23b2fd6c2e7239e7ae96db736a87a18648eb2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    ips: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eeae95d61dd573d24fa913d1af465357923652cc571faae61673f0504912a5b(
    *,
    ips: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0362b09858aa19ad4b560eaab9f5f45f016a9fe86b9d22b49aaafd3be97d57e6(
    *,
    organization_arn: builtins.str,
    topic_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__040416e5e85b8b6efea40b26f9845395df834451bac0b29f36262918b9e5af97(
    *,
    actions: typing.Optional[typing.Sequence[IReceiptRuleAction]] = None,
    after: typing.Optional[IReceiptRule] = None,
    enabled: typing.Optional[builtins.bool] = None,
    receipt_rule_name: typing.Optional[builtins.str] = None,
    recipients: typing.Optional[typing.Sequence[builtins.str]] = None,
    scan_enabled: typing.Optional[builtins.bool] = None,
    tls_policy: typing.Optional[TlsPolicy] = None,
    rule_set: IReceiptRuleSet,
) -> None:
    """Type checking stubs"""
    pass
