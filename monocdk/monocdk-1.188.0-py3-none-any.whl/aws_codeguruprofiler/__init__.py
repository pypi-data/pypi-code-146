'''
# AWS::CodeGuruProfiler Construct Library

Amazon CodeGuru Profiler collects runtime performance data from your live applications, and provides recommendations that can help you fine-tune your application performance.

## Installation

Import to your project:

```python
import monocdk as codeguruprofiler
```

## Basic usage

Here's how to setup a profiling group and give your compute role permissions to publish to the profiling group to the profiling agent can publish profiling information:

```python
# The execution role of your application that publishes to the ProfilingGroup via CodeGuru Profiler Profiling Agent. (the following is merely an example)
publish_app_role = iam.Role(self, "PublishAppRole",
    assumed_by=iam.AccountRootPrincipal()
)

profiling_group = codeguruprofiler.ProfilingGroup(self, "MyProfilingGroup")
profiling_group.grant_publish(publish_app_role)
```

## Compute Platform configuration

Code Guru Profiler supports multiple compute environments.
They can be configured when creating a Profiling Group by using the `computePlatform` property:

```python
profiling_group = codeguruprofiler.ProfilingGroup(self, "MyProfilingGroup",
    compute_platform=codeguruprofiler.ComputePlatform.AWS_LAMBDA
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

from .._jsii import *

import constructs as _constructs_77d1e7e8
from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_iam import Grant as _Grant_bcb5eae7, IGrantable as _IGrantable_4c5a91d1


@jsii.implements(_IInspectable_82c04a63)
class CfnProfilingGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codeguruprofiler.CfnProfilingGroup",
):
    '''A CloudFormation ``AWS::CodeGuruProfiler::ProfilingGroup``.

    Creates a profiling group.

    :cloudformationResource: AWS::CodeGuruProfiler::ProfilingGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_codeguruprofiler as codeguruprofiler
        
        # agent_permissions: Any
        
        cfn_profiling_group = codeguruprofiler.CfnProfilingGroup(self, "MyCfnProfilingGroup",
            profiling_group_name="profilingGroupName",
        
            # the properties below are optional
            agent_permissions=agent_permissions,
            anomaly_detection_notification_configuration=[codeguruprofiler.CfnProfilingGroup.ChannelProperty(
                channel_uri="channelUri",
        
                # the properties below are optional
                channel_id="channelId"
            )],
            compute_platform="computePlatform",
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
        profiling_group_name: builtins.str,
        agent_permissions: typing.Any = None,
        anomaly_detection_notification_configuration: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnProfilingGroup.ChannelProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        compute_platform: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::CodeGuruProfiler::ProfilingGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param profiling_group_name: The name of the profiling group.
        :param agent_permissions: The agent permissions attached to this profiling group. This action group grants ``ConfigureAgent`` and ``PostAgentProfile`` permissions to perform actions required by the profiling agent. The Json consists of key ``Principals`` . *Principals* : A list of string ARNs for the roles and users you want to grant access to the profiling group. Wildcards are not supported in the ARNs. You are allowed to provide up to 50 ARNs. An empty list is not permitted. This is a required key. For more information, see `Resource-based policies in CodeGuru Profiler <https://docs.aws.amazon.com/codeguru/latest/profiler-ug/resource-based-policies.html>`_ in the *Amazon CodeGuru Profiler user guide* , `ConfigureAgent <https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_ConfigureAgent.html>`_ , and `PostAgentProfile <https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_PostAgentProfile.html>`_ .
        :param anomaly_detection_notification_configuration: Adds anomaly notifications for a profiling group.
        :param compute_platform: The compute platform of the profiling group. Use ``AWSLambda`` if your application runs on AWS Lambda. Use ``Default`` if your application runs on a compute platform that is not AWS Lambda , such an Amazon EC2 instance, an on-premises server, or a different platform. If not specified, ``Default`` is used. This property is immutable.
        :param tags: A list of tags to add to the created profiling group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c147f15afcfd40ccf0c7aa3e75ac50f1434ee102c4251cd3029eef4e0a836265)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnProfilingGroupProps(
            profiling_group_name=profiling_group_name,
            agent_permissions=agent_permissions,
            anomaly_detection_notification_configuration=anomaly_detection_notification_configuration,
            compute_platform=compute_platform,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61a87438de57d97cfd0de7c94f26acdfbf5c06b515b599c4550c3a08e5685547)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b730c469c26ceb8ebce53409aba10d990ef7045bf7dff2c3e29d320460dc4876)
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
        '''The full Amazon Resource Name (ARN) for that profiling group.

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
        '''A list of tags to add to the created profiling group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="agentPermissions")
    def agent_permissions(self) -> typing.Any:
        '''The agent permissions attached to this profiling group.

        This action group grants ``ConfigureAgent`` and ``PostAgentProfile`` permissions to perform actions required by the profiling agent. The Json consists of key ``Principals`` .

        *Principals* : A list of string ARNs for the roles and users you want to grant access to the profiling group. Wildcards are not supported in the ARNs. You are allowed to provide up to 50 ARNs. An empty list is not permitted. This is a required key.

        For more information, see `Resource-based policies in CodeGuru Profiler <https://docs.aws.amazon.com/codeguru/latest/profiler-ug/resource-based-policies.html>`_ in the *Amazon CodeGuru Profiler user guide* , `ConfigureAgent <https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_ConfigureAgent.html>`_ , and `PostAgentProfile <https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_PostAgentProfile.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-agentpermissions
        '''
        return typing.cast(typing.Any, jsii.get(self, "agentPermissions"))

    @agent_permissions.setter
    def agent_permissions(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84cc55f74d60e23db9bd2320149a9cfb7cf94ee9218da0a4f3f4824ed88e07bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "agentPermissions", value)

    @builtins.property
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> builtins.str:
        '''The name of the profiling group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-profilinggroupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "profilingGroupName"))

    @profiling_group_name.setter
    def profiling_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a201710be2f4884bec93ab68a4bc0cca94491d7e54c33e19f37b72b700f03910)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "profilingGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="anomalyDetectionNotificationConfiguration")
    def anomaly_detection_notification_configuration(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnProfilingGroup.ChannelProperty", _IResolvable_a771d0ef]]]]:
        '''Adds anomaly notifications for a profiling group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-anomalydetectionnotificationconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnProfilingGroup.ChannelProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "anomalyDetectionNotificationConfiguration"))

    @anomaly_detection_notification_configuration.setter
    def anomaly_detection_notification_configuration(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnProfilingGroup.ChannelProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fe2ee5dad4c228b7578ca5d03f3c76cd906a4bd006eaa3ceb28598988205e83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "anomalyDetectionNotificationConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="computePlatform")
    def compute_platform(self) -> typing.Optional[builtins.str]:
        '''The compute platform of the profiling group.

        Use ``AWSLambda`` if your application runs on AWS Lambda. Use ``Default`` if your application runs on a compute platform that is not AWS Lambda , such an Amazon EC2 instance, an on-premises server, or a different platform. If not specified, ``Default`` is used. This property is immutable.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-computeplatform
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "computePlatform"))

    @compute_platform.setter
    def compute_platform(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8dfa43532e1980fecaeec009d59d2cd3978289134199ed517c2d8239569dd3f7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "computePlatform", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_codeguruprofiler.CfnProfilingGroup.AgentPermissionsProperty",
        jsii_struct_bases=[],
        name_mapping={"principals": "principals"},
    )
    class AgentPermissionsProperty:
        def __init__(self, *, principals: typing.Sequence[builtins.str]) -> None:
            '''
            :param principals: ``CfnProfilingGroup.AgentPermissionsProperty.Principals``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeguruprofiler-profilinggroup-agentpermissions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_codeguruprofiler as codeguruprofiler
                
                agent_permissions_property = codeguruprofiler.CfnProfilingGroup.AgentPermissionsProperty(
                    principals=["principals"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e054255d739c53c8b081417b87ef9d2ca58659d5a5af88f27a2d383a339bf6fb)
                check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "principals": principals,
            }

        @builtins.property
        def principals(self) -> typing.List[builtins.str]:
            '''``CfnProfilingGroup.AgentPermissionsProperty.Principals``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeguruprofiler-profilinggroup-agentpermissions.html#cfn-codeguruprofiler-profilinggroup-agentpermissions-principals
            '''
            result = self._values.get("principals")
            assert result is not None, "Required property 'principals' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AgentPermissionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_codeguruprofiler.CfnProfilingGroup.ChannelProperty",
        jsii_struct_bases=[],
        name_mapping={"channel_uri": "channelUri", "channel_id": "channelId"},
    )
    class ChannelProperty:
        def __init__(
            self,
            *,
            channel_uri: builtins.str,
            channel_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Notification medium for users to get alerted for events that occur in application profile.

            We support SNS topic as a notification channel.

            :param channel_uri: The channel URI.
            :param channel_id: The channel ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeguruprofiler-profilinggroup-channel.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_codeguruprofiler as codeguruprofiler
                
                channel_property = codeguruprofiler.CfnProfilingGroup.ChannelProperty(
                    channel_uri="channelUri",
                
                    # the properties below are optional
                    channel_id="channelId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a121df9637198a172138cba1b8ad825df4aeb7df6545d8f12fa2669ccc633f12)
                check_type(argname="argument channel_uri", value=channel_uri, expected_type=type_hints["channel_uri"])
                check_type(argname="argument channel_id", value=channel_id, expected_type=type_hints["channel_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "channel_uri": channel_uri,
            }
            if channel_id is not None:
                self._values["channel_id"] = channel_id

        @builtins.property
        def channel_uri(self) -> builtins.str:
            '''The channel URI.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeguruprofiler-profilinggroup-channel.html#cfn-codeguruprofiler-profilinggroup-channel-channeluri
            '''
            result = self._values.get("channel_uri")
            assert result is not None, "Required property 'channel_uri' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def channel_id(self) -> typing.Optional[builtins.str]:
            '''The channel ID.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codeguruprofiler-profilinggroup-channel.html#cfn-codeguruprofiler-profilinggroup-channel-channelid
            '''
            result = self._values.get("channel_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ChannelProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_codeguruprofiler.CfnProfilingGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "profiling_group_name": "profilingGroupName",
        "agent_permissions": "agentPermissions",
        "anomaly_detection_notification_configuration": "anomalyDetectionNotificationConfiguration",
        "compute_platform": "computePlatform",
        "tags": "tags",
    },
)
class CfnProfilingGroupProps:
    def __init__(
        self,
        *,
        profiling_group_name: builtins.str,
        agent_permissions: typing.Any = None,
        anomaly_detection_notification_configuration: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnProfilingGroup.ChannelProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        compute_platform: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnProfilingGroup``.

        :param profiling_group_name: The name of the profiling group.
        :param agent_permissions: The agent permissions attached to this profiling group. This action group grants ``ConfigureAgent`` and ``PostAgentProfile`` permissions to perform actions required by the profiling agent. The Json consists of key ``Principals`` . *Principals* : A list of string ARNs for the roles and users you want to grant access to the profiling group. Wildcards are not supported in the ARNs. You are allowed to provide up to 50 ARNs. An empty list is not permitted. This is a required key. For more information, see `Resource-based policies in CodeGuru Profiler <https://docs.aws.amazon.com/codeguru/latest/profiler-ug/resource-based-policies.html>`_ in the *Amazon CodeGuru Profiler user guide* , `ConfigureAgent <https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_ConfigureAgent.html>`_ , and `PostAgentProfile <https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_PostAgentProfile.html>`_ .
        :param anomaly_detection_notification_configuration: Adds anomaly notifications for a profiling group.
        :param compute_platform: The compute platform of the profiling group. Use ``AWSLambda`` if your application runs on AWS Lambda. Use ``Default`` if your application runs on a compute platform that is not AWS Lambda , such an Amazon EC2 instance, an on-premises server, or a different platform. If not specified, ``Default`` is used. This property is immutable.
        :param tags: A list of tags to add to the created profiling group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codeguruprofiler as codeguruprofiler
            
            # agent_permissions: Any
            
            cfn_profiling_group_props = codeguruprofiler.CfnProfilingGroupProps(
                profiling_group_name="profilingGroupName",
            
                # the properties below are optional
                agent_permissions=agent_permissions,
                anomaly_detection_notification_configuration=[codeguruprofiler.CfnProfilingGroup.ChannelProperty(
                    channel_uri="channelUri",
            
                    # the properties below are optional
                    channel_id="channelId"
                )],
                compute_platform="computePlatform",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be81e62e03c44d7f55ee84a526c4d5efc09f0b896792679dfca84de9719fad4a)
            check_type(argname="argument profiling_group_name", value=profiling_group_name, expected_type=type_hints["profiling_group_name"])
            check_type(argname="argument agent_permissions", value=agent_permissions, expected_type=type_hints["agent_permissions"])
            check_type(argname="argument anomaly_detection_notification_configuration", value=anomaly_detection_notification_configuration, expected_type=type_hints["anomaly_detection_notification_configuration"])
            check_type(argname="argument compute_platform", value=compute_platform, expected_type=type_hints["compute_platform"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "profiling_group_name": profiling_group_name,
        }
        if agent_permissions is not None:
            self._values["agent_permissions"] = agent_permissions
        if anomaly_detection_notification_configuration is not None:
            self._values["anomaly_detection_notification_configuration"] = anomaly_detection_notification_configuration
        if compute_platform is not None:
            self._values["compute_platform"] = compute_platform
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def profiling_group_name(self) -> builtins.str:
        '''The name of the profiling group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-profilinggroupname
        '''
        result = self._values.get("profiling_group_name")
        assert result is not None, "Required property 'profiling_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def agent_permissions(self) -> typing.Any:
        '''The agent permissions attached to this profiling group.

        This action group grants ``ConfigureAgent`` and ``PostAgentProfile`` permissions to perform actions required by the profiling agent. The Json consists of key ``Principals`` .

        *Principals* : A list of string ARNs for the roles and users you want to grant access to the profiling group. Wildcards are not supported in the ARNs. You are allowed to provide up to 50 ARNs. An empty list is not permitted. This is a required key.

        For more information, see `Resource-based policies in CodeGuru Profiler <https://docs.aws.amazon.com/codeguru/latest/profiler-ug/resource-based-policies.html>`_ in the *Amazon CodeGuru Profiler user guide* , `ConfigureAgent <https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_ConfigureAgent.html>`_ , and `PostAgentProfile <https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_PostAgentProfile.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-agentpermissions
        '''
        result = self._values.get("agent_permissions")
        return typing.cast(typing.Any, result)

    @builtins.property
    def anomaly_detection_notification_configuration(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnProfilingGroup.ChannelProperty, _IResolvable_a771d0ef]]]]:
        '''Adds anomaly notifications for a profiling group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-anomalydetectionnotificationconfiguration
        '''
        result = self._values.get("anomaly_detection_notification_configuration")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnProfilingGroup.ChannelProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def compute_platform(self) -> typing.Optional[builtins.str]:
        '''The compute platform of the profiling group.

        Use ``AWSLambda`` if your application runs on AWS Lambda. Use ``Default`` if your application runs on a compute platform that is not AWS Lambda , such an Amazon EC2 instance, an on-premises server, or a different platform. If not specified, ``Default`` is used. This property is immutable.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-computeplatform
        '''
        result = self._values.get("compute_platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of tags to add to the created profiling group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codeguruprofiler-profilinggroup.html#cfn-codeguruprofiler-profilinggroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnProfilingGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_codeguruprofiler.ComputePlatform")
class ComputePlatform(enum.Enum):
    '''(experimental) The compute platform of the profiling group.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        profiling_group = codeguruprofiler.ProfilingGroup(self, "MyProfilingGroup",
            compute_platform=codeguruprofiler.ComputePlatform.AWS_LAMBDA
        )
    '''

    AWS_LAMBDA = "AWS_LAMBDA"
    '''(experimental) Use AWS_LAMBDA if your application runs on AWS Lambda.

    :stability: experimental
    '''
    DEFAULT = "DEFAULT"
    '''(experimental) Use Default if your application runs on a compute platform that is not AWS Lambda, such an Amazon EC2 instance, an on-premises server, or a different platform.

    :stability: experimental
    '''


@jsii.interface(jsii_type="monocdk.aws_codeguruprofiler.IProfilingGroup")
class IProfilingGroup(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) IResource represents a Profiling Group.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> builtins.str:
        '''(experimental) A name for the profiling group.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant access to publish profiling information to the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:ConfigureAgent
        - codeguru-profiler:PostAgentProfile

        :param grantee: Principal to grant publish rights to.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant access to read profiling information from the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:GetProfile
        - codeguru-profiler:DescribeProfilingGroup

        :param grantee: Principal to grant read rights to.

        :stability: experimental
        '''
        ...


class _IProfilingGroupProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) IResource represents a Profiling Group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_codeguruprofiler.IProfilingGroup"

    @builtins.property
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> builtins.str:
        '''(experimental) A name for the profiling group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "profilingGroupName"))

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant access to publish profiling information to the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:ConfigureAgent
        - codeguru-profiler:PostAgentProfile

        :param grantee: Principal to grant publish rights to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8834739b5ea420371487cf0f03caf56c32948541887a16fde9df3651c3d60c09)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPublish", [grantee]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant access to read profiling information from the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:GetProfile
        - codeguru-profiler:DescribeProfilingGroup

        :param grantee: Principal to grant read rights to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38ca6c84101cd710d909419b5a367c0b8ed7378c52e464444abc61a1e6224105)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantRead", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IProfilingGroup).__jsii_proxy_class__ = lambda : _IProfilingGroupProxy


@jsii.implements(IProfilingGroup)
class ProfilingGroup(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_codeguruprofiler.ProfilingGroup",
):
    '''(experimental) A new Profiling Group.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # The execution role of your application that publishes to the ProfilingGroup via CodeGuru Profiler Profiling Agent. (the following is merely an example)
        publish_app_role = iam.Role(self, "PublishAppRole",
            assumed_by=iam.AccountRootPrincipal()
        )
        
        profiling_group = codeguruprofiler.ProfilingGroup(self, "MyProfilingGroup")
        profiling_group.grant_publish(publish_app_role)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        compute_platform: typing.Optional[ComputePlatform] = None,
        profiling_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param compute_platform: (experimental) The compute platform of the profiling group. Default: ComputePlatform.DEFAULT
        :param profiling_group_name: (experimental) A name for the profiling group. Default: - automatically generated name.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c003743a12aa0af5578e84a26b8eda3544e8c51ddb5d15706efb50891883dcf9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ProfilingGroupProps(
            compute_platform=compute_platform,
            profiling_group_name=profiling_group_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromProfilingGroupArn")
    @builtins.classmethod
    def from_profiling_group_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        profiling_group_arn: builtins.str,
    ) -> IProfilingGroup:
        '''(experimental) Import an existing Profiling Group provided an ARN.

        :param scope: The parent creating construct.
        :param id: The construct's name.
        :param profiling_group_arn: Profiling Group ARN.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf3c6101a8372f3c5c6e4c8ab8ba224e1072d8cfc76421703ce9143f4466e283)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument profiling_group_arn", value=profiling_group_arn, expected_type=type_hints["profiling_group_arn"])
        return typing.cast(IProfilingGroup, jsii.sinvoke(cls, "fromProfilingGroupArn", [scope, id, profiling_group_arn]))

    @jsii.member(jsii_name="fromProfilingGroupName")
    @builtins.classmethod
    def from_profiling_group_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        profiling_group_name: builtins.str,
    ) -> IProfilingGroup:
        '''(experimental) Import an existing Profiling Group provided a Profiling Group Name.

        :param scope: The parent creating construct.
        :param id: The construct's name.
        :param profiling_group_name: Profiling Group Name.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f906c2116c11d76a8436f713cfd07d160c1f87be1b8fd189a54ba0ae20a0ff9d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument profiling_group_name", value=profiling_group_name, expected_type=type_hints["profiling_group_name"])
        return typing.cast(IProfilingGroup, jsii.sinvoke(cls, "fromProfilingGroupName", [scope, id, profiling_group_name]))

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant access to publish profiling information to the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:ConfigureAgent
        - codeguru-profiler:PostAgentProfile

        :param grantee: Principal to grant publish rights to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8820b833f1d3304aced83e7df51f3e5f48ff6ab79fb01e815adfb1511521b15d)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantPublish", [grantee]))

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant access to read profiling information from the Profiling Group to the given identity.

        This will grant the following permissions:

        - codeguru-profiler:GetProfile
        - codeguru-profiler:DescribeProfilingGroup

        :param grantee: Principal to grant read rights to.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f1c2cf85b2b4a3a4ca39fdb466d8be2308d30db79334a91ead763b0023471bf6)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantRead", [grantee]))

    @builtins.property
    @jsii.member(jsii_name="profilingGroupArn")
    def profiling_group_arn(self) -> builtins.str:
        '''(experimental) The ARN of the Profiling Group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "profilingGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="profilingGroupName")
    def profiling_group_name(self) -> builtins.str:
        '''(experimental) The name of the Profiling Group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "profilingGroupName"))


@jsii.data_type(
    jsii_type="monocdk.aws_codeguruprofiler.ProfilingGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "compute_platform": "computePlatform",
        "profiling_group_name": "profilingGroupName",
    },
)
class ProfilingGroupProps:
    def __init__(
        self,
        *,
        compute_platform: typing.Optional[ComputePlatform] = None,
        profiling_group_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for creating a new Profiling Group.

        :param compute_platform: (experimental) The compute platform of the profiling group. Default: ComputePlatform.DEFAULT
        :param profiling_group_name: (experimental) A name for the profiling group. Default: - automatically generated name.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            profiling_group = codeguruprofiler.ProfilingGroup(self, "MyProfilingGroup",
                compute_platform=codeguruprofiler.ComputePlatform.AWS_LAMBDA
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5af9828488b902ad2f28a9def533650611b0c99188afb653312375e1292deaf)
            check_type(argname="argument compute_platform", value=compute_platform, expected_type=type_hints["compute_platform"])
            check_type(argname="argument profiling_group_name", value=profiling_group_name, expected_type=type_hints["profiling_group_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if compute_platform is not None:
            self._values["compute_platform"] = compute_platform
        if profiling_group_name is not None:
            self._values["profiling_group_name"] = profiling_group_name

    @builtins.property
    def compute_platform(self) -> typing.Optional[ComputePlatform]:
        '''(experimental) The compute platform of the profiling group.

        :default: ComputePlatform.DEFAULT

        :stability: experimental
        '''
        result = self._values.get("compute_platform")
        return typing.cast(typing.Optional[ComputePlatform], result)

    @builtins.property
    def profiling_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the profiling group.

        :default: - automatically generated name.

        :stability: experimental
        '''
        result = self._values.get("profiling_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProfilingGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnProfilingGroup",
    "CfnProfilingGroupProps",
    "ComputePlatform",
    "IProfilingGroup",
    "ProfilingGroup",
    "ProfilingGroupProps",
]

publication.publish()

def _typecheckingstub__c147f15afcfd40ccf0c7aa3e75ac50f1434ee102c4251cd3029eef4e0a836265(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    profiling_group_name: builtins.str,
    agent_permissions: typing.Any = None,
    anomaly_detection_notification_configuration: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnProfilingGroup.ChannelProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    compute_platform: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61a87438de57d97cfd0de7c94f26acdfbf5c06b515b599c4550c3a08e5685547(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b730c469c26ceb8ebce53409aba10d990ef7045bf7dff2c3e29d320460dc4876(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84cc55f74d60e23db9bd2320149a9cfb7cf94ee9218da0a4f3f4824ed88e07bc(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a201710be2f4884bec93ab68a4bc0cca94491d7e54c33e19f37b72b700f03910(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fe2ee5dad4c228b7578ca5d03f3c76cd906a4bd006eaa3ceb28598988205e83(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnProfilingGroup.ChannelProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8dfa43532e1980fecaeec009d59d2cd3978289134199ed517c2d8239569dd3f7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e054255d739c53c8b081417b87ef9d2ca58659d5a5af88f27a2d383a339bf6fb(
    *,
    principals: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a121df9637198a172138cba1b8ad825df4aeb7df6545d8f12fa2669ccc633f12(
    *,
    channel_uri: builtins.str,
    channel_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be81e62e03c44d7f55ee84a526c4d5efc09f0b896792679dfca84de9719fad4a(
    *,
    profiling_group_name: builtins.str,
    agent_permissions: typing.Any = None,
    anomaly_detection_notification_configuration: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnProfilingGroup.ChannelProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    compute_platform: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8834739b5ea420371487cf0f03caf56c32948541887a16fde9df3651c3d60c09(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ca6c84101cd710d909419b5a367c0b8ed7378c52e464444abc61a1e6224105(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c003743a12aa0af5578e84a26b8eda3544e8c51ddb5d15706efb50891883dcf9(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    compute_platform: typing.Optional[ComputePlatform] = None,
    profiling_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf3c6101a8372f3c5c6e4c8ab8ba224e1072d8cfc76421703ce9143f4466e283(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    profiling_group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f906c2116c11d76a8436f713cfd07d160c1f87be1b8fd189a54ba0ae20a0ff9d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    profiling_group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8820b833f1d3304aced83e7df51f3e5f48ff6ab79fb01e815adfb1511521b15d(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1c2cf85b2b4a3a4ca39fdb466d8be2308d30db79334a91ead763b0023471bf6(
    grantee: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5af9828488b902ad2f28a9def533650611b0c99188afb653312375e1292deaf(
    *,
    compute_platform: typing.Optional[ComputePlatform] = None,
    profiling_group_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
