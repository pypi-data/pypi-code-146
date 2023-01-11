'''
# AWS::MediaConnect Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as mediaconnect
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for MediaConnect construct libraries](https://constructs.dev/search?q=mediaconnect)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::MediaConnect resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MediaConnect.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::MediaConnect](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_MediaConnect.html).

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
class CfnFlow(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_mediaconnect.CfnFlow",
):
    '''A CloudFormation ``AWS::MediaConnect::Flow``.

    The AWS::MediaConnect::Flow resource defines a connection between one or more video sources and one or more outputs. For each flow, you specify the transport protocol to use, encryption information, and details for any outputs or entitlements that you want. AWS Elemental MediaConnect returns an ingest endpoint where you can send your live video as a single unicast stream. The service replicates and distributes the video to every output that you specify, whether inside or outside the AWS Cloud. You can also set up entitlements on a flow to allow other AWS accounts to access your content.

    :cloudformationResource: AWS::MediaConnect::Flow
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_mediaconnect as mediaconnect
        
        cfn_flow = mediaconnect.CfnFlow(self, "MyCfnFlow",
            name="name",
            source=mediaconnect.CfnFlow.SourceProperty(
                decryption=mediaconnect.CfnFlow.EncryptionProperty(
                    role_arn="roleArn",
        
                    # the properties below are optional
                    algorithm="algorithm",
                    constant_initialization_vector="constantInitializationVector",
                    device_id="deviceId",
                    key_type="keyType",
                    region="region",
                    resource_id="resourceId",
                    secret_arn="secretArn",
                    url="url"
                ),
                description="description",
                entitlement_arn="entitlementArn",
                ingest_ip="ingestIp",
                ingest_port=123,
                max_bitrate=123,
                max_latency=123,
                min_latency=123,
                name="name",
                protocol="protocol",
                sender_control_port=123,
                sender_ip_address="senderIpAddress",
                source_arn="sourceArn",
                source_ingest_port="sourceIngestPort",
                source_listener_address="sourceListenerAddress",
                source_listener_port=123,
                stream_id="streamId",
                vpc_interface_name="vpcInterfaceName",
                whitelist_cidr="whitelistCidr"
            ),
        
            # the properties below are optional
            availability_zone="availabilityZone",
            source_failover_config=mediaconnect.CfnFlow.FailoverConfigProperty(
                failover_mode="failoverMode",
                recovery_window=123,
                source_priority=mediaconnect.CfnFlow.SourcePriorityProperty(
                    primary_source="primarySource"
                ),
                state="state"
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        name: builtins.str,
        source: typing.Union[typing.Union["CfnFlow.SourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        availability_zone: typing.Optional[builtins.str] = None,
        source_failover_config: typing.Optional[typing.Union[typing.Union["CfnFlow.FailoverConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::MediaConnect::Flow``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name of the flow.
        :param source: The settings for the source that you want to use for the new flow.
        :param availability_zone: The Availability Zone that you want to create the flow in. These options are limited to the Availability Zones within the current AWS Region.
        :param source_failover_config: The settings for source failover.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__677ad3f0bbb1ecbf8c17fb53fcc71e60b60639a087942ce4d7cf79175c4de9c0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFlowProps(
            name=name,
            source=source,
            availability_zone=availability_zone,
            source_failover_config=source_failover_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2377a5329b6d62e97968a8a81e2b340e8851f9575c33803cd8c3d84e74919eef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28a79f4bb0771f4adbd18735028ef90d2da89338df6ed91f7c264892c1c61e5b)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrFlowArn")
    def attr_flow_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the flow.

        :cloudformationAttribute: FlowArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFlowArn"))

    @builtins.property
    @jsii.member(jsii_name="attrFlowAvailabilityZone")
    def attr_flow_availability_zone(self) -> builtins.str:
        '''The Availability Zone that the flow was created in.

        These options are limited to the Availability Zones within the current AWS Region.

        :cloudformationAttribute: FlowAvailabilityZone
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFlowAvailabilityZone"))

    @builtins.property
    @jsii.member(jsii_name="attrSourceIngestIp")
    def attr_source_ingest_ip(self) -> builtins.str:
        '''The IP address that the flow listens on for incoming content.

        :cloudformationAttribute: Source.IngestIp
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSourceIngestIp"))

    @builtins.property
    @jsii.member(jsii_name="attrSourceSourceArn")
    def attr_source_source_arn(self) -> builtins.str:
        '''The ARN of the source.

        :cloudformationAttribute: Source.SourceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSourceSourceArn"))

    @builtins.property
    @jsii.member(jsii_name="attrSourceSourceIngestPort")
    def attr_source_source_ingest_port(self) -> builtins.str:
        '''The port that the flow will be listening on for incoming content.

        :cloudformationAttribute: Source.SourceIngestPort
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSourceSourceIngestPort"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39c98570900ca64fa5c1db8882310135b13544c67ff60943a4aacde4d0e9828d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> typing.Union["CfnFlow.SourceProperty", _IResolvable_a771d0ef]:
        '''The settings for the source that you want to use for the new flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-source
        '''
        return typing.cast(typing.Union["CfnFlow.SourceProperty", _IResolvable_a771d0ef], jsii.get(self, "source"))

    @source.setter
    def source(
        self,
        value: typing.Union["CfnFlow.SourceProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26067bec9d6b9fab198df82e9a4fa160128c7f9e82083e74581b7f6e9624e66f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "source", value)

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Availability Zone that you want to create the flow in.

        These options are limited to the Availability Zones within the current AWS Region.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-availabilityzone
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "availabilityZone"))

    @availability_zone.setter
    def availability_zone(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e04c225f4a3e86d061288fe2f8d254c5c0aed5f4cce8d640af684d7c350c6c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "availabilityZone", value)

    @builtins.property
    @jsii.member(jsii_name="sourceFailoverConfig")
    def source_failover_config(
        self,
    ) -> typing.Optional[typing.Union["CfnFlow.FailoverConfigProperty", _IResolvable_a771d0ef]]:
        '''The settings for source failover.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-sourcefailoverconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFlow.FailoverConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "sourceFailoverConfig"))

    @source_failover_config.setter
    def source_failover_config(
        self,
        value: typing.Optional[typing.Union["CfnFlow.FailoverConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d7f6b2380180266cfed4f38d565b4eafceef23486f423c7e3bbff67ed5d1761)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceFailoverConfig", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_mediaconnect.CfnFlow.EncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "role_arn": "roleArn",
            "algorithm": "algorithm",
            "constant_initialization_vector": "constantInitializationVector",
            "device_id": "deviceId",
            "key_type": "keyType",
            "region": "region",
            "resource_id": "resourceId",
            "secret_arn": "secretArn",
            "url": "url",
        },
    )
    class EncryptionProperty:
        def __init__(
            self,
            *,
            role_arn: builtins.str,
            algorithm: typing.Optional[builtins.str] = None,
            constant_initialization_vector: typing.Optional[builtins.str] = None,
            device_id: typing.Optional[builtins.str] = None,
            key_type: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
            resource_id: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the encryption of the flow.

            :param role_arn: The Amazon Resource Name (ARN) of the role that you created during setup (when you set up MediaConnect as a trusted entity).
            :param algorithm: The type of algorithm that is used for the encryption (such as aes128, aes192, or aes256).
            :param constant_initialization_vector: A 128-bit, 16-byte hex value represented by a 32-character string, to be used with the key for encrypting content. This parameter is not valid for static key encryption.
            :param device_id: The value of one of the devices that you configured with your digital rights management (DRM) platform key provider. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param key_type: The type of key that is used for the encryption. If you don't specify a ``keyType`` value, the service uses the default setting ( ``static-key`` ).
            :param region: The AWS Region that the API Gateway proxy endpoint was created in. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param resource_id: An identifier for the content. The service sends this value to the key server to identify the current endpoint. The resource ID is also known as the content ID. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param secret_arn: The ARN of the secret that you created in AWS Secrets Manager to store the encryption key.
            :param url: The URL from the API Gateway proxy that you set up to talk to your key server. This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediaconnect as mediaconnect
                
                encryption_property = mediaconnect.CfnFlow.EncryptionProperty(
                    role_arn="roleArn",
                
                    # the properties below are optional
                    algorithm="algorithm",
                    constant_initialization_vector="constantInitializationVector",
                    device_id="deviceId",
                    key_type="keyType",
                    region="region",
                    resource_id="resourceId",
                    secret_arn="secretArn",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c08c417f3091b2f1cdc728267dd891ce46cdaebd1d220c2e75c5c5eb244ea4a8)
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
                check_type(argname="argument constant_initialization_vector", value=constant_initialization_vector, expected_type=type_hints["constant_initialization_vector"])
                check_type(argname="argument device_id", value=device_id, expected_type=type_hints["device_id"])
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "role_arn": role_arn,
            }
            if algorithm is not None:
                self._values["algorithm"] = algorithm
            if constant_initialization_vector is not None:
                self._values["constant_initialization_vector"] = constant_initialization_vector
            if device_id is not None:
                self._values["device_id"] = device_id
            if key_type is not None:
                self._values["key_type"] = key_type
            if region is not None:
                self._values["region"] = region
            if resource_id is not None:
                self._values["resource_id"] = resource_id
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def role_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the role that you created during setup (when you set up MediaConnect as a trusted entity).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-rolearn
            '''
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def algorithm(self) -> typing.Optional[builtins.str]:
            '''The type of algorithm that is used for the encryption (such as aes128, aes192, or aes256).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-algorithm
            '''
            result = self._values.get("algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def constant_initialization_vector(self) -> typing.Optional[builtins.str]:
            '''A 128-bit, 16-byte hex value represented by a 32-character string, to be used with the key for encrypting content.

            This parameter is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-constantinitializationvector
            '''
            result = self._values.get("constant_initialization_vector")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_id(self) -> typing.Optional[builtins.str]:
            '''The value of one of the devices that you configured with your digital rights management (DRM) platform key provider.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-deviceid
            '''
            result = self._values.get("device_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_type(self) -> typing.Optional[builtins.str]:
            '''The type of key that is used for the encryption.

            If you don't specify a ``keyType`` value, the service uses the default setting ( ``static-key`` ).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-keytype
            '''
            result = self._values.get("key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region that the API Gateway proxy endpoint was created in.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_id(self) -> typing.Optional[builtins.str]:
            '''An identifier for the content.

            The service sends this value to the key server to identify the current endpoint. The resource ID is also known as the content ID. This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-resourceid
            '''
            result = self._values.get("resource_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the secret that you created in AWS Secrets Manager to store the encryption key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL from the API Gateway proxy that you set up to talk to your key server.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-encryption.html#cfn-mediaconnect-flow-encryption-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediaconnect.CfnFlow.FailoverConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "failover_mode": "failoverMode",
            "recovery_window": "recoveryWindow",
            "source_priority": "sourcePriority",
            "state": "state",
        },
    )
    class FailoverConfigProperty:
        def __init__(
            self,
            *,
            failover_mode: typing.Optional[builtins.str] = None,
            recovery_window: typing.Optional[jsii.Number] = None,
            source_priority: typing.Optional[typing.Union[typing.Union["CfnFlow.SourcePriorityProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            state: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The settings for source failover.

            :param failover_mode: The type of failover you choose for this flow. MERGE combines the source streams into a single stream, allowing graceful recovery from any single-source loss. FAILOVER allows switching between different streams.
            :param recovery_window: The size of the buffer (delay) that the service maintains. A larger buffer means a longer delay in transmitting the stream, but more room for error correction. A smaller buffer means a shorter delay, but less room for error correction. You can choose a value from 100-500 ms. If you keep this field blank, the service uses the default value of 200 ms. This setting only applies when Failover Mode is set to MERGE.
            :param source_priority: The priority you want to assign to a source. You can have a primary stream and a backup stream or two equally prioritized streams. This setting only applies when Failover Mode is set to FAILOVER.
            :param state: The state of source failover on the flow. If the state is disabled, the flow can have only one source. If the state is enabled, the flow can have one or two sources.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-failoverconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediaconnect as mediaconnect
                
                failover_config_property = mediaconnect.CfnFlow.FailoverConfigProperty(
                    failover_mode="failoverMode",
                    recovery_window=123,
                    source_priority=mediaconnect.CfnFlow.SourcePriorityProperty(
                        primary_source="primarySource"
                    ),
                    state="state"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4f1c8de1ea6c38f9b23367e03c9fa5f93275a0dd3a030ab5b1b0e5218ee384d4)
                check_type(argname="argument failover_mode", value=failover_mode, expected_type=type_hints["failover_mode"])
                check_type(argname="argument recovery_window", value=recovery_window, expected_type=type_hints["recovery_window"])
                check_type(argname="argument source_priority", value=source_priority, expected_type=type_hints["source_priority"])
                check_type(argname="argument state", value=state, expected_type=type_hints["state"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if failover_mode is not None:
                self._values["failover_mode"] = failover_mode
            if recovery_window is not None:
                self._values["recovery_window"] = recovery_window
            if source_priority is not None:
                self._values["source_priority"] = source_priority
            if state is not None:
                self._values["state"] = state

        @builtins.property
        def failover_mode(self) -> typing.Optional[builtins.str]:
            '''The type of failover you choose for this flow.

            MERGE combines the source streams into a single stream, allowing graceful recovery from any single-source loss. FAILOVER allows switching between different streams.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-failoverconfig.html#cfn-mediaconnect-flow-failoverconfig-failovermode
            '''
            result = self._values.get("failover_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def recovery_window(self) -> typing.Optional[jsii.Number]:
            '''The size of the buffer (delay) that the service maintains.

            A larger buffer means a longer delay in transmitting the stream, but more room for error correction. A smaller buffer means a shorter delay, but less room for error correction. You can choose a value from 100-500 ms. If you keep this field blank, the service uses the default value of 200 ms. This setting only applies when Failover Mode is set to MERGE.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-failoverconfig.html#cfn-mediaconnect-flow-failoverconfig-recoverywindow
            '''
            result = self._values.get("recovery_window")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def source_priority(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.SourcePriorityProperty", _IResolvable_a771d0ef]]:
            '''The priority you want to assign to a source.

            You can have a primary stream and a backup stream or two equally prioritized streams. This setting only applies when Failover Mode is set to FAILOVER.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-failoverconfig.html#cfn-mediaconnect-flow-failoverconfig-sourcepriority
            '''
            result = self._values.get("source_priority")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.SourcePriorityProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def state(self) -> typing.Optional[builtins.str]:
            '''The state of source failover on the flow.

            If the state is disabled, the flow can have only one source. If the state is enabled, the flow can have one or two sources.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-failoverconfig.html#cfn-mediaconnect-flow-failoverconfig-state
            '''
            result = self._values.get("state")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FailoverConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediaconnect.CfnFlow.SourcePriorityProperty",
        jsii_struct_bases=[],
        name_mapping={"primary_source": "primarySource"},
    )
    class SourcePriorityProperty:
        def __init__(self, *, primary_source: builtins.str) -> None:
            '''The priority you want to assign to a source.

            You can have a primary stream and a backup stream or two equally prioritized streams. This setting only applies when Failover Mode is set to FAILOVER.

            :param primary_source: The name of the source you choose as the primary source for this flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-sourcepriority.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediaconnect as mediaconnect
                
                source_priority_property = mediaconnect.CfnFlow.SourcePriorityProperty(
                    primary_source="primarySource"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__482e14dba0d2888a051941c86c4ecf4857661fdea59dad9e0154586148046182)
                check_type(argname="argument primary_source", value=primary_source, expected_type=type_hints["primary_source"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "primary_source": primary_source,
            }

        @builtins.property
        def primary_source(self) -> builtins.str:
            '''The name of the source you choose as the primary source for this flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-sourcepriority.html#cfn-mediaconnect-flow-sourcepriority-primarysource
            '''
            result = self._values.get("primary_source")
            assert result is not None, "Required property 'primary_source' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourcePriorityProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediaconnect.CfnFlow.SourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "decryption": "decryption",
            "description": "description",
            "entitlement_arn": "entitlementArn",
            "ingest_ip": "ingestIp",
            "ingest_port": "ingestPort",
            "max_bitrate": "maxBitrate",
            "max_latency": "maxLatency",
            "min_latency": "minLatency",
            "name": "name",
            "protocol": "protocol",
            "sender_control_port": "senderControlPort",
            "sender_ip_address": "senderIpAddress",
            "source_arn": "sourceArn",
            "source_ingest_port": "sourceIngestPort",
            "source_listener_address": "sourceListenerAddress",
            "source_listener_port": "sourceListenerPort",
            "stream_id": "streamId",
            "vpc_interface_name": "vpcInterfaceName",
            "whitelist_cidr": "whitelistCidr",
        },
    )
    class SourceProperty:
        def __init__(
            self,
            *,
            decryption: typing.Optional[typing.Union[typing.Union["CfnFlow.EncryptionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            description: typing.Optional[builtins.str] = None,
            entitlement_arn: typing.Optional[builtins.str] = None,
            ingest_ip: typing.Optional[builtins.str] = None,
            ingest_port: typing.Optional[jsii.Number] = None,
            max_bitrate: typing.Optional[jsii.Number] = None,
            max_latency: typing.Optional[jsii.Number] = None,
            min_latency: typing.Optional[jsii.Number] = None,
            name: typing.Optional[builtins.str] = None,
            protocol: typing.Optional[builtins.str] = None,
            sender_control_port: typing.Optional[jsii.Number] = None,
            sender_ip_address: typing.Optional[builtins.str] = None,
            source_arn: typing.Optional[builtins.str] = None,
            source_ingest_port: typing.Optional[builtins.str] = None,
            source_listener_address: typing.Optional[builtins.str] = None,
            source_listener_port: typing.Optional[jsii.Number] = None,
            stream_id: typing.Optional[builtins.str] = None,
            vpc_interface_name: typing.Optional[builtins.str] = None,
            whitelist_cidr: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The details of the sources of the flow.

            If you are creating a flow with a VPC source, you must first create the flow with a temporary standard source by doing the following:

            - Use CloudFormation to create a flow with a standard source that uses the flow’s public IP address.
            - Use CloudFormation to create the VPC interface to add to this flow. This can also be done as part of the previous step.
            - After CloudFormation has created the flow and the VPC interface, update the source to point to the VPC interface that you created.

            :param decryption: The type of encryption that is used on the content ingested from the source.
            :param description: A description of the source. This description is not visible outside of the current AWS account.
            :param entitlement_arn: The ARN of the entitlement that allows you to subscribe to content that comes from another AWS account. The entitlement is set by the content originator and the ARN is generated as part of the originator’s flow.
            :param ingest_ip: The IP address that the flow listens on for incoming content.
            :param ingest_port: The port that the flow listens on for incoming content. If the protocol of the source is Zixi, the port must be set to 2088.
            :param max_bitrate: The maximum bitrate for RIST, RTP, and RTP-FEC streams.
            :param max_latency: The maximum latency in milliseconds for a RIST or Zixi-based source.
            :param min_latency: The minimum latency in milliseconds for SRT-based streams. In streams that use the SRT protocol, this value that you set on your MediaConnect source or output represents the minimal potential latency of that connection. The latency of the stream is set to the highest number between the sender’s minimum latency and the receiver’s minimum latency.
            :param name: The name of the source.
            :param protocol: The protocol that is used by the source. AWS CloudFormation does not currently support CDI or ST 2110 JPEG XS source protocols.
            :param sender_control_port: The port that the flow uses to send outbound requests to initiate connection with the sender.
            :param sender_ip_address: The IP address that the flow communicates with to initiate connection with the sender.
            :param source_arn: The ARN of the source.
            :param source_ingest_port: The port that the flow will be listening on for incoming content.
            :param source_listener_address: Source IP or domain name for SRT-caller protocol.
            :param source_listener_port: Source port for SRT-caller protocol.
            :param stream_id: The stream ID that you want to use for the transport. This parameter applies only to Zixi-based streams.
            :param vpc_interface_name: The name of the VPC interface that the source content comes from.
            :param whitelist_cidr: The range of IP addresses that are allowed to contribute content to your source. Format the IP addresses as a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediaconnect as mediaconnect
                
                source_property = mediaconnect.CfnFlow.SourceProperty(
                    decryption=mediaconnect.CfnFlow.EncryptionProperty(
                        role_arn="roleArn",
                
                        # the properties below are optional
                        algorithm="algorithm",
                        constant_initialization_vector="constantInitializationVector",
                        device_id="deviceId",
                        key_type="keyType",
                        region="region",
                        resource_id="resourceId",
                        secret_arn="secretArn",
                        url="url"
                    ),
                    description="description",
                    entitlement_arn="entitlementArn",
                    ingest_ip="ingestIp",
                    ingest_port=123,
                    max_bitrate=123,
                    max_latency=123,
                    min_latency=123,
                    name="name",
                    protocol="protocol",
                    sender_control_port=123,
                    sender_ip_address="senderIpAddress",
                    source_arn="sourceArn",
                    source_ingest_port="sourceIngestPort",
                    source_listener_address="sourceListenerAddress",
                    source_listener_port=123,
                    stream_id="streamId",
                    vpc_interface_name="vpcInterfaceName",
                    whitelist_cidr="whitelistCidr"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9bacfc8576f0d9be4e32fc82a1bbf42fa275e9ad99357e29ed2501b502ed339a)
                check_type(argname="argument decryption", value=decryption, expected_type=type_hints["decryption"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument entitlement_arn", value=entitlement_arn, expected_type=type_hints["entitlement_arn"])
                check_type(argname="argument ingest_ip", value=ingest_ip, expected_type=type_hints["ingest_ip"])
                check_type(argname="argument ingest_port", value=ingest_port, expected_type=type_hints["ingest_port"])
                check_type(argname="argument max_bitrate", value=max_bitrate, expected_type=type_hints["max_bitrate"])
                check_type(argname="argument max_latency", value=max_latency, expected_type=type_hints["max_latency"])
                check_type(argname="argument min_latency", value=min_latency, expected_type=type_hints["min_latency"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument sender_control_port", value=sender_control_port, expected_type=type_hints["sender_control_port"])
                check_type(argname="argument sender_ip_address", value=sender_ip_address, expected_type=type_hints["sender_ip_address"])
                check_type(argname="argument source_arn", value=source_arn, expected_type=type_hints["source_arn"])
                check_type(argname="argument source_ingest_port", value=source_ingest_port, expected_type=type_hints["source_ingest_port"])
                check_type(argname="argument source_listener_address", value=source_listener_address, expected_type=type_hints["source_listener_address"])
                check_type(argname="argument source_listener_port", value=source_listener_port, expected_type=type_hints["source_listener_port"])
                check_type(argname="argument stream_id", value=stream_id, expected_type=type_hints["stream_id"])
                check_type(argname="argument vpc_interface_name", value=vpc_interface_name, expected_type=type_hints["vpc_interface_name"])
                check_type(argname="argument whitelist_cidr", value=whitelist_cidr, expected_type=type_hints["whitelist_cidr"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if decryption is not None:
                self._values["decryption"] = decryption
            if description is not None:
                self._values["description"] = description
            if entitlement_arn is not None:
                self._values["entitlement_arn"] = entitlement_arn
            if ingest_ip is not None:
                self._values["ingest_ip"] = ingest_ip
            if ingest_port is not None:
                self._values["ingest_port"] = ingest_port
            if max_bitrate is not None:
                self._values["max_bitrate"] = max_bitrate
            if max_latency is not None:
                self._values["max_latency"] = max_latency
            if min_latency is not None:
                self._values["min_latency"] = min_latency
            if name is not None:
                self._values["name"] = name
            if protocol is not None:
                self._values["protocol"] = protocol
            if sender_control_port is not None:
                self._values["sender_control_port"] = sender_control_port
            if sender_ip_address is not None:
                self._values["sender_ip_address"] = sender_ip_address
            if source_arn is not None:
                self._values["source_arn"] = source_arn
            if source_ingest_port is not None:
                self._values["source_ingest_port"] = source_ingest_port
            if source_listener_address is not None:
                self._values["source_listener_address"] = source_listener_address
            if source_listener_port is not None:
                self._values["source_listener_port"] = source_listener_port
            if stream_id is not None:
                self._values["stream_id"] = stream_id
            if vpc_interface_name is not None:
                self._values["vpc_interface_name"] = vpc_interface_name
            if whitelist_cidr is not None:
                self._values["whitelist_cidr"] = whitelist_cidr

        @builtins.property
        def decryption(
            self,
        ) -> typing.Optional[typing.Union["CfnFlow.EncryptionProperty", _IResolvable_a771d0ef]]:
            '''The type of encryption that is used on the content ingested from the source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-decryption
            '''
            result = self._values.get("decryption")
            return typing.cast(typing.Optional[typing.Union["CfnFlow.EncryptionProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description of the source.

            This description is not visible outside of the current AWS account.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def entitlement_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the entitlement that allows you to subscribe to content that comes from another AWS account.

            The entitlement is set by the content originator and the ARN is generated as part of the originator’s flow.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-entitlementarn
            '''
            result = self._values.get("entitlement_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ingest_ip(self) -> typing.Optional[builtins.str]:
            '''The IP address that the flow listens on for incoming content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-ingestip
            '''
            result = self._values.get("ingest_ip")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def ingest_port(self) -> typing.Optional[jsii.Number]:
            '''The port that the flow listens on for incoming content.

            If the protocol of the source is Zixi, the port must be set to 2088.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-ingestport
            '''
            result = self._values.get("ingest_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_bitrate(self) -> typing.Optional[jsii.Number]:
            '''The maximum bitrate for RIST, RTP, and RTP-FEC streams.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-maxbitrate
            '''
            result = self._values.get("max_bitrate")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_latency(self) -> typing.Optional[jsii.Number]:
            '''The maximum latency in milliseconds for a RIST or Zixi-based source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-maxlatency
            '''
            result = self._values.get("max_latency")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def min_latency(self) -> typing.Optional[jsii.Number]:
            '''The minimum latency in milliseconds for SRT-based streams.

            In streams that use the SRT protocol, this value that you set on your MediaConnect source or output represents the minimal potential latency of that connection. The latency of the stream is set to the highest number between the sender’s minimum latency and the receiver’s minimum latency.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-minlatency
            '''
            result = self._values.get("min_latency")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol that is used by the source.

            AWS CloudFormation does not currently support CDI or ST 2110 JPEG XS source protocols.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def sender_control_port(self) -> typing.Optional[jsii.Number]:
            '''The port that the flow uses to send outbound requests to initiate connection with the sender.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-sendercontrolport
            '''
            result = self._values.get("sender_control_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def sender_ip_address(self) -> typing.Optional[builtins.str]:
            '''The IP address that the flow communicates with to initiate connection with the sender.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-senderipaddress
            '''
            result = self._values.get("sender_ip_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the source.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-sourcearn
            '''
            result = self._values.get("source_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_ingest_port(self) -> typing.Optional[builtins.str]:
            '''The port that the flow will be listening on for incoming content.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-sourceingestport
            '''
            result = self._values.get("source_ingest_port")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_listener_address(self) -> typing.Optional[builtins.str]:
            '''Source IP or domain name for SRT-caller protocol.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-sourcelisteneraddress
            '''
            result = self._values.get("source_listener_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_listener_port(self) -> typing.Optional[jsii.Number]:
            '''Source port for SRT-caller protocol.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-sourcelistenerport
            '''
            result = self._values.get("source_listener_port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def stream_id(self) -> typing.Optional[builtins.str]:
            '''The stream ID that you want to use for the transport.

            This parameter applies only to Zixi-based streams.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-streamid
            '''
            result = self._values.get("stream_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def vpc_interface_name(self) -> typing.Optional[builtins.str]:
            '''The name of the VPC interface that the source content comes from.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-vpcinterfacename
            '''
            result = self._values.get("vpc_interface_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def whitelist_cidr(self) -> typing.Optional[builtins.str]:
            '''The range of IP addresses that are allowed to contribute content to your source.

            Format the IP addresses as a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flow-source.html#cfn-mediaconnect-flow-source-whitelistcidr
            '''
            result = self._values.get("whitelist_cidr")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnFlowEntitlement(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_mediaconnect.CfnFlowEntitlement",
):
    '''A CloudFormation ``AWS::MediaConnect::FlowEntitlement``.

    The AWS::MediaConnect::FlowEntitlement resource defines the permission that an AWS account grants to another AWS account to allow access to the content in a specific AWS Elemental MediaConnect flow. The content originator grants an entitlement to a specific AWS account (the subscriber). When an entitlement is granted, the subscriber can create a flow using the originator's flow as the source. Each flow can have up to 50 entitlements.

    :cloudformationResource: AWS::MediaConnect::FlowEntitlement
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_mediaconnect as mediaconnect
        
        cfn_flow_entitlement = mediaconnect.CfnFlowEntitlement(self, "MyCfnFlowEntitlement",
            description="description",
            flow_arn="flowArn",
            name="name",
            subscribers=["subscribers"],
        
            # the properties below are optional
            data_transfer_subscriber_fee_percent=123,
            encryption=mediaconnect.CfnFlowEntitlement.EncryptionProperty(
                algorithm="algorithm",
                role_arn="roleArn",
        
                # the properties below are optional
                constant_initialization_vector="constantInitializationVector",
                device_id="deviceId",
                key_type="keyType",
                region="region",
                resource_id="resourceId",
                secret_arn="secretArn",
                url="url"
            ),
            entitlement_status="entitlementStatus"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: builtins.str,
        flow_arn: builtins.str,
        name: builtins.str,
        subscribers: typing.Sequence[builtins.str],
        data_transfer_subscriber_fee_percent: typing.Optional[jsii.Number] = None,
        encryption: typing.Optional[typing.Union[typing.Union["CfnFlowEntitlement.EncryptionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        entitlement_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::MediaConnect::FlowEntitlement``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: A description of the entitlement. This description appears only on the MediaConnect console and is not visible outside of the current AWS account.
        :param flow_arn: The Amazon Resource Name (ARN) of the flow.
        :param name: The name of the entitlement. This value must be unique within the current flow.
        :param subscribers: The AWS account IDs that you want to share your content with. The receiving accounts (subscribers) will be allowed to create their own flows using your content as the source.
        :param data_transfer_subscriber_fee_percent: The percentage of the entitlement data transfer fee that you want the subscriber to be responsible for.
        :param encryption: The type of encryption that MediaConnect will use on the output that is associated with the entitlement.
        :param entitlement_status: An indication of whether the new entitlement should be enabled or disabled as soon as it is created. If you don’t specify the entitlementStatus field in your request, MediaConnect sets it to ENABLED.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18880888e4b71846ae07f794759e4b50a6d8bb1fdeb8d77d0b8c42c9296eb3d6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFlowEntitlementProps(
            description=description,
            flow_arn=flow_arn,
            name=name,
            subscribers=subscribers,
            data_transfer_subscriber_fee_percent=data_transfer_subscriber_fee_percent,
            encryption=encryption,
            entitlement_status=entitlement_status,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f15ff7c6c6fe5e27409e4a17a3fe4bcdac993a94c2176b0c5fff65f29ea75771)
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
            type_hints = typing.get_type_hints(_typecheckingstub__064cc526d8bfa90208606e94fb1132afdae6ce70457f8d140d59101b55fb3382)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrEntitlementArn")
    def attr_entitlement_arn(self) -> builtins.str:
        '''The entitlement ARN.

        :cloudformationAttribute: EntitlementArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEntitlementArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''A description of the entitlement.

        This description appears only on the MediaConnect console and is not visible outside of the current AWS account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-description
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8660fd0ef83e6bf995729002afb473891316c40e7673c6b33823c89adc7c6f68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="flowArn")
    def flow_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-flowarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "flowArn"))

    @flow_arn.setter
    def flow_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91535e402252ee56b5180debfa994bd9b2ccc4ee19e21db1bcabe2a18b2a9084)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flowArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the entitlement.

        This value must be unique within the current flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19cd78b7c63b00f4f068b5fc5fbd3615037e3d6c6af12b965bcebdc7bc820f55)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="subscribers")
    def subscribers(self) -> typing.List[builtins.str]:
        '''The AWS account IDs that you want to share your content with.

        The receiving accounts (subscribers) will be allowed to create their own flows using your content as the source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-subscribers
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "subscribers"))

    @subscribers.setter
    def subscribers(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c9a2c2f931bd42bc400ae5ffe45ca29f83b5d86fa9efb64889ebb86359553f9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subscribers", value)

    @builtins.property
    @jsii.member(jsii_name="dataTransferSubscriberFeePercent")
    def data_transfer_subscriber_fee_percent(self) -> typing.Optional[jsii.Number]:
        '''The percentage of the entitlement data transfer fee that you want the subscriber to be responsible for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-datatransfersubscriberfeepercent
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataTransferSubscriberFeePercent"))

    @data_transfer_subscriber_fee_percent.setter
    def data_transfer_subscriber_fee_percent(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0aaf7df2dd32084636437cb83c86925259f8e8baf5ee1b26a253fc52a93f25a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataTransferSubscriberFeePercent", value)

    @builtins.property
    @jsii.member(jsii_name="encryption")
    def encryption(
        self,
    ) -> typing.Optional[typing.Union["CfnFlowEntitlement.EncryptionProperty", _IResolvable_a771d0ef]]:
        '''The type of encryption that MediaConnect will use on the output that is associated with the entitlement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-encryption
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFlowEntitlement.EncryptionProperty", _IResolvable_a771d0ef]], jsii.get(self, "encryption"))

    @encryption.setter
    def encryption(
        self,
        value: typing.Optional[typing.Union["CfnFlowEntitlement.EncryptionProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6307d772cfa7e8d8c34220467717165a96d599387f06530dc33d46c0a6aeb832)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryption", value)

    @builtins.property
    @jsii.member(jsii_name="entitlementStatus")
    def entitlement_status(self) -> typing.Optional[builtins.str]:
        '''An indication of whether the new entitlement should be enabled or disabled as soon as it is created.

        If you don’t specify the entitlementStatus field in your request, MediaConnect sets it to ENABLED.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-entitlementstatus
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entitlementStatus"))

    @entitlement_status.setter
    def entitlement_status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf84e8be89c1109124a732ff8dc22b675622f35df70191b2eddb8287ec6cf0b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entitlementStatus", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_mediaconnect.CfnFlowEntitlement.EncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "algorithm": "algorithm",
            "role_arn": "roleArn",
            "constant_initialization_vector": "constantInitializationVector",
            "device_id": "deviceId",
            "key_type": "keyType",
            "region": "region",
            "resource_id": "resourceId",
            "secret_arn": "secretArn",
            "url": "url",
        },
    )
    class EncryptionProperty:
        def __init__(
            self,
            *,
            algorithm: builtins.str,
            role_arn: builtins.str,
            constant_initialization_vector: typing.Optional[builtins.str] = None,
            device_id: typing.Optional[builtins.str] = None,
            key_type: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
            resource_id: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the encryption of the flow.

            :param algorithm: The type of algorithm that is used for the encryption (such as aes128, aes192, or aes256).
            :param role_arn: The Amazon Resource Name (ARN) of the role that you created during setup (when you set up MediaConnect as a trusted entity).
            :param constant_initialization_vector: A 128-bit, 16-byte hex value represented by a 32-character string, to be used with the key for encrypting content. This parameter is not valid for static key encryption.
            :param device_id: The value of one of the devices that you configured with your digital rights management (DRM) platform key provider. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param key_type: The type of key that is used for the encryption. If you don't specify a ``keyType`` value, the service uses the default setting ( ``static-key`` ).
            :param region: The AWS Region that the API Gateway proxy endpoint was created in. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param resource_id: An identifier for the content. The service sends this value to the key server to identify the current endpoint. The resource ID is also known as the content ID. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param secret_arn: The ARN of the secret that you created in AWS Secrets Manager to store the encryption key.
            :param url: The URL from the API Gateway proxy that you set up to talk to your key server. This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediaconnect as mediaconnect
                
                encryption_property = mediaconnect.CfnFlowEntitlement.EncryptionProperty(
                    algorithm="algorithm",
                    role_arn="roleArn",
                
                    # the properties below are optional
                    constant_initialization_vector="constantInitializationVector",
                    device_id="deviceId",
                    key_type="keyType",
                    region="region",
                    resource_id="resourceId",
                    secret_arn="secretArn",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__78faac540172799eeb6b1066c6d0e2b6ae426d3830a9f1ba6b2aacf4e722747d)
                check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument constant_initialization_vector", value=constant_initialization_vector, expected_type=type_hints["constant_initialization_vector"])
                check_type(argname="argument device_id", value=device_id, expected_type=type_hints["device_id"])
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "algorithm": algorithm,
                "role_arn": role_arn,
            }
            if constant_initialization_vector is not None:
                self._values["constant_initialization_vector"] = constant_initialization_vector
            if device_id is not None:
                self._values["device_id"] = device_id
            if key_type is not None:
                self._values["key_type"] = key_type
            if region is not None:
                self._values["region"] = region
            if resource_id is not None:
                self._values["resource_id"] = resource_id
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def algorithm(self) -> builtins.str:
            '''The type of algorithm that is used for the encryption (such as aes128, aes192, or aes256).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-algorithm
            '''
            result = self._values.get("algorithm")
            assert result is not None, "Required property 'algorithm' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def role_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the role that you created during setup (when you set up MediaConnect as a trusted entity).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-rolearn
            '''
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def constant_initialization_vector(self) -> typing.Optional[builtins.str]:
            '''A 128-bit, 16-byte hex value represented by a 32-character string, to be used with the key for encrypting content.

            This parameter is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-constantinitializationvector
            '''
            result = self._values.get("constant_initialization_vector")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_id(self) -> typing.Optional[builtins.str]:
            '''The value of one of the devices that you configured with your digital rights management (DRM) platform key provider.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-deviceid
            '''
            result = self._values.get("device_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_type(self) -> typing.Optional[builtins.str]:
            '''The type of key that is used for the encryption.

            If you don't specify a ``keyType`` value, the service uses the default setting ( ``static-key`` ).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-keytype
            '''
            result = self._values.get("key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region that the API Gateway proxy endpoint was created in.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_id(self) -> typing.Optional[builtins.str]:
            '''An identifier for the content.

            The service sends this value to the key server to identify the current endpoint. The resource ID is also known as the content ID. This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-resourceid
            '''
            result = self._values.get("resource_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the secret that you created in AWS Secrets Manager to store the encryption key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL from the API Gateway proxy that you set up to talk to your key server.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowentitlement-encryption.html#cfn-mediaconnect-flowentitlement-encryption-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_mediaconnect.CfnFlowEntitlementProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "flow_arn": "flowArn",
        "name": "name",
        "subscribers": "subscribers",
        "data_transfer_subscriber_fee_percent": "dataTransferSubscriberFeePercent",
        "encryption": "encryption",
        "entitlement_status": "entitlementStatus",
    },
)
class CfnFlowEntitlementProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        flow_arn: builtins.str,
        name: builtins.str,
        subscribers: typing.Sequence[builtins.str],
        data_transfer_subscriber_fee_percent: typing.Optional[jsii.Number] = None,
        encryption: typing.Optional[typing.Union[typing.Union[CfnFlowEntitlement.EncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        entitlement_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnFlowEntitlement``.

        :param description: A description of the entitlement. This description appears only on the MediaConnect console and is not visible outside of the current AWS account.
        :param flow_arn: The Amazon Resource Name (ARN) of the flow.
        :param name: The name of the entitlement. This value must be unique within the current flow.
        :param subscribers: The AWS account IDs that you want to share your content with. The receiving accounts (subscribers) will be allowed to create their own flows using your content as the source.
        :param data_transfer_subscriber_fee_percent: The percentage of the entitlement data transfer fee that you want the subscriber to be responsible for.
        :param encryption: The type of encryption that MediaConnect will use on the output that is associated with the entitlement.
        :param entitlement_status: An indication of whether the new entitlement should be enabled or disabled as soon as it is created. If you don’t specify the entitlementStatus field in your request, MediaConnect sets it to ENABLED.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_mediaconnect as mediaconnect
            
            cfn_flow_entitlement_props = mediaconnect.CfnFlowEntitlementProps(
                description="description",
                flow_arn="flowArn",
                name="name",
                subscribers=["subscribers"],
            
                # the properties below are optional
                data_transfer_subscriber_fee_percent=123,
                encryption=mediaconnect.CfnFlowEntitlement.EncryptionProperty(
                    algorithm="algorithm",
                    role_arn="roleArn",
            
                    # the properties below are optional
                    constant_initialization_vector="constantInitializationVector",
                    device_id="deviceId",
                    key_type="keyType",
                    region="region",
                    resource_id="resourceId",
                    secret_arn="secretArn",
                    url="url"
                ),
                entitlement_status="entitlementStatus"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2b9bdfc2cc118279a2b87ae533b7cad4db373b533b3405acee867d9928a7798)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument flow_arn", value=flow_arn, expected_type=type_hints["flow_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subscribers", value=subscribers, expected_type=type_hints["subscribers"])
            check_type(argname="argument data_transfer_subscriber_fee_percent", value=data_transfer_subscriber_fee_percent, expected_type=type_hints["data_transfer_subscriber_fee_percent"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument entitlement_status", value=entitlement_status, expected_type=type_hints["entitlement_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "flow_arn": flow_arn,
            "name": name,
            "subscribers": subscribers,
        }
        if data_transfer_subscriber_fee_percent is not None:
            self._values["data_transfer_subscriber_fee_percent"] = data_transfer_subscriber_fee_percent
        if encryption is not None:
            self._values["encryption"] = encryption
        if entitlement_status is not None:
            self._values["entitlement_status"] = entitlement_status

    @builtins.property
    def description(self) -> builtins.str:
        '''A description of the entitlement.

        This description appears only on the MediaConnect console and is not visible outside of the current AWS account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def flow_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-flowarn
        '''
        result = self._values.get("flow_arn")
        assert result is not None, "Required property 'flow_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the entitlement.

        This value must be unique within the current flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subscribers(self) -> typing.List[builtins.str]:
        '''The AWS account IDs that you want to share your content with.

        The receiving accounts (subscribers) will be allowed to create their own flows using your content as the source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-subscribers
        '''
        result = self._values.get("subscribers")
        assert result is not None, "Required property 'subscribers' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def data_transfer_subscriber_fee_percent(self) -> typing.Optional[jsii.Number]:
        '''The percentage of the entitlement data transfer fee that you want the subscriber to be responsible for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-datatransfersubscriberfeepercent
        '''
        result = self._values.get("data_transfer_subscriber_fee_percent")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def encryption(
        self,
    ) -> typing.Optional[typing.Union[CfnFlowEntitlement.EncryptionProperty, _IResolvable_a771d0ef]]:
        '''The type of encryption that MediaConnect will use on the output that is associated with the entitlement.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-encryption
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[typing.Union[CfnFlowEntitlement.EncryptionProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def entitlement_status(self) -> typing.Optional[builtins.str]:
        '''An indication of whether the new entitlement should be enabled or disabled as soon as it is created.

        If you don’t specify the entitlementStatus field in your request, MediaConnect sets it to ENABLED.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowentitlement.html#cfn-mediaconnect-flowentitlement-entitlementstatus
        '''
        result = self._values.get("entitlement_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFlowEntitlementProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnFlowOutput(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_mediaconnect.CfnFlowOutput",
):
    '''A CloudFormation ``AWS::MediaConnect::FlowOutput``.

    The AWS::MediaConnect::FlowOutput resource defines the destination address, protocol, and port that AWS Elemental MediaConnect sends the ingested video to. Each flow can have up to 50 outputs. An output can have the same protocol or a different protocol from the source. The following protocols are supported: RIST, RTP, RTP-FEC, SRT-listener, SRT-caller, Zixi pull, Zixi push, and Fujitsu-QoS. CDI and ST 2110 JPEG XS protocols are not currently supported by AWS CloudFormation.

    :cloudformationResource: AWS::MediaConnect::FlowOutput
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_mediaconnect as mediaconnect
        
        cfn_flow_output = mediaconnect.CfnFlowOutput(self, "MyCfnFlowOutput",
            flow_arn="flowArn",
            protocol="protocol",
        
            # the properties below are optional
            cidr_allow_list=["cidrAllowList"],
            description="description",
            destination="destination",
            encryption=mediaconnect.CfnFlowOutput.EncryptionProperty(
                role_arn="roleArn",
                secret_arn="secretArn",
        
                # the properties below are optional
                algorithm="algorithm",
                key_type="keyType"
            ),
            max_latency=123,
            min_latency=123,
            name="name",
            port=123,
            remote_id="remoteId",
            smoothing_latency=123,
            stream_id="streamId",
            vpc_interface_attachment=mediaconnect.CfnFlowOutput.VpcInterfaceAttachmentProperty(
                vpc_interface_name="vpcInterfaceName"
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        flow_arn: builtins.str,
        protocol: builtins.str,
        cidr_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        destination: typing.Optional[builtins.str] = None,
        encryption: typing.Optional[typing.Union[typing.Union["CfnFlowOutput.EncryptionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        max_latency: typing.Optional[jsii.Number] = None,
        min_latency: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        remote_id: typing.Optional[builtins.str] = None,
        smoothing_latency: typing.Optional[jsii.Number] = None,
        stream_id: typing.Optional[builtins.str] = None,
        vpc_interface_attachment: typing.Optional[typing.Union[typing.Union["CfnFlowOutput.VpcInterfaceAttachmentProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::MediaConnect::FlowOutput``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param flow_arn: The Amazon Resource Name (ARN) of the flow this output is attached to.
        :param protocol: The protocol to use for the output.
        :param cidr_allow_list: The range of IP addresses that are allowed to initiate output requests to this flow. Format the IP addresses as a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.
        :param description: A description of the output. This description is not visible outside of the current AWS account even if the account grants entitlements to other accounts.
        :param destination: The IP address where you want to send the output.
        :param encryption: The encryption credentials that you want to use for the output.
        :param max_latency: The maximum latency in milliseconds. This parameter applies only to RIST-based, Zixi-based, and Fujitsu-based streams.
        :param min_latency: The minimum latency in milliseconds for SRT-based streams. In streams that use the SRT protocol, this value that you set on your MediaConnect source or output represents the minimal potential latency of that connection. The latency of the stream is set to the highest number between the sender’s minimum latency and the receiver’s minimum latency.
        :param name: The name of the VPC interface.
        :param port: The port to use when MediaConnect distributes content to the output.
        :param remote_id: The identifier that is assigned to the Zixi receiver. This parameter applies only to outputs that use Zixi pull.
        :param smoothing_latency: The smoothing latency in milliseconds for RIST, RTP, and RTP-FEC streams.
        :param stream_id: The stream ID that you want to use for this transport. This parameter applies only to Zixi and SRT caller-based streams.
        :param vpc_interface_attachment: The VPC interface that you want to send your output to.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__783a86052e919a1ec9b2f7e162ba0ae621fc030564aafecff1ef4bc4de1c4582)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFlowOutputProps(
            flow_arn=flow_arn,
            protocol=protocol,
            cidr_allow_list=cidr_allow_list,
            description=description,
            destination=destination,
            encryption=encryption,
            max_latency=max_latency,
            min_latency=min_latency,
            name=name,
            port=port,
            remote_id=remote_id,
            smoothing_latency=smoothing_latency,
            stream_id=stream_id,
            vpc_interface_attachment=vpc_interface_attachment,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be7aa6364d3ec5bb4fd8c022307a3160b129b6fb3e85be1eeaa1b14b1ef1f6bb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7fdd1caaccc701d4686c89e023afb1433d009ea6d5a3b45a5a393e87ff31fcd)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrOutputArn")
    def attr_output_arn(self) -> builtins.str:
        '''The ARN of the output.

        :cloudformationAttribute: OutputArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOutputArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="flowArn")
    def flow_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the flow this output is attached to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-flowarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "flowArn"))

    @flow_arn.setter
    def flow_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64d2fb856996b0e0e76e621d058cbb48c0a6e1e3cc2259c413554b1cebca57fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flowArn", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        '''The protocol to use for the output.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-protocol
        '''
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc6aaa5b559d34a41e6293ad6ce506b7c25a4872c4c2c0405926a0acca3f3a42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="cidrAllowList")
    def cidr_allow_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The range of IP addresses that are allowed to initiate output requests to this flow.

        Format the IP addresses as a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-cidrallowlist
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "cidrAllowList"))

    @cidr_allow_list.setter
    def cidr_allow_list(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1f44c8ef17b12239b984d17b709453754e6481386d73ceaed6d5e8bfb579cf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cidrAllowList", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the output.

        This description is not visible outside of the current AWS account even if the account grants entitlements to other accounts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ba848510921aa4d87cb5e839761513aafc12c7d5940ee1b1627daf66668b95f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="destination")
    def destination(self) -> typing.Optional[builtins.str]:
        '''The IP address where you want to send the output.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-destination
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destination"))

    @destination.setter
    def destination(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90e1311bc6a0d826a0bd66cedb1af8462a12bd7eda423a53c852f0d16ff5df58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destination", value)

    @builtins.property
    @jsii.member(jsii_name="encryption")
    def encryption(
        self,
    ) -> typing.Optional[typing.Union["CfnFlowOutput.EncryptionProperty", _IResolvable_a771d0ef]]:
        '''The encryption credentials that you want to use for the output.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-encryption
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFlowOutput.EncryptionProperty", _IResolvable_a771d0ef]], jsii.get(self, "encryption"))

    @encryption.setter
    def encryption(
        self,
        value: typing.Optional[typing.Union["CfnFlowOutput.EncryptionProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0193cc392c9bf77ccba750573777e6719c1545c8ba88f9c06de1066d166a3d9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "encryption", value)

    @builtins.property
    @jsii.member(jsii_name="maxLatency")
    def max_latency(self) -> typing.Optional[jsii.Number]:
        '''The maximum latency in milliseconds.

        This parameter applies only to RIST-based, Zixi-based, and Fujitsu-based streams.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-maxlatency
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxLatency"))

    @max_latency.setter
    def max_latency(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ab9e471bbdfe7ac9786e44dbdf5748db8b9fe344ca6679ffff81e8c78c13264)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxLatency", value)

    @builtins.property
    @jsii.member(jsii_name="minLatency")
    def min_latency(self) -> typing.Optional[jsii.Number]:
        '''The minimum latency in milliseconds for SRT-based streams.

        In streams that use the SRT protocol, this value that you set on your MediaConnect source or output represents the minimal potential latency of that connection. The latency of the stream is set to the highest number between the sender’s minimum latency and the receiver’s minimum latency.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-minlatency
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "minLatency"))

    @min_latency.setter
    def min_latency(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18d53969d6da0b0807de0e0ad5537b749a20ea51392c9a8a49b17c2c67f27f66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "minLatency", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the VPC interface.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8d88988f89160f89533ec5442856f41a14d11d775ff9ce560d9d16407e1581d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port to use when MediaConnect distributes content to the output.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-port
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "port"))

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__494cb6e520d7a1efafda911460d1377f2e593f30a7de4e7591e7d792db0d2737)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="remoteId")
    def remote_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that is assigned to the Zixi receiver.

        This parameter applies only to outputs that use Zixi pull.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-remoteid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "remoteId"))

    @remote_id.setter
    def remote_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aaf07cc2b6ca5470f39dbe47538f98bc9335c2ca0515d29e0aa26183334359e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remoteId", value)

    @builtins.property
    @jsii.member(jsii_name="smoothingLatency")
    def smoothing_latency(self) -> typing.Optional[jsii.Number]:
        '''The smoothing latency in milliseconds for RIST, RTP, and RTP-FEC streams.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-smoothinglatency
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "smoothingLatency"))

    @smoothing_latency.setter
    def smoothing_latency(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6210f516674e4667d9afbc11fe71bef0a715f86c8eb2ea23e37883ea6cc5f95f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "smoothingLatency", value)

    @builtins.property
    @jsii.member(jsii_name="streamId")
    def stream_id(self) -> typing.Optional[builtins.str]:
        '''The stream ID that you want to use for this transport.

        This parameter applies only to Zixi and SRT caller-based streams.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-streamid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamId"))

    @stream_id.setter
    def stream_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb1682ee60a28ddeb3533a188ce74e61e7fe77715ebe440575b8e3f6833b9ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamId", value)

    @builtins.property
    @jsii.member(jsii_name="vpcInterfaceAttachment")
    def vpc_interface_attachment(
        self,
    ) -> typing.Optional[typing.Union["CfnFlowOutput.VpcInterfaceAttachmentProperty", _IResolvable_a771d0ef]]:
        '''The VPC interface that you want to send your output to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-vpcinterfaceattachment
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFlowOutput.VpcInterfaceAttachmentProperty", _IResolvable_a771d0ef]], jsii.get(self, "vpcInterfaceAttachment"))

    @vpc_interface_attachment.setter
    def vpc_interface_attachment(
        self,
        value: typing.Optional[typing.Union["CfnFlowOutput.VpcInterfaceAttachmentProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26e5a3703efaa0ec3e944402910679953cd697fed4e858ec095a2cc6dde07cf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcInterfaceAttachment", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_mediaconnect.CfnFlowOutput.EncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "role_arn": "roleArn",
            "secret_arn": "secretArn",
            "algorithm": "algorithm",
            "key_type": "keyType",
        },
    )
    class EncryptionProperty:
        def __init__(
            self,
            *,
            role_arn: builtins.str,
            secret_arn: builtins.str,
            algorithm: typing.Optional[builtins.str] = None,
            key_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the encryption of the flow.

            :param role_arn: The Amazon Resource Name (ARN) of the role that you created during setup (when you set up MediaConnect as a trusted entity).
            :param secret_arn: The ARN of the secret that you created in AWS Secrets Manager to store the encryption key.
            :param algorithm: The type of algorithm that is used for the encryption (such as aes128, aes192, or aes256).
            :param key_type: The type of key that is used for the encryption. If you don't specify a ``keyType`` value, the service uses the default setting ( ``static-key`` ).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-encryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediaconnect as mediaconnect
                
                encryption_property = mediaconnect.CfnFlowOutput.EncryptionProperty(
                    role_arn="roleArn",
                    secret_arn="secretArn",
                
                    # the properties below are optional
                    algorithm="algorithm",
                    key_type="keyType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__65a2f411484c3a4bc259cbf6a8e0c219ea553db2bdb680d8f95abd71df584045)
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "role_arn": role_arn,
                "secret_arn": secret_arn,
            }
            if algorithm is not None:
                self._values["algorithm"] = algorithm
            if key_type is not None:
                self._values["key_type"] = key_type

        @builtins.property
        def role_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the role that you created during setup (when you set up MediaConnect as a trusted entity).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-encryption.html#cfn-mediaconnect-flowoutput-encryption-rolearn
            '''
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def secret_arn(self) -> builtins.str:
            '''The ARN of the secret that you created in AWS Secrets Manager to store the encryption key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-encryption.html#cfn-mediaconnect-flowoutput-encryption-secretarn
            '''
            result = self._values.get("secret_arn")
            assert result is not None, "Required property 'secret_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def algorithm(self) -> typing.Optional[builtins.str]:
            '''The type of algorithm that is used for the encryption (such as aes128, aes192, or aes256).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-encryption.html#cfn-mediaconnect-flowoutput-encryption-algorithm
            '''
            result = self._values.get("algorithm")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_type(self) -> typing.Optional[builtins.str]:
            '''The type of key that is used for the encryption.

            If you don't specify a ``keyType`` value, the service uses the default setting ( ``static-key`` ).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-encryption.html#cfn-mediaconnect-flowoutput-encryption-keytype
            '''
            result = self._values.get("key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_mediaconnect.CfnFlowOutput.VpcInterfaceAttachmentProperty",
        jsii_struct_bases=[],
        name_mapping={"vpc_interface_name": "vpcInterfaceName"},
    )
    class VpcInterfaceAttachmentProperty:
        def __init__(
            self,
            *,
            vpc_interface_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The VPC interface that you want to send your output to.

            :param vpc_interface_name: The name of the VPC interface that you want to send your output to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-vpcinterfaceattachment.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediaconnect as mediaconnect
                
                vpc_interface_attachment_property = mediaconnect.CfnFlowOutput.VpcInterfaceAttachmentProperty(
                    vpc_interface_name="vpcInterfaceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a74863b23494168aab7acbef025f3c39f979c5cc7c2de5440f5494b398728846)
                check_type(argname="argument vpc_interface_name", value=vpc_interface_name, expected_type=type_hints["vpc_interface_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if vpc_interface_name is not None:
                self._values["vpc_interface_name"] = vpc_interface_name

        @builtins.property
        def vpc_interface_name(self) -> typing.Optional[builtins.str]:
            '''The name of the VPC interface that you want to send your output to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowoutput-vpcinterfaceattachment.html#cfn-mediaconnect-flowoutput-vpcinterfaceattachment-vpcinterfacename
            '''
            result = self._values.get("vpc_interface_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VpcInterfaceAttachmentProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_mediaconnect.CfnFlowOutputProps",
    jsii_struct_bases=[],
    name_mapping={
        "flow_arn": "flowArn",
        "protocol": "protocol",
        "cidr_allow_list": "cidrAllowList",
        "description": "description",
        "destination": "destination",
        "encryption": "encryption",
        "max_latency": "maxLatency",
        "min_latency": "minLatency",
        "name": "name",
        "port": "port",
        "remote_id": "remoteId",
        "smoothing_latency": "smoothingLatency",
        "stream_id": "streamId",
        "vpc_interface_attachment": "vpcInterfaceAttachment",
    },
)
class CfnFlowOutputProps:
    def __init__(
        self,
        *,
        flow_arn: builtins.str,
        protocol: builtins.str,
        cidr_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        description: typing.Optional[builtins.str] = None,
        destination: typing.Optional[builtins.str] = None,
        encryption: typing.Optional[typing.Union[typing.Union[CfnFlowOutput.EncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        max_latency: typing.Optional[jsii.Number] = None,
        min_latency: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        remote_id: typing.Optional[builtins.str] = None,
        smoothing_latency: typing.Optional[jsii.Number] = None,
        stream_id: typing.Optional[builtins.str] = None,
        vpc_interface_attachment: typing.Optional[typing.Union[typing.Union[CfnFlowOutput.VpcInterfaceAttachmentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnFlowOutput``.

        :param flow_arn: The Amazon Resource Name (ARN) of the flow this output is attached to.
        :param protocol: The protocol to use for the output.
        :param cidr_allow_list: The range of IP addresses that are allowed to initiate output requests to this flow. Format the IP addresses as a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.
        :param description: A description of the output. This description is not visible outside of the current AWS account even if the account grants entitlements to other accounts.
        :param destination: The IP address where you want to send the output.
        :param encryption: The encryption credentials that you want to use for the output.
        :param max_latency: The maximum latency in milliseconds. This parameter applies only to RIST-based, Zixi-based, and Fujitsu-based streams.
        :param min_latency: The minimum latency in milliseconds for SRT-based streams. In streams that use the SRT protocol, this value that you set on your MediaConnect source or output represents the minimal potential latency of that connection. The latency of the stream is set to the highest number between the sender’s minimum latency and the receiver’s minimum latency.
        :param name: The name of the VPC interface.
        :param port: The port to use when MediaConnect distributes content to the output.
        :param remote_id: The identifier that is assigned to the Zixi receiver. This parameter applies only to outputs that use Zixi pull.
        :param smoothing_latency: The smoothing latency in milliseconds for RIST, RTP, and RTP-FEC streams.
        :param stream_id: The stream ID that you want to use for this transport. This parameter applies only to Zixi and SRT caller-based streams.
        :param vpc_interface_attachment: The VPC interface that you want to send your output to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_mediaconnect as mediaconnect
            
            cfn_flow_output_props = mediaconnect.CfnFlowOutputProps(
                flow_arn="flowArn",
                protocol="protocol",
            
                # the properties below are optional
                cidr_allow_list=["cidrAllowList"],
                description="description",
                destination="destination",
                encryption=mediaconnect.CfnFlowOutput.EncryptionProperty(
                    role_arn="roleArn",
                    secret_arn="secretArn",
            
                    # the properties below are optional
                    algorithm="algorithm",
                    key_type="keyType"
                ),
                max_latency=123,
                min_latency=123,
                name="name",
                port=123,
                remote_id="remoteId",
                smoothing_latency=123,
                stream_id="streamId",
                vpc_interface_attachment=mediaconnect.CfnFlowOutput.VpcInterfaceAttachmentProperty(
                    vpc_interface_name="vpcInterfaceName"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccba2126e06e8c24a6d8916a495ec85e9612d70179092776b8f9f29bd7a87243)
            check_type(argname="argument flow_arn", value=flow_arn, expected_type=type_hints["flow_arn"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument cidr_allow_list", value=cidr_allow_list, expected_type=type_hints["cidr_allow_list"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
            check_type(argname="argument encryption", value=encryption, expected_type=type_hints["encryption"])
            check_type(argname="argument max_latency", value=max_latency, expected_type=type_hints["max_latency"])
            check_type(argname="argument min_latency", value=min_latency, expected_type=type_hints["min_latency"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument remote_id", value=remote_id, expected_type=type_hints["remote_id"])
            check_type(argname="argument smoothing_latency", value=smoothing_latency, expected_type=type_hints["smoothing_latency"])
            check_type(argname="argument stream_id", value=stream_id, expected_type=type_hints["stream_id"])
            check_type(argname="argument vpc_interface_attachment", value=vpc_interface_attachment, expected_type=type_hints["vpc_interface_attachment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "flow_arn": flow_arn,
            "protocol": protocol,
        }
        if cidr_allow_list is not None:
            self._values["cidr_allow_list"] = cidr_allow_list
        if description is not None:
            self._values["description"] = description
        if destination is not None:
            self._values["destination"] = destination
        if encryption is not None:
            self._values["encryption"] = encryption
        if max_latency is not None:
            self._values["max_latency"] = max_latency
        if min_latency is not None:
            self._values["min_latency"] = min_latency
        if name is not None:
            self._values["name"] = name
        if port is not None:
            self._values["port"] = port
        if remote_id is not None:
            self._values["remote_id"] = remote_id
        if smoothing_latency is not None:
            self._values["smoothing_latency"] = smoothing_latency
        if stream_id is not None:
            self._values["stream_id"] = stream_id
        if vpc_interface_attachment is not None:
            self._values["vpc_interface_attachment"] = vpc_interface_attachment

    @builtins.property
    def flow_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the flow this output is attached to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-flowarn
        '''
        result = self._values.get("flow_arn")
        assert result is not None, "Required property 'flow_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''The protocol to use for the output.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-protocol
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cidr_allow_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The range of IP addresses that are allowed to initiate output requests to this flow.

        Format the IP addresses as a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-cidrallowlist
        '''
        result = self._values.get("cidr_allow_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the output.

        This description is not visible outside of the current AWS account even if the account grants entitlements to other accounts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def destination(self) -> typing.Optional[builtins.str]:
        '''The IP address where you want to send the output.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-destination
        '''
        result = self._values.get("destination")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption(
        self,
    ) -> typing.Optional[typing.Union[CfnFlowOutput.EncryptionProperty, _IResolvable_a771d0ef]]:
        '''The encryption credentials that you want to use for the output.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-encryption
        '''
        result = self._values.get("encryption")
        return typing.cast(typing.Optional[typing.Union[CfnFlowOutput.EncryptionProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def max_latency(self) -> typing.Optional[jsii.Number]:
        '''The maximum latency in milliseconds.

        This parameter applies only to RIST-based, Zixi-based, and Fujitsu-based streams.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-maxlatency
        '''
        result = self._values.get("max_latency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def min_latency(self) -> typing.Optional[jsii.Number]:
        '''The minimum latency in milliseconds for SRT-based streams.

        In streams that use the SRT protocol, this value that you set on your MediaConnect source or output represents the minimal potential latency of that connection. The latency of the stream is set to the highest number between the sender’s minimum latency and the receiver’s minimum latency.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-minlatency
        '''
        result = self._values.get("min_latency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the VPC interface.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The port to use when MediaConnect distributes content to the output.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def remote_id(self) -> typing.Optional[builtins.str]:
        '''The identifier that is assigned to the Zixi receiver.

        This parameter applies only to outputs that use Zixi pull.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-remoteid
        '''
        result = self._values.get("remote_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def smoothing_latency(self) -> typing.Optional[jsii.Number]:
        '''The smoothing latency in milliseconds for RIST, RTP, and RTP-FEC streams.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-smoothinglatency
        '''
        result = self._values.get("smoothing_latency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stream_id(self) -> typing.Optional[builtins.str]:
        '''The stream ID that you want to use for this transport.

        This parameter applies only to Zixi and SRT caller-based streams.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-streamid
        '''
        result = self._values.get("stream_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_interface_attachment(
        self,
    ) -> typing.Optional[typing.Union[CfnFlowOutput.VpcInterfaceAttachmentProperty, _IResolvable_a771d0ef]]:
        '''The VPC interface that you want to send your output to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowoutput.html#cfn-mediaconnect-flowoutput-vpcinterfaceattachment
        '''
        result = self._values.get("vpc_interface_attachment")
        return typing.cast(typing.Optional[typing.Union[CfnFlowOutput.VpcInterfaceAttachmentProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFlowOutputProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_mediaconnect.CfnFlowProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "source": "source",
        "availability_zone": "availabilityZone",
        "source_failover_config": "sourceFailoverConfig",
    },
)
class CfnFlowProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        source: typing.Union[typing.Union[CfnFlow.SourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        availability_zone: typing.Optional[builtins.str] = None,
        source_failover_config: typing.Optional[typing.Union[typing.Union[CfnFlow.FailoverConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnFlow``.

        :param name: The name of the flow.
        :param source: The settings for the source that you want to use for the new flow.
        :param availability_zone: The Availability Zone that you want to create the flow in. These options are limited to the Availability Zones within the current AWS Region.
        :param source_failover_config: The settings for source failover.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_mediaconnect as mediaconnect
            
            cfn_flow_props = mediaconnect.CfnFlowProps(
                name="name",
                source=mediaconnect.CfnFlow.SourceProperty(
                    decryption=mediaconnect.CfnFlow.EncryptionProperty(
                        role_arn="roleArn",
            
                        # the properties below are optional
                        algorithm="algorithm",
                        constant_initialization_vector="constantInitializationVector",
                        device_id="deviceId",
                        key_type="keyType",
                        region="region",
                        resource_id="resourceId",
                        secret_arn="secretArn",
                        url="url"
                    ),
                    description="description",
                    entitlement_arn="entitlementArn",
                    ingest_ip="ingestIp",
                    ingest_port=123,
                    max_bitrate=123,
                    max_latency=123,
                    min_latency=123,
                    name="name",
                    protocol="protocol",
                    sender_control_port=123,
                    sender_ip_address="senderIpAddress",
                    source_arn="sourceArn",
                    source_ingest_port="sourceIngestPort",
                    source_listener_address="sourceListenerAddress",
                    source_listener_port=123,
                    stream_id="streamId",
                    vpc_interface_name="vpcInterfaceName",
                    whitelist_cidr="whitelistCidr"
                ),
            
                # the properties below are optional
                availability_zone="availabilityZone",
                source_failover_config=mediaconnect.CfnFlow.FailoverConfigProperty(
                    failover_mode="failoverMode",
                    recovery_window=123,
                    source_priority=mediaconnect.CfnFlow.SourcePriorityProperty(
                        primary_source="primarySource"
                    ),
                    state="state"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02242ddd9efca6abff6b707b9a5c619a997606384b1a9d68360bbc246e7812aa)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
            check_type(argname="argument source_failover_config", value=source_failover_config, expected_type=type_hints["source_failover_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "source": source,
        }
        if availability_zone is not None:
            self._values["availability_zone"] = availability_zone
        if source_failover_config is not None:
            self._values["source_failover_config"] = source_failover_config

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source(self) -> typing.Union[CfnFlow.SourceProperty, _IResolvable_a771d0ef]:
        '''The settings for the source that you want to use for the new flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-source
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(typing.Union[CfnFlow.SourceProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def availability_zone(self) -> typing.Optional[builtins.str]:
        '''The Availability Zone that you want to create the flow in.

        These options are limited to the Availability Zones within the current AWS Region.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-availabilityzone
        '''
        result = self._values.get("availability_zone")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_failover_config(
        self,
    ) -> typing.Optional[typing.Union[CfnFlow.FailoverConfigProperty, _IResolvable_a771d0ef]]:
        '''The settings for source failover.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flow.html#cfn-mediaconnect-flow-sourcefailoverconfig
        '''
        result = self._values.get("source_failover_config")
        return typing.cast(typing.Optional[typing.Union[CfnFlow.FailoverConfigProperty, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFlowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnFlowSource(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_mediaconnect.CfnFlowSource",
):
    '''A CloudFormation ``AWS::MediaConnect::FlowSource``.

    The AWS::MediaConnect::FlowSource resource is used to add additional sources to an existing flow. Adding an additional source requires Failover to be enabled. When you enable Failover, the additional source must use the same protocol as the existing source. A source is the external video content that includes configuration information (encryption and source type) and a network address. Each flow has at least one source. A standard source comes from a source other than another AWS Elemental MediaConnect flow, such as an on-premises encoder.

    :cloudformationResource: AWS::MediaConnect::FlowSource
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_mediaconnect as mediaconnect
        
        cfn_flow_source = mediaconnect.CfnFlowSource(self, "MyCfnFlowSource",
            description="description",
            name="name",
        
            # the properties below are optional
            decryption=mediaconnect.CfnFlowSource.EncryptionProperty(
                algorithm="algorithm",
                role_arn="roleArn",
        
                # the properties below are optional
                constant_initialization_vector="constantInitializationVector",
                device_id="deviceId",
                key_type="keyType",
                region="region",
                resource_id="resourceId",
                secret_arn="secretArn",
                url="url"
            ),
            entitlement_arn="entitlementArn",
            flow_arn="flowArn",
            ingest_port=123,
            max_bitrate=123,
            max_latency=123,
            protocol="protocol",
            stream_id="streamId",
            vpc_interface_name="vpcInterfaceName",
            whitelist_cidr="whitelistCidr"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        description: builtins.str,
        name: builtins.str,
        decryption: typing.Optional[typing.Union[typing.Union["CfnFlowSource.EncryptionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        entitlement_arn: typing.Optional[builtins.str] = None,
        flow_arn: typing.Optional[builtins.str] = None,
        ingest_port: typing.Optional[jsii.Number] = None,
        max_bitrate: typing.Optional[jsii.Number] = None,
        max_latency: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        stream_id: typing.Optional[builtins.str] = None,
        vpc_interface_name: typing.Optional[builtins.str] = None,
        whitelist_cidr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::MediaConnect::FlowSource``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: A description of the source. This description is not visible outside of the current AWS account.
        :param name: The name of the source.
        :param decryption: The type of encryption that is used on the content ingested from the source.
        :param entitlement_arn: The ARN of the entitlement that allows you to subscribe to the flow. The entitlement is set by the content originator, and the ARN is generated as part of the originator's flow.
        :param flow_arn: The Amazon Resource Name (ARN) of the flow this source is connected to. The flow must have Failover enabled to add an additional source.
        :param ingest_port: The port that the flow listens on for incoming content. If the protocol of the source is Zixi, the port must be set to 2088.
        :param max_bitrate: The maximum bitrate for RIST, RTP, and RTP-FEC streams.
        :param max_latency: The maximum latency in milliseconds. This parameter applies only to RIST-based, Zixi-based, and Fujitsu-based streams.
        :param protocol: The protocol that the source uses to deliver the content to MediaConnect. Adding additional sources to an existing flow requires Failover to be enabled. When you enable Failover, the additional source must use the same protocol as the existing source. Only the following protocols support failover: Zixi-push, RTP-FEC, RTP, and RIST.
        :param stream_id: The stream ID that you want to use for this transport. This parameter applies only to Zixi and SRT caller-based streams.
        :param vpc_interface_name: The name of the VPC interface that you want to send your output to.
        :param whitelist_cidr: The range of IP addresses that are allowed to contribute content to your source. Format the IP addresses as a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b95b77f3c9a48502139cd66722219f93b4563f348c9d3728c264ca9bc1274199)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFlowSourceProps(
            description=description,
            name=name,
            decryption=decryption,
            entitlement_arn=entitlement_arn,
            flow_arn=flow_arn,
            ingest_port=ingest_port,
            max_bitrate=max_bitrate,
            max_latency=max_latency,
            protocol=protocol,
            stream_id=stream_id,
            vpc_interface_name=vpc_interface_name,
            whitelist_cidr=whitelist_cidr,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__472689544607a53bd1ea6a0c286f007ff1ef33403b1ce3378566f6683251f596)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c90efd5c480d5a635b36566a2a2c2e8d68f3013d7f91ed876e164e947b9abf3)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrIngestIp")
    def attr_ingest_ip(self) -> builtins.str:
        '''The IP address that the flow listens on for incoming content.

        :cloudformationAttribute: IngestIp
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrIngestIp"))

    @builtins.property
    @jsii.member(jsii_name="attrSourceArn")
    def attr_source_arn(self) -> builtins.str:
        '''The ARN of the source.

        :cloudformationAttribute: SourceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSourceArn"))

    @builtins.property
    @jsii.member(jsii_name="attrSourceIngestPort")
    def attr_source_ingest_port(self) -> builtins.str:
        '''
        :cloudformationAttribute: SourceIngestPort
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSourceIngestPort"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''A description of the source.

        This description is not visible outside of the current AWS account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-description
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70bb0860698f6906c0a0e3b9470f833d9aec8f817979950a4825be9c0be681c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60558c6f2729711f9bdb34bc6885014c9090f884d9a3fea693b8f2479a3147cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="decryption")
    def decryption(
        self,
    ) -> typing.Optional[typing.Union["CfnFlowSource.EncryptionProperty", _IResolvable_a771d0ef]]:
        '''The type of encryption that is used on the content ingested from the source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-decryption
        '''
        return typing.cast(typing.Optional[typing.Union["CfnFlowSource.EncryptionProperty", _IResolvable_a771d0ef]], jsii.get(self, "decryption"))

    @decryption.setter
    def decryption(
        self,
        value: typing.Optional[typing.Union["CfnFlowSource.EncryptionProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb89a58d632b446fa3ae12511ee31f6cf5bd1b20846e003fa7d8866a87a76c09)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "decryption", value)

    @builtins.property
    @jsii.member(jsii_name="entitlementArn")
    def entitlement_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the entitlement that allows you to subscribe to the flow.

        The entitlement is set by the content originator, and the ARN is generated as part of the originator's flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-entitlementarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "entitlementArn"))

    @entitlement_arn.setter
    def entitlement_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af54c0f5240b49d830375c5c1f4b2379444f09f9b38c0736940ef74992cc14ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "entitlementArn", value)

    @builtins.property
    @jsii.member(jsii_name="flowArn")
    def flow_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the flow this source is connected to.

        The flow must have Failover enabled to add an additional source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-flowarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "flowArn"))

    @flow_arn.setter
    def flow_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d48be8f29afb3248d99cf9a194453557dd54e19c8f6972d4065792aab3fa4b20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flowArn", value)

    @builtins.property
    @jsii.member(jsii_name="ingestPort")
    def ingest_port(self) -> typing.Optional[jsii.Number]:
        '''The port that the flow listens on for incoming content.

        If the protocol of the source is Zixi, the port must be set to 2088.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-ingestport
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ingestPort"))

    @ingest_port.setter
    def ingest_port(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43958bc6085ff4b6f9159aae20b6b213a0b50976052d6cbf9810f80899f9d2a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ingestPort", value)

    @builtins.property
    @jsii.member(jsii_name="maxBitrate")
    def max_bitrate(self) -> typing.Optional[jsii.Number]:
        '''The maximum bitrate for RIST, RTP, and RTP-FEC streams.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-maxbitrate
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxBitrate"))

    @max_bitrate.setter
    def max_bitrate(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e5d4064f4880434100d2d5da975eb6face78a379733c4d22ad59ef56acd2bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxBitrate", value)

    @builtins.property
    @jsii.member(jsii_name="maxLatency")
    def max_latency(self) -> typing.Optional[jsii.Number]:
        '''The maximum latency in milliseconds.

        This parameter applies only to RIST-based, Zixi-based, and Fujitsu-based streams.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-maxlatency
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxLatency"))

    @max_latency.setter
    def max_latency(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9337d4cd88d796a3e30a1e2dc66c29006d50cfa8a89bcb9ae44b0023c088b7e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxLatency", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol that the source uses to deliver the content to MediaConnect.

        Adding additional sources to an existing flow requires Failover to be enabled. When you enable Failover, the additional source must use the same protocol as the existing source. Only the following protocols support failover: Zixi-push, RTP-FEC, RTP, and RIST.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-protocol
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b69823ea4b26ef689fe5cab4bdec2f42b3f26b7d17d63aa01e24cb704727ba4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="streamId")
    def stream_id(self) -> typing.Optional[builtins.str]:
        '''The stream ID that you want to use for this transport.

        This parameter applies only to Zixi and SRT caller-based streams.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-streamid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "streamId"))

    @stream_id.setter
    def stream_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7389982c19b6e71c032e13d499077491bc124ee254b4ef51b14329607b7cf8f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamId", value)

    @builtins.property
    @jsii.member(jsii_name="vpcInterfaceName")
    def vpc_interface_name(self) -> typing.Optional[builtins.str]:
        '''The name of the VPC interface that you want to send your output to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-vpcinterfacename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcInterfaceName"))

    @vpc_interface_name.setter
    def vpc_interface_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bf61a499e7e335276cae9973a6ec66891d343f0a7629039c829051e6585ad1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcInterfaceName", value)

    @builtins.property
    @jsii.member(jsii_name="whitelistCidr")
    def whitelist_cidr(self) -> typing.Optional[builtins.str]:
        '''The range of IP addresses that are allowed to contribute content to your source.

        Format the IP addresses as a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-whitelistcidr
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "whitelistCidr"))

    @whitelist_cidr.setter
    def whitelist_cidr(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ac2b04ce8dcb50b7c68fdac1ffe4739750c9a700c385073bc5b8be2ac630943)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "whitelistCidr", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_mediaconnect.CfnFlowSource.EncryptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "algorithm": "algorithm",
            "role_arn": "roleArn",
            "constant_initialization_vector": "constantInitializationVector",
            "device_id": "deviceId",
            "key_type": "keyType",
            "region": "region",
            "resource_id": "resourceId",
            "secret_arn": "secretArn",
            "url": "url",
        },
    )
    class EncryptionProperty:
        def __init__(
            self,
            *,
            algorithm: builtins.str,
            role_arn: builtins.str,
            constant_initialization_vector: typing.Optional[builtins.str] = None,
            device_id: typing.Optional[builtins.str] = None,
            key_type: typing.Optional[builtins.str] = None,
            region: typing.Optional[builtins.str] = None,
            resource_id: typing.Optional[builtins.str] = None,
            secret_arn: typing.Optional[builtins.str] = None,
            url: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Information about the encryption of the flow.

            :param algorithm: The type of algorithm that is used for the encryption (such as aes128, aes192, or aes256).
            :param role_arn: The Amazon Resource Name (ARN) of the role that you created during setup (when you set up MediaConnect as a trusted entity).
            :param constant_initialization_vector: A 128-bit, 16-byte hex value represented by a 32-character string, to be used with the key for encrypting content. This parameter is not valid for static key encryption.
            :param device_id: The value of one of the devices that you configured with your digital rights management (DRM) platform key provider. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param key_type: The type of key that is used for the encryption. If you don't specify a ``keyType`` value, the service uses the default setting ( ``static-key`` ).
            :param region: The AWS Region that the API Gateway proxy endpoint was created in. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param resource_id: An identifier for the content. The service sends this value to the key server to identify the current endpoint. The resource ID is also known as the content ID. This parameter is required for SPEKE encryption and is not valid for static key encryption.
            :param secret_arn: The ARN of the secret that you created in AWS Secrets Manager to store the encryption key.
            :param url: The URL from the API Gateway proxy that you set up to talk to your key server. This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_mediaconnect as mediaconnect
                
                encryption_property = mediaconnect.CfnFlowSource.EncryptionProperty(
                    algorithm="algorithm",
                    role_arn="roleArn",
                
                    # the properties below are optional
                    constant_initialization_vector="constantInitializationVector",
                    device_id="deviceId",
                    key_type="keyType",
                    region="region",
                    resource_id="resourceId",
                    secret_arn="secretArn",
                    url="url"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cef6da15b97cd39c850e5161cafda266db664a9e56b57f63df294d1d488876cc)
                check_type(argname="argument algorithm", value=algorithm, expected_type=type_hints["algorithm"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument constant_initialization_vector", value=constant_initialization_vector, expected_type=type_hints["constant_initialization_vector"])
                check_type(argname="argument device_id", value=device_id, expected_type=type_hints["device_id"])
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
                check_type(argname="argument region", value=region, expected_type=type_hints["region"])
                check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
                check_type(argname="argument secret_arn", value=secret_arn, expected_type=type_hints["secret_arn"])
                check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "algorithm": algorithm,
                "role_arn": role_arn,
            }
            if constant_initialization_vector is not None:
                self._values["constant_initialization_vector"] = constant_initialization_vector
            if device_id is not None:
                self._values["device_id"] = device_id
            if key_type is not None:
                self._values["key_type"] = key_type
            if region is not None:
                self._values["region"] = region
            if resource_id is not None:
                self._values["resource_id"] = resource_id
            if secret_arn is not None:
                self._values["secret_arn"] = secret_arn
            if url is not None:
                self._values["url"] = url

        @builtins.property
        def algorithm(self) -> builtins.str:
            '''The type of algorithm that is used for the encryption (such as aes128, aes192, or aes256).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-algorithm
            '''
            result = self._values.get("algorithm")
            assert result is not None, "Required property 'algorithm' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def role_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the role that you created during setup (when you set up MediaConnect as a trusted entity).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-rolearn
            '''
            result = self._values.get("role_arn")
            assert result is not None, "Required property 'role_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def constant_initialization_vector(self) -> typing.Optional[builtins.str]:
            '''A 128-bit, 16-byte hex value represented by a 32-character string, to be used with the key for encrypting content.

            This parameter is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-constantinitializationvector
            '''
            result = self._values.get("constant_initialization_vector")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def device_id(self) -> typing.Optional[builtins.str]:
            '''The value of one of the devices that you configured with your digital rights management (DRM) platform key provider.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-deviceid
            '''
            result = self._values.get("device_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def key_type(self) -> typing.Optional[builtins.str]:
            '''The type of key that is used for the encryption.

            If you don't specify a ``keyType`` value, the service uses the default setting ( ``static-key`` ).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-keytype
            '''
            result = self._values.get("key_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def region(self) -> typing.Optional[builtins.str]:
            '''The AWS Region that the API Gateway proxy endpoint was created in.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-region
            '''
            result = self._values.get("region")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def resource_id(self) -> typing.Optional[builtins.str]:
            '''An identifier for the content.

            The service sends this value to the key server to identify the current endpoint. The resource ID is also known as the content ID. This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-resourceid
            '''
            result = self._values.get("resource_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def secret_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the secret that you created in AWS Secrets Manager to store the encryption key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-secretarn
            '''
            result = self._values.get("secret_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def url(self) -> typing.Optional[builtins.str]:
            '''The URL from the API Gateway proxy that you set up to talk to your key server.

            This parameter is required for SPEKE encryption and is not valid for static key encryption.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-mediaconnect-flowsource-encryption.html#cfn-mediaconnect-flowsource-encryption-url
            '''
            result = self._values.get("url")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EncryptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_mediaconnect.CfnFlowSourceProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "name": "name",
        "decryption": "decryption",
        "entitlement_arn": "entitlementArn",
        "flow_arn": "flowArn",
        "ingest_port": "ingestPort",
        "max_bitrate": "maxBitrate",
        "max_latency": "maxLatency",
        "protocol": "protocol",
        "stream_id": "streamId",
        "vpc_interface_name": "vpcInterfaceName",
        "whitelist_cidr": "whitelistCidr",
    },
)
class CfnFlowSourceProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        name: builtins.str,
        decryption: typing.Optional[typing.Union[typing.Union[CfnFlowSource.EncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        entitlement_arn: typing.Optional[builtins.str] = None,
        flow_arn: typing.Optional[builtins.str] = None,
        ingest_port: typing.Optional[jsii.Number] = None,
        max_bitrate: typing.Optional[jsii.Number] = None,
        max_latency: typing.Optional[jsii.Number] = None,
        protocol: typing.Optional[builtins.str] = None,
        stream_id: typing.Optional[builtins.str] = None,
        vpc_interface_name: typing.Optional[builtins.str] = None,
        whitelist_cidr: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnFlowSource``.

        :param description: A description of the source. This description is not visible outside of the current AWS account.
        :param name: The name of the source.
        :param decryption: The type of encryption that is used on the content ingested from the source.
        :param entitlement_arn: The ARN of the entitlement that allows you to subscribe to the flow. The entitlement is set by the content originator, and the ARN is generated as part of the originator's flow.
        :param flow_arn: The Amazon Resource Name (ARN) of the flow this source is connected to. The flow must have Failover enabled to add an additional source.
        :param ingest_port: The port that the flow listens on for incoming content. If the protocol of the source is Zixi, the port must be set to 2088.
        :param max_bitrate: The maximum bitrate for RIST, RTP, and RTP-FEC streams.
        :param max_latency: The maximum latency in milliseconds. This parameter applies only to RIST-based, Zixi-based, and Fujitsu-based streams.
        :param protocol: The protocol that the source uses to deliver the content to MediaConnect. Adding additional sources to an existing flow requires Failover to be enabled. When you enable Failover, the additional source must use the same protocol as the existing source. Only the following protocols support failover: Zixi-push, RTP-FEC, RTP, and RIST.
        :param stream_id: The stream ID that you want to use for this transport. This parameter applies only to Zixi and SRT caller-based streams.
        :param vpc_interface_name: The name of the VPC interface that you want to send your output to.
        :param whitelist_cidr: The range of IP addresses that are allowed to contribute content to your source. Format the IP addresses as a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_mediaconnect as mediaconnect
            
            cfn_flow_source_props = mediaconnect.CfnFlowSourceProps(
                description="description",
                name="name",
            
                # the properties below are optional
                decryption=mediaconnect.CfnFlowSource.EncryptionProperty(
                    algorithm="algorithm",
                    role_arn="roleArn",
            
                    # the properties below are optional
                    constant_initialization_vector="constantInitializationVector",
                    device_id="deviceId",
                    key_type="keyType",
                    region="region",
                    resource_id="resourceId",
                    secret_arn="secretArn",
                    url="url"
                ),
                entitlement_arn="entitlementArn",
                flow_arn="flowArn",
                ingest_port=123,
                max_bitrate=123,
                max_latency=123,
                protocol="protocol",
                stream_id="streamId",
                vpc_interface_name="vpcInterfaceName",
                whitelist_cidr="whitelistCidr"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__344b0d30803d22210de8ec8d4e2f31007a4481c0e804552558c9c258585a40a7)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument decryption", value=decryption, expected_type=type_hints["decryption"])
            check_type(argname="argument entitlement_arn", value=entitlement_arn, expected_type=type_hints["entitlement_arn"])
            check_type(argname="argument flow_arn", value=flow_arn, expected_type=type_hints["flow_arn"])
            check_type(argname="argument ingest_port", value=ingest_port, expected_type=type_hints["ingest_port"])
            check_type(argname="argument max_bitrate", value=max_bitrate, expected_type=type_hints["max_bitrate"])
            check_type(argname="argument max_latency", value=max_latency, expected_type=type_hints["max_latency"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument stream_id", value=stream_id, expected_type=type_hints["stream_id"])
            check_type(argname="argument vpc_interface_name", value=vpc_interface_name, expected_type=type_hints["vpc_interface_name"])
            check_type(argname="argument whitelist_cidr", value=whitelist_cidr, expected_type=type_hints["whitelist_cidr"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "name": name,
        }
        if decryption is not None:
            self._values["decryption"] = decryption
        if entitlement_arn is not None:
            self._values["entitlement_arn"] = entitlement_arn
        if flow_arn is not None:
            self._values["flow_arn"] = flow_arn
        if ingest_port is not None:
            self._values["ingest_port"] = ingest_port
        if max_bitrate is not None:
            self._values["max_bitrate"] = max_bitrate
        if max_latency is not None:
            self._values["max_latency"] = max_latency
        if protocol is not None:
            self._values["protocol"] = protocol
        if stream_id is not None:
            self._values["stream_id"] = stream_id
        if vpc_interface_name is not None:
            self._values["vpc_interface_name"] = vpc_interface_name
        if whitelist_cidr is not None:
            self._values["whitelist_cidr"] = whitelist_cidr

    @builtins.property
    def description(self) -> builtins.str:
        '''A description of the source.

        This description is not visible outside of the current AWS account.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def decryption(
        self,
    ) -> typing.Optional[typing.Union[CfnFlowSource.EncryptionProperty, _IResolvable_a771d0ef]]:
        '''The type of encryption that is used on the content ingested from the source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-decryption
        '''
        result = self._values.get("decryption")
        return typing.cast(typing.Optional[typing.Union[CfnFlowSource.EncryptionProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def entitlement_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the entitlement that allows you to subscribe to the flow.

        The entitlement is set by the content originator, and the ARN is generated as part of the originator's flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-entitlementarn
        '''
        result = self._values.get("entitlement_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def flow_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the flow this source is connected to.

        The flow must have Failover enabled to add an additional source.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-flowarn
        '''
        result = self._values.get("flow_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ingest_port(self) -> typing.Optional[jsii.Number]:
        '''The port that the flow listens on for incoming content.

        If the protocol of the source is Zixi, the port must be set to 2088.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-ingestport
        '''
        result = self._values.get("ingest_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_bitrate(self) -> typing.Optional[jsii.Number]:
        '''The maximum bitrate for RIST, RTP, and RTP-FEC streams.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-maxbitrate
        '''
        result = self._values.get("max_bitrate")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def max_latency(self) -> typing.Optional[jsii.Number]:
        '''The maximum latency in milliseconds.

        This parameter applies only to RIST-based, Zixi-based, and Fujitsu-based streams.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-maxlatency
        '''
        result = self._values.get("max_latency")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def protocol(self) -> typing.Optional[builtins.str]:
        '''The protocol that the source uses to deliver the content to MediaConnect.

        Adding additional sources to an existing flow requires Failover to be enabled. When you enable Failover, the additional source must use the same protocol as the existing source. Only the following protocols support failover: Zixi-push, RTP-FEC, RTP, and RIST.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-protocol
        '''
        result = self._values.get("protocol")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stream_id(self) -> typing.Optional[builtins.str]:
        '''The stream ID that you want to use for this transport.

        This parameter applies only to Zixi and SRT caller-based streams.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-streamid
        '''
        result = self._values.get("stream_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_interface_name(self) -> typing.Optional[builtins.str]:
        '''The name of the VPC interface that you want to send your output to.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-vpcinterfacename
        '''
        result = self._values.get("vpc_interface_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def whitelist_cidr(self) -> typing.Optional[builtins.str]:
        '''The range of IP addresses that are allowed to contribute content to your source.

        Format the IP addresses as a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowsource.html#cfn-mediaconnect-flowsource-whitelistcidr
        '''
        result = self._values.get("whitelist_cidr")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFlowSourceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnFlowVpcInterface(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_mediaconnect.CfnFlowVpcInterface",
):
    '''A CloudFormation ``AWS::MediaConnect::FlowVpcInterface``.

    The AWS::MediaConnect::FlowVpcInterface resource is a connection between your AWS Elemental MediaConnect flow and a virtual private cloud (VPC) that you created using the Amazon Virtual Private Cloud service.

    To avoid streaming your content over the public internet, you can add up to two VPC interfaces to your flow and use those connections to transfer content between your VPC and MediaConnect.

    You can update an existing flow to add a VPC interface. If you haven’t created the flow yet, you must create the flow with a temporary standard source by doing the following:

    - Use CloudFormation to create a flow with a standard source that uses to the flow’s public IP address.
    - Use CloudFormation to create a VPC interface to add to this flow. This can also be done as part of the previous step.
    - After CloudFormation has created the flow and the VPC interface, update the source to point to the VPC interface that you created.

    :cloudformationResource: AWS::MediaConnect::FlowVpcInterface
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_mediaconnect as mediaconnect
        
        cfn_flow_vpc_interface = mediaconnect.CfnFlowVpcInterface(self, "MyCfnFlowVpcInterface",
            flow_arn="flowArn",
            name="name",
            role_arn="roleArn",
            security_group_ids=["securityGroupIds"],
            subnet_id="subnetId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        flow_arn: builtins.str,
        name: builtins.str,
        role_arn: builtins.str,
        security_group_ids: typing.Sequence[builtins.str],
        subnet_id: builtins.str,
    ) -> None:
        '''Create a new ``AWS::MediaConnect::FlowVpcInterface``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param flow_arn: The Amazon Resource Name (ARN) of the flow.
        :param name: The name of the VPC Interface. This value must be unique within the current flow.
        :param role_arn: The Amazon Resource Name (ARN) of the role that you created when you set up MediaConnect as a trusted service.
        :param security_group_ids: The VPC security groups that you want MediaConnect to use for your VPC configuration. You must include at least one security group in the request.
        :param subnet_id: The subnet IDs that you want to use for your VPC interface. A range of IP addresses in your VPC. When you create your VPC, you specify a range of IPv4 addresses for the VPC in the form of a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16. This is the primary CIDR block for your VPC. When you create a subnet for your VPC, you specify the CIDR block for the subnet, which is a subset of the VPC CIDR block. The subnets that you use across all VPC interfaces on the flow must be in the same Availability Zone as the flow.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4bbd60f282e3c7b82e7a5ebacffb63081a76622872a3171ef0a507f5a513494)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFlowVpcInterfaceProps(
            flow_arn=flow_arn,
            name=name,
            role_arn=role_arn,
            security_group_ids=security_group_ids,
            subnet_id=subnet_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab759b1ad0d8c522ed4954df00db3302c8f47d5c0fa48f2b4b0de04194c147d9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ecdb853a3566e399e6288d90704260a4726f3c5181f5c514b0d8fd24ec05f8de)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrNetworkInterfaceIds")
    def attr_network_interface_ids(self) -> typing.List[builtins.str]:
        '''The IDs of the network interfaces that MediaConnect created in your account.

        :cloudformationAttribute: NetworkInterfaceIds
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrNetworkInterfaceIds"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="flowArn")
    def flow_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html#cfn-mediaconnect-flowvpcinterface-flowarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "flowArn"))

    @flow_arn.setter
    def flow_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c3934674f9ec440d82456a4efe779ab8795a50844bdcc45ad44e16c8ab04223)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "flowArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the VPC Interface.

        This value must be unique within the current flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html#cfn-mediaconnect-flowvpcinterface-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__048d06cd1d95f8988f9fbd150ada6447fad76b10a8f8d81b5eea326b6e0af6a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the role that you created when you set up MediaConnect as a trusted service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html#cfn-mediaconnect-flowvpcinterface-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e7fded90ceb4e982f850a9233a90365be6591affe288e043d3cb82947eba540)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        '''The VPC security groups that you want MediaConnect to use for your VPC configuration.

        You must include at least one security group in the request.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html#cfn-mediaconnect-flowvpcinterface-securitygroupids
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__503f178fb4948a77601dd751e0e5a706ec79540f25dc1a413d1324ba48acfd60)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        '''The subnet IDs that you want to use for your VPC interface.

        A range of IP addresses in your VPC. When you create your VPC, you specify a range of IPv4 addresses for the VPC in the form of a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16. This is the primary CIDR block for your VPC. When you create a subnet for your VPC, you specify the CIDR block for the subnet, which is a subset of the VPC CIDR block.

        The subnets that you use across all VPC interfaces on the flow must be in the same Availability Zone as the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html#cfn-mediaconnect-flowvpcinterface-subnetid
        '''
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b12fe431c40231fc7632bff0071536d75299ca07261600bf62f701f374ea4cd8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_mediaconnect.CfnFlowVpcInterfaceProps",
    jsii_struct_bases=[],
    name_mapping={
        "flow_arn": "flowArn",
        "name": "name",
        "role_arn": "roleArn",
        "security_group_ids": "securityGroupIds",
        "subnet_id": "subnetId",
    },
)
class CfnFlowVpcInterfaceProps:
    def __init__(
        self,
        *,
        flow_arn: builtins.str,
        name: builtins.str,
        role_arn: builtins.str,
        security_group_ids: typing.Sequence[builtins.str],
        subnet_id: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnFlowVpcInterface``.

        :param flow_arn: The Amazon Resource Name (ARN) of the flow.
        :param name: The name of the VPC Interface. This value must be unique within the current flow.
        :param role_arn: The Amazon Resource Name (ARN) of the role that you created when you set up MediaConnect as a trusted service.
        :param security_group_ids: The VPC security groups that you want MediaConnect to use for your VPC configuration. You must include at least one security group in the request.
        :param subnet_id: The subnet IDs that you want to use for your VPC interface. A range of IP addresses in your VPC. When you create your VPC, you specify a range of IPv4 addresses for the VPC in the form of a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16. This is the primary CIDR block for your VPC. When you create a subnet for your VPC, you specify the CIDR block for the subnet, which is a subset of the VPC CIDR block. The subnets that you use across all VPC interfaces on the flow must be in the same Availability Zone as the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_mediaconnect as mediaconnect
            
            cfn_flow_vpc_interface_props = mediaconnect.CfnFlowVpcInterfaceProps(
                flow_arn="flowArn",
                name="name",
                role_arn="roleArn",
                security_group_ids=["securityGroupIds"],
                subnet_id="subnetId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c649d582b82ee4d090cbab99a837293eab8f2ef5ea36cb8fcc679e862a1b7fdb)
            check_type(argname="argument flow_arn", value=flow_arn, expected_type=type_hints["flow_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "flow_arn": flow_arn,
            "name": name,
            "role_arn": role_arn,
            "security_group_ids": security_group_ids,
            "subnet_id": subnet_id,
        }

    @builtins.property
    def flow_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html#cfn-mediaconnect-flowvpcinterface-flowarn
        '''
        result = self._values.get("flow_arn")
        assert result is not None, "Required property 'flow_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the VPC Interface.

        This value must be unique within the current flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html#cfn-mediaconnect-flowvpcinterface-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the role that you created when you set up MediaConnect as a trusted service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html#cfn-mediaconnect-flowvpcinterface-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def security_group_ids(self) -> typing.List[builtins.str]:
        '''The VPC security groups that you want MediaConnect to use for your VPC configuration.

        You must include at least one security group in the request.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html#cfn-mediaconnect-flowvpcinterface-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        assert result is not None, "Required property 'security_group_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''The subnet IDs that you want to use for your VPC interface.

        A range of IP addresses in your VPC. When you create your VPC, you specify a range of IPv4 addresses for the VPC in the form of a Classless Inter-Domain Routing (CIDR) block; for example, 10.0.0.0/16. This is the primary CIDR block for your VPC. When you create a subnet for your VPC, you specify the CIDR block for the subnet, which is a subset of the VPC CIDR block.

        The subnets that you use across all VPC interfaces on the flow must be in the same Availability Zone as the flow.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-mediaconnect-flowvpcinterface.html#cfn-mediaconnect-flowvpcinterface-subnetid
        '''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFlowVpcInterfaceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnFlow",
    "CfnFlowEntitlement",
    "CfnFlowEntitlementProps",
    "CfnFlowOutput",
    "CfnFlowOutputProps",
    "CfnFlowProps",
    "CfnFlowSource",
    "CfnFlowSourceProps",
    "CfnFlowVpcInterface",
    "CfnFlowVpcInterfaceProps",
]

publication.publish()

def _typecheckingstub__677ad3f0bbb1ecbf8c17fb53fcc71e60b60639a087942ce4d7cf79175c4de9c0(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    source: typing.Union[typing.Union[CfnFlow.SourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    availability_zone: typing.Optional[builtins.str] = None,
    source_failover_config: typing.Optional[typing.Union[typing.Union[CfnFlow.FailoverConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2377a5329b6d62e97968a8a81e2b340e8851f9575c33803cd8c3d84e74919eef(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28a79f4bb0771f4adbd18735028ef90d2da89338df6ed91f7c264892c1c61e5b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39c98570900ca64fa5c1db8882310135b13544c67ff60943a4aacde4d0e9828d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26067bec9d6b9fab198df82e9a4fa160128c7f9e82083e74581b7f6e9624e66f(
    value: typing.Union[CfnFlow.SourceProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e04c225f4a3e86d061288fe2f8d254c5c0aed5f4cce8d640af684d7c350c6c50(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d7f6b2380180266cfed4f38d565b4eafceef23486f423c7e3bbff67ed5d1761(
    value: typing.Optional[typing.Union[CfnFlow.FailoverConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c08c417f3091b2f1cdc728267dd891ce46cdaebd1d220c2e75c5c5eb244ea4a8(
    *,
    role_arn: builtins.str,
    algorithm: typing.Optional[builtins.str] = None,
    constant_initialization_vector: typing.Optional[builtins.str] = None,
    device_id: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f1c8de1ea6c38f9b23367e03c9fa5f93275a0dd3a030ab5b1b0e5218ee384d4(
    *,
    failover_mode: typing.Optional[builtins.str] = None,
    recovery_window: typing.Optional[jsii.Number] = None,
    source_priority: typing.Optional[typing.Union[typing.Union[CfnFlow.SourcePriorityProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    state: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__482e14dba0d2888a051941c86c4ecf4857661fdea59dad9e0154586148046182(
    *,
    primary_source: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9bacfc8576f0d9be4e32fc82a1bbf42fa275e9ad99357e29ed2501b502ed339a(
    *,
    decryption: typing.Optional[typing.Union[typing.Union[CfnFlow.EncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    entitlement_arn: typing.Optional[builtins.str] = None,
    ingest_ip: typing.Optional[builtins.str] = None,
    ingest_port: typing.Optional[jsii.Number] = None,
    max_bitrate: typing.Optional[jsii.Number] = None,
    max_latency: typing.Optional[jsii.Number] = None,
    min_latency: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    protocol: typing.Optional[builtins.str] = None,
    sender_control_port: typing.Optional[jsii.Number] = None,
    sender_ip_address: typing.Optional[builtins.str] = None,
    source_arn: typing.Optional[builtins.str] = None,
    source_ingest_port: typing.Optional[builtins.str] = None,
    source_listener_address: typing.Optional[builtins.str] = None,
    source_listener_port: typing.Optional[jsii.Number] = None,
    stream_id: typing.Optional[builtins.str] = None,
    vpc_interface_name: typing.Optional[builtins.str] = None,
    whitelist_cidr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18880888e4b71846ae07f794759e4b50a6d8bb1fdeb8d77d0b8c42c9296eb3d6(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    description: builtins.str,
    flow_arn: builtins.str,
    name: builtins.str,
    subscribers: typing.Sequence[builtins.str],
    data_transfer_subscriber_fee_percent: typing.Optional[jsii.Number] = None,
    encryption: typing.Optional[typing.Union[typing.Union[CfnFlowEntitlement.EncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    entitlement_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f15ff7c6c6fe5e27409e4a17a3fe4bcdac993a94c2176b0c5fff65f29ea75771(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__064cc526d8bfa90208606e94fb1132afdae6ce70457f8d140d59101b55fb3382(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8660fd0ef83e6bf995729002afb473891316c40e7673c6b33823c89adc7c6f68(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91535e402252ee56b5180debfa994bd9b2ccc4ee19e21db1bcabe2a18b2a9084(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19cd78b7c63b00f4f068b5fc5fbd3615037e3d6c6af12b965bcebdc7bc820f55(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c9a2c2f931bd42bc400ae5ffe45ca29f83b5d86fa9efb64889ebb86359553f9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0aaf7df2dd32084636437cb83c86925259f8e8baf5ee1b26a253fc52a93f25a2(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6307d772cfa7e8d8c34220467717165a96d599387f06530dc33d46c0a6aeb832(
    value: typing.Optional[typing.Union[CfnFlowEntitlement.EncryptionProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf84e8be89c1109124a732ff8dc22b675622f35df70191b2eddb8287ec6cf0b6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78faac540172799eeb6b1066c6d0e2b6ae426d3830a9f1ba6b2aacf4e722747d(
    *,
    algorithm: builtins.str,
    role_arn: builtins.str,
    constant_initialization_vector: typing.Optional[builtins.str] = None,
    device_id: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2b9bdfc2cc118279a2b87ae533b7cad4db373b533b3405acee867d9928a7798(
    *,
    description: builtins.str,
    flow_arn: builtins.str,
    name: builtins.str,
    subscribers: typing.Sequence[builtins.str],
    data_transfer_subscriber_fee_percent: typing.Optional[jsii.Number] = None,
    encryption: typing.Optional[typing.Union[typing.Union[CfnFlowEntitlement.EncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    entitlement_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__783a86052e919a1ec9b2f7e162ba0ae621fc030564aafecff1ef4bc4de1c4582(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    flow_arn: builtins.str,
    protocol: builtins.str,
    cidr_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    destination: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[typing.Union[typing.Union[CfnFlowOutput.EncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    max_latency: typing.Optional[jsii.Number] = None,
    min_latency: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    remote_id: typing.Optional[builtins.str] = None,
    smoothing_latency: typing.Optional[jsii.Number] = None,
    stream_id: typing.Optional[builtins.str] = None,
    vpc_interface_attachment: typing.Optional[typing.Union[typing.Union[CfnFlowOutput.VpcInterfaceAttachmentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be7aa6364d3ec5bb4fd8c022307a3160b129b6fb3e85be1eeaa1b14b1ef1f6bb(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7fdd1caaccc701d4686c89e023afb1433d009ea6d5a3b45a5a393e87ff31fcd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d2fb856996b0e0e76e621d058cbb48c0a6e1e3cc2259c413554b1cebca57fd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc6aaa5b559d34a41e6293ad6ce506b7c25a4872c4c2c0405926a0acca3f3a42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1f44c8ef17b12239b984d17b709453754e6481386d73ceaed6d5e8bfb579cf5(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ba848510921aa4d87cb5e839761513aafc12c7d5940ee1b1627daf66668b95f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90e1311bc6a0d826a0bd66cedb1af8462a12bd7eda423a53c852f0d16ff5df58(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0193cc392c9bf77ccba750573777e6719c1545c8ba88f9c06de1066d166a3d9(
    value: typing.Optional[typing.Union[CfnFlowOutput.EncryptionProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab9e471bbdfe7ac9786e44dbdf5748db8b9fe344ca6679ffff81e8c78c13264(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18d53969d6da0b0807de0e0ad5537b749a20ea51392c9a8a49b17c2c67f27f66(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8d88988f89160f89533ec5442856f41a14d11d775ff9ce560d9d16407e1581d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__494cb6e520d7a1efafda911460d1377f2e593f30a7de4e7591e7d792db0d2737(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf07cc2b6ca5470f39dbe47538f98bc9335c2ca0515d29e0aa26183334359e3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6210f516674e4667d9afbc11fe71bef0a715f86c8eb2ea23e37883ea6cc5f95f(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb1682ee60a28ddeb3533a188ce74e61e7fe77715ebe440575b8e3f6833b9ed(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26e5a3703efaa0ec3e944402910679953cd697fed4e858ec095a2cc6dde07cf9(
    value: typing.Optional[typing.Union[CfnFlowOutput.VpcInterfaceAttachmentProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65a2f411484c3a4bc259cbf6a8e0c219ea553db2bdb680d8f95abd71df584045(
    *,
    role_arn: builtins.str,
    secret_arn: builtins.str,
    algorithm: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a74863b23494168aab7acbef025f3c39f979c5cc7c2de5440f5494b398728846(
    *,
    vpc_interface_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccba2126e06e8c24a6d8916a495ec85e9612d70179092776b8f9f29bd7a87243(
    *,
    flow_arn: builtins.str,
    protocol: builtins.str,
    cidr_allow_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    description: typing.Optional[builtins.str] = None,
    destination: typing.Optional[builtins.str] = None,
    encryption: typing.Optional[typing.Union[typing.Union[CfnFlowOutput.EncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    max_latency: typing.Optional[jsii.Number] = None,
    min_latency: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    remote_id: typing.Optional[builtins.str] = None,
    smoothing_latency: typing.Optional[jsii.Number] = None,
    stream_id: typing.Optional[builtins.str] = None,
    vpc_interface_attachment: typing.Optional[typing.Union[typing.Union[CfnFlowOutput.VpcInterfaceAttachmentProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02242ddd9efca6abff6b707b9a5c619a997606384b1a9d68360bbc246e7812aa(
    *,
    name: builtins.str,
    source: typing.Union[typing.Union[CfnFlow.SourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    availability_zone: typing.Optional[builtins.str] = None,
    source_failover_config: typing.Optional[typing.Union[typing.Union[CfnFlow.FailoverConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b95b77f3c9a48502139cd66722219f93b4563f348c9d3728c264ca9bc1274199(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    description: builtins.str,
    name: builtins.str,
    decryption: typing.Optional[typing.Union[typing.Union[CfnFlowSource.EncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    entitlement_arn: typing.Optional[builtins.str] = None,
    flow_arn: typing.Optional[builtins.str] = None,
    ingest_port: typing.Optional[jsii.Number] = None,
    max_bitrate: typing.Optional[jsii.Number] = None,
    max_latency: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    stream_id: typing.Optional[builtins.str] = None,
    vpc_interface_name: typing.Optional[builtins.str] = None,
    whitelist_cidr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__472689544607a53bd1ea6a0c286f007ff1ef33403b1ce3378566f6683251f596(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c90efd5c480d5a635b36566a2a2c2e8d68f3013d7f91ed876e164e947b9abf3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70bb0860698f6906c0a0e3b9470f833d9aec8f817979950a4825be9c0be681c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60558c6f2729711f9bdb34bc6885014c9090f884d9a3fea693b8f2479a3147cb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb89a58d632b446fa3ae12511ee31f6cf5bd1b20846e003fa7d8866a87a76c09(
    value: typing.Optional[typing.Union[CfnFlowSource.EncryptionProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af54c0f5240b49d830375c5c1f4b2379444f09f9b38c0736940ef74992cc14ff(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d48be8f29afb3248d99cf9a194453557dd54e19c8f6972d4065792aab3fa4b20(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43958bc6085ff4b6f9159aae20b6b213a0b50976052d6cbf9810f80899f9d2a4(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e5d4064f4880434100d2d5da975eb6face78a379733c4d22ad59ef56acd2bf(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9337d4cd88d796a3e30a1e2dc66c29006d50cfa8a89bcb9ae44b0023c088b7e8(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b69823ea4b26ef689fe5cab4bdec2f42b3f26b7d17d63aa01e24cb704727ba4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7389982c19b6e71c032e13d499077491bc124ee254b4ef51b14329607b7cf8f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf61a499e7e335276cae9973a6ec66891d343f0a7629039c829051e6585ad1c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ac2b04ce8dcb50b7c68fdac1ffe4739750c9a700c385073bc5b8be2ac630943(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cef6da15b97cd39c850e5161cafda266db664a9e56b57f63df294d1d488876cc(
    *,
    algorithm: builtins.str,
    role_arn: builtins.str,
    constant_initialization_vector: typing.Optional[builtins.str] = None,
    device_id: typing.Optional[builtins.str] = None,
    key_type: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
    secret_arn: typing.Optional[builtins.str] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__344b0d30803d22210de8ec8d4e2f31007a4481c0e804552558c9c258585a40a7(
    *,
    description: builtins.str,
    name: builtins.str,
    decryption: typing.Optional[typing.Union[typing.Union[CfnFlowSource.EncryptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    entitlement_arn: typing.Optional[builtins.str] = None,
    flow_arn: typing.Optional[builtins.str] = None,
    ingest_port: typing.Optional[jsii.Number] = None,
    max_bitrate: typing.Optional[jsii.Number] = None,
    max_latency: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    stream_id: typing.Optional[builtins.str] = None,
    vpc_interface_name: typing.Optional[builtins.str] = None,
    whitelist_cidr: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4bbd60f282e3c7b82e7a5ebacffb63081a76622872a3171ef0a507f5a513494(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    flow_arn: builtins.str,
    name: builtins.str,
    role_arn: builtins.str,
    security_group_ids: typing.Sequence[builtins.str],
    subnet_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab759b1ad0d8c522ed4954df00db3302c8f47d5c0fa48f2b4b0de04194c147d9(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecdb853a3566e399e6288d90704260a4726f3c5181f5c514b0d8fd24ec05f8de(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3934674f9ec440d82456a4efe779ab8795a50844bdcc45ad44e16c8ab04223(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048d06cd1d95f8988f9fbd150ada6447fad76b10a8f8d81b5eea326b6e0af6a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e7fded90ceb4e982f850a9233a90365be6591affe288e043d3cb82947eba540(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__503f178fb4948a77601dd751e0e5a706ec79540f25dc1a413d1324ba48acfd60(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b12fe431c40231fc7632bff0071536d75299ca07261600bf62f701f374ea4cd8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c649d582b82ee4d090cbab99a837293eab8f2ef5ea36cb8fcc679e862a1b7fdb(
    *,
    flow_arn: builtins.str,
    name: builtins.str,
    role_arn: builtins.str,
    security_group_ids: typing.Sequence[builtins.str],
    subnet_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
