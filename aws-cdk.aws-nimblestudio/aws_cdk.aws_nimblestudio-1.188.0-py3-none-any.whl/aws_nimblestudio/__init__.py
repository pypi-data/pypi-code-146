'''
# AWS::NimbleStudio Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_nimblestudio as nimblestudio
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for NimbleStudio construct libraries](https://constructs.dev/search?q=nimblestudio)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::NimbleStudio resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_NimbleStudio.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::NimbleStudio](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_NimbleStudio.html).

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
class CfnLaunchProfile(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-nimblestudio.CfnLaunchProfile",
):
    '''A CloudFormation ``AWS::NimbleStudio::LaunchProfile``.

    The ``AWS::NimbleStudio::LaunchProfile`` resource represents access permissions for a set of studio components, including types of workstations, render farms, and shared file systems. Launch profiles are shared with studio users to give them access to the set of studio components.

    :cloudformationResource: AWS::NimbleStudio::LaunchProfile
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_nimblestudio as nimblestudio
        
        cfn_launch_profile = nimblestudio.CfnLaunchProfile(self, "MyCfnLaunchProfile",
            ec2_subnet_ids=["ec2SubnetIds"],
            launch_profile_protocol_versions=["launchProfileProtocolVersions"],
            name="name",
            stream_configuration=nimblestudio.CfnLaunchProfile.StreamConfigurationProperty(
                clipboard_mode="clipboardMode",
                ec2_instance_types=["ec2InstanceTypes"],
                streaming_image_ids=["streamingImageIds"],
        
                # the properties below are optional
                automatic_termination_mode="automaticTerminationMode",
                max_session_length_in_minutes=123,
                max_stopped_session_length_in_minutes=123,
                session_persistence_mode="sessionPersistenceMode",
                session_storage=nimblestudio.CfnLaunchProfile.StreamConfigurationSessionStorageProperty(
                    mode=["mode"],
        
                    # the properties below are optional
                    root=nimblestudio.CfnLaunchProfile.StreamingSessionStorageRootProperty(
                        linux="linux",
                        windows="windows"
                    )
                ),
                volume_configuration=nimblestudio.CfnLaunchProfile.VolumeConfigurationProperty(
                    iops=123,
                    size=123,
                    throughput=123
                )
            ),
            studio_component_ids=["studioComponentIds"],
            studio_id="studioId",
        
            # the properties below are optional
            description="description",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        ec2_subnet_ids: typing.Sequence[builtins.str],
        launch_profile_protocol_versions: typing.Sequence[builtins.str],
        name: builtins.str,
        stream_configuration: typing.Union[typing.Union["CfnLaunchProfile.StreamConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        studio_component_ids: typing.Sequence[builtins.str],
        studio_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::NimbleStudio::LaunchProfile``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param ec2_subnet_ids: Unique identifiers for a collection of EC2 subnets.
        :param launch_profile_protocol_versions: The version number of the protocol that is used by the launch profile. The only valid version is "2021-03-31".
        :param name: A friendly name for the launch profile.
        :param stream_configuration: A configuration for a streaming session.
        :param studio_component_ids: Unique identifiers for a collection of studio components that can be used with this launch profile.
        :param studio_id: The unique identifier for a studio resource. In Nimble Studio , all other resources are contained in a studio resource.
        :param description: A human-readable description of the launch profile.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d706b82a7a91577cd4b6a4dc0f563d3830fc7adf7ae6306064928adfbd60c93)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLaunchProfileProps(
            ec2_subnet_ids=ec2_subnet_ids,
            launch_profile_protocol_versions=launch_profile_protocol_versions,
            name=name,
            stream_configuration=stream_configuration,
            studio_component_ids=studio_component_ids,
            studio_id=studio_id,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b281c4576432fdf56a0cdb4e7eccb10886b20a2e9771a11b0fe20a20a9db994f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad1d5b2d8f88a48733ff3916d4b74abd89513f8916d26ce04e84cbf00d92e404)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrLaunchProfileId")
    def attr_launch_profile_id(self) -> builtins.str:
        '''The unique identifier for the launch profile resource.

        :cloudformationAttribute: LaunchProfileId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLaunchProfileId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="ec2SubnetIds")
    def ec2_subnet_ids(self) -> typing.List[builtins.str]:
        '''Unique identifiers for a collection of EC2 subnets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-ec2subnetids
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ec2SubnetIds"))

    @ec2_subnet_ids.setter
    def ec2_subnet_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__989ae23e71b803c8e5d7f1d02a1c5be61b93f14d8687f593ff04dc8a0885c625)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2SubnetIds", value)

    @builtins.property
    @jsii.member(jsii_name="launchProfileProtocolVersions")
    def launch_profile_protocol_versions(self) -> typing.List[builtins.str]:
        '''The version number of the protocol that is used by the launch profile.

        The only valid version is "2021-03-31".

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-launchprofileprotocolversions
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "launchProfileProtocolVersions"))

    @launch_profile_protocol_versions.setter
    def launch_profile_protocol_versions(
        self,
        value: typing.List[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea7d9297fe6bb2ece9c002f35ee642260336e5b3634e8bffa8d77ea966ce0ec0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "launchProfileProtocolVersions", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A friendly name for the launch profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a4bf5eea26dff69b3b5b3431a5052fee9b7660bd369cbd520f1091f5ac03950)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="streamConfiguration")
    def stream_configuration(
        self,
    ) -> typing.Union["CfnLaunchProfile.StreamConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''A configuration for a streaming session.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-streamconfiguration
        '''
        return typing.cast(typing.Union["CfnLaunchProfile.StreamConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "streamConfiguration"))

    @stream_configuration.setter
    def stream_configuration(
        self,
        value: typing.Union["CfnLaunchProfile.StreamConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab59aca4b1f94ee78095a524dbd42e154a5a2df26c71551e163f7bd3c53764a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "streamConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="studioComponentIds")
    def studio_component_ids(self) -> typing.List[builtins.str]:
        '''Unique identifiers for a collection of studio components that can be used with this launch profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-studiocomponentids
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "studioComponentIds"))

    @studio_component_ids.setter
    def studio_component_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__046493ed4963566972420336ab11b4dc00df1adc22ac47774c2870a2b11f80c9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "studioComponentIds", value)

    @builtins.property
    @jsii.member(jsii_name="studioId")
    def studio_id(self) -> builtins.str:
        '''The unique identifier for a studio resource.

        In Nimble Studio , all other resources are contained in a studio resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-studioid
        '''
        return typing.cast(builtins.str, jsii.get(self, "studioId"))

    @studio_id.setter
    def studio_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a43ec03580b10205db0e2ff7c8d4d728d37cc06c9bcc54f697700699480acfc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "studioId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the launch profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f54330e3fad8cf4f1aa82b625a6a8f032f2acae66d60c2981ab40618170b52d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-nimblestudio.CfnLaunchProfile.StreamConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "clipboard_mode": "clipboardMode",
            "ec2_instance_types": "ec2InstanceTypes",
            "streaming_image_ids": "streamingImageIds",
            "automatic_termination_mode": "automaticTerminationMode",
            "max_session_length_in_minutes": "maxSessionLengthInMinutes",
            "max_stopped_session_length_in_minutes": "maxStoppedSessionLengthInMinutes",
            "session_persistence_mode": "sessionPersistenceMode",
            "session_storage": "sessionStorage",
            "volume_configuration": "volumeConfiguration",
        },
    )
    class StreamConfigurationProperty:
        def __init__(
            self,
            *,
            clipboard_mode: builtins.str,
            ec2_instance_types: typing.Sequence[builtins.str],
            streaming_image_ids: typing.Sequence[builtins.str],
            automatic_termination_mode: typing.Optional[builtins.str] = None,
            max_session_length_in_minutes: typing.Optional[jsii.Number] = None,
            max_stopped_session_length_in_minutes: typing.Optional[jsii.Number] = None,
            session_persistence_mode: typing.Optional[builtins.str] = None,
            session_storage: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLaunchProfile.StreamConfigurationSessionStorageProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            volume_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLaunchProfile.VolumeConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A configuration for a streaming session.

            :param clipboard_mode: Allows or deactivates the use of the system clipboard to copy and paste between the streaming session and streaming client.
            :param ec2_instance_types: The EC2 instance types that users can select from when launching a streaming session with this launch profile.
            :param streaming_image_ids: The streaming images that users can select from when launching a streaming session with this launch profile.
            :param automatic_termination_mode: Indicates if a streaming session created from this launch profile should be terminated automatically or retained without termination after being in a ``STOPPED`` state. - When ``ACTIVATED`` , the streaming session is scheduled for termination after being in the ``STOPPED`` state for the time specified in ``maxStoppedSessionLengthInMinutes`` . - When ``DEACTIVATED`` , the streaming session can remain in the ``STOPPED`` state indefinitely. This parameter is only allowed when ``sessionPersistenceMode`` is ``ACTIVATED`` . When allowed, the default value for this parameter is ``DEACTIVATED`` .
            :param max_session_length_in_minutes: The length of time, in minutes, that a streaming session can be active before it is stopped or terminated. After this point, Nimble Studio automatically terminates or stops the session. The default length of time is 690 minutes, and the maximum length of time is 30 days.
            :param max_stopped_session_length_in_minutes: Integer that determines if you can start and stop your sessions and how long a session can stay in the ``STOPPED`` state. The default value is 0. The maximum value is 5760. This field is allowed only when ``sessionPersistenceMode`` is ``ACTIVATED`` and ``automaticTerminationMode`` is ``ACTIVATED`` . If the value is set to 0, your sessions can’t be ``STOPPED`` . If you then call ``StopStreamingSession`` , the session fails. If the time that a session stays in the ``READY`` state exceeds the ``maxSessionLengthInMinutes`` value, the session will automatically be terminated (instead of ``STOPPED`` ). If the value is set to a positive number, the session can be stopped. You can call ``StopStreamingSession`` to stop sessions in the ``READY`` state. If the time that a session stays in the ``READY`` state exceeds the ``maxSessionLengthInMinutes`` value, the session will automatically be stopped (instead of terminated).
            :param session_persistence_mode: Determine if a streaming session created from this launch profile can configure persistent storage. This means that ``volumeConfiguration`` and ``automaticTerminationMode`` are configured.
            :param session_storage: The upload storage for a streaming session.
            :param volume_configuration: Custom volume configuration for the root volumes that are attached to streaming sessions. This parameter is only allowed when ``sessionPersistenceMode`` is ``ACTIVATED`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_nimblestudio as nimblestudio
                
                stream_configuration_property = nimblestudio.CfnLaunchProfile.StreamConfigurationProperty(
                    clipboard_mode="clipboardMode",
                    ec2_instance_types=["ec2InstanceTypes"],
                    streaming_image_ids=["streamingImageIds"],
                
                    # the properties below are optional
                    automatic_termination_mode="automaticTerminationMode",
                    max_session_length_in_minutes=123,
                    max_stopped_session_length_in_minutes=123,
                    session_persistence_mode="sessionPersistenceMode",
                    session_storage=nimblestudio.CfnLaunchProfile.StreamConfigurationSessionStorageProperty(
                        mode=["mode"],
                
                        # the properties below are optional
                        root=nimblestudio.CfnLaunchProfile.StreamingSessionStorageRootProperty(
                            linux="linux",
                            windows="windows"
                        )
                    ),
                    volume_configuration=nimblestudio.CfnLaunchProfile.VolumeConfigurationProperty(
                        iops=123,
                        size=123,
                        throughput=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c27e0247a6b4dedb1fd0283836ff19245e67a73abdfdacecd630ef2fd4f978fa)
                check_type(argname="argument clipboard_mode", value=clipboard_mode, expected_type=type_hints["clipboard_mode"])
                check_type(argname="argument ec2_instance_types", value=ec2_instance_types, expected_type=type_hints["ec2_instance_types"])
                check_type(argname="argument streaming_image_ids", value=streaming_image_ids, expected_type=type_hints["streaming_image_ids"])
                check_type(argname="argument automatic_termination_mode", value=automatic_termination_mode, expected_type=type_hints["automatic_termination_mode"])
                check_type(argname="argument max_session_length_in_minutes", value=max_session_length_in_minutes, expected_type=type_hints["max_session_length_in_minutes"])
                check_type(argname="argument max_stopped_session_length_in_minutes", value=max_stopped_session_length_in_minutes, expected_type=type_hints["max_stopped_session_length_in_minutes"])
                check_type(argname="argument session_persistence_mode", value=session_persistence_mode, expected_type=type_hints["session_persistence_mode"])
                check_type(argname="argument session_storage", value=session_storage, expected_type=type_hints["session_storage"])
                check_type(argname="argument volume_configuration", value=volume_configuration, expected_type=type_hints["volume_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "clipboard_mode": clipboard_mode,
                "ec2_instance_types": ec2_instance_types,
                "streaming_image_ids": streaming_image_ids,
            }
            if automatic_termination_mode is not None:
                self._values["automatic_termination_mode"] = automatic_termination_mode
            if max_session_length_in_minutes is not None:
                self._values["max_session_length_in_minutes"] = max_session_length_in_minutes
            if max_stopped_session_length_in_minutes is not None:
                self._values["max_stopped_session_length_in_minutes"] = max_stopped_session_length_in_minutes
            if session_persistence_mode is not None:
                self._values["session_persistence_mode"] = session_persistence_mode
            if session_storage is not None:
                self._values["session_storage"] = session_storage
            if volume_configuration is not None:
                self._values["volume_configuration"] = volume_configuration

        @builtins.property
        def clipboard_mode(self) -> builtins.str:
            '''Allows or deactivates the use of the system clipboard to copy and paste between the streaming session and streaming client.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-clipboardmode
            '''
            result = self._values.get("clipboard_mode")
            assert result is not None, "Required property 'clipboard_mode' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def ec2_instance_types(self) -> typing.List[builtins.str]:
            '''The EC2 instance types that users can select from when launching a streaming session with this launch profile.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-ec2instancetypes
            '''
            result = self._values.get("ec2_instance_types")
            assert result is not None, "Required property 'ec2_instance_types' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def streaming_image_ids(self) -> typing.List[builtins.str]:
            '''The streaming images that users can select from when launching a streaming session with this launch profile.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-streamingimageids
            '''
            result = self._values.get("streaming_image_ids")
            assert result is not None, "Required property 'streaming_image_ids' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def automatic_termination_mode(self) -> typing.Optional[builtins.str]:
            '''Indicates if a streaming session created from this launch profile should be terminated automatically or retained without termination after being in a ``STOPPED`` state.

            - When ``ACTIVATED`` , the streaming session is scheduled for termination after being in the ``STOPPED`` state for the time specified in ``maxStoppedSessionLengthInMinutes`` .
            - When ``DEACTIVATED`` , the streaming session can remain in the ``STOPPED`` state indefinitely.

            This parameter is only allowed when ``sessionPersistenceMode`` is ``ACTIVATED`` . When allowed, the default value for this parameter is ``DEACTIVATED`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-automaticterminationmode
            '''
            result = self._values.get("automatic_termination_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def max_session_length_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''The length of time, in minutes, that a streaming session can be active before it is stopped or terminated.

            After this point, Nimble Studio automatically terminates or stops the session. The default length of time is 690 minutes, and the maximum length of time is 30 days.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-maxsessionlengthinminutes
            '''
            result = self._values.get("max_session_length_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_stopped_session_length_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''Integer that determines if you can start and stop your sessions and how long a session can stay in the ``STOPPED`` state.

            The default value is 0. The maximum value is 5760.

            This field is allowed only when ``sessionPersistenceMode`` is ``ACTIVATED`` and ``automaticTerminationMode`` is ``ACTIVATED`` .

            If the value is set to 0, your sessions can’t be ``STOPPED`` . If you then call ``StopStreamingSession`` , the session fails. If the time that a session stays in the ``READY`` state exceeds the ``maxSessionLengthInMinutes`` value, the session will automatically be terminated (instead of ``STOPPED`` ).

            If the value is set to a positive number, the session can be stopped. You can call ``StopStreamingSession`` to stop sessions in the ``READY`` state. If the time that a session stays in the ``READY`` state exceeds the ``maxSessionLengthInMinutes`` value, the session will automatically be stopped (instead of terminated).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-maxstoppedsessionlengthinminutes
            '''
            result = self._values.get("max_stopped_session_length_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def session_persistence_mode(self) -> typing.Optional[builtins.str]:
            '''Determine if a streaming session created from this launch profile can configure persistent storage.

            This means that ``volumeConfiguration`` and ``automaticTerminationMode`` are configured.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-sessionpersistencemode
            '''
            result = self._values.get("session_persistence_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def session_storage(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLaunchProfile.StreamConfigurationSessionStorageProperty"]]:
            '''The upload storage for a streaming session.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-sessionstorage
            '''
            result = self._values.get("session_storage")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLaunchProfile.StreamConfigurationSessionStorageProperty"]], result)

        @builtins.property
        def volume_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLaunchProfile.VolumeConfigurationProperty"]]:
            '''Custom volume configuration for the root volumes that are attached to streaming sessions.

            This parameter is only allowed when ``sessionPersistenceMode`` is ``ACTIVATED`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfiguration.html#cfn-nimblestudio-launchprofile-streamconfiguration-volumeconfiguration
            '''
            result = self._values.get("volume_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLaunchProfile.VolumeConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-nimblestudio.CfnLaunchProfile.StreamConfigurationSessionStorageProperty",
        jsii_struct_bases=[],
        name_mapping={"mode": "mode", "root": "root"},
    )
    class StreamConfigurationSessionStorageProperty:
        def __init__(
            self,
            *,
            mode: typing.Sequence[builtins.str],
            root: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLaunchProfile.StreamingSessionStorageRootProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration for a streaming session’s upload storage.

            :param mode: Allows artists to upload files to their workstations. The only valid option is ``UPLOAD`` .
            :param root: The configuration for the upload storage root of the streaming session.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfigurationsessionstorage.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_nimblestudio as nimblestudio
                
                stream_configuration_session_storage_property = nimblestudio.CfnLaunchProfile.StreamConfigurationSessionStorageProperty(
                    mode=["mode"],
                
                    # the properties below are optional
                    root=nimblestudio.CfnLaunchProfile.StreamingSessionStorageRootProperty(
                        linux="linux",
                        windows="windows"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dd44924c51f708c535c68c35760db8e4f08965b1aabe98a16a8a37acb955fba8)
                check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
                check_type(argname="argument root", value=root, expected_type=type_hints["root"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "mode": mode,
            }
            if root is not None:
                self._values["root"] = root

        @builtins.property
        def mode(self) -> typing.List[builtins.str]:
            '''Allows artists to upload files to their workstations.

            The only valid option is ``UPLOAD`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfigurationsessionstorage.html#cfn-nimblestudio-launchprofile-streamconfigurationsessionstorage-mode
            '''
            result = self._values.get("mode")
            assert result is not None, "Required property 'mode' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def root(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLaunchProfile.StreamingSessionStorageRootProperty"]]:
            '''The configuration for the upload storage root of the streaming session.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamconfigurationsessionstorage.html#cfn-nimblestudio-launchprofile-streamconfigurationsessionstorage-root
            '''
            result = self._values.get("root")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLaunchProfile.StreamingSessionStorageRootProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamConfigurationSessionStorageProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-nimblestudio.CfnLaunchProfile.StreamingSessionStorageRootProperty",
        jsii_struct_bases=[],
        name_mapping={"linux": "linux", "windows": "windows"},
    )
    class StreamingSessionStorageRootProperty:
        def __init__(
            self,
            *,
            linux: typing.Optional[builtins.str] = None,
            windows: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The upload storage root location (folder) on streaming workstations where files are uploaded.

            :param linux: The folder path in Linux workstations where files are uploaded.
            :param windows: The folder path in Windows workstations where files are uploaded.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamingsessionstorageroot.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_nimblestudio as nimblestudio
                
                streaming_session_storage_root_property = nimblestudio.CfnLaunchProfile.StreamingSessionStorageRootProperty(
                    linux="linux",
                    windows="windows"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e80f915f75434409c047ae00ed2529f3e5014f688f5003fb98f42d7acb79554)
                check_type(argname="argument linux", value=linux, expected_type=type_hints["linux"])
                check_type(argname="argument windows", value=windows, expected_type=type_hints["windows"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if linux is not None:
                self._values["linux"] = linux
            if windows is not None:
                self._values["windows"] = windows

        @builtins.property
        def linux(self) -> typing.Optional[builtins.str]:
            '''The folder path in Linux workstations where files are uploaded.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamingsessionstorageroot.html#cfn-nimblestudio-launchprofile-streamingsessionstorageroot-linux
            '''
            result = self._values.get("linux")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def windows(self) -> typing.Optional[builtins.str]:
            '''The folder path in Windows workstations where files are uploaded.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-streamingsessionstorageroot.html#cfn-nimblestudio-launchprofile-streamingsessionstorageroot-windows
            '''
            result = self._values.get("windows")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamingSessionStorageRootProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-nimblestudio.CfnLaunchProfile.VolumeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"iops": "iops", "size": "size", "throughput": "throughput"},
    )
    class VolumeConfigurationProperty:
        def __init__(
            self,
            *,
            iops: typing.Optional[jsii.Number] = None,
            size: typing.Optional[jsii.Number] = None,
            throughput: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Custom volume configuration for the root volumes that are attached to streaming sessions.

            This parameter is only allowed when ``sessionPersistenceMode`` is ``ACTIVATED`` .

            :param iops: The number of I/O operations per second for the root volume that is attached to streaming session.
            :param size: The size of the root volume that is attached to the streaming session. The root volume size is measured in GiBs.
            :param throughput: The throughput to provision for the root volume that is attached to the streaming session. The throughput is measured in MiB/s.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-volumeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_nimblestudio as nimblestudio
                
                volume_configuration_property = nimblestudio.CfnLaunchProfile.VolumeConfigurationProperty(
                    iops=123,
                    size=123,
                    throughput=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ab1af60c683c69aa0e66077f0cfc6e4d4a01fb6a939adfa3ce827d23bdc2ee4e)
                check_type(argname="argument iops", value=iops, expected_type=type_hints["iops"])
                check_type(argname="argument size", value=size, expected_type=type_hints["size"])
                check_type(argname="argument throughput", value=throughput, expected_type=type_hints["throughput"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if iops is not None:
                self._values["iops"] = iops
            if size is not None:
                self._values["size"] = size
            if throughput is not None:
                self._values["throughput"] = throughput

        @builtins.property
        def iops(self) -> typing.Optional[jsii.Number]:
            '''The number of I/O operations per second for the root volume that is attached to streaming session.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-volumeconfiguration.html#cfn-nimblestudio-launchprofile-volumeconfiguration-iops
            '''
            result = self._values.get("iops")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def size(self) -> typing.Optional[jsii.Number]:
            '''The size of the root volume that is attached to the streaming session.

            The root volume size is measured in GiBs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-volumeconfiguration.html#cfn-nimblestudio-launchprofile-volumeconfiguration-size
            '''
            result = self._values.get("size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def throughput(self) -> typing.Optional[jsii.Number]:
            '''The throughput to provision for the root volume that is attached to the streaming session.

            The throughput is measured in MiB/s.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-launchprofile-volumeconfiguration.html#cfn-nimblestudio-launchprofile-volumeconfiguration-throughput
            '''
            result = self._values.get("throughput")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VolumeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-nimblestudio.CfnLaunchProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "ec2_subnet_ids": "ec2SubnetIds",
        "launch_profile_protocol_versions": "launchProfileProtocolVersions",
        "name": "name",
        "stream_configuration": "streamConfiguration",
        "studio_component_ids": "studioComponentIds",
        "studio_id": "studioId",
        "description": "description",
        "tags": "tags",
    },
)
class CfnLaunchProfileProps:
    def __init__(
        self,
        *,
        ec2_subnet_ids: typing.Sequence[builtins.str],
        launch_profile_protocol_versions: typing.Sequence[builtins.str],
        name: builtins.str,
        stream_configuration: typing.Union[typing.Union[CfnLaunchProfile.StreamConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
        studio_component_ids: typing.Sequence[builtins.str],
        studio_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnLaunchProfile``.

        :param ec2_subnet_ids: Unique identifiers for a collection of EC2 subnets.
        :param launch_profile_protocol_versions: The version number of the protocol that is used by the launch profile. The only valid version is "2021-03-31".
        :param name: A friendly name for the launch profile.
        :param stream_configuration: A configuration for a streaming session.
        :param studio_component_ids: Unique identifiers for a collection of studio components that can be used with this launch profile.
        :param studio_id: The unique identifier for a studio resource. In Nimble Studio , all other resources are contained in a studio resource.
        :param description: A human-readable description of the launch profile.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_nimblestudio as nimblestudio
            
            cfn_launch_profile_props = nimblestudio.CfnLaunchProfileProps(
                ec2_subnet_ids=["ec2SubnetIds"],
                launch_profile_protocol_versions=["launchProfileProtocolVersions"],
                name="name",
                stream_configuration=nimblestudio.CfnLaunchProfile.StreamConfigurationProperty(
                    clipboard_mode="clipboardMode",
                    ec2_instance_types=["ec2InstanceTypes"],
                    streaming_image_ids=["streamingImageIds"],
            
                    # the properties below are optional
                    automatic_termination_mode="automaticTerminationMode",
                    max_session_length_in_minutes=123,
                    max_stopped_session_length_in_minutes=123,
                    session_persistence_mode="sessionPersistenceMode",
                    session_storage=nimblestudio.CfnLaunchProfile.StreamConfigurationSessionStorageProperty(
                        mode=["mode"],
            
                        # the properties below are optional
                        root=nimblestudio.CfnLaunchProfile.StreamingSessionStorageRootProperty(
                            linux="linux",
                            windows="windows"
                        )
                    ),
                    volume_configuration=nimblestudio.CfnLaunchProfile.VolumeConfigurationProperty(
                        iops=123,
                        size=123,
                        throughput=123
                    )
                ),
                studio_component_ids=["studioComponentIds"],
                studio_id="studioId",
            
                # the properties below are optional
                description="description",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68420745cc9ebe00a6bd75134a3d6120500b0d96caba0aa41ddf4e042f83df6e)
            check_type(argname="argument ec2_subnet_ids", value=ec2_subnet_ids, expected_type=type_hints["ec2_subnet_ids"])
            check_type(argname="argument launch_profile_protocol_versions", value=launch_profile_protocol_versions, expected_type=type_hints["launch_profile_protocol_versions"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument stream_configuration", value=stream_configuration, expected_type=type_hints["stream_configuration"])
            check_type(argname="argument studio_component_ids", value=studio_component_ids, expected_type=type_hints["studio_component_ids"])
            check_type(argname="argument studio_id", value=studio_id, expected_type=type_hints["studio_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ec2_subnet_ids": ec2_subnet_ids,
            "launch_profile_protocol_versions": launch_profile_protocol_versions,
            "name": name,
            "stream_configuration": stream_configuration,
            "studio_component_ids": studio_component_ids,
            "studio_id": studio_id,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def ec2_subnet_ids(self) -> typing.List[builtins.str]:
        '''Unique identifiers for a collection of EC2 subnets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-ec2subnetids
        '''
        result = self._values.get("ec2_subnet_ids")
        assert result is not None, "Required property 'ec2_subnet_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def launch_profile_protocol_versions(self) -> typing.List[builtins.str]:
        '''The version number of the protocol that is used by the launch profile.

        The only valid version is "2021-03-31".

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-launchprofileprotocolversions
        '''
        result = self._values.get("launch_profile_protocol_versions")
        assert result is not None, "Required property 'launch_profile_protocol_versions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A friendly name for the launch profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stream_configuration(
        self,
    ) -> typing.Union[CfnLaunchProfile.StreamConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''A configuration for a streaming session.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-streamconfiguration
        '''
        result = self._values.get("stream_configuration")
        assert result is not None, "Required property 'stream_configuration' is missing"
        return typing.cast(typing.Union[CfnLaunchProfile.StreamConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def studio_component_ids(self) -> typing.List[builtins.str]:
        '''Unique identifiers for a collection of studio components that can be used with this launch profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-studiocomponentids
        '''
        result = self._values.get("studio_component_ids")
        assert result is not None, "Required property 'studio_component_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def studio_id(self) -> builtins.str:
        '''The unique identifier for a studio resource.

        In Nimble Studio , all other resources are contained in a studio resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-studioid
        '''
        result = self._values.get("studio_id")
        assert result is not None, "Required property 'studio_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the launch profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-launchprofile.html#cfn-nimblestudio-launchprofile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLaunchProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnStreamingImage(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-nimblestudio.CfnStreamingImage",
):
    '''A CloudFormation ``AWS::NimbleStudio::StreamingImage``.

    The ``AWS::NimbleStudio::StreamingImage`` resource creates a streaming image in a studio. A streaming image defines the operating system and software to be used in an  streaming session.

    :cloudformationResource: AWS::NimbleStudio::StreamingImage
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_nimblestudio as nimblestudio
        
        cfn_streaming_image = nimblestudio.CfnStreamingImage(self, "MyCfnStreamingImage",
            ec2_image_id="ec2ImageId",
            name="name",
            studio_id="studioId",
        
            # the properties below are optional
            description="description",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        ec2_image_id: builtins.str,
        name: builtins.str,
        studio_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::NimbleStudio::StreamingImage``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param ec2_image_id: The ID of an EC2 machine image with which to create the streaming image.
        :param name: A friendly name for a streaming image resource.
        :param studio_id: The unique identifier for a studio resource. In Nimble Studio , all other resources are contained in a studio resource.
        :param description: A human-readable description of the streaming image.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__129bcb55764199a2e00737a05265b615b8a638197429620f4d5e2a6603005221)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStreamingImageProps(
            ec2_image_id=ec2_image_id,
            name=name,
            studio_id=studio_id,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9808f7a09ec5aaa95181195b6570a04cc3aceb37fd1f27f5fe7d7c553df7778)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a173c2ea5a6add1b80e6dbf60fbdae6265204dd4f9b295f91e79979d1408e311)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrEncryptionConfigurationKeyArn")
    def attr_encryption_configuration_key_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: EncryptionConfiguration.KeyArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEncryptionConfigurationKeyArn"))

    @builtins.property
    @jsii.member(jsii_name="attrEncryptionConfigurationKeyType")
    def attr_encryption_configuration_key_type(self) -> builtins.str:
        '''
        :cloudformationAttribute: EncryptionConfiguration.KeyType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEncryptionConfigurationKeyType"))

    @builtins.property
    @jsii.member(jsii_name="attrEulaIds")
    def attr_eula_ids(self) -> typing.List[builtins.str]:
        '''The list of IDs of EULAs that must be accepted before a streaming session can be started using this streaming image.

        :cloudformationAttribute: EulaIds
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrEulaIds"))

    @builtins.property
    @jsii.member(jsii_name="attrOwner")
    def attr_owner(self) -> builtins.str:
        '''The owner of the streaming image, either the studioId that contains the streaming image or 'amazon' for images that are provided by  .

        :cloudformationAttribute: Owner
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOwner"))

    @builtins.property
    @jsii.member(jsii_name="attrPlatform")
    def attr_platform(self) -> builtins.str:
        '''The platform of the streaming image, either WINDOWS or LINUX.

        :cloudformationAttribute: Platform
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPlatform"))

    @builtins.property
    @jsii.member(jsii_name="attrStreamingImageId")
    def attr_streaming_image_id(self) -> builtins.str:
        '''The unique identifier for the streaming image resource.

        :cloudformationAttribute: StreamingImageId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStreamingImageId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html#cfn-nimblestudio-streamingimage-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="ec2ImageId")
    def ec2_image_id(self) -> builtins.str:
        '''The ID of an EC2 machine image with which to create the streaming image.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html#cfn-nimblestudio-streamingimage-ec2imageid
        '''
        return typing.cast(builtins.str, jsii.get(self, "ec2ImageId"))

    @ec2_image_id.setter
    def ec2_image_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1cfc1fb57d8ece4e26fee507bcb2e0ca87e59c0f6683c256e76c458221fb21d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2ImageId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A friendly name for a streaming image resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html#cfn-nimblestudio-streamingimage-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ede13a87b51265b8ccfba2a79ff7f225815a93b6c2f046041861314c830dcf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="studioId")
    def studio_id(self) -> builtins.str:
        '''The unique identifier for a studio resource.

        In Nimble Studio , all other resources are contained in a studio resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html#cfn-nimblestudio-streamingimage-studioid
        '''
        return typing.cast(builtins.str, jsii.get(self, "studioId"))

    @studio_id.setter
    def studio_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c45f9d0cba20af393b3ccac3e2ae65bf3b1c270dd712e34941035069c362df0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "studioId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the streaming image.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html#cfn-nimblestudio-streamingimage-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__560ad2d07af6ee660b511f5e13cdf70eb488125410d958a74110039159fa7462)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-nimblestudio.CfnStreamingImage.StreamingImageEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"key_type": "keyType", "key_arn": "keyArn"},
    )
    class StreamingImageEncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            key_type: builtins.str,
            key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies how a streaming image is encrypted.

            :param key_type: The type of KMS key that is used to encrypt studio data.
            :param key_arn: The ARN for a KMS key that is used to encrypt studio data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-streamingimage-streamingimageencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_nimblestudio as nimblestudio
                
                streaming_image_encryption_configuration_property = nimblestudio.CfnStreamingImage.StreamingImageEncryptionConfigurationProperty(
                    key_type="keyType",
                
                    # the properties below are optional
                    key_arn="keyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b2c112749720dc22b211c3ae3bc413ac276cb62bd422e239dd7605d4aebe1445)
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
                check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key_type": key_type,
            }
            if key_arn is not None:
                self._values["key_arn"] = key_arn

        @builtins.property
        def key_type(self) -> builtins.str:
            '''The type of KMS key that is used to encrypt studio data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-streamingimage-streamingimageencryptionconfiguration.html#cfn-nimblestudio-streamingimage-streamingimageencryptionconfiguration-keytype
            '''
            result = self._values.get("key_type")
            assert result is not None, "Required property 'key_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN for a KMS key that is used to encrypt studio data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-streamingimage-streamingimageencryptionconfiguration.html#cfn-nimblestudio-streamingimage-streamingimageencryptionconfiguration-keyarn
            '''
            result = self._values.get("key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StreamingImageEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-nimblestudio.CfnStreamingImageProps",
    jsii_struct_bases=[],
    name_mapping={
        "ec2_image_id": "ec2ImageId",
        "name": "name",
        "studio_id": "studioId",
        "description": "description",
        "tags": "tags",
    },
)
class CfnStreamingImageProps:
    def __init__(
        self,
        *,
        ec2_image_id: builtins.str,
        name: builtins.str,
        studio_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnStreamingImage``.

        :param ec2_image_id: The ID of an EC2 machine image with which to create the streaming image.
        :param name: A friendly name for a streaming image resource.
        :param studio_id: The unique identifier for a studio resource. In Nimble Studio , all other resources are contained in a studio resource.
        :param description: A human-readable description of the streaming image.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_nimblestudio as nimblestudio
            
            cfn_streaming_image_props = nimblestudio.CfnStreamingImageProps(
                ec2_image_id="ec2ImageId",
                name="name",
                studio_id="studioId",
            
                # the properties below are optional
                description="description",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a45b9f4ccb3fed6e2352a60c283856d49fe5939f7d668c114362718721b2c762)
            check_type(argname="argument ec2_image_id", value=ec2_image_id, expected_type=type_hints["ec2_image_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument studio_id", value=studio_id, expected_type=type_hints["studio_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ec2_image_id": ec2_image_id,
            "name": name,
            "studio_id": studio_id,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def ec2_image_id(self) -> builtins.str:
        '''The ID of an EC2 machine image with which to create the streaming image.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html#cfn-nimblestudio-streamingimage-ec2imageid
        '''
        result = self._values.get("ec2_image_id")
        assert result is not None, "Required property 'ec2_image_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A friendly name for a streaming image resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html#cfn-nimblestudio-streamingimage-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def studio_id(self) -> builtins.str:
        '''The unique identifier for a studio resource.

        In Nimble Studio , all other resources are contained in a studio resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html#cfn-nimblestudio-streamingimage-studioid
        '''
        result = self._values.get("studio_id")
        assert result is not None, "Required property 'studio_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description of the streaming image.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html#cfn-nimblestudio-streamingimage-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-streamingimage.html#cfn-nimblestudio-streamingimage-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStreamingImageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnStudio(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-nimblestudio.CfnStudio",
):
    '''A CloudFormation ``AWS::NimbleStudio::Studio``.

    The ``AWS::NimbleStudio::Studio`` resource creates a new studio resource. In  , all other resources are contained in a studio.

    When creating a studio, two IAM roles must be provided: the admin role and the user role. These roles are assumed by your users when they log in to the  portal. The user role must have the AmazonNimbleStudio-StudioUser managed policy attached for the portal to function properly. The Admin Role must have the AmazonNimbleStudio-StudioAdmin managed policy attached for the portal to function properly.

    You can optionally specify an AWS Key Management Service key in the StudioEncryptionConfiguration. In Nimble Studio, resource names, descriptions, initialization scripts, and other data you provide are always encrypted at rest using an AWS Key Management Service key. By default, this key is owned by AWS and managed on your behalf. You may provide your own AWS Key Management Service key when calling CreateStudio to encrypt this data using a key that you own and manage. When providing an AWS Key Management Service key during studio creation,  creates AWS Key Management Service grants in your account to provide your studio user and admin roles access to these AWS Key Management Service keys. If you delete this grant, the studio will no longer be accessible to your portal users. If you delete the studio AWS Key Management Service key, your studio will no longer be accessible.

    :cloudformationResource: AWS::NimbleStudio::Studio
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_nimblestudio as nimblestudio
        
        cfn_studio = nimblestudio.CfnStudio(self, "MyCfnStudio",
            admin_role_arn="adminRoleArn",
            display_name="displayName",
            studio_name="studioName",
            user_role_arn="userRoleArn",
        
            # the properties below are optional
            studio_encryption_configuration=nimblestudio.CfnStudio.StudioEncryptionConfigurationProperty(
                key_type="keyType",
        
                # the properties below are optional
                key_arn="keyArn"
            ),
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        admin_role_arn: builtins.str,
        display_name: builtins.str,
        studio_name: builtins.str,
        user_role_arn: builtins.str,
        studio_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStudio.StudioEncryptionConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::NimbleStudio::Studio``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param admin_role_arn: The IAM role that studio admins assume when logging in to the Nimble Studio portal.
        :param display_name: A friendly name for the studio.
        :param studio_name: The name of the studio, as included in the URL when accessing it in the Nimble Studio portal.
        :param user_role_arn: The IAM role that studio users assume when logging in to the Nimble Studio portal.
        :param studio_encryption_configuration: Configuration of the encryption method that is used for the studio.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90d4c4a93bf43d8cad8646079a6db65776199e513ccb3ac4a462da0c319a522e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStudioProps(
            admin_role_arn=admin_role_arn,
            display_name=display_name,
            studio_name=studio_name,
            user_role_arn=user_role_arn,
            studio_encryption_configuration=studio_encryption_configuration,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8ae356054a13f377e56d0acc1c2fb15289817fffa6c1d730a75e1174031c60e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ec25845a60c2ae8080cf4128b541171eb07373c48040ec0e63a91cdbc5553953)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrHomeRegion")
    def attr_home_region(self) -> builtins.str:
        '''The AWS Region where the studio resource is located.

        For example, ``us-west-2`` .

        :cloudformationAttribute: HomeRegion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrHomeRegion"))

    @builtins.property
    @jsii.member(jsii_name="attrSsoClientId")
    def attr_sso_client_id(self) -> builtins.str:
        '''The IAM Identity Center application client ID that is used to integrate with IAM Identity Center , which enables IAM Identity Center users to log into the  portal.

        :cloudformationAttribute: SsoClientId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSsoClientId"))

    @builtins.property
    @jsii.member(jsii_name="attrStudioId")
    def attr_studio_id(self) -> builtins.str:
        '''The unique identifier for the studio resource.

        :cloudformationAttribute: StudioId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStudioId"))

    @builtins.property
    @jsii.member(jsii_name="attrStudioUrl")
    def attr_studio_url(self) -> builtins.str:
        '''The unique identifier for the studio resource.

        :cloudformationAttribute: StudioUrl
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStudioUrl"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="adminRoleArn")
    def admin_role_arn(self) -> builtins.str:
        '''The IAM role that studio admins assume when logging in to the Nimble Studio portal.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-adminrolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "adminRoleArn"))

    @admin_role_arn.setter
    def admin_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e862a04070bc9123b253fed701bcb720a1ad533998d15ee16c90f8dfe761287c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "adminRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="displayName")
    def display_name(self) -> builtins.str:
        '''A friendly name for the studio.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-displayname
        '''
        return typing.cast(builtins.str, jsii.get(self, "displayName"))

    @display_name.setter
    def display_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4cb73b22ed94b3610e3b8a19162f859a34d32315187162dec2ba760a061ca82)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "displayName", value)

    @builtins.property
    @jsii.member(jsii_name="studioName")
    def studio_name(self) -> builtins.str:
        '''The name of the studio, as included in the URL when accessing it in the Nimble Studio portal.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-studioname
        '''
        return typing.cast(builtins.str, jsii.get(self, "studioName"))

    @studio_name.setter
    def studio_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afd7fc3e2d7714b1c70b114b7f41ba099d32ac7cf6aafea0938d0b5a205af0ff)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "studioName", value)

    @builtins.property
    @jsii.member(jsii_name="userRoleArn")
    def user_role_arn(self) -> builtins.str:
        '''The IAM role that studio users assume when logging in to the Nimble Studio portal.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-userrolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "userRoleArn"))

    @user_role_arn.setter
    def user_role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7507d2abad38e6bb3cf4248a440e64eab7890005342ab7f747139bb4fae3ecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="studioEncryptionConfiguration")
    def studio_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudio.StudioEncryptionConfigurationProperty"]]:
        '''Configuration of the encryption method that is used for the studio.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-studioencryptionconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudio.StudioEncryptionConfigurationProperty"]], jsii.get(self, "studioEncryptionConfiguration"))

    @studio_encryption_configuration.setter
    def studio_encryption_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudio.StudioEncryptionConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae28e2b022215876656ef6d565dff4b388ce4e5b845c7a0f7053eabfd2a0e3fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "studioEncryptionConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-nimblestudio.CfnStudio.StudioEncryptionConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"key_type": "keyType", "key_arn": "keyArn"},
    )
    class StudioEncryptionConfigurationProperty:
        def __init__(
            self,
            *,
            key_type: builtins.str,
            key_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration of the encryption method that is used for the studio.

            :param key_type: The type of KMS key that is used to encrypt studio data.
            :param key_arn: The ARN for a KMS key that is used to encrypt studio data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studio-studioencryptionconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_nimblestudio as nimblestudio
                
                studio_encryption_configuration_property = nimblestudio.CfnStudio.StudioEncryptionConfigurationProperty(
                    key_type="keyType",
                
                    # the properties below are optional
                    key_arn="keyArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__151bc8d4ad08e04e58d0a0ecc1a979fc613a85fc1f3d2b31137859a84b9f1e74)
                check_type(argname="argument key_type", value=key_type, expected_type=type_hints["key_type"])
                check_type(argname="argument key_arn", value=key_arn, expected_type=type_hints["key_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key_type": key_type,
            }
            if key_arn is not None:
                self._values["key_arn"] = key_arn

        @builtins.property
        def key_type(self) -> builtins.str:
            '''The type of KMS key that is used to encrypt studio data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studio-studioencryptionconfiguration.html#cfn-nimblestudio-studio-studioencryptionconfiguration-keytype
            '''
            result = self._values.get("key_type")
            assert result is not None, "Required property 'key_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def key_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN for a KMS key that is used to encrypt studio data.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studio-studioencryptionconfiguration.html#cfn-nimblestudio-studio-studioencryptionconfiguration-keyarn
            '''
            result = self._values.get("key_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StudioEncryptionConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnStudioComponent(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-nimblestudio.CfnStudioComponent",
):
    '''A CloudFormation ``AWS::NimbleStudio::StudioComponent``.

    The ``AWS::NimbleStudio::StudioComponent`` resource represents a network resource that is used by a studio's users and workflows. A typical studio contains studio components for the following: a render farm, an Active Directory, a licensing service, and a shared file system.

    Access to a studio component is managed by specifying security groups for the resource, as well as its endpoint.

    A studio component also has a set of initialization scripts, which are returned by ``GetLaunchProfileInitialization`` . These initialization scripts run on streaming sessions when they start. They provide users with flexibility in controlling how studio resources are configured on a streaming session.

    :cloudformationResource: AWS::NimbleStudio::StudioComponent
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_nimblestudio as nimblestudio
        
        cfn_studio_component = nimblestudio.CfnStudioComponent(self, "MyCfnStudioComponent",
            name="name",
            studio_id="studioId",
            type="type",
        
            # the properties below are optional
            configuration=nimblestudio.CfnStudioComponent.StudioComponentConfigurationProperty(
                active_directory_configuration=nimblestudio.CfnStudioComponent.ActiveDirectoryConfigurationProperty(
                    computer_attributes=[nimblestudio.CfnStudioComponent.ActiveDirectoryComputerAttributeProperty(
                        name="name",
                        value="value"
                    )],
                    directory_id="directoryId",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                ),
                compute_farm_configuration=nimblestudio.CfnStudioComponent.ComputeFarmConfigurationProperty(
                    active_directory_user="activeDirectoryUser",
                    endpoint="endpoint"
                ),
                license_service_configuration=nimblestudio.CfnStudioComponent.LicenseServiceConfigurationProperty(
                    endpoint="endpoint"
                ),
                shared_file_system_configuration=nimblestudio.CfnStudioComponent.SharedFileSystemConfigurationProperty(
                    endpoint="endpoint",
                    file_system_id="fileSystemId",
                    linux_mount_point="linuxMountPoint",
                    share_name="shareName",
                    windows_mount_drive="windowsMountDrive"
                )
            ),
            description="description",
            ec2_security_group_ids=["ec2SecurityGroupIds"],
            initialization_scripts=[nimblestudio.CfnStudioComponent.StudioComponentInitializationScriptProperty(
                launch_profile_protocol_version="launchProfileProtocolVersion",
                platform="platform",
                run_context="runContext",
                script="script"
            )],
            script_parameters=[nimblestudio.CfnStudioComponent.ScriptParameterKeyValueProperty(
                key="key",
                value="value"
            )],
            subtype="subtype",
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        name: builtins.str,
        studio_id: builtins.str,
        type: builtins.str,
        configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStudioComponent.StudioComponentConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        ec2_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        initialization_scripts: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStudioComponent.StudioComponentInitializationScriptProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        script_parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStudioComponent.ScriptParameterKeyValueProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        subtype: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::NimbleStudio::StudioComponent``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: A friendly name for the studio component resource.
        :param studio_id: The unique identifier for a studio resource. In Nimble Studio , all other resources are contained in a studio resource.
        :param type: The type of the studio component.
        :param configuration: The configuration of the studio component, based on component type.
        :param description: A human-readable description for the studio component resource.
        :param ec2_security_group_ids: The EC2 security groups that control access to the studio component.
        :param initialization_scripts: Initialization scripts for studio components.
        :param script_parameters: Parameters for the studio component scripts.
        :param subtype: The specific subtype of a studio component.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e3c0eb16d04afe47169ddb9a2fa82d6b006a1d3ed3e3da212e3238a07ad3626)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnStudioComponentProps(
            name=name,
            studio_id=studio_id,
            type=type,
            configuration=configuration,
            description=description,
            ec2_security_group_ids=ec2_security_group_ids,
            initialization_scripts=initialization_scripts,
            script_parameters=script_parameters,
            subtype=subtype,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1c7ed2ebebd50254a1314b40c49f5286c5f3774e8de2a8d1c4e53a728c955a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50fd5b9d6806280cb1e48abf3995098f3c85825b03840cad70eb761fe9d4ced3)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrStudioComponentId")
    def attr_studio_component_id(self) -> builtins.str:
        '''The unique identifier for the studio component resource.

        :cloudformationAttribute: StudioComponentId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStudioComponentId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A friendly name for the studio component resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8415d32224058d2bb343ff394b3d04243d94f6796b27e295e2c1e2b86e659a87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="studioId")
    def studio_id(self) -> builtins.str:
        '''The unique identifier for a studio resource.

        In Nimble Studio , all other resources are contained in a studio resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-studioid
        '''
        return typing.cast(builtins.str, jsii.get(self, "studioId"))

    @studio_id.setter
    def studio_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__069fcdc083af7272e9a6f980f6f260985ef2f568a023128e586fb6aea26418a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "studioId", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of the studio component.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e158b2dbd41296d887d193ab2cdaff33c2aa69ae68bb1fee966136566b9973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="configuration")
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.StudioComponentConfigurationProperty"]]:
        '''The configuration of the studio component, based on component type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-configuration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.StudioComponentConfigurationProperty"]], jsii.get(self, "configuration"))

    @configuration.setter
    def configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.StudioComponentConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__320e9dd79576eb41c8a341fec73cf6746aa6e0f7561271e2606dd4751f77f5fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configuration", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description for the studio component resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a10b7a0d7e029f35fc0fba06ad63b68890e07cc77691ae4093af86b92fd3b1f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="ec2SecurityGroupIds")
    def ec2_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The EC2 security groups that control access to the studio component.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-ec2securitygroupids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ec2SecurityGroupIds"))

    @ec2_security_group_ids.setter
    def ec2_security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a24d585026939a006d5e9fcfffac490028a542729cdf34fe6f42573adaa4a6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ec2SecurityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="initializationScripts")
    def initialization_scripts(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.StudioComponentInitializationScriptProperty"]]]]:
        '''Initialization scripts for studio components.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-initializationscripts
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.StudioComponentInitializationScriptProperty"]]]], jsii.get(self, "initializationScripts"))

    @initialization_scripts.setter
    def initialization_scripts(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.StudioComponentInitializationScriptProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c95f9b38b6e1514c87ae00a5beaafc01971a81098366d3e9acf0331635232ede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initializationScripts", value)

    @builtins.property
    @jsii.member(jsii_name="scriptParameters")
    def script_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.ScriptParameterKeyValueProperty"]]]]:
        '''Parameters for the studio component scripts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-scriptparameters
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.ScriptParameterKeyValueProperty"]]]], jsii.get(self, "scriptParameters"))

    @script_parameters.setter
    def script_parameters(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.ScriptParameterKeyValueProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e921e6fda58b2a48f40d8279270eb15322a0546640442433f17ca177c4bbb98)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scriptParameters", value)

    @builtins.property
    @jsii.member(jsii_name="subtype")
    def subtype(self) -> typing.Optional[builtins.str]:
        '''The specific subtype of a studio component.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-subtype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subtype"))

    @subtype.setter
    def subtype(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81d6310c8c115eea45e5a9017a06976d07404bc8ddb7a8be74577762ecad5d0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subtype", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-nimblestudio.CfnStudioComponent.ActiveDirectoryComputerAttributeProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class ActiveDirectoryComputerAttributeProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''An LDAP attribute of an Active Directory computer account, in the form of a name:value pair.

            :param name: The name for the LDAP attribute.
            :param value: The value for the LDAP attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-activedirectorycomputerattribute.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_nimblestudio as nimblestudio
                
                active_directory_computer_attribute_property = nimblestudio.CfnStudioComponent.ActiveDirectoryComputerAttributeProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b875f54a611b59e7df903b01e6b986501f90ce1958e7dcd23fbd220f2cffb993)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name for the LDAP attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-activedirectorycomputerattribute.html#cfn-nimblestudio-studiocomponent-activedirectorycomputerattribute-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The value for the LDAP attribute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-activedirectorycomputerattribute.html#cfn-nimblestudio-studiocomponent-activedirectorycomputerattribute-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActiveDirectoryComputerAttributeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-nimblestudio.CfnStudioComponent.ActiveDirectoryConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "computer_attributes": "computerAttributes",
            "directory_id": "directoryId",
            "organizational_unit_distinguished_name": "organizationalUnitDistinguishedName",
        },
    )
    class ActiveDirectoryConfigurationProperty:
        def __init__(
            self,
            *,
            computer_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStudioComponent.ActiveDirectoryComputerAttributeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            directory_id: typing.Optional[builtins.str] = None,
            organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for a AWS Directory Service for Microsoft Active Directory studio resource.

            :param computer_attributes: A collection of custom attributes for an Active Directory computer.
            :param directory_id: The directory ID of the AWS Directory Service for Microsoft Active Directory to access using this studio component.
            :param organizational_unit_distinguished_name: The distinguished name (DN) and organizational unit (OU) of an Active Directory computer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-activedirectoryconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_nimblestudio as nimblestudio
                
                active_directory_configuration_property = nimblestudio.CfnStudioComponent.ActiveDirectoryConfigurationProperty(
                    computer_attributes=[nimblestudio.CfnStudioComponent.ActiveDirectoryComputerAttributeProperty(
                        name="name",
                        value="value"
                    )],
                    directory_id="directoryId",
                    organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6a0b3cde54cba5bac452a8c40a593708fc40133d88c0769d404dc1cde4bc4d0c)
                check_type(argname="argument computer_attributes", value=computer_attributes, expected_type=type_hints["computer_attributes"])
                check_type(argname="argument directory_id", value=directory_id, expected_type=type_hints["directory_id"])
                check_type(argname="argument organizational_unit_distinguished_name", value=organizational_unit_distinguished_name, expected_type=type_hints["organizational_unit_distinguished_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if computer_attributes is not None:
                self._values["computer_attributes"] = computer_attributes
            if directory_id is not None:
                self._values["directory_id"] = directory_id
            if organizational_unit_distinguished_name is not None:
                self._values["organizational_unit_distinguished_name"] = organizational_unit_distinguished_name

        @builtins.property
        def computer_attributes(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.ActiveDirectoryComputerAttributeProperty"]]]]:
            '''A collection of custom attributes for an Active Directory computer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-activedirectoryconfiguration.html#cfn-nimblestudio-studiocomponent-activedirectoryconfiguration-computerattributes
            '''
            result = self._values.get("computer_attributes")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.ActiveDirectoryComputerAttributeProperty"]]]], result)

        @builtins.property
        def directory_id(self) -> typing.Optional[builtins.str]:
            '''The directory ID of the AWS Directory Service for Microsoft Active Directory to access using this studio component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-activedirectoryconfiguration.html#cfn-nimblestudio-studiocomponent-activedirectoryconfiguration-directoryid
            '''
            result = self._values.get("directory_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def organizational_unit_distinguished_name(
            self,
        ) -> typing.Optional[builtins.str]:
            '''The distinguished name (DN) and organizational unit (OU) of an Active Directory computer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-activedirectoryconfiguration.html#cfn-nimblestudio-studiocomponent-activedirectoryconfiguration-organizationalunitdistinguishedname
            '''
            result = self._values.get("organizational_unit_distinguished_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActiveDirectoryConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-nimblestudio.CfnStudioComponent.ComputeFarmConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "active_directory_user": "activeDirectoryUser",
            "endpoint": "endpoint",
        },
    )
    class ComputeFarmConfigurationProperty:
        def __init__(
            self,
            *,
            active_directory_user: typing.Optional[builtins.str] = None,
            endpoint: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for a render farm that is associated with a studio resource.

            :param active_directory_user: The name of an Active Directory user that is used on ComputeFarm worker instances.
            :param endpoint: The endpoint of the ComputeFarm that is accessed by the studio component resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-computefarmconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_nimblestudio as nimblestudio
                
                compute_farm_configuration_property = nimblestudio.CfnStudioComponent.ComputeFarmConfigurationProperty(
                    active_directory_user="activeDirectoryUser",
                    endpoint="endpoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f0e9d6e0b80f05807a7bbd8ffc59d0b9cb16bd374ca0f2b27be522aa05c0c62e)
                check_type(argname="argument active_directory_user", value=active_directory_user, expected_type=type_hints["active_directory_user"])
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if active_directory_user is not None:
                self._values["active_directory_user"] = active_directory_user
            if endpoint is not None:
                self._values["endpoint"] = endpoint

        @builtins.property
        def active_directory_user(self) -> typing.Optional[builtins.str]:
            '''The name of an Active Directory user that is used on ComputeFarm worker instances.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-computefarmconfiguration.html#cfn-nimblestudio-studiocomponent-computefarmconfiguration-activedirectoryuser
            '''
            result = self._values.get("active_directory_user")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''The endpoint of the ComputeFarm that is accessed by the studio component resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-computefarmconfiguration.html#cfn-nimblestudio-studiocomponent-computefarmconfiguration-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComputeFarmConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-nimblestudio.CfnStudioComponent.LicenseServiceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"endpoint": "endpoint"},
    )
    class LicenseServiceConfigurationProperty:
        def __init__(self, *, endpoint: typing.Optional[builtins.str] = None) -> None:
            '''The configuration for a license service that is associated with a studio resource.

            :param endpoint: The endpoint of the license service that is accessed by the studio component resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-licenseserviceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_nimblestudio as nimblestudio
                
                license_service_configuration_property = nimblestudio.CfnStudioComponent.LicenseServiceConfigurationProperty(
                    endpoint="endpoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6c8b84605ea5ade2ab06d5496a764b61d7bd2d5a1f3940a7bc53273918d2a336)
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint is not None:
                self._values["endpoint"] = endpoint

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''The endpoint of the license service that is accessed by the studio component resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-licenseserviceconfiguration.html#cfn-nimblestudio-studiocomponent-licenseserviceconfiguration-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LicenseServiceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-nimblestudio.CfnStudioComponent.ScriptParameterKeyValueProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ScriptParameterKeyValueProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A parameter for a studio component script, in the form of a key-value pair.

            :param key: A script parameter key.
            :param value: A script parameter value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-scriptparameterkeyvalue.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_nimblestudio as nimblestudio
                
                script_parameter_key_value_property = nimblestudio.CfnStudioComponent.ScriptParameterKeyValueProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__781146a9f5a1a93e08c1052f807c5b5057ec43b8e68c56edefaaf2bb9527e04b)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''A script parameter key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-scriptparameterkeyvalue.html#cfn-nimblestudio-studiocomponent-scriptparameterkeyvalue-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''A script parameter value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-scriptparameterkeyvalue.html#cfn-nimblestudio-studiocomponent-scriptparameterkeyvalue-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScriptParameterKeyValueProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-nimblestudio.CfnStudioComponent.SharedFileSystemConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "endpoint": "endpoint",
            "file_system_id": "fileSystemId",
            "linux_mount_point": "linuxMountPoint",
            "share_name": "shareName",
            "windows_mount_drive": "windowsMountDrive",
        },
    )
    class SharedFileSystemConfigurationProperty:
        def __init__(
            self,
            *,
            endpoint: typing.Optional[builtins.str] = None,
            file_system_id: typing.Optional[builtins.str] = None,
            linux_mount_point: typing.Optional[builtins.str] = None,
            share_name: typing.Optional[builtins.str] = None,
            windows_mount_drive: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The configuration for a shared file storage system that is associated with a studio resource.

            :param endpoint: The endpoint of the shared file system that is accessed by the studio component resource.
            :param file_system_id: The unique identifier for a file system.
            :param linux_mount_point: The mount location for a shared file system on a Linux virtual workstation.
            :param share_name: The name of the file share.
            :param windows_mount_drive: The mount location for a shared file system on a Windows virtual workstation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-sharedfilesystemconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_nimblestudio as nimblestudio
                
                shared_file_system_configuration_property = nimblestudio.CfnStudioComponent.SharedFileSystemConfigurationProperty(
                    endpoint="endpoint",
                    file_system_id="fileSystemId",
                    linux_mount_point="linuxMountPoint",
                    share_name="shareName",
                    windows_mount_drive="windowsMountDrive"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__42b99b4bc908fa99efb7f34ea662d3125db2ac9186c6229b314b583cfd7894be)
                check_type(argname="argument endpoint", value=endpoint, expected_type=type_hints["endpoint"])
                check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
                check_type(argname="argument linux_mount_point", value=linux_mount_point, expected_type=type_hints["linux_mount_point"])
                check_type(argname="argument share_name", value=share_name, expected_type=type_hints["share_name"])
                check_type(argname="argument windows_mount_drive", value=windows_mount_drive, expected_type=type_hints["windows_mount_drive"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if endpoint is not None:
                self._values["endpoint"] = endpoint
            if file_system_id is not None:
                self._values["file_system_id"] = file_system_id
            if linux_mount_point is not None:
                self._values["linux_mount_point"] = linux_mount_point
            if share_name is not None:
                self._values["share_name"] = share_name
            if windows_mount_drive is not None:
                self._values["windows_mount_drive"] = windows_mount_drive

        @builtins.property
        def endpoint(self) -> typing.Optional[builtins.str]:
            '''The endpoint of the shared file system that is accessed by the studio component resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-sharedfilesystemconfiguration.html#cfn-nimblestudio-studiocomponent-sharedfilesystemconfiguration-endpoint
            '''
            result = self._values.get("endpoint")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def file_system_id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier for a file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-sharedfilesystemconfiguration.html#cfn-nimblestudio-studiocomponent-sharedfilesystemconfiguration-filesystemid
            '''
            result = self._values.get("file_system_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def linux_mount_point(self) -> typing.Optional[builtins.str]:
            '''The mount location for a shared file system on a Linux virtual workstation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-sharedfilesystemconfiguration.html#cfn-nimblestudio-studiocomponent-sharedfilesystemconfiguration-linuxmountpoint
            '''
            result = self._values.get("linux_mount_point")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def share_name(self) -> typing.Optional[builtins.str]:
            '''The name of the file share.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-sharedfilesystemconfiguration.html#cfn-nimblestudio-studiocomponent-sharedfilesystemconfiguration-sharename
            '''
            result = self._values.get("share_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def windows_mount_drive(self) -> typing.Optional[builtins.str]:
            '''The mount location for a shared file system on a Windows virtual workstation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-sharedfilesystemconfiguration.html#cfn-nimblestudio-studiocomponent-sharedfilesystemconfiguration-windowsmountdrive
            '''
            result = self._values.get("windows_mount_drive")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SharedFileSystemConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-nimblestudio.CfnStudioComponent.StudioComponentConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "active_directory_configuration": "activeDirectoryConfiguration",
            "compute_farm_configuration": "computeFarmConfiguration",
            "license_service_configuration": "licenseServiceConfiguration",
            "shared_file_system_configuration": "sharedFileSystemConfiguration",
        },
    )
    class StudioComponentConfigurationProperty:
        def __init__(
            self,
            *,
            active_directory_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStudioComponent.ActiveDirectoryConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            compute_farm_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStudioComponent.ComputeFarmConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            license_service_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStudioComponent.LicenseServiceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            shared_file_system_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnStudioComponent.SharedFileSystemConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The configuration of the studio component, based on component type.

            :param active_directory_configuration: The configuration for a AWS Directory Service for Microsoft Active Directory studio resource.
            :param compute_farm_configuration: The configuration for a render farm that is associated with a studio resource.
            :param license_service_configuration: The configuration for a license service that is associated with a studio resource.
            :param shared_file_system_configuration: The configuration for a shared file storage system that is associated with a studio resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_nimblestudio as nimblestudio
                
                studio_component_configuration_property = nimblestudio.CfnStudioComponent.StudioComponentConfigurationProperty(
                    active_directory_configuration=nimblestudio.CfnStudioComponent.ActiveDirectoryConfigurationProperty(
                        computer_attributes=[nimblestudio.CfnStudioComponent.ActiveDirectoryComputerAttributeProperty(
                            name="name",
                            value="value"
                        )],
                        directory_id="directoryId",
                        organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                    ),
                    compute_farm_configuration=nimblestudio.CfnStudioComponent.ComputeFarmConfigurationProperty(
                        active_directory_user="activeDirectoryUser",
                        endpoint="endpoint"
                    ),
                    license_service_configuration=nimblestudio.CfnStudioComponent.LicenseServiceConfigurationProperty(
                        endpoint="endpoint"
                    ),
                    shared_file_system_configuration=nimblestudio.CfnStudioComponent.SharedFileSystemConfigurationProperty(
                        endpoint="endpoint",
                        file_system_id="fileSystemId",
                        linux_mount_point="linuxMountPoint",
                        share_name="shareName",
                        windows_mount_drive="windowsMountDrive"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b067c27972287b8a8943fd79e6becb04b7f27f91d2172d88c6ec70b52a02eeb8)
                check_type(argname="argument active_directory_configuration", value=active_directory_configuration, expected_type=type_hints["active_directory_configuration"])
                check_type(argname="argument compute_farm_configuration", value=compute_farm_configuration, expected_type=type_hints["compute_farm_configuration"])
                check_type(argname="argument license_service_configuration", value=license_service_configuration, expected_type=type_hints["license_service_configuration"])
                check_type(argname="argument shared_file_system_configuration", value=shared_file_system_configuration, expected_type=type_hints["shared_file_system_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if active_directory_configuration is not None:
                self._values["active_directory_configuration"] = active_directory_configuration
            if compute_farm_configuration is not None:
                self._values["compute_farm_configuration"] = compute_farm_configuration
            if license_service_configuration is not None:
                self._values["license_service_configuration"] = license_service_configuration
            if shared_file_system_configuration is not None:
                self._values["shared_file_system_configuration"] = shared_file_system_configuration

        @builtins.property
        def active_directory_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.ActiveDirectoryConfigurationProperty"]]:
            '''The configuration for a AWS Directory Service for Microsoft Active Directory studio resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentconfiguration.html#cfn-nimblestudio-studiocomponent-studiocomponentconfiguration-activedirectoryconfiguration
            '''
            result = self._values.get("active_directory_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.ActiveDirectoryConfigurationProperty"]], result)

        @builtins.property
        def compute_farm_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.ComputeFarmConfigurationProperty"]]:
            '''The configuration for a render farm that is associated with a studio resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentconfiguration.html#cfn-nimblestudio-studiocomponent-studiocomponentconfiguration-computefarmconfiguration
            '''
            result = self._values.get("compute_farm_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.ComputeFarmConfigurationProperty"]], result)

        @builtins.property
        def license_service_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.LicenseServiceConfigurationProperty"]]:
            '''The configuration for a license service that is associated with a studio resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentconfiguration.html#cfn-nimblestudio-studiocomponent-studiocomponentconfiguration-licenseserviceconfiguration
            '''
            result = self._values.get("license_service_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.LicenseServiceConfigurationProperty"]], result)

        @builtins.property
        def shared_file_system_configuration(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.SharedFileSystemConfigurationProperty"]]:
            '''The configuration for a shared file storage system that is associated with a studio resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentconfiguration.html#cfn-nimblestudio-studiocomponent-studiocomponentconfiguration-sharedfilesystemconfiguration
            '''
            result = self._values.get("shared_file_system_configuration")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnStudioComponent.SharedFileSystemConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StudioComponentConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-nimblestudio.CfnStudioComponent.StudioComponentInitializationScriptProperty",
        jsii_struct_bases=[],
        name_mapping={
            "launch_profile_protocol_version": "launchProfileProtocolVersion",
            "platform": "platform",
            "run_context": "runContext",
            "script": "script",
        },
    )
    class StudioComponentInitializationScriptProperty:
        def __init__(
            self,
            *,
            launch_profile_protocol_version: typing.Optional[builtins.str] = None,
            platform: typing.Optional[builtins.str] = None,
            run_context: typing.Optional[builtins.str] = None,
            script: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Initialization scripts for studio components.

            :param launch_profile_protocol_version: The version number of the protocol that is used by the launch profile. The only valid version is "2021-03-31".
            :param platform: The platform of the initialization script, either Windows or Linux.
            :param run_context: The method to use when running the initialization script.
            :param script: The initialization script.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentinitializationscript.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_nimblestudio as nimblestudio
                
                studio_component_initialization_script_property = nimblestudio.CfnStudioComponent.StudioComponentInitializationScriptProperty(
                    launch_profile_protocol_version="launchProfileProtocolVersion",
                    platform="platform",
                    run_context="runContext",
                    script="script"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__273c2d59ae7e1c5c919f75c2bc128f61cebebf9de0e1619a4a31eb7661a1b875)
                check_type(argname="argument launch_profile_protocol_version", value=launch_profile_protocol_version, expected_type=type_hints["launch_profile_protocol_version"])
                check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
                check_type(argname="argument run_context", value=run_context, expected_type=type_hints["run_context"])
                check_type(argname="argument script", value=script, expected_type=type_hints["script"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if launch_profile_protocol_version is not None:
                self._values["launch_profile_protocol_version"] = launch_profile_protocol_version
            if platform is not None:
                self._values["platform"] = platform
            if run_context is not None:
                self._values["run_context"] = run_context
            if script is not None:
                self._values["script"] = script

        @builtins.property
        def launch_profile_protocol_version(self) -> typing.Optional[builtins.str]:
            '''The version number of the protocol that is used by the launch profile.

            The only valid version is "2021-03-31".

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentinitializationscript.html#cfn-nimblestudio-studiocomponent-studiocomponentinitializationscript-launchprofileprotocolversion
            '''
            result = self._values.get("launch_profile_protocol_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def platform(self) -> typing.Optional[builtins.str]:
            '''The platform of the initialization script, either Windows or Linux.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentinitializationscript.html#cfn-nimblestudio-studiocomponent-studiocomponentinitializationscript-platform
            '''
            result = self._values.get("platform")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def run_context(self) -> typing.Optional[builtins.str]:
            '''The method to use when running the initialization script.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentinitializationscript.html#cfn-nimblestudio-studiocomponent-studiocomponentinitializationscript-runcontext
            '''
            result = self._values.get("run_context")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def script(self) -> typing.Optional[builtins.str]:
            '''The initialization script.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-nimblestudio-studiocomponent-studiocomponentinitializationscript.html#cfn-nimblestudio-studiocomponent-studiocomponentinitializationscript-script
            '''
            result = self._values.get("script")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StudioComponentInitializationScriptProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-nimblestudio.CfnStudioComponentProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "studio_id": "studioId",
        "type": "type",
        "configuration": "configuration",
        "description": "description",
        "ec2_security_group_ids": "ec2SecurityGroupIds",
        "initialization_scripts": "initializationScripts",
        "script_parameters": "scriptParameters",
        "subtype": "subtype",
        "tags": "tags",
    },
)
class CfnStudioComponentProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        studio_id: builtins.str,
        type: builtins.str,
        configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStudioComponent.StudioComponentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        ec2_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        initialization_scripts: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStudioComponent.StudioComponentInitializationScriptProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        script_parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStudioComponent.ScriptParameterKeyValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        subtype: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnStudioComponent``.

        :param name: A friendly name for the studio component resource.
        :param studio_id: The unique identifier for a studio resource. In Nimble Studio , all other resources are contained in a studio resource.
        :param type: The type of the studio component.
        :param configuration: The configuration of the studio component, based on component type.
        :param description: A human-readable description for the studio component resource.
        :param ec2_security_group_ids: The EC2 security groups that control access to the studio component.
        :param initialization_scripts: Initialization scripts for studio components.
        :param script_parameters: Parameters for the studio component scripts.
        :param subtype: The specific subtype of a studio component.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_nimblestudio as nimblestudio
            
            cfn_studio_component_props = nimblestudio.CfnStudioComponentProps(
                name="name",
                studio_id="studioId",
                type="type",
            
                # the properties below are optional
                configuration=nimblestudio.CfnStudioComponent.StudioComponentConfigurationProperty(
                    active_directory_configuration=nimblestudio.CfnStudioComponent.ActiveDirectoryConfigurationProperty(
                        computer_attributes=[nimblestudio.CfnStudioComponent.ActiveDirectoryComputerAttributeProperty(
                            name="name",
                            value="value"
                        )],
                        directory_id="directoryId",
                        organizational_unit_distinguished_name="organizationalUnitDistinguishedName"
                    ),
                    compute_farm_configuration=nimblestudio.CfnStudioComponent.ComputeFarmConfigurationProperty(
                        active_directory_user="activeDirectoryUser",
                        endpoint="endpoint"
                    ),
                    license_service_configuration=nimblestudio.CfnStudioComponent.LicenseServiceConfigurationProperty(
                        endpoint="endpoint"
                    ),
                    shared_file_system_configuration=nimblestudio.CfnStudioComponent.SharedFileSystemConfigurationProperty(
                        endpoint="endpoint",
                        file_system_id="fileSystemId",
                        linux_mount_point="linuxMountPoint",
                        share_name="shareName",
                        windows_mount_drive="windowsMountDrive"
                    )
                ),
                description="description",
                ec2_security_group_ids=["ec2SecurityGroupIds"],
                initialization_scripts=[nimblestudio.CfnStudioComponent.StudioComponentInitializationScriptProperty(
                    launch_profile_protocol_version="launchProfileProtocolVersion",
                    platform="platform",
                    run_context="runContext",
                    script="script"
                )],
                script_parameters=[nimblestudio.CfnStudioComponent.ScriptParameterKeyValueProperty(
                    key="key",
                    value="value"
                )],
                subtype="subtype",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a906fc8dd291692c93929e40d19adab6e31e32a079bd5f5b0b291c01e3698de9)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument studio_id", value=studio_id, expected_type=type_hints["studio_id"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument configuration", value=configuration, expected_type=type_hints["configuration"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument ec2_security_group_ids", value=ec2_security_group_ids, expected_type=type_hints["ec2_security_group_ids"])
            check_type(argname="argument initialization_scripts", value=initialization_scripts, expected_type=type_hints["initialization_scripts"])
            check_type(argname="argument script_parameters", value=script_parameters, expected_type=type_hints["script_parameters"])
            check_type(argname="argument subtype", value=subtype, expected_type=type_hints["subtype"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "studio_id": studio_id,
            "type": type,
        }
        if configuration is not None:
            self._values["configuration"] = configuration
        if description is not None:
            self._values["description"] = description
        if ec2_security_group_ids is not None:
            self._values["ec2_security_group_ids"] = ec2_security_group_ids
        if initialization_scripts is not None:
            self._values["initialization_scripts"] = initialization_scripts
        if script_parameters is not None:
            self._values["script_parameters"] = script_parameters
        if subtype is not None:
            self._values["subtype"] = subtype
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''A friendly name for the studio component resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def studio_id(self) -> builtins.str:
        '''The unique identifier for a studio resource.

        In Nimble Studio , all other resources are contained in a studio resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-studioid
        '''
        result = self._values.get("studio_id")
        assert result is not None, "Required property 'studio_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of the studio component.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStudioComponent.StudioComponentConfigurationProperty]]:
        '''The configuration of the studio component, based on component type.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-configuration
        '''
        result = self._values.get("configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStudioComponent.StudioComponentConfigurationProperty]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A human-readable description for the studio component resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ec2_security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The EC2 security groups that control access to the studio component.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-ec2securitygroupids
        '''
        result = self._values.get("ec2_security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def initialization_scripts(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStudioComponent.StudioComponentInitializationScriptProperty]]]]:
        '''Initialization scripts for studio components.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-initializationscripts
        '''
        result = self._values.get("initialization_scripts")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStudioComponent.StudioComponentInitializationScriptProperty]]]], result)

    @builtins.property
    def script_parameters(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStudioComponent.ScriptParameterKeyValueProperty]]]]:
        '''Parameters for the studio component scripts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-scriptparameters
        '''
        result = self._values.get("script_parameters")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStudioComponent.ScriptParameterKeyValueProperty]]]], result)

    @builtins.property
    def subtype(self) -> typing.Optional[builtins.str]:
        '''The specific subtype of a studio component.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-subtype
        '''
        result = self._values.get("subtype")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studiocomponent.html#cfn-nimblestudio-studiocomponent-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStudioComponentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-nimblestudio.CfnStudioProps",
    jsii_struct_bases=[],
    name_mapping={
        "admin_role_arn": "adminRoleArn",
        "display_name": "displayName",
        "studio_name": "studioName",
        "user_role_arn": "userRoleArn",
        "studio_encryption_configuration": "studioEncryptionConfiguration",
        "tags": "tags",
    },
)
class CfnStudioProps:
    def __init__(
        self,
        *,
        admin_role_arn: builtins.str,
        display_name: builtins.str,
        studio_name: builtins.str,
        user_role_arn: builtins.str,
        studio_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStudio.StudioEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnStudio``.

        :param admin_role_arn: The IAM role that studio admins assume when logging in to the Nimble Studio portal.
        :param display_name: A friendly name for the studio.
        :param studio_name: The name of the studio, as included in the URL when accessing it in the Nimble Studio portal.
        :param user_role_arn: The IAM role that studio users assume when logging in to the Nimble Studio portal.
        :param studio_encryption_configuration: Configuration of the encryption method that is used for the studio.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_nimblestudio as nimblestudio
            
            cfn_studio_props = nimblestudio.CfnStudioProps(
                admin_role_arn="adminRoleArn",
                display_name="displayName",
                studio_name="studioName",
                user_role_arn="userRoleArn",
            
                # the properties below are optional
                studio_encryption_configuration=nimblestudio.CfnStudio.StudioEncryptionConfigurationProperty(
                    key_type="keyType",
            
                    # the properties below are optional
                    key_arn="keyArn"
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9695157240e3b6bf507b20f69766263178b738d876c9af5d3a53a4125c026be1)
            check_type(argname="argument admin_role_arn", value=admin_role_arn, expected_type=type_hints["admin_role_arn"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument studio_name", value=studio_name, expected_type=type_hints["studio_name"])
            check_type(argname="argument user_role_arn", value=user_role_arn, expected_type=type_hints["user_role_arn"])
            check_type(argname="argument studio_encryption_configuration", value=studio_encryption_configuration, expected_type=type_hints["studio_encryption_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_role_arn": admin_role_arn,
            "display_name": display_name,
            "studio_name": studio_name,
            "user_role_arn": user_role_arn,
        }
        if studio_encryption_configuration is not None:
            self._values["studio_encryption_configuration"] = studio_encryption_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def admin_role_arn(self) -> builtins.str:
        '''The IAM role that studio admins assume when logging in to the Nimble Studio portal.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-adminrolearn
        '''
        result = self._values.get("admin_role_arn")
        assert result is not None, "Required property 'admin_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> builtins.str:
        '''A friendly name for the studio.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-displayname
        '''
        result = self._values.get("display_name")
        assert result is not None, "Required property 'display_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def studio_name(self) -> builtins.str:
        '''The name of the studio, as included in the URL when accessing it in the Nimble Studio portal.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-studioname
        '''
        result = self._values.get("studio_name")
        assert result is not None, "Required property 'studio_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def user_role_arn(self) -> builtins.str:
        '''The IAM role that studio users assume when logging in to the Nimble Studio portal.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-userrolearn
        '''
        result = self._values.get("user_role_arn")
        assert result is not None, "Required property 'user_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def studio_encryption_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStudio.StudioEncryptionConfigurationProperty]]:
        '''Configuration of the encryption method that is used for the studio.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-studioencryptionconfiguration
        '''
        result = self._values.get("studio_encryption_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStudio.StudioEncryptionConfigurationProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-nimblestudio-studio.html#cfn-nimblestudio-studio-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnStudioProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnLaunchProfile",
    "CfnLaunchProfileProps",
    "CfnStreamingImage",
    "CfnStreamingImageProps",
    "CfnStudio",
    "CfnStudioComponent",
    "CfnStudioComponentProps",
    "CfnStudioProps",
]

publication.publish()

def _typecheckingstub__4d706b82a7a91577cd4b6a4dc0f563d3830fc7adf7ae6306064928adfbd60c93(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    ec2_subnet_ids: typing.Sequence[builtins.str],
    launch_profile_protocol_versions: typing.Sequence[builtins.str],
    name: builtins.str,
    stream_configuration: typing.Union[typing.Union[CfnLaunchProfile.StreamConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    studio_component_ids: typing.Sequence[builtins.str],
    studio_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b281c4576432fdf56a0cdb4e7eccb10886b20a2e9771a11b0fe20a20a9db994f(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad1d5b2d8f88a48733ff3916d4b74abd89513f8916d26ce04e84cbf00d92e404(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__989ae23e71b803c8e5d7f1d02a1c5be61b93f14d8687f593ff04dc8a0885c625(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7d9297fe6bb2ece9c002f35ee642260336e5b3634e8bffa8d77ea966ce0ec0(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a4bf5eea26dff69b3b5b3431a5052fee9b7660bd369cbd520f1091f5ac03950(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab59aca4b1f94ee78095a524dbd42e154a5a2df26c71551e163f7bd3c53764a5(
    value: typing.Union[CfnLaunchProfile.StreamConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__046493ed4963566972420336ab11b4dc00df1adc22ac47774c2870a2b11f80c9(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a43ec03580b10205db0e2ff7c8d4d728d37cc06c9bcc54f697700699480acfc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f54330e3fad8cf4f1aa82b625a6a8f032f2acae66d60c2981ab40618170b52d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c27e0247a6b4dedb1fd0283836ff19245e67a73abdfdacecd630ef2fd4f978fa(
    *,
    clipboard_mode: builtins.str,
    ec2_instance_types: typing.Sequence[builtins.str],
    streaming_image_ids: typing.Sequence[builtins.str],
    automatic_termination_mode: typing.Optional[builtins.str] = None,
    max_session_length_in_minutes: typing.Optional[jsii.Number] = None,
    max_stopped_session_length_in_minutes: typing.Optional[jsii.Number] = None,
    session_persistence_mode: typing.Optional[builtins.str] = None,
    session_storage: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLaunchProfile.StreamConfigurationSessionStorageProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    volume_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLaunchProfile.VolumeConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd44924c51f708c535c68c35760db8e4f08965b1aabe98a16a8a37acb955fba8(
    *,
    mode: typing.Sequence[builtins.str],
    root: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLaunchProfile.StreamingSessionStorageRootProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e80f915f75434409c047ae00ed2529f3e5014f688f5003fb98f42d7acb79554(
    *,
    linux: typing.Optional[builtins.str] = None,
    windows: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab1af60c683c69aa0e66077f0cfc6e4d4a01fb6a939adfa3ce827d23bdc2ee4e(
    *,
    iops: typing.Optional[jsii.Number] = None,
    size: typing.Optional[jsii.Number] = None,
    throughput: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68420745cc9ebe00a6bd75134a3d6120500b0d96caba0aa41ddf4e042f83df6e(
    *,
    ec2_subnet_ids: typing.Sequence[builtins.str],
    launch_profile_protocol_versions: typing.Sequence[builtins.str],
    name: builtins.str,
    stream_configuration: typing.Union[typing.Union[CfnLaunchProfile.StreamConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    studio_component_ids: typing.Sequence[builtins.str],
    studio_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__129bcb55764199a2e00737a05265b615b8a638197429620f4d5e2a6603005221(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    ec2_image_id: builtins.str,
    name: builtins.str,
    studio_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9808f7a09ec5aaa95181195b6570a04cc3aceb37fd1f27f5fe7d7c553df7778(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a173c2ea5a6add1b80e6dbf60fbdae6265204dd4f9b295f91e79979d1408e311(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1cfc1fb57d8ece4e26fee507bcb2e0ca87e59c0f6683c256e76c458221fb21d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ede13a87b51265b8ccfba2a79ff7f225815a93b6c2f046041861314c830dcf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c45f9d0cba20af393b3ccac3e2ae65bf3b1c270dd712e34941035069c362df0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__560ad2d07af6ee660b511f5e13cdf70eb488125410d958a74110039159fa7462(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2c112749720dc22b211c3ae3bc413ac276cb62bd422e239dd7605d4aebe1445(
    *,
    key_type: builtins.str,
    key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a45b9f4ccb3fed6e2352a60c283856d49fe5939f7d668c114362718721b2c762(
    *,
    ec2_image_id: builtins.str,
    name: builtins.str,
    studio_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90d4c4a93bf43d8cad8646079a6db65776199e513ccb3ac4a462da0c319a522e(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    admin_role_arn: builtins.str,
    display_name: builtins.str,
    studio_name: builtins.str,
    user_role_arn: builtins.str,
    studio_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStudio.StudioEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8ae356054a13f377e56d0acc1c2fb15289817fffa6c1d730a75e1174031c60e(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec25845a60c2ae8080cf4128b541171eb07373c48040ec0e63a91cdbc5553953(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e862a04070bc9123b253fed701bcb720a1ad533998d15ee16c90f8dfe761287c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4cb73b22ed94b3610e3b8a19162f859a34d32315187162dec2ba760a061ca82(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afd7fc3e2d7714b1c70b114b7f41ba099d32ac7cf6aafea0938d0b5a205af0ff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7507d2abad38e6bb3cf4248a440e64eab7890005342ab7f747139bb4fae3ecf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae28e2b022215876656ef6d565dff4b388ce4e5b845c7a0f7053eabfd2a0e3fc(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStudio.StudioEncryptionConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__151bc8d4ad08e04e58d0a0ecc1a979fc613a85fc1f3d2b31137859a84b9f1e74(
    *,
    key_type: builtins.str,
    key_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e3c0eb16d04afe47169ddb9a2fa82d6b006a1d3ed3e3da212e3238a07ad3626(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    studio_id: builtins.str,
    type: builtins.str,
    configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStudioComponent.StudioComponentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    ec2_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    initialization_scripts: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStudioComponent.StudioComponentInitializationScriptProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    script_parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStudioComponent.ScriptParameterKeyValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    subtype: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1c7ed2ebebd50254a1314b40c49f5286c5f3774e8de2a8d1c4e53a728c955a3(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50fd5b9d6806280cb1e48abf3995098f3c85825b03840cad70eb761fe9d4ced3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8415d32224058d2bb343ff394b3d04243d94f6796b27e295e2c1e2b86e659a87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__069fcdc083af7272e9a6f980f6f260985ef2f568a023128e586fb6aea26418a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e158b2dbd41296d887d193ab2cdaff33c2aa69ae68bb1fee966136566b9973(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__320e9dd79576eb41c8a341fec73cf6746aa6e0f7561271e2606dd4751f77f5fc(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStudioComponent.StudioComponentConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a10b7a0d7e029f35fc0fba06ad63b68890e07cc77691ae4093af86b92fd3b1f4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a24d585026939a006d5e9fcfffac490028a542729cdf34fe6f42573adaa4a6b(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c95f9b38b6e1514c87ae00a5beaafc01971a81098366d3e9acf0331635232ede(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStudioComponent.StudioComponentInitializationScriptProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e921e6fda58b2a48f40d8279270eb15322a0546640442433f17ca177c4bbb98(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnStudioComponent.ScriptParameterKeyValueProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d6310c8c115eea45e5a9017a06976d07404bc8ddb7a8be74577762ecad5d0f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b875f54a611b59e7df903b01e6b986501f90ce1958e7dcd23fbd220f2cffb993(
    *,
    name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a0b3cde54cba5bac452a8c40a593708fc40133d88c0769d404dc1cde4bc4d0c(
    *,
    computer_attributes: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStudioComponent.ActiveDirectoryComputerAttributeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    directory_id: typing.Optional[builtins.str] = None,
    organizational_unit_distinguished_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0e9d6e0b80f05807a7bbd8ffc59d0b9cb16bd374ca0f2b27be522aa05c0c62e(
    *,
    active_directory_user: typing.Optional[builtins.str] = None,
    endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c8b84605ea5ade2ab06d5496a764b61d7bd2d5a1f3940a7bc53273918d2a336(
    *,
    endpoint: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__781146a9f5a1a93e08c1052f807c5b5057ec43b8e68c56edefaaf2bb9527e04b(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42b99b4bc908fa99efb7f34ea662d3125db2ac9186c6229b314b583cfd7894be(
    *,
    endpoint: typing.Optional[builtins.str] = None,
    file_system_id: typing.Optional[builtins.str] = None,
    linux_mount_point: typing.Optional[builtins.str] = None,
    share_name: typing.Optional[builtins.str] = None,
    windows_mount_drive: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b067c27972287b8a8943fd79e6becb04b7f27f91d2172d88c6ec70b52a02eeb8(
    *,
    active_directory_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStudioComponent.ActiveDirectoryConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    compute_farm_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStudioComponent.ComputeFarmConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    license_service_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStudioComponent.LicenseServiceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    shared_file_system_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStudioComponent.SharedFileSystemConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__273c2d59ae7e1c5c919f75c2bc128f61cebebf9de0e1619a4a31eb7661a1b875(
    *,
    launch_profile_protocol_version: typing.Optional[builtins.str] = None,
    platform: typing.Optional[builtins.str] = None,
    run_context: typing.Optional[builtins.str] = None,
    script: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a906fc8dd291692c93929e40d19adab6e31e32a079bd5f5b0b291c01e3698de9(
    *,
    name: builtins.str,
    studio_id: builtins.str,
    type: builtins.str,
    configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStudioComponent.StudioComponentConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    ec2_security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    initialization_scripts: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStudioComponent.StudioComponentInitializationScriptProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    script_parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStudioComponent.ScriptParameterKeyValueProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    subtype: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9695157240e3b6bf507b20f69766263178b738d876c9af5d3a53a4125c026be1(
    *,
    admin_role_arn: builtins.str,
    display_name: builtins.str,
    studio_name: builtins.str,
    user_role_arn: builtins.str,
    studio_encryption_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnStudio.StudioEncryptionConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
