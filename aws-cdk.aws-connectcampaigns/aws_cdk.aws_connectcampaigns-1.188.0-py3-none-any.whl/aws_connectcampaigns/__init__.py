'''
# AWS::ConnectCampaigns Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_connectcampaigns as connectcampaigns
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for ConnectCampaigns construct libraries](https://constructs.dev/search?q=connectcampaigns)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::ConnectCampaigns resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ConnectCampaigns.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::ConnectCampaigns](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ConnectCampaigns.html).

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
class CfnCampaign(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-connectcampaigns.CfnCampaign",
):
    '''A CloudFormation ``AWS::ConnectCampaigns::Campaign``.

    Contains information about an outbound campaign.

    :cloudformationResource: AWS::ConnectCampaigns::Campaign
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_connectcampaigns as connectcampaigns
        
        cfn_campaign = connectcampaigns.CfnCampaign(self, "MyCfnCampaign",
            connect_instance_arn="connectInstanceArn",
            dialer_config=connectcampaigns.CfnCampaign.DialerConfigProperty(
                predictive_dialer_config=connectcampaigns.CfnCampaign.PredictiveDialerConfigProperty(
                    bandwidth_allocation=123
                ),
                progressive_dialer_config=connectcampaigns.CfnCampaign.ProgressiveDialerConfigProperty(
                    bandwidth_allocation=123
                )
            ),
            name="name",
            outbound_call_config=connectcampaigns.CfnCampaign.OutboundCallConfigProperty(
                connect_contact_flow_arn="connectContactFlowArn",
                connect_queue_arn="connectQueueArn",
        
                # the properties below are optional
                connect_source_phone_number="connectSourcePhoneNumber"
            ),
        
            # the properties below are optional
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        connect_instance_arn: builtins.str,
        dialer_config: typing.Union[typing.Union["CfnCampaign.DialerConfigProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        name: builtins.str,
        outbound_call_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.OutboundCallConfigProperty", typing.Dict[builtins.str, typing.Any]]],
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ConnectCampaigns::Campaign``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param connect_instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param dialer_config: Contains information about the dialer configuration.
        :param name: The name of the campaign.
        :param outbound_call_config: Contains information about the outbound call configuration.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bab2f80828974889c071f1f252ed1da7be1ff31457489340589ec84d138ff668)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnCampaignProps(
            connect_instance_arn=connect_instance_arn,
            dialer_config=dialer_config,
            name=name,
            outbound_call_config=outbound_call_config,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c1ed1e168f26fd696e08b3e6f9a44a6d9cc2620c3ba4dec9ce6a48cbc44bdae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af54adf4cb4f5abb211921b883afa8aa07ff9c372ffe64737207220a551586cc)
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
        '''The Amazon Resource Name (ARN) of the high-volume outbound campaign.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="connectInstanceArn")
    def connect_instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-connectinstancearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "connectInstanceArn"))

    @connect_instance_arn.setter
    def connect_instance_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77798f9c493c8e42598e245185a24baa331422c45be9e4b893153273edec671f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectInstanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="dialerConfig")
    def dialer_config(
        self,
    ) -> typing.Union["CfnCampaign.DialerConfigProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''Contains information about the dialer configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-dialerconfig
        '''
        return typing.cast(typing.Union["CfnCampaign.DialerConfigProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "dialerConfig"))

    @dialer_config.setter
    def dialer_config(
        self,
        value: typing.Union["CfnCampaign.DialerConfigProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b92e5e9d59f72efb7e0ba9e366c3f1ddf0823ad83e4239b73a39e474d709e37)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dialerConfig", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea692d7db1ea06e308aaa0cb0fde8f9699b8c54e3c2571a102955fd6e1626515)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="outboundCallConfig")
    def outbound_call_config(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.OutboundCallConfigProperty"]:
        '''Contains information about the outbound call configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-outboundcallconfig
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.OutboundCallConfigProperty"], jsii.get(self, "outboundCallConfig"))

    @outbound_call_config.setter
    def outbound_call_config(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.OutboundCallConfigProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69329a64473fc486a71fec58776bfff6def77c750c1dda79cb07bb421287052a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundCallConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connectcampaigns.CfnCampaign.DialerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "predictive_dialer_config": "predictiveDialerConfig",
            "progressive_dialer_config": "progressiveDialerConfig",
        },
    )
    class DialerConfigProperty:
        def __init__(
            self,
            *,
            predictive_dialer_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.PredictiveDialerConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            progressive_dialer_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnCampaign.ProgressiveDialerConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains dialer configuration for an outbound campaign.

            :param predictive_dialer_config: The configuration of the predictive dialer.
            :param progressive_dialer_config: The configuration of the progressive dialer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-dialerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_connectcampaigns as connectcampaigns
                
                dialer_config_property = connectcampaigns.CfnCampaign.DialerConfigProperty(
                    predictive_dialer_config=connectcampaigns.CfnCampaign.PredictiveDialerConfigProperty(
                        bandwidth_allocation=123
                    ),
                    progressive_dialer_config=connectcampaigns.CfnCampaign.ProgressiveDialerConfigProperty(
                        bandwidth_allocation=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8848b8c47fe490af1e6d3c90761571edd46415a7d7448a84efeb6dee19f71aaa)
                check_type(argname="argument predictive_dialer_config", value=predictive_dialer_config, expected_type=type_hints["predictive_dialer_config"])
                check_type(argname="argument progressive_dialer_config", value=progressive_dialer_config, expected_type=type_hints["progressive_dialer_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if predictive_dialer_config is not None:
                self._values["predictive_dialer_config"] = predictive_dialer_config
            if progressive_dialer_config is not None:
                self._values["progressive_dialer_config"] = progressive_dialer_config

        @builtins.property
        def predictive_dialer_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.PredictiveDialerConfigProperty"]]:
            '''The configuration of the predictive dialer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-dialerconfig.html#cfn-connectcampaigns-campaign-dialerconfig-predictivedialerconfig
            '''
            result = self._values.get("predictive_dialer_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.PredictiveDialerConfigProperty"]], result)

        @builtins.property
        def progressive_dialer_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.ProgressiveDialerConfigProperty"]]:
            '''The configuration of the progressive dialer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-dialerconfig.html#cfn-connectcampaigns-campaign-dialerconfig-progressivedialerconfig
            '''
            result = self._values.get("progressive_dialer_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnCampaign.ProgressiveDialerConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DialerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connectcampaigns.CfnCampaign.OutboundCallConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "connect_contact_flow_arn": "connectContactFlowArn",
            "connect_queue_arn": "connectQueueArn",
            "connect_source_phone_number": "connectSourcePhoneNumber",
        },
    )
    class OutboundCallConfigProperty:
        def __init__(
            self,
            *,
            connect_contact_flow_arn: builtins.str,
            connect_queue_arn: builtins.str,
            connect_source_phone_number: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains outbound call configuration for an outbound campaign.

            :param connect_contact_flow_arn: The Amazon Resource Name (ARN) of the flow.
            :param connect_queue_arn: The Amazon Resource Name (ARN) of the queue.
            :param connect_source_phone_number: The phone number associated with the outbound call. This is the caller ID that is displayed to customers when an agent calls them.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-outboundcallconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_connectcampaigns as connectcampaigns
                
                outbound_call_config_property = connectcampaigns.CfnCampaign.OutboundCallConfigProperty(
                    connect_contact_flow_arn="connectContactFlowArn",
                    connect_queue_arn="connectQueueArn",
                
                    # the properties below are optional
                    connect_source_phone_number="connectSourcePhoneNumber"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__380ce6940f9f245bf0f17918cf98d600050b58de5f16db2ec5d253623339b5df)
                check_type(argname="argument connect_contact_flow_arn", value=connect_contact_flow_arn, expected_type=type_hints["connect_contact_flow_arn"])
                check_type(argname="argument connect_queue_arn", value=connect_queue_arn, expected_type=type_hints["connect_queue_arn"])
                check_type(argname="argument connect_source_phone_number", value=connect_source_phone_number, expected_type=type_hints["connect_source_phone_number"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "connect_contact_flow_arn": connect_contact_flow_arn,
                "connect_queue_arn": connect_queue_arn,
            }
            if connect_source_phone_number is not None:
                self._values["connect_source_phone_number"] = connect_source_phone_number

        @builtins.property
        def connect_contact_flow_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-outboundcallconfig.html#cfn-connectcampaigns-campaign-outboundcallconfig-connectcontactflowarn
            '''
            result = self._values.get("connect_contact_flow_arn")
            assert result is not None, "Required property 'connect_contact_flow_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def connect_queue_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the queue.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-outboundcallconfig.html#cfn-connectcampaigns-campaign-outboundcallconfig-connectqueuearn
            '''
            result = self._values.get("connect_queue_arn")
            assert result is not None, "Required property 'connect_queue_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def connect_source_phone_number(self) -> typing.Optional[builtins.str]:
            '''The phone number associated with the outbound call.

            This is the caller ID that is displayed to customers when an agent calls them.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-outboundcallconfig.html#cfn-connectcampaigns-campaign-outboundcallconfig-connectsourcephonenumber
            '''
            result = self._values.get("connect_source_phone_number")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OutboundCallConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connectcampaigns.CfnCampaign.PredictiveDialerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"bandwidth_allocation": "bandwidthAllocation"},
    )
    class PredictiveDialerConfigProperty:
        def __init__(self, *, bandwidth_allocation: jsii.Number) -> None:
            '''Contains predictive dialer configuration for an outbound campaign.

            :param bandwidth_allocation: Bandwidth allocation for the predictive dialer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-predictivedialerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_connectcampaigns as connectcampaigns
                
                predictive_dialer_config_property = connectcampaigns.CfnCampaign.PredictiveDialerConfigProperty(
                    bandwidth_allocation=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b245195057915c7ef501a6e039898e2b667eee9c56d00c56ca7983ff3b5a11f1)
                check_type(argname="argument bandwidth_allocation", value=bandwidth_allocation, expected_type=type_hints["bandwidth_allocation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bandwidth_allocation": bandwidth_allocation,
            }

        @builtins.property
        def bandwidth_allocation(self) -> jsii.Number:
            '''Bandwidth allocation for the predictive dialer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-predictivedialerconfig.html#cfn-connectcampaigns-campaign-predictivedialerconfig-bandwidthallocation
            '''
            result = self._values.get("bandwidth_allocation")
            assert result is not None, "Required property 'bandwidth_allocation' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PredictiveDialerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-connectcampaigns.CfnCampaign.ProgressiveDialerConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"bandwidth_allocation": "bandwidthAllocation"},
    )
    class ProgressiveDialerConfigProperty:
        def __init__(self, *, bandwidth_allocation: jsii.Number) -> None:
            '''Contains progressive dialer configuration for an outbound campaign.

            :param bandwidth_allocation: Bandwidth allocation for the progressive dialer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-progressivedialerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_connectcampaigns as connectcampaigns
                
                progressive_dialer_config_property = connectcampaigns.CfnCampaign.ProgressiveDialerConfigProperty(
                    bandwidth_allocation=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a6143ce83584c511a6883b427ba3872549286bd4afc4cda04160569be9da4ab5)
                check_type(argname="argument bandwidth_allocation", value=bandwidth_allocation, expected_type=type_hints["bandwidth_allocation"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bandwidth_allocation": bandwidth_allocation,
            }

        @builtins.property
        def bandwidth_allocation(self) -> jsii.Number:
            '''Bandwidth allocation for the progressive dialer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-progressivedialerconfig.html#cfn-connectcampaigns-campaign-progressivedialerconfig-bandwidthallocation
            '''
            result = self._values.get("bandwidth_allocation")
            assert result is not None, "Required property 'bandwidth_allocation' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ProgressiveDialerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-connectcampaigns.CfnCampaignProps",
    jsii_struct_bases=[],
    name_mapping={
        "connect_instance_arn": "connectInstanceArn",
        "dialer_config": "dialerConfig",
        "name": "name",
        "outbound_call_config": "outboundCallConfig",
        "tags": "tags",
    },
)
class CfnCampaignProps:
    def __init__(
        self,
        *,
        connect_instance_arn: builtins.str,
        dialer_config: typing.Union[typing.Union[CfnCampaign.DialerConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        name: builtins.str,
        outbound_call_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.OutboundCallConfigProperty, typing.Dict[builtins.str, typing.Any]]],
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnCampaign``.

        :param connect_instance_arn: The Amazon Resource Name (ARN) of the Amazon Connect instance.
        :param dialer_config: Contains information about the dialer configuration.
        :param name: The name of the campaign.
        :param outbound_call_config: Contains information about the outbound call configuration.
        :param tags: The tags used to organize, track, or control access for this resource. For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_connectcampaigns as connectcampaigns
            
            cfn_campaign_props = connectcampaigns.CfnCampaignProps(
                connect_instance_arn="connectInstanceArn",
                dialer_config=connectcampaigns.CfnCampaign.DialerConfigProperty(
                    predictive_dialer_config=connectcampaigns.CfnCampaign.PredictiveDialerConfigProperty(
                        bandwidth_allocation=123
                    ),
                    progressive_dialer_config=connectcampaigns.CfnCampaign.ProgressiveDialerConfigProperty(
                        bandwidth_allocation=123
                    )
                ),
                name="name",
                outbound_call_config=connectcampaigns.CfnCampaign.OutboundCallConfigProperty(
                    connect_contact_flow_arn="connectContactFlowArn",
                    connect_queue_arn="connectQueueArn",
            
                    # the properties below are optional
                    connect_source_phone_number="connectSourcePhoneNumber"
                ),
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74e0da6b8509f42d5ddea59aa3d74449b658dbea3da4af05a71726033fc4baaa)
            check_type(argname="argument connect_instance_arn", value=connect_instance_arn, expected_type=type_hints["connect_instance_arn"])
            check_type(argname="argument dialer_config", value=dialer_config, expected_type=type_hints["dialer_config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument outbound_call_config", value=outbound_call_config, expected_type=type_hints["outbound_call_config"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connect_instance_arn": connect_instance_arn,
            "dialer_config": dialer_config,
            "name": name,
            "outbound_call_config": outbound_call_config,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def connect_instance_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the Amazon Connect instance.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-connectinstancearn
        '''
        result = self._values.get("connect_instance_arn")
        assert result is not None, "Required property 'connect_instance_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def dialer_config(
        self,
    ) -> typing.Union[CfnCampaign.DialerConfigProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''Contains information about the dialer configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-dialerconfig
        '''
        result = self._values.get("dialer_config")
        assert result is not None, "Required property 'dialer_config' is missing"
        return typing.cast(typing.Union[CfnCampaign.DialerConfigProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the campaign.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def outbound_call_config(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.OutboundCallConfigProperty]:
        '''Contains information about the outbound call configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-outboundcallconfig
        '''
        result = self._values.get("outbound_call_config")
        assert result is not None, "Required property 'outbound_call_config' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.OutboundCallConfigProperty], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnCampaignProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnCampaign",
    "CfnCampaignProps",
]

publication.publish()

def _typecheckingstub__bab2f80828974889c071f1f252ed1da7be1ff31457489340589ec84d138ff668(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    connect_instance_arn: builtins.str,
    dialer_config: typing.Union[typing.Union[CfnCampaign.DialerConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    name: builtins.str,
    outbound_call_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.OutboundCallConfigProperty, typing.Dict[builtins.str, typing.Any]]],
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c1ed1e168f26fd696e08b3e6f9a44a6d9cc2620c3ba4dec9ce6a48cbc44bdae(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af54adf4cb4f5abb211921b883afa8aa07ff9c372ffe64737207220a551586cc(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77798f9c493c8e42598e245185a24baa331422c45be9e4b893153273edec671f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b92e5e9d59f72efb7e0ba9e366c3f1ddf0823ad83e4239b73a39e474d709e37(
    value: typing.Union[CfnCampaign.DialerConfigProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea692d7db1ea06e308aaa0cb0fde8f9699b8c54e3c2571a102955fd6e1626515(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69329a64473fc486a71fec58776bfff6def77c750c1dda79cb07bb421287052a(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnCampaign.OutboundCallConfigProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8848b8c47fe490af1e6d3c90761571edd46415a7d7448a84efeb6dee19f71aaa(
    *,
    predictive_dialer_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.PredictiveDialerConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    progressive_dialer_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.ProgressiveDialerConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__380ce6940f9f245bf0f17918cf98d600050b58de5f16db2ec5d253623339b5df(
    *,
    connect_contact_flow_arn: builtins.str,
    connect_queue_arn: builtins.str,
    connect_source_phone_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b245195057915c7ef501a6e039898e2b667eee9c56d00c56ca7983ff3b5a11f1(
    *,
    bandwidth_allocation: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a6143ce83584c511a6883b427ba3872549286bd4afc4cda04160569be9da4ab5(
    *,
    bandwidth_allocation: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74e0da6b8509f42d5ddea59aa3d74449b658dbea3da4af05a71726033fc4baaa(
    *,
    connect_instance_arn: builtins.str,
    dialer_config: typing.Union[typing.Union[CfnCampaign.DialerConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    name: builtins.str,
    outbound_call_config: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnCampaign.OutboundCallConfigProperty, typing.Dict[builtins.str, typing.Any]]],
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
