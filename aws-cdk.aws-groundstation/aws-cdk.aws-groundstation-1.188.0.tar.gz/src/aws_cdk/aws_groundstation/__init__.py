'''
# AWS::GroundStation Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_groundstation as groundstation
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for GroundStation construct libraries](https://constructs.dev/search?q=groundstation)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::GroundStation resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_GroundStation.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::GroundStation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_GroundStation.html).

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
class CfnConfig(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-groundstation.CfnConfig",
):
    '''A CloudFormation ``AWS::GroundStation::Config``.

    Creates a ``Config`` with the specified parameters.

    Config objects provide Ground Station with the details necessary in order to schedule and execute satellite contacts.

    :cloudformationResource: AWS::GroundStation::Config
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-config.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_groundstation as groundstation
        
        cfn_config = groundstation.CfnConfig(self, "MyCfnConfig",
            config_data=groundstation.CfnConfig.ConfigDataProperty(
                antenna_downlink_config=groundstation.CfnConfig.AntennaDownlinkConfigProperty(
                    spectrum_config=groundstation.CfnConfig.SpectrumConfigProperty(
                        bandwidth=groundstation.CfnConfig.FrequencyBandwidthProperty(
                            units="units",
                            value=123
                        ),
                        center_frequency=groundstation.CfnConfig.FrequencyProperty(
                            units="units",
                            value=123
                        ),
                        polarization="polarization"
                    )
                ),
                antenna_downlink_demod_decode_config=groundstation.CfnConfig.AntennaDownlinkDemodDecodeConfigProperty(
                    decode_config=groundstation.CfnConfig.DecodeConfigProperty(
                        unvalidated_json="unvalidatedJson"
                    ),
                    demodulation_config=groundstation.CfnConfig.DemodulationConfigProperty(
                        unvalidated_json="unvalidatedJson"
                    ),
                    spectrum_config=groundstation.CfnConfig.SpectrumConfigProperty(
                        bandwidth=groundstation.CfnConfig.FrequencyBandwidthProperty(
                            units="units",
                            value=123
                        ),
                        center_frequency=groundstation.CfnConfig.FrequencyProperty(
                            units="units",
                            value=123
                        ),
                        polarization="polarization"
                    )
                ),
                antenna_uplink_config=groundstation.CfnConfig.AntennaUplinkConfigProperty(
                    spectrum_config=groundstation.CfnConfig.UplinkSpectrumConfigProperty(
                        center_frequency=groundstation.CfnConfig.FrequencyProperty(
                            units="units",
                            value=123
                        ),
                        polarization="polarization"
                    ),
                    target_eirp=groundstation.CfnConfig.EirpProperty(
                        units="units",
                        value=123
                    ),
                    transmit_disabled=False
                ),
                dataflow_endpoint_config=groundstation.CfnConfig.DataflowEndpointConfigProperty(
                    dataflow_endpoint_name="dataflowEndpointName",
                    dataflow_endpoint_region="dataflowEndpointRegion"
                ),
                s3_recording_config=groundstation.CfnConfig.S3RecordingConfigProperty(
                    bucket_arn="bucketArn",
                    prefix="prefix",
                    role_arn="roleArn"
                ),
                tracking_config=groundstation.CfnConfig.TrackingConfigProperty(
                    autotrack="autotrack"
                ),
                uplink_echo_config=groundstation.CfnConfig.UplinkEchoConfigProperty(
                    antenna_uplink_config_arn="antennaUplinkConfigArn",
                    enabled=False
                )
            ),
            name="name",
        
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
        config_data: typing.Union[typing.Union["CfnConfig.ConfigDataProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        name: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::GroundStation::Config``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param config_data: Object containing the parameters of a config. Only one subtype may be specified per config. See the subtype definitions for a description of each config subtype.
        :param name: The name of the config object.
        :param tags: Tags assigned to a resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a66226c0ffefe260355517f4d1acebe79e041ea6e1699e3c865e6d1461f77e5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConfigProps(config_data=config_data, name=name, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__101da11792814c4646c50b409bf4342e9c786928eee616ea5eca0300fc871058)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a30a6ca400530884bee2a9ccb4533ff77fcffbcd647aaeb466bb016da7cbd5a6)
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
        '''The ARN of the config, such as ``arn:aws:groundstation:us-east-2:1234567890:config/tracking/9940bf3b-d2ba-427e-9906-842b5e5d2296`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the config, such as ``9940bf3b-d2ba-427e-9906-842b5e5d2296`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrType")
    def attr_type(self) -> builtins.str:
        '''The type of the config, such as ``tracking`` .

        :cloudformationAttribute: Type
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrType"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Tags assigned to a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-config.html#cfn-groundstation-config-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="configData")
    def config_data(
        self,
    ) -> typing.Union["CfnConfig.ConfigDataProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''Object containing the parameters of a config.

        Only one subtype may be specified per config. See the subtype definitions for a description of each config subtype.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-config.html#cfn-groundstation-config-configdata
        '''
        return typing.cast(typing.Union["CfnConfig.ConfigDataProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "configData"))

    @config_data.setter
    def config_data(
        self,
        value: typing.Union["CfnConfig.ConfigDataProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__244f52381ce3fd1b21bd8a1a350b116e35e92321ed19edf624ee5960d3e8f938)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configData", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the config object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-config.html#cfn-groundstation-config-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2035b97f6e7c3a70389e994bcf27940d02bb8d0de3f90cbc747845549213d264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnConfig.AntennaDownlinkConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"spectrum_config": "spectrumConfig"},
    )
    class AntennaDownlinkConfigProperty:
        def __init__(
            self,
            *,
            spectrum_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfig.SpectrumConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides information about how AWS Ground Station should configure an antenna for downlink during a contact.

            Use an antenna downlink config in a mission profile to receive the downlink data in raw DigIF format.

            :param spectrum_config: Defines the spectrum configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennadownlinkconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                antenna_downlink_config_property = groundstation.CfnConfig.AntennaDownlinkConfigProperty(
                    spectrum_config=groundstation.CfnConfig.SpectrumConfigProperty(
                        bandwidth=groundstation.CfnConfig.FrequencyBandwidthProperty(
                            units="units",
                            value=123
                        ),
                        center_frequency=groundstation.CfnConfig.FrequencyProperty(
                            units="units",
                            value=123
                        ),
                        polarization="polarization"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c713f87077d7b5f45fb63c46cf106277d47b4ca23419f756dfc166b2b69bed42)
                check_type(argname="argument spectrum_config", value=spectrum_config, expected_type=type_hints["spectrum_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if spectrum_config is not None:
                self._values["spectrum_config"] = spectrum_config

        @builtins.property
        def spectrum_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.SpectrumConfigProperty"]]:
            '''Defines the spectrum configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennadownlinkconfig.html#cfn-groundstation-config-antennadownlinkconfig-spectrumconfig
            '''
            result = self._values.get("spectrum_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.SpectrumConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AntennaDownlinkConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnConfig.AntennaDownlinkDemodDecodeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "decode_config": "decodeConfig",
            "demodulation_config": "demodulationConfig",
            "spectrum_config": "spectrumConfig",
        },
    )
    class AntennaDownlinkDemodDecodeConfigProperty:
        def __init__(
            self,
            *,
            decode_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfig.DecodeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            demodulation_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfig.DemodulationConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            spectrum_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfig.SpectrumConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Provides information about how AWS Ground Station should configure an antenna for downlink during a contact.

            Use an antenna downlink demod decode config in a mission profile to receive the downlink data that has been demodulated and decoded.

            :param decode_config: Defines how the RF signal will be decoded.
            :param demodulation_config: Defines how the RF signal will be demodulated.
            :param spectrum_config: Defines the spectrum configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennadownlinkdemoddecodeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                antenna_downlink_demod_decode_config_property = groundstation.CfnConfig.AntennaDownlinkDemodDecodeConfigProperty(
                    decode_config=groundstation.CfnConfig.DecodeConfigProperty(
                        unvalidated_json="unvalidatedJson"
                    ),
                    demodulation_config=groundstation.CfnConfig.DemodulationConfigProperty(
                        unvalidated_json="unvalidatedJson"
                    ),
                    spectrum_config=groundstation.CfnConfig.SpectrumConfigProperty(
                        bandwidth=groundstation.CfnConfig.FrequencyBandwidthProperty(
                            units="units",
                            value=123
                        ),
                        center_frequency=groundstation.CfnConfig.FrequencyProperty(
                            units="units",
                            value=123
                        ),
                        polarization="polarization"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab4da4296af976b99a747e0561ba3f38682c8b16e11580254c564d6f07e3417a)
                check_type(argname="argument decode_config", value=decode_config, expected_type=type_hints["decode_config"])
                check_type(argname="argument demodulation_config", value=demodulation_config, expected_type=type_hints["demodulation_config"])
                check_type(argname="argument spectrum_config", value=spectrum_config, expected_type=type_hints["spectrum_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if decode_config is not None:
                self._values["decode_config"] = decode_config
            if demodulation_config is not None:
                self._values["demodulation_config"] = demodulation_config
            if spectrum_config is not None:
                self._values["spectrum_config"] = spectrum_config

        @builtins.property
        def decode_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.DecodeConfigProperty"]]:
            '''Defines how the RF signal will be decoded.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennadownlinkdemoddecodeconfig.html#cfn-groundstation-config-antennadownlinkdemoddecodeconfig-decodeconfig
            '''
            result = self._values.get("decode_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.DecodeConfigProperty"]], result)

        @builtins.property
        def demodulation_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.DemodulationConfigProperty"]]:
            '''Defines how the RF signal will be demodulated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennadownlinkdemoddecodeconfig.html#cfn-groundstation-config-antennadownlinkdemoddecodeconfig-demodulationconfig
            '''
            result = self._values.get("demodulation_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.DemodulationConfigProperty"]], result)

        @builtins.property
        def spectrum_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.SpectrumConfigProperty"]]:
            '''Defines the spectrum configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennadownlinkdemoddecodeconfig.html#cfn-groundstation-config-antennadownlinkdemoddecodeconfig-spectrumconfig
            '''
            result = self._values.get("spectrum_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.SpectrumConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AntennaDownlinkDemodDecodeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnConfig.AntennaUplinkConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "spectrum_config": "spectrumConfig",
            "target_eirp": "targetEirp",
            "transmit_disabled": "transmitDisabled",
        },
    )
    class AntennaUplinkConfigProperty:
        def __init__(
            self,
            *,
            spectrum_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfig.UplinkSpectrumConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            target_eirp: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfig.EirpProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            transmit_disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Provides information about how AWS Ground Station should configure an antenna for uplink during a contact.

            :param spectrum_config: Defines the spectrum configuration.
            :param target_eirp: The equivalent isotropically radiated power (EIRP) to use for uplink transmissions. Valid values are between 20.0 to 50.0 dBW.
            :param transmit_disabled: Whether or not uplink transmit is disabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennauplinkconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                antenna_uplink_config_property = groundstation.CfnConfig.AntennaUplinkConfigProperty(
                    spectrum_config=groundstation.CfnConfig.UplinkSpectrumConfigProperty(
                        center_frequency=groundstation.CfnConfig.FrequencyProperty(
                            units="units",
                            value=123
                        ),
                        polarization="polarization"
                    ),
                    target_eirp=groundstation.CfnConfig.EirpProperty(
                        units="units",
                        value=123
                    ),
                    transmit_disabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__899df7a0aa92715f23a5f142db897044f116aa020dca9be2892cdcf397dd6acb)
                check_type(argname="argument spectrum_config", value=spectrum_config, expected_type=type_hints["spectrum_config"])
                check_type(argname="argument target_eirp", value=target_eirp, expected_type=type_hints["target_eirp"])
                check_type(argname="argument transmit_disabled", value=transmit_disabled, expected_type=type_hints["transmit_disabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if spectrum_config is not None:
                self._values["spectrum_config"] = spectrum_config
            if target_eirp is not None:
                self._values["target_eirp"] = target_eirp
            if transmit_disabled is not None:
                self._values["transmit_disabled"] = transmit_disabled

        @builtins.property
        def spectrum_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.UplinkSpectrumConfigProperty"]]:
            '''Defines the spectrum configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennauplinkconfig.html#cfn-groundstation-config-antennauplinkconfig-spectrumconfig
            '''
            result = self._values.get("spectrum_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.UplinkSpectrumConfigProperty"]], result)

        @builtins.property
        def target_eirp(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.EirpProperty"]]:
            '''The equivalent isotropically radiated power (EIRP) to use for uplink transmissions.

            Valid values are between 20.0 to 50.0 dBW.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennauplinkconfig.html#cfn-groundstation-config-antennauplinkconfig-targeteirp
            '''
            result = self._values.get("target_eirp")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.EirpProperty"]], result)

        @builtins.property
        def transmit_disabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Whether or not uplink transmit is disabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-antennauplinkconfig.html#cfn-groundstation-config-antennauplinkconfig-transmitdisabled
            '''
            result = self._values.get("transmit_disabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AntennaUplinkConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnConfig.ConfigDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "antenna_downlink_config": "antennaDownlinkConfig",
            "antenna_downlink_demod_decode_config": "antennaDownlinkDemodDecodeConfig",
            "antenna_uplink_config": "antennaUplinkConfig",
            "dataflow_endpoint_config": "dataflowEndpointConfig",
            "s3_recording_config": "s3RecordingConfig",
            "tracking_config": "trackingConfig",
            "uplink_echo_config": "uplinkEchoConfig",
        },
    )
    class ConfigDataProperty:
        def __init__(
            self,
            *,
            antenna_downlink_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfig.AntennaDownlinkConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            antenna_downlink_demod_decode_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfig.AntennaDownlinkDemodDecodeConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            antenna_uplink_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfig.AntennaUplinkConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            dataflow_endpoint_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfig.DataflowEndpointConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            s3_recording_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfig.S3RecordingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            tracking_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfig.TrackingConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            uplink_echo_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfig.UplinkEchoConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Config objects provide information to Ground Station about how to configure the antenna and how data flows during a contact.

            :param antenna_downlink_config: Provides information for an antenna downlink config object. Antenna downlink config objects are used to provide parameters for downlinks where no demodulation or decoding is performed by Ground Station (RF over IP downlinks).
            :param antenna_downlink_demod_decode_config: Provides information for a downlink demod decode config object. Downlink demod decode config objects are used to provide parameters for downlinks where the Ground Station service will demodulate and decode the downlinked data.
            :param antenna_uplink_config: Provides information for an uplink config object. Uplink config objects are used to provide parameters for uplink contacts.
            :param dataflow_endpoint_config: Provides information for a dataflow endpoint config object. Dataflow endpoint config objects are used to provide parameters about which IP endpoint(s) to use during a contact. Dataflow endpoints are where Ground Station sends data during a downlink contact and where Ground Station receives data to send to the satellite during an uplink contact.
            :param s3_recording_config: Provides information for an S3 recording config object. S3 recording config objects are used to provide parameters for S3 recording during downlink contacts.
            :param tracking_config: Provides information for a tracking config object. Tracking config objects are used to provide parameters about how to track the satellite through the sky during a contact.
            :param uplink_echo_config: Provides information for an uplink echo config object. Uplink echo config objects are used to provide parameters for uplink echo during uplink contacts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-configdata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                config_data_property = groundstation.CfnConfig.ConfigDataProperty(
                    antenna_downlink_config=groundstation.CfnConfig.AntennaDownlinkConfigProperty(
                        spectrum_config=groundstation.CfnConfig.SpectrumConfigProperty(
                            bandwidth=groundstation.CfnConfig.FrequencyBandwidthProperty(
                                units="units",
                                value=123
                            ),
                            center_frequency=groundstation.CfnConfig.FrequencyProperty(
                                units="units",
                                value=123
                            ),
                            polarization="polarization"
                        )
                    ),
                    antenna_downlink_demod_decode_config=groundstation.CfnConfig.AntennaDownlinkDemodDecodeConfigProperty(
                        decode_config=groundstation.CfnConfig.DecodeConfigProperty(
                            unvalidated_json="unvalidatedJson"
                        ),
                        demodulation_config=groundstation.CfnConfig.DemodulationConfigProperty(
                            unvalidated_json="unvalidatedJson"
                        ),
                        spectrum_config=groundstation.CfnConfig.SpectrumConfigProperty(
                            bandwidth=groundstation.CfnConfig.FrequencyBandwidthProperty(
                                units="units",
                                value=123
                            ),
                            center_frequency=groundstation.CfnConfig.FrequencyProperty(
                                units="units",
                                value=123
                            ),
                            polarization="polarization"
                        )
                    ),
                    antenna_uplink_config=groundstation.CfnConfig.AntennaUplinkConfigProperty(
                        spectrum_config=groundstation.CfnConfig.UplinkSpectrumConfigProperty(
                            center_frequency=groundstation.CfnConfig.FrequencyProperty(
                                units="units",
                                value=123
                            ),
                            polarization="polarization"
                        ),
                        target_eirp=groundstation.CfnConfig.EirpProperty(
                            units="units",
                            value=123
                        ),
                        transmit_disabled=False
                    ),
                    dataflow_endpoint_config=groundstation.CfnConfig.DataflowEndpointConfigProperty(
                        dataflow_endpoint_name="dataflowEndpointName",
                        dataflow_endpoint_region="dataflowEndpointRegion"
                    ),
                    s3_recording_config=groundstation.CfnConfig.S3RecordingConfigProperty(
                        bucket_arn="bucketArn",
                        prefix="prefix",
                        role_arn="roleArn"
                    ),
                    tracking_config=groundstation.CfnConfig.TrackingConfigProperty(
                        autotrack="autotrack"
                    ),
                    uplink_echo_config=groundstation.CfnConfig.UplinkEchoConfigProperty(
                        antenna_uplink_config_arn="antennaUplinkConfigArn",
                        enabled=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c655fc0ff34b8fa8d668de7fe98c19b9f642b15d2752bf77c93bdc6f1460d1af)
                check_type(argname="argument antenna_downlink_config", value=antenna_downlink_config, expected_type=type_hints["antenna_downlink_config"])
                check_type(argname="argument antenna_downlink_demod_decode_config", value=antenna_downlink_demod_decode_config, expected_type=type_hints["antenna_downlink_demod_decode_config"])
                check_type(argname="argument antenna_uplink_config", value=antenna_uplink_config, expected_type=type_hints["antenna_uplink_config"])
                check_type(argname="argument dataflow_endpoint_config", value=dataflow_endpoint_config, expected_type=type_hints["dataflow_endpoint_config"])
                check_type(argname="argument s3_recording_config", value=s3_recording_config, expected_type=type_hints["s3_recording_config"])
                check_type(argname="argument tracking_config", value=tracking_config, expected_type=type_hints["tracking_config"])
                check_type(argname="argument uplink_echo_config", value=uplink_echo_config, expected_type=type_hints["uplink_echo_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if antenna_downlink_config is not None:
                self._values["antenna_downlink_config"] = antenna_downlink_config
            if antenna_downlink_demod_decode_config is not None:
                self._values["antenna_downlink_demod_decode_config"] = antenna_downlink_demod_decode_config
            if antenna_uplink_config is not None:
                self._values["antenna_uplink_config"] = antenna_uplink_config
            if dataflow_endpoint_config is not None:
                self._values["dataflow_endpoint_config"] = dataflow_endpoint_config
            if s3_recording_config is not None:
                self._values["s3_recording_config"] = s3_recording_config
            if tracking_config is not None:
                self._values["tracking_config"] = tracking_config
            if uplink_echo_config is not None:
                self._values["uplink_echo_config"] = uplink_echo_config

        @builtins.property
        def antenna_downlink_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.AntennaDownlinkConfigProperty"]]:
            '''Provides information for an antenna downlink config object.

            Antenna downlink config objects are used to provide parameters for downlinks where no demodulation or decoding is performed by Ground Station (RF over IP downlinks).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-configdata.html#cfn-groundstation-config-configdata-antennadownlinkconfig
            '''
            result = self._values.get("antenna_downlink_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.AntennaDownlinkConfigProperty"]], result)

        @builtins.property
        def antenna_downlink_demod_decode_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.AntennaDownlinkDemodDecodeConfigProperty"]]:
            '''Provides information for a downlink demod decode config object.

            Downlink demod decode config objects are used to provide parameters for downlinks where the Ground Station service will demodulate and decode the downlinked data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-configdata.html#cfn-groundstation-config-configdata-antennadownlinkdemoddecodeconfig
            '''
            result = self._values.get("antenna_downlink_demod_decode_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.AntennaDownlinkDemodDecodeConfigProperty"]], result)

        @builtins.property
        def antenna_uplink_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.AntennaUplinkConfigProperty"]]:
            '''Provides information for an uplink config object.

            Uplink config objects are used to provide parameters for uplink contacts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-configdata.html#cfn-groundstation-config-configdata-antennauplinkconfig
            '''
            result = self._values.get("antenna_uplink_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.AntennaUplinkConfigProperty"]], result)

        @builtins.property
        def dataflow_endpoint_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.DataflowEndpointConfigProperty"]]:
            '''Provides information for a dataflow endpoint config object.

            Dataflow endpoint config objects are used to provide parameters about which IP endpoint(s) to use during a contact. Dataflow endpoints are where Ground Station sends data during a downlink contact and where Ground Station receives data to send to the satellite during an uplink contact.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-configdata.html#cfn-groundstation-config-configdata-dataflowendpointconfig
            '''
            result = self._values.get("dataflow_endpoint_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.DataflowEndpointConfigProperty"]], result)

        @builtins.property
        def s3_recording_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.S3RecordingConfigProperty"]]:
            '''Provides information for an S3 recording config object.

            S3 recording config objects are used to provide parameters for S3 recording during downlink contacts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-configdata.html#cfn-groundstation-config-configdata-s3recordingconfig
            '''
            result = self._values.get("s3_recording_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.S3RecordingConfigProperty"]], result)

        @builtins.property
        def tracking_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.TrackingConfigProperty"]]:
            '''Provides information for a tracking config object.

            Tracking config objects are used to provide parameters about how to track the satellite through the sky during a contact.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-configdata.html#cfn-groundstation-config-configdata-trackingconfig
            '''
            result = self._values.get("tracking_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.TrackingConfigProperty"]], result)

        @builtins.property
        def uplink_echo_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.UplinkEchoConfigProperty"]]:
            '''Provides information for an uplink echo config object.

            Uplink echo config objects are used to provide parameters for uplink echo during uplink contacts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-configdata.html#cfn-groundstation-config-configdata-uplinkechoconfig
            '''
            result = self._values.get("uplink_echo_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.UplinkEchoConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnConfig.DataflowEndpointConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dataflow_endpoint_name": "dataflowEndpointName",
            "dataflow_endpoint_region": "dataflowEndpointRegion",
        },
    )
    class DataflowEndpointConfigProperty:
        def __init__(
            self,
            *,
            dataflow_endpoint_name: typing.Optional[builtins.str] = None,
            dataflow_endpoint_region: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information to AWS Ground Station about which IP endpoints to use during a contact.

            :param dataflow_endpoint_name: The name of the dataflow endpoint to use during contacts.
            :param dataflow_endpoint_region: The region of the dataflow endpoint to use during contacts. When omitted, Ground Station will use the region of the contact.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-dataflowendpointconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                dataflow_endpoint_config_property = groundstation.CfnConfig.DataflowEndpointConfigProperty(
                    dataflow_endpoint_name="dataflowEndpointName",
                    dataflow_endpoint_region="dataflowEndpointRegion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1cc8804f23fcfc9295e0d4e46e0d5b47366a132b967fb86f4b0894b93698709c)
                check_type(argname="argument dataflow_endpoint_name", value=dataflow_endpoint_name, expected_type=type_hints["dataflow_endpoint_name"])
                check_type(argname="argument dataflow_endpoint_region", value=dataflow_endpoint_region, expected_type=type_hints["dataflow_endpoint_region"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dataflow_endpoint_name is not None:
                self._values["dataflow_endpoint_name"] = dataflow_endpoint_name
            if dataflow_endpoint_region is not None:
                self._values["dataflow_endpoint_region"] = dataflow_endpoint_region

        @builtins.property
        def dataflow_endpoint_name(self) -> typing.Optional[builtins.str]:
            '''The name of the dataflow endpoint to use during contacts.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-dataflowendpointconfig.html#cfn-groundstation-config-dataflowendpointconfig-dataflowendpointname
            '''
            result = self._values.get("dataflow_endpoint_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def dataflow_endpoint_region(self) -> typing.Optional[builtins.str]:
            '''The region of the dataflow endpoint to use during contacts.

            When omitted, Ground Station will use the region of the contact.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-dataflowendpointconfig.html#cfn-groundstation-config-dataflowendpointconfig-dataflowendpointregion
            '''
            result = self._values.get("dataflow_endpoint_region")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataflowEndpointConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnConfig.DecodeConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"unvalidated_json": "unvalidatedJson"},
    )
    class DecodeConfigProperty:
        def __init__(
            self,
            *,
            unvalidated_json: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines decoding settings.

            :param unvalidated_json: The decoding settings are in JSON format and define a set of steps to perform to decode the data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-decodeconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                decode_config_property = groundstation.CfnConfig.DecodeConfigProperty(
                    unvalidated_json="unvalidatedJson"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fa9ddd92d96b7ab84d9ce8b9c0b2ccd302a4ae67b8b1d5a32bdd6d94adc5c3ac)
                check_type(argname="argument unvalidated_json", value=unvalidated_json, expected_type=type_hints["unvalidated_json"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if unvalidated_json is not None:
                self._values["unvalidated_json"] = unvalidated_json

        @builtins.property
        def unvalidated_json(self) -> typing.Optional[builtins.str]:
            '''The decoding settings are in JSON format and define a set of steps to perform to decode the data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-decodeconfig.html#cfn-groundstation-config-decodeconfig-unvalidatedjson
            '''
            result = self._values.get("unvalidated_json")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DecodeConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnConfig.DemodulationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"unvalidated_json": "unvalidatedJson"},
    )
    class DemodulationConfigProperty:
        def __init__(
            self,
            *,
            unvalidated_json: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines demodulation settings.

            :param unvalidated_json: The demodulation settings are in JSON format and define parameters for demodulation, for example which modulation scheme (e.g. PSK, QPSK, etc.) and matched filter to use.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-demodulationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                demodulation_config_property = groundstation.CfnConfig.DemodulationConfigProperty(
                    unvalidated_json="unvalidatedJson"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__778a68bb0ae35fac72b46361ffdac655363d201a5d85d02f52bc3b2919ade7bf)
                check_type(argname="argument unvalidated_json", value=unvalidated_json, expected_type=type_hints["unvalidated_json"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if unvalidated_json is not None:
                self._values["unvalidated_json"] = unvalidated_json

        @builtins.property
        def unvalidated_json(self) -> typing.Optional[builtins.str]:
            '''The demodulation settings are in JSON format and define parameters for demodulation, for example which modulation scheme (e.g. PSK, QPSK, etc.) and matched filter to use.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-demodulationconfig.html#cfn-groundstation-config-demodulationconfig-unvalidatedjson
            '''
            result = self._values.get("unvalidated_json")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DemodulationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnConfig.EirpProperty",
        jsii_struct_bases=[],
        name_mapping={"units": "units", "value": "value"},
    )
    class EirpProperty:
        def __init__(
            self,
            *,
            units: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines an equivalent isotropically radiated power (EIRP).

            :param units: The units of the EIRP.
            :param value: The value of the EIRP. Valid values are between 20.0 to 50.0 dBW.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-eirp.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                eirp_property = groundstation.CfnConfig.EirpProperty(
                    units="units",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee4f7ae35c19c26eb1f6bf40bf77a6afb46cdf732ad12f30f6e514098fec03f9)
                check_type(argname="argument units", value=units, expected_type=type_hints["units"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if units is not None:
                self._values["units"] = units
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def units(self) -> typing.Optional[builtins.str]:
            '''The units of the EIRP.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-eirp.html#cfn-groundstation-config-eirp-units
            '''
            result = self._values.get("units")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The value of the EIRP.

            Valid values are between 20.0 to 50.0 dBW.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-eirp.html#cfn-groundstation-config-eirp-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EirpProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnConfig.FrequencyBandwidthProperty",
        jsii_struct_bases=[],
        name_mapping={"units": "units", "value": "value"},
    )
    class FrequencyBandwidthProperty:
        def __init__(
            self,
            *,
            units: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines a bandwidth.

            :param units: The units of the bandwidth.
            :param value: The value of the bandwidth. AWS Ground Station currently has the following bandwidth limitations:. - For ``AntennaDownlinkDemodDecodeconfig`` , valid values are between 125 kHz to 650 MHz. - For ``AntennaDownlinkconfig`` , valid values are between 10 kHz to 54 MHz. - For ``AntennaUplinkConfig`` , valid values are between 10 kHz to 54 MHz.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-frequencybandwidth.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                frequency_bandwidth_property = groundstation.CfnConfig.FrequencyBandwidthProperty(
                    units="units",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8f51546bea29a5a10efdd92b6b1bda765319fc1989f5fe87d9400cbda1316eab)
                check_type(argname="argument units", value=units, expected_type=type_hints["units"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if units is not None:
                self._values["units"] = units
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def units(self) -> typing.Optional[builtins.str]:
            '''The units of the bandwidth.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-frequencybandwidth.html#cfn-groundstation-config-frequencybandwidth-units
            '''
            result = self._values.get("units")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The value of the bandwidth. AWS Ground Station currently has the following bandwidth limitations:.

            - For ``AntennaDownlinkDemodDecodeconfig`` , valid values are between 125 kHz to 650 MHz.
            - For ``AntennaDownlinkconfig`` , valid values are between 10 kHz to 54 MHz.
            - For ``AntennaUplinkConfig`` , valid values are between 10 kHz to 54 MHz.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-frequencybandwidth.html#cfn-groundstation-config-frequencybandwidth-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FrequencyBandwidthProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnConfig.FrequencyProperty",
        jsii_struct_bases=[],
        name_mapping={"units": "units", "value": "value"},
    )
    class FrequencyProperty:
        def __init__(
            self,
            *,
            units: typing.Optional[builtins.str] = None,
            value: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Defines a frequency.

            :param units: The units of the frequency.
            :param value: The value of the frequency. Valid values are between 2200 to 2300 MHz and 7750 to 8400 MHz for downlink and 2025 to 2120 MHz for uplink.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-frequency.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                frequency_property = groundstation.CfnConfig.FrequencyProperty(
                    units="units",
                    value=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b00b26fb1fc4cb8e8d5504bfc080cfd89ef1df4d7d394375c989598fdb6c0572)
                check_type(argname="argument units", value=units, expected_type=type_hints["units"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if units is not None:
                self._values["units"] = units
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def units(self) -> typing.Optional[builtins.str]:
            '''The units of the frequency.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-frequency.html#cfn-groundstation-config-frequency-units
            '''
            result = self._values.get("units")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[jsii.Number]:
            '''The value of the frequency.

            Valid values are between 2200 to 2300 MHz and 7750 to 8400 MHz for downlink and 2025 to 2120 MHz for uplink.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-frequency.html#cfn-groundstation-config-frequency-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FrequencyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnConfig.S3RecordingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bucket_arn": "bucketArn",
            "prefix": "prefix",
            "role_arn": "roleArn",
        },
    )
    class S3RecordingConfigProperty:
        def __init__(
            self,
            *,
            bucket_arn: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
            role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Provides information about how AWS Ground Station should save downlink data to S3.

            :param bucket_arn: S3 Bucket where the data is written. The name of the S3 Bucket provided must begin with ``aws-groundstation`` .
            :param prefix: The prefix of the S3 data object. If you choose to use any optional keys for substitution, these values will be replaced with the corresponding information from your contact details. For example, a prefix of ``{satellite_id}/{year}/{month}/{day}/`` will replaced with ``fake_satellite_id/2021/01/10/`` *Optional keys for substitution* : ``{satellite_id}`` | ``{config-name}`` | ``{config-id}`` | ``{year}`` | ``{month}`` | ``{day}``
            :param role_arn: Defines the ARN of the role assumed for putting archives to S3.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-s3recordingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                s3_recording_config_property = groundstation.CfnConfig.S3RecordingConfigProperty(
                    bucket_arn="bucketArn",
                    prefix="prefix",
                    role_arn="roleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d923a50e053722ecf5e7908423da9aad6436d7de70138ad9041d367b0d93d4a2)
                check_type(argname="argument bucket_arn", value=bucket_arn, expected_type=type_hints["bucket_arn"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bucket_arn is not None:
                self._values["bucket_arn"] = bucket_arn
            if prefix is not None:
                self._values["prefix"] = prefix
            if role_arn is not None:
                self._values["role_arn"] = role_arn

        @builtins.property
        def bucket_arn(self) -> typing.Optional[builtins.str]:
            '''S3 Bucket where the data is written.

            The name of the S3 Bucket provided must begin with ``aws-groundstation`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-s3recordingconfig.html#cfn-groundstation-config-s3recordingconfig-bucketarn
            '''
            result = self._values.get("bucket_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The prefix of the S3 data object.

            If you choose to use any optional keys for substitution, these values will be replaced with the corresponding information from your contact details. For example, a prefix of ``{satellite_id}/{year}/{month}/{day}/`` will replaced with ``fake_satellite_id/2021/01/10/``

            *Optional keys for substitution* : ``{satellite_id}`` | ``{config-name}`` | ``{config-id}`` | ``{year}`` | ``{month}`` | ``{day}``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-s3recordingconfig.html#cfn-groundstation-config-s3recordingconfig-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''Defines the ARN of the role assumed for putting archives to S3.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-s3recordingconfig.html#cfn-groundstation-config-s3recordingconfig-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3RecordingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnConfig.SpectrumConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "bandwidth": "bandwidth",
            "center_frequency": "centerFrequency",
            "polarization": "polarization",
        },
    )
    class SpectrumConfigProperty:
        def __init__(
            self,
            *,
            bandwidth: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfig.FrequencyBandwidthProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            center_frequency: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfig.FrequencyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            polarization: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a spectrum.

            :param bandwidth: The bandwidth of the spectrum. AWS Ground Station currently has the following bandwidth limitations:. - For ``AntennaDownlinkDemodDecodeconfig`` , valid values are between 125 kHz to 650 MHz. - For ``AntennaDownlinkconfig`` , valid values are between 10 kHz to 54 MHz. - For ``AntennaUplinkConfig`` , valid values are between 10 kHz to 54 MHz.
            :param center_frequency: The center frequency of the spectrum. Valid values are between 2200 to 2300 MHz and 7750 to 8400 MHz for downlink and 2025 to 2120 MHz for uplink.
            :param polarization: The polarization of the spectrum. Valid values are ``"RIGHT_HAND"`` and ``"LEFT_HAND"`` . Capturing both ``"RIGHT_HAND"`` and ``"LEFT_HAND"`` polarization requires two separate configs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-spectrumconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                spectrum_config_property = groundstation.CfnConfig.SpectrumConfigProperty(
                    bandwidth=groundstation.CfnConfig.FrequencyBandwidthProperty(
                        units="units",
                        value=123
                    ),
                    center_frequency=groundstation.CfnConfig.FrequencyProperty(
                        units="units",
                        value=123
                    ),
                    polarization="polarization"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b92ee55000ccfff89a1e39e84f98faa5111305d360afe90c978c677f24ef9ba)
                check_type(argname="argument bandwidth", value=bandwidth, expected_type=type_hints["bandwidth"])
                check_type(argname="argument center_frequency", value=center_frequency, expected_type=type_hints["center_frequency"])
                check_type(argname="argument polarization", value=polarization, expected_type=type_hints["polarization"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if bandwidth is not None:
                self._values["bandwidth"] = bandwidth
            if center_frequency is not None:
                self._values["center_frequency"] = center_frequency
            if polarization is not None:
                self._values["polarization"] = polarization

        @builtins.property
        def bandwidth(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.FrequencyBandwidthProperty"]]:
            '''The bandwidth of the spectrum. AWS Ground Station currently has the following bandwidth limitations:.

            - For ``AntennaDownlinkDemodDecodeconfig`` , valid values are between 125 kHz to 650 MHz.
            - For ``AntennaDownlinkconfig`` , valid values are between 10 kHz to 54 MHz.
            - For ``AntennaUplinkConfig`` , valid values are between 10 kHz to 54 MHz.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-spectrumconfig.html#cfn-groundstation-config-spectrumconfig-bandwidth
            '''
            result = self._values.get("bandwidth")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.FrequencyBandwidthProperty"]], result)

        @builtins.property
        def center_frequency(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.FrequencyProperty"]]:
            '''The center frequency of the spectrum.

            Valid values are between 2200 to 2300 MHz and 7750 to 8400 MHz for downlink and 2025 to 2120 MHz for uplink.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-spectrumconfig.html#cfn-groundstation-config-spectrumconfig-centerfrequency
            '''
            result = self._values.get("center_frequency")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.FrequencyProperty"]], result)

        @builtins.property
        def polarization(self) -> typing.Optional[builtins.str]:
            '''The polarization of the spectrum.

            Valid values are ``"RIGHT_HAND"`` and ``"LEFT_HAND"`` . Capturing both ``"RIGHT_HAND"`` and ``"LEFT_HAND"`` polarization requires two separate configs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-spectrumconfig.html#cfn-groundstation-config-spectrumconfig-polarization
            '''
            result = self._values.get("polarization")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SpectrumConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnConfig.TrackingConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"autotrack": "autotrack"},
    )
    class TrackingConfigProperty:
        def __init__(self, *, autotrack: typing.Optional[builtins.str] = None) -> None:
            '''Provides information about how AWS Ground Station should track the satellite through the sky during a contact.

            :param autotrack: Specifies whether or not to use autotrack. ``REMOVED`` specifies that program track should only be used during the contact. ``PREFERRED`` specifies that autotracking is preferred during the contact but fallback to program track if the signal is lost. ``REQUIRED`` specifies that autotracking is required during the contact and not to use program track if the signal is lost.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-trackingconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                tracking_config_property = groundstation.CfnConfig.TrackingConfigProperty(
                    autotrack="autotrack"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__61756774cd615929a6255fccd0e5684535d70e0bee721a89ea7db5b8e9ea8b01)
                check_type(argname="argument autotrack", value=autotrack, expected_type=type_hints["autotrack"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if autotrack is not None:
                self._values["autotrack"] = autotrack

        @builtins.property
        def autotrack(self) -> typing.Optional[builtins.str]:
            '''Specifies whether or not to use autotrack.

            ``REMOVED`` specifies that program track should only be used during the contact. ``PREFERRED`` specifies that autotracking is preferred during the contact but fallback to program track if the signal is lost. ``REQUIRED`` specifies that autotracking is required during the contact and not to use program track if the signal is lost.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-trackingconfig.html#cfn-groundstation-config-trackingconfig-autotrack
            '''
            result = self._values.get("autotrack")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TrackingConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnConfig.UplinkEchoConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "antenna_uplink_config_arn": "antennaUplinkConfigArn",
            "enabled": "enabled",
        },
    )
    class UplinkEchoConfigProperty:
        def __init__(
            self,
            *,
            antenna_uplink_config_arn: typing.Optional[builtins.str] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Provides information about how AWS Ground Station should echo back uplink transmissions to a dataflow endpoint.

            :param antenna_uplink_config_arn: Defines the ARN of the uplink config to echo back to a dataflow endpoint.
            :param enabled: Whether or not uplink echo is enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-uplinkechoconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                uplink_echo_config_property = groundstation.CfnConfig.UplinkEchoConfigProperty(
                    antenna_uplink_config_arn="antennaUplinkConfigArn",
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__65dda3649b8891f5cb4882f10df6b8169722f51d55b33d855f6dbfb0b512f3b4)
                check_type(argname="argument antenna_uplink_config_arn", value=antenna_uplink_config_arn, expected_type=type_hints["antenna_uplink_config_arn"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if antenna_uplink_config_arn is not None:
                self._values["antenna_uplink_config_arn"] = antenna_uplink_config_arn
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def antenna_uplink_config_arn(self) -> typing.Optional[builtins.str]:
            '''Defines the ARN of the uplink config to echo back to a dataflow endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-uplinkechoconfig.html#cfn-groundstation-config-uplinkechoconfig-antennauplinkconfigarn
            '''
            result = self._values.get("antenna_uplink_config_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Whether or not uplink echo is enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-uplinkechoconfig.html#cfn-groundstation-config-uplinkechoconfig-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UplinkEchoConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnConfig.UplinkSpectrumConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "center_frequency": "centerFrequency",
            "polarization": "polarization",
        },
    )
    class UplinkSpectrumConfigProperty:
        def __init__(
            self,
            *,
            center_frequency: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfig.FrequencyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            polarization: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Defines a uplink spectrum.

            :param center_frequency: The center frequency of the spectrum. Valid values are between 2200 to 2300 MHz and 7750 to 8400 MHz for downlink and 2025 to 2120 MHz for uplink.
            :param polarization: The polarization of the spectrum. Valid values are ``"RIGHT_HAND"`` and ``"LEFT_HAND"`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-uplinkspectrumconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                uplink_spectrum_config_property = groundstation.CfnConfig.UplinkSpectrumConfigProperty(
                    center_frequency=groundstation.CfnConfig.FrequencyProperty(
                        units="units",
                        value=123
                    ),
                    polarization="polarization"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ba478f7a6c24bc3e8cfcc660fdd5001652420bea4976dcb2c501beada3b31f6b)
                check_type(argname="argument center_frequency", value=center_frequency, expected_type=type_hints["center_frequency"])
                check_type(argname="argument polarization", value=polarization, expected_type=type_hints["polarization"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if center_frequency is not None:
                self._values["center_frequency"] = center_frequency
            if polarization is not None:
                self._values["polarization"] = polarization

        @builtins.property
        def center_frequency(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.FrequencyProperty"]]:
            '''The center frequency of the spectrum.

            Valid values are between 2200 to 2300 MHz and 7750 to 8400 MHz for downlink and 2025 to 2120 MHz for uplink.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-uplinkspectrumconfig.html#cfn-groundstation-config-uplinkspectrumconfig-centerfrequency
            '''
            result = self._values.get("center_frequency")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfig.FrequencyProperty"]], result)

        @builtins.property
        def polarization(self) -> typing.Optional[builtins.str]:
            '''The polarization of the spectrum.

            Valid values are ``"RIGHT_HAND"`` and ``"LEFT_HAND"`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-config-uplinkspectrumconfig.html#cfn-groundstation-config-uplinkspectrumconfig-polarization
            '''
            result = self._values.get("polarization")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "UplinkSpectrumConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-groundstation.CfnConfigProps",
    jsii_struct_bases=[],
    name_mapping={"config_data": "configData", "name": "name", "tags": "tags"},
)
class CfnConfigProps:
    def __init__(
        self,
        *,
        config_data: typing.Union[typing.Union[CfnConfig.ConfigDataProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        name: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnConfig``.

        :param config_data: Object containing the parameters of a config. Only one subtype may be specified per config. See the subtype definitions for a description of each config subtype.
        :param name: The name of the config object.
        :param tags: Tags assigned to a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-config.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_groundstation as groundstation
            
            cfn_config_props = groundstation.CfnConfigProps(
                config_data=groundstation.CfnConfig.ConfigDataProperty(
                    antenna_downlink_config=groundstation.CfnConfig.AntennaDownlinkConfigProperty(
                        spectrum_config=groundstation.CfnConfig.SpectrumConfigProperty(
                            bandwidth=groundstation.CfnConfig.FrequencyBandwidthProperty(
                                units="units",
                                value=123
                            ),
                            center_frequency=groundstation.CfnConfig.FrequencyProperty(
                                units="units",
                                value=123
                            ),
                            polarization="polarization"
                        )
                    ),
                    antenna_downlink_demod_decode_config=groundstation.CfnConfig.AntennaDownlinkDemodDecodeConfigProperty(
                        decode_config=groundstation.CfnConfig.DecodeConfigProperty(
                            unvalidated_json="unvalidatedJson"
                        ),
                        demodulation_config=groundstation.CfnConfig.DemodulationConfigProperty(
                            unvalidated_json="unvalidatedJson"
                        ),
                        spectrum_config=groundstation.CfnConfig.SpectrumConfigProperty(
                            bandwidth=groundstation.CfnConfig.FrequencyBandwidthProperty(
                                units="units",
                                value=123
                            ),
                            center_frequency=groundstation.CfnConfig.FrequencyProperty(
                                units="units",
                                value=123
                            ),
                            polarization="polarization"
                        )
                    ),
                    antenna_uplink_config=groundstation.CfnConfig.AntennaUplinkConfigProperty(
                        spectrum_config=groundstation.CfnConfig.UplinkSpectrumConfigProperty(
                            center_frequency=groundstation.CfnConfig.FrequencyProperty(
                                units="units",
                                value=123
                            ),
                            polarization="polarization"
                        ),
                        target_eirp=groundstation.CfnConfig.EirpProperty(
                            units="units",
                            value=123
                        ),
                        transmit_disabled=False
                    ),
                    dataflow_endpoint_config=groundstation.CfnConfig.DataflowEndpointConfigProperty(
                        dataflow_endpoint_name="dataflowEndpointName",
                        dataflow_endpoint_region="dataflowEndpointRegion"
                    ),
                    s3_recording_config=groundstation.CfnConfig.S3RecordingConfigProperty(
                        bucket_arn="bucketArn",
                        prefix="prefix",
                        role_arn="roleArn"
                    ),
                    tracking_config=groundstation.CfnConfig.TrackingConfigProperty(
                        autotrack="autotrack"
                    ),
                    uplink_echo_config=groundstation.CfnConfig.UplinkEchoConfigProperty(
                        antenna_uplink_config_arn="antennaUplinkConfigArn",
                        enabled=False
                    )
                ),
                name="name",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6e9c04ba760dd27487871e84c0eb1bcd26f5837ec554bb5fac1de72daf389bc7)
            check_type(argname="argument config_data", value=config_data, expected_type=type_hints["config_data"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "config_data": config_data,
            "name": name,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def config_data(
        self,
    ) -> typing.Union[CfnConfig.ConfigDataProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''Object containing the parameters of a config.

        Only one subtype may be specified per config. See the subtype definitions for a description of each config subtype.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-config.html#cfn-groundstation-config-configdata
        '''
        result = self._values.get("config_data")
        assert result is not None, "Required property 'config_data' is missing"
        return typing.cast(typing.Union[CfnConfig.ConfigDataProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the config object.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-config.html#cfn-groundstation-config-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Tags assigned to a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-config.html#cfn-groundstation-config-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDataflowEndpointGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-groundstation.CfnDataflowEndpointGroup",
):
    '''A CloudFormation ``AWS::GroundStation::DataflowEndpointGroup``.

    Creates a Dataflow Endpoint Group request.

    Dataflow endpoint groups contain a list of endpoints. When the name of a dataflow endpoint group is specified in a mission profile, the Ground Station service will connect to the endpoints and flow data during a contact.

    For more information about dataflow endpoint groups, see `Dataflow Endpoint Groups <https://docs.aws.amazon.com/ground-station/latest/ug/dataflowendpointgroups.html>`_ .

    :cloudformationResource: AWS::GroundStation::DataflowEndpointGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-dataflowendpointgroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_groundstation as groundstation
        
        cfn_dataflow_endpoint_group = groundstation.CfnDataflowEndpointGroup(self, "MyCfnDataflowEndpointGroup",
            endpoint_details=[groundstation.CfnDataflowEndpointGroup.EndpointDetailsProperty(
                endpoint=groundstation.CfnDataflowEndpointGroup.DataflowEndpointProperty(
                    address=groundstation.CfnDataflowEndpointGroup.SocketAddressProperty(
                        name="name",
                        port=123
                    ),
                    mtu=123,
                    name="name"
                ),
                security_details=groundstation.CfnDataflowEndpointGroup.SecurityDetailsProperty(
                    role_arn="roleArn",
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            )],
        
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
        endpoint_details: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDataflowEndpointGroup.EndpointDetailsProperty", typing.Dict[builtins.str, typing.Any]]]]],
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::GroundStation::DataflowEndpointGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param endpoint_details: List of Endpoint Details, containing address and port for each endpoint.
        :param tags: Tags assigned to a resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9221e851b699979a50595b4fb0c2691a1a71971f0c6e4e78c33fde622364c79d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDataflowEndpointGroupProps(
            endpoint_details=endpoint_details, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2215c37654f489ba8b55b58fce2211fd1b3289a758092da982a1a3714ab2676f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca78a936f616507f9d13a44b5e038e851123457fe79d8ab88aefe62a008338c0)
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
        '''The ARN of the dataflow endpoint group, such as ``arn:aws:groundstation:us-east-2:1234567890:dataflow-endpoint-group/9940bf3b-d2ba-427e-9906-842b5e5d2296`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''UUID of a dataflow endpoint group.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Tags assigned to a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-dataflowendpointgroup.html#cfn-groundstation-dataflowendpointgroup-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="endpointDetails")
    def endpoint_details(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDataflowEndpointGroup.EndpointDetailsProperty"]]]:
        '''List of Endpoint Details, containing address and port for each endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-dataflowendpointgroup.html#cfn-groundstation-dataflowendpointgroup-endpointdetails
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDataflowEndpointGroup.EndpointDetailsProperty"]]], jsii.get(self, "endpointDetails"))

    @endpoint_details.setter
    def endpoint_details(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDataflowEndpointGroup.EndpointDetailsProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f782b85ce2121f6ca0b7fcf83e1f7016f4e19797be6eee1b76d2472ca365e0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endpointDetails", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnDataflowEndpointGroup.DataflowEndpointProperty",
        jsii_struct_bases=[],
        name_mapping={"address": "address", "mtu": "mtu", "name": "name"},
    )
    class DataflowEndpointProperty:
        def __init__(
            self,
            *,
            address: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDataflowEndpointGroup.SocketAddressProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            mtu: typing.Optional[jsii.Number] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information such as socket address and name that defines an endpoint.

            :param address: The address and port of an endpoint.
            :param mtu: Maximum transmission unit (MTU) size in bytes of a dataflow endpoint. Valid values are between 1400 and 1500. A default value of 1500 is used if not set.
            :param name: The endpoint name. When listing available contacts for a satellite, Ground Station searches for a dataflow endpoint whose name matches the value specified by the dataflow endpoint config of the selected mission profile. If no matching dataflow endpoints are found then Ground Station will not display any available contacts for the satellite.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-dataflowendpoint.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                dataflow_endpoint_property = groundstation.CfnDataflowEndpointGroup.DataflowEndpointProperty(
                    address=groundstation.CfnDataflowEndpointGroup.SocketAddressProperty(
                        name="name",
                        port=123
                    ),
                    mtu=123,
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__985db239e325084c1ba9626cbca71f050dcc911a1e6529fc2fc98565ba20ff1a)
                check_type(argname="argument address", value=address, expected_type=type_hints["address"])
                check_type(argname="argument mtu", value=mtu, expected_type=type_hints["mtu"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if address is not None:
                self._values["address"] = address
            if mtu is not None:
                self._values["mtu"] = mtu
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def address(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDataflowEndpointGroup.SocketAddressProperty"]]:
            '''The address and port of an endpoint.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-dataflowendpoint.html#cfn-groundstation-dataflowendpointgroup-dataflowendpoint-address
            '''
            result = self._values.get("address")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDataflowEndpointGroup.SocketAddressProperty"]], result)

        @builtins.property
        def mtu(self) -> typing.Optional[jsii.Number]:
            '''Maximum transmission unit (MTU) size in bytes of a dataflow endpoint.

            Valid values are between 1400 and 1500. A default value of 1500 is used if not set.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-dataflowendpoint.html#cfn-groundstation-dataflowendpointgroup-dataflowendpoint-mtu
            '''
            result = self._values.get("mtu")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The endpoint name.

            When listing available contacts for a satellite, Ground Station searches for a dataflow endpoint whose name matches the value specified by the dataflow endpoint config of the selected mission profile. If no matching dataflow endpoints are found then Ground Station will not display any available contacts for the satellite.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-dataflowendpoint.html#cfn-groundstation-dataflowendpointgroup-dataflowendpoint-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataflowEndpointProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnDataflowEndpointGroup.EndpointDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint": "endpoint", "security_details": "securityDetails"},
    )
    class EndpointDetailsProperty:
        def __init__(
            self,
            *,
            endpoint: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDataflowEndpointGroup.DataflowEndpointProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            security_details: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnDataflowEndpointGroup.SecurityDetailsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The security details and endpoint information.

            :param endpoint: Information about the endpoint such as name and the endpoint address.
            :param security_details: The role ARN, and IDs for security groups and subnets.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-endpointdetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                endpoint_details_property = groundstation.CfnDataflowEndpointGroup.EndpointDetailsProperty(
                    endpoint=groundstation.CfnDataflowEndpointGroup.DataflowEndpointProperty(
                        address=groundstation.CfnDataflowEndpointGroup.SocketAddressProperty(
                            name="name",
                            port=123
                        ),
                        mtu=123,
                        name="name"
                    ),
                    security_details=groundstation.CfnDataflowEndpointGroup.SecurityDetailsProperty(
                        role_arn="roleArn",
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__05fc028280ea57b48447af622ddb586568450641f0b99f23c178bd0260cf104c)
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument security_details", value=security_details, expected_type=type_hints["security_details"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint is not None:
                self._values["endpoint"] = endpoint
            if security_details is not None:
                self._values["security_details"] = security_details

        @builtins.property
        def endpoint(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDataflowEndpointGroup.DataflowEndpointProperty"]]:
            '''Information about the endpoint such as name and the endpoint address.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-endpointdetails.html#cfn-groundstation-dataflowendpointgroup-endpointdetails-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDataflowEndpointGroup.DataflowEndpointProperty"]], result)

        @builtins.property
        def security_details(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDataflowEndpointGroup.SecurityDetailsProperty"]]:
            '''The role ARN, and IDs for security groups and subnets.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-endpointdetails.html#cfn-groundstation-dataflowendpointgroup-endpointdetails-securitydetails
            '''
            result = self._values.get("security_details")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnDataflowEndpointGroup.SecurityDetailsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EndpointDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnDataflowEndpointGroup.SecurityDetailsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "role_arn": "roleArn",
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class SecurityDetailsProperty:
        def __init__(
            self,
            *,
            role_arn: typing.Optional[builtins.str] = None,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Information about IAM roles, subnets, and security groups needed for this DataflowEndpointGroup.

            :param role_arn: The ARN of a role which Ground Station has permission to assume, such as ``arn:aws:iam::1234567890:role/DataDeliveryServiceRole`` . Ground Station will assume this role and create an ENI in your VPC on the specified subnet upon creation of a dataflow endpoint group. This ENI is used as the ingress/egress point for data streamed during a satellite contact.
            :param security_group_ids: The security group Ids of the security role, such as ``sg-1234567890abcdef0`` .
            :param subnet_ids: The subnet Ids of the security details, such as ``subnet-12345678`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-securitydetails.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                security_details_property = groundstation.CfnDataflowEndpointGroup.SecurityDetailsProperty(
                    role_arn="roleArn",
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__45f5d2663e597ce6f9d10b1fd718b40d3dd459d2b23f1c5a2e53fbcfdcb3d069)
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of a role which Ground Station has permission to assume, such as ``arn:aws:iam::1234567890:role/DataDeliveryServiceRole`` .

            Ground Station will assume this role and create an ENI in your VPC on the specified subnet upon creation of a dataflow endpoint group. This ENI is used as the ingress/egress point for data streamed during a satellite contact.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-securitydetails.html#cfn-groundstation-dataflowendpointgroup-securitydetails-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The security group Ids of the security role, such as ``sg-1234567890abcdef0`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-securitydetails.html#cfn-groundstation-dataflowendpointgroup-securitydetails-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The subnet Ids of the security details, such as ``subnet-12345678`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-securitydetails.html#cfn-groundstation-dataflowendpointgroup-securitydetails-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecurityDetailsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnDataflowEndpointGroup.SocketAddressProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "port": "port"},
    )
    class SocketAddressProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The address of the endpoint, such as ``192.168.1.1`` .

            :param name: The name of the endpoint, such as ``Endpoint 1`` .
            :param port: The port of the endpoint, such as ``55888`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-socketaddress.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                socket_address_property = groundstation.CfnDataflowEndpointGroup.SocketAddressProperty(
                    name="name",
                    port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9c0e8c6e40c2eb55f0c6664ed6c5f86a60f6741830db0c8293c6d7893039c30a)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the endpoint, such as ``Endpoint 1`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-socketaddress.html#cfn-groundstation-dataflowendpointgroup-socketaddress-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port of the endpoint, such as ``55888`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-dataflowendpointgroup-socketaddress.html#cfn-groundstation-dataflowendpointgroup-socketaddress-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SocketAddressProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-groundstation.CfnDataflowEndpointGroupProps",
    jsii_struct_bases=[],
    name_mapping={"endpoint_details": "endpointDetails", "tags": "tags"},
)
class CfnDataflowEndpointGroupProps:
    def __init__(
        self,
        *,
        endpoint_details: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDataflowEndpointGroup.EndpointDetailsProperty, typing.Dict[builtins.str, typing.Any]]]]],
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDataflowEndpointGroup``.

        :param endpoint_details: List of Endpoint Details, containing address and port for each endpoint.
        :param tags: Tags assigned to a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-dataflowendpointgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_groundstation as groundstation
            
            cfn_dataflow_endpoint_group_props = groundstation.CfnDataflowEndpointGroupProps(
                endpoint_details=[groundstation.CfnDataflowEndpointGroup.EndpointDetailsProperty(
                    endpoint=groundstation.CfnDataflowEndpointGroup.DataflowEndpointProperty(
                        address=groundstation.CfnDataflowEndpointGroup.SocketAddressProperty(
                            name="name",
                            port=123
                        ),
                        mtu=123,
                        name="name"
                    ),
                    security_details=groundstation.CfnDataflowEndpointGroup.SecurityDetailsProperty(
                        role_arn="roleArn",
                        security_group_ids=["securityGroupIds"],
                        subnet_ids=["subnetIds"]
                    )
                )],
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b26ca9e83d55b38a1f253ee025d66980b0997298622314c35405926e6f2705e7)
            check_type(argname="argument endpoint_details", value=endpoint_details, expected_type=type_hints["endpoint_details"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "endpoint_details": endpoint_details,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def endpoint_details(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDataflowEndpointGroup.EndpointDetailsProperty]]]:
        '''List of Endpoint Details, containing address and port for each endpoint.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-dataflowendpointgroup.html#cfn-groundstation-dataflowendpointgroup-endpointdetails
        '''
        result = self._values.get("endpoint_details")
        assert result is not None, "Required property 'endpoint_details' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDataflowEndpointGroup.EndpointDetailsProperty]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Tags assigned to a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-dataflowendpointgroup.html#cfn-groundstation-dataflowendpointgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDataflowEndpointGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnMissionProfile(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-groundstation.CfnMissionProfile",
):
    '''A CloudFormation ``AWS::GroundStation::MissionProfile``.

    Mission profiles specify parameters and provide references to config objects to define how Ground Station lists and executes contacts.

    :cloudformationResource: AWS::GroundStation::MissionProfile
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_groundstation as groundstation
        
        cfn_mission_profile = groundstation.CfnMissionProfile(self, "MyCfnMissionProfile",
            dataflow_edges=[groundstation.CfnMissionProfile.DataflowEdgeProperty(
                destination="destination",
                source="source"
            )],
            minimum_viable_contact_duration_seconds=123,
            name="name",
            tracking_config_arn="trackingConfigArn",
        
            # the properties below are optional
            contact_post_pass_duration_seconds=123,
            contact_pre_pass_duration_seconds=123,
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
        dataflow_edges: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnMissionProfile.DataflowEdgeProperty", typing.Dict[builtins.str, typing.Any]]]]],
        minimum_viable_contact_duration_seconds: jsii.Number,
        name: builtins.str,
        tracking_config_arn: builtins.str,
        contact_post_pass_duration_seconds: typing.Optional[jsii.Number] = None,
        contact_pre_pass_duration_seconds: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::GroundStation::MissionProfile``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param dataflow_edges: A list containing lists of config ARNs. Each list of config ARNs is an edge, with a "from" config and a "to" config.
        :param minimum_viable_contact_duration_seconds: Minimum length of a contact in seconds that Ground Station will return when listing contacts. Ground Station will not return contacts shorter than this duration.
        :param name: The name of the mission profile.
        :param tracking_config_arn: The ARN of a tracking config objects that defines how to track the satellite through the sky during a contact.
        :param contact_post_pass_duration_seconds: Amount of time in seconds after a contact ends that you’d like to receive a CloudWatch Event indicating the pass has finished. For more information on CloudWatch Events, see the `What Is CloudWatch Events? <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/WhatIsCloudWatchEvents.html>`_
        :param contact_pre_pass_duration_seconds: Amount of time in seconds prior to contact start that you'd like to receive a CloudWatch Event indicating an upcoming pass. For more information on CloudWatch Events, see the `What Is CloudWatch Events? <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/WhatIsCloudWatchEvents.html>`_
        :param tags: Tags assigned to the mission profile.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a37c1f4bdb8615f72d387c7a38896c3fb90b671ca37cac77210c221e3a39d7e4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMissionProfileProps(
            dataflow_edges=dataflow_edges,
            minimum_viable_contact_duration_seconds=minimum_viable_contact_duration_seconds,
            name=name,
            tracking_config_arn=tracking_config_arn,
            contact_post_pass_duration_seconds=contact_post_pass_duration_seconds,
            contact_pre_pass_duration_seconds=contact_pre_pass_duration_seconds,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1c407750508bee29ce478f90e262de45db13822b3426664533abd3c56e3539b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bf24aee5f270e999dc2975223e4a9383a32d962824d0bc7c3f81c36a378588bc)
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
        '''The ARN of the mission profile, such as ``arn:aws:groundstation:us-east-2:1234567890:mission-profile/9940bf3b-d2ba-427e-9906-842b5e5d2296`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the mission profile, such as ``9940bf3b-d2ba-427e-9906-842b5e5d2296`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrRegion")
    def attr_region(self) -> builtins.str:
        '''The region of the mission profile.

        :cloudformationAttribute: Region
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRegion"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Tags assigned to the mission profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="dataflowEdges")
    def dataflow_edges(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnMissionProfile.DataflowEdgeProperty"]]]:
        '''A list containing lists of config ARNs.

        Each list of config ARNs is an edge, with a "from" config and a "to" config.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-dataflowedges
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnMissionProfile.DataflowEdgeProperty"]]], jsii.get(self, "dataflowEdges"))

    @dataflow_edges.setter
    def dataflow_edges(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnMissionProfile.DataflowEdgeProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80eaa6fa6a7eb9279740e36d7a13bdbedd2600cde4b61b8103017948a6f92ab3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataflowEdges", value)

    @builtins.property
    @jsii.member(jsii_name="minimumViableContactDurationSeconds")
    def minimum_viable_contact_duration_seconds(self) -> jsii.Number:
        '''Minimum length of a contact in seconds that Ground Station will return when listing contacts.

        Ground Station will not return contacts shorter than this duration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-minimumviablecontactdurationseconds
        '''
        return typing.cast(jsii.Number, jsii.get(self, "minimumViableContactDurationSeconds"))

    @minimum_viable_contact_duration_seconds.setter
    def minimum_viable_contact_duration_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e048893bc3e200a024aab6223ae7105236f71d56653bf9c276cbe00c1043179)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minimumViableContactDurationSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the mission profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__428ac38702f046efb32c284741b700fde79ac9d5149d46932d07bd2e608788ab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="trackingConfigArn")
    def tracking_config_arn(self) -> builtins.str:
        '''The ARN of a tracking config objects that defines how to track the satellite through the sky during a contact.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-trackingconfigarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "trackingConfigArn"))

    @tracking_config_arn.setter
    def tracking_config_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c1e87e2133aefb041321cb563be5146e0f386bbac18ebf87d895523d921de15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trackingConfigArn", value)

    @builtins.property
    @jsii.member(jsii_name="contactPostPassDurationSeconds")
    def contact_post_pass_duration_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time in seconds after a contact ends that you’d like to receive a CloudWatch Event indicating the pass has finished.

        For more information on CloudWatch Events, see the `What Is CloudWatch Events? <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/WhatIsCloudWatchEvents.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-contactpostpassdurationseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "contactPostPassDurationSeconds"))

    @contact_post_pass_duration_seconds.setter
    def contact_post_pass_duration_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__941337c7156242dd1f13aae9f183be195ca1db00d25faef010e21d23cdb10635)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactPostPassDurationSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="contactPrePassDurationSeconds")
    def contact_pre_pass_duration_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time in seconds prior to contact start that you'd like to receive a CloudWatch Event indicating an upcoming pass.

        For more information on CloudWatch Events, see the `What Is CloudWatch Events? <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/WhatIsCloudWatchEvents.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-contactprepassdurationseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "contactPrePassDurationSeconds"))

    @contact_pre_pass_duration_seconds.setter
    def contact_pre_pass_duration_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89d84355380a051905b950b223fc01fe24175954f166d920d56576332c9eeed9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contactPrePassDurationSeconds", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-groundstation.CfnMissionProfile.DataflowEdgeProperty",
        jsii_struct_bases=[],
        name_mapping={"destination": "destination", "source": "source"},
    )
    class DataflowEdgeProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[builtins.str] = None,
            source: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A dataflow edge defines from where and to where data will flow during a contact.

            :param destination: The ARN of the destination for this dataflow edge. For example, specify the ARN of a dataflow endpoint config for a downlink edge or an antenna uplink config for an uplink edge.
            :param source: The ARN of the source for this dataflow edge. For example, specify the ARN of an antenna downlink config for a downlink edge or a dataflow endpoint config for an uplink edge.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-missionprofile-dataflowedge.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_groundstation as groundstation
                
                dataflow_edge_property = groundstation.CfnMissionProfile.DataflowEdgeProperty(
                    destination="destination",
                    source="source"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__58789a46833f5d329dae396d0075a24341364b422d1d3cd50ecae30e3d5d7e6e)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if source is not None:
                self._values["source"] = source

        @builtins.property
        def destination(self) -> typing.Optional[builtins.str]:
            '''The ARN of the destination for this dataflow edge.

            For example, specify the ARN of a dataflow endpoint config for a downlink edge or an antenna uplink config for an uplink edge.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-missionprofile-dataflowedge.html#cfn-groundstation-missionprofile-dataflowedge-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source(self) -> typing.Optional[builtins.str]:
            '''The ARN of the source for this dataflow edge.

            For example, specify the ARN of an antenna downlink config for a downlink edge or a dataflow endpoint config for an uplink edge.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-groundstation-missionprofile-dataflowedge.html#cfn-groundstation-missionprofile-dataflowedge-source
            '''
            result = self._values.get("source")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DataflowEdgeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-groundstation.CfnMissionProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "dataflow_edges": "dataflowEdges",
        "minimum_viable_contact_duration_seconds": "minimumViableContactDurationSeconds",
        "name": "name",
        "tracking_config_arn": "trackingConfigArn",
        "contact_post_pass_duration_seconds": "contactPostPassDurationSeconds",
        "contact_pre_pass_duration_seconds": "contactPrePassDurationSeconds",
        "tags": "tags",
    },
)
class CfnMissionProfileProps:
    def __init__(
        self,
        *,
        dataflow_edges: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnMissionProfile.DataflowEdgeProperty, typing.Dict[builtins.str, typing.Any]]]]],
        minimum_viable_contact_duration_seconds: jsii.Number,
        name: builtins.str,
        tracking_config_arn: builtins.str,
        contact_post_pass_duration_seconds: typing.Optional[jsii.Number] = None,
        contact_pre_pass_duration_seconds: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnMissionProfile``.

        :param dataflow_edges: A list containing lists of config ARNs. Each list of config ARNs is an edge, with a "from" config and a "to" config.
        :param minimum_viable_contact_duration_seconds: Minimum length of a contact in seconds that Ground Station will return when listing contacts. Ground Station will not return contacts shorter than this duration.
        :param name: The name of the mission profile.
        :param tracking_config_arn: The ARN of a tracking config objects that defines how to track the satellite through the sky during a contact.
        :param contact_post_pass_duration_seconds: Amount of time in seconds after a contact ends that you’d like to receive a CloudWatch Event indicating the pass has finished. For more information on CloudWatch Events, see the `What Is CloudWatch Events? <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/WhatIsCloudWatchEvents.html>`_
        :param contact_pre_pass_duration_seconds: Amount of time in seconds prior to contact start that you'd like to receive a CloudWatch Event indicating an upcoming pass. For more information on CloudWatch Events, see the `What Is CloudWatch Events? <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/WhatIsCloudWatchEvents.html>`_
        :param tags: Tags assigned to the mission profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_groundstation as groundstation
            
            cfn_mission_profile_props = groundstation.CfnMissionProfileProps(
                dataflow_edges=[groundstation.CfnMissionProfile.DataflowEdgeProperty(
                    destination="destination",
                    source="source"
                )],
                minimum_viable_contact_duration_seconds=123,
                name="name",
                tracking_config_arn="trackingConfigArn",
            
                # the properties below are optional
                contact_post_pass_duration_seconds=123,
                contact_pre_pass_duration_seconds=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d2d0b247335ad999f7da38c49abe8e78b6ebfbdb9284cc36367442f105056b9)
            check_type(argname="argument dataflow_edges", value=dataflow_edges, expected_type=type_hints["dataflow_edges"])
            check_type(argname="argument minimum_viable_contact_duration_seconds", value=minimum_viable_contact_duration_seconds, expected_type=type_hints["minimum_viable_contact_duration_seconds"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tracking_config_arn", value=tracking_config_arn, expected_type=type_hints["tracking_config_arn"])
            check_type(argname="argument contact_post_pass_duration_seconds", value=contact_post_pass_duration_seconds, expected_type=type_hints["contact_post_pass_duration_seconds"])
            check_type(argname="argument contact_pre_pass_duration_seconds", value=contact_pre_pass_duration_seconds, expected_type=type_hints["contact_pre_pass_duration_seconds"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "dataflow_edges": dataflow_edges,
            "minimum_viable_contact_duration_seconds": minimum_viable_contact_duration_seconds,
            "name": name,
            "tracking_config_arn": tracking_config_arn,
        }
        if contact_post_pass_duration_seconds is not None:
            self._values["contact_post_pass_duration_seconds"] = contact_post_pass_duration_seconds
        if contact_pre_pass_duration_seconds is not None:
            self._values["contact_pre_pass_duration_seconds"] = contact_pre_pass_duration_seconds
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def dataflow_edges(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnMissionProfile.DataflowEdgeProperty]]]:
        '''A list containing lists of config ARNs.

        Each list of config ARNs is an edge, with a "from" config and a "to" config.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-dataflowedges
        '''
        result = self._values.get("dataflow_edges")
        assert result is not None, "Required property 'dataflow_edges' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnMissionProfile.DataflowEdgeProperty]]], result)

    @builtins.property
    def minimum_viable_contact_duration_seconds(self) -> jsii.Number:
        '''Minimum length of a contact in seconds that Ground Station will return when listing contacts.

        Ground Station will not return contacts shorter than this duration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-minimumviablecontactdurationseconds
        '''
        result = self._values.get("minimum_viable_contact_duration_seconds")
        assert result is not None, "Required property 'minimum_viable_contact_duration_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the mission profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tracking_config_arn(self) -> builtins.str:
        '''The ARN of a tracking config objects that defines how to track the satellite through the sky during a contact.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-trackingconfigarn
        '''
        result = self._values.get("tracking_config_arn")
        assert result is not None, "Required property 'tracking_config_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def contact_post_pass_duration_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time in seconds after a contact ends that you’d like to receive a CloudWatch Event indicating the pass has finished.

        For more information on CloudWatch Events, see the `What Is CloudWatch Events? <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/WhatIsCloudWatchEvents.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-contactpostpassdurationseconds
        '''
        result = self._values.get("contact_post_pass_duration_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def contact_pre_pass_duration_seconds(self) -> typing.Optional[jsii.Number]:
        '''Amount of time in seconds prior to contact start that you'd like to receive a CloudWatch Event indicating an upcoming pass.

        For more information on CloudWatch Events, see the `What Is CloudWatch Events? <https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/WhatIsCloudWatchEvents.html>`_

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-contactprepassdurationseconds
        '''
        result = self._values.get("contact_pre_pass_duration_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Tags assigned to the mission profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-groundstation-missionprofile.html#cfn-groundstation-missionprofile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMissionProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnConfig",
    "CfnConfigProps",
    "CfnDataflowEndpointGroup",
    "CfnDataflowEndpointGroupProps",
    "CfnMissionProfile",
    "CfnMissionProfileProps",
]

publication.publish()

def _typecheckingstub__8a66226c0ffefe260355517f4d1acebe79e041ea6e1699e3c865e6d1461f77e5(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    config_data: typing.Union[typing.Union[CfnConfig.ConfigDataProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    name: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__101da11792814c4646c50b409bf4342e9c786928eee616ea5eca0300fc871058(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a30a6ca400530884bee2a9ccb4533ff77fcffbcd647aaeb466bb016da7cbd5a6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__244f52381ce3fd1b21bd8a1a350b116e35e92321ed19edf624ee5960d3e8f938(
    value: typing.Union[CfnConfig.ConfigDataProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2035b97f6e7c3a70389e994bcf27940d02bb8d0de3f90cbc747845549213d264(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c713f87077d7b5f45fb63c46cf106277d47b4ca23419f756dfc166b2b69bed42(
    *,
    spectrum_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfig.SpectrumConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab4da4296af976b99a747e0561ba3f38682c8b16e11580254c564d6f07e3417a(
    *,
    decode_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfig.DecodeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    demodulation_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfig.DemodulationConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    spectrum_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfig.SpectrumConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__899df7a0aa92715f23a5f142db897044f116aa020dca9be2892cdcf397dd6acb(
    *,
    spectrum_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfig.UplinkSpectrumConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_eirp: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfig.EirpProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    transmit_disabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c655fc0ff34b8fa8d668de7fe98c19b9f642b15d2752bf77c93bdc6f1460d1af(
    *,
    antenna_downlink_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfig.AntennaDownlinkConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    antenna_downlink_demod_decode_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfig.AntennaDownlinkDemodDecodeConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    antenna_uplink_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfig.AntennaUplinkConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    dataflow_endpoint_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfig.DataflowEndpointConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    s3_recording_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfig.S3RecordingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tracking_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfig.TrackingConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    uplink_echo_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfig.UplinkEchoConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc8804f23fcfc9295e0d4e46e0d5b47366a132b967fb86f4b0894b93698709c(
    *,
    dataflow_endpoint_name: typing.Optional[builtins.str] = None,
    dataflow_endpoint_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa9ddd92d96b7ab84d9ce8b9c0b2ccd302a4ae67b8b1d5a32bdd6d94adc5c3ac(
    *,
    unvalidated_json: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__778a68bb0ae35fac72b46361ffdac655363d201a5d85d02f52bc3b2919ade7bf(
    *,
    unvalidated_json: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee4f7ae35c19c26eb1f6bf40bf77a6afb46cdf732ad12f30f6e514098fec03f9(
    *,
    units: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f51546bea29a5a10efdd92b6b1bda765319fc1989f5fe87d9400cbda1316eab(
    *,
    units: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b00b26fb1fc4cb8e8d5504bfc080cfd89ef1df4d7d394375c989598fdb6c0572(
    *,
    units: typing.Optional[builtins.str] = None,
    value: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d923a50e053722ecf5e7908423da9aad6436d7de70138ad9041d367b0d93d4a2(
    *,
    bucket_arn: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b92ee55000ccfff89a1e39e84f98faa5111305d360afe90c978c677f24ef9ba(
    *,
    bandwidth: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfig.FrequencyBandwidthProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    center_frequency: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfig.FrequencyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    polarization: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61756774cd615929a6255fccd0e5684535d70e0bee721a89ea7db5b8e9ea8b01(
    *,
    autotrack: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65dda3649b8891f5cb4882f10df6b8169722f51d55b33d855f6dbfb0b512f3b4(
    *,
    antenna_uplink_config_arn: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba478f7a6c24bc3e8cfcc660fdd5001652420bea4976dcb2c501beada3b31f6b(
    *,
    center_frequency: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfig.FrequencyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    polarization: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e9c04ba760dd27487871e84c0eb1bcd26f5837ec554bb5fac1de72daf389bc7(
    *,
    config_data: typing.Union[typing.Union[CfnConfig.ConfigDataProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    name: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9221e851b699979a50595b4fb0c2691a1a71971f0c6e4e78c33fde622364c79d(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    endpoint_details: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDataflowEndpointGroup.EndpointDetailsProperty, typing.Dict[builtins.str, typing.Any]]]]],
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2215c37654f489ba8b55b58fce2211fd1b3289a758092da982a1a3714ab2676f(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca78a936f616507f9d13a44b5e038e851123457fe79d8ab88aefe62a008338c0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f782b85ce2121f6ca0b7fcf83e1f7016f4e19797be6eee1b76d2472ca365e0d(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnDataflowEndpointGroup.EndpointDetailsProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__985db239e325084c1ba9626cbca71f050dcc911a1e6529fc2fc98565ba20ff1a(
    *,
    address: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDataflowEndpointGroup.SocketAddressProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    mtu: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05fc028280ea57b48447af622ddb586568450641f0b99f23c178bd0260cf104c(
    *,
    endpoint: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDataflowEndpointGroup.DataflowEndpointProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    security_details: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDataflowEndpointGroup.SecurityDetailsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45f5d2663e597ce6f9d10b1fd718b40d3dd459d2b23f1c5a2e53fbcfdcb3d069(
    *,
    role_arn: typing.Optional[builtins.str] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c0e8c6e40c2eb55f0c6664ed6c5f86a60f6741830db0c8293c6d7893039c30a(
    *,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b26ca9e83d55b38a1f253ee025d66980b0997298622314c35405926e6f2705e7(
    *,
    endpoint_details: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnDataflowEndpointGroup.EndpointDetailsProperty, typing.Dict[builtins.str, typing.Any]]]]],
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a37c1f4bdb8615f72d387c7a38896c3fb90b671ca37cac77210c221e3a39d7e4(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    dataflow_edges: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnMissionProfile.DataflowEdgeProperty, typing.Dict[builtins.str, typing.Any]]]]],
    minimum_viable_contact_duration_seconds: jsii.Number,
    name: builtins.str,
    tracking_config_arn: builtins.str,
    contact_post_pass_duration_seconds: typing.Optional[jsii.Number] = None,
    contact_pre_pass_duration_seconds: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c407750508bee29ce478f90e262de45db13822b3426664533abd3c56e3539b(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf24aee5f270e999dc2975223e4a9383a32d962824d0bc7c3f81c36a378588bc(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80eaa6fa6a7eb9279740e36d7a13bdbedd2600cde4b61b8103017948a6f92ab3(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnMissionProfile.DataflowEdgeProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e048893bc3e200a024aab6223ae7105236f71d56653bf9c276cbe00c1043179(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__428ac38702f046efb32c284741b700fde79ac9d5149d46932d07bd2e608788ab(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c1e87e2133aefb041321cb563be5146e0f386bbac18ebf87d895523d921de15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__941337c7156242dd1f13aae9f183be195ca1db00d25faef010e21d23cdb10635(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89d84355380a051905b950b223fc01fe24175954f166d920d56576332c9eeed9(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58789a46833f5d329dae396d0075a24341364b422d1d3cd50ecae30e3d5d7e6e(
    *,
    destination: typing.Optional[builtins.str] = None,
    source: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2d0b247335ad999f7da38c49abe8e78b6ebfbdb9284cc36367442f105056b9(
    *,
    dataflow_edges: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnMissionProfile.DataflowEdgeProperty, typing.Dict[builtins.str, typing.Any]]]]],
    minimum_viable_contact_duration_seconds: jsii.Number,
    name: builtins.str,
    tracking_config_arn: builtins.str,
    contact_post_pass_duration_seconds: typing.Optional[jsii.Number] = None,
    contact_pre_pass_duration_seconds: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
