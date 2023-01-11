'''
# AWS::GreengrassV2 Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as greengrass
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for GreengrassV2 construct libraries](https://constructs.dev/search?q=greengrassv2)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::GreengrassV2 resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_GreengrassV2.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::GreengrassV2](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_GreengrassV2.html).

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
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnComponentVersion(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_greengrassv2.CfnComponentVersion",
):
    '''A CloudFormation ``AWS::GreengrassV2::ComponentVersion``.

    Creates a component. Components are software that run on AWS IoT Greengrass core devices. After you develop and test a component on your core device, you can use this operation to upload your component to AWS IoT Greengrass . Then, you can deploy the component to other core devices.

    You can use this operation to do the following:

    - *Create components from recipes*

    Create a component from a recipe, which is a file that defines the component's metadata, parameters, dependencies, lifecycle, artifacts, and platform capability. For more information, see `AWS IoT Greengrass component recipe reference <https://docs.aws.amazon.com/greengrass/v2/developerguide/component-recipe-reference.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

    To create a component from a recipe, specify ``inlineRecipe`` when you call this operation.

    - *Create components from Lambda functions*

    Create a component from an AWS Lambda function that runs on AWS IoT Greengrass . This creates a recipe and artifacts from the Lambda function's deployment package. You can use this operation to migrate Lambda functions from AWS IoT Greengrass V1 to AWS IoT Greengrass V2 .

    This function only accepts Lambda functions that use the following runtimes:

    - Python 2.7 – ``python2.7``
    - Python 3.7 – ``python3.7``
    - Python 3.8 – ``python3.8``
    - Java 8 – ``java8``
    - Node.js 10 – ``nodejs10.x``
    - Node.js 12 – ``nodejs12.x``

    To create a component from a Lambda function, specify ``lambdaFunction`` when you call this operation.

    :cloudformationResource: AWS::GreengrassV2::ComponentVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-componentversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_greengrassv2 as greengrassv2
        
        cfn_component_version = greengrassv2.CfnComponentVersion(self, "MyCfnComponentVersion",
            inline_recipe="inlineRecipe",
            lambda_function=greengrassv2.CfnComponentVersion.LambdaFunctionRecipeSourceProperty(
                component_dependencies={
                    "component_dependencies_key": greengrassv2.CfnComponentVersion.ComponentDependencyRequirementProperty(
                        dependency_type="dependencyType",
                        version_requirement="versionRequirement"
                    )
                },
                component_lambda_parameters=greengrassv2.CfnComponentVersion.LambdaExecutionParametersProperty(
                    environment_variables={
                        "environment_variables_key": "environmentVariables"
                    },
                    event_sources=[greengrassv2.CfnComponentVersion.LambdaEventSourceProperty(
                        topic="topic",
                        type="type"
                    )],
                    exec_args=["execArgs"],
                    input_payload_encoding_type="inputPayloadEncodingType",
                    linux_process_params=greengrassv2.CfnComponentVersion.LambdaLinuxProcessParamsProperty(
                        container_params=greengrassv2.CfnComponentVersion.LambdaContainerParamsProperty(
                            devices=[greengrassv2.CfnComponentVersion.LambdaDeviceMountProperty(
                                add_group_owner=False,
                                path="path",
                                permission="permission"
                            )],
                            memory_size_in_kb=123,
                            mount_ro_sysfs=False,
                            volumes=[greengrassv2.CfnComponentVersion.LambdaVolumeMountProperty(
                                add_group_owner=False,
                                destination_path="destinationPath",
                                permission="permission",
                                source_path="sourcePath"
                            )]
                        ),
                        isolation_mode="isolationMode"
                    ),
                    max_idle_time_in_seconds=123,
                    max_instances_count=123,
                    max_queue_size=123,
                    pinned=False,
                    status_timeout_in_seconds=123,
                    timeout_in_seconds=123
                ),
                component_name="componentName",
                component_platforms=[greengrassv2.CfnComponentVersion.ComponentPlatformProperty(
                    attributes={
                        "attributes_key": "attributes"
                    },
                    name="name"
                )],
                component_version="componentVersion",
                lambda_arn="lambdaArn"
            ),
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        inline_recipe: typing.Optional[builtins.str] = None,
        lambda_function: typing.Optional[typing.Union[typing.Union["CfnComponentVersion.LambdaFunctionRecipeSourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::GreengrassV2::ComponentVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param inline_recipe: The recipe to use to create the component. The recipe defines the component's metadata, parameters, dependencies, lifecycle, artifacts, and platform compatibility. You must specify either ``InlineRecipe`` or ``LambdaFunction`` .
        :param lambda_function: The parameters to create a component from a Lambda function. You must specify either ``InlineRecipe`` or ``LambdaFunction`` .
        :param tags: Application-specific metadata to attach to the component version. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tag your AWS IoT Greengrass Version 2 resources <https://docs.aws.amazon.com/greengrass/v2/developerguide/tag-resources.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__367836b0c10b75b5cb241353a886a5a5e492dd8c50a222db6671d0796907f4d7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnComponentVersionProps(
            inline_recipe=inline_recipe, lambda_function=lambda_function, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3fb33a480b0f385d15d97e830de0923f435d9853464bee51166c928ea8363dd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__338f4f82e6d431f73b968d336b9061bd14482610f200e746e00b5671e382f739)
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
        '''The ARN of the component version.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrComponentName")
    def attr_component_name(self) -> builtins.str:
        '''The name of the component.

        :cloudformationAttribute: ComponentName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrComponentName"))

    @builtins.property
    @jsii.member(jsii_name="attrComponentVersion")
    def attr_component_version(self) -> builtins.str:
        '''The version of the component.

        :cloudformationAttribute: ComponentVersion
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrComponentVersion"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Application-specific metadata to attach to the component version.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tag your AWS IoT Greengrass Version 2 resources <https://docs.aws.amazon.com/greengrass/v2/developerguide/tag-resources.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-componentversion.html#cfn-greengrassv2-componentversion-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="inlineRecipe")
    def inline_recipe(self) -> typing.Optional[builtins.str]:
        '''The recipe to use to create the component.

        The recipe defines the component's metadata, parameters, dependencies, lifecycle, artifacts, and platform compatibility.

        You must specify either ``InlineRecipe`` or ``LambdaFunction`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-componentversion.html#cfn-greengrassv2-componentversion-inlinerecipe
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "inlineRecipe"))

    @inline_recipe.setter
    def inline_recipe(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5de086987d04f39f7375f143596e93b11b33c4a8f34ce25b06f542271448e22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "inlineRecipe", value)

    @builtins.property
    @jsii.member(jsii_name="lambdaFunction")
    def lambda_function(
        self,
    ) -> typing.Optional[typing.Union["CfnComponentVersion.LambdaFunctionRecipeSourceProperty", _IResolvable_a771d0ef]]:
        '''The parameters to create a component from a Lambda function.

        You must specify either ``InlineRecipe`` or ``LambdaFunction`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-componentversion.html#cfn-greengrassv2-componentversion-lambdafunction
        '''
        return typing.cast(typing.Optional[typing.Union["CfnComponentVersion.LambdaFunctionRecipeSourceProperty", _IResolvable_a771d0ef]], jsii.get(self, "lambdaFunction"))

    @lambda_function.setter
    def lambda_function(
        self,
        value: typing.Optional[typing.Union["CfnComponentVersion.LambdaFunctionRecipeSourceProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eeca3819844e642b32b994374a94a0b300e8a6ec4b9fef246d5e40fb7172d728)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "lambdaFunction", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnComponentVersion.ComponentDependencyRequirementProperty",
        jsii_struct_bases=[],
        name_mapping={
            "dependency_type": "dependencyType",
            "version_requirement": "versionRequirement",
        },
    )
    class ComponentDependencyRequirementProperty:
        def __init__(
            self,
            *,
            dependency_type: typing.Optional[builtins.str] = None,
            version_requirement: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a component dependency for a Lambda function component.

            :param dependency_type: The type of this dependency. Choose from the following options:. - ``SOFT`` – The component doesn't restart if the dependency changes state. - ``HARD`` – The component restarts if the dependency changes state. Default: ``HARD``
            :param version_requirement: The component version requirement for the component dependency. AWS IoT Greengrass uses semantic version constraints. For more information, see `Semantic Versioning <https://docs.aws.amazon.com/https://semver.org/>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-componentdependencyrequirement.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                component_dependency_requirement_property = greengrassv2.CfnComponentVersion.ComponentDependencyRequirementProperty(
                    dependency_type="dependencyType",
                    version_requirement="versionRequirement"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b21032cf8c65f0a4da2e9b3544b46f0bed9409e81a5b82f5e7ff7d5b9e2d8144)
                check_type(argname="argument dependency_type", value=dependency_type, expected_type=type_hints["dependency_type"])
                check_type(argname="argument version_requirement", value=version_requirement, expected_type=type_hints["version_requirement"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if dependency_type is not None:
                self._values["dependency_type"] = dependency_type
            if version_requirement is not None:
                self._values["version_requirement"] = version_requirement

        @builtins.property
        def dependency_type(self) -> typing.Optional[builtins.str]:
            '''The type of this dependency. Choose from the following options:.

            - ``SOFT`` – The component doesn't restart if the dependency changes state.
            - ``HARD`` – The component restarts if the dependency changes state.

            Default: ``HARD``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-componentdependencyrequirement.html#cfn-greengrassv2-componentversion-componentdependencyrequirement-dependencytype
            '''
            result = self._values.get("dependency_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version_requirement(self) -> typing.Optional[builtins.str]:
            '''The component version requirement for the component dependency.

            AWS IoT Greengrass uses semantic version constraints. For more information, see `Semantic Versioning <https://docs.aws.amazon.com/https://semver.org/>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-componentdependencyrequirement.html#cfn-greengrassv2-componentversion-componentdependencyrequirement-versionrequirement
            '''
            result = self._values.get("version_requirement")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentDependencyRequirementProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnComponentVersion.ComponentPlatformProperty",
        jsii_struct_bases=[],
        name_mapping={"attributes": "attributes", "name": "name"},
    )
    class ComponentPlatformProperty:
        def __init__(
            self,
            *,
            attributes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a platform that a component supports.

            :param attributes: A dictionary of attributes for the platform. The AWS IoT Greengrass Core software defines the ``os`` and ``platform`` by default. You can specify additional platform attributes for a core device when you deploy the AWS IoT Greengrass nucleus component. For more information, see the `AWS IoT Greengrass nucleus component <https://docs.aws.amazon.com/greengrass/v2/developerguide/greengrass-nucleus-component.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .
            :param name: The friendly name of the platform. This name helps you identify the platform. If you omit this parameter, AWS IoT Greengrass creates a friendly name from the ``os`` and ``architecture`` of the platform.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-componentplatform.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                component_platform_property = greengrassv2.CfnComponentVersion.ComponentPlatformProperty(
                    attributes={
                        "attributes_key": "attributes"
                    },
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0e8633ff0fcbcbf7d4829394d49a6b2a6c1251d2bd9d0d91cde64cad4b63fc64)
                check_type(argname="argument attributes", value=attributes, expected_type=type_hints["attributes"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if attributes is not None:
                self._values["attributes"] = attributes
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def attributes(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''A dictionary of attributes for the platform.

            The AWS IoT Greengrass Core software defines the ``os`` and ``platform`` by default. You can specify additional platform attributes for a core device when you deploy the AWS IoT Greengrass nucleus component. For more information, see the `AWS IoT Greengrass nucleus component <https://docs.aws.amazon.com/greengrass/v2/developerguide/greengrass-nucleus-component.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-componentplatform.html#cfn-greengrassv2-componentversion-componentplatform-attributes
            '''
            result = self._values.get("attributes")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The friendly name of the platform. This name helps you identify the platform.

            If you omit this parameter, AWS IoT Greengrass creates a friendly name from the ``os`` and ``architecture`` of the platform.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-componentplatform.html#cfn-greengrassv2-componentversion-componentplatform-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentPlatformProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnComponentVersion.LambdaContainerParamsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "devices": "devices",
            "memory_size_in_kb": "memorySizeInKb",
            "mount_ro_sysfs": "mountRoSysfs",
            "volumes": "volumes",
        },
    )
    class LambdaContainerParamsProperty:
        def __init__(
            self,
            *,
            devices: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnComponentVersion.LambdaDeviceMountProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            memory_size_in_kb: typing.Optional[jsii.Number] = None,
            mount_ro_sysfs: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            volumes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnComponentVersion.LambdaVolumeMountProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''Contains information about a container in which AWS Lambda functions run on AWS IoT Greengrass core devices.

            :param devices: The list of system devices that the container can access.
            :param memory_size_in_kb: The memory size of the container, expressed in kilobytes. Default: ``16384`` (16 MB)
            :param mount_ro_sysfs: Whether or not the container can read information from the device's ``/sys`` folder. Default: ``false``
            :param volumes: The list of volumes that the container can access.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdacontainerparams.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                lambda_container_params_property = greengrassv2.CfnComponentVersion.LambdaContainerParamsProperty(
                    devices=[greengrassv2.CfnComponentVersion.LambdaDeviceMountProperty(
                        add_group_owner=False,
                        path="path",
                        permission="permission"
                    )],
                    memory_size_in_kb=123,
                    mount_ro_sysfs=False,
                    volumes=[greengrassv2.CfnComponentVersion.LambdaVolumeMountProperty(
                        add_group_owner=False,
                        destination_path="destinationPath",
                        permission="permission",
                        source_path="sourcePath"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8a11394b6651ec377a8088918c206587a570e49edab30e4f69bb846e7dcc1c43)
                check_type(argname="argument devices", value=devices, expected_type=type_hints["devices"])
                check_type(argname="argument memory_size_in_kb", value=memory_size_in_kb, expected_type=type_hints["memory_size_in_kb"])
                check_type(argname="argument mount_ro_sysfs", value=mount_ro_sysfs, expected_type=type_hints["mount_ro_sysfs"])
                check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if devices is not None:
                self._values["devices"] = devices
            if memory_size_in_kb is not None:
                self._values["memory_size_in_kb"] = memory_size_in_kb
            if mount_ro_sysfs is not None:
                self._values["mount_ro_sysfs"] = mount_ro_sysfs
            if volumes is not None:
                self._values["volumes"] = volumes

        @builtins.property
        def devices(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponentVersion.LambdaDeviceMountProperty", _IResolvable_a771d0ef]]]]:
            '''The list of system devices that the container can access.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdacontainerparams.html#cfn-greengrassv2-componentversion-lambdacontainerparams-devices
            '''
            result = self._values.get("devices")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponentVersion.LambdaDeviceMountProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def memory_size_in_kb(self) -> typing.Optional[jsii.Number]:
            '''The memory size of the container, expressed in kilobytes.

            Default: ``16384`` (16 MB)

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdacontainerparams.html#cfn-greengrassv2-componentversion-lambdacontainerparams-memorysizeinkb
            '''
            result = self._values.get("memory_size_in_kb")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def mount_ro_sysfs(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Whether or not the container can read information from the device's ``/sys`` folder.

            Default: ``false``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdacontainerparams.html#cfn-greengrassv2-componentversion-lambdacontainerparams-mountrosysfs
            '''
            result = self._values.get("mount_ro_sysfs")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def volumes(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponentVersion.LambdaVolumeMountProperty", _IResolvable_a771d0ef]]]]:
            '''The list of volumes that the container can access.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdacontainerparams.html#cfn-greengrassv2-componentversion-lambdacontainerparams-volumes
            '''
            result = self._values.get("volumes")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponentVersion.LambdaVolumeMountProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaContainerParamsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnComponentVersion.LambdaDeviceMountProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_group_owner": "addGroupOwner",
            "path": "path",
            "permission": "permission",
        },
    )
    class LambdaDeviceMountProperty:
        def __init__(
            self,
            *,
            add_group_owner: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            path: typing.Optional[builtins.str] = None,
            permission: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a device that Linux processes in a container can access.

            :param add_group_owner: Whether or not to add the component's system user as an owner of the device. Default: ``false``
            :param path: The mount path for the device in the file system.
            :param permission: The permission to access the device: read/only ( ``ro`` ) or read/write ( ``rw`` ). Default: ``ro``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdadevicemount.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                lambda_device_mount_property = greengrassv2.CfnComponentVersion.LambdaDeviceMountProperty(
                    add_group_owner=False,
                    path="path",
                    permission="permission"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b715079a837485b41d661ec2e1557d589178997f66b393fd2bfb26d6d10b3f47)
                check_type(argname="argument add_group_owner", value=add_group_owner, expected_type=type_hints["add_group_owner"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if add_group_owner is not None:
                self._values["add_group_owner"] = add_group_owner
            if path is not None:
                self._values["path"] = path
            if permission is not None:
                self._values["permission"] = permission

        @builtins.property
        def add_group_owner(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Whether or not to add the component's system user as an owner of the device.

            Default: ``false``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdadevicemount.html#cfn-greengrassv2-componentversion-lambdadevicemount-addgroupowner
            '''
            result = self._values.get("add_group_owner")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The mount path for the device in the file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdadevicemount.html#cfn-greengrassv2-componentversion-lambdadevicemount-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def permission(self) -> typing.Optional[builtins.str]:
            '''The permission to access the device: read/only ( ``ro`` ) or read/write ( ``rw`` ).

            Default: ``ro``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdadevicemount.html#cfn-greengrassv2-componentversion-lambdadevicemount-permission
            '''
            result = self._values.get("permission")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaDeviceMountProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnComponentVersion.LambdaEventSourceProperty",
        jsii_struct_bases=[],
        name_mapping={"topic": "topic", "type": "type"},
    )
    class LambdaEventSourceProperty:
        def __init__(
            self,
            *,
            topic: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about an event source for an AWS Lambda function.

            The event source defines the topics on which this Lambda function subscribes to receive messages that run the function.

            :param topic: The topic to which to subscribe to receive event messages.
            :param type: The type of event source. Choose from the following options:. - ``PUB_SUB`` – Subscribe to local publish/subscribe messages. This event source type doesn't support MQTT wildcards ( ``+`` and ``#`` ) in the event source topic. - ``IOT_CORE`` – Subscribe to AWS IoT Core MQTT messages. This event source type supports MQTT wildcards ( ``+`` and ``#`` ) in the event source topic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaeventsource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                lambda_event_source_property = greengrassv2.CfnComponentVersion.LambdaEventSourceProperty(
                    topic="topic",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__28254b5c0c8738d6f53f3d23eeb930a95cdd096b763c3345bcfc5cc4927e47cd)
                check_type(argname="argument topic", value=topic, expected_type=type_hints["topic"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if topic is not None:
                self._values["topic"] = topic
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def topic(self) -> typing.Optional[builtins.str]:
            '''The topic to which to subscribe to receive event messages.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaeventsource.html#cfn-greengrassv2-componentversion-lambdaeventsource-topic
            '''
            result = self._values.get("topic")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of event source. Choose from the following options:.

            - ``PUB_SUB`` – Subscribe to local publish/subscribe messages. This event source type doesn't support MQTT wildcards ( ``+`` and ``#`` ) in the event source topic.
            - ``IOT_CORE`` – Subscribe to AWS IoT Core MQTT messages. This event source type supports MQTT wildcards ( ``+`` and ``#`` ) in the event source topic.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaeventsource.html#cfn-greengrassv2-componentversion-lambdaeventsource-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaEventSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnComponentVersion.LambdaExecutionParametersProperty",
        jsii_struct_bases=[],
        name_mapping={
            "environment_variables": "environmentVariables",
            "event_sources": "eventSources",
            "exec_args": "execArgs",
            "input_payload_encoding_type": "inputPayloadEncodingType",
            "linux_process_params": "linuxProcessParams",
            "max_idle_time_in_seconds": "maxIdleTimeInSeconds",
            "max_instances_count": "maxInstancesCount",
            "max_queue_size": "maxQueueSize",
            "pinned": "pinned",
            "status_timeout_in_seconds": "statusTimeoutInSeconds",
            "timeout_in_seconds": "timeoutInSeconds",
        },
    )
    class LambdaExecutionParametersProperty:
        def __init__(
            self,
            *,
            environment_variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
            event_sources: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnComponentVersion.LambdaEventSourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            exec_args: typing.Optional[typing.Sequence[builtins.str]] = None,
            input_payload_encoding_type: typing.Optional[builtins.str] = None,
            linux_process_params: typing.Optional[typing.Union[typing.Union["CfnComponentVersion.LambdaLinuxProcessParamsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            max_idle_time_in_seconds: typing.Optional[jsii.Number] = None,
            max_instances_count: typing.Optional[jsii.Number] = None,
            max_queue_size: typing.Optional[jsii.Number] = None,
            pinned: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            status_timeout_in_seconds: typing.Optional[jsii.Number] = None,
            timeout_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains parameters for a Lambda function that runs on AWS IoT Greengrass .

            :param environment_variables: The map of environment variables that are available to the Lambda function when it runs.
            :param event_sources: The list of event sources to which to subscribe to receive work messages. The Lambda function runs when it receives a message from an event source. You can subscribe this function to local publish/subscribe messages and AWS IoT Core MQTT messages.
            :param exec_args: The list of arguments to pass to the Lambda function when it runs.
            :param input_payload_encoding_type: The encoding type that the Lambda function supports. Default: ``json``
            :param linux_process_params: The parameters for the Linux process that contains the Lambda function.
            :param max_idle_time_in_seconds: The maximum amount of time in seconds that a non-pinned Lambda function can idle before the AWS IoT Greengrass Core software stops its process.
            :param max_instances_count: The maximum number of instances that a non-pinned Lambda function can run at the same time.
            :param max_queue_size: The maximum size of the message queue for the Lambda function component. The AWS IoT Greengrass core device stores messages in a FIFO (first-in-first-out) queue until it can run the Lambda function to consume each message.
            :param pinned: Whether or not the Lambda function is pinned, or long-lived. - A pinned Lambda function starts when the AWS IoT Greengrass Core starts and keeps running in its own container. - A non-pinned Lambda function starts only when it receives a work item and exists after it idles for ``maxIdleTimeInSeconds`` . If the function has multiple work items, the AWS IoT Greengrass Core software creates multiple instances of the function. Default: ``true``
            :param status_timeout_in_seconds: The interval in seconds at which a pinned (also known as long-lived) Lambda function component sends status updates to the Lambda manager component.
            :param timeout_in_seconds: The maximum amount of time in seconds that the Lambda function can process a work item.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                lambda_execution_parameters_property = greengrassv2.CfnComponentVersion.LambdaExecutionParametersProperty(
                    environment_variables={
                        "environment_variables_key": "environmentVariables"
                    },
                    event_sources=[greengrassv2.CfnComponentVersion.LambdaEventSourceProperty(
                        topic="topic",
                        type="type"
                    )],
                    exec_args=["execArgs"],
                    input_payload_encoding_type="inputPayloadEncodingType",
                    linux_process_params=greengrassv2.CfnComponentVersion.LambdaLinuxProcessParamsProperty(
                        container_params=greengrassv2.CfnComponentVersion.LambdaContainerParamsProperty(
                            devices=[greengrassv2.CfnComponentVersion.LambdaDeviceMountProperty(
                                add_group_owner=False,
                                path="path",
                                permission="permission"
                            )],
                            memory_size_in_kb=123,
                            mount_ro_sysfs=False,
                            volumes=[greengrassv2.CfnComponentVersion.LambdaVolumeMountProperty(
                                add_group_owner=False,
                                destination_path="destinationPath",
                                permission="permission",
                                source_path="sourcePath"
                            )]
                        ),
                        isolation_mode="isolationMode"
                    ),
                    max_idle_time_in_seconds=123,
                    max_instances_count=123,
                    max_queue_size=123,
                    pinned=False,
                    status_timeout_in_seconds=123,
                    timeout_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2cb0fcd118106691fca08a5d2bbd6298e4de8db5a5b8ed862ac67f3891ceedf2)
                check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
                check_type(argname="argument event_sources", value=event_sources, expected_type=type_hints["event_sources"])
                check_type(argname="argument exec_args", value=exec_args, expected_type=type_hints["exec_args"])
                check_type(argname="argument input_payload_encoding_type", value=input_payload_encoding_type, expected_type=type_hints["input_payload_encoding_type"])
                check_type(argname="argument linux_process_params", value=linux_process_params, expected_type=type_hints["linux_process_params"])
                check_type(argname="argument max_idle_time_in_seconds", value=max_idle_time_in_seconds, expected_type=type_hints["max_idle_time_in_seconds"])
                check_type(argname="argument max_instances_count", value=max_instances_count, expected_type=type_hints["max_instances_count"])
                check_type(argname="argument max_queue_size", value=max_queue_size, expected_type=type_hints["max_queue_size"])
                check_type(argname="argument pinned", value=pinned, expected_type=type_hints["pinned"])
                check_type(argname="argument status_timeout_in_seconds", value=status_timeout_in_seconds, expected_type=type_hints["status_timeout_in_seconds"])
                check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if environment_variables is not None:
                self._values["environment_variables"] = environment_variables
            if event_sources is not None:
                self._values["event_sources"] = event_sources
            if exec_args is not None:
                self._values["exec_args"] = exec_args
            if input_payload_encoding_type is not None:
                self._values["input_payload_encoding_type"] = input_payload_encoding_type
            if linux_process_params is not None:
                self._values["linux_process_params"] = linux_process_params
            if max_idle_time_in_seconds is not None:
                self._values["max_idle_time_in_seconds"] = max_idle_time_in_seconds
            if max_instances_count is not None:
                self._values["max_instances_count"] = max_instances_count
            if max_queue_size is not None:
                self._values["max_queue_size"] = max_queue_size
            if pinned is not None:
                self._values["pinned"] = pinned
            if status_timeout_in_seconds is not None:
                self._values["status_timeout_in_seconds"] = status_timeout_in_seconds
            if timeout_in_seconds is not None:
                self._values["timeout_in_seconds"] = timeout_in_seconds

        @builtins.property
        def environment_variables(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]]:
            '''The map of environment variables that are available to the Lambda function when it runs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-environmentvariables
            '''
            result = self._values.get("environment_variables")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def event_sources(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponentVersion.LambdaEventSourceProperty", _IResolvable_a771d0ef]]]]:
            '''The list of event sources to which to subscribe to receive work messages.

            The Lambda function runs when it receives a message from an event source. You can subscribe this function to local publish/subscribe messages and AWS IoT Core MQTT messages.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-eventsources
            '''
            result = self._values.get("event_sources")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponentVersion.LambdaEventSourceProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def exec_args(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of arguments to pass to the Lambda function when it runs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-execargs
            '''
            result = self._values.get("exec_args")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def input_payload_encoding_type(self) -> typing.Optional[builtins.str]:
            '''The encoding type that the Lambda function supports.

            Default: ``json``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-inputpayloadencodingtype
            '''
            result = self._values.get("input_payload_encoding_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def linux_process_params(
            self,
        ) -> typing.Optional[typing.Union["CfnComponentVersion.LambdaLinuxProcessParamsProperty", _IResolvable_a771d0ef]]:
            '''The parameters for the Linux process that contains the Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-linuxprocessparams
            '''
            result = self._values.get("linux_process_params")
            return typing.cast(typing.Optional[typing.Union["CfnComponentVersion.LambdaLinuxProcessParamsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def max_idle_time_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of time in seconds that a non-pinned Lambda function can idle before the AWS IoT Greengrass Core software stops its process.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-maxidletimeinseconds
            '''
            result = self._values.get("max_idle_time_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_instances_count(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of instances that a non-pinned Lambda function can run at the same time.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-maxinstancescount
            '''
            result = self._values.get("max_instances_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def max_queue_size(self) -> typing.Optional[jsii.Number]:
            '''The maximum size of the message queue for the Lambda function component.

            The AWS IoT Greengrass core device stores messages in a FIFO (first-in-first-out) queue until it can run the Lambda function to consume each message.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-maxqueuesize
            '''
            result = self._values.get("max_queue_size")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def pinned(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Whether or not the Lambda function is pinned, or long-lived.

            - A pinned Lambda function starts when the AWS IoT Greengrass Core starts and keeps running in its own container.
            - A non-pinned Lambda function starts only when it receives a work item and exists after it idles for ``maxIdleTimeInSeconds`` . If the function has multiple work items, the AWS IoT Greengrass Core software creates multiple instances of the function.

            Default: ``true``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-pinned
            '''
            result = self._values.get("pinned")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def status_timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The interval in seconds at which a pinned (also known as long-lived) Lambda function component sends status updates to the Lambda manager component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-statustimeoutinseconds
            '''
            result = self._values.get("status_timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of time in seconds that the Lambda function can process a work item.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdaexecutionparameters.html#cfn-greengrassv2-componentversion-lambdaexecutionparameters-timeoutinseconds
            '''
            result = self._values.get("timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaExecutionParametersProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnComponentVersion.LambdaFunctionRecipeSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_dependencies": "componentDependencies",
            "component_lambda_parameters": "componentLambdaParameters",
            "component_name": "componentName",
            "component_platforms": "componentPlatforms",
            "component_version": "componentVersion",
            "lambda_arn": "lambdaArn",
        },
    )
    class LambdaFunctionRecipeSourceProperty:
        def __init__(
            self,
            *,
            component_dependencies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnComponentVersion.ComponentDependencyRequirementProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            component_lambda_parameters: typing.Optional[typing.Union[typing.Union["CfnComponentVersion.LambdaExecutionParametersProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            component_name: typing.Optional[builtins.str] = None,
            component_platforms: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnComponentVersion.ComponentPlatformProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            component_version: typing.Optional[builtins.str] = None,
            lambda_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about an AWS Lambda function to import to create a component.

            :param component_dependencies: The component versions on which this Lambda function component depends.
            :param component_lambda_parameters: The system and runtime parameters for the Lambda function as it runs on the AWS IoT Greengrass core device.
            :param component_name: The name of the component. Defaults to the name of the Lambda function.
            :param component_platforms: The platforms that the component version supports.
            :param component_version: The version of the component. Defaults to the version of the Lambda function as a semantic version. For example, if your function version is ``3`` , the component version becomes ``3.0.0`` .
            :param lambda_arn: The ARN of the Lambda function. The ARN must include the version of the function to import. You can't use version aliases like ``$LATEST`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdafunctionrecipesource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                lambda_function_recipe_source_property = greengrassv2.CfnComponentVersion.LambdaFunctionRecipeSourceProperty(
                    component_dependencies={
                        "component_dependencies_key": greengrassv2.CfnComponentVersion.ComponentDependencyRequirementProperty(
                            dependency_type="dependencyType",
                            version_requirement="versionRequirement"
                        )
                    },
                    component_lambda_parameters=greengrassv2.CfnComponentVersion.LambdaExecutionParametersProperty(
                        environment_variables={
                            "environment_variables_key": "environmentVariables"
                        },
                        event_sources=[greengrassv2.CfnComponentVersion.LambdaEventSourceProperty(
                            topic="topic",
                            type="type"
                        )],
                        exec_args=["execArgs"],
                        input_payload_encoding_type="inputPayloadEncodingType",
                        linux_process_params=greengrassv2.CfnComponentVersion.LambdaLinuxProcessParamsProperty(
                            container_params=greengrassv2.CfnComponentVersion.LambdaContainerParamsProperty(
                                devices=[greengrassv2.CfnComponentVersion.LambdaDeviceMountProperty(
                                    add_group_owner=False,
                                    path="path",
                                    permission="permission"
                                )],
                                memory_size_in_kb=123,
                                mount_ro_sysfs=False,
                                volumes=[greengrassv2.CfnComponentVersion.LambdaVolumeMountProperty(
                                    add_group_owner=False,
                                    destination_path="destinationPath",
                                    permission="permission",
                                    source_path="sourcePath"
                                )]
                            ),
                            isolation_mode="isolationMode"
                        ),
                        max_idle_time_in_seconds=123,
                        max_instances_count=123,
                        max_queue_size=123,
                        pinned=False,
                        status_timeout_in_seconds=123,
                        timeout_in_seconds=123
                    ),
                    component_name="componentName",
                    component_platforms=[greengrassv2.CfnComponentVersion.ComponentPlatformProperty(
                        attributes={
                            "attributes_key": "attributes"
                        },
                        name="name"
                    )],
                    component_version="componentVersion",
                    lambda_arn="lambdaArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8fa2878407d907f9cf40cfe5146e23e6c305973019a998d7756a028906e64c74)
                check_type(argname="argument component_dependencies", value=component_dependencies, expected_type=type_hints["component_dependencies"])
                check_type(argname="argument component_lambda_parameters", value=component_lambda_parameters, expected_type=type_hints["component_lambda_parameters"])
                check_type(argname="argument component_name", value=component_name, expected_type=type_hints["component_name"])
                check_type(argname="argument component_platforms", value=component_platforms, expected_type=type_hints["component_platforms"])
                check_type(argname="argument component_version", value=component_version, expected_type=type_hints["component_version"])
                check_type(argname="argument lambda_arn", value=lambda_arn, expected_type=type_hints["lambda_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_dependencies is not None:
                self._values["component_dependencies"] = component_dependencies
            if component_lambda_parameters is not None:
                self._values["component_lambda_parameters"] = component_lambda_parameters
            if component_name is not None:
                self._values["component_name"] = component_name
            if component_platforms is not None:
                self._values["component_platforms"] = component_platforms
            if component_version is not None:
                self._values["component_version"] = component_version
            if lambda_arn is not None:
                self._values["lambda_arn"] = lambda_arn

        @builtins.property
        def component_dependencies(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponentVersion.ComponentDependencyRequirementProperty", _IResolvable_a771d0ef]]]]:
            '''The component versions on which this Lambda function component depends.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdafunctionrecipesource.html#cfn-greengrassv2-componentversion-lambdafunctionrecipesource-componentdependencies
            '''
            result = self._values.get("component_dependencies")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnComponentVersion.ComponentDependencyRequirementProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def component_lambda_parameters(
            self,
        ) -> typing.Optional[typing.Union["CfnComponentVersion.LambdaExecutionParametersProperty", _IResolvable_a771d0ef]]:
            '''The system and runtime parameters for the Lambda function as it runs on the AWS IoT Greengrass core device.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdafunctionrecipesource.html#cfn-greengrassv2-componentversion-lambdafunctionrecipesource-componentlambdaparameters
            '''
            result = self._values.get("component_lambda_parameters")
            return typing.cast(typing.Optional[typing.Union["CfnComponentVersion.LambdaExecutionParametersProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def component_name(self) -> typing.Optional[builtins.str]:
            '''The name of the component.

            Defaults to the name of the Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdafunctionrecipesource.html#cfn-greengrassv2-componentversion-lambdafunctionrecipesource-componentname
            '''
            result = self._values.get("component_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def component_platforms(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponentVersion.ComponentPlatformProperty", _IResolvable_a771d0ef]]]]:
            '''The platforms that the component version supports.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdafunctionrecipesource.html#cfn-greengrassv2-componentversion-lambdafunctionrecipesource-componentplatforms
            '''
            result = self._values.get("component_platforms")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnComponentVersion.ComponentPlatformProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def component_version(self) -> typing.Optional[builtins.str]:
            '''The version of the component.

            Defaults to the version of the Lambda function as a semantic version. For example, if your function version is ``3`` , the component version becomes ``3.0.0`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdafunctionrecipesource.html#cfn-greengrassv2-componentversion-lambdafunctionrecipesource-componentversion
            '''
            result = self._values.get("component_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def lambda_arn(self) -> typing.Optional[builtins.str]:
            '''The ARN of the Lambda function.

            The ARN must include the version of the function to import. You can't use version aliases like ``$LATEST`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdafunctionrecipesource.html#cfn-greengrassv2-componentversion-lambdafunctionrecipesource-lambdaarn
            '''
            result = self._values.get("lambda_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaFunctionRecipeSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnComponentVersion.LambdaLinuxProcessParamsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "container_params": "containerParams",
            "isolation_mode": "isolationMode",
        },
    )
    class LambdaLinuxProcessParamsProperty:
        def __init__(
            self,
            *,
            container_params: typing.Optional[typing.Union[typing.Union["CfnComponentVersion.LambdaContainerParamsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            isolation_mode: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains parameters for a Linux process that contains an AWS Lambda function.

            :param container_params: The parameters for the container in which the Lambda function runs.
            :param isolation_mode: The isolation mode for the process that contains the Lambda function. The process can run in an isolated runtime environment inside the AWS IoT Greengrass container, or as a regular process outside any container. Default: ``GreengrassContainer``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdalinuxprocessparams.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                lambda_linux_process_params_property = greengrassv2.CfnComponentVersion.LambdaLinuxProcessParamsProperty(
                    container_params=greengrassv2.CfnComponentVersion.LambdaContainerParamsProperty(
                        devices=[greengrassv2.CfnComponentVersion.LambdaDeviceMountProperty(
                            add_group_owner=False,
                            path="path",
                            permission="permission"
                        )],
                        memory_size_in_kb=123,
                        mount_ro_sysfs=False,
                        volumes=[greengrassv2.CfnComponentVersion.LambdaVolumeMountProperty(
                            add_group_owner=False,
                            destination_path="destinationPath",
                            permission="permission",
                            source_path="sourcePath"
                        )]
                    ),
                    isolation_mode="isolationMode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a84c2e346dd2e08aac3bb2df5f5f31297462946f1db412969c0766c162683c03)
                check_type(argname="argument container_params", value=container_params, expected_type=type_hints["container_params"])
                check_type(argname="argument isolation_mode", value=isolation_mode, expected_type=type_hints["isolation_mode"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if container_params is not None:
                self._values["container_params"] = container_params
            if isolation_mode is not None:
                self._values["isolation_mode"] = isolation_mode

        @builtins.property
        def container_params(
            self,
        ) -> typing.Optional[typing.Union["CfnComponentVersion.LambdaContainerParamsProperty", _IResolvable_a771d0ef]]:
            '''The parameters for the container in which the Lambda function runs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdalinuxprocessparams.html#cfn-greengrassv2-componentversion-lambdalinuxprocessparams-containerparams
            '''
            result = self._values.get("container_params")
            return typing.cast(typing.Optional[typing.Union["CfnComponentVersion.LambdaContainerParamsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def isolation_mode(self) -> typing.Optional[builtins.str]:
            '''The isolation mode for the process that contains the Lambda function.

            The process can run in an isolated runtime environment inside the AWS IoT Greengrass container, or as a regular process outside any container.

            Default: ``GreengrassContainer``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdalinuxprocessparams.html#cfn-greengrassv2-componentversion-lambdalinuxprocessparams-isolationmode
            '''
            result = self._values.get("isolation_mode")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaLinuxProcessParamsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnComponentVersion.LambdaVolumeMountProperty",
        jsii_struct_bases=[],
        name_mapping={
            "add_group_owner": "addGroupOwner",
            "destination_path": "destinationPath",
            "permission": "permission",
            "source_path": "sourcePath",
        },
    )
    class LambdaVolumeMountProperty:
        def __init__(
            self,
            *,
            add_group_owner: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            destination_path: typing.Optional[builtins.str] = None,
            permission: typing.Optional[builtins.str] = None,
            source_path: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about a volume that Linux processes in a container can access.

            When you define a volume, the AWS IoT Greengrass Core software mounts the source files to the destination inside the container.

            :param add_group_owner: Whether or not to add the AWS IoT Greengrass user group as an owner of the volume. Default: ``false``
            :param destination_path: The path to the logical volume in the file system.
            :param permission: The permission to access the volume: read/only ( ``ro`` ) or read/write ( ``rw`` ). Default: ``ro``
            :param source_path: The path to the physical volume in the file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdavolumemount.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                lambda_volume_mount_property = greengrassv2.CfnComponentVersion.LambdaVolumeMountProperty(
                    add_group_owner=False,
                    destination_path="destinationPath",
                    permission="permission",
                    source_path="sourcePath"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fe6c5550aec759bb5e48ba9a97bd37dd5cebc03608100593b67ebe3b39afa543)
                check_type(argname="argument add_group_owner", value=add_group_owner, expected_type=type_hints["add_group_owner"])
                check_type(argname="argument destination_path", value=destination_path, expected_type=type_hints["destination_path"])
                check_type(argname="argument permission", value=permission, expected_type=type_hints["permission"])
                check_type(argname="argument source_path", value=source_path, expected_type=type_hints["source_path"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if add_group_owner is not None:
                self._values["add_group_owner"] = add_group_owner
            if destination_path is not None:
                self._values["destination_path"] = destination_path
            if permission is not None:
                self._values["permission"] = permission
            if source_path is not None:
                self._values["source_path"] = source_path

        @builtins.property
        def add_group_owner(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Whether or not to add the AWS IoT Greengrass user group as an owner of the volume.

            Default: ``false``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdavolumemount.html#cfn-greengrassv2-componentversion-lambdavolumemount-addgroupowner
            '''
            result = self._values.get("add_group_owner")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def destination_path(self) -> typing.Optional[builtins.str]:
            '''The path to the logical volume in the file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdavolumemount.html#cfn-greengrassv2-componentversion-lambdavolumemount-destinationpath
            '''
            result = self._values.get("destination_path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def permission(self) -> typing.Optional[builtins.str]:
            '''The permission to access the volume: read/only ( ``ro`` ) or read/write ( ``rw`` ).

            Default: ``ro``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdavolumemount.html#cfn-greengrassv2-componentversion-lambdavolumemount-permission
            '''
            result = self._values.get("permission")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def source_path(self) -> typing.Optional[builtins.str]:
            '''The path to the physical volume in the file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-componentversion-lambdavolumemount.html#cfn-greengrassv2-componentversion-lambdavolumemount-sourcepath
            '''
            result = self._values.get("source_path")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LambdaVolumeMountProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_greengrassv2.CfnComponentVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "inline_recipe": "inlineRecipe",
        "lambda_function": "lambdaFunction",
        "tags": "tags",
    },
)
class CfnComponentVersionProps:
    def __init__(
        self,
        *,
        inline_recipe: typing.Optional[builtins.str] = None,
        lambda_function: typing.Optional[typing.Union[typing.Union[CfnComponentVersion.LambdaFunctionRecipeSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnComponentVersion``.

        :param inline_recipe: The recipe to use to create the component. The recipe defines the component's metadata, parameters, dependencies, lifecycle, artifacts, and platform compatibility. You must specify either ``InlineRecipe`` or ``LambdaFunction`` .
        :param lambda_function: The parameters to create a component from a Lambda function. You must specify either ``InlineRecipe`` or ``LambdaFunction`` .
        :param tags: Application-specific metadata to attach to the component version. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tag your AWS IoT Greengrass Version 2 resources <https://docs.aws.amazon.com/greengrass/v2/developerguide/tag-resources.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-componentversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_greengrassv2 as greengrassv2
            
            cfn_component_version_props = greengrassv2.CfnComponentVersionProps(
                inline_recipe="inlineRecipe",
                lambda_function=greengrassv2.CfnComponentVersion.LambdaFunctionRecipeSourceProperty(
                    component_dependencies={
                        "component_dependencies_key": greengrassv2.CfnComponentVersion.ComponentDependencyRequirementProperty(
                            dependency_type="dependencyType",
                            version_requirement="versionRequirement"
                        )
                    },
                    component_lambda_parameters=greengrassv2.CfnComponentVersion.LambdaExecutionParametersProperty(
                        environment_variables={
                            "environment_variables_key": "environmentVariables"
                        },
                        event_sources=[greengrassv2.CfnComponentVersion.LambdaEventSourceProperty(
                            topic="topic",
                            type="type"
                        )],
                        exec_args=["execArgs"],
                        input_payload_encoding_type="inputPayloadEncodingType",
                        linux_process_params=greengrassv2.CfnComponentVersion.LambdaLinuxProcessParamsProperty(
                            container_params=greengrassv2.CfnComponentVersion.LambdaContainerParamsProperty(
                                devices=[greengrassv2.CfnComponentVersion.LambdaDeviceMountProperty(
                                    add_group_owner=False,
                                    path="path",
                                    permission="permission"
                                )],
                                memory_size_in_kb=123,
                                mount_ro_sysfs=False,
                                volumes=[greengrassv2.CfnComponentVersion.LambdaVolumeMountProperty(
                                    add_group_owner=False,
                                    destination_path="destinationPath",
                                    permission="permission",
                                    source_path="sourcePath"
                                )]
                            ),
                            isolation_mode="isolationMode"
                        ),
                        max_idle_time_in_seconds=123,
                        max_instances_count=123,
                        max_queue_size=123,
                        pinned=False,
                        status_timeout_in_seconds=123,
                        timeout_in_seconds=123
                    ),
                    component_name="componentName",
                    component_platforms=[greengrassv2.CfnComponentVersion.ComponentPlatformProperty(
                        attributes={
                            "attributes_key": "attributes"
                        },
                        name="name"
                    )],
                    component_version="componentVersion",
                    lambda_arn="lambdaArn"
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a1d300df7036df025b73636bea689d9af2bab1ce9f631b0a5249efcf4164f9b)
            check_type(argname="argument inline_recipe", value=inline_recipe, expected_type=type_hints["inline_recipe"])
            check_type(argname="argument lambda_function", value=lambda_function, expected_type=type_hints["lambda_function"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if inline_recipe is not None:
            self._values["inline_recipe"] = inline_recipe
        if lambda_function is not None:
            self._values["lambda_function"] = lambda_function
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def inline_recipe(self) -> typing.Optional[builtins.str]:
        '''The recipe to use to create the component.

        The recipe defines the component's metadata, parameters, dependencies, lifecycle, artifacts, and platform compatibility.

        You must specify either ``InlineRecipe`` or ``LambdaFunction`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-componentversion.html#cfn-greengrassv2-componentversion-inlinerecipe
        '''
        result = self._values.get("inline_recipe")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lambda_function(
        self,
    ) -> typing.Optional[typing.Union[CfnComponentVersion.LambdaFunctionRecipeSourceProperty, _IResolvable_a771d0ef]]:
        '''The parameters to create a component from a Lambda function.

        You must specify either ``InlineRecipe`` or ``LambdaFunction`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-componentversion.html#cfn-greengrassv2-componentversion-lambdafunction
        '''
        result = self._values.get("lambda_function")
        return typing.cast(typing.Optional[typing.Union[CfnComponentVersion.LambdaFunctionRecipeSourceProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Application-specific metadata to attach to the component version.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tag your AWS IoT Greengrass Version 2 resources <https://docs.aws.amazon.com/greengrass/v2/developerguide/tag-resources.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-componentversion.html#cfn-greengrassv2-componentversion-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnComponentVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDeployment(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_greengrassv2.CfnDeployment",
):
    '''A CloudFormation ``AWS::GreengrassV2::Deployment``.

    Creates a continuous deployment for a target, which is a AWS IoT Greengrass core device or group of core devices. When you add a new core device to a group of core devices that has a deployment, AWS IoT Greengrass deploys that group's deployment to the new device.

    You can define one deployment for each target. When you create a new deployment for a target that has an existing deployment, you replace the previous deployment. AWS IoT Greengrass applies the new deployment to the target devices.

    You can only add, update, or delete up to 10 deployments at a time to a single target.

    Every deployment has a revision number that indicates how many deployment revisions you define for a target. Use this operation to create a new revision of an existing deployment. This operation returns the revision number of the new deployment when you create it.

    For more information, see the `Create deployments <https://docs.aws.amazon.com/greengrass/v2/latest/developerguide/create-deployments.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .
    .. epigraph::

       Deployment resources are deleted when you delete stacks. To keep the deployments in a stack, you must specify ``"DeletionPolicy": "Retain"`` on each deployment resource in the stack template that you want to keep. For more information, see `DeletionPolicy <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-attribute-deletionpolicy.html>`_ .

       You can only delete up to 10 deployment resources at a time. If you delete more than 10 resources, you receive an error.

    :cloudformationResource: AWS::GreengrassV2::Deployment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_greengrassv2 as greengrassv2
        
        # rate_increase_criteria: Any
        
        cfn_deployment = greengrassv2.CfnDeployment(self, "MyCfnDeployment",
            target_arn="targetArn",
        
            # the properties below are optional
            components={
                "components_key": greengrassv2.CfnDeployment.ComponentDeploymentSpecificationProperty(
                    component_version="componentVersion",
                    configuration_update=greengrassv2.CfnDeployment.ComponentConfigurationUpdateProperty(
                        merge="merge",
                        reset=["reset"]
                    ),
                    run_with=greengrassv2.CfnDeployment.ComponentRunWithProperty(
                        posix_user="posixUser",
                        system_resource_limits=greengrassv2.CfnDeployment.SystemResourceLimitsProperty(
                            cpus=123,
                            memory=123
                        ),
                        windows_user="windowsUser"
                    )
                )
            },
            deployment_name="deploymentName",
            deployment_policies=greengrassv2.CfnDeployment.DeploymentPoliciesProperty(
                component_update_policy=greengrassv2.CfnDeployment.DeploymentComponentUpdatePolicyProperty(
                    action="action",
                    timeout_in_seconds=123
                ),
                configuration_validation_policy=greengrassv2.CfnDeployment.DeploymentConfigurationValidationPolicyProperty(
                    timeout_in_seconds=123
                ),
                failure_handling_policy="failureHandlingPolicy"
            ),
            iot_job_configuration=greengrassv2.CfnDeployment.DeploymentIoTJobConfigurationProperty(
                abort_config=greengrassv2.CfnDeployment.IoTJobAbortConfigProperty(
                    criteria_list=[greengrassv2.CfnDeployment.IoTJobAbortCriteriaProperty(
                        action="action",
                        failure_type="failureType",
                        min_number_of_executed_things=123,
                        threshold_percentage=123
                    )]
                ),
                job_executions_rollout_config=greengrassv2.CfnDeployment.IoTJobExecutionsRolloutConfigProperty(
                    exponential_rate=greengrassv2.CfnDeployment.IoTJobExponentialRolloutRateProperty(
                        base_rate_per_minute=123,
                        increment_factor=123,
                        rate_increase_criteria=rate_increase_criteria
                    ),
                    maximum_per_minute=123
                ),
                timeout_config=greengrassv2.CfnDeployment.IoTJobTimeoutConfigProperty(
                    in_progress_timeout_in_minutes=123
                )
            ),
            tags={
                "tags_key": "tags"
            }
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        target_arn: builtins.str,
        components: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnDeployment.ComponentDeploymentSpecificationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        deployment_name: typing.Optional[builtins.str] = None,
        deployment_policies: typing.Optional[typing.Union[typing.Union["CfnDeployment.DeploymentPoliciesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        iot_job_configuration: typing.Optional[typing.Union[typing.Union["CfnDeployment.DeploymentIoTJobConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::GreengrassV2::Deployment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param target_arn: The ARN of the target AWS IoT thing or thing group.
        :param components: The components to deploy. This is a dictionary, where each key is the name of a component, and each key's value is the version and configuration to deploy for that component.
        :param deployment_name: The name of the deployment.
        :param deployment_policies: The deployment policies for the deployment. These policies define how the deployment updates components and handles failure.
        :param iot_job_configuration: The job configuration for the deployment configuration. The job configuration specifies the rollout, timeout, and stop configurations for the deployment configuration.
        :param tags: Application-specific metadata to attach to the deployment. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tag your AWS IoT Greengrass Version 2 resources <https://docs.aws.amazon.com/greengrass/v2/developerguide/tag-resources.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99e732ca39ddcada02a116f52e0ce75f19737af7f42b25924073b503b01a0643)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDeploymentProps(
            target_arn=target_arn,
            components=components,
            deployment_name=deployment_name,
            deployment_policies=deployment_policies,
            iot_job_configuration=iot_job_configuration,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__578649b46579783b9d0421ed49592fd16c87b8b2ce4e945f662d3fd7966e71a3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3a73abf67ec3457b7d02ca8be4126e0c3ecebb2a3c665a1b2d2ae1993dcb574)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrDeploymentId")
    def attr_deployment_id(self) -> builtins.str:
        '''The ID of the deployment.

        :cloudformationAttribute: DeploymentId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDeploymentId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Application-specific metadata to attach to the deployment.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tag your AWS IoT Greengrass Version 2 resources <https://docs.aws.amazon.com/greengrass/v2/developerguide/tag-resources.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="targetArn")
    def target_arn(self) -> builtins.str:
        '''The ARN of the target AWS IoT thing or thing group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-targetarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "targetArn"))

    @target_arn.setter
    def target_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e9d72418e960a4a4fd6879c4d082e5aa077a8cb08f0c4c36de1384f339211ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetArn", value)

    @builtins.property
    @jsii.member(jsii_name="components")
    def components(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnDeployment.ComponentDeploymentSpecificationProperty", _IResolvable_a771d0ef]]]]:
        '''The components to deploy.

        This is a dictionary, where each key is the name of a component, and each key's value is the version and configuration to deploy for that component.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-components
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnDeployment.ComponentDeploymentSpecificationProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "components"))

    @components.setter
    def components(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnDeployment.ComponentDeploymentSpecificationProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a13aacacc96f5eb2979e446d8145ac6c29f7c7841b2366ee47127bedbd68977d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "components", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentName")
    def deployment_name(self) -> typing.Optional[builtins.str]:
        '''The name of the deployment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-deploymentname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deploymentName"))

    @deployment_name.setter
    def deployment_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ec29a9aa0935488a334c3a19e8b9b4c0afa9364c0239aaa4788cb5d3771585f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentName", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentPolicies")
    def deployment_policies(
        self,
    ) -> typing.Optional[typing.Union["CfnDeployment.DeploymentPoliciesProperty", _IResolvable_a771d0ef]]:
        '''The deployment policies for the deployment.

        These policies define how the deployment updates components and handles failure.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-deploymentpolicies
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDeployment.DeploymentPoliciesProperty", _IResolvable_a771d0ef]], jsii.get(self, "deploymentPolicies"))

    @deployment_policies.setter
    def deployment_policies(
        self,
        value: typing.Optional[typing.Union["CfnDeployment.DeploymentPoliciesProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc1dc5630343bc19b06adbc7d438837b32859a77686c0a99afad7ab5fae18375)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentPolicies", value)

    @builtins.property
    @jsii.member(jsii_name="iotJobConfiguration")
    def iot_job_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnDeployment.DeploymentIoTJobConfigurationProperty", _IResolvable_a771d0ef]]:
        '''The job configuration for the deployment configuration.

        The job configuration specifies the rollout, timeout, and stop configurations for the deployment configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-iotjobconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnDeployment.DeploymentIoTJobConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "iotJobConfiguration"))

    @iot_job_configuration.setter
    def iot_job_configuration(
        self,
        value: typing.Optional[typing.Union["CfnDeployment.DeploymentIoTJobConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__248dbb8b6bfc5db9850ead36b6f76c87cda7bee7862cde09b6811b4e19bbc9cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iotJobConfiguration", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnDeployment.ComponentConfigurationUpdateProperty",
        jsii_struct_bases=[],
        name_mapping={"merge": "merge", "reset": "reset"},
    )
    class ComponentConfigurationUpdateProperty:
        def __init__(
            self,
            *,
            merge: typing.Optional[builtins.str] = None,
            reset: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Contains information about a deployment's update to a component's configuration on AWS IoT Greengrass core devices.

            For more information, see `Update component configurations <https://docs.aws.amazon.com/greengrass/v2/developerguide/update-component-configurations.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :param merge: A serialized JSON string that contains the configuration object to merge to target devices. The core device merges this configuration with the component's existing configuration. If this is the first time a component deploys on a device, the core device merges this configuration with the component's default configuration. This means that the core device keeps it's existing configuration for keys and values that you don't specify in this object. For more information, see `Merge configuration updates <https://docs.aws.amazon.com/greengrass/v2/developerguide/update-component-configurations.html#merge-configuration-update>`_ in the *AWS IoT Greengrass V2 Developer Guide* .
            :param reset: The list of configuration nodes to reset to default values on target devices. Use JSON pointers to specify each node to reset. JSON pointers start with a forward slash ( ``/`` ) and use forward slashes to separate the key for each level in the object. For more information, see the `JSON pointer specification <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc6901>`_ and `Reset configuration updates <https://docs.aws.amazon.com/greengrass/v2/developerguide/update-component-configurations.html#reset-configuration-update>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentconfigurationupdate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                component_configuration_update_property = greengrassv2.CfnDeployment.ComponentConfigurationUpdateProperty(
                    merge="merge",
                    reset=["reset"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f16d59a933932d581729af72d04bb49cc11188ebab2abf6b7f848f9ad464e31f)
                check_type(argname="argument merge", value=merge, expected_type=type_hints["merge"])
                check_type(argname="argument reset", value=reset, expected_type=type_hints["reset"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if merge is not None:
                self._values["merge"] = merge
            if reset is not None:
                self._values["reset"] = reset

        @builtins.property
        def merge(self) -> typing.Optional[builtins.str]:
            '''A serialized JSON string that contains the configuration object to merge to target devices.

            The core device merges this configuration with the component's existing configuration. If this is the first time a component deploys on a device, the core device merges this configuration with the component's default configuration. This means that the core device keeps it's existing configuration for keys and values that you don't specify in this object. For more information, see `Merge configuration updates <https://docs.aws.amazon.com/greengrass/v2/developerguide/update-component-configurations.html#merge-configuration-update>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentconfigurationupdate.html#cfn-greengrassv2-deployment-componentconfigurationupdate-merge
            '''
            result = self._values.get("merge")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def reset(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of configuration nodes to reset to default values on target devices.

            Use JSON pointers to specify each node to reset. JSON pointers start with a forward slash ( ``/`` ) and use forward slashes to separate the key for each level in the object. For more information, see the `JSON pointer specification <https://docs.aws.amazon.com/https://tools.ietf.org/html/rfc6901>`_ and `Reset configuration updates <https://docs.aws.amazon.com/greengrass/v2/developerguide/update-component-configurations.html#reset-configuration-update>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentconfigurationupdate.html#cfn-greengrassv2-deployment-componentconfigurationupdate-reset
            '''
            result = self._values.get("reset")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentConfigurationUpdateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnDeployment.ComponentDeploymentSpecificationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_version": "componentVersion",
            "configuration_update": "configurationUpdate",
            "run_with": "runWith",
        },
    )
    class ComponentDeploymentSpecificationProperty:
        def __init__(
            self,
            *,
            component_version: typing.Optional[builtins.str] = None,
            configuration_update: typing.Optional[typing.Union[typing.Union["CfnDeployment.ComponentConfigurationUpdateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            run_with: typing.Optional[typing.Union[typing.Union["CfnDeployment.ComponentRunWithProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Contains information about a component to deploy.

            :param component_version: The version of the component.
            :param configuration_update: The configuration updates to deploy for the component. You can define reset updates and merge updates. A reset updates the keys that you specify to the default configuration for the component. A merge updates the core device's component configuration with the keys and values that you specify. The AWS IoT Greengrass Core software applies reset updates before it applies merge updates. For more information, see `Update component configuration <https://docs.aws.amazon.com/greengrass/v2/developerguide/update-component-configurations.html>`_ .
            :param run_with: The system user and group that the software uses to run component processes on the core device. If you omit this parameter, the software uses the system user and group that you configure for the core device. For more information, see `Configure the user and group that run components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-user>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentdeploymentspecification.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                component_deployment_specification_property = greengrassv2.CfnDeployment.ComponentDeploymentSpecificationProperty(
                    component_version="componentVersion",
                    configuration_update=greengrassv2.CfnDeployment.ComponentConfigurationUpdateProperty(
                        merge="merge",
                        reset=["reset"]
                    ),
                    run_with=greengrassv2.CfnDeployment.ComponentRunWithProperty(
                        posix_user="posixUser",
                        system_resource_limits=greengrassv2.CfnDeployment.SystemResourceLimitsProperty(
                            cpus=123,
                            memory=123
                        ),
                        windows_user="windowsUser"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__886b1eddb14044b2d4d525a1b37724f3cf9957f456651e4c88d7a95f448372d0)
                check_type(argname="argument component_version", value=component_version, expected_type=type_hints["component_version"])
                check_type(argname="argument configuration_update", value=configuration_update, expected_type=type_hints["configuration_update"])
                check_type(argname="argument run_with", value=run_with, expected_type=type_hints["run_with"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_version is not None:
                self._values["component_version"] = component_version
            if configuration_update is not None:
                self._values["configuration_update"] = configuration_update
            if run_with is not None:
                self._values["run_with"] = run_with

        @builtins.property
        def component_version(self) -> typing.Optional[builtins.str]:
            '''The version of the component.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentdeploymentspecification.html#cfn-greengrassv2-deployment-componentdeploymentspecification-componentversion
            '''
            result = self._values.get("component_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def configuration_update(
            self,
        ) -> typing.Optional[typing.Union["CfnDeployment.ComponentConfigurationUpdateProperty", _IResolvable_a771d0ef]]:
            '''The configuration updates to deploy for the component.

            You can define reset updates and merge updates. A reset updates the keys that you specify to the default configuration for the component. A merge updates the core device's component configuration with the keys and values that you specify. The AWS IoT Greengrass Core software applies reset updates before it applies merge updates. For more information, see `Update component configuration <https://docs.aws.amazon.com/greengrass/v2/developerguide/update-component-configurations.html>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentdeploymentspecification.html#cfn-greengrassv2-deployment-componentdeploymentspecification-configurationupdate
            '''
            result = self._values.get("configuration_update")
            return typing.cast(typing.Optional[typing.Union["CfnDeployment.ComponentConfigurationUpdateProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def run_with(
            self,
        ) -> typing.Optional[typing.Union["CfnDeployment.ComponentRunWithProperty", _IResolvable_a771d0ef]]:
            '''The system user and group that the  software uses to run component processes on the core device.

            If you omit this parameter, the  software uses the system user and group that you configure for the core device. For more information, see `Configure the user and group that run components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-user>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentdeploymentspecification.html#cfn-greengrassv2-deployment-componentdeploymentspecification-runwith
            '''
            result = self._values.get("run_with")
            return typing.cast(typing.Optional[typing.Union["CfnDeployment.ComponentRunWithProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentDeploymentSpecificationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnDeployment.ComponentRunWithProperty",
        jsii_struct_bases=[],
        name_mapping={
            "posix_user": "posixUser",
            "system_resource_limits": "systemResourceLimits",
            "windows_user": "windowsUser",
        },
    )
    class ComponentRunWithProperty:
        def __init__(
            self,
            *,
            posix_user: typing.Optional[builtins.str] = None,
            system_resource_limits: typing.Optional[typing.Union[typing.Union["CfnDeployment.SystemResourceLimitsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            windows_user: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information system user and group that the AWS IoT Greengrass Core software uses to run component processes on the core device.

            For more information, see `Configure the user and group that run components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-user>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :param posix_user: The POSIX system user and (optional) group to use to run this component. Specify the user and group separated by a colon ( ``:`` ) in the following format: ``user:group`` . The group is optional. If you don't specify a group, the AWS IoT Greengrass Core software uses the primary user for the group.
            :param system_resource_limits: The system resource limits to apply to this component's process on the core device. AWS IoT Greengrass supports this feature only on Linux core devices. If you omit this parameter, the AWS IoT Greengrass Core software uses the default system resource limits that you configure on the AWS IoT Greengrass nucleus component. For more information, see `Configure system resource limits for components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-system-resource-limits>`_ .
            :param windows_user: The Windows user to use to run this component on Windows core devices. The user must exist on each Windows core device, and its name and password must be in the LocalSystem account's Credentials Manager instance. If you omit this parameter, the AWS IoT Greengrass Core software uses the default Windows user that you configure on the AWS IoT Greengrass nucleus component. For more information, see `Configure the user and group that run components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-user>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentrunwith.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                component_run_with_property = greengrassv2.CfnDeployment.ComponentRunWithProperty(
                    posix_user="posixUser",
                    system_resource_limits=greengrassv2.CfnDeployment.SystemResourceLimitsProperty(
                        cpus=123,
                        memory=123
                    ),
                    windows_user="windowsUser"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0bc1762e82a98eb850efa4dd5845e7699f153f371b18b78c954ce4dec4029bca)
                check_type(argname="argument posix_user", value=posix_user, expected_type=type_hints["posix_user"])
                check_type(argname="argument system_resource_limits", value=system_resource_limits, expected_type=type_hints["system_resource_limits"])
                check_type(argname="argument windows_user", value=windows_user, expected_type=type_hints["windows_user"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if posix_user is not None:
                self._values["posix_user"] = posix_user
            if system_resource_limits is not None:
                self._values["system_resource_limits"] = system_resource_limits
            if windows_user is not None:
                self._values["windows_user"] = windows_user

        @builtins.property
        def posix_user(self) -> typing.Optional[builtins.str]:
            '''The POSIX system user and (optional) group to use to run this component.

            Specify the user and group separated by a colon ( ``:`` ) in the following format: ``user:group`` . The group is optional. If you don't specify a group, the AWS IoT Greengrass Core software uses the primary user for the group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentrunwith.html#cfn-greengrassv2-deployment-componentrunwith-posixuser
            '''
            result = self._values.get("posix_user")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def system_resource_limits(
            self,
        ) -> typing.Optional[typing.Union["CfnDeployment.SystemResourceLimitsProperty", _IResolvable_a771d0ef]]:
            '''The system resource limits to apply to this component's process on the core device.

            AWS IoT Greengrass supports this feature only on Linux core devices.

            If you omit this parameter, the AWS IoT Greengrass Core software uses the default system resource limits that you configure on the AWS IoT Greengrass nucleus component. For more information, see `Configure system resource limits for components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-system-resource-limits>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentrunwith.html#cfn-greengrassv2-deployment-componentrunwith-systemresourcelimits
            '''
            result = self._values.get("system_resource_limits")
            return typing.cast(typing.Optional[typing.Union["CfnDeployment.SystemResourceLimitsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def windows_user(self) -> typing.Optional[builtins.str]:
            '''The Windows user to use to run this component on Windows core devices.

            The user must exist on each Windows core device, and its name and password must be in the LocalSystem account's Credentials Manager instance.

            If you omit this parameter, the AWS IoT Greengrass Core software uses the default Windows user that you configure on the AWS IoT Greengrass nucleus component. For more information, see `Configure the user and group that run components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-user>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-componentrunwith.html#cfn-greengrassv2-deployment-componentrunwith-windowsuser
            '''
            result = self._values.get("windows_user")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ComponentRunWithProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnDeployment.DeploymentComponentUpdatePolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action", "timeout_in_seconds": "timeoutInSeconds"},
    )
    class DeploymentComponentUpdatePolicyProperty:
        def __init__(
            self,
            *,
            action: typing.Optional[builtins.str] = None,
            timeout_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains information about a deployment's policy that defines when components are safe to update.

            Each component on a device can report whether or not it's ready to update. After a component and its dependencies are ready, they can apply the update in the deployment. You can configure whether or not the deployment notifies components of an update and waits for a response. You specify the amount of time each component has to respond to the update notification.

            :param action: Whether or not to notify components and wait for components to become safe to update. Choose from the following options: - ``NOTIFY_COMPONENTS`` – The deployment notifies each component before it stops and updates that component. Components can use the `SubscribeToComponentUpdates <https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-operation-subscribetocomponentupdates>`_ IPC operation to receive these notifications. Then, components can respond with the `DeferComponentUpdate <https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-operation-defercomponentupdate>`_ IPC operation. For more information, see the `Create deployments <https://docs.aws.amazon.com/greengrass/v2/latest/developerguide/create-deployments.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* . - ``SKIP_NOTIFY_COMPONENTS`` – The deployment doesn't notify components or wait for them to be safe to update. Default: ``NOTIFY_COMPONENTS``
            :param timeout_in_seconds: The amount of time in seconds that each component on a device has to report that it's safe to update. If the component waits for longer than this timeout, then the deployment proceeds on the device. Default: ``60``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentcomponentupdatepolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                deployment_component_update_policy_property = greengrassv2.CfnDeployment.DeploymentComponentUpdatePolicyProperty(
                    action="action",
                    timeout_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4fd09e96c8d3aa2bdbc501ae47e3560207f41696c8fcebcd5700f70066e4f5fc)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action
            if timeout_in_seconds is not None:
                self._values["timeout_in_seconds"] = timeout_in_seconds

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''Whether or not to notify components and wait for components to become safe to update.

            Choose from the following options:

            - ``NOTIFY_COMPONENTS`` – The deployment notifies each component before it stops and updates that component. Components can use the `SubscribeToComponentUpdates <https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-operation-subscribetocomponentupdates>`_ IPC operation to receive these notifications. Then, components can respond with the `DeferComponentUpdate <https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-operation-defercomponentupdate>`_ IPC operation. For more information, see the `Create deployments <https://docs.aws.amazon.com/greengrass/v2/latest/developerguide/create-deployments.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .
            - ``SKIP_NOTIFY_COMPONENTS`` – The deployment doesn't notify components or wait for them to be safe to update.

            Default: ``NOTIFY_COMPONENTS``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentcomponentupdatepolicy.html#cfn-greengrassv2-deployment-deploymentcomponentupdatepolicy-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The amount of time in seconds that each component on a device has to report that it's safe to update.

            If the component waits for longer than this timeout, then the deployment proceeds on the device.

            Default: ``60``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentcomponentupdatepolicy.html#cfn-greengrassv2-deployment-deploymentcomponentupdatepolicy-timeoutinseconds
            '''
            result = self._values.get("timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentComponentUpdatePolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnDeployment.DeploymentConfigurationValidationPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"timeout_in_seconds": "timeoutInSeconds"},
    )
    class DeploymentConfigurationValidationPolicyProperty:
        def __init__(
            self,
            *,
            timeout_in_seconds: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains information about how long a component on a core device can validate its configuration updates before it times out.

            Components can use the `SubscribeToValidateConfigurationUpdates <https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-operation-subscribetovalidateconfigurationupdates>`_ IPC operation to receive notifications when a deployment specifies a configuration update. Then, components can respond with the `SendConfigurationValidityReport <https://docs.aws.amazon.com/greengrass/v2/developerguide/interprocess-communication.html#ipc-operation-sendconfigurationvalidityreport>`_ IPC operation. For more information, see the `Create deployments <https://docs.aws.amazon.com/greengrass/v2/latest/developerguide/create-deployments.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

            :param timeout_in_seconds: The amount of time in seconds that a component can validate its configuration updates. If the validation time exceeds this timeout, then the deployment proceeds for the device. Default: ``30``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentconfigurationvalidationpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                deployment_configuration_validation_policy_property = greengrassv2.CfnDeployment.DeploymentConfigurationValidationPolicyProperty(
                    timeout_in_seconds=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__343efa1fe45d3f89c991694032bd11f5c420bb6186b754a3167ca1be6c51b0fc)
                check_type(argname="argument timeout_in_seconds", value=timeout_in_seconds, expected_type=type_hints["timeout_in_seconds"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if timeout_in_seconds is not None:
                self._values["timeout_in_seconds"] = timeout_in_seconds

        @builtins.property
        def timeout_in_seconds(self) -> typing.Optional[jsii.Number]:
            '''The amount of time in seconds that a component can validate its configuration updates.

            If the validation time exceeds this timeout, then the deployment proceeds for the device.

            Default: ``30``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentconfigurationvalidationpolicy.html#cfn-greengrassv2-deployment-deploymentconfigurationvalidationpolicy-timeoutinseconds
            '''
            result = self._values.get("timeout_in_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentConfigurationValidationPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnDeployment.DeploymentIoTJobConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "abort_config": "abortConfig",
            "job_executions_rollout_config": "jobExecutionsRolloutConfig",
            "timeout_config": "timeoutConfig",
        },
    )
    class DeploymentIoTJobConfigurationProperty:
        def __init__(
            self,
            *,
            abort_config: typing.Optional[typing.Union[typing.Union["CfnDeployment.IoTJobAbortConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            job_executions_rollout_config: typing.Optional[typing.Union[typing.Union["CfnDeployment.IoTJobExecutionsRolloutConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            timeout_config: typing.Optional[typing.Union[typing.Union["CfnDeployment.IoTJobTimeoutConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Contains information about an AWS IoT job configuration.

            :param abort_config: The stop configuration for the job. This configuration defines when and how to stop a job rollout.
            :param job_executions_rollout_config: The rollout configuration for the job. This configuration defines the rate at which the job rolls out to the fleet of target devices.
            :param timeout_config: The timeout configuration for the job. This configuration defines the amount of time each device has to complete the job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentiotjobconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                # rate_increase_criteria: Any
                
                deployment_io_tJob_configuration_property = greengrassv2.CfnDeployment.DeploymentIoTJobConfigurationProperty(
                    abort_config=greengrassv2.CfnDeployment.IoTJobAbortConfigProperty(
                        criteria_list=[greengrassv2.CfnDeployment.IoTJobAbortCriteriaProperty(
                            action="action",
                            failure_type="failureType",
                            min_number_of_executed_things=123,
                            threshold_percentage=123
                        )]
                    ),
                    job_executions_rollout_config=greengrassv2.CfnDeployment.IoTJobExecutionsRolloutConfigProperty(
                        exponential_rate=greengrassv2.CfnDeployment.IoTJobExponentialRolloutRateProperty(
                            base_rate_per_minute=123,
                            increment_factor=123,
                            rate_increase_criteria=rate_increase_criteria
                        ),
                        maximum_per_minute=123
                    ),
                    timeout_config=greengrassv2.CfnDeployment.IoTJobTimeoutConfigProperty(
                        in_progress_timeout_in_minutes=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__97d9d259a89cb065fa404f164423030529b6a9e8cc0094207a124f14dfa2ea31)
                check_type(argname="argument abort_config", value=abort_config, expected_type=type_hints["abort_config"])
                check_type(argname="argument job_executions_rollout_config", value=job_executions_rollout_config, expected_type=type_hints["job_executions_rollout_config"])
                check_type(argname="argument timeout_config", value=timeout_config, expected_type=type_hints["timeout_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if abort_config is not None:
                self._values["abort_config"] = abort_config
            if job_executions_rollout_config is not None:
                self._values["job_executions_rollout_config"] = job_executions_rollout_config
            if timeout_config is not None:
                self._values["timeout_config"] = timeout_config

        @builtins.property
        def abort_config(
            self,
        ) -> typing.Optional[typing.Union["CfnDeployment.IoTJobAbortConfigProperty", _IResolvable_a771d0ef]]:
            '''The stop configuration for the job.

            This configuration defines when and how to stop a job rollout.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentiotjobconfiguration.html#cfn-greengrassv2-deployment-deploymentiotjobconfiguration-abortconfig
            '''
            result = self._values.get("abort_config")
            return typing.cast(typing.Optional[typing.Union["CfnDeployment.IoTJobAbortConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def job_executions_rollout_config(
            self,
        ) -> typing.Optional[typing.Union["CfnDeployment.IoTJobExecutionsRolloutConfigProperty", _IResolvable_a771d0ef]]:
            '''The rollout configuration for the job.

            This configuration defines the rate at which the job rolls out to the fleet of target devices.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentiotjobconfiguration.html#cfn-greengrassv2-deployment-deploymentiotjobconfiguration-jobexecutionsrolloutconfig
            '''
            result = self._values.get("job_executions_rollout_config")
            return typing.cast(typing.Optional[typing.Union["CfnDeployment.IoTJobExecutionsRolloutConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def timeout_config(
            self,
        ) -> typing.Optional[typing.Union["CfnDeployment.IoTJobTimeoutConfigProperty", _IResolvable_a771d0ef]]:
            '''The timeout configuration for the job.

            This configuration defines the amount of time each device has to complete the job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentiotjobconfiguration.html#cfn-greengrassv2-deployment-deploymentiotjobconfiguration-timeoutconfig
            '''
            result = self._values.get("timeout_config")
            return typing.cast(typing.Optional[typing.Union["CfnDeployment.IoTJobTimeoutConfigProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentIoTJobConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnDeployment.DeploymentPoliciesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "component_update_policy": "componentUpdatePolicy",
            "configuration_validation_policy": "configurationValidationPolicy",
            "failure_handling_policy": "failureHandlingPolicy",
        },
    )
    class DeploymentPoliciesProperty:
        def __init__(
            self,
            *,
            component_update_policy: typing.Optional[typing.Union[typing.Union["CfnDeployment.DeploymentComponentUpdatePolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            configuration_validation_policy: typing.Optional[typing.Union[typing.Union["CfnDeployment.DeploymentConfigurationValidationPolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            failure_handling_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Contains information about policies that define how a deployment updates components and handles failure.

            :param component_update_policy: The component update policy for the configuration deployment. This policy defines when it's safe to deploy the configuration to devices.
            :param configuration_validation_policy: The configuration validation policy for the configuration deployment. This policy defines how long each component has to validate its configure updates.
            :param failure_handling_policy: The failure handling policy for the configuration deployment. This policy defines what to do if the deployment fails. Default: ``ROLLBACK``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentpolicies.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                deployment_policies_property = greengrassv2.CfnDeployment.DeploymentPoliciesProperty(
                    component_update_policy=greengrassv2.CfnDeployment.DeploymentComponentUpdatePolicyProperty(
                        action="action",
                        timeout_in_seconds=123
                    ),
                    configuration_validation_policy=greengrassv2.CfnDeployment.DeploymentConfigurationValidationPolicyProperty(
                        timeout_in_seconds=123
                    ),
                    failure_handling_policy="failureHandlingPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__136b521be437c2a00355faf7eb5c7cae6d68ed5795ea493bc2cd5175b1fd55a5)
                check_type(argname="argument component_update_policy", value=component_update_policy, expected_type=type_hints["component_update_policy"])
                check_type(argname="argument configuration_validation_policy", value=configuration_validation_policy, expected_type=type_hints["configuration_validation_policy"])
                check_type(argname="argument failure_handling_policy", value=failure_handling_policy, expected_type=type_hints["failure_handling_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if component_update_policy is not None:
                self._values["component_update_policy"] = component_update_policy
            if configuration_validation_policy is not None:
                self._values["configuration_validation_policy"] = configuration_validation_policy
            if failure_handling_policy is not None:
                self._values["failure_handling_policy"] = failure_handling_policy

        @builtins.property
        def component_update_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnDeployment.DeploymentComponentUpdatePolicyProperty", _IResolvable_a771d0ef]]:
            '''The component update policy for the configuration deployment.

            This policy defines when it's safe to deploy the configuration to devices.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentpolicies.html#cfn-greengrassv2-deployment-deploymentpolicies-componentupdatepolicy
            '''
            result = self._values.get("component_update_policy")
            return typing.cast(typing.Optional[typing.Union["CfnDeployment.DeploymentComponentUpdatePolicyProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def configuration_validation_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnDeployment.DeploymentConfigurationValidationPolicyProperty", _IResolvable_a771d0ef]]:
            '''The configuration validation policy for the configuration deployment.

            This policy defines how long each component has to validate its configure updates.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentpolicies.html#cfn-greengrassv2-deployment-deploymentpolicies-configurationvalidationpolicy
            '''
            result = self._values.get("configuration_validation_policy")
            return typing.cast(typing.Optional[typing.Union["CfnDeployment.DeploymentConfigurationValidationPolicyProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def failure_handling_policy(self) -> typing.Optional[builtins.str]:
            '''The failure handling policy for the configuration deployment. This policy defines what to do if the deployment fails.

            Default: ``ROLLBACK``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-deploymentpolicies.html#cfn-greengrassv2-deployment-deploymentpolicies-failurehandlingpolicy
            '''
            result = self._values.get("failure_handling_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DeploymentPoliciesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnDeployment.IoTJobAbortConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"criteria_list": "criteriaList"},
    )
    class IoTJobAbortConfigProperty:
        def __init__(
            self,
            *,
            criteria_list: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnDeployment.IoTJobAbortCriteriaProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        ) -> None:
            '''Contains a list of criteria that define when and how to cancel a configuration deployment.

            :param criteria_list: The list of criteria that define when and how to cancel the configuration deployment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobabortconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                io_tJob_abort_config_property = greengrassv2.CfnDeployment.IoTJobAbortConfigProperty(
                    criteria_list=[greengrassv2.CfnDeployment.IoTJobAbortCriteriaProperty(
                        action="action",
                        failure_type="failureType",
                        min_number_of_executed_things=123,
                        threshold_percentage=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e8b6a1e4186de7c5b502787caa0812a58ef304c028dc84b1e9845acb42b438d8)
                check_type(argname="argument criteria_list", value=criteria_list, expected_type=type_hints["criteria_list"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "criteria_list": criteria_list,
            }

        @builtins.property
        def criteria_list(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeployment.IoTJobAbortCriteriaProperty", _IResolvable_a771d0ef]]]:
            '''The list of criteria that define when and how to cancel the configuration deployment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobabortconfig.html#cfn-greengrassv2-deployment-iotjobabortconfig-criterialist
            '''
            result = self._values.get("criteria_list")
            assert result is not None, "Required property 'criteria_list' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDeployment.IoTJobAbortCriteriaProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IoTJobAbortConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnDeployment.IoTJobAbortCriteriaProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "failure_type": "failureType",
            "min_number_of_executed_things": "minNumberOfExecutedThings",
            "threshold_percentage": "thresholdPercentage",
        },
    )
    class IoTJobAbortCriteriaProperty:
        def __init__(
            self,
            *,
            action: builtins.str,
            failure_type: builtins.str,
            min_number_of_executed_things: jsii.Number,
            threshold_percentage: jsii.Number,
        ) -> None:
            '''Contains criteria that define when and how to cancel a job.

            The deployment stops if the following conditions are true:

            - The number of things that receive the deployment exceeds the ``minNumberOfExecutedThings`` .
            - The percentage of failures with type ``failureType`` exceeds the ``thresholdPercentage`` .

            :param action: The action to perform when the criteria are met.
            :param failure_type: The type of job deployment failure that can cancel a job.
            :param min_number_of_executed_things: The minimum number of things that receive the configuration before the job can cancel.
            :param threshold_percentage: The minimum percentage of ``failureType`` failures that occur before the job can cancel. This parameter supports up to two digits after the decimal (for example, you can specify ``10.9`` or ``10.99`` , but not ``10.999`` ).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobabortcriteria.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                io_tJob_abort_criteria_property = greengrassv2.CfnDeployment.IoTJobAbortCriteriaProperty(
                    action="action",
                    failure_type="failureType",
                    min_number_of_executed_things=123,
                    threshold_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2ed5e1171b1c25fa60ef4094949ba3ec2286dd80b25edce650a00d18ac324e09)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument failure_type", value=failure_type, expected_type=type_hints["failure_type"])
                check_type(argname="argument min_number_of_executed_things", value=min_number_of_executed_things, expected_type=type_hints["min_number_of_executed_things"])
                check_type(argname="argument threshold_percentage", value=threshold_percentage, expected_type=type_hints["threshold_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "action": action,
                "failure_type": failure_type,
                "min_number_of_executed_things": min_number_of_executed_things,
                "threshold_percentage": threshold_percentage,
            }

        @builtins.property
        def action(self) -> builtins.str:
            '''The action to perform when the criteria are met.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobabortcriteria.html#cfn-greengrassv2-deployment-iotjobabortcriteria-action
            '''
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def failure_type(self) -> builtins.str:
            '''The type of job deployment failure that can cancel a job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobabortcriteria.html#cfn-greengrassv2-deployment-iotjobabortcriteria-failuretype
            '''
            result = self._values.get("failure_type")
            assert result is not None, "Required property 'failure_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def min_number_of_executed_things(self) -> jsii.Number:
            '''The minimum number of things that receive the configuration before the job can cancel.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobabortcriteria.html#cfn-greengrassv2-deployment-iotjobabortcriteria-minnumberofexecutedthings
            '''
            result = self._values.get("min_number_of_executed_things")
            assert result is not None, "Required property 'min_number_of_executed_things' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def threshold_percentage(self) -> jsii.Number:
            '''The minimum percentage of ``failureType`` failures that occur before the job can cancel.

            This parameter supports up to two digits after the decimal (for example, you can specify ``10.9`` or ``10.99`` , but not ``10.999`` ).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobabortcriteria.html#cfn-greengrassv2-deployment-iotjobabortcriteria-thresholdpercentage
            '''
            result = self._values.get("threshold_percentage")
            assert result is not None, "Required property 'threshold_percentage' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IoTJobAbortCriteriaProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnDeployment.IoTJobExecutionsRolloutConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "exponential_rate": "exponentialRate",
            "maximum_per_minute": "maximumPerMinute",
        },
    )
    class IoTJobExecutionsRolloutConfigProperty:
        def __init__(
            self,
            *,
            exponential_rate: typing.Optional[typing.Union[typing.Union["CfnDeployment.IoTJobExponentialRolloutRateProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            maximum_per_minute: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains information about the rollout configuration for a job.

            This configuration defines the rate at which the job deploys a configuration to a fleet of target devices.

            :param exponential_rate: The exponential rate to increase the job rollout rate.
            :param maximum_per_minute: The maximum number of devices that receive a pending job notification, per minute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobexecutionsrolloutconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                # rate_increase_criteria: Any
                
                io_tJob_executions_rollout_config_property = greengrassv2.CfnDeployment.IoTJobExecutionsRolloutConfigProperty(
                    exponential_rate=greengrassv2.CfnDeployment.IoTJobExponentialRolloutRateProperty(
                        base_rate_per_minute=123,
                        increment_factor=123,
                        rate_increase_criteria=rate_increase_criteria
                    ),
                    maximum_per_minute=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6e0c3f6134458f6fe9aa627f90ca260f73c131e7aff81d46c6cf6c862dd9b4d3)
                check_type(argname="argument exponential_rate", value=exponential_rate, expected_type=type_hints["exponential_rate"])
                check_type(argname="argument maximum_per_minute", value=maximum_per_minute, expected_type=type_hints["maximum_per_minute"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exponential_rate is not None:
                self._values["exponential_rate"] = exponential_rate
            if maximum_per_minute is not None:
                self._values["maximum_per_minute"] = maximum_per_minute

        @builtins.property
        def exponential_rate(
            self,
        ) -> typing.Optional[typing.Union["CfnDeployment.IoTJobExponentialRolloutRateProperty", _IResolvable_a771d0ef]]:
            '''The exponential rate to increase the job rollout rate.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobexecutionsrolloutconfig.html#cfn-greengrassv2-deployment-iotjobexecutionsrolloutconfig-exponentialrate
            '''
            result = self._values.get("exponential_rate")
            return typing.cast(typing.Optional[typing.Union["CfnDeployment.IoTJobExponentialRolloutRateProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def maximum_per_minute(self) -> typing.Optional[jsii.Number]:
            '''The maximum number of devices that receive a pending job notification, per minute.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobexecutionsrolloutconfig.html#cfn-greengrassv2-deployment-iotjobexecutionsrolloutconfig-maximumperminute
            '''
            result = self._values.get("maximum_per_minute")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IoTJobExecutionsRolloutConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnDeployment.IoTJobExponentialRolloutRateProperty",
        jsii_struct_bases=[],
        name_mapping={
            "base_rate_per_minute": "baseRatePerMinute",
            "increment_factor": "incrementFactor",
            "rate_increase_criteria": "rateIncreaseCriteria",
        },
    )
    class IoTJobExponentialRolloutRateProperty:
        def __init__(
            self,
            *,
            base_rate_per_minute: jsii.Number,
            increment_factor: jsii.Number,
            rate_increase_criteria: typing.Any,
        ) -> None:
            '''Contains information about an exponential rollout rate for a configuration deployment job.

            :param base_rate_per_minute: The minimum number of devices that receive a pending job notification, per minute, when the job starts. This parameter defines the initial rollout rate of the job.
            :param increment_factor: The exponential factor to increase the rollout rate for the job. This parameter supports up to one digit after the decimal (for example, you can specify ``1.5`` , but not ``1.55`` ).
            :param rate_increase_criteria: The criteria to increase the rollout rate for the job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobexponentialrolloutrate.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                # rate_increase_criteria: Any
                
                io_tJob_exponential_rollout_rate_property = greengrassv2.CfnDeployment.IoTJobExponentialRolloutRateProperty(
                    base_rate_per_minute=123,
                    increment_factor=123,
                    rate_increase_criteria=rate_increase_criteria
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6e6b55f6112037e09600639df49f0f32475141b80d7a11fd40fba5d5680d4c78)
                check_type(argname="argument base_rate_per_minute", value=base_rate_per_minute, expected_type=type_hints["base_rate_per_minute"])
                check_type(argname="argument increment_factor", value=increment_factor, expected_type=type_hints["increment_factor"])
                check_type(argname="argument rate_increase_criteria", value=rate_increase_criteria, expected_type=type_hints["rate_increase_criteria"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "base_rate_per_minute": base_rate_per_minute,
                "increment_factor": increment_factor,
                "rate_increase_criteria": rate_increase_criteria,
            }

        @builtins.property
        def base_rate_per_minute(self) -> jsii.Number:
            '''The minimum number of devices that receive a pending job notification, per minute, when the job starts.

            This parameter defines the initial rollout rate of the job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobexponentialrolloutrate.html#cfn-greengrassv2-deployment-iotjobexponentialrolloutrate-baserateperminute
            '''
            result = self._values.get("base_rate_per_minute")
            assert result is not None, "Required property 'base_rate_per_minute' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def increment_factor(self) -> jsii.Number:
            '''The exponential factor to increase the rollout rate for the job.

            This parameter supports up to one digit after the decimal (for example, you can specify ``1.5`` , but not ``1.55`` ).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobexponentialrolloutrate.html#cfn-greengrassv2-deployment-iotjobexponentialrolloutrate-incrementfactor
            '''
            result = self._values.get("increment_factor")
            assert result is not None, "Required property 'increment_factor' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def rate_increase_criteria(self) -> typing.Any:
            '''The criteria to increase the rollout rate for the job.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobexponentialrolloutrate.html#cfn-greengrassv2-deployment-iotjobexponentialrolloutrate-rateincreasecriteria
            '''
            result = self._values.get("rate_increase_criteria")
            assert result is not None, "Required property 'rate_increase_criteria' is missing"
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IoTJobExponentialRolloutRateProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnDeployment.IoTJobTimeoutConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"in_progress_timeout_in_minutes": "inProgressTimeoutInMinutes"},
    )
    class IoTJobTimeoutConfigProperty:
        def __init__(
            self,
            *,
            in_progress_timeout_in_minutes: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains information about the timeout configuration for a job.

            :param in_progress_timeout_in_minutes: The amount of time, in minutes, that devices have to complete the job. The timer starts when the job status is set to ``IN_PROGRESS`` . If the job status doesn't change to a terminal state before the time expires, then the job status is set to ``TIMED_OUT`` . The timeout interval must be between 1 minute and 7 days (10080 minutes).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobtimeoutconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                io_tJob_timeout_config_property = greengrassv2.CfnDeployment.IoTJobTimeoutConfigProperty(
                    in_progress_timeout_in_minutes=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__25f70bf302078f768b7e12c726150eff34b9d78e330b9a05b7fc12f825cf0cb6)
                check_type(argname="argument in_progress_timeout_in_minutes", value=in_progress_timeout_in_minutes, expected_type=type_hints["in_progress_timeout_in_minutes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if in_progress_timeout_in_minutes is not None:
                self._values["in_progress_timeout_in_minutes"] = in_progress_timeout_in_minutes

        @builtins.property
        def in_progress_timeout_in_minutes(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in minutes, that devices have to complete the job.

            The timer starts when the job status is set to ``IN_PROGRESS`` . If the job status doesn't change to a terminal state before the time expires, then the job status is set to ``TIMED_OUT`` .

            The timeout interval must be between 1 minute and 7 days (10080 minutes).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-iotjobtimeoutconfig.html#cfn-greengrassv2-deployment-iotjobtimeoutconfig-inprogresstimeoutinminutes
            '''
            result = self._values.get("in_progress_timeout_in_minutes")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IoTJobTimeoutConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_greengrassv2.CfnDeployment.SystemResourceLimitsProperty",
        jsii_struct_bases=[],
        name_mapping={"cpus": "cpus", "memory": "memory"},
    )
    class SystemResourceLimitsProperty:
        def __init__(
            self,
            *,
            cpus: typing.Optional[jsii.Number] = None,
            memory: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Contains information about system resource limits that the  software applies to a component's processes.

            :param cpus: The maximum amount of CPU time that a component's processes can use on the core device. A core device's total CPU time is equivalent to the device's number of CPU cores. For example, on a core device with 4 CPU cores, you can set this value to 2 to limit the component's processes to 50 percent usage of each CPU core. On a device with 1 CPU core, you can set this value to 0.25 to limit the component's processes to 25 percent usage of the CPU. If you set this value to a number greater than the number of CPU cores, the AWS IoT Greengrass Core software doesn't limit the component's CPU usage.
            :param memory: The maximum amount of RAM, expressed in kilobytes, that a component's processes can use on the core device. For more information, see `Configure system resource limits for components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-system-resource-limits>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-systemresourcelimits.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_greengrassv2 as greengrassv2
                
                system_resource_limits_property = greengrassv2.CfnDeployment.SystemResourceLimitsProperty(
                    cpus=123,
                    memory=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a9c01e1cf5daa08ea2dd3a054841007d5cb7b05a11a567925b5fd2853d0f9f29)
                check_type(argname="argument cpus", value=cpus, expected_type=type_hints["cpus"])
                check_type(argname="argument memory", value=memory, expected_type=type_hints["memory"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if cpus is not None:
                self._values["cpus"] = cpus
            if memory is not None:
                self._values["memory"] = memory

        @builtins.property
        def cpus(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of CPU time that a component's processes can use on the core device.

            A core device's total CPU time is equivalent to the device's number of CPU cores. For example, on a core device with 4 CPU cores, you can set this value to 2 to limit the component's processes to 50 percent usage of each CPU core. On a device with 1 CPU core, you can set this value to 0.25 to limit the component's processes to 25 percent usage of the CPU. If you set this value to a number greater than the number of CPU cores, the AWS IoT Greengrass Core software doesn't limit the component's CPU usage.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-systemresourcelimits.html#cfn-greengrassv2-deployment-systemresourcelimits-cpus
            '''
            result = self._values.get("cpus")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def memory(self) -> typing.Optional[jsii.Number]:
            '''The maximum amount of RAM, expressed in kilobytes, that a component's processes can use on the core device.

            For more information, see `Configure system resource limits for components <https://docs.aws.amazon.com/greengrass/v2/developerguide/configure-greengrass-core-v2.html#configure-component-system-resource-limits>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-greengrassv2-deployment-systemresourcelimits.html#cfn-greengrassv2-deployment-systemresourcelimits-memory
            '''
            result = self._values.get("memory")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SystemResourceLimitsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_greengrassv2.CfnDeploymentProps",
    jsii_struct_bases=[],
    name_mapping={
        "target_arn": "targetArn",
        "components": "components",
        "deployment_name": "deploymentName",
        "deployment_policies": "deploymentPolicies",
        "iot_job_configuration": "iotJobConfiguration",
        "tags": "tags",
    },
)
class CfnDeploymentProps:
    def __init__(
        self,
        *,
        target_arn: builtins.str,
        components: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnDeployment.ComponentDeploymentSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        deployment_name: typing.Optional[builtins.str] = None,
        deployment_policies: typing.Optional[typing.Union[typing.Union[CfnDeployment.DeploymentPoliciesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        iot_job_configuration: typing.Optional[typing.Union[typing.Union[CfnDeployment.DeploymentIoTJobConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDeployment``.

        :param target_arn: The ARN of the target AWS IoT thing or thing group.
        :param components: The components to deploy. This is a dictionary, where each key is the name of a component, and each key's value is the version and configuration to deploy for that component.
        :param deployment_name: The name of the deployment.
        :param deployment_policies: The deployment policies for the deployment. These policies define how the deployment updates components and handles failure.
        :param iot_job_configuration: The job configuration for the deployment configuration. The job configuration specifies the rollout, timeout, and stop configurations for the deployment configuration.
        :param tags: Application-specific metadata to attach to the deployment. You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tag your AWS IoT Greengrass Version 2 resources <https://docs.aws.amazon.com/greengrass/v2/developerguide/tag-resources.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* . This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates:: "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value" }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_greengrassv2 as greengrassv2
            
            # rate_increase_criteria: Any
            
            cfn_deployment_props = greengrassv2.CfnDeploymentProps(
                target_arn="targetArn",
            
                # the properties below are optional
                components={
                    "components_key": greengrassv2.CfnDeployment.ComponentDeploymentSpecificationProperty(
                        component_version="componentVersion",
                        configuration_update=greengrassv2.CfnDeployment.ComponentConfigurationUpdateProperty(
                            merge="merge",
                            reset=["reset"]
                        ),
                        run_with=greengrassv2.CfnDeployment.ComponentRunWithProperty(
                            posix_user="posixUser",
                            system_resource_limits=greengrassv2.CfnDeployment.SystemResourceLimitsProperty(
                                cpus=123,
                                memory=123
                            ),
                            windows_user="windowsUser"
                        )
                    )
                },
                deployment_name="deploymentName",
                deployment_policies=greengrassv2.CfnDeployment.DeploymentPoliciesProperty(
                    component_update_policy=greengrassv2.CfnDeployment.DeploymentComponentUpdatePolicyProperty(
                        action="action",
                        timeout_in_seconds=123
                    ),
                    configuration_validation_policy=greengrassv2.CfnDeployment.DeploymentConfigurationValidationPolicyProperty(
                        timeout_in_seconds=123
                    ),
                    failure_handling_policy="failureHandlingPolicy"
                ),
                iot_job_configuration=greengrassv2.CfnDeployment.DeploymentIoTJobConfigurationProperty(
                    abort_config=greengrassv2.CfnDeployment.IoTJobAbortConfigProperty(
                        criteria_list=[greengrassv2.CfnDeployment.IoTJobAbortCriteriaProperty(
                            action="action",
                            failure_type="failureType",
                            min_number_of_executed_things=123,
                            threshold_percentage=123
                        )]
                    ),
                    job_executions_rollout_config=greengrassv2.CfnDeployment.IoTJobExecutionsRolloutConfigProperty(
                        exponential_rate=greengrassv2.CfnDeployment.IoTJobExponentialRolloutRateProperty(
                            base_rate_per_minute=123,
                            increment_factor=123,
                            rate_increase_criteria=rate_increase_criteria
                        ),
                        maximum_per_minute=123
                    ),
                    timeout_config=greengrassv2.CfnDeployment.IoTJobTimeoutConfigProperty(
                        in_progress_timeout_in_minutes=123
                    )
                ),
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a559f6082c24b32179e3d68007ee3c25e4282d292ce5c44f139a5b31cbffeef)
            check_type(argname="argument target_arn", value=target_arn, expected_type=type_hints["target_arn"])
            check_type(argname="argument components", value=components, expected_type=type_hints["components"])
            check_type(argname="argument deployment_name", value=deployment_name, expected_type=type_hints["deployment_name"])
            check_type(argname="argument deployment_policies", value=deployment_policies, expected_type=type_hints["deployment_policies"])
            check_type(argname="argument iot_job_configuration", value=iot_job_configuration, expected_type=type_hints["iot_job_configuration"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "target_arn": target_arn,
        }
        if components is not None:
            self._values["components"] = components
        if deployment_name is not None:
            self._values["deployment_name"] = deployment_name
        if deployment_policies is not None:
            self._values["deployment_policies"] = deployment_policies
        if iot_job_configuration is not None:
            self._values["iot_job_configuration"] = iot_job_configuration
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def target_arn(self) -> builtins.str:
        '''The ARN of the target AWS IoT thing or thing group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-targetarn
        '''
        result = self._values.get("target_arn")
        assert result is not None, "Required property 'target_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def components(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnDeployment.ComponentDeploymentSpecificationProperty, _IResolvable_a771d0ef]]]]:
        '''The components to deploy.

        This is a dictionary, where each key is the name of a component, and each key's value is the version and configuration to deploy for that component.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-components
        '''
        result = self._values.get("components")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnDeployment.ComponentDeploymentSpecificationProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def deployment_name(self) -> typing.Optional[builtins.str]:
        '''The name of the deployment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-deploymentname
        '''
        result = self._values.get("deployment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def deployment_policies(
        self,
    ) -> typing.Optional[typing.Union[CfnDeployment.DeploymentPoliciesProperty, _IResolvable_a771d0ef]]:
        '''The deployment policies for the deployment.

        These policies define how the deployment updates components and handles failure.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-deploymentpolicies
        '''
        result = self._values.get("deployment_policies")
        return typing.cast(typing.Optional[typing.Union[CfnDeployment.DeploymentPoliciesProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def iot_job_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnDeployment.DeploymentIoTJobConfigurationProperty, _IResolvable_a771d0ef]]:
        '''The job configuration for the deployment configuration.

        The job configuration specifies the rollout, timeout, and stop configurations for the deployment configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-iotjobconfiguration
        '''
        result = self._values.get("iot_job_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnDeployment.DeploymentIoTJobConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Application-specific metadata to attach to the deployment.

        You can use tags in IAM policies to control access to AWS IoT Greengrass resources. You can also use tags to categorize your resources. For more information, see `Tag your AWS IoT Greengrass Version 2 resources <https://docs.aws.amazon.com/greengrass/v2/developerguide/tag-resources.html>`_ in the *AWS IoT Greengrass V2 Developer Guide* .

        This ``Json`` property type is processed as a map of key-value pairs. It uses the following format, which is different from most ``Tags`` implementations in AWS CloudFormation templates::

           "Tags": { "KeyName0": "value", "KeyName1": "value", "KeyName2": "value"
           }

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-greengrassv2-deployment.html#cfn-greengrassv2-deployment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnComponentVersion",
    "CfnComponentVersionProps",
    "CfnDeployment",
    "CfnDeploymentProps",
]

publication.publish()

def _typecheckingstub__367836b0c10b75b5cb241353a886a5a5e492dd8c50a222db6671d0796907f4d7(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    inline_recipe: typing.Optional[builtins.str] = None,
    lambda_function: typing.Optional[typing.Union[typing.Union[CfnComponentVersion.LambdaFunctionRecipeSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3fb33a480b0f385d15d97e830de0923f435d9853464bee51166c928ea8363dd(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__338f4f82e6d431f73b968d336b9061bd14482610f200e746e00b5671e382f739(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5de086987d04f39f7375f143596e93b11b33c4a8f34ce25b06f542271448e22(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eeca3819844e642b32b994374a94a0b300e8a6ec4b9fef246d5e40fb7172d728(
    value: typing.Optional[typing.Union[CfnComponentVersion.LambdaFunctionRecipeSourceProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b21032cf8c65f0a4da2e9b3544b46f0bed9409e81a5b82f5e7ff7d5b9e2d8144(
    *,
    dependency_type: typing.Optional[builtins.str] = None,
    version_requirement: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e8633ff0fcbcbf7d4829394d49a6b2a6c1251d2bd9d0d91cde64cad4b63fc64(
    *,
    attributes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a11394b6651ec377a8088918c206587a570e49edab30e4f69bb846e7dcc1c43(
    *,
    devices: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponentVersion.LambdaDeviceMountProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    memory_size_in_kb: typing.Optional[jsii.Number] = None,
    mount_ro_sysfs: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    volumes: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponentVersion.LambdaVolumeMountProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b715079a837485b41d661ec2e1557d589178997f66b393fd2bfb26d6d10b3f47(
    *,
    add_group_owner: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    path: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28254b5c0c8738d6f53f3d23eeb930a95cdd096b763c3345bcfc5cc4927e47cd(
    *,
    topic: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cb0fcd118106691fca08a5d2bbd6298e4de8db5a5b8ed862ac67f3891ceedf2(
    *,
    environment_variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]] = None,
    event_sources: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponentVersion.LambdaEventSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    exec_args: typing.Optional[typing.Sequence[builtins.str]] = None,
    input_payload_encoding_type: typing.Optional[builtins.str] = None,
    linux_process_params: typing.Optional[typing.Union[typing.Union[CfnComponentVersion.LambdaLinuxProcessParamsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    max_idle_time_in_seconds: typing.Optional[jsii.Number] = None,
    max_instances_count: typing.Optional[jsii.Number] = None,
    max_queue_size: typing.Optional[jsii.Number] = None,
    pinned: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    status_timeout_in_seconds: typing.Optional[jsii.Number] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fa2878407d907f9cf40cfe5146e23e6c305973019a998d7756a028906e64c74(
    *,
    component_dependencies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnComponentVersion.ComponentDependencyRequirementProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    component_lambda_parameters: typing.Optional[typing.Union[typing.Union[CfnComponentVersion.LambdaExecutionParametersProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    component_name: typing.Optional[builtins.str] = None,
    component_platforms: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnComponentVersion.ComponentPlatformProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    component_version: typing.Optional[builtins.str] = None,
    lambda_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a84c2e346dd2e08aac3bb2df5f5f31297462946f1db412969c0766c162683c03(
    *,
    container_params: typing.Optional[typing.Union[typing.Union[CfnComponentVersion.LambdaContainerParamsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    isolation_mode: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe6c5550aec759bb5e48ba9a97bd37dd5cebc03608100593b67ebe3b39afa543(
    *,
    add_group_owner: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    destination_path: typing.Optional[builtins.str] = None,
    permission: typing.Optional[builtins.str] = None,
    source_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a1d300df7036df025b73636bea689d9af2bab1ce9f631b0a5249efcf4164f9b(
    *,
    inline_recipe: typing.Optional[builtins.str] = None,
    lambda_function: typing.Optional[typing.Union[typing.Union[CfnComponentVersion.LambdaFunctionRecipeSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99e732ca39ddcada02a116f52e0ce75f19737af7f42b25924073b503b01a0643(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    target_arn: builtins.str,
    components: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnDeployment.ComponentDeploymentSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    deployment_name: typing.Optional[builtins.str] = None,
    deployment_policies: typing.Optional[typing.Union[typing.Union[CfnDeployment.DeploymentPoliciesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    iot_job_configuration: typing.Optional[typing.Union[typing.Union[CfnDeployment.DeploymentIoTJobConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__578649b46579783b9d0421ed49592fd16c87b8b2ce4e945f662d3fd7966e71a3(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3a73abf67ec3457b7d02ca8be4126e0c3ecebb2a3c665a1b2d2ae1993dcb574(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e9d72418e960a4a4fd6879c4d082e5aa077a8cb08f0c4c36de1384f339211ae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a13aacacc96f5eb2979e446d8145ac6c29f7c7841b2366ee47127bedbd68977d(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[CfnDeployment.ComponentDeploymentSpecificationProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ec29a9aa0935488a334c3a19e8b9b4c0afa9364c0239aaa4788cb5d3771585f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc1dc5630343bc19b06adbc7d438837b32859a77686c0a99afad7ab5fae18375(
    value: typing.Optional[typing.Union[CfnDeployment.DeploymentPoliciesProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__248dbb8b6bfc5db9850ead36b6f76c87cda7bee7862cde09b6811b4e19bbc9cf(
    value: typing.Optional[typing.Union[CfnDeployment.DeploymentIoTJobConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f16d59a933932d581729af72d04bb49cc11188ebab2abf6b7f848f9ad464e31f(
    *,
    merge: typing.Optional[builtins.str] = None,
    reset: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__886b1eddb14044b2d4d525a1b37724f3cf9957f456651e4c88d7a95f448372d0(
    *,
    component_version: typing.Optional[builtins.str] = None,
    configuration_update: typing.Optional[typing.Union[typing.Union[CfnDeployment.ComponentConfigurationUpdateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    run_with: typing.Optional[typing.Union[typing.Union[CfnDeployment.ComponentRunWithProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bc1762e82a98eb850efa4dd5845e7699f153f371b18b78c954ce4dec4029bca(
    *,
    posix_user: typing.Optional[builtins.str] = None,
    system_resource_limits: typing.Optional[typing.Union[typing.Union[CfnDeployment.SystemResourceLimitsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    windows_user: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fd09e96c8d3aa2bdbc501ae47e3560207f41696c8fcebcd5700f70066e4f5fc(
    *,
    action: typing.Optional[builtins.str] = None,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__343efa1fe45d3f89c991694032bd11f5c420bb6186b754a3167ca1be6c51b0fc(
    *,
    timeout_in_seconds: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d9d259a89cb065fa404f164423030529b6a9e8cc0094207a124f14dfa2ea31(
    *,
    abort_config: typing.Optional[typing.Union[typing.Union[CfnDeployment.IoTJobAbortConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    job_executions_rollout_config: typing.Optional[typing.Union[typing.Union[CfnDeployment.IoTJobExecutionsRolloutConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    timeout_config: typing.Optional[typing.Union[typing.Union[CfnDeployment.IoTJobTimeoutConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__136b521be437c2a00355faf7eb5c7cae6d68ed5795ea493bc2cd5175b1fd55a5(
    *,
    component_update_policy: typing.Optional[typing.Union[typing.Union[CfnDeployment.DeploymentComponentUpdatePolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    configuration_validation_policy: typing.Optional[typing.Union[typing.Union[CfnDeployment.DeploymentConfigurationValidationPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    failure_handling_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8b6a1e4186de7c5b502787caa0812a58ef304c028dc84b1e9845acb42b438d8(
    *,
    criteria_list: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDeployment.IoTJobAbortCriteriaProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ed5e1171b1c25fa60ef4094949ba3ec2286dd80b25edce650a00d18ac324e09(
    *,
    action: builtins.str,
    failure_type: builtins.str,
    min_number_of_executed_things: jsii.Number,
    threshold_percentage: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e0c3f6134458f6fe9aa627f90ca260f73c131e7aff81d46c6cf6c862dd9b4d3(
    *,
    exponential_rate: typing.Optional[typing.Union[typing.Union[CfnDeployment.IoTJobExponentialRolloutRateProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    maximum_per_minute: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e6b55f6112037e09600639df49f0f32475141b80d7a11fd40fba5d5680d4c78(
    *,
    base_rate_per_minute: jsii.Number,
    increment_factor: jsii.Number,
    rate_increase_criteria: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25f70bf302078f768b7e12c726150eff34b9d78e330b9a05b7fc12f825cf0cb6(
    *,
    in_progress_timeout_in_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9c01e1cf5daa08ea2dd3a054841007d5cb7b05a11a567925b5fd2853d0f9f29(
    *,
    cpus: typing.Optional[jsii.Number] = None,
    memory: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a559f6082c24b32179e3d68007ee3c25e4282d292ce5c44f139a5b31cbffeef(
    *,
    target_arn: builtins.str,
    components: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnDeployment.ComponentDeploymentSpecificationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    deployment_name: typing.Optional[builtins.str] = None,
    deployment_policies: typing.Optional[typing.Union[typing.Union[CfnDeployment.DeploymentPoliciesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    iot_job_configuration: typing.Optional[typing.Union[typing.Union[CfnDeployment.DeploymentIoTJobConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
