'''
# AWS::KinesisVideo Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_kinesisvideo as kinesisvideo
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for KinesisVideo construct libraries](https://constructs.dev/search?q=kinesisvideo)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::KinesisVideo resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_KinesisVideo.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::KinesisVideo](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_KinesisVideo.html).

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
class CfnSignalingChannel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kinesisvideo.CfnSignalingChannel",
):
    '''A CloudFormation ``AWS::KinesisVideo::SignalingChannel``.

    Specifies a signaling channel.

    ``CreateSignalingChannel`` is an asynchronous operation.

    :cloudformationResource: AWS::KinesisVideo::SignalingChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-signalingchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_kinesisvideo as kinesisvideo
        
        cfn_signaling_channel = kinesisvideo.CfnSignalingChannel(self, "MyCfnSignalingChannel",
            message_ttl_seconds=123,
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            type="type"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        message_ttl_seconds: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::KinesisVideo::SignalingChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param message_ttl_seconds: The period of time a signaling channel retains undelivered messages before they are discarded.
        :param name: A name for the signaling channel that you are creating. It must be unique for each AWS account and AWS Region .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param type: A type of the signaling channel that you are creating. Currently, ``SINGLE_MASTER`` is the only supported channel type.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961e1bd08ac2456689473efb67cf521c3a6db38334cc60575a3ab304d24d4fc4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSignalingChannelProps(
            message_ttl_seconds=message_ttl_seconds, name=name, tags=tags, type=type
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__45a7dfc1ecc46ddd9cc1ccedee8e1ad2d53b3a3e54bb3d64c8365cd136e19250)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd53d26282726cad857bc607290570a09225859587036008413324c833803fc9)
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
        '''The Amazon Resource Name (ARN) of the signaling channel.

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
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-signalingchannel.html#cfn-kinesisvideo-signalingchannel-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="messageTtlSeconds")
    def message_ttl_seconds(self) -> typing.Optional[jsii.Number]:
        '''The period of time a signaling channel retains undelivered messages before they are discarded.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-signalingchannel.html#cfn-kinesisvideo-signalingchannel-messagettlseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "messageTtlSeconds"))

    @message_ttl_seconds.setter
    def message_ttl_seconds(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__64e792176b4ee3094144d172f0b05833d32a0f789cc5cd10e1e75a18d3d72436)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "messageTtlSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the signaling channel that you are creating.

        It must be unique for each AWS account and AWS Region .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-signalingchannel.html#cfn-kinesisvideo-signalingchannel-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36de142e4cc8bc5788f1ab28bd40260a56254601ae7ef8784fd2968e1bdd8763)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''A type of the signaling channel that you are creating.

        Currently, ``SINGLE_MASTER`` is the only supported channel type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-signalingchannel.html#cfn-kinesisvideo-signalingchannel-type
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d0bae06b6d886878a0d937e85c9d54342993149b8642f77e0dc244494705332)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesisvideo.CfnSignalingChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "message_ttl_seconds": "messageTtlSeconds",
        "name": "name",
        "tags": "tags",
        "type": "type",
    },
)
class CfnSignalingChannelProps:
    def __init__(
        self,
        *,
        message_ttl_seconds: typing.Optional[jsii.Number] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnSignalingChannel``.

        :param message_ttl_seconds: The period of time a signaling channel retains undelivered messages before they are discarded.
        :param name: A name for the signaling channel that you are creating. It must be unique for each AWS account and AWS Region .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param type: A type of the signaling channel that you are creating. Currently, ``SINGLE_MASTER`` is the only supported channel type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-signalingchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_kinesisvideo as kinesisvideo
            
            cfn_signaling_channel_props = kinesisvideo.CfnSignalingChannelProps(
                message_ttl_seconds=123,
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54d6098391ae923ec16bad8e2e78bc6edac447db307348a931db56ae8284453c)
            check_type(argname="argument message_ttl_seconds", value=message_ttl_seconds, expected_type=type_hints["message_ttl_seconds"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if message_ttl_seconds is not None:
            self._values["message_ttl_seconds"] = message_ttl_seconds
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def message_ttl_seconds(self) -> typing.Optional[jsii.Number]:
        '''The period of time a signaling channel retains undelivered messages before they are discarded.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-signalingchannel.html#cfn-kinesisvideo-signalingchannel-messagettlseconds
        '''
        result = self._values.get("message_ttl_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for the signaling channel that you are creating.

        It must be unique for each AWS account and AWS Region .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-signalingchannel.html#cfn-kinesisvideo-signalingchannel-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-signalingchannel.html#cfn-kinesisvideo-signalingchannel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''A type of the signaling channel that you are creating.

        Currently, ``SINGLE_MASTER`` is the only supported channel type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-signalingchannel.html#cfn-kinesisvideo-signalingchannel-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSignalingChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnStream(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-kinesisvideo.CfnStream",
):
    '''A CloudFormation ``AWS::KinesisVideo::Stream``.

    Specifies a new Kinesis video stream.

    When you create a new stream, Kinesis Video Streams assigns it a version number. When you change the stream's metadata, Kinesis Video Streams updates the version.

    ``CreateStream`` is an asynchronous operation.

    For information about how the service works, see `How it Works <https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/how-it-works.html>`_ .

    You must have permissions for the ``KinesisVideo:CreateStream`` action.

    :cloudformationResource: AWS::KinesisVideo::Stream
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_kinesisvideo as kinesisvideo
        
        cfn_stream = kinesisvideo.CfnStream(self, "MyCfnStream",
            data_retention_in_hours=123,
            device_name="deviceName",
            kms_key_id="kmsKeyId",
            media_type="mediaType",
            name="name",
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
        data_retention_in_hours: typing.Optional[jsii.Number] = None,
        device_name: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        media_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::KinesisVideo::Stream``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param data_retention_in_hours: How long the stream retains data, in hours.
        :param device_name: The name of the device that is associated with the stream.
        :param kms_key_id: The ID of the AWS Key Management Service ( AWS KMS ) key that Kinesis Video Streams uses to encrypt data on the stream.
        :param media_type: The ``MediaType`` of the stream.
        :param name: The name of the stream.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b6c414cd96c8455b7c228801c8fd5827da3c19271ee31c0cbc18bb27a2264fa7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStreamProps(
            data_retention_in_hours=data_retention_in_hours,
            device_name=device_name,
            kms_key_id=kms_key_id,
            media_type=media_type,
            name=name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b19ec39330d2d2d201b4899e5d1ceed92198ac73792094dd096e79aa8655a62b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__99f2fea18f3459ca385a88869c7d145c27352679becab76c9efbec3e1a5e2201)
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
        '''The Amazon Resource Name (ARN) of the stream.

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
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="dataRetentionInHours")
    def data_retention_in_hours(self) -> typing.Optional[jsii.Number]:
        '''How long the stream retains data, in hours.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-dataretentioninhours
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "dataRetentionInHours"))

    @data_retention_in_hours.setter
    def data_retention_in_hours(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52ffb11fe0b5aacfe07932ee466150d62946ebccbe035e3813612e6a324d88bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dataRetentionInHours", value)

    @builtins.property
    @jsii.member(jsii_name="deviceName")
    def device_name(self) -> typing.Optional[builtins.str]:
        '''The name of the device that is associated with the stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-devicename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deviceName"))

    @device_name.setter
    def device_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8128e1f465bdfb6068d5bf2d728c31817982d46750745e43b62634ab65a0e11)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deviceName", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the AWS Key Management Service ( AWS KMS ) key that Kinesis Video Streams uses to encrypt data on the stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dbbae3ea70a6fadc89941ceef7d181be6f0a22f9071a29dde4e21f3bd2458ec)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="mediaType")
    def media_type(self) -> typing.Optional[builtins.str]:
        '''The ``MediaType`` of the stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-mediatype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mediaType"))

    @media_type.setter
    def media_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97571e185d1721b7682d3509b62b5e3cb6897c9457ccc709308a089c6a81be65)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mediaType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8718de6ec4163e0f7e691629dabeaa8d3b10f009a00694779300d11b352f01a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-kinesisvideo.CfnStreamProps",
    jsii_struct_bases=[],
    name_mapping={
        "data_retention_in_hours": "dataRetentionInHours",
        "device_name": "deviceName",
        "kms_key_id": "kmsKeyId",
        "media_type": "mediaType",
        "name": "name",
        "tags": "tags",
    },
)
class CfnStreamProps:
    def __init__(
        self,
        *,
        data_retention_in_hours: typing.Optional[jsii.Number] = None,
        device_name: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        media_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnStream``.

        :param data_retention_in_hours: How long the stream retains data, in hours.
        :param device_name: The name of the device that is associated with the stream.
        :param kms_key_id: The ID of the AWS Key Management Service ( AWS KMS ) key that Kinesis Video Streams uses to encrypt data on the stream.
        :param media_type: The ``MediaType`` of the stream.
        :param name: The name of the stream.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_kinesisvideo as kinesisvideo
            
            cfn_stream_props = kinesisvideo.CfnStreamProps(
                data_retention_in_hours=123,
                device_name="deviceName",
                kms_key_id="kmsKeyId",
                media_type="mediaType",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc3d78e9ade52dd80a0ce4e676ce9af600058a6679931aee619dccc96de20140)
            check_type(argname="argument data_retention_in_hours", value=data_retention_in_hours, expected_type=type_hints["data_retention_in_hours"])
            check_type(argname="argument device_name", value=device_name, expected_type=type_hints["device_name"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument media_type", value=media_type, expected_type=type_hints["media_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if data_retention_in_hours is not None:
            self._values["data_retention_in_hours"] = data_retention_in_hours
        if device_name is not None:
            self._values["device_name"] = device_name
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if media_type is not None:
            self._values["media_type"] = media_type
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def data_retention_in_hours(self) -> typing.Optional[jsii.Number]:
        '''How long the stream retains data, in hours.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-dataretentioninhours
        '''
        result = self._values.get("data_retention_in_hours")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def device_name(self) -> typing.Optional[builtins.str]:
        '''The name of the device that is associated with the stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-devicename
        '''
        result = self._values.get("device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the AWS Key Management Service ( AWS KMS ) key that Kinesis Video Streams uses to encrypt data on the stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def media_type(self) -> typing.Optional[builtins.str]:
        '''The ``MediaType`` of the stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-mediatype
        '''
        result = self._values.get("media_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisvideo-stream.html#cfn-kinesisvideo-stream-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnSignalingChannel",
    "CfnSignalingChannelProps",
    "CfnStream",
    "CfnStreamProps",
]

publication.publish()

def _typecheckingstub__961e1bd08ac2456689473efb67cf521c3a6db38334cc60575a3ab304d24d4fc4(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    message_ttl_seconds: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45a7dfc1ecc46ddd9cc1ccedee8e1ad2d53b3a3e54bb3d64c8365cd136e19250(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd53d26282726cad857bc607290570a09225859587036008413324c833803fc9(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64e792176b4ee3094144d172f0b05833d32a0f789cc5cd10e1e75a18d3d72436(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36de142e4cc8bc5788f1ab28bd40260a56254601ae7ef8784fd2968e1bdd8763(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d0bae06b6d886878a0d937e85c9d54342993149b8642f77e0dc244494705332(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54d6098391ae923ec16bad8e2e78bc6edac447db307348a931db56ae8284453c(
    *,
    message_ttl_seconds: typing.Optional[jsii.Number] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6c414cd96c8455b7c228801c8fd5827da3c19271ee31c0cbc18bb27a2264fa7(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    data_retention_in_hours: typing.Optional[jsii.Number] = None,
    device_name: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    media_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b19ec39330d2d2d201b4899e5d1ceed92198ac73792094dd096e79aa8655a62b(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99f2fea18f3459ca385a88869c7d145c27352679becab76c9efbec3e1a5e2201(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52ffb11fe0b5aacfe07932ee466150d62946ebccbe035e3813612e6a324d88bd(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8128e1f465bdfb6068d5bf2d728c31817982d46750745e43b62634ab65a0e11(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dbbae3ea70a6fadc89941ceef7d181be6f0a22f9071a29dde4e21f3bd2458ec(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97571e185d1721b7682d3509b62b5e3cb6897c9457ccc709308a089c6a81be65(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8718de6ec4163e0f7e691629dabeaa8d3b10f009a00694779300d11b352f01a2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc3d78e9ade52dd80a0ce4e676ce9af600058a6679931aee619dccc96de20140(
    *,
    data_retention_in_hours: typing.Optional[jsii.Number] = None,
    device_name: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    media_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
