'''
# AWS::EMRServerless Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_emrserverless as emrserverless
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for EMRServerless construct libraries](https://constructs.dev/search?q=emrserverless)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::EMRServerless resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_EMRServerless.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::EMRServerless](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_EMRServerless.html).

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
class CfnApplication(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-emrserverless.CfnApplication",
):
    '''A CloudFormation ``AWS::EMRServerless::Application``.

    The ``AWS::EMRServerless::Application`` resource specifies an EMR Serverless application. An application uses open source analytics frameworks to run jobs that process data. To create an application, you must specify the release version for the open source framework version you want to use and the type of application you want, such as Apache Spark or Apache Hive. After you create an application, you can submit data processing jobs or interactive requests to it.

    :cloudformationResource: AWS::EMRServerless::Application
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_emrserverless as emrserverless
        
        cfn_application = emrserverless.CfnApplication(self, "MyCfnApplication",
            release_label="releaseLabel",
            type="type",
        
            # the properties below are optional
            architecture="architecture",
            auto_start_configuration=emrserverless.CfnApplication.AutoStartConfigurationProperty(
                enabled=False
            ),
            auto_stop_configuration=emrserverless.CfnApplication.AutoStopConfigurationProperty(
                enabled=False,
                idle_timeout_minutes=123
            ),
            initial_capacity=[emrserverless.CfnApplication.InitialCapacityConfigKeyValuePairProperty(
                key="key",
                value=emrserverless.CfnApplication.InitialCapacityConfigProperty(
                    worker_configuration=emrserverless.CfnApplication.WorkerConfigurationProperty(
                        cpu="cpu",
                        memory="memory",
        
                        # the properties below are optional
                        disk="disk"
                    ),
                    worker_count=123
                )
            )],
            maximum_capacity=emrserverless.CfnApplication.MaximumAllowedResourcesProperty(
                cpu="cpu",
                memory="memory",
        
                # the properties below are optional
                disk="disk"
            ),
            name="name",
            network_configuration=emrserverless.CfnApplication.NetworkConfigurationProperty(
                security_group_ids=["securityGroupIds"],
                subnet_ids=["subnetIds"]
            ),
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
        release_label: builtins.str,
        type: builtins.str,
        architecture: typing.Optional[builtins.str] = None,
        auto_start_configuration: typing.Optional[typing.Union[typing.Union["CfnApplication.AutoStartConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        auto_stop_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApplication.AutoStopConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        initial_capacity: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApplication.InitialCapacityConfigKeyValuePairProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        maximum_capacity: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApplication.MaximumAllowedResourcesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        network_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApplication.NetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::EMRServerless::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param release_label: The EMR release version associated with the application. *Minimum* : 1 *Maximum* : 64 *Pattern* : ``^[A-Za-z0-9._/-]+$``
        :param type: The type of application, such as Spark or Hive.
        :param architecture: The CPU architecture type of the application. Allowed values: ``X86_64`` or ``ARM64``
        :param auto_start_configuration: The configuration for an application to automatically start on job submission.
        :param auto_stop_configuration: The configuration for an application to automatically stop after a certain amount of time being idle.
        :param initial_capacity: The initial capacity of the application.
        :param maximum_capacity: The maximum capacity of the application. This is cumulative across all workers at any given point in time during the lifespan of the application is created. No new resources will be created once any one of the defined limits is hit.
        :param name: The name of the application. *Minimum* : 1 *Maximum* : 64 *Pattern* : ``^[A-Za-z0-9._\\\\/#-]+$``
        :param network_configuration: The network configuration for customer VPC connectivity for the application.
        :param tags: The tags assigned to the application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c43e9a1cc87f8e9909f905993b5411b578cabe85440ca32c60c769e0544ffd6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationProps(
            release_label=release_label,
            type=type,
            architecture=architecture,
            auto_start_configuration=auto_start_configuration,
            auto_stop_configuration=auto_stop_configuration,
            initial_capacity=initial_capacity,
            maximum_capacity=maximum_capacity,
            name=name,
            network_configuration=network_configuration,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b000495631c615df24622de393225ab7b5ab2f2cd3d6c019cd77a544d2adbd0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f3089778c978d28e8eec7d7e5bf737e35f9f2c88b15c58aeef9fb9d3169a7091)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrApplicationId")
    def attr_application_id(self) -> builtins.str:
        '''The ID of the application, such as ``ab4rp1abcs8xz47n3x0example`` .

        :cloudformationAttribute: ApplicationId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrApplicationId"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the project.

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
        '''The tags assigned to the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="releaseLabel")
    def release_label(self) -> builtins.str:
        '''The EMR release version associated with the application.

        *Minimum* : 1

        *Maximum* : 64

        *Pattern* : ``^[A-Za-z0-9._/-]+$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-releaselabel
        '''
        return typing.cast(builtins.str, jsii.get(self, "releaseLabel"))

    @release_label.setter
    def release_label(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f040abf2796728145422ba345c7280e1882ca56a93798ec8d04578c424a0cf41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "releaseLabel", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of application, such as Spark or Hive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ffc6644afbddd2110977215737cb601db2a813b9fcb80e472d822e60cf473a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> typing.Optional[builtins.str]:
        '''The CPU architecture type of the application.

        Allowed values: ``X86_64`` or ``ARM64``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-architecture
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "architecture"))

    @architecture.setter
    def architecture(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__633c944ab002662272329cd2ab53054a421544659413787f2c0b2dad01aee3be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "architecture", value)

    @builtins.property
    @jsii.member(jsii_name="autoStartConfiguration")
    def auto_start_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnApplication.AutoStartConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]]:
        '''The configuration for an application to automatically start on job submission.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-autostartconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApplication.AutoStartConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "autoStartConfiguration"))

    @auto_start_configuration.setter
    def auto_start_configuration(
        self,
        value: typing.Optional[typing.Union["CfnApplication.AutoStartConfigurationProperty", _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcc92144333fa6a0918945f1a1c483c9c6e2cd93bb706c1b5e1dc0130a7aa0f3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoStartConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="autoStopConfiguration")
    def auto_stop_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.AutoStopConfigurationProperty"]]:
        '''The configuration for an application to automatically stop after a certain amount of time being idle.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-autostopconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.AutoStopConfigurationProperty"]], jsii.get(self, "autoStopConfiguration"))

    @auto_stop_configuration.setter
    def auto_stop_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.AutoStopConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c68631a69cf3bda8ae7d964e25b12e8e294697448d8197c2432b13028dbf9514)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoStopConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="initialCapacity")
    def initial_capacity(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.InitialCapacityConfigKeyValuePairProperty"]]]]:
        '''The initial capacity of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-initialcapacity
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.InitialCapacityConfigKeyValuePairProperty"]]]], jsii.get(self, "initialCapacity"))

    @initial_capacity.setter
    def initial_capacity(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.InitialCapacityConfigKeyValuePairProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7d6df0a17fbedc0853acda87e0b78a1f838a3ee10414fefd80337c94fbdd7f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "initialCapacity", value)

    @builtins.property
    @jsii.member(jsii_name="maximumCapacity")
    def maximum_capacity(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.MaximumAllowedResourcesProperty"]]:
        '''The maximum capacity of the application.

        This is cumulative across all workers at any given point in time during the lifespan of the application is created. No new resources will be created once any one of the defined limits is hit.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-maximumcapacity
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.MaximumAllowedResourcesProperty"]], jsii.get(self, "maximumCapacity"))

    @maximum_capacity.setter
    def maximum_capacity(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.MaximumAllowedResourcesProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb2f9c42f5dde30a69eb7dd3222f8ffae825b5c95d6840f00a654a977d2ad7d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maximumCapacity", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the application.

        *Minimum* : 1

        *Maximum* : 64

        *Pattern* : ``^[A-Za-z0-9._\\\\/#-]+$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30a71da96a2b3cf8fe63a539c2c4153d85504210e2a8dca8e70265eb40613c4d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="networkConfiguration")
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.NetworkConfigurationProperty"]]:
        '''The network configuration for customer VPC connectivity for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-networkconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.NetworkConfigurationProperty"]], jsii.get(self, "networkConfiguration"))

    @network_configuration.setter
    def network_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.NetworkConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6950254fbb841a6f83fe777bec8b833d5d15d1dafbd7515772ef993e38b80c5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-emrserverless.CfnApplication.AutoStartConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"enabled": "enabled"},
    )
    class AutoStartConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''The conﬁguration for an application to automatically start on job submission.

            :param enabled: Enables the application to automatically start on job submission. Defaults to true.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-autostartconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_emrserverless as emrserverless
                
                auto_start_configuration_property = emrserverless.CfnApplication.AutoStartConfigurationProperty(
                    enabled=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__18daf1a39548ff8ae0c6bc1d45bf6356180ec62b69a172e09a7b00829f244df3)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Enables the application to automatically start on job submission.

            Defaults to true.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-autostartconfiguration.html#cfn-emrserverless-application-autostartconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoStartConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-emrserverless.CfnApplication.AutoStopConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "idle_timeout_minutes": "idleTimeoutMinutes",
        },
    )
    class AutoStopConfigurationProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            idle_timeout_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The conﬁguration for an application to automatically stop after a certain amount of time being idle.

            :param enabled: Enables the application to automatically stop after a certain amount of time being idle. Defaults to true.
            :param idle_timeout_minutes: The amount of idle time in minutes after which your application will automatically stop. Defaults to 15 minutes. *Minimum* : 1 *Maximum* : 10080

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-autostopconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_emrserverless as emrserverless
                
                auto_stop_configuration_property = emrserverless.CfnApplication.AutoStopConfigurationProperty(
                    enabled=False,
                    idle_timeout_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__91e755663f779db4860da63be3bb8ccd650760952ccd79b6692ccada7ca574ee)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument idle_timeout_minutes", value=idle_timeout_minutes, expected_type=type_hints["idle_timeout_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if idle_timeout_minutes is not None:
                self._values["idle_timeout_minutes"] = idle_timeout_minutes

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Enables the application to automatically stop after a certain amount of time being idle.

            Defaults to true.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-autostopconfiguration.html#cfn-emrserverless-application-autostopconfiguration-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def idle_timeout_minutes(self) -> typing.Optional[jsii.Number]:
            '''The amount of idle time in minutes after which your application will automatically stop. Defaults to 15 minutes.

            *Minimum* : 1

            *Maximum* : 10080

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-autostopconfiguration.html#cfn-emrserverless-application-autostopconfiguration-idletimeoutminutes
            '''
            result = self._values.get("idle_timeout_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoStopConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-emrserverless.CfnApplication.InitialCapacityConfigKeyValuePairProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class InitialCapacityConfigKeyValuePairProperty:
        def __init__(
            self,
            *,
            key: builtins.str,
            value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApplication.InitialCapacityConfigProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''The initial capacity configuration per worker.

            :param key: The worker type for an analytics framework. For Spark applications, the key can either be set to ``Driver`` or ``Executor`` . For Hive applications, it can be set to ``HiveDriver`` or ``TezTask`` . *Minimum* : 1 *Maximum* : 50 *Pattern* : ``^[a-zA-Z]+[-_]*[a-zA-Z]+$``
            :param value: The value for the initial capacity configuration per worker.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-initialcapacityconfigkeyvaluepair.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_emrserverless as emrserverless
                
                initial_capacity_config_key_value_pair_property = emrserverless.CfnApplication.InitialCapacityConfigKeyValuePairProperty(
                    key="key",
                    value=emrserverless.CfnApplication.InitialCapacityConfigProperty(
                        worker_configuration=emrserverless.CfnApplication.WorkerConfigurationProperty(
                            cpu="cpu",
                            memory="memory",
                
                            # the properties below are optional
                            disk="disk"
                        ),
                        worker_count=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d2120fff03e840ecb86b1ea45eab1101f7e6113b6be3a81a134306d203e4dad4)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''The worker type for an analytics framework.

            For Spark applications, the key can either be set to ``Driver`` or ``Executor`` . For Hive applications, it can be set to ``HiveDriver`` or ``TezTask`` .

            *Minimum* : 1

            *Maximum* : 50

            *Pattern* : ``^[a-zA-Z]+[-_]*[a-zA-Z]+$``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-initialcapacityconfigkeyvaluepair.html#cfn-emrserverless-application-initialcapacityconfigkeyvaluepair-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.InitialCapacityConfigProperty"]:
            '''The value for the initial capacity configuration per worker.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-initialcapacityconfigkeyvaluepair.html#cfn-emrserverless-application-initialcapacityconfigkeyvaluepair-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.InitialCapacityConfigProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InitialCapacityConfigKeyValuePairProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-emrserverless.CfnApplication.InitialCapacityConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "worker_configuration": "workerConfiguration",
            "worker_count": "workerCount",
        },
    )
    class InitialCapacityConfigProperty:
        def __init__(
            self,
            *,
            worker_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApplication.WorkerConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
            worker_count: jsii.Number,
        ) -> None:
            '''The initial capacity configuration per worker.

            :param worker_configuration: The resource configuration of the initial capacity configuration.
            :param worker_count: The number of workers in the initial capacity configuration. *Minimum* : 1 *Maximum* : 1000000

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-initialcapacityconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_emrserverless as emrserverless
                
                initial_capacity_config_property = emrserverless.CfnApplication.InitialCapacityConfigProperty(
                    worker_configuration=emrserverless.CfnApplication.WorkerConfigurationProperty(
                        cpu="cpu",
                        memory="memory",
                
                        # the properties below are optional
                        disk="disk"
                    ),
                    worker_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8d19ed5fc43acfed8b20a236f6ae7f1ffc5c1fc7196a7c8ec65228e8bf687813)
                check_type(argname="argument worker_configuration", value=worker_configuration, expected_type=type_hints["worker_configuration"])
                check_type(argname="argument worker_count", value=worker_count, expected_type=type_hints["worker_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "worker_configuration": worker_configuration,
                "worker_count": worker_count,
            }

        @builtins.property
        def worker_configuration(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.WorkerConfigurationProperty"]:
            '''The resource configuration of the initial capacity configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-initialcapacityconfig.html#cfn-emrserverless-application-initialcapacityconfig-workerconfiguration
            '''
            result = self._values.get("worker_configuration")
            assert result is not None, "Required property 'worker_configuration' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.WorkerConfigurationProperty"], result)

        @builtins.property
        def worker_count(self) -> jsii.Number:
            '''The number of workers in the initial capacity configuration.

            *Minimum* : 1

            *Maximum* : 1000000

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-initialcapacityconfig.html#cfn-emrserverless-application-initialcapacityconfig-workercount
            '''
            result = self._values.get("worker_count")
            assert result is not None, "Required property 'worker_count' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "InitialCapacityConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-emrserverless.CfnApplication.MaximumAllowedResourcesProperty",
        jsii_struct_bases=[],
        name_mapping={"cpu": "cpu", "memory": "memory", "disk": "disk"},
    )
    class MaximumAllowedResourcesProperty:
        def __init__(
            self,
            *,
            cpu: builtins.str,
            memory: builtins.str,
            disk: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The maximum allowed cumulative resources for an application.

            No new resources will be created once the limit is hit.

            :param cpu: The maximum allowed CPU for an application. *Minimum* : 1 *Maximum* : 15 *Pattern* : ``^[1-9][0-9]*(\\\\s)?(vCPU|vcpu|VCPU)?$``
            :param memory: The maximum allowed resources for an application. *Minimum* : 1 *Maximum* : 15 *Pattern* : ``^[1-9][0-9]*(\\\\s)?(GB|gb|gB|Gb)?$``
            :param disk: The maximum allowed disk for an application. *Minimum* : 1 *Maximum* : 15 *Pattern* : ``^[1-9][0-9]*(\\\\s)?(GB|gb|gB|Gb)$"``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-maximumallowedresources.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_emrserverless as emrserverless
                
                maximum_allowed_resources_property = emrserverless.CfnApplication.MaximumAllowedResourcesProperty(
                    cpu="cpu",
                    memory="memory",
                
                    # the properties below are optional
                    disk="disk"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__75c646052eec2766735ddd80e9da5865a3e1c882860772bd2695d3ab16ae3fee)
                check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
                check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
                check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cpu": cpu,
                "memory": memory,
            }
            if disk is not None:
                self._values["disk"] = disk

        @builtins.property
        def cpu(self) -> builtins.str:
            '''The maximum allowed CPU for an application.

            *Minimum* : 1

            *Maximum* : 15

            *Pattern* : ``^[1-9][0-9]*(\\\\s)?(vCPU|vcpu|VCPU)?$``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-maximumallowedresources.html#cfn-emrserverless-application-maximumallowedresources-cpu
            '''
            result = self._values.get("cpu")
            assert result is not None, "Required property 'cpu' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def memory(self) -> builtins.str:
            '''The maximum allowed resources for an application.

            *Minimum* : 1

            *Maximum* : 15

            *Pattern* : ``^[1-9][0-9]*(\\\\s)?(GB|gb|gB|Gb)?$``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-maximumallowedresources.html#cfn-emrserverless-application-maximumallowedresources-memory
            '''
            result = self._values.get("memory")
            assert result is not None, "Required property 'memory' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def disk(self) -> typing.Optional[builtins.str]:
            '''The maximum allowed disk for an application.

            *Minimum* : 1

            *Maximum* : 15

            *Pattern* : ``^[1-9][0-9]*(\\\\s)?(GB|gb|gB|Gb)$"``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-maximumallowedresources.html#cfn-emrserverless-application-maximumallowedresources-disk
            '''
            result = self._values.get("disk")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaximumAllowedResourcesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-emrserverless.CfnApplication.NetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "security_group_ids": "securityGroupIds",
            "subnet_ids": "subnetIds",
        },
    )
    class NetworkConfigurationProperty:
        def __init__(
            self,
            *,
            security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
            subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''The network configuration for customer VPC connectivity.

            :param security_group_ids: The array of security group Ids for customer VPC connectivity. *Minimum* : 1 *Maximum* : 32 *Pattern* : ``^[-0-9a-zA-Z]+``
            :param subnet_ids: The array of subnet Ids for customer VPC connectivity. *Minimum* : 1 *Maximum* : 32 *Pattern* : ``^[-0-9a-zA-Z]+``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-networkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_emrserverless as emrserverless
                
                network_configuration_property = emrserverless.CfnApplication.NetworkConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bea026b225eefaf0221b30e1fd554bc61462627f7fa365bb71322ac2c10f1237)
                check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
                check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if security_group_ids is not None:
                self._values["security_group_ids"] = security_group_ids
            if subnet_ids is not None:
                self._values["subnet_ids"] = subnet_ids

        @builtins.property
        def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The array of security group Ids for customer VPC connectivity.

            *Minimum* : 1

            *Maximum* : 32

            *Pattern* : ``^[-0-9a-zA-Z]+``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-networkconfiguration.html#cfn-emrserverless-application-networkconfiguration-securitygroupids
            '''
            result = self._values.get("security_group_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The array of subnet Ids for customer VPC connectivity.

            *Minimum* : 1

            *Maximum* : 32

            *Pattern* : ``^[-0-9a-zA-Z]+``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-networkconfiguration.html#cfn-emrserverless-application-networkconfiguration-subnetids
            '''
            result = self._values.get("subnet_ids")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-emrserverless.CfnApplication.WorkerConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"cpu": "cpu", "memory": "memory", "disk": "disk"},
    )
    class WorkerConfigurationProperty:
        def __init__(
            self,
            *,
            cpu: builtins.str,
            memory: builtins.str,
            disk: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The resource configuration of the initial capacity configuration.

            :param cpu: *Minimum* : 1. *Maximum* : 15 *Pattern* : ``^[1-9][0-9]*(\\\\s)?(vCPU|vcpu|VCPU)?$``
            :param memory: *Minimum* : 1. *Maximum* : 15 *Pattern* : ``^[1-9][0-9]*(\\\\s)?(GB|gb|gB|Gb)?$``
            :param disk: *Minimum* : 1. *Maximum* : 15 *Pattern* : ``^[1-9][0-9]*(\\\\s)?(GB|gb|gB|Gb)$"``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-workerconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_emrserverless as emrserverless
                
                worker_configuration_property = emrserverless.CfnApplication.WorkerConfigurationProperty(
                    cpu="cpu",
                    memory="memory",
                
                    # the properties below are optional
                    disk="disk"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2e7ca31ef92c1ea53bcaa6021683cd6e2aeeda510ffcce79b9012125853ad6fc)
                check_type(argname="argument cpu", value=cpu, expected_type=type_hints["cpu"])
                check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
                check_type(argname="argument disk", value=disk, expected_type=type_hints["disk"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "cpu": cpu,
                "memory": memory,
            }
            if disk is not None:
                self._values["disk"] = disk

        @builtins.property
        def cpu(self) -> builtins.str:
            '''*Minimum* : 1.

            *Maximum* : 15

            *Pattern* : ``^[1-9][0-9]*(\\\\s)?(vCPU|vcpu|VCPU)?$``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-workerconfiguration.html#cfn-emrserverless-application-workerconfiguration-cpu
            '''
            result = self._values.get("cpu")
            assert result is not None, "Required property 'cpu' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def memory(self) -> builtins.str:
            '''*Minimum* : 1.

            *Maximum* : 15

            *Pattern* : ``^[1-9][0-9]*(\\\\s)?(GB|gb|gB|Gb)?$``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-workerconfiguration.html#cfn-emrserverless-application-workerconfiguration-memory
            '''
            result = self._values.get("memory")
            assert result is not None, "Required property 'memory' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def disk(self) -> typing.Optional[builtins.str]:
            '''*Minimum* : 1.

            *Maximum* : 15

            *Pattern* : ``^[1-9][0-9]*(\\\\s)?(GB|gb|gB|Gb)$"``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-emrserverless-application-workerconfiguration.html#cfn-emrserverless-application-workerconfiguration-disk
            '''
            result = self._values.get("disk")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WorkerConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-emrserverless.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "release_label": "releaseLabel",
        "type": "type",
        "architecture": "architecture",
        "auto_start_configuration": "autoStartConfiguration",
        "auto_stop_configuration": "autoStopConfiguration",
        "initial_capacity": "initialCapacity",
        "maximum_capacity": "maximumCapacity",
        "name": "name",
        "network_configuration": "networkConfiguration",
        "tags": "tags",
    },
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        release_label: builtins.str,
        type: builtins.str,
        architecture: typing.Optional[builtins.str] = None,
        auto_start_configuration: typing.Optional[typing.Union[typing.Union[CfnApplication.AutoStartConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
        auto_stop_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.AutoStopConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        initial_capacity: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.InitialCapacityConfigKeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        maximum_capacity: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.MaximumAllowedResourcesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        network_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApplication``.

        :param release_label: The EMR release version associated with the application. *Minimum* : 1 *Maximum* : 64 *Pattern* : ``^[A-Za-z0-9._/-]+$``
        :param type: The type of application, such as Spark or Hive.
        :param architecture: The CPU architecture type of the application. Allowed values: ``X86_64`` or ``ARM64``
        :param auto_start_configuration: The configuration for an application to automatically start on job submission.
        :param auto_stop_configuration: The configuration for an application to automatically stop after a certain amount of time being idle.
        :param initial_capacity: The initial capacity of the application.
        :param maximum_capacity: The maximum capacity of the application. This is cumulative across all workers at any given point in time during the lifespan of the application is created. No new resources will be created once any one of the defined limits is hit.
        :param name: The name of the application. *Minimum* : 1 *Maximum* : 64 *Pattern* : ``^[A-Za-z0-9._\\\\/#-]+$``
        :param network_configuration: The network configuration for customer VPC connectivity for the application.
        :param tags: The tags assigned to the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_emrserverless as emrserverless
            
            cfn_application_props = emrserverless.CfnApplicationProps(
                release_label="releaseLabel",
                type="type",
            
                # the properties below are optional
                architecture="architecture",
                auto_start_configuration=emrserverless.CfnApplication.AutoStartConfigurationProperty(
                    enabled=False
                ),
                auto_stop_configuration=emrserverless.CfnApplication.AutoStopConfigurationProperty(
                    enabled=False,
                    idle_timeout_minutes=123
                ),
                initial_capacity=[emrserverless.CfnApplication.InitialCapacityConfigKeyValuePairProperty(
                    key="key",
                    value=emrserverless.CfnApplication.InitialCapacityConfigProperty(
                        worker_configuration=emrserverless.CfnApplication.WorkerConfigurationProperty(
                            cpu="cpu",
                            memory="memory",
            
                            # the properties below are optional
                            disk="disk"
                        ),
                        worker_count=123
                    )
                )],
                maximum_capacity=emrserverless.CfnApplication.MaximumAllowedResourcesProperty(
                    cpu="cpu",
                    memory="memory",
            
                    # the properties below are optional
                    disk="disk"
                ),
                name="name",
                network_configuration=emrserverless.CfnApplication.NetworkConfigurationProperty(
                    security_group_ids=["securityGroupIds"],
                    subnet_ids=["subnetIds"]
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dda6243a8dd7afa1563a766fbd7ce9ba4a69f83a72c9f08d199ef6fd6ae8686)
            check_type(argname="argument release_label", value=release_label, expected_type=type_hints["release_label"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument auto_start_configuration", value=auto_start_configuration, expected_type=type_hints["auto_start_configuration"])
            check_type(argname="argument auto_stop_configuration", value=auto_stop_configuration, expected_type=type_hints["auto_stop_configuration"])
            check_type(argname="argument initial_capacity", value=initial_capacity, expected_type=type_hints["initial_capacity"])
            check_type(argname="argument maximum_capacity", value=maximum_capacity, expected_type=type_hints["maximum_capacity"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "release_label": release_label,
            "type": type,
        }
        if architecture is not None:
            self._values["architecture"] = architecture
        if auto_start_configuration is not None:
            self._values["auto_start_configuration"] = auto_start_configuration
        if auto_stop_configuration is not None:
            self._values["auto_stop_configuration"] = auto_stop_configuration
        if initial_capacity is not None:
            self._values["initial_capacity"] = initial_capacity
        if maximum_capacity is not None:
            self._values["maximum_capacity"] = maximum_capacity
        if name is not None:
            self._values["name"] = name
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def release_label(self) -> builtins.str:
        '''The EMR release version associated with the application.

        *Minimum* : 1

        *Maximum* : 64

        *Pattern* : ``^[A-Za-z0-9._/-]+$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-releaselabel
        '''
        result = self._values.get("release_label")
        assert result is not None, "Required property 'release_label' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of application, such as Spark or Hive.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def architecture(self) -> typing.Optional[builtins.str]:
        '''The CPU architecture type of the application.

        Allowed values: ``X86_64`` or ``ARM64``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-architecture
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_start_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnApplication.AutoStartConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]]:
        '''The configuration for an application to automatically start on job submission.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-autostartconfiguration
        '''
        result = self._values.get("auto_start_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnApplication.AutoStartConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def auto_stop_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplication.AutoStopConfigurationProperty]]:
        '''The configuration for an application to automatically stop after a certain amount of time being idle.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-autostopconfiguration
        '''
        result = self._values.get("auto_stop_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplication.AutoStopConfigurationProperty]], result)

    @builtins.property
    def initial_capacity(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplication.InitialCapacityConfigKeyValuePairProperty]]]]:
        '''The initial capacity of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-initialcapacity
        '''
        result = self._values.get("initial_capacity")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplication.InitialCapacityConfigKeyValuePairProperty]]]], result)

    @builtins.property
    def maximum_capacity(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplication.MaximumAllowedResourcesProperty]]:
        '''The maximum capacity of the application.

        This is cumulative across all workers at any given point in time during the lifespan of the application is created. No new resources will be created once any one of the defined limits is hit.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-maximumcapacity
        '''
        result = self._values.get("maximum_capacity")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplication.MaximumAllowedResourcesProperty]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the application.

        *Minimum* : 1

        *Maximum* : 64

        *Pattern* : ``^[A-Za-z0-9._\\\\/#-]+$``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplication.NetworkConfigurationProperty]]:
        '''The network configuration for customer VPC connectivity for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-networkconfiguration
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplication.NetworkConfigurationProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags assigned to the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-emrserverless-application.html#cfn-emrserverless-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApplication",
    "CfnApplicationProps",
]

publication.publish()

def _typecheckingstub__5c43e9a1cc87f8e9909f905993b5411b578cabe85440ca32c60c769e0544ffd6(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    release_label: builtins.str,
    type: builtins.str,
    architecture: typing.Optional[builtins.str] = None,
    auto_start_configuration: typing.Optional[typing.Union[typing.Union[CfnApplication.AutoStartConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    auto_stop_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.AutoStopConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    initial_capacity: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.InitialCapacityConfigKeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    maximum_capacity: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.MaximumAllowedResourcesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b000495631c615df24622de393225ab7b5ab2f2cd3d6c019cd77a544d2adbd0(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3089778c978d28e8eec7d7e5bf737e35f9f2c88b15c58aeef9fb9d3169a7091(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f040abf2796728145422ba345c7280e1882ca56a93798ec8d04578c424a0cf41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ffc6644afbddd2110977215737cb601db2a813b9fcb80e472d822e60cf473a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__633c944ab002662272329cd2ab53054a421544659413787f2c0b2dad01aee3be(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcc92144333fa6a0918945f1a1c483c9c6e2cd93bb706c1b5e1dc0130a7aa0f3(
    value: typing.Optional[typing.Union[CfnApplication.AutoStartConfigurationProperty, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c68631a69cf3bda8ae7d964e25b12e8e294697448d8197c2432b13028dbf9514(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplication.AutoStopConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7d6df0a17fbedc0853acda87e0b78a1f838a3ee10414fefd80337c94fbdd7f0(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplication.InitialCapacityConfigKeyValuePairProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb2f9c42f5dde30a69eb7dd3222f8ffae825b5c95d6840f00a654a977d2ad7d5(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplication.MaximumAllowedResourcesProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30a71da96a2b3cf8fe63a539c2c4153d85504210e2a8dca8e70265eb40613c4d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6950254fbb841a6f83fe777bec8b833d5d15d1dafbd7515772ef993e38b80c5b(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplication.NetworkConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18daf1a39548ff8ae0c6bc1d45bf6356180ec62b69a172e09a7b00829f244df3(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e755663f779db4860da63be3bb8ccd650760952ccd79b6692ccada7ca574ee(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    idle_timeout_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2120fff03e840ecb86b1ea45eab1101f7e6113b6be3a81a134306d203e4dad4(
    *,
    key: builtins.str,
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.InitialCapacityConfigProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d19ed5fc43acfed8b20a236f6ae7f1ffc5c1fc7196a7c8ec65228e8bf687813(
    *,
    worker_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.WorkerConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    worker_count: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75c646052eec2766735ddd80e9da5865a3e1c882860772bd2695d3ab16ae3fee(
    *,
    cpu: builtins.str,
    memory: builtins.str,
    disk: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bea026b225eefaf0221b30e1fd554bc61462627f7fa365bb71322ac2c10f1237(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e7ca31ef92c1ea53bcaa6021683cd6e2aeeda510ffcce79b9012125853ad6fc(
    *,
    cpu: builtins.str,
    memory: builtins.str,
    disk: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dda6243a8dd7afa1563a766fbd7ce9ba4a69f83a72c9f08d199ef6fd6ae8686(
    *,
    release_label: builtins.str,
    type: builtins.str,
    architecture: typing.Optional[builtins.str] = None,
    auto_start_configuration: typing.Optional[typing.Union[typing.Union[CfnApplication.AutoStartConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    auto_stop_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.AutoStopConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    initial_capacity: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.InitialCapacityConfigKeyValuePairProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    maximum_capacity: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.MaximumAllowedResourcesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
