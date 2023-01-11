'''
# AWS::M2 Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as m2
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for M2 construct libraries](https://constructs.dev/search?q=m2)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::M2 resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_M2.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::M2](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_M2.html).

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
class CfnApplication(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_m2.CfnApplication",
):
    '''A CloudFormation ``AWS::M2::Application``.

    Specifies a new application with given parameters. Requires an existing runtime environment and application definition file.

    For information about application definitions, see the `AWS Mainframe Modernization User Guide <https://docs.aws.amazon.com/m2/latest/userguide/applications-m2-definition.html>`_ .

    :cloudformationResource: AWS::M2::Application
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_m2 as m2
        
        cfn_application = m2.CfnApplication(self, "MyCfnApplication",
            definition=m2.CfnApplication.DefinitionProperty(
                content="content",
                s3_location="s3Location"
            ),
            engine_type="engineType",
            name="name",
        
            # the properties below are optional
            description="description",
            kms_key_id="kmsKeyId",
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
        definition: typing.Union[typing.Union["CfnApplication.DefinitionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        engine_type: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::M2::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param definition: The application definition for a particular application. You can specify either inline JSON or an Amazon S3 bucket location. For information about application definitions, see the `AWS Mainframe Modernization User Guide <https://docs.aws.amazon.com/m2/latest/userguide/applications-m2-definition.html>`_ .
        :param engine_type: The type of the target platform for this application.
        :param name: The name of the application.
        :param description: The description of the application.
        :param kms_key_id: The identifier of a customer managed key.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f391dc1b969dfd831609b4bf3887ebafa7c571218389b9cf8ef2f6abf05a28b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationProps(
            definition=definition,
            engine_type=engine_type,
            name=name,
            description=description,
            kms_key_id=kms_key_id,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae4e7b0201375292850906bbe5e4141213b6d7caf147b1a1bfd328f46287076)
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
            type_hints = typing.get_type_hints(_typecheckingstub__952192cb2398a6a3569071281d5b71a988a0a8cfb4a5d9963ebb6298b87ad8d0)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrApplicationArn")
    def attr_application_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the application.

        :cloudformationAttribute: ApplicationArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrApplicationArn"))

    @builtins.property
    @jsii.member(jsii_name="attrApplicationId")
    def attr_application_id(self) -> builtins.str:
        '''The identifier of the application.

        :cloudformationAttribute: ApplicationId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrApplicationId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(
        self,
    ) -> typing.Union["CfnApplication.DefinitionProperty", _IResolvable_a771d0ef]:
        '''The application definition for a particular application. You can specify either inline JSON or an Amazon S3 bucket location.

        For information about application definitions, see the `AWS Mainframe Modernization User Guide <https://docs.aws.amazon.com/m2/latest/userguide/applications-m2-definition.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-definition
        '''
        return typing.cast(typing.Union["CfnApplication.DefinitionProperty", _IResolvable_a771d0ef], jsii.get(self, "definition"))

    @definition.setter
    def definition(
        self,
        value: typing.Union["CfnApplication.DefinitionProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f4d5c7d5e77a0e7374336f46943727e32bfce68fad4ad447e9ad8091bf45c61b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "definition", value)

    @builtins.property
    @jsii.member(jsii_name="engineType")
    def engine_type(self) -> builtins.str:
        '''The type of the target platform for this application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-enginetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "engineType"))

    @engine_type.setter
    def engine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a0e7a9a1c6347cfdca26610489c43a53f97abf60b881b36d561eed8bc7cef85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d810ca0401f462b5eec217ff6d02e593ae70c1069c6c30dedb71a1e6e1e9b12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77120bb7e6b688972ce04deb9bf893f246f3bea10696ce3f720de8e1c2987423)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of a customer managed key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d1b517302a4a732d02e08d98aad9b24f8780e35b33d8a6d782c9844b884cac6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_m2.CfnApplication.DefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"content": "content", "s3_location": "s3Location"},
    )
    class DefinitionProperty:
        def __init__(
            self,
            *,
            content: typing.Optional[builtins.str] = None,
            s3_location: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The application definition for a particular application.

            You can specify either inline JSON or an Amazon S3 bucket location.

            :param content: The content of the application definition. This is a JSON object that contains the resource configuration/definitions that identify an application.
            :param s3_location: The S3 bucket that contains the application definition.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-application-definition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_m2 as m2
                
                definition_property = m2.CfnApplication.DefinitionProperty(
                    content="content",
                    s3_location="s3Location"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fad95f17d0d8cf39f03ece774029cc8e0b396bdcf0f76a3c2ff8feae4b7c463a)
                check_type(argname="argument content", value=content, expected_type=type_hints["content"])
                check_type(argname="argument s3_location", value=s3_location, expected_type=type_hints["s3_location"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content is not None:
                self._values["content"] = content
            if s3_location is not None:
                self._values["s3_location"] = s3_location

        @builtins.property
        def content(self) -> typing.Optional[builtins.str]:
            '''The content of the application definition.

            This is a JSON object that contains the resource configuration/definitions that identify an application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-application-definition.html#cfn-m2-application-definition-content
            '''
            result = self._values.get("content")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def s3_location(self) -> typing.Optional[builtins.str]:
            '''The S3 bucket that contains the application definition.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-application-definition.html#cfn-m2-application-definition-s3location
            '''
            result = self._values.get("s3_location")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_m2.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "definition": "definition",
        "engine_type": "engineType",
        "name": "name",
        "description": "description",
        "kms_key_id": "kmsKeyId",
        "tags": "tags",
    },
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        definition: typing.Union[typing.Union[CfnApplication.DefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        engine_type: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApplication``.

        :param definition: The application definition for a particular application. You can specify either inline JSON or an Amazon S3 bucket location. For information about application definitions, see the `AWS Mainframe Modernization User Guide <https://docs.aws.amazon.com/m2/latest/userguide/applications-m2-definition.html>`_ .
        :param engine_type: The type of the target platform for this application.
        :param name: The name of the application.
        :param description: The description of the application.
        :param kms_key_id: The identifier of a customer managed key.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_m2 as m2
            
            cfn_application_props = m2.CfnApplicationProps(
                definition=m2.CfnApplication.DefinitionProperty(
                    content="content",
                    s3_location="s3Location"
                ),
                engine_type="engineType",
                name="name",
            
                # the properties below are optional
                description="description",
                kms_key_id="kmsKeyId",
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a3637dc604d5563bcde8c8a5951e6aed69c651939e3dad4c022c20fbd55640b)
            check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            check_type(argname="argument engine_type", value=engine_type, expected_type=type_hints["engine_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "definition": definition,
            "engine_type": engine_type,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def definition(
        self,
    ) -> typing.Union[CfnApplication.DefinitionProperty, _IResolvable_a771d0ef]:
        '''The application definition for a particular application. You can specify either inline JSON or an Amazon S3 bucket location.

        For information about application definitions, see the `AWS Mainframe Modernization User Guide <https://docs.aws.amazon.com/m2/latest/userguide/applications-m2-definition.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-definition
        '''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(typing.Union[CfnApplication.DefinitionProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def engine_type(self) -> builtins.str:
        '''The type of the target platform for this application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-enginetype
        '''
        result = self._values.get("engine_type")
        assert result is not None, "Required property 'engine_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of a customer managed key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnEnvironment(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_m2.CfnEnvironment",
):
    '''A CloudFormation ``AWS::M2::Environment``.

    Specifies a runtime environment for a given runtime engine.

    :cloudformationResource: AWS::M2::Environment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_m2 as m2
        
        cfn_environment = m2.CfnEnvironment(self, "MyCfnEnvironment",
            engine_type="engineType",
            instance_type="instanceType",
            name="name",
        
            # the properties below are optional
            description="description",
            engine_version="engineVersion",
            high_availability_config=m2.CfnEnvironment.HighAvailabilityConfigProperty(
                desired_capacity=123
            ),
            kms_key_id="kmsKeyId",
            preferred_maintenance_window="preferredMaintenanceWindow",
            publicly_accessible=False,
            security_group_ids=["securityGroupIds"],
            storage_configurations=[m2.CfnEnvironment.StorageConfigurationProperty(
                efs=m2.CfnEnvironment.EfsStorageConfigurationProperty(
                    file_system_id="fileSystemId",
                    mount_point="mountPoint"
                ),
                fsx=m2.CfnEnvironment.FsxStorageConfigurationProperty(
                    file_system_id="fileSystemId",
                    mount_point="mountPoint"
                )
            )],
            subnet_ids=["subnetIds"],
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
        engine_type: builtins.str,
        instance_type: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        high_availability_config: typing.Optional[typing.Union[typing.Union["CfnEnvironment.HighAvailabilityConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        storage_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnEnvironment.StorageConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::M2::Environment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param engine_type: The target platform for the runtime environment.
        :param instance_type: The instance type of the runtime environment.
        :param name: The name of the runtime environment.
        :param description: The description of the runtime environment.
        :param engine_version: The version of the runtime engine.
        :param high_availability_config: Defines the details of a high availability configuration.
        :param kms_key_id: The identifier of a customer managed key.
        :param preferred_maintenance_window: Configures the maintenance window you want for the runtime environment. If you do not provide a value, a random system-generated value will be assigned.
        :param publicly_accessible: Specifies whether the runtime environment is publicly accessible.
        :param security_group_ids: The list of security groups for the VPC associated with this runtime environment.
        :param storage_configurations: Defines the storage configuration for a runtime environment.
        :param subnet_ids: The list of subnets associated with the VPC for this runtime environment.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54fae7b392cb1ef7a16e25177b6cf9f108a974095d8a2dd31f32bd3ad449270f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEnvironmentProps(
            engine_type=engine_type,
            instance_type=instance_type,
            name=name,
            description=description,
            engine_version=engine_version,
            high_availability_config=high_availability_config,
            kms_key_id=kms_key_id,
            preferred_maintenance_window=preferred_maintenance_window,
            publicly_accessible=publicly_accessible,
            security_group_ids=security_group_ids,
            storage_configurations=storage_configurations,
            subnet_ids=subnet_ids,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba476f2306f11a7f744e13a05e9c3357f9ee9210befe30dd11780720e932851e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a7fa3a6a4026388b0a3d43603a5988efd5f1437faaf2d3f540241b266a64bc6e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrEnvironmentArn")
    def attr_environment_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the runtime environment.

        :cloudformationAttribute: EnvironmentArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEnvironmentArn"))

    @builtins.property
    @jsii.member(jsii_name="attrEnvironmentId")
    def attr_environment_id(self) -> builtins.str:
        '''The unique identifier of the runtime environment.

        :cloudformationAttribute: EnvironmentId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEnvironmentId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="engineType")
    def engine_type(self) -> builtins.str:
        '''The target platform for the runtime environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-enginetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "engineType"))

    @engine_type.setter
    def engine_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0cde25d6123b2dfa2062b5bd871f5458a4657088fb8207d11a2ce0222e3238f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineType", value)

    @builtins.property
    @jsii.member(jsii_name="instanceType")
    def instance_type(self) -> builtins.str:
        '''The instance type of the runtime environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-instancetype
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceType"))

    @instance_type.setter
    def instance_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aabab80a324fd47f798ae9c99575b94f769d17d0d7a2e9d43564dce647b4117d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name of the runtime environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c396604c36ef46972e43cfef738b4f9e3c5ad1515bf0b9206c0b0529a831e14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the runtime environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f93642af34d04943edf7725bef0d253f4774f6d802aa62cbc6810f125f86590)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="engineVersion")
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version of the runtime engine.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-engineversion
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "engineVersion"))

    @engine_version.setter
    def engine_version(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f84b57d103baafbd1c184d55f1175e1d815a341fd042b1ed13bf22737b17224d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="highAvailabilityConfig")
    def high_availability_config(
        self,
    ) -> typing.Optional[typing.Union["CfnEnvironment.HighAvailabilityConfigProperty", _IResolvable_a771d0ef]]:
        '''Defines the details of a high availability configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-highavailabilityconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnEnvironment.HighAvailabilityConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "highAvailabilityConfig"))

    @high_availability_config.setter
    def high_availability_config(
        self,
        value: typing.Optional[typing.Union["CfnEnvironment.HighAvailabilityConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4d72ba49a8abc6e46b93f6f359d1df01aada73df9cf578d68ffc2871e141002)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "highAvailabilityConfig", value)

    @builtins.property
    @jsii.member(jsii_name="kmsKeyId")
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of a customer managed key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-kmskeyid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "kmsKeyId"))

    @kms_key_id.setter
    def kms_key_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ca66c0ffdbed1f674729134f10c7ee5c95d653343a0573363958d3e41d0e548)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @builtins.property
    @jsii.member(jsii_name="preferredMaintenanceWindow")
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''Configures the maintenance window you want for the runtime environment.

        If you do not provide a value, a random system-generated value will be assigned.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-preferredmaintenancewindow
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredMaintenanceWindow"))

    @preferred_maintenance_window.setter
    def preferred_maintenance_window(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7177a7f3948fb82521016eb9e1123092c0d1cd875c71e7b1cef84030f27952fa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property
    @jsii.member(jsii_name="publiclyAccessible")
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether the runtime environment is publicly accessible.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-publiclyaccessible
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "publiclyAccessible"))

    @publicly_accessible.setter
    def publicly_accessible(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f82c3b98b65a586215e77a9fc72623359bcc7a25e452c4d75b0a3c9a90199e53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publiclyAccessible", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of security groups for the VPC associated with this runtime environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-securitygroupids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__504ac76f645d55eb4933c01c8431dfc0bec13943b5969ac72a47985d64c1dfbb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="storageConfigurations")
    def storage_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEnvironment.StorageConfigurationProperty", _IResolvable_a771d0ef]]]]:
        '''Defines the storage configuration for a runtime environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-storageconfigurations
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEnvironment.StorageConfigurationProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "storageConfigurations"))

    @storage_configurations.setter
    def storage_configurations(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEnvironment.StorageConfigurationProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d8813ae37275cbff20dee5a2dc705482a57d00efc4ffe221be65455f7769666)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageConfigurations", value)

    @builtins.property
    @jsii.member(jsii_name="subnetIds")
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of subnets associated with the VPC for this runtime environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-subnetids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "subnetIds"))

    @subnet_ids.setter
    def subnet_ids(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6172d5592e7ec9236e0001a69b7d53ee89659678d2f18e8829e2bae11c4f4d45)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_m2.CfnEnvironment.EfsStorageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"file_system_id": "fileSystemId", "mount_point": "mountPoint"},
    )
    class EfsStorageConfigurationProperty:
        def __init__(
            self,
            *,
            file_system_id: builtins.str,
            mount_point: builtins.str,
        ) -> None:
            '''Defines the storage configuration for an Amazon EFS file system.

            :param file_system_id: The file system identifier.
            :param mount_point: The mount point for the file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-efsstorageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_m2 as m2
                
                efs_storage_configuration_property = m2.CfnEnvironment.EfsStorageConfigurationProperty(
                    file_system_id="fileSystemId",
                    mount_point="mountPoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a900881de75888b14aceb9c8d6b8dd545d5c6ae4cc8a292f3684725cc794e5c)
                check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
                check_type(argname="argument mount_point", value=mount_point, expected_type=type_hints["mount_point"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "file_system_id": file_system_id,
                "mount_point": mount_point,
            }

        @builtins.property
        def file_system_id(self) -> builtins.str:
            '''The file system identifier.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-efsstorageconfiguration.html#cfn-m2-environment-efsstorageconfiguration-filesystemid
            '''
            result = self._values.get("file_system_id")
            assert result is not None, "Required property 'file_system_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def mount_point(self) -> builtins.str:
            '''The mount point for the file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-efsstorageconfiguration.html#cfn-m2-environment-efsstorageconfiguration-mountpoint
            '''
            result = self._values.get("mount_point")
            assert result is not None, "Required property 'mount_point' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EfsStorageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_m2.CfnEnvironment.FsxStorageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"file_system_id": "fileSystemId", "mount_point": "mountPoint"},
    )
    class FsxStorageConfigurationProperty:
        def __init__(
            self,
            *,
            file_system_id: builtins.str,
            mount_point: builtins.str,
        ) -> None:
            '''Defines the storage configuration for an Amazon FSx file system.

            :param file_system_id: The file system identifier.
            :param mount_point: The mount point for the file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-fsxstorageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_m2 as m2
                
                fsx_storage_configuration_property = m2.CfnEnvironment.FsxStorageConfigurationProperty(
                    file_system_id="fileSystemId",
                    mount_point="mountPoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__113066e1dfb5e7e3a5a1e683d7bbdc75c9481e5844c707d11f385d9157f66878)
                check_type(argname="argument file_system_id", value=file_system_id, expected_type=type_hints["file_system_id"])
                check_type(argname="argument mount_point", value=mount_point, expected_type=type_hints["mount_point"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "file_system_id": file_system_id,
                "mount_point": mount_point,
            }

        @builtins.property
        def file_system_id(self) -> builtins.str:
            '''The file system identifier.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-fsxstorageconfiguration.html#cfn-m2-environment-fsxstorageconfiguration-filesystemid
            '''
            result = self._values.get("file_system_id")
            assert result is not None, "Required property 'file_system_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def mount_point(self) -> builtins.str:
            '''The mount point for the file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-fsxstorageconfiguration.html#cfn-m2-environment-fsxstorageconfiguration-mountpoint
            '''
            result = self._values.get("mount_point")
            assert result is not None, "Required property 'mount_point' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FsxStorageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_m2.CfnEnvironment.HighAvailabilityConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"desired_capacity": "desiredCapacity"},
    )
    class HighAvailabilityConfigProperty:
        def __init__(self, *, desired_capacity: jsii.Number) -> None:
            '''Defines the details of a high availability configuration.

            :param desired_capacity: The number of instances in a high availability configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-highavailabilityconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_m2 as m2
                
                high_availability_config_property = m2.CfnEnvironment.HighAvailabilityConfigProperty(
                    desired_capacity=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fbd4095bcf4793db9aa7c842c56c66983e40476c4a1fabe4f2703725f34f83a9)
                check_type(argname="argument desired_capacity", value=desired_capacity, expected_type=type_hints["desired_capacity"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "desired_capacity": desired_capacity,
            }

        @builtins.property
        def desired_capacity(self) -> jsii.Number:
            '''The number of instances in a high availability configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-highavailabilityconfig.html#cfn-m2-environment-highavailabilityconfig-desiredcapacity
            '''
            result = self._values.get("desired_capacity")
            assert result is not None, "Required property 'desired_capacity' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HighAvailabilityConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_m2.CfnEnvironment.StorageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"efs": "efs", "fsx": "fsx"},
    )
    class StorageConfigurationProperty:
        def __init__(
            self,
            *,
            efs: typing.Optional[typing.Union[typing.Union["CfnEnvironment.EfsStorageConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            fsx: typing.Optional[typing.Union[typing.Union["CfnEnvironment.FsxStorageConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Defines the storage configuration for a runtime environment.

            :param efs: Defines the storage configuration for an Amazon EFS file system.
            :param fsx: Defines the storage configuration for an Amazon FSx file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-storageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_m2 as m2
                
                storage_configuration_property = m2.CfnEnvironment.StorageConfigurationProperty(
                    efs=m2.CfnEnvironment.EfsStorageConfigurationProperty(
                        file_system_id="fileSystemId",
                        mount_point="mountPoint"
                    ),
                    fsx=m2.CfnEnvironment.FsxStorageConfigurationProperty(
                        file_system_id="fileSystemId",
                        mount_point="mountPoint"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ad4fd8e4615314c23d9812222befc779c91c49bc1d69a7e44350726158ee2e6b)
                check_type(argname="argument efs", value=efs, expected_type=type_hints["efs"])
                check_type(argname="argument fsx", value=fsx, expected_type=type_hints["fsx"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if efs is not None:
                self._values["efs"] = efs
            if fsx is not None:
                self._values["fsx"] = fsx

        @builtins.property
        def efs(
            self,
        ) -> typing.Optional[typing.Union["CfnEnvironment.EfsStorageConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Defines the storage configuration for an Amazon EFS file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-storageconfiguration.html#cfn-m2-environment-storageconfiguration-efs
            '''
            result = self._values.get("efs")
            return typing.cast(typing.Optional[typing.Union["CfnEnvironment.EfsStorageConfigurationProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def fsx(
            self,
        ) -> typing.Optional[typing.Union["CfnEnvironment.FsxStorageConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Defines the storage configuration for an Amazon FSx file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-storageconfiguration.html#cfn-m2-environment-storageconfiguration-fsx
            '''
            result = self._values.get("fsx")
            return typing.cast(typing.Optional[typing.Union["CfnEnvironment.FsxStorageConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_m2.CfnEnvironmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "engine_type": "engineType",
        "instance_type": "instanceType",
        "name": "name",
        "description": "description",
        "engine_version": "engineVersion",
        "high_availability_config": "highAvailabilityConfig",
        "kms_key_id": "kmsKeyId",
        "preferred_maintenance_window": "preferredMaintenanceWindow",
        "publicly_accessible": "publiclyAccessible",
        "security_group_ids": "securityGroupIds",
        "storage_configurations": "storageConfigurations",
        "subnet_ids": "subnetIds",
        "tags": "tags",
    },
)
class CfnEnvironmentProps:
    def __init__(
        self,
        *,
        engine_type: builtins.str,
        instance_type: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        high_availability_config: typing.Optional[typing.Union[typing.Union[CfnEnvironment.HighAvailabilityConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        storage_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEnvironment.StorageConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnEnvironment``.

        :param engine_type: The target platform for the runtime environment.
        :param instance_type: The instance type of the runtime environment.
        :param name: The name of the runtime environment.
        :param description: The description of the runtime environment.
        :param engine_version: The version of the runtime engine.
        :param high_availability_config: Defines the details of a high availability configuration.
        :param kms_key_id: The identifier of a customer managed key.
        :param preferred_maintenance_window: Configures the maintenance window you want for the runtime environment. If you do not provide a value, a random system-generated value will be assigned.
        :param publicly_accessible: Specifies whether the runtime environment is publicly accessible.
        :param security_group_ids: The list of security groups for the VPC associated with this runtime environment.
        :param storage_configurations: Defines the storage configuration for a runtime environment.
        :param subnet_ids: The list of subnets associated with the VPC for this runtime environment.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_m2 as m2
            
            cfn_environment_props = m2.CfnEnvironmentProps(
                engine_type="engineType",
                instance_type="instanceType",
                name="name",
            
                # the properties below are optional
                description="description",
                engine_version="engineVersion",
                high_availability_config=m2.CfnEnvironment.HighAvailabilityConfigProperty(
                    desired_capacity=123
                ),
                kms_key_id="kmsKeyId",
                preferred_maintenance_window="preferredMaintenanceWindow",
                publicly_accessible=False,
                security_group_ids=["securityGroupIds"],
                storage_configurations=[m2.CfnEnvironment.StorageConfigurationProperty(
                    efs=m2.CfnEnvironment.EfsStorageConfigurationProperty(
                        file_system_id="fileSystemId",
                        mount_point="mountPoint"
                    ),
                    fsx=m2.CfnEnvironment.FsxStorageConfigurationProperty(
                        file_system_id="fileSystemId",
                        mount_point="mountPoint"
                    )
                )],
                subnet_ids=["subnetIds"],
                tags={
                    "tags_key": "tags"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d9bdce057a4f99aec506d52f867a1ba56c0d5a96a438127f272bfea3e9655790)
            check_type(argname="argument engine_type", value=engine_type, expected_type=type_hints["engine_type"])
            check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument engine_version", value=engine_version, expected_type=type_hints["engine_version"])
            check_type(argname="argument high_availability_config", value=high_availability_config, expected_type=type_hints["high_availability_config"])
            check_type(argname="argument kms_key_id", value=kms_key_id, expected_type=type_hints["kms_key_id"])
            check_type(argname="argument preferred_maintenance_window", value=preferred_maintenance_window, expected_type=type_hints["preferred_maintenance_window"])
            check_type(argname="argument publicly_accessible", value=publicly_accessible, expected_type=type_hints["publicly_accessible"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument storage_configurations", value=storage_configurations, expected_type=type_hints["storage_configurations"])
            check_type(argname="argument subnet_ids", value=subnet_ids, expected_type=type_hints["subnet_ids"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "engine_type": engine_type,
            "instance_type": instance_type,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if engine_version is not None:
            self._values["engine_version"] = engine_version
        if high_availability_config is not None:
            self._values["high_availability_config"] = high_availability_config
        if kms_key_id is not None:
            self._values["kms_key_id"] = kms_key_id
        if preferred_maintenance_window is not None:
            self._values["preferred_maintenance_window"] = preferred_maintenance_window
        if publicly_accessible is not None:
            self._values["publicly_accessible"] = publicly_accessible
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if storage_configurations is not None:
            self._values["storage_configurations"] = storage_configurations
        if subnet_ids is not None:
            self._values["subnet_ids"] = subnet_ids
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def engine_type(self) -> builtins.str:
        '''The target platform for the runtime environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-enginetype
        '''
        result = self._values.get("engine_type")
        assert result is not None, "Required property 'engine_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def instance_type(self) -> builtins.str:
        '''The instance type of the runtime environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-instancetype
        '''
        result = self._values.get("instance_type")
        assert result is not None, "Required property 'instance_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the runtime environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the runtime environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def engine_version(self) -> typing.Optional[builtins.str]:
        '''The version of the runtime engine.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-engineversion
        '''
        result = self._values.get("engine_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def high_availability_config(
        self,
    ) -> typing.Optional[typing.Union[CfnEnvironment.HighAvailabilityConfigProperty, _IResolvable_a771d0ef]]:
        '''Defines the details of a high availability configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-highavailabilityconfig
        '''
        result = self._values.get("high_availability_config")
        return typing.cast(typing.Optional[typing.Union[CfnEnvironment.HighAvailabilityConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def kms_key_id(self) -> typing.Optional[builtins.str]:
        '''The identifier of a customer managed key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-kmskeyid
        '''
        result = self._values.get("kms_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_maintenance_window(self) -> typing.Optional[builtins.str]:
        '''Configures the maintenance window you want for the runtime environment.

        If you do not provide a value, a random system-generated value will be assigned.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-preferredmaintenancewindow
        '''
        result = self._values.get("preferred_maintenance_window")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether the runtime environment is publicly accessible.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-publiclyaccessible
        '''
        result = self._values.get("publicly_accessible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of security groups for the VPC associated with this runtime environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def storage_configurations(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnEnvironment.StorageConfigurationProperty, _IResolvable_a771d0ef]]]]:
        '''Defines the storage configuration for a runtime environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-storageconfigurations
        '''
        result = self._values.get("storage_configurations")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnEnvironment.StorageConfigurationProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def subnet_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The list of subnets associated with the VPC for this runtime environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-subnetids
        '''
        result = self._values.get("subnet_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApplication",
    "CfnApplicationProps",
    "CfnEnvironment",
    "CfnEnvironmentProps",
]

publication.publish()

def _typecheckingstub__9f391dc1b969dfd831609b4bf3887ebafa7c571218389b9cf8ef2f6abf05a28b(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    definition: typing.Union[typing.Union[CfnApplication.DefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    engine_type: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae4e7b0201375292850906bbe5e4141213b6d7caf147b1a1bfd328f46287076(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__952192cb2398a6a3569071281d5b71a988a0a8cfb4a5d9963ebb6298b87ad8d0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4d5c7d5e77a0e7374336f46943727e32bfce68fad4ad447e9ad8091bf45c61b(
    value: typing.Union[CfnApplication.DefinitionProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a0e7a9a1c6347cfdca26610489c43a53f97abf60b881b36d561eed8bc7cef85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d810ca0401f462b5eec217ff6d02e593ae70c1069c6c30dedb71a1e6e1e9b12(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77120bb7e6b688972ce04deb9bf893f246f3bea10696ce3f720de8e1c2987423(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d1b517302a4a732d02e08d98aad9b24f8780e35b33d8a6d782c9844b884cac6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fad95f17d0d8cf39f03ece774029cc8e0b396bdcf0f76a3c2ff8feae4b7c463a(
    *,
    content: typing.Optional[builtins.str] = None,
    s3_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a3637dc604d5563bcde8c8a5951e6aed69c651939e3dad4c022c20fbd55640b(
    *,
    definition: typing.Union[typing.Union[CfnApplication.DefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    engine_type: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54fae7b392cb1ef7a16e25177b6cf9f108a974095d8a2dd31f32bd3ad449270f(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    engine_type: builtins.str,
    instance_type: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    high_availability_config: typing.Optional[typing.Union[typing.Union[CfnEnvironment.HighAvailabilityConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    storage_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEnvironment.StorageConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba476f2306f11a7f744e13a05e9c3357f9ee9210befe30dd11780720e932851e(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7fa3a6a4026388b0a3d43603a5988efd5f1437faaf2d3f540241b266a64bc6e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0cde25d6123b2dfa2062b5bd871f5458a4657088fb8207d11a2ce0222e3238f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aabab80a324fd47f798ae9c99575b94f769d17d0d7a2e9d43564dce647b4117d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c396604c36ef46972e43cfef738b4f9e3c5ad1515bf0b9206c0b0529a831e14(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f93642af34d04943edf7725bef0d253f4774f6d802aa62cbc6810f125f86590(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84b57d103baafbd1c184d55f1175e1d815a341fd042b1ed13bf22737b17224d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4d72ba49a8abc6e46b93f6f359d1df01aada73df9cf578d68ffc2871e141002(
    value: typing.Optional[typing.Union[CfnEnvironment.HighAvailabilityConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ca66c0ffdbed1f674729134f10c7ee5c95d653343a0573363958d3e41d0e548(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7177a7f3948fb82521016eb9e1123092c0d1cd875c71e7b1cef84030f27952fa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82c3b98b65a586215e77a9fc72623359bcc7a25e452c4d75b0a3c9a90199e53(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__504ac76f645d55eb4933c01c8431dfc0bec13943b5969ac72a47985d64c1dfbb(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d8813ae37275cbff20dee5a2dc705482a57d00efc4ffe221be65455f7769666(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnEnvironment.StorageConfigurationProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6172d5592e7ec9236e0001a69b7d53ee89659678d2f18e8829e2bae11c4f4d45(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a900881de75888b14aceb9c8d6b8dd545d5c6ae4cc8a292f3684725cc794e5c(
    *,
    file_system_id: builtins.str,
    mount_point: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113066e1dfb5e7e3a5a1e683d7bbdc75c9481e5844c707d11f385d9157f66878(
    *,
    file_system_id: builtins.str,
    mount_point: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbd4095bcf4793db9aa7c842c56c66983e40476c4a1fabe4f2703725f34f83a9(
    *,
    desired_capacity: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad4fd8e4615314c23d9812222befc779c91c49bc1d69a7e44350726158ee2e6b(
    *,
    efs: typing.Optional[typing.Union[typing.Union[CfnEnvironment.EfsStorageConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    fsx: typing.Optional[typing.Union[typing.Union[CfnEnvironment.FsxStorageConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d9bdce057a4f99aec506d52f867a1ba56c0d5a96a438127f272bfea3e9655790(
    *,
    engine_type: builtins.str,
    instance_type: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    high_availability_config: typing.Optional[typing.Union[typing.Union[CfnEnvironment.HighAvailabilityConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    storage_configurations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEnvironment.StorageConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
