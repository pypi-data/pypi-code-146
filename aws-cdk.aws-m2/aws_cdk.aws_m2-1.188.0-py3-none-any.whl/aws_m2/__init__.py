'''
# AWS::M2 Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_m2 as m2
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

from ._jsii import *

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnApplication(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-m2.CfnApplication",
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
        import aws_cdk.aws_m2 as m2
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        definition: typing.Union[typing.Union["CfnApplication.DefinitionProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b40bb4f41a08b733fe6497ac2c5ed13354f03cd9a7d9ec74795fa84f4332f94)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25946d1e92f1ae5c53f26aae286fc96f2af7eeb2fa0def327d9b5177a60f2739)
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
            type_hints = typing.get_type_hints(_typecheckingstub__95d843d41ef773e18542edcf0d33c50ec495be2baf7e995f1e64d4efe0277532)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="definition")
    def definition(
        self,
    ) -> typing.Union["CfnApplication.DefinitionProperty", _aws_cdk_core_f4b25747.IResolvable]:
        '''The application definition for a particular application. You can specify either inline JSON or an Amazon S3 bucket location.

        For information about application definitions, see the `AWS Mainframe Modernization User Guide <https://docs.aws.amazon.com/m2/latest/userguide/applications-m2-definition.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-definition
        '''
        return typing.cast(typing.Union["CfnApplication.DefinitionProperty", _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "definition"))

    @definition.setter
    def definition(
        self,
        value: typing.Union["CfnApplication.DefinitionProperty", _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f0ae2fc2578919cfbf186bc6b9dbad7dd640bba5c69eb0cd2e55813bff8c4a4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca1c091644d5fd83c506a5e4a8f99b012af2f97498d4e0f5519675ec9a184e98)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6840b7bef829a909c387355ca9b874f5c079efb94e007a69ce7ac33d988b091a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f84cf4d0c3ac541a49b62b6d55a984e294f5a5056aacaf35793c872b8e5fc268)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0e389dee42c79940f488fb4937a9bd60c27a654fd62fafa5f49d37b74a9de17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "kmsKeyId", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-m2.CfnApplication.DefinitionProperty",
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
                import aws_cdk.aws_m2 as m2
                
                definition_property = m2.CfnApplication.DefinitionProperty(
                    content="content",
                    s3_location="s3Location"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4513bd3505c01ffbc5528321b3a4ee8ab88a73f68db21f01e7f716428deb0e14)
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
    jsii_type="@aws-cdk/aws-m2.CfnApplicationProps",
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
        definition: typing.Union[typing.Union[CfnApplication.DefinitionProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
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
            import aws_cdk.aws_m2 as m2
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__2404c099d129cb00d38cb6569ae21d46e7b9daaab2636f7ad32a1c542e596119)
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
    ) -> typing.Union[CfnApplication.DefinitionProperty, _aws_cdk_core_f4b25747.IResolvable]:
        '''The application definition for a particular application. You can specify either inline JSON or an Amazon S3 bucket location.

        For information about application definitions, see the `AWS Mainframe Modernization User Guide <https://docs.aws.amazon.com/m2/latest/userguide/applications-m2-definition.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-application.html#cfn-m2-application-definition
        '''
        result = self._values.get("definition")
        assert result is not None, "Required property 'definition' is missing"
        return typing.cast(typing.Union[CfnApplication.DefinitionProperty, _aws_cdk_core_f4b25747.IResolvable], result)

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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnEnvironment(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-m2.CfnEnvironment",
):
    '''A CloudFormation ``AWS::M2::Environment``.

    Specifies a runtime environment for a given runtime engine.

    :cloudformationResource: AWS::M2::Environment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_m2 as m2
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        engine_type: builtins.str,
        instance_type: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        engine_version: typing.Optional[builtins.str] = None,
        high_availability_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEnvironment.HighAvailabilityConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        storage_configurations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEnvironment.StorageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__883f4c0e0348f2cbda154fa0bc1792376955dbb823cb0f0396ab756135a20eec)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a883d33e3ad63d0ecb56c144a996456977a663d2693bd3b186bfcd6015bc35e1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2508c70510fddd40a17628c381401327591ee0a809feafab4f41bf546ddfe9e4)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ca6a22f2eca06fe8e776e31e545dc88998cc2fe08e1f274e1d6f27543edc5105)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b33777b954a0b9fe4837a0c6d01026bdb9da8b01ef61f8760aca3df5aef5106c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__97ad134eabef6f0ecb9436274011d0620daefb48cc96f281ea07a95c7537e349)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2dba85fa80cefd1e40770b84759fd46ffee54b6bffdc4fb2f6c8c19d97be70a1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9cdbac826b554ede4079a7818ddc77e949859399602716eea31a78a5d1ab0e59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "engineVersion", value)

    @builtins.property
    @jsii.member(jsii_name="highAvailabilityConfig")
    def high_availability_config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.HighAvailabilityConfigProperty"]]:
        '''Defines the details of a high availability configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-highavailabilityconfig
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.HighAvailabilityConfigProperty"]], jsii.get(self, "highAvailabilityConfig"))

    @high_availability_config.setter
    def high_availability_config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.HighAvailabilityConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e4f524818957aca7ef3faee5b6eed31177113bf20d9182c2221897a1be5980d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__71af29a8dafa346cc55ec540963015d44f7efa2bcc471bf6f0701ef5fc4b9236)
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
            type_hints = typing.get_type_hints(_typecheckingstub__22be6bf51f48621230e5e09eb6a3966042a76c43ac399b651810d1746c1b1b99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredMaintenanceWindow", value)

    @builtins.property
    @jsii.member(jsii_name="publiclyAccessible")
    def publicly_accessible(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether the runtime environment is publicly accessible.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-publiclyaccessible
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "publiclyAccessible"))

    @publicly_accessible.setter
    def publicly_accessible(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daa7cc00cf21691e423f68dace11eeb97a81b330714eaa7775153b366201ac12)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c618441f2bd2909bdd0790242cc271b8cba260762643b556c667ab4fa9b5186)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="storageConfigurations")
    def storage_configurations(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.StorageConfigurationProperty"]]]]:
        '''Defines the storage configuration for a runtime environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-storageconfigurations
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.StorageConfigurationProperty"]]]], jsii.get(self, "storageConfigurations"))

    @storage_configurations.setter
    def storage_configurations(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.StorageConfigurationProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2094dfc52804e8f1b5a5d338965b30e3b8f68b140b0b53ac6b2a1fc147625ca7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a67ed98a26f8382b4e7acc974e3e1750a4c75acea0a6f4e941daea51aea29db9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetIds", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-m2.CfnEnvironment.EfsStorageConfigurationProperty",
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
                import aws_cdk.aws_m2 as m2
                
                efs_storage_configuration_property = m2.CfnEnvironment.EfsStorageConfigurationProperty(
                    file_system_id="fileSystemId",
                    mount_point="mountPoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0550b299c3e9a795089d9d96c992969d5dd3a367d611109a71eeae62f0739e88)
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
        jsii_type="@aws-cdk/aws-m2.CfnEnvironment.FsxStorageConfigurationProperty",
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
                import aws_cdk.aws_m2 as m2
                
                fsx_storage_configuration_property = m2.CfnEnvironment.FsxStorageConfigurationProperty(
                    file_system_id="fileSystemId",
                    mount_point="mountPoint"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4cf28e0fe80f1653032be33d4ea8db5e4fc454fc1aa957db8ab651163ea56480)
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
        jsii_type="@aws-cdk/aws-m2.CfnEnvironment.HighAvailabilityConfigProperty",
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
                import aws_cdk.aws_m2 as m2
                
                high_availability_config_property = m2.CfnEnvironment.HighAvailabilityConfigProperty(
                    desired_capacity=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b1904d09e4a74dae5db1ff2b187fbe338621b77d251bac23f1934c52f7c76fd)
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
        jsii_type="@aws-cdk/aws-m2.CfnEnvironment.StorageConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"efs": "efs", "fsx": "fsx"},
    )
    class StorageConfigurationProperty:
        def __init__(
            self,
            *,
            efs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEnvironment.EfsStorageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            fsx: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEnvironment.FsxStorageConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Defines the storage configuration for a runtime environment.

            :param efs: Defines the storage configuration for an Amazon EFS file system.
            :param fsx: Defines the storage configuration for an Amazon FSx file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-storageconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_m2 as m2
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__49c561392b16e0a38ed24ffeeadc219beb8737f33826dc34d498dc8a08c2733e)
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
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.EfsStorageConfigurationProperty"]]:
            '''Defines the storage configuration for an Amazon EFS file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-storageconfiguration.html#cfn-m2-environment-storageconfiguration-efs
            '''
            result = self._values.get("efs")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.EfsStorageConfigurationProperty"]], result)

        @builtins.property
        def fsx(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.FsxStorageConfigurationProperty"]]:
            '''Defines the storage configuration for an Amazon FSx file system.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-m2-environment-storageconfiguration.html#cfn-m2-environment-storageconfiguration-fsx
            '''
            result = self._values.get("fsx")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.FsxStorageConfigurationProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StorageConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-m2.CfnEnvironmentProps",
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
        high_availability_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEnvironment.HighAvailabilityConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        kms_key_id: typing.Optional[builtins.str] = None,
        preferred_maintenance_window: typing.Optional[builtins.str] = None,
        publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        storage_configurations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEnvironment.StorageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
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
            import aws_cdk.aws_m2 as m2
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__76b0315510d3cf7cd9e9359d057a573a26d33167d1f797fd1a3381a84d8287b8)
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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEnvironment.HighAvailabilityConfigProperty]]:
        '''Defines the details of a high availability configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-highavailabilityconfig
        '''
        result = self._values.get("high_availability_config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEnvironment.HighAvailabilityConfigProperty]], result)

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
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies whether the runtime environment is publicly accessible.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-publiclyaccessible
        '''
        result = self._values.get("publicly_accessible")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEnvironment.StorageConfigurationProperty]]]]:
        '''Defines the storage configuration for a runtime environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-m2-environment.html#cfn-m2-environment-storageconfigurations
        '''
        result = self._values.get("storage_configurations")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEnvironment.StorageConfigurationProperty]]]], result)

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

def _typecheckingstub__8b40bb4f41a08b733fe6497ac2c5ed13354f03cd9a7d9ec74795fa84f4332f94(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    definition: typing.Union[typing.Union[CfnApplication.DefinitionProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    engine_type: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25946d1e92f1ae5c53f26aae286fc96f2af7eeb2fa0def327d9b5177a60f2739(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95d843d41ef773e18542edcf0d33c50ec495be2baf7e995f1e64d4efe0277532(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f0ae2fc2578919cfbf186bc6b9dbad7dd640bba5c69eb0cd2e55813bff8c4a4(
    value: typing.Union[CfnApplication.DefinitionProperty, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca1c091644d5fd83c506a5e4a8f99b012af2f97498d4e0f5519675ec9a184e98(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6840b7bef829a909c387355ca9b874f5c079efb94e007a69ce7ac33d988b091a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f84cf4d0c3ac541a49b62b6d55a984e294f5a5056aacaf35793c872b8e5fc268(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0e389dee42c79940f488fb4937a9bd60c27a654fd62fafa5f49d37b74a9de17(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4513bd3505c01ffbc5528321b3a4ee8ab88a73f68db21f01e7f716428deb0e14(
    *,
    content: typing.Optional[builtins.str] = None,
    s3_location: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2404c099d129cb00d38cb6569ae21d46e7b9daaab2636f7ad32a1c542e596119(
    *,
    definition: typing.Union[typing.Union[CfnApplication.DefinitionProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable],
    engine_type: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__883f4c0e0348f2cbda154fa0bc1792376955dbb823cb0f0396ab756135a20eec(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    engine_type: builtins.str,
    instance_type: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    high_availability_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEnvironment.HighAvailabilityConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    storage_configurations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEnvironment.StorageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a883d33e3ad63d0ecb56c144a996456977a663d2693bd3b186bfcd6015bc35e1(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2508c70510fddd40a17628c381401327591ee0a809feafab4f41bf546ddfe9e4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca6a22f2eca06fe8e776e31e545dc88998cc2fe08e1f274e1d6f27543edc5105(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b33777b954a0b9fe4837a0c6d01026bdb9da8b01ef61f8760aca3df5aef5106c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ad134eabef6f0ecb9436274011d0620daefb48cc96f281ea07a95c7537e349(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dba85fa80cefd1e40770b84759fd46ffee54b6bffdc4fb2f6c8c19d97be70a1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cdbac826b554ede4079a7818ddc77e949859399602716eea31a78a5d1ab0e59(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e4f524818957aca7ef3faee5b6eed31177113bf20d9182c2221897a1be5980d(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEnvironment.HighAvailabilityConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71af29a8dafa346cc55ec540963015d44f7efa2bcc471bf6f0701ef5fc4b9236(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22be6bf51f48621230e5e09eb6a3966042a76c43ac399b651810d1746c1b1b99(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daa7cc00cf21691e423f68dace11eeb97a81b330714eaa7775153b366201ac12(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c618441f2bd2909bdd0790242cc271b8cba260762643b556c667ab4fa9b5186(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2094dfc52804e8f1b5a5d338965b30e3b8f68b140b0b53ac6b2a1fc147625ca7(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEnvironment.StorageConfigurationProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a67ed98a26f8382b4e7acc974e3e1750a4c75acea0a6f4e941daea51aea29db9(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0550b299c3e9a795089d9d96c992969d5dd3a367d611109a71eeae62f0739e88(
    *,
    file_system_id: builtins.str,
    mount_point: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf28e0fe80f1653032be33d4ea8db5e4fc454fc1aa957db8ab651163ea56480(
    *,
    file_system_id: builtins.str,
    mount_point: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b1904d09e4a74dae5db1ff2b187fbe338621b77d251bac23f1934c52f7c76fd(
    *,
    desired_capacity: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49c561392b16e0a38ed24ffeeadc219beb8737f33826dc34d498dc8a08c2733e(
    *,
    efs: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEnvironment.EfsStorageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    fsx: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEnvironment.FsxStorageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76b0315510d3cf7cd9e9359d057a573a26d33167d1f797fd1a3381a84d8287b8(
    *,
    engine_type: builtins.str,
    instance_type: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    engine_version: typing.Optional[builtins.str] = None,
    high_availability_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEnvironment.HighAvailabilityConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    kms_key_id: typing.Optional[builtins.str] = None,
    preferred_maintenance_window: typing.Optional[builtins.str] = None,
    publicly_accessible: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    storage_configurations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEnvironment.StorageConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    subnet_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass
