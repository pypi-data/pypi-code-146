'''
# AWS::ConnectCampaigns Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as connectcampaigns
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

from .._jsii import *

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnCampaign(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_connectcampaigns.CfnCampaign",
):
    '''A CloudFormation ``AWS::ConnectCampaigns::Campaign``.

    Contains information about an outbound campaign.

    :cloudformationResource: AWS::ConnectCampaigns::Campaign
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_connectcampaigns as connectcampaigns
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        connect_instance_arn: builtins.str,
        dialer_config: typing.Union[typing.Union["CfnCampaign.DialerConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        name: builtins.str,
        outbound_call_config: typing.Union[typing.Union["CfnCampaign.OutboundCallConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbaba8141a7b887be49cd2b85669265d5f557216af8168ff0a50572350dce7dc)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71f430eda2f9ba94a5a0095f0bca2ab4052b4b6df19eb8861b1d2959ffa3cfbc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e34f6ff9d142a8c21cb66f544f5075e9f72e4a509c5cabda36256a098ae13e6)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__17323489f0ff03e7a1c412d42484c82713bc06a4db4623d6bc65318fbb0c0fc5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectInstanceArn", value)

    @builtins.property
    @jsii.member(jsii_name="dialerConfig")
    def dialer_config(
        self,
    ) -> typing.Union["CfnCampaign.DialerConfigProperty", _IResolvable_a771d0ef]:
        '''Contains information about the dialer configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-dialerconfig
        '''
        return typing.cast(typing.Union["CfnCampaign.DialerConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "dialerConfig"))

    @dialer_config.setter
    def dialer_config(
        self,
        value: typing.Union["CfnCampaign.DialerConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad9d2fc8720c41f5752cc38fb5e571017ebea175e809db172fdeb805ba188efc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd3ac1e58666762bd42fecf7cd8dc4915c85b79c2220efc409d929c3b3982013)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="outboundCallConfig")
    def outbound_call_config(
        self,
    ) -> typing.Union["CfnCampaign.OutboundCallConfigProperty", _IResolvable_a771d0ef]:
        '''Contains information about the outbound call configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-outboundcallconfig
        '''
        return typing.cast(typing.Union["CfnCampaign.OutboundCallConfigProperty", _IResolvable_a771d0ef], jsii.get(self, "outboundCallConfig"))

    @outbound_call_config.setter
    def outbound_call_config(
        self,
        value: typing.Union["CfnCampaign.OutboundCallConfigProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fdd26982d15fbfc42cf9bd0af9bc9f8f8ced126f95b7dce8a6e752c7c1a334c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outboundCallConfig", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_connectcampaigns.CfnCampaign.DialerConfigProperty",
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
            predictive_dialer_config: typing.Optional[typing.Union[typing.Union["CfnCampaign.PredictiveDialerConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            progressive_dialer_config: typing.Optional[typing.Union[typing.Union["CfnCampaign.ProgressiveDialerConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Contains dialer configuration for an outbound campaign.

            :param predictive_dialer_config: The configuration of the predictive dialer.
            :param progressive_dialer_config: The configuration of the progressive dialer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-dialerconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_connectcampaigns as connectcampaigns
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__34d89407b4512ac0f304f837bcdeb76dd9c4d93925992b4474b402dcca02326d)
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
        ) -> typing.Optional[typing.Union["CfnCampaign.PredictiveDialerConfigProperty", _IResolvable_a771d0ef]]:
            '''The configuration of the predictive dialer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-dialerconfig.html#cfn-connectcampaigns-campaign-dialerconfig-predictivedialerconfig
            '''
            result = self._values.get("predictive_dialer_config")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.PredictiveDialerConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def progressive_dialer_config(
            self,
        ) -> typing.Optional[typing.Union["CfnCampaign.ProgressiveDialerConfigProperty", _IResolvable_a771d0ef]]:
            '''The configuration of the progressive dialer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-connectcampaigns-campaign-dialerconfig.html#cfn-connectcampaigns-campaign-dialerconfig-progressivedialerconfig
            '''
            result = self._values.get("progressive_dialer_config")
            return typing.cast(typing.Optional[typing.Union["CfnCampaign.ProgressiveDialerConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DialerConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_connectcampaigns.CfnCampaign.OutboundCallConfigProperty",
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
                from monocdk import aws_connectcampaigns as connectcampaigns
                
                outbound_call_config_property = connectcampaigns.CfnCampaign.OutboundCallConfigProperty(
                    connect_contact_flow_arn="connectContactFlowArn",
                    connect_queue_arn="connectQueueArn",
                
                    # the properties below are optional
                    connect_source_phone_number="connectSourcePhoneNumber"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f467913badf5391e467146bc92dae8ffe9d9965a4991d0f511d0cbf66398c987)
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
        jsii_type="monocdk.aws_connectcampaigns.CfnCampaign.PredictiveDialerConfigProperty",
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
                from monocdk import aws_connectcampaigns as connectcampaigns
                
                predictive_dialer_config_property = connectcampaigns.CfnCampaign.PredictiveDialerConfigProperty(
                    bandwidth_allocation=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dc83bf2b9386b23f56955ff5c19536e0033f05dca0e80690de98c6fea7cdac05)
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
        jsii_type="monocdk.aws_connectcampaigns.CfnCampaign.ProgressiveDialerConfigProperty",
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
                from monocdk import aws_connectcampaigns as connectcampaigns
                
                progressive_dialer_config_property = connectcampaigns.CfnCampaign.ProgressiveDialerConfigProperty(
                    bandwidth_allocation=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__23819c1677655e528473094cbcdad452b8cf0e8bd37e02c1578ef41a680e96cd)
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
    jsii_type="monocdk.aws_connectcampaigns.CfnCampaignProps",
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
        dialer_config: typing.Union[typing.Union[CfnCampaign.DialerConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        name: builtins.str,
        outbound_call_config: typing.Union[typing.Union[CfnCampaign.OutboundCallConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_connectcampaigns as connectcampaigns
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__818e61ba987048b0cc92df30f5ff9f5ab18011d8a901632c441d32cb69989e14)
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
    ) -> typing.Union[CfnCampaign.DialerConfigProperty, _IResolvable_a771d0ef]:
        '''Contains information about the dialer configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-dialerconfig
        '''
        result = self._values.get("dialer_config")
        assert result is not None, "Required property 'dialer_config' is missing"
        return typing.cast(typing.Union[CfnCampaign.DialerConfigProperty, _IResolvable_a771d0ef], result)

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
    ) -> typing.Union[CfnCampaign.OutboundCallConfigProperty, _IResolvable_a771d0ef]:
        '''Contains information about the outbound call configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-outboundcallconfig
        '''
        result = self._values.get("outbound_call_config")
        assert result is not None, "Required property 'outbound_call_config' is missing"
        return typing.cast(typing.Union[CfnCampaign.OutboundCallConfigProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags used to organize, track, or control access for this resource.

        For example, { "tags": {"key1":"value1", "key2":"value2"} }.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-connectcampaigns-campaign.html#cfn-connectcampaigns-campaign-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

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

def _typecheckingstub__fbaba8141a7b887be49cd2b85669265d5f557216af8168ff0a50572350dce7dc(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    connect_instance_arn: builtins.str,
    dialer_config: typing.Union[typing.Union[CfnCampaign.DialerConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    name: builtins.str,
    outbound_call_config: typing.Union[typing.Union[CfnCampaign.OutboundCallConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71f430eda2f9ba94a5a0095f0bca2ab4052b4b6df19eb8861b1d2959ffa3cfbc(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e34f6ff9d142a8c21cb66f544f5075e9f72e4a509c5cabda36256a098ae13e6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17323489f0ff03e7a1c412d42484c82713bc06a4db4623d6bc65318fbb0c0fc5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad9d2fc8720c41f5752cc38fb5e571017ebea175e809db172fdeb805ba188efc(
    value: typing.Union[CfnCampaign.DialerConfigProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3ac1e58666762bd42fecf7cd8dc4915c85b79c2220efc409d929c3b3982013(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fdd26982d15fbfc42cf9bd0af9bc9f8f8ced126f95b7dce8a6e752c7c1a334c(
    value: typing.Union[CfnCampaign.OutboundCallConfigProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d89407b4512ac0f304f837bcdeb76dd9c4d93925992b4474b402dcca02326d(
    *,
    predictive_dialer_config: typing.Optional[typing.Union[typing.Union[CfnCampaign.PredictiveDialerConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    progressive_dialer_config: typing.Optional[typing.Union[typing.Union[CfnCampaign.ProgressiveDialerConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f467913badf5391e467146bc92dae8ffe9d9965a4991d0f511d0cbf66398c987(
    *,
    connect_contact_flow_arn: builtins.str,
    connect_queue_arn: builtins.str,
    connect_source_phone_number: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc83bf2b9386b23f56955ff5c19536e0033f05dca0e80690de98c6fea7cdac05(
    *,
    bandwidth_allocation: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23819c1677655e528473094cbcdad452b8cf0e8bd37e02c1578ef41a680e96cd(
    *,
    bandwidth_allocation: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__818e61ba987048b0cc92df30f5ff9f5ab18011d8a901632c441d32cb69989e14(
    *,
    connect_instance_arn: builtins.str,
    dialer_config: typing.Union[typing.Union[CfnCampaign.DialerConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    name: builtins.str,
    outbound_call_config: typing.Union[typing.Union[CfnCampaign.OutboundCallConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
