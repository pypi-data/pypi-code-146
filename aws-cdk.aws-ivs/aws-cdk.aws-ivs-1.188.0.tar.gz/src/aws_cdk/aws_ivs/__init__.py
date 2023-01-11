'''
# AWS::IVS Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

Amazon Interactive Video Service (Amazon IVS) is a managed live streaming
solution that is quick and easy to set up, and ideal for creating interactive
video experiences. Send your live streams to Amazon IVS using streaming software
and the service does everything you need to make low-latency live video
available to any viewer around the world, letting you focus on building
interactive experiences alongside the live video. You can easily customize and
enhance the audience experience through the Amazon IVS player SDK and timed
metadata APIs, allowing you to build a more valuable relationship with your
viewers on your own websites and applications.

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Channels

An Amazon IVS channel stores configuration information related to your live
stream. You first create a channel and then contribute video to it using the
channel’s stream key to start your live stream.

You can create a channel

```python
my_channel = ivs.Channel(self, "Channel")
```

### Importing an existing channel

You can reference an existing channel, for example, if you need to create a
stream key for an existing channel

```python
my_channel = ivs.Channel.from_channel_arn(self, "Channel", my_channel_arn)
```

## Stream Keys

A Stream Key is used by a broadcast encoder to initiate a stream and identify
to Amazon IVS which customer and channel the stream is for. If you are
storing this value, it should be treated as if it were a password.

You can create a stream key for a given channel

```python
my_stream_key = my_channel.add_stream_key("StreamKey")
```

## Private Channels

Amazon IVS offers the ability to create private channels, allowing
you to restrict your streams by channel or viewer. You control access
to video playback by enabling playback authorization on channels and
generating signed JSON Web Tokens (JWTs) for authorized playback requests.

A playback token is a JWT that you sign (with a playback authorization key)
and include with every playback request for a channel that has playback
authorization enabled.

In order for Amazon IVS to validate the token, you need to upload
the public key that corresponds to the private key you use to sign the token.

```python
key_pair = ivs.PlaybackKeyPair(self, "PlaybackKeyPair",
    public_key_material=my_public_key_pem_string
)
```

Then, when creating a channel, specify the authorized property

```python
my_channel = ivs.Channel(self, "Channel",
    authorized=True
)
```
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnChannel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ivs.CfnChannel",
):
    '''A CloudFormation ``AWS::IVS::Channel``.

    The ``AWS::IVS::Channel`` resource specifies an  channel. A channel stores configuration information related to your live stream. For more information, see `CreateChannel <https://docs.aws.amazon.com/ivs/latest/APIReference/API_CreateChannel.html>`_ in the *Amazon Interactive Video Service API Reference* .
    .. epigraph::

       By default, the IVS API CreateChannel endpoint creates a stream key in addition to a channel. The  Channel resource *does not* create a stream key; to create a stream key, use the StreamKey resource instead.

    :cloudformationResource: AWS::IVS::Channel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ivs as ivs
        
        cfn_channel = ivs.CfnChannel(self, "MyCfnChannel",
            authorized=False,
            latency_mode="latencyMode",
            name="name",
            recording_configuration_arn="recordingConfigurationArn",
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
        authorized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        latency_mode: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        recording_configuration_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::IVS::Channel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param authorized: Whether the channel is authorized. *Default* : ``false``
        :param latency_mode: Channel latency mode. Valid values:. - ``NORMAL`` : Use NORMAL to broadcast and deliver live video up to Full HD. - ``LOW`` : Use LOW for near real-time interactions with viewers. .. epigraph:: In the console, ``LOW`` and ``NORMAL`` correspond to ``Ultra-low`` and ``Standard`` , respectively. *Default* : ``LOW``
        :param name: Channel name.
        :param recording_configuration_arn: The ARN of a RecordingConfiguration resource. An empty string indicates that recording is disabled for the channel. A RecordingConfiguration ARN indicates that recording is enabled using the specified recording configuration. See the `RecordingConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html>`_ resource for more information and an example. *Default* : "" (empty string, recording is disabled)
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param type: The channel type, which determines the allowable resolution and bitrate. *If you exceed the allowable resolution or bitrate, the stream probably will disconnect immediately.* Valid values: - ``STANDARD`` : Video is transcoded: multiple qualities are generated from the original input to automatically give viewers the best experience for their devices and network conditions. Transcoding allows higher playback quality across a range of download speeds. Resolution can be up to 1080p and bitrate can be up to 8.5 Mbps. Audio is transcoded only for renditions 360p and below; above that, audio is passed through. - ``BASIC`` : Video is transmuxed: Amazon IVS delivers the original input to viewers. The viewer’s video-quality choice is limited to the original input. Resolution can be up to 1080p and bitrate can be up to 1.5 Mbps for 480p and up to 3.5 Mbps for resolutions between 480p and 1080p. *Default* : ``STANDARD``
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49be12fe1f38ed9c33dec23ad664f18867cf2a35360912c221c659e48cac4695)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnChannelProps(
            authorized=authorized,
            latency_mode=latency_mode,
            name=name,
            recording_configuration_arn=recording_configuration_arn,
            tags=tags,
            type=type,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e602c9fe026a76c66a38e53e3eb7ab3e3e6bf0be5acc9c8aa9c053dad5f1205)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cee82e9e7ec5f66518c5edbdb7234356cd7660053374c96a41c918f080beb3e)
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
        '''The channel ARN.

        For example: ``arn:aws:ivs:us-west-2:123456789012:channel/abcdABCDefgh``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrIngestEndpoint")
    def attr_ingest_endpoint(self) -> builtins.str:
        '''Channel ingest endpoint, part of the definition of an ingest server, used when you set up streaming software.

        For example: ``a1b2c3d4e5f6.global-contribute.live-video.net``

        :cloudformationAttribute: IngestEndpoint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrIngestEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="attrPlaybackUrl")
    def attr_playback_url(self) -> builtins.str:
        '''Channel playback URL.

        For example: ``https://a1b2c3d4e5f6.us-west-2.playback.live-video.net/api/video/v1/us-west-2.123456789012.channel.abcdEFGH.m3u8``

        :cloudformationAttribute: PlaybackUrl
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPlaybackUrl"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="authorized")
    def authorized(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Whether the channel is authorized.

        *Default* : ``false``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-authorized
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "authorized"))

    @authorized.setter
    def authorized(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a177793aff6b53af7dcd951960186bfe1fc0cf2f812ffb1312e57bc84b69c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authorized", value)

    @builtins.property
    @jsii.member(jsii_name="latencyMode")
    def latency_mode(self) -> typing.Optional[builtins.str]:
        '''Channel latency mode. Valid values:.

        - ``NORMAL`` : Use NORMAL to broadcast and deliver live video up to Full HD.
        - ``LOW`` : Use LOW for near real-time interactions with viewers.

        .. epigraph::

           In the  console, ``LOW`` and ``NORMAL`` correspond to ``Ultra-low`` and ``Standard`` , respectively.

        *Default* : ``LOW``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-latencymode
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "latencyMode"))

    @latency_mode.setter
    def latency_mode(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bee2e2db8299c6a00a147093ebaa19782be6f39ec78b0769f097965ba08574dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "latencyMode", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''Channel name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__caf2096317c6f1414c874e1a6f4689c4809861c1baf399830ffd93975ce58988)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="recordingConfigurationArn")
    def recording_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of a RecordingConfiguration resource.

        An empty string indicates that recording is disabled for the channel. A RecordingConfiguration ARN indicates that recording is enabled using the specified recording configuration. See the `RecordingConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html>`_ resource for more information and an example.

        *Default* : "" (empty string, recording is disabled)

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-recordingconfigurationarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recordingConfigurationArn"))

    @recording_configuration_arn.setter
    def recording_configuration_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0142d4dd6139b4c80e170cd41a4a79596cfb983c53b8c63db1a5d672c9ccd67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordingConfigurationArn", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''The channel type, which determines the allowable resolution and bitrate.

        *If you exceed the allowable resolution or bitrate, the stream probably will disconnect immediately.* Valid values:

        - ``STANDARD`` : Video is transcoded: multiple qualities are generated from the original input to automatically give viewers the best experience for their devices and network conditions. Transcoding allows higher playback quality across a range of download speeds. Resolution can be up to 1080p and bitrate can be up to 8.5 Mbps. Audio is transcoded only for renditions 360p and below; above that, audio is passed through.
        - ``BASIC`` : Video is transmuxed: Amazon IVS delivers the original input to viewers. The viewer’s video-quality choice is limited to the original input. Resolution can be up to 1080p and bitrate can be up to 1.5 Mbps for 480p and up to 3.5 Mbps for resolutions between 480p and 1080p.

        *Default* : ``STANDARD``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-type
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2fe6ae1b755c4ffd1aa78afb50a45dbb6c916430aa7a932a476548f084ed321)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ivs.CfnChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "authorized": "authorized",
        "latency_mode": "latencyMode",
        "name": "name",
        "recording_configuration_arn": "recordingConfigurationArn",
        "tags": "tags",
        "type": "type",
    },
)
class CfnChannelProps:
    def __init__(
        self,
        *,
        authorized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        latency_mode: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        recording_configuration_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnChannel``.

        :param authorized: Whether the channel is authorized. *Default* : ``false``
        :param latency_mode: Channel latency mode. Valid values:. - ``NORMAL`` : Use NORMAL to broadcast and deliver live video up to Full HD. - ``LOW`` : Use LOW for near real-time interactions with viewers. .. epigraph:: In the console, ``LOW`` and ``NORMAL`` correspond to ``Ultra-low`` and ``Standard`` , respectively. *Default* : ``LOW``
        :param name: Channel name.
        :param recording_configuration_arn: The ARN of a RecordingConfiguration resource. An empty string indicates that recording is disabled for the channel. A RecordingConfiguration ARN indicates that recording is enabled using the specified recording configuration. See the `RecordingConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html>`_ resource for more information and an example. *Default* : "" (empty string, recording is disabled)
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param type: The channel type, which determines the allowable resolution and bitrate. *If you exceed the allowable resolution or bitrate, the stream probably will disconnect immediately.* Valid values: - ``STANDARD`` : Video is transcoded: multiple qualities are generated from the original input to automatically give viewers the best experience for their devices and network conditions. Transcoding allows higher playback quality across a range of download speeds. Resolution can be up to 1080p and bitrate can be up to 8.5 Mbps. Audio is transcoded only for renditions 360p and below; above that, audio is passed through. - ``BASIC`` : Video is transmuxed: Amazon IVS delivers the original input to viewers. The viewer’s video-quality choice is limited to the original input. Resolution can be up to 1080p and bitrate can be up to 1.5 Mbps for 480p and up to 3.5 Mbps for resolutions between 480p and 1080p. *Default* : ``STANDARD``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ivs as ivs
            
            cfn_channel_props = ivs.CfnChannelProps(
                authorized=False,
                latency_mode="latencyMode",
                name="name",
                recording_configuration_arn="recordingConfigurationArn",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                type="type"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b6b94e41ea63a88d5416b041469e00329fcfcc9f82be5b420ee03a04449e08e)
            check_type(argname="argument authorized", value=authorized, expected_type=type_hints["authorized"])
            check_type(argname="argument latency_mode", value=latency_mode, expected_type=type_hints["latency_mode"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument recording_configuration_arn", value=recording_configuration_arn, expected_type=type_hints["recording_configuration_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorized is not None:
            self._values["authorized"] = authorized
        if latency_mode is not None:
            self._values["latency_mode"] = latency_mode
        if name is not None:
            self._values["name"] = name
        if recording_configuration_arn is not None:
            self._values["recording_configuration_arn"] = recording_configuration_arn
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def authorized(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Whether the channel is authorized.

        *Default* : ``false``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-authorized
        '''
        result = self._values.get("authorized")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def latency_mode(self) -> typing.Optional[builtins.str]:
        '''Channel latency mode. Valid values:.

        - ``NORMAL`` : Use NORMAL to broadcast and deliver live video up to Full HD.
        - ``LOW`` : Use LOW for near real-time interactions with viewers.

        .. epigraph::

           In the  console, ``LOW`` and ``NORMAL`` correspond to ``Ultra-low`` and ``Standard`` , respectively.

        *Default* : ``LOW``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-latencymode
        '''
        result = self._values.get("latency_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Channel name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recording_configuration_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of a RecordingConfiguration resource.

        An empty string indicates that recording is disabled for the channel. A RecordingConfiguration ARN indicates that recording is enabled using the specified recording configuration. See the `RecordingConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html>`_ resource for more information and an example.

        *Default* : "" (empty string, recording is disabled)

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-recordingconfigurationarn
        '''
        result = self._values.get("recording_configuration_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The channel type, which determines the allowable resolution and bitrate.

        *If you exceed the allowable resolution or bitrate, the stream probably will disconnect immediately.* Valid values:

        - ``STANDARD`` : Video is transcoded: multiple qualities are generated from the original input to automatically give viewers the best experience for their devices and network conditions. Transcoding allows higher playback quality across a range of download speeds. Resolution can be up to 1080p and bitrate can be up to 8.5 Mbps. Audio is transcoded only for renditions 360p and below; above that, audio is passed through.
        - ``BASIC`` : Video is transmuxed: Amazon IVS delivers the original input to viewers. The viewer’s video-quality choice is limited to the original input. Resolution can be up to 1080p and bitrate can be up to 1.5 Mbps for 480p and up to 3.5 Mbps for resolutions between 480p and 1080p.

        *Default* : ``STANDARD``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html#cfn-ivs-channel-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnPlaybackKeyPair(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ivs.CfnPlaybackKeyPair",
):
    '''A CloudFormation ``AWS::IVS::PlaybackKeyPair``.

    The ``AWS::IVS::PlaybackKeyPair`` resource specifies an  playback key pair.  uses a public playback key to validate playback tokens that have been signed with the corresponding private key. For more information, see `Setting Up Private Channels <https://docs.aws.amazon.com/ivs/latest/userguide/private-channels.html>`_ in the *Amazon Interactive Video Service User Guide* .

    :cloudformationResource: AWS::IVS::PlaybackKeyPair
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ivs as ivs
        
        cfn_playback_key_pair = ivs.CfnPlaybackKeyPair(self, "MyCfnPlaybackKeyPair",
            name="name",
            public_key_material="publicKeyMaterial",
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
        name: typing.Optional[builtins.str] = None,
        public_key_material: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IVS::PlaybackKeyPair``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: Playback-key-pair name. The value does not need to be unique.
        :param public_key_material: The public portion of a customer-generated key pair.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6243183d4c8423c420991a7b133706df1f5b6c311c1cb4978e82282054e3f24c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPlaybackKeyPairProps(
            name=name, public_key_material=public_key_material, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44eb4da6d50b28f1244ccbe4763d17283dcdda097880d1bc19b2af4ce82022ef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa1d101c639b7fdea78f89aa8f85b67dad33f03cbc27669c091a7432f07b88fe)
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
        '''Key-pair ARN.

        For example: ``arn:aws:ivs:us-west-2:693991300569:playback-key/f99cde61-c2b0-4df3-8941-ca7d38acca1a``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrFingerprint")
    def attr_fingerprint(self) -> builtins.str:
        '''Key-pair identifier.

        For example: ``98:0d:1a:a0:19:96:1e:ea:0a:0a:2c:9a:42:19:2b:e7``

        :cloudformationAttribute: Fingerprint
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFingerprint"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html#cfn-ivs-playbackkeypair-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''Playback-key-pair name.

        The value does not need to be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html#cfn-ivs-playbackkeypair-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52f39a5ebcadebf9f1261f1ad384acc6bad76ea39182302282fbca92a11d42d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="publicKeyMaterial")
    def public_key_material(self) -> typing.Optional[builtins.str]:
        '''The public portion of a customer-generated key pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html#cfn-ivs-playbackkeypair-publickeymaterial
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "publicKeyMaterial"))

    @public_key_material.setter
    def public_key_material(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3ad3e8fc80edf0ee6bf99554700d864ae2fe3d20bfc992ec743041e6abadf2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicKeyMaterial", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ivs.CfnPlaybackKeyPairProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "public_key_material": "publicKeyMaterial",
        "tags": "tags",
    },
)
class CfnPlaybackKeyPairProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        public_key_material: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPlaybackKeyPair``.

        :param name: Playback-key-pair name. The value does not need to be unique.
        :param public_key_material: The public portion of a customer-generated key pair.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ivs as ivs
            
            cfn_playback_key_pair_props = ivs.CfnPlaybackKeyPairProps(
                name="name",
                public_key_material="publicKeyMaterial",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d007241b49fcc0c7cdc24afceaa4b235cf27e76205563c474814c174764d824c)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument public_key_material", value=public_key_material, expected_type=type_hints["public_key_material"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if public_key_material is not None:
            self._values["public_key_material"] = public_key_material
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Playback-key-pair name.

        The value does not need to be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html#cfn-ivs-playbackkeypair-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def public_key_material(self) -> typing.Optional[builtins.str]:
        '''The public portion of a customer-generated key pair.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html#cfn-ivs-playbackkeypair-publickeymaterial
        '''
        result = self._values.get("public_key_material")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-playbackkeypair.html#cfn-ivs-playbackkeypair-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPlaybackKeyPairProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRecordingConfiguration(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ivs.CfnRecordingConfiguration",
):
    '''A CloudFormation ``AWS::IVS::RecordingConfiguration``.

    The ``AWS::IVS::RecordingConfiguration`` resource specifies an  recording configuration. A recording configuration enables the recording of a channel’s live streams to a data store. Multiple channels can reference the same recording configuration. For more information, see `RecordingConfiguration <https://docs.aws.amazon.com/ivs/latest/APIReference/API_RecordingConfiguration.html>`_ in the *Amazon Interactive Video Service API Reference* .

    :cloudformationResource: AWS::IVS::RecordingConfiguration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ivs as ivs
        
        cfn_recording_configuration = ivs.CfnRecordingConfiguration(self, "MyCfnRecordingConfiguration",
            destination_configuration=ivs.CfnRecordingConfiguration.DestinationConfigurationProperty(
                s3=ivs.CfnRecordingConfiguration.S3DestinationConfigurationProperty(
                    bucket_name="bucketName"
                )
            ),
        
            # the properties below are optional
            name="name",
            recording_reconnect_window_seconds=123,
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            thumbnail_configuration=ivs.CfnRecordingConfiguration.ThumbnailConfigurationProperty(
                recording_mode="recordingMode",
        
                # the properties below are optional
                target_interval_seconds=123
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        destination_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRecordingConfiguration.DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        name: typing.Optional[builtins.str] = None,
        recording_reconnect_window_seconds: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        thumbnail_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRecordingConfiguration.ThumbnailConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IVS::RecordingConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_configuration: A destination configuration contains information about where recorded video will be stored. See the `DestinationConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-destinationconfiguration.html>`_ property type for more information.
        :param name: Recording-configuration name. The value does not need to be unique.
        :param recording_reconnect_window_seconds: If a broadcast disconnects and then reconnects within the specified interval, the multiple streams will be considered a single broadcast and merged together. *Default* : ``0``
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param thumbnail_configuration: A thumbnail configuration enables/disables the recording of thumbnails for a live session and controls the interval at which thumbnails are generated for the live session. See the `ThumbnailConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thunbnailconfiguration.html>`_ property type for more information.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc1f7f59bfe6ef830c02e1cef7e92524dd4a813d3844f26bb97ff71bfbc9f7a8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRecordingConfigurationProps(
            destination_configuration=destination_configuration,
            name=name,
            recording_reconnect_window_seconds=recording_reconnect_window_seconds,
            tags=tags,
            thumbnail_configuration=thumbnail_configuration,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__394123dc466235c21b1da90745c9013426a71b63a0b9dd27484661ee0fc91d8a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c01b11456c9fb31e9821d387889aaf9f258c723b9fd7d87e2a072291348f1859)
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
        '''The recording configuration ARN.

        For example: ``arn:aws:ivs:us-west-2:123456789012:recording-configuration/abcdABCDefgh``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''Indicates the current state of the recording configuration.

        When the state is ``ACTIVE`` , the configuration is ready to record a channel stream. Valid values: ``CREATING`` | ``CREATE_FAILED`` | ``ACTIVE`` .

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html#cfn-ivs-recordingconfiguration-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="destinationConfiguration")
    def destination_configuration(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRecordingConfiguration.DestinationConfigurationProperty"]:
        '''A destination configuration contains information about where recorded video will be stored.

        See the `DestinationConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-destinationconfiguration.html>`_ property type for more information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html#cfn-ivs-recordingconfiguration-destinationconfiguration
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRecordingConfiguration.DestinationConfigurationProperty"], jsii.get(self, "destinationConfiguration"))

    @destination_configuration.setter
    def destination_configuration(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRecordingConfiguration.DestinationConfigurationProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76c12dd2e6bca954b077dff37b7d9a3bbf88a8d7e4e2dcf8f143a05966e80c1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''Recording-configuration name.

        The value does not need to be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html#cfn-ivs-recordingconfiguration-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__91d029abb26d6f06c95a113dc08bbd3b1797a54b0318f3a15181db4977740bdc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="recordingReconnectWindowSeconds")
    def recording_reconnect_window_seconds(self) -> typing.Optional[jsii.Number]:
        '''If a broadcast disconnects and then reconnects within the specified interval, the multiple streams will be considered a single broadcast and merged together.

        *Default* : ``0``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html#cfn-ivs-recordingconfiguration-recordingreconnectwindowseconds
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "recordingReconnectWindowSeconds"))

    @recording_reconnect_window_seconds.setter
    def recording_reconnect_window_seconds(
        self,
        value: typing.Optional[jsii.Number],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0984a0f267178eb11c47eca7d03f1cba997ccc7b6e06df0033ec619a237acb1c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recordingReconnectWindowSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="thumbnailConfiguration")
    def thumbnail_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRecordingConfiguration.ThumbnailConfigurationProperty"]]:
        '''A thumbnail configuration enables/disables the recording of thumbnails for a live session and controls the interval at which thumbnails are generated for the live session.

        See the `ThumbnailConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thunbnailconfiguration.html>`_ property type for more information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html#cfn-ivs-recordingconfiguration-thumbnailconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRecordingConfiguration.ThumbnailConfigurationProperty"]], jsii.get(self, "thumbnailConfiguration"))

    @thumbnail_configuration.setter
    def thumbnail_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRecordingConfiguration.ThumbnailConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15b7162f28ce9297a0822e1b2ed3e3f5287defe20621a5a98078e0cfc11df6e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thumbnailConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ivs.CfnRecordingConfiguration.DestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"s3": "s3"},
    )
    class DestinationConfigurationProperty:
        def __init__(
            self,
            *,
            s3: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRecordingConfiguration.S3DestinationConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''The DestinationConfiguration property type describes the location where recorded videos will be stored.

            Each member represents a type of destination configuration. For recording, you define one and only one type of destination configuration.

            :param s3: An S3 destination configuration where recorded videos will be stored. See the `S3DestinationConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-s3destinationconfiguration.html>`_ property type for more information.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-destinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ivs as ivs
                
                destination_configuration_property = ivs.CfnRecordingConfiguration.DestinationConfigurationProperty(
                    s3=ivs.CfnRecordingConfiguration.S3DestinationConfigurationProperty(
                        bucket_name="bucketName"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a1c9fba07b1fceb2b4443463af1e444883ac000a67f4951327ad088cfa5d4b3)
                check_type(argname="argument s3", value=s3, expected_type=type_hints["s3"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3": s3,
            }

        @builtins.property
        def s3(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRecordingConfiguration.S3DestinationConfigurationProperty"]:
            '''An S3 destination configuration where recorded videos will be stored.

            See the `S3DestinationConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-s3destinationconfiguration.html>`_ property type for more information.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-destinationconfiguration.html#cfn-ivs-recordingconfiguration-destinationconfiguration-s3
            '''
            result = self._values.get("s3")
            assert result is not None, "Required property 's3' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRecordingConfiguration.S3DestinationConfigurationProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ivs.CfnRecordingConfiguration.S3DestinationConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName"},
    )
    class S3DestinationConfigurationProperty:
        def __init__(self, *, bucket_name: builtins.str) -> None:
            '''The S3DestinationConfiguration property type describes an S3 location where recorded videos will be stored.

            :param bucket_name: Location (S3 bucket name) where recorded videos will be stored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-s3destinationconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ivs as ivs
                
                s3_destination_configuration_property = ivs.CfnRecordingConfiguration.S3DestinationConfigurationProperty(
                    bucket_name="bucketName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__10f790191169448cf1196c16f2f4dd15330b1a6d5ed3dc23ff096a5ad90a6529)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
            }

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''Location (S3 bucket name) where recorded videos will be stored.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-s3destinationconfiguration.html#cfn-ivs-recordingconfiguration-s3destinationconfiguration-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3DestinationConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-ivs.CfnRecordingConfiguration.ThumbnailConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "recording_mode": "recordingMode",
            "target_interval_seconds": "targetIntervalSeconds",
        },
    )
    class ThumbnailConfigurationProperty:
        def __init__(
            self,
            *,
            recording_mode: builtins.str,
            target_interval_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The ThumbnailConfiguration property type describes a configuration of thumbnails for recorded video.

            :param recording_mode: Thumbnail recording mode. Valid values:. - ``DISABLED`` : Use DISABLED to disable the generation of thumbnails for recorded video. - ``INTERVAL`` : Use INTERVAL to enable the generation of thumbnails for recorded video at a time interval controlled by the `TargetIntervalSeconds <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thumbnailconfiguration.html#cfn-ivs-recordingconfiguration-thumbnailconfiguration-targetintervalseconds>`_ property. *Default* : ``INTERVAL``
            :param target_interval_seconds: The targeted thumbnail-generation interval in seconds. This is configurable (and required) only if `RecordingMode <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thumbnailconfiguration.html#cfn-ivs-recordingconfiguration-thumbnailconfiguration-recordingmode>`_ is ``INTERVAL`` . .. epigraph:: Setting a value for ``TargetIntervalSeconds`` does not guarantee that thumbnails are generated at the specified interval. For thumbnails to be generated at the ``TargetIntervalSeconds`` interval, the ``IDR/Keyframe`` value for the input video must be less than the ``TargetIntervalSeconds`` value. See `Amazon IVS Streaming Configuration <https://docs.aws.amazon.com/ivs/latest/userguide/streaming-config.html>`_ for information on setting ``IDR/Keyframe`` to the recommended value in video-encoder settings. *Default* : 60 *Valid Range* : Minumum value of 5. Maximum value of 60.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thumbnailconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_ivs as ivs
                
                thumbnail_configuration_property = ivs.CfnRecordingConfiguration.ThumbnailConfigurationProperty(
                    recording_mode="recordingMode",
                
                    # the properties below are optional
                    target_interval_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f1516e49c9f8d6ae8778e6654cac7a77d28d2a77cecc6c97e1e348336ccd7c5b)
                check_type(argname="argument recording_mode", value=recording_mode, expected_type=type_hints["recording_mode"])
                check_type(argname="argument target_interval_seconds", value=target_interval_seconds, expected_type=type_hints["target_interval_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "recording_mode": recording_mode,
            }
            if target_interval_seconds is not None:
                self._values["target_interval_seconds"] = target_interval_seconds

        @builtins.property
        def recording_mode(self) -> builtins.str:
            '''Thumbnail recording mode. Valid values:.

            - ``DISABLED`` : Use DISABLED to disable the generation of thumbnails for recorded video.
            - ``INTERVAL`` : Use INTERVAL to enable the generation of thumbnails for recorded video at a time interval controlled by the `TargetIntervalSeconds <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thumbnailconfiguration.html#cfn-ivs-recordingconfiguration-thumbnailconfiguration-targetintervalseconds>`_ property.

            *Default* : ``INTERVAL``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thumbnailconfiguration.html#cfn-ivs-recordingconfiguration-thumbnailconfiguration-recordingmode
            '''
            result = self._values.get("recording_mode")
            assert result is not None, "Required property 'recording_mode' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def target_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''The targeted thumbnail-generation interval in seconds. This is configurable (and required) only if `RecordingMode <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thumbnailconfiguration.html#cfn-ivs-recordingconfiguration-thumbnailconfiguration-recordingmode>`_ is ``INTERVAL`` .

            .. epigraph::

               Setting a value for ``TargetIntervalSeconds`` does not guarantee that thumbnails are generated at the specified interval. For thumbnails to be generated at the ``TargetIntervalSeconds`` interval, the ``IDR/Keyframe`` value for the input video must be less than the ``TargetIntervalSeconds`` value. See `Amazon IVS Streaming Configuration <https://docs.aws.amazon.com/ivs/latest/userguide/streaming-config.html>`_ for information on setting ``IDR/Keyframe`` to the recommended value in video-encoder settings.

            *Default* : 60

            *Valid Range* : Minumum value of 5. Maximum value of 60.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thumbnailconfiguration.html#cfn-ivs-recordingconfiguration-thumbnailconfiguration-targetintervalseconds
            '''
            result = self._values.get("target_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ThumbnailConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ivs.CfnRecordingConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_configuration": "destinationConfiguration",
        "name": "name",
        "recording_reconnect_window_seconds": "recordingReconnectWindowSeconds",
        "tags": "tags",
        "thumbnail_configuration": "thumbnailConfiguration",
    },
)
class CfnRecordingConfigurationProps:
    def __init__(
        self,
        *,
        destination_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRecordingConfiguration.DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
        name: typing.Optional[builtins.str] = None,
        recording_reconnect_window_seconds: typing.Optional[jsii.Number] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        thumbnail_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRecordingConfiguration.ThumbnailConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRecordingConfiguration``.

        :param destination_configuration: A destination configuration contains information about where recorded video will be stored. See the `DestinationConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-destinationconfiguration.html>`_ property type for more information.
        :param name: Recording-configuration name. The value does not need to be unique.
        :param recording_reconnect_window_seconds: If a broadcast disconnects and then reconnects within the specified interval, the multiple streams will be considered a single broadcast and merged together. *Default* : ``0``
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        :param thumbnail_configuration: A thumbnail configuration enables/disables the recording of thumbnails for a live session and controls the interval at which thumbnails are generated for the live session. See the `ThumbnailConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thunbnailconfiguration.html>`_ property type for more information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ivs as ivs
            
            cfn_recording_configuration_props = ivs.CfnRecordingConfigurationProps(
                destination_configuration=ivs.CfnRecordingConfiguration.DestinationConfigurationProperty(
                    s3=ivs.CfnRecordingConfiguration.S3DestinationConfigurationProperty(
                        bucket_name="bucketName"
                    )
                ),
            
                # the properties below are optional
                name="name",
                recording_reconnect_window_seconds=123,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                thumbnail_configuration=ivs.CfnRecordingConfiguration.ThumbnailConfigurationProperty(
                    recording_mode="recordingMode",
            
                    # the properties below are optional
                    target_interval_seconds=123
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7e54bda807c048eb2ba5f6be1eaaeae0e66d5b936b1e960f6e716ea8932d292)
            check_type(argname="argument destination_configuration", value=destination_configuration, expected_type=type_hints["destination_configuration"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument recording_reconnect_window_seconds", value=recording_reconnect_window_seconds, expected_type=type_hints["recording_reconnect_window_seconds"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument thumbnail_configuration", value=thumbnail_configuration, expected_type=type_hints["thumbnail_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_configuration": destination_configuration,
        }
        if name is not None:
            self._values["name"] = name
        if recording_reconnect_window_seconds is not None:
            self._values["recording_reconnect_window_seconds"] = recording_reconnect_window_seconds
        if tags is not None:
            self._values["tags"] = tags
        if thumbnail_configuration is not None:
            self._values["thumbnail_configuration"] = thumbnail_configuration

    @builtins.property
    def destination_configuration(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRecordingConfiguration.DestinationConfigurationProperty]:
        '''A destination configuration contains information about where recorded video will be stored.

        See the `DestinationConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-destinationconfiguration.html>`_ property type for more information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html#cfn-ivs-recordingconfiguration-destinationconfiguration
        '''
        result = self._values.get("destination_configuration")
        assert result is not None, "Required property 'destination_configuration' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRecordingConfiguration.DestinationConfigurationProperty], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''Recording-configuration name.

        The value does not need to be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html#cfn-ivs-recordingconfiguration-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recording_reconnect_window_seconds(self) -> typing.Optional[jsii.Number]:
        '''If a broadcast disconnects and then reconnects within the specified interval, the multiple streams will be considered a single broadcast and merged together.

        *Default* : ``0``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html#cfn-ivs-recordingconfiguration-recordingreconnectwindowseconds
        '''
        result = self._values.get("recording_reconnect_window_seconds")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html#cfn-ivs-recordingconfiguration-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def thumbnail_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRecordingConfiguration.ThumbnailConfigurationProperty]]:
        '''A thumbnail configuration enables/disables the recording of thumbnails for a live session and controls the interval at which thumbnails are generated for the live session.

        See the `ThumbnailConfiguration <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ivs-recordingconfiguration-thunbnailconfiguration.html>`_ property type for more information.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-recordingconfiguration.html#cfn-ivs-recordingconfiguration-thumbnailconfiguration
        '''
        result = self._values.get("thumbnail_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRecordingConfiguration.ThumbnailConfigurationProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRecordingConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnStreamKey(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ivs.CfnStreamKey",
):
    '''A CloudFormation ``AWS::IVS::StreamKey``.

    The ``AWS::IVS::StreamKey`` resource specifies an  stream key associated with the referenced channel. Use a stream key to initiate a live stream.

    :cloudformationResource: AWS::IVS::StreamKey
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-streamkey.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ivs as ivs
        
        cfn_stream_key = ivs.CfnStreamKey(self, "MyCfnStreamKey",
            channel_arn="channelArn",
        
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
        channel_arn: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IVS::StreamKey``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param channel_arn: Channel ARN for the stream.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad4745815acea57eff3ecd2f7cb2ba4a8613ce7519c2165fd1f60b0ead28b89a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStreamKeyProps(channel_arn=channel_arn, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7583d68a7f27d57bf564715942430cdfd6f13c2d14f803321954ffd138c60902)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c8f40f1faa2f540af32d067133c58d924fb3059cbdd4dc2bf5a005beec6a20a)
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
        '''The stream-key ARN.

        For example: ``arn:aws:ivs:us-west-2:123456789012:stream-key/g1H2I3j4k5L6``

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrValue")
    def attr_value(self) -> builtins.str:
        '''The stream-key value.

        For example: ``sk_us-west-2_abcdABCDefgh_567890abcdef``

        :cloudformationAttribute: Value
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrValue"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-streamkey.html#cfn-ivs-streamkey-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="channelArn")
    def channel_arn(self) -> builtins.str:
        '''Channel ARN for the stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-streamkey.html#cfn-ivs-streamkey-channelarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelArn"))

    @channel_arn.setter
    def channel_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ca998d3e7e709418ddfcb6c4bda1948b4c8b316a65f7680e53f33dc155ab527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "channelArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ivs.CfnStreamKeyProps",
    jsii_struct_bases=[],
    name_mapping={"channel_arn": "channelArn", "tags": "tags"},
)
class CfnStreamKeyProps:
    def __init__(
        self,
        *,
        channel_arn: builtins.str,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnStreamKey``.

        :param channel_arn: Channel ARN for the stream.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-streamkey.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ivs as ivs
            
            cfn_stream_key_props = ivs.CfnStreamKeyProps(
                channel_arn="channelArn",
            
                # the properties below are optional
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ced95982ad59cd8b99cb2e47d74a2a51830d61b47e490b479332368786aae19)
            check_type(argname="argument channel_arn", value=channel_arn, expected_type=type_hints["channel_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel_arn": channel_arn,
        }
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def channel_arn(self) -> builtins.str:
        '''Channel ARN for the stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-streamkey.html#cfn-ivs-streamkey-channelarn
        '''
        result = self._values.get("channel_arn")
        assert result is not None, "Required property 'channel_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-streamkey.html#cfn-ivs-streamkey-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamKeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ivs.ChannelProps",
    jsii_struct_bases=[],
    name_mapping={
        "authorized": "authorized",
        "latency_mode": "latencyMode",
        "name": "name",
        "type": "type",
    },
)
class ChannelProps:
    def __init__(
        self,
        *,
        authorized: typing.Optional[builtins.bool] = None,
        latency_mode: typing.Optional["LatencyMode"] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional["ChannelType"] = None,
    ) -> None:
        '''(experimental) Properties for creating a new Channel.

        :param authorized: (experimental) Whether the channel is authorized. If you wish to make an authorized channel, you will need to ensure that a PlaybackKeyPair has been uploaded to your account as this is used to validate the signed JWT that is required for authorization Default: false
        :param latency_mode: (experimental) Channel latency mode. Default: LatencyMode.LOW
        :param name: (experimental) Channel name. Default: - None
        :param type: (experimental) The channel type, which determines the allowable resolution and bitrate. If you exceed the allowable resolution or bitrate, the stream will disconnect immediately Default: ChannelType.STANDARD

        :stability: experimental
        :exampleMetadata: infused

        Example::

            my_channel = ivs.Channel(self, "Channel",
                authorized=True
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c89787c4d6b6f9bb36304a1c903fbebf73b7d92ae10f1d9b57b12466498b359)
            check_type(argname="argument authorized", value=authorized, expected_type=type_hints["authorized"])
            check_type(argname="argument latency_mode", value=latency_mode, expected_type=type_hints["latency_mode"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authorized is not None:
            self._values["authorized"] = authorized
        if latency_mode is not None:
            self._values["latency_mode"] = latency_mode
        if name is not None:
            self._values["name"] = name
        if type is not None:
            self._values["type"] = type

    @builtins.property
    def authorized(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the channel is authorized.

        If you wish to make an authorized channel, you will need to ensure that
        a PlaybackKeyPair has been uploaded to your account as this is used to
        validate the signed JWT that is required for authorization

        :default: false

        :stability: experimental
        '''
        result = self._values.get("authorized")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def latency_mode(self) -> typing.Optional["LatencyMode"]:
        '''(experimental) Channel latency mode.

        :default: LatencyMode.LOW

        :stability: experimental
        '''
        result = self._values.get("latency_mode")
        return typing.cast(typing.Optional["LatencyMode"], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Channel name.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def type(self) -> typing.Optional["ChannelType"]:
        '''(experimental) The channel type, which determines the allowable resolution and bitrate.

        If you exceed the allowable resolution or bitrate, the stream will disconnect immediately

        :default: ChannelType.STANDARD

        :stability: experimental
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional["ChannelType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="@aws-cdk/aws-ivs.ChannelType")
class ChannelType(enum.Enum):
    '''(experimental) The channel type, which determines the allowable resolution and bitrate.

    If you exceed the allowable resolution or bitrate, the stream probably will disconnect immediately.

    :stability: experimental
    '''

    STANDARD = "STANDARD"
    '''(experimental) Multiple qualities are generated from the original input, to automatically give viewers the best experience for their devices and network conditions.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html
    :stability: experimental
    '''
    BASIC = "BASIC"
    '''(experimental) delivers the original input to viewers.

    The viewer’s video-quality choice is limited to the original input.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ivs-channel.html
    :stability: experimental
    '''


@jsii.interface(jsii_type="@aws-cdk/aws-ivs.IChannel")
class IChannel(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an IVS Channel.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="channelArn")
    def channel_arn(self) -> builtins.str:
        '''(experimental) The channel ARN.

        For example: arn:aws:ivs:us-west-2:123456789012:channel/abcdABCDefgh

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addStreamKey")
    def add_stream_key(self, id: builtins.str) -> "StreamKey":
        '''(experimental) Adds a stream key for this IVS Channel.

        :param id: construct ID.

        :stability: experimental
        '''
        ...


class _IChannelProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an IVS Channel.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ivs.IChannel"

    @builtins.property
    @jsii.member(jsii_name="channelArn")
    def channel_arn(self) -> builtins.str:
        '''(experimental) The channel ARN.

        For example: arn:aws:ivs:us-west-2:123456789012:channel/abcdABCDefgh

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelArn"))

    @jsii.member(jsii_name="addStreamKey")
    def add_stream_key(self, id: builtins.str) -> "StreamKey":
        '''(experimental) Adds a stream key for this IVS Channel.

        :param id: construct ID.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4038ed39c94ed1d46f4bfb34bcf5a73cbad95967b5d6b1ebf87bfda4e4dfbe44)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("StreamKey", jsii.invoke(self, "addStreamKey", [id]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IChannel).__jsii_proxy_class__ = lambda : _IChannelProxy


@jsii.interface(jsii_type="@aws-cdk/aws-ivs.IPlaybackKeyPair")
class IPlaybackKeyPair(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an IVS Playback Key Pair.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="playbackKeyPairArn")
    def playback_key_pair_arn(self) -> builtins.str:
        '''(experimental) Key-pair ARN.

        For example: arn:aws:ivs:us-west-2:693991300569:playback-key/f99cde61-c2b0-4df3-8941-ca7d38acca1a

        :stability: experimental
        :attribute: true
        '''
        ...


class _IPlaybackKeyPairProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an IVS Playback Key Pair.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ivs.IPlaybackKeyPair"

    @builtins.property
    @jsii.member(jsii_name="playbackKeyPairArn")
    def playback_key_pair_arn(self) -> builtins.str:
        '''(experimental) Key-pair ARN.

        For example: arn:aws:ivs:us-west-2:693991300569:playback-key/f99cde61-c2b0-4df3-8941-ca7d38acca1a

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "playbackKeyPairArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPlaybackKeyPair).__jsii_proxy_class__ = lambda : _IPlaybackKeyPairProxy


@jsii.interface(jsii_type="@aws-cdk/aws-ivs.IStreamKey")
class IStreamKey(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
    '''(experimental) Represents an IVS Stream Key.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="streamKeyArn")
    def stream_key_arn(self) -> builtins.str:
        '''(experimental) The stream-key ARN.

        For example: arn:aws:ivs:us-west-2:123456789012:stream-key/g1H2I3j4k5L6

        :stability: experimental
        :attribute: true
        '''
        ...


class _IStreamKeyProxy(
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''(experimental) Represents an IVS Stream Key.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-ivs.IStreamKey"

    @builtins.property
    @jsii.member(jsii_name="streamKeyArn")
    def stream_key_arn(self) -> builtins.str:
        '''(experimental) The stream-key ARN.

        For example: arn:aws:ivs:us-west-2:123456789012:stream-key/g1H2I3j4k5L6

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "streamKeyArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStreamKey).__jsii_proxy_class__ = lambda : _IStreamKeyProxy


@jsii.enum(jsii_type="@aws-cdk/aws-ivs.LatencyMode")
class LatencyMode(enum.Enum):
    '''(experimental) Channel latency mode.

    :stability: experimental
    '''

    LOW = "LOW"
    '''(experimental) Use LOW to minimize broadcaster-to-viewer latency for interactive broadcasts.

    :stability: experimental
    '''
    NORMAL = "NORMAL"
    '''(experimental) Use NORMAL for broadcasts that do not require viewer interaction.

    :stability: experimental
    '''


@jsii.implements(IPlaybackKeyPair)
class PlaybackKeyPair(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ivs.PlaybackKeyPair",
):
    '''(experimental) A new IVS Playback Key Pair.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        key_pair = ivs.PlaybackKeyPair(self, "PlaybackKeyPair",
            public_key_material=my_public_key_pem_string
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        public_key_material: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param public_key_material: (experimental) The public portion of a customer-generated key pair.
        :param name: (experimental) An arbitrary string (a nickname) assigned to a playback key pair that helps the customer identify that resource. The value does not need to be unique. Default: None

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__906e9b922558a67adf00b2d711d4d97b3dcf3d50cc3f073ba256f2275441a2d2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PlaybackKeyPairProps(
            public_key_material=public_key_material, name=name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="playbackKeyPairArn")
    def playback_key_pair_arn(self) -> builtins.str:
        '''(experimental) Key-pair ARN.

        For example: arn:aws:ivs:us-west-2:693991300569:playback-key/f99cde61-c2b0-4df3-8941-ca7d38acca1a

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "playbackKeyPairArn"))

    @builtins.property
    @jsii.member(jsii_name="playbackKeyPairFingerprint")
    def playback_key_pair_fingerprint(self) -> builtins.str:
        '''(experimental) Key-pair identifier.

        For example: 98:0d:1a:a0:19:96:1e:ea:0a:0a:2c:9a:42:19:2b:e7

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "playbackKeyPairFingerprint"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ivs.PlaybackKeyPairProps",
    jsii_struct_bases=[],
    name_mapping={"public_key_material": "publicKeyMaterial", "name": "name"},
)
class PlaybackKeyPairProps:
    def __init__(
        self,
        *,
        public_key_material: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for creating a new Playback Key Pair.

        :param public_key_material: (experimental) The public portion of a customer-generated key pair.
        :param name: (experimental) An arbitrary string (a nickname) assigned to a playback key pair that helps the customer identify that resource. The value does not need to be unique. Default: None

        :stability: experimental
        :exampleMetadata: infused

        Example::

            key_pair = ivs.PlaybackKeyPair(self, "PlaybackKeyPair",
                public_key_material=my_public_key_pem_string
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be780fa10a22c5d0662504b918e5eb1f955ed354355040c706472a310d04c72e)
            check_type(argname="argument public_key_material", value=public_key_material, expected_type=type_hints["public_key_material"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "public_key_material": public_key_material,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def public_key_material(self) -> builtins.str:
        '''(experimental) The public portion of a customer-generated key pair.

        :stability: experimental
        '''
        result = self._values.get("public_key_material")
        assert result is not None, "Required property 'public_key_material' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) An arbitrary string (a nickname) assigned to a playback key pair that helps the customer identify that resource.

        The value does not need to be unique.

        :default: None

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PlaybackKeyPairProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IStreamKey)
class StreamKey(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ivs.StreamKey",
):
    '''(experimental) A new IVS Stream Key.

    :stability: experimental
    :exampleMetadata: fixture=with-channel infused

    Example::

        my_stream_key = my_channel.add_stream_key("StreamKey")
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        channel: IChannel,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param channel: (experimental) Channel ARN for the stream.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd69b58b5bab5b94388a35dc111efeca55ed2bb5b9c14fc3a229269cbca4e13e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = StreamKeyProps(channel=channel)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="streamKeyArn")
    def stream_key_arn(self) -> builtins.str:
        '''(experimental) The stream-key ARN.

        For example: arn:aws:ivs:us-west-2:123456789012:stream-key/g1H2I3j4k5L6

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "streamKeyArn"))

    @builtins.property
    @jsii.member(jsii_name="streamKeyValue")
    def stream_key_value(self) -> builtins.str:
        '''(experimental) The stream-key value.

        For example: sk_us-west-2_abcdABCDefgh_567890abcdef

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "streamKeyValue"))


@jsii.data_type(
    jsii_type="@aws-cdk/aws-ivs.StreamKeyProps",
    jsii_struct_bases=[],
    name_mapping={"channel": "channel"},
)
class StreamKeyProps:
    def __init__(self, *, channel: IChannel) -> None:
        '''(experimental) Properties for creating a new Stream Key.

        :param channel: (experimental) Channel ARN for the stream.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_ivs as ivs
            
            # channel: ivs.Channel
            
            stream_key_props = ivs.StreamKeyProps(
                channel=channel
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1349fe9c3535837b914c8f196bd55ebe4074ca884d27fdce60ceb7c34e1d7963)
            check_type(argname="argument channel", value=channel, expected_type=type_hints["channel"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "channel": channel,
        }

    @builtins.property
    def channel(self) -> IChannel:
        '''(experimental) Channel ARN for the stream.

        :stability: experimental
        '''
        result = self._values.get("channel")
        assert result is not None, "Required property 'channel' is missing"
        return typing.cast(IChannel, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StreamKeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IChannel)
class Channel(
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-ivs.Channel",
):
    '''(experimental) A new IVS channel.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        my_channel = ivs.Channel(self, "Channel")
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        authorized: typing.Optional[builtins.bool] = None,
        latency_mode: typing.Optional[LatencyMode] = None,
        name: typing.Optional[builtins.str] = None,
        type: typing.Optional[ChannelType] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param authorized: (experimental) Whether the channel is authorized. If you wish to make an authorized channel, you will need to ensure that a PlaybackKeyPair has been uploaded to your account as this is used to validate the signed JWT that is required for authorization Default: false
        :param latency_mode: (experimental) Channel latency mode. Default: LatencyMode.LOW
        :param name: (experimental) Channel name. Default: - None
        :param type: (experimental) The channel type, which determines the allowable resolution and bitrate. If you exceed the allowable resolution or bitrate, the stream will disconnect immediately Default: ChannelType.STANDARD

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f71cbfc4c7d0608cb01d35fa79b40a1ea574eb371f8a52fcbe23654ae4eb2e9a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ChannelProps(
            authorized=authorized, latency_mode=latency_mode, name=name, type=type
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromChannelArn")
    @builtins.classmethod
    def from_channel_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        channel_arn: builtins.str,
    ) -> IChannel:
        '''(experimental) Import an existing channel.

        :param scope: -
        :param id: -
        :param channel_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c48aad0af5e331ae66fb168ee4f0cf0372456dab11b030ed0cab0d53c1e768e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument channel_arn", value=channel_arn, expected_type=type_hints["channel_arn"])
        return typing.cast(IChannel, jsii.sinvoke(cls, "fromChannelArn", [scope, id, channel_arn]))

    @jsii.member(jsii_name="addStreamKey")
    def add_stream_key(self, id: builtins.str) -> StreamKey:
        '''(experimental) Adds a stream key for this IVS Channel.

        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c30f344cb886ff2762caa8e2d32e7fc967c5d3035e47f88f876a4840d715611)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast(StreamKey, jsii.invoke(self, "addStreamKey", [id]))

    @builtins.property
    @jsii.member(jsii_name="channelArn")
    def channel_arn(self) -> builtins.str:
        '''(experimental) The channel ARN.

        For example: arn:aws:ivs:us-west-2:123456789012:channel/abcdABCDefgh

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelArn"))

    @builtins.property
    @jsii.member(jsii_name="channelIngestEndpoint")
    def channel_ingest_endpoint(self) -> builtins.str:
        '''(experimental) Channel ingest endpoint, part of the definition of an ingest server, used when you set up streaming software.

        For example: a1b2c3d4e5f6.global-contribute.live-video.net

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelIngestEndpoint"))

    @builtins.property
    @jsii.member(jsii_name="channelPlaybackUrl")
    def channel_playback_url(self) -> builtins.str:
        '''(experimental) Channel playback URL.

        For example:
        https://a1b2c3d4e5f6.us-west-2.playback.live-video.net/api/video/v1/us-west-2.123456789012.channel.abcdEFGH.m3u8

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "channelPlaybackUrl"))


__all__ = [
    "CfnChannel",
    "CfnChannelProps",
    "CfnPlaybackKeyPair",
    "CfnPlaybackKeyPairProps",
    "CfnRecordingConfiguration",
    "CfnRecordingConfigurationProps",
    "CfnStreamKey",
    "CfnStreamKeyProps",
    "Channel",
    "ChannelProps",
    "ChannelType",
    "IChannel",
    "IPlaybackKeyPair",
    "IStreamKey",
    "LatencyMode",
    "PlaybackKeyPair",
    "PlaybackKeyPairProps",
    "StreamKey",
    "StreamKeyProps",
]

publication.publish()

def _typecheckingstub__49be12fe1f38ed9c33dec23ad664f18867cf2a35360912c221c659e48cac4695(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    authorized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    latency_mode: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    recording_configuration_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e602c9fe026a76c66a38e53e3eb7ab3e3e6bf0be5acc9c8aa9c053dad5f1205(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cee82e9e7ec5f66518c5edbdb7234356cd7660053374c96a41c918f080beb3e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a177793aff6b53af7dcd951960186bfe1fc0cf2f812ffb1312e57bc84b69c4d(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bee2e2db8299c6a00a147093ebaa19782be6f39ec78b0769f097965ba08574dc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__caf2096317c6f1414c874e1a6f4689c4809861c1baf399830ffd93975ce58988(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0142d4dd6139b4c80e170cd41a4a79596cfb983c53b8c63db1a5d672c9ccd67(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2fe6ae1b755c4ffd1aa78afb50a45dbb6c916430aa7a932a476548f084ed321(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b6b94e41ea63a88d5416b041469e00329fcfcc9f82be5b420ee03a04449e08e(
    *,
    authorized: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    latency_mode: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    recording_configuration_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6243183d4c8423c420991a7b133706df1f5b6c311c1cb4978e82282054e3f24c(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: typing.Optional[builtins.str] = None,
    public_key_material: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44eb4da6d50b28f1244ccbe4763d17283dcdda097880d1bc19b2af4ce82022ef(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa1d101c639b7fdea78f89aa8f85b67dad33f03cbc27669c091a7432f07b88fe(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52f39a5ebcadebf9f1261f1ad384acc6bad76ea39182302282fbca92a11d42d5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3ad3e8fc80edf0ee6bf99554700d864ae2fe3d20bfc992ec743041e6abadf2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d007241b49fcc0c7cdc24afceaa4b235cf27e76205563c474814c174764d824c(
    *,
    name: typing.Optional[builtins.str] = None,
    public_key_material: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc1f7f59bfe6ef830c02e1cef7e92524dd4a813d3844f26bb97ff71bfbc9f7a8(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    destination_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRecordingConfiguration.DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    name: typing.Optional[builtins.str] = None,
    recording_reconnect_window_seconds: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    thumbnail_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRecordingConfiguration.ThumbnailConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__394123dc466235c21b1da90745c9013426a71b63a0b9dd27484661ee0fc91d8a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c01b11456c9fb31e9821d387889aaf9f258c723b9fd7d87e2a072291348f1859(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76c12dd2e6bca954b077dff37b7d9a3bbf88a8d7e4e2dcf8f143a05966e80c1f(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRecordingConfiguration.DestinationConfigurationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91d029abb26d6f06c95a113dc08bbd3b1797a54b0318f3a15181db4977740bdc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0984a0f267178eb11c47eca7d03f1cba997ccc7b6e06df0033ec619a237acb1c(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15b7162f28ce9297a0822e1b2ed3e3f5287defe20621a5a98078e0cfc11df6e7(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRecordingConfiguration.ThumbnailConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a1c9fba07b1fceb2b4443463af1e444883ac000a67f4951327ad088cfa5d4b3(
    *,
    s3: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRecordingConfiguration.S3DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10f790191169448cf1196c16f2f4dd15330b1a6d5ed3dc23ff096a5ad90a6529(
    *,
    bucket_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1516e49c9f8d6ae8778e6654cac7a77d28d2a77cecc6c97e1e348336ccd7c5b(
    *,
    recording_mode: builtins.str,
    target_interval_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7e54bda807c048eb2ba5f6be1eaaeae0e66d5b936b1e960f6e716ea8932d292(
    *,
    destination_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRecordingConfiguration.DestinationConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    name: typing.Optional[builtins.str] = None,
    recording_reconnect_window_seconds: typing.Optional[jsii.Number] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    thumbnail_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRecordingConfiguration.ThumbnailConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad4745815acea57eff3ecd2f7cb2ba4a8613ce7519c2165fd1f60b0ead28b89a(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    channel_arn: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7583d68a7f27d57bf564715942430cdfd6f13c2d14f803321954ffd138c60902(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c8f40f1faa2f540af32d067133c58d924fb3059cbdd4dc2bf5a005beec6a20a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca998d3e7e709418ddfcb6c4bda1948b4c8b316a65f7680e53f33dc155ab527(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ced95982ad59cd8b99cb2e47d74a2a51830d61b47e490b479332368786aae19(
    *,
    channel_arn: builtins.str,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c89787c4d6b6f9bb36304a1c903fbebf73b7d92ae10f1d9b57b12466498b359(
    *,
    authorized: typing.Optional[builtins.bool] = None,
    latency_mode: typing.Optional[LatencyMode] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[ChannelType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4038ed39c94ed1d46f4bfb34bcf5a73cbad95967b5d6b1ebf87bfda4e4dfbe44(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__906e9b922558a67adf00b2d711d4d97b3dcf3d50cc3f073ba256f2275441a2d2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    public_key_material: builtins.str,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be780fa10a22c5d0662504b918e5eb1f955ed354355040c706472a310d04c72e(
    *,
    public_key_material: builtins.str,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd69b58b5bab5b94388a35dc111efeca55ed2bb5b9c14fc3a229269cbca4e13e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    channel: IChannel,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1349fe9c3535837b914c8f196bd55ebe4074ca884d27fdce60ceb7c34e1d7963(
    *,
    channel: IChannel,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f71cbfc4c7d0608cb01d35fa79b40a1ea574eb371f8a52fcbe23654ae4eb2e9a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    authorized: typing.Optional[builtins.bool] = None,
    latency_mode: typing.Optional[LatencyMode] = None,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[ChannelType] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c48aad0af5e331ae66fb168ee4f0cf0372456dab11b030ed0cab0d53c1e768e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    channel_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c30f344cb886ff2762caa8e2d32e7fc967c5d3035e47f88f876a4840d715611(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
