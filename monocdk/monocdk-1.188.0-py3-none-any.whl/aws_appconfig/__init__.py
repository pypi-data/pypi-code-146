'''
# AWS::AppConfig Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as appconfig
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for AppConfig construct libraries](https://constructs.dev/search?q=appconfig)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::AppConfig resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppConfig.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::AppConfig](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AppConfig.html).

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
class CfnApplication(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appconfig.CfnApplication",
):
    '''A CloudFormation ``AWS::AppConfig::Application``.

    The ``AWS::AppConfig::Application`` resource creates an application. In AWS AppConfig , an application is simply an organizational construct like a folder. This organizational construct has a relationship with some unit of executable code. For example, you could create an application called MyMobileApp to organize and manage configuration data for a mobile application installed by your users.

    AWS AppConfig requires that you create resources and deploy a configuration in the following order:

    - Create an application
    - Create an environment
    - Create a configuration profile
    - Create a deployment strategy
    - Deploy the configuration

    For more information, see `AWS AppConfig <https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html>`_ in the *AWS AppConfig User Guide* .

    :cloudformationResource: AWS::AppConfig::Application
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-application.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appconfig as appconfig
        
        cfn_application = appconfig.CfnApplication(self, "MyCfnApplication",
            name="name",
        
            # the properties below are optional
            description="description",
            tags=[appconfig.CfnApplication.TagsProperty(
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
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnApplication.TagsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AppConfig::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: A name for the application.
        :param description: A description of the application.
        :param tags: Metadata to assign to the application. Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec152a2424059a52defce300feb837353a1ccec3c21563f8fdea009a72b89d73)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationProps(name=name, description=description, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c9aae7cdb36122bb6c4ab8463c102a4fb2925d6974c1f59967dc03304d701ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa346e99720de56b7ba79900dd51f9351bb8ec09b75e2909c99e0ca83e69dd2e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A name for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-application.html#cfn-appconfig-application-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db03372be65c650c74040bfa9e9373ee2f55a018d5e257613ad1d4d16ae3cba2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-application.html#cfn-appconfig-application-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec31f469612e1138eedb31c77883512dd32329fda9e02f11eb836ee50cd99a41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["CfnApplication.TagsProperty"]]:
        '''Metadata to assign to the application.

        Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-application.html#cfn-appconfig-application-tags
        '''
        return typing.cast(typing.Optional[typing.List["CfnApplication.TagsProperty"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["CfnApplication.TagsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fae9db3331e3c5d64b3a00b60bace9e22e36c8b6f420f6963f2e98a311b164fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appconfig.CfnApplication.TagsProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Metadata to assign to the application.

            Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.

            :param key: The key-value string map. The valid character set is ``[a-zA-Z+-=._:/]`` . The tag key can be up to 128 characters and must not start with ``aws:`` .
            :param value: The tag value can be up to 256 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-application-tags.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appconfig as appconfig
                
                tags_property = appconfig.CfnApplication.TagsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__960b2812ec9fe7b48b718dbac53e02a21b0beb7e275f461a29962ded820f9961)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key-value string map.

            The valid character set is ``[a-zA-Z+-=._:/]`` . The tag key can be up to 128 characters and must not start with ``aws:`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-application-tags.html#cfn-appconfig-application-tags-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The tag value can be up to 256 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-application-tags.html#cfn-appconfig-application-tags-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appconfig.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "description": "description", "tags": "tags"},
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[CfnApplication.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApplication``.

        :param name: A name for the application.
        :param description: A description of the application.
        :param tags: Metadata to assign to the application. Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appconfig as appconfig
            
            cfn_application_props = appconfig.CfnApplicationProps(
                name="name",
            
                # the properties below are optional
                description="description",
                tags=[appconfig.CfnApplication.TagsProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__357c8ae80f97ad1d610c76688854f27219ad431090a0b9c8e29c1ea65dda0b66)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''A name for the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-application.html#cfn-appconfig-application-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-application.html#cfn-appconfig-application-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[CfnApplication.TagsProperty]]:
        '''Metadata to assign to the application.

        Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-application.html#cfn-appconfig-application-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[CfnApplication.TagsProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnConfigurationProfile(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appconfig.CfnConfigurationProfile",
):
    '''A CloudFormation ``AWS::AppConfig::ConfigurationProfile``.

    The ``AWS::AppConfig::ConfigurationProfile`` resource creates a configuration profile that enables AWS AppConfig to access the configuration source. Valid configuration sources include AWS Systems Manager (SSM) documents, SSM Parameter Store parameters, and Amazon S3 . A configuration profile includes the following information.

    - The Uri location of the configuration data.
    - The AWS Identity and Access Management ( IAM ) role that provides access to the configuration data.
    - A validator for the configuration data. Available validators include either a JSON Schema or the Amazon Resource Name (ARN) of an AWS Lambda function.

    AWS AppConfig requires that you create resources and deploy a configuration in the following order:

    - Create an application
    - Create an environment
    - Create a configuration profile
    - Create a deployment strategy
    - Deploy the configuration

    For more information, see `AWS AppConfig <https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html>`_ in the *AWS AppConfig User Guide* .

    :cloudformationResource: AWS::AppConfig::ConfigurationProfile
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appconfig as appconfig
        
        cfn_configuration_profile = appconfig.CfnConfigurationProfile(self, "MyCfnConfigurationProfile",
            application_id="applicationId",
            location_uri="locationUri",
            name="name",
        
            # the properties below are optional
            description="description",
            retrieval_role_arn="retrievalRoleArn",
            tags=[appconfig.CfnConfigurationProfile.TagsProperty(
                key="key",
                value="value"
            )],
            type="type",
            validators=[appconfig.CfnConfigurationProfile.ValidatorsProperty(
                content="content",
                type="type"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_id: builtins.str,
        location_uri: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        retrieval_role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnConfigurationProfile.TagsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
        validators: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnConfigurationProfile.ValidatorsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AppConfig::ConfigurationProfile``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The application ID.
        :param location_uri: A URI to locate the configuration. You can specify the AWS AppConfig hosted configuration store, Systems Manager (SSM) document, an SSM Parameter Store parameter, or an Amazon S3 object. For the hosted configuration store and for feature flags, specify ``hosted`` . For an SSM document, specify either the document name in the format ``ssm-document://<Document_name>`` or the Amazon Resource Name (ARN). For a parameter, specify either the parameter name in the format ``ssm-parameter://<Parameter_name>`` or the ARN. For an Amazon S3 object, specify the URI in the following format: ``s3://<bucket>/<objectKey>`` . Here is an example: ``s3://my-bucket/my-app/us-east-1/my-config.json``
        :param name: A name for the configuration profile.
        :param description: A description of the configuration profile.
        :param retrieval_role_arn: The ARN of an IAM role with permission to access the configuration at the specified ``LocationUri`` . .. epigraph:: A retrieval role ARN is not required for configurations stored in the AWS AppConfig hosted configuration store. It is required for all other sources that store your configuration.
        :param tags: Metadata to assign to the configuration profile. Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.
        :param type: The type of configurations contained in the profile. AWS AppConfig supports ``feature flags`` and ``freeform`` configurations. We recommend you create feature flag configurations to enable or disable new features and freeform configurations to distribute configurations to an application. When calling this API, enter one of the following values for ``Type`` : ``AWS.AppConfig.FeatureFlags`` ``AWS.Freeform``
        :param validators: A list of methods for validating the configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4bf602951e7752d0034cae15c7747926298a301f74acc64a6c17c88a5e4c410)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConfigurationProfileProps(
            application_id=application_id,
            location_uri=location_uri,
            name=name,
            description=description,
            retrieval_role_arn=retrieval_role_arn,
            tags=tags,
            type=type,
            validators=validators,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b6f4977d311db9bfa16e0c5f5a3af46057e8fc1c35f6ac26f73169b8690f6ae)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c13487eeded5b42e89b931e8e4432a2654066ad862e334d1fdd83dcc4e56b9cb)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The application ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f5e76a2700709291108cc6e532f1a4393dd43f3921d8c8467968a8a63703952)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="locationUri")
    def location_uri(self) -> builtins.str:
        '''A URI to locate the configuration.

        You can specify the AWS AppConfig hosted configuration store, Systems Manager (SSM) document, an SSM Parameter Store parameter, or an Amazon S3 object. For the hosted configuration store and for feature flags, specify ``hosted`` . For an SSM document, specify either the document name in the format ``ssm-document://<Document_name>`` or the Amazon Resource Name (ARN). For a parameter, specify either the parameter name in the format ``ssm-parameter://<Parameter_name>`` or the ARN. For an Amazon S3 object, specify the URI in the following format: ``s3://<bucket>/<objectKey>`` . Here is an example: ``s3://my-bucket/my-app/us-east-1/my-config.json``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-locationuri
        '''
        return typing.cast(builtins.str, jsii.get(self, "locationUri"))

    @location_uri.setter
    def location_uri(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff97b168e6f301d1671c26e67d27f4af286d6d3ff4e91ed47e5701e0ae33671)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locationUri", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A name for the configuration profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__096c5799793d92c65fdeffea02afa19ada49b599d590619302db56764d1332f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the configuration profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44e108938c05e845d3ad88d8e000dfa8c040d95650f892739963d12d9786d48a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="retrievalRoleArn")
    def retrieval_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an IAM role with permission to access the configuration at the specified ``LocationUri`` .

        .. epigraph::

           A retrieval role ARN is not required for configurations stored in the AWS AppConfig hosted configuration store. It is required for all other sources that store your configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-retrievalrolearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "retrievalRoleArn"))

    @retrieval_role_arn.setter
    def retrieval_role_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccac18e19ae9b4f17548d1235009136dc600a742ebc38b820f975f4992339a46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "retrievalRoleArn", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnConfigurationProfile.TagsProperty"]]:
        '''Metadata to assign to the configuration profile.

        Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-tags
        '''
        return typing.cast(typing.Optional[typing.List["CfnConfigurationProfile.TagsProperty"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["CfnConfigurationProfile.TagsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9280488cb4ab8117a46a52344337a74a2231278ebb301fbe899d41cb842fc105)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of configurations contained in the profile.

        AWS AppConfig supports ``feature flags`` and ``freeform`` configurations. We recommend you create feature flag configurations to enable or disable new features and freeform configurations to distribute configurations to an application. When calling this API, enter one of the following values for ``Type`` :

        ``AWS.AppConfig.FeatureFlags``

        ``AWS.Freeform``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-type
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "type"))

    @type.setter
    def type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f5a28cee2b2da0f0166102ecfa3453dc5b45b225fa94b631af6ae767be8cd6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="validators")
    def validators(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnConfigurationProfile.ValidatorsProperty", _IResolvable_a771d0ef]]]]:
        '''A list of methods for validating the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-validators
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnConfigurationProfile.ValidatorsProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "validators"))

    @validators.setter
    def validators(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnConfigurationProfile.ValidatorsProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0c1807f3d918ee8c709b06715b0ca85b5cdac64bbac8602c25c8cb9b4bb38fe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validators", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appconfig.CfnConfigurationProfile.TagsProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Metadata to assign to the configuration profile.

            Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.

            :param key: The key-value string map. The valid character set is ``[a-zA-Z+-=._:/]`` . The tag key can be up to 128 characters and must not start with ``aws:`` .
            :param value: The tag value can be up to 256 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-configurationprofile-tags.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appconfig as appconfig
                
                tags_property = appconfig.CfnConfigurationProfile.TagsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__284511a37056bcc175d3eee47fa90074831bfde8a7c3167aa7c088924db1290a)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key-value string map.

            The valid character set is ``[a-zA-Z+-=._:/]`` . The tag key can be up to 128 characters and must not start with ``aws:`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-configurationprofile-tags.html#cfn-appconfig-configurationprofile-tags-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The tag value can be up to 256 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-configurationprofile-tags.html#cfn-appconfig-configurationprofile-tags-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appconfig.CfnConfigurationProfile.ValidatorsProperty",
        jsii_struct_bases=[],
        name_mapping={"content": "content", "type": "type"},
    )
    class ValidatorsProperty:
        def __init__(
            self,
            *,
            content: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A validator provides a syntactic or semantic check to ensure the configuration that you want to deploy functions as intended.

            To validate your application configuration data, you provide a schema or an AWS Lambda function that runs against the configuration. The configuration deployment or update can only proceed when the configuration data is valid.

            :param content: Either the JSON Schema content or the Amazon Resource Name (ARN) of an Lambda function.
            :param type: AWS AppConfig supports validators of type ``JSON_SCHEMA`` and ``LAMBDA``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-configurationprofile-validators.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appconfig as appconfig
                
                validators_property = appconfig.CfnConfigurationProfile.ValidatorsProperty(
                    content="content",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__92cb623060f8be207323219f2dfccd6d68490453218828390667c826cd8e0d50)
                check_type(argname="argument content", value=content, expected_type=type_hints["content"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if content is not None:
                self._values["content"] = content
            if type is not None:
                self._values["type"] = type

        @builtins.property
        def content(self) -> typing.Optional[builtins.str]:
            '''Either the JSON Schema content or the Amazon Resource Name (ARN) of an Lambda function.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-configurationprofile-validators.html#cfn-appconfig-configurationprofile-validators-content
            '''
            result = self._values.get("content")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''AWS AppConfig supports validators of type ``JSON_SCHEMA`` and ``LAMBDA``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-configurationprofile-validators.html#cfn-appconfig-configurationprofile-validators-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ValidatorsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appconfig.CfnConfigurationProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "location_uri": "locationUri",
        "name": "name",
        "description": "description",
        "retrieval_role_arn": "retrievalRoleArn",
        "tags": "tags",
        "type": "type",
        "validators": "validators",
    },
)
class CfnConfigurationProfileProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        location_uri: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        retrieval_role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[CfnConfigurationProfile.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
        validators: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnConfigurationProfile.ValidatorsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnConfigurationProfile``.

        :param application_id: The application ID.
        :param location_uri: A URI to locate the configuration. You can specify the AWS AppConfig hosted configuration store, Systems Manager (SSM) document, an SSM Parameter Store parameter, or an Amazon S3 object. For the hosted configuration store and for feature flags, specify ``hosted`` . For an SSM document, specify either the document name in the format ``ssm-document://<Document_name>`` or the Amazon Resource Name (ARN). For a parameter, specify either the parameter name in the format ``ssm-parameter://<Parameter_name>`` or the ARN. For an Amazon S3 object, specify the URI in the following format: ``s3://<bucket>/<objectKey>`` . Here is an example: ``s3://my-bucket/my-app/us-east-1/my-config.json``
        :param name: A name for the configuration profile.
        :param description: A description of the configuration profile.
        :param retrieval_role_arn: The ARN of an IAM role with permission to access the configuration at the specified ``LocationUri`` . .. epigraph:: A retrieval role ARN is not required for configurations stored in the AWS AppConfig hosted configuration store. It is required for all other sources that store your configuration.
        :param tags: Metadata to assign to the configuration profile. Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.
        :param type: The type of configurations contained in the profile. AWS AppConfig supports ``feature flags`` and ``freeform`` configurations. We recommend you create feature flag configurations to enable or disable new features and freeform configurations to distribute configurations to an application. When calling this API, enter one of the following values for ``Type`` : ``AWS.AppConfig.FeatureFlags`` ``AWS.Freeform``
        :param validators: A list of methods for validating the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appconfig as appconfig
            
            cfn_configuration_profile_props = appconfig.CfnConfigurationProfileProps(
                application_id="applicationId",
                location_uri="locationUri",
                name="name",
            
                # the properties below are optional
                description="description",
                retrieval_role_arn="retrievalRoleArn",
                tags=[appconfig.CfnConfigurationProfile.TagsProperty(
                    key="key",
                    value="value"
                )],
                type="type",
                validators=[appconfig.CfnConfigurationProfile.ValidatorsProperty(
                    content="content",
                    type="type"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__985557944d583335f64edcaaa04451a0217dfebf6dc1a2b4cc47636249138950)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument location_uri", value=location_uri, expected_type=type_hints["location_uri"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument retrieval_role_arn", value=retrieval_role_arn, expected_type=type_hints["retrieval_role_arn"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument validators", value=validators, expected_type=type_hints["validators"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "location_uri": location_uri,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if retrieval_role_arn is not None:
            self._values["retrieval_role_arn"] = retrieval_role_arn
        if tags is not None:
            self._values["tags"] = tags
        if type is not None:
            self._values["type"] = type
        if validators is not None:
            self._values["validators"] = validators

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The application ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def location_uri(self) -> builtins.str:
        '''A URI to locate the configuration.

        You can specify the AWS AppConfig hosted configuration store, Systems Manager (SSM) document, an SSM Parameter Store parameter, or an Amazon S3 object. For the hosted configuration store and for feature flags, specify ``hosted`` . For an SSM document, specify either the document name in the format ``ssm-document://<Document_name>`` or the Amazon Resource Name (ARN). For a parameter, specify either the parameter name in the format ``ssm-parameter://<Parameter_name>`` or the ARN. For an Amazon S3 object, specify the URI in the following format: ``s3://<bucket>/<objectKey>`` . Here is an example: ``s3://my-bucket/my-app/us-east-1/my-config.json``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-locationuri
        '''
        result = self._values.get("location_uri")
        assert result is not None, "Required property 'location_uri' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A name for the configuration profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the configuration profile.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def retrieval_role_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of an IAM role with permission to access the configuration at the specified ``LocationUri`` .

        .. epigraph::

           A retrieval role ARN is not required for configurations stored in the AWS AppConfig hosted configuration store. It is required for all other sources that store your configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-retrievalrolearn
        '''
        result = self._values.get("retrieval_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(
        self,
    ) -> typing.Optional[typing.List[CfnConfigurationProfile.TagsProperty]]:
        '''Metadata to assign to the configuration profile.

        Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[CfnConfigurationProfile.TagsProperty]], result)

    @builtins.property
    def type(self) -> typing.Optional[builtins.str]:
        '''The type of configurations contained in the profile.

        AWS AppConfig supports ``feature flags`` and ``freeform`` configurations. We recommend you create feature flag configurations to enable or disable new features and freeform configurations to distribute configurations to an application. When calling this API, enter one of the following values for ``Type`` :

        ``AWS.AppConfig.FeatureFlags``

        ``AWS.Freeform``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-type
        '''
        result = self._values.get("type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def validators(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnConfigurationProfile.ValidatorsProperty, _IResolvable_a771d0ef]]]]:
        '''A list of methods for validating the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-validators
        '''
        result = self._values.get("validators")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnConfigurationProfile.ValidatorsProperty, _IResolvable_a771d0ef]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDeployment(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appconfig.CfnDeployment",
):
    '''A CloudFormation ``AWS::AppConfig::Deployment``.

    The ``AWS::AppConfig::Deployment`` resource starts a deployment. Starting a deployment in AWS AppConfig calls the ``StartDeployment`` API action. This call includes the IDs of the AWS AppConfig application, the environment, the configuration profile, and (optionally) the configuration data version to deploy. The call also includes the ID of the deployment strategy to use, which determines how the configuration data is deployed.

    AWS AppConfig monitors the distribution to all hosts and reports status. If a distribution fails, then AWS AppConfig rolls back the configuration.

    AWS AppConfig requires that you create resources and deploy a configuration in the following order:

    - Create an application
    - Create an environment
    - Create a configuration profile
    - Create a deployment strategy
    - Deploy the configuration

    For more information, see `AWS AppConfig <https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html>`_ in the *AWS AppConfig User Guide* .

    :cloudformationResource: AWS::AppConfig::Deployment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appconfig as appconfig
        
        cfn_deployment = appconfig.CfnDeployment(self, "MyCfnDeployment",
            application_id="applicationId",
            configuration_profile_id="configurationProfileId",
            configuration_version="configurationVersion",
            deployment_strategy_id="deploymentStrategyId",
            environment_id="environmentId",
        
            # the properties below are optional
            description="description",
            tags=[appconfig.CfnDeployment.TagsProperty(
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
        application_id: builtins.str,
        configuration_profile_id: builtins.str,
        configuration_version: builtins.str,
        deployment_strategy_id: builtins.str,
        environment_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnDeployment.TagsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AppConfig::Deployment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The application ID.
        :param configuration_profile_id: The configuration profile ID.
        :param configuration_version: The configuration version to deploy.
        :param deployment_strategy_id: The deployment strategy ID.
        :param environment_id: The environment ID.
        :param description: A description of the deployment.
        :param tags: Metadata to assign to the deployment. Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31d91590582afbfb0f4740993d3fe5611f9a1fe54d092d86ab4e585607affa20)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDeploymentProps(
            application_id=application_id,
            configuration_profile_id=configuration_profile_id,
            configuration_version=configuration_version,
            deployment_strategy_id=deployment_strategy_id,
            environment_id=environment_id,
            description=description,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01ebc720888f69e802f8006a8e194bbaab52fd7d29aaaad1fe569c110bfb49a9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf93d3aa0dae4949ede1cfc17d4734e2aabe9568d46040f918ba257b9b666640)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The application ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f163064b8e69de45a38c3e758c285bd030d58ebcf44412a0b5a0eb20ef15af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="configurationProfileId")
    def configuration_profile_id(self) -> builtins.str:
        '''The configuration profile ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-configurationprofileid
        '''
        return typing.cast(builtins.str, jsii.get(self, "configurationProfileId"))

    @configuration_profile_id.setter
    def configuration_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__890c0c0edc41cda6e989b94415c3b6f7facfd4d4c981c9094b48d3e05c35d82c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="configurationVersion")
    def configuration_version(self) -> builtins.str:
        '''The configuration version to deploy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-configurationversion
        '''
        return typing.cast(builtins.str, jsii.get(self, "configurationVersion"))

    @configuration_version.setter
    def configuration_version(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d044d5d42f276984b46b365607ce058c56d47478e79cd981c409e0e44226840)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationVersion", value)

    @builtins.property
    @jsii.member(jsii_name="deploymentStrategyId")
    def deployment_strategy_id(self) -> builtins.str:
        '''The deployment strategy ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-deploymentstrategyid
        '''
        return typing.cast(builtins.str, jsii.get(self, "deploymentStrategyId"))

    @deployment_strategy_id.setter
    def deployment_strategy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b035266d2353f73984b59d02f3a01a21621186071ba68921f2e95521aef39f3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentStrategyId", value)

    @builtins.property
    @jsii.member(jsii_name="environmentId")
    def environment_id(self) -> builtins.str:
        '''The environment ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-environmentid
        '''
        return typing.cast(builtins.str, jsii.get(self, "environmentId"))

    @environment_id.setter
    def environment_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8eb3d80e11429b543ddccbae034fa996842840dc4b5e1edfb886b0aee8c6ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the deployment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83e06eec9ab8783bad7282b3a0b8ed548ac168d6c67eb0be8f85b373cb32681c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["CfnDeployment.TagsProperty"]]:
        '''Metadata to assign to the deployment.

        Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-tags
        '''
        return typing.cast(typing.Optional[typing.List["CfnDeployment.TagsProperty"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["CfnDeployment.TagsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a92c52a739ce418ade74ef8a53bc13eed4b0c5163f06e1520d7c770961a1e04f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appconfig.CfnDeployment.TagsProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Metadata to assign to the deployment strategy.

            Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.

            :param key: The key-value string map. The valid character set is ``[a-zA-Z+-=._:/]`` . The tag key can be up to 128 characters and must not start with ``aws:`` .
            :param value: The tag value can be up to 256 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-deployment-tags.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appconfig as appconfig
                
                tags_property = appconfig.CfnDeployment.TagsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f039a35888b449375bbb33de09f04b0d89771125367147dd85b1ff70bcd6c560)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key-value string map.

            The valid character set is ``[a-zA-Z+-=._:/]`` . The tag key can be up to 128 characters and must not start with ``aws:`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-deployment-tags.html#cfn-appconfig-deployment-tags-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The tag value can be up to 256 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-deployment-tags.html#cfn-appconfig-deployment-tags-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appconfig.CfnDeploymentProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "configuration_profile_id": "configurationProfileId",
        "configuration_version": "configurationVersion",
        "deployment_strategy_id": "deploymentStrategyId",
        "environment_id": "environmentId",
        "description": "description",
        "tags": "tags",
    },
)
class CfnDeploymentProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        configuration_profile_id: builtins.str,
        configuration_version: builtins.str,
        deployment_strategy_id: builtins.str,
        environment_id: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[CfnDeployment.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDeployment``.

        :param application_id: The application ID.
        :param configuration_profile_id: The configuration profile ID.
        :param configuration_version: The configuration version to deploy.
        :param deployment_strategy_id: The deployment strategy ID.
        :param environment_id: The environment ID.
        :param description: A description of the deployment.
        :param tags: Metadata to assign to the deployment. Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appconfig as appconfig
            
            cfn_deployment_props = appconfig.CfnDeploymentProps(
                application_id="applicationId",
                configuration_profile_id="configurationProfileId",
                configuration_version="configurationVersion",
                deployment_strategy_id="deploymentStrategyId",
                environment_id="environmentId",
            
                # the properties below are optional
                description="description",
                tags=[appconfig.CfnDeployment.TagsProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd989d75d91d791c870ffcfda42d84192270e9f375c5481f70ba1849f04e2c85)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument configuration_profile_id", value=configuration_profile_id, expected_type=type_hints["configuration_profile_id"])
            check_type(argname="argument configuration_version", value=configuration_version, expected_type=type_hints["configuration_version"])
            check_type(argname="argument deployment_strategy_id", value=deployment_strategy_id, expected_type=type_hints["deployment_strategy_id"])
            check_type(argname="argument environment_id", value=environment_id, expected_type=type_hints["environment_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "configuration_profile_id": configuration_profile_id,
            "configuration_version": configuration_version,
            "deployment_strategy_id": deployment_strategy_id,
            "environment_id": environment_id,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The application ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration_profile_id(self) -> builtins.str:
        '''The configuration profile ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-configurationprofileid
        '''
        result = self._values.get("configuration_profile_id")
        assert result is not None, "Required property 'configuration_profile_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration_version(self) -> builtins.str:
        '''The configuration version to deploy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-configurationversion
        '''
        result = self._values.get("configuration_version")
        assert result is not None, "Required property 'configuration_version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def deployment_strategy_id(self) -> builtins.str:
        '''The deployment strategy ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-deploymentstrategyid
        '''
        result = self._values.get("deployment_strategy_id")
        assert result is not None, "Required property 'deployment_strategy_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def environment_id(self) -> builtins.str:
        '''The environment ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-environmentid
        '''
        result = self._values.get("environment_id")
        assert result is not None, "Required property 'environment_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the deployment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[CfnDeployment.TagsProperty]]:
        '''Metadata to assign to the deployment.

        Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deployment.html#cfn-appconfig-deployment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[CfnDeployment.TagsProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDeploymentStrategy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appconfig.CfnDeploymentStrategy",
):
    '''A CloudFormation ``AWS::AppConfig::DeploymentStrategy``.

    The ``AWS::AppConfig::DeploymentStrategy`` resource creates an AWS AppConfig deployment strategy. A deployment strategy defines important criteria for rolling out your configuration to the designated targets. A deployment strategy includes: the overall duration required, a percentage of targets to receive the deployment during each interval, an algorithm that defines how percentage grows, and bake time.

    AWS AppConfig requires that you create resources and deploy a configuration in the following order:

    - Create an application
    - Create an environment
    - Create a configuration profile
    - Create a deployment strategy
    - Deploy the configuration

    For more information, see `AWS AppConfig <https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html>`_ in the *AWS AppConfig User Guide* .

    :cloudformationResource: AWS::AppConfig::DeploymentStrategy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appconfig as appconfig
        
        cfn_deployment_strategy = appconfig.CfnDeploymentStrategy(self, "MyCfnDeploymentStrategy",
            deployment_duration_in_minutes=123,
            growth_factor=123,
            name="name",
            replicate_to="replicateTo",
        
            # the properties below are optional
            description="description",
            final_bake_time_in_minutes=123,
            growth_type="growthType",
            tags=[appconfig.CfnDeploymentStrategy.TagsProperty(
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
        deployment_duration_in_minutes: jsii.Number,
        growth_factor: jsii.Number,
        name: builtins.str,
        replicate_to: builtins.str,
        description: typing.Optional[builtins.str] = None,
        final_bake_time_in_minutes: typing.Optional[jsii.Number] = None,
        growth_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnDeploymentStrategy.TagsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AppConfig::DeploymentStrategy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param deployment_duration_in_minutes: Total amount of time for a deployment to last.
        :param growth_factor: The percentage of targets to receive a deployed configuration during each interval.
        :param name: A name for the deployment strategy.
        :param replicate_to: Save the deployment strategy to a Systems Manager (SSM) document.
        :param description: A description of the deployment strategy.
        :param final_bake_time_in_minutes: Specifies the amount of time AWS AppConfig monitors for Amazon CloudWatch alarms after the configuration has been deployed to 100% of its targets, before considering the deployment to be complete. If an alarm is triggered during this time, AWS AppConfig rolls back the deployment. You must configure permissions for AWS AppConfig to roll back based on CloudWatch alarms. For more information, see `Configuring permissions for rollback based on Amazon CloudWatch alarms <https://docs.aws.amazon.com/appconfig/latest/userguide/getting-started-with-appconfig-cloudwatch-alarms-permissions.html>`_ in the *AWS AppConfig User Guide* .
        :param growth_type: The algorithm used to define how percentage grows over time. AWS AppConfig supports the following growth types:. *Linear* : For this type, AWS AppConfig processes the deployment by dividing the total number of targets by the value specified for ``Step percentage`` . For example, a linear deployment that uses a ``Step percentage`` of 10 deploys the configuration to 10 percent of the hosts. After those deployments are complete, the system deploys the configuration to the next 10 percent. This continues until 100% of the targets have successfully received the configuration. *Exponential* : For this type, AWS AppConfig processes the deployment exponentially using the following formula: ``G*(2^N)`` . In this formula, ``G`` is the growth factor specified by the user and ``N`` is the number of steps until the configuration is deployed to all targets. For example, if you specify a growth factor of 2, then the system rolls out the configuration as follows: ``2*(2^0)`` ``2*(2^1)`` ``2*(2^2)`` Expressed numerically, the deployment rolls out as follows: 2% of the targets, 4% of the targets, 8% of the targets, and continues until the configuration has been deployed to all targets.
        :param tags: Assigns metadata to an AWS AppConfig resource. Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define. You can specify a maximum of 50 tags for a resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__481342cd0fdd96ab41cc7b15fa403873d1183a0b11928f43ac67f414808f47b5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDeploymentStrategyProps(
            deployment_duration_in_minutes=deployment_duration_in_minutes,
            growth_factor=growth_factor,
            name=name,
            replicate_to=replicate_to,
            description=description,
            final_bake_time_in_minutes=final_bake_time_in_minutes,
            growth_type=growth_type,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0092b855e91c4ddae7907da4470c73a11dbdadfb9eb5571515ed0ba8d2239e0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__13951255808e5d20c9e446bfa6adbcbee9a243c8b87e62e53b3216bb458bcc1a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="deploymentDurationInMinutes")
    def deployment_duration_in_minutes(self) -> jsii.Number:
        '''Total amount of time for a deployment to last.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-deploymentdurationinminutes
        '''
        return typing.cast(jsii.Number, jsii.get(self, "deploymentDurationInMinutes"))

    @deployment_duration_in_minutes.setter
    def deployment_duration_in_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce31284d0d46c4c03baf948fbc5d9f4a398546e2f87738e55f48fbf3162d3220)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deploymentDurationInMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="growthFactor")
    def growth_factor(self) -> jsii.Number:
        '''The percentage of targets to receive a deployed configuration during each interval.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-growthfactor
        '''
        return typing.cast(jsii.Number, jsii.get(self, "growthFactor"))

    @growth_factor.setter
    def growth_factor(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7aaf39038cddf436fe3343d85881d882a0243cf8a5e6e3cfa6d29f081c8fc50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "growthFactor", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A name for the deployment strategy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a4e5d179df7235725bc5fc078fe3ab54d0da987816894a23953fd121a19a8496)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="replicateTo")
    def replicate_to(self) -> builtins.str:
        '''Save the deployment strategy to a Systems Manager (SSM) document.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-replicateto
        '''
        return typing.cast(builtins.str, jsii.get(self, "replicateTo"))

    @replicate_to.setter
    def replicate_to(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c16dc0767220e0dee71818c7ce4a4b708d1dab4af1bab9d185e7276f50883fae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "replicateTo", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the deployment strategy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__099668ee724a39f3667b1f19d2cc3330693512f5f19e4244f7ac57d6cdf3f438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="finalBakeTimeInMinutes")
    def final_bake_time_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Specifies the amount of time AWS AppConfig monitors for Amazon CloudWatch alarms after the configuration has been deployed to 100% of its targets, before considering the deployment to be complete.

        If an alarm is triggered during this time, AWS AppConfig rolls back the deployment. You must configure permissions for AWS AppConfig to roll back based on CloudWatch alarms. For more information, see `Configuring permissions for rollback based on Amazon CloudWatch alarms <https://docs.aws.amazon.com/appconfig/latest/userguide/getting-started-with-appconfig-cloudwatch-alarms-permissions.html>`_ in the *AWS AppConfig User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-finalbaketimeinminutes
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "finalBakeTimeInMinutes"))

    @final_bake_time_in_minutes.setter
    def final_bake_time_in_minutes(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21f359c44b99ce7aee090ddfc047d6cfb51b962ed3f40c1357315f23166ec231)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "finalBakeTimeInMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="growthType")
    def growth_type(self) -> typing.Optional[builtins.str]:
        '''The algorithm used to define how percentage grows over time. AWS AppConfig supports the following growth types:.

        *Linear* : For this type, AWS AppConfig processes the deployment by dividing the total number of targets by the value specified for ``Step percentage`` . For example, a linear deployment that uses a ``Step percentage`` of 10 deploys the configuration to 10 percent of the hosts. After those deployments are complete, the system deploys the configuration to the next 10 percent. This continues until 100% of the targets have successfully received the configuration.

        *Exponential* : For this type, AWS AppConfig processes the deployment exponentially using the following formula: ``G*(2^N)`` . In this formula, ``G`` is the growth factor specified by the user and ``N`` is the number of steps until the configuration is deployed to all targets. For example, if you specify a growth factor of 2, then the system rolls out the configuration as follows:

        ``2*(2^0)``

        ``2*(2^1)``

        ``2*(2^2)``

        Expressed numerically, the deployment rolls out as follows: 2% of the targets, 4% of the targets, 8% of the targets, and continues until the configuration has been deployed to all targets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-growthtype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "growthType"))

    @growth_type.setter
    def growth_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b669863584816c4889434ed8e9a692c10794b35ebab75af4cab3946eae97d5b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "growthType", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(
        self,
    ) -> typing.Optional[typing.List["CfnDeploymentStrategy.TagsProperty"]]:
        '''Assigns metadata to an AWS AppConfig resource.

        Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define. You can specify a maximum of 50 tags for a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-tags
        '''
        return typing.cast(typing.Optional[typing.List["CfnDeploymentStrategy.TagsProperty"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["CfnDeploymentStrategy.TagsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebc480a83e8366a4ecd36d27e46ea7bc61602571aabf04f84e626bf52d484dce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appconfig.CfnDeploymentStrategy.TagsProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Metadata to assign to the deployment strategy.

            Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.

            :param key: The key-value string map. The valid character set is ``[a-zA-Z+-=._:/]`` . The tag key can be up to 128 characters and must not start with ``aws:`` .
            :param value: The tag value can be up to 256 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-deploymentstrategy-tags.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appconfig as appconfig
                
                tags_property = appconfig.CfnDeploymentStrategy.TagsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b63d0f4461ddf0a02e4819c483ee6a81c1f0bac7b62b29653d5fdd1defddb9dd)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key-value string map.

            The valid character set is ``[a-zA-Z+-=._:/]`` . The tag key can be up to 128 characters and must not start with ``aws:`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-deploymentstrategy-tags.html#cfn-appconfig-deploymentstrategy-tags-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The tag value can be up to 256 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-deploymentstrategy-tags.html#cfn-appconfig-deploymentstrategy-tags-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appconfig.CfnDeploymentStrategyProps",
    jsii_struct_bases=[],
    name_mapping={
        "deployment_duration_in_minutes": "deploymentDurationInMinutes",
        "growth_factor": "growthFactor",
        "name": "name",
        "replicate_to": "replicateTo",
        "description": "description",
        "final_bake_time_in_minutes": "finalBakeTimeInMinutes",
        "growth_type": "growthType",
        "tags": "tags",
    },
)
class CfnDeploymentStrategyProps:
    def __init__(
        self,
        *,
        deployment_duration_in_minutes: jsii.Number,
        growth_factor: jsii.Number,
        name: builtins.str,
        replicate_to: builtins.str,
        description: typing.Optional[builtins.str] = None,
        final_bake_time_in_minutes: typing.Optional[jsii.Number] = None,
        growth_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[CfnDeploymentStrategy.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDeploymentStrategy``.

        :param deployment_duration_in_minutes: Total amount of time for a deployment to last.
        :param growth_factor: The percentage of targets to receive a deployed configuration during each interval.
        :param name: A name for the deployment strategy.
        :param replicate_to: Save the deployment strategy to a Systems Manager (SSM) document.
        :param description: A description of the deployment strategy.
        :param final_bake_time_in_minutes: Specifies the amount of time AWS AppConfig monitors for Amazon CloudWatch alarms after the configuration has been deployed to 100% of its targets, before considering the deployment to be complete. If an alarm is triggered during this time, AWS AppConfig rolls back the deployment. You must configure permissions for AWS AppConfig to roll back based on CloudWatch alarms. For more information, see `Configuring permissions for rollback based on Amazon CloudWatch alarms <https://docs.aws.amazon.com/appconfig/latest/userguide/getting-started-with-appconfig-cloudwatch-alarms-permissions.html>`_ in the *AWS AppConfig User Guide* .
        :param growth_type: The algorithm used to define how percentage grows over time. AWS AppConfig supports the following growth types:. *Linear* : For this type, AWS AppConfig processes the deployment by dividing the total number of targets by the value specified for ``Step percentage`` . For example, a linear deployment that uses a ``Step percentage`` of 10 deploys the configuration to 10 percent of the hosts. After those deployments are complete, the system deploys the configuration to the next 10 percent. This continues until 100% of the targets have successfully received the configuration. *Exponential* : For this type, AWS AppConfig processes the deployment exponentially using the following formula: ``G*(2^N)`` . In this formula, ``G`` is the growth factor specified by the user and ``N`` is the number of steps until the configuration is deployed to all targets. For example, if you specify a growth factor of 2, then the system rolls out the configuration as follows: ``2*(2^0)`` ``2*(2^1)`` ``2*(2^2)`` Expressed numerically, the deployment rolls out as follows: 2% of the targets, 4% of the targets, 8% of the targets, and continues until the configuration has been deployed to all targets.
        :param tags: Assigns metadata to an AWS AppConfig resource. Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define. You can specify a maximum of 50 tags for a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appconfig as appconfig
            
            cfn_deployment_strategy_props = appconfig.CfnDeploymentStrategyProps(
                deployment_duration_in_minutes=123,
                growth_factor=123,
                name="name",
                replicate_to="replicateTo",
            
                # the properties below are optional
                description="description",
                final_bake_time_in_minutes=123,
                growth_type="growthType",
                tags=[appconfig.CfnDeploymentStrategy.TagsProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5502d1d82b937060c2b1b8f821c60e2a0fe96416a40e73ee0d4d122add8add8)
            check_type(argname="argument deployment_duration_in_minutes", value=deployment_duration_in_minutes, expected_type=type_hints["deployment_duration_in_minutes"])
            check_type(argname="argument growth_factor", value=growth_factor, expected_type=type_hints["growth_factor"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument replicate_to", value=replicate_to, expected_type=type_hints["replicate_to"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument final_bake_time_in_minutes", value=final_bake_time_in_minutes, expected_type=type_hints["final_bake_time_in_minutes"])
            check_type(argname="argument growth_type", value=growth_type, expected_type=type_hints["growth_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "deployment_duration_in_minutes": deployment_duration_in_minutes,
            "growth_factor": growth_factor,
            "name": name,
            "replicate_to": replicate_to,
        }
        if description is not None:
            self._values["description"] = description
        if final_bake_time_in_minutes is not None:
            self._values["final_bake_time_in_minutes"] = final_bake_time_in_minutes
        if growth_type is not None:
            self._values["growth_type"] = growth_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def deployment_duration_in_minutes(self) -> jsii.Number:
        '''Total amount of time for a deployment to last.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-deploymentdurationinminutes
        '''
        result = self._values.get("deployment_duration_in_minutes")
        assert result is not None, "Required property 'deployment_duration_in_minutes' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def growth_factor(self) -> jsii.Number:
        '''The percentage of targets to receive a deployed configuration during each interval.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-growthfactor
        '''
        result = self._values.get("growth_factor")
        assert result is not None, "Required property 'growth_factor' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A name for the deployment strategy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def replicate_to(self) -> builtins.str:
        '''Save the deployment strategy to a Systems Manager (SSM) document.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-replicateto
        '''
        result = self._values.get("replicate_to")
        assert result is not None, "Required property 'replicate_to' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the deployment strategy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def final_bake_time_in_minutes(self) -> typing.Optional[jsii.Number]:
        '''Specifies the amount of time AWS AppConfig monitors for Amazon CloudWatch alarms after the configuration has been deployed to 100% of its targets, before considering the deployment to be complete.

        If an alarm is triggered during this time, AWS AppConfig rolls back the deployment. You must configure permissions for AWS AppConfig to roll back based on CloudWatch alarms. For more information, see `Configuring permissions for rollback based on Amazon CloudWatch alarms <https://docs.aws.amazon.com/appconfig/latest/userguide/getting-started-with-appconfig-cloudwatch-alarms-permissions.html>`_ in the *AWS AppConfig User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-finalbaketimeinminutes
        '''
        result = self._values.get("final_bake_time_in_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def growth_type(self) -> typing.Optional[builtins.str]:
        '''The algorithm used to define how percentage grows over time. AWS AppConfig supports the following growth types:.

        *Linear* : For this type, AWS AppConfig processes the deployment by dividing the total number of targets by the value specified for ``Step percentage`` . For example, a linear deployment that uses a ``Step percentage`` of 10 deploys the configuration to 10 percent of the hosts. After those deployments are complete, the system deploys the configuration to the next 10 percent. This continues until 100% of the targets have successfully received the configuration.

        *Exponential* : For this type, AWS AppConfig processes the deployment exponentially using the following formula: ``G*(2^N)`` . In this formula, ``G`` is the growth factor specified by the user and ``N`` is the number of steps until the configuration is deployed to all targets. For example, if you specify a growth factor of 2, then the system rolls out the configuration as follows:

        ``2*(2^0)``

        ``2*(2^1)``

        ``2*(2^2)``

        Expressed numerically, the deployment rolls out as follows: 2% of the targets, 4% of the targets, 8% of the targets, and continues until the configuration has been deployed to all targets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-growthtype
        '''
        result = self._values.get("growth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[CfnDeploymentStrategy.TagsProperty]]:
        '''Assigns metadata to an AWS AppConfig resource.

        Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define. You can specify a maximum of 50 tags for a resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-deploymentstrategy.html#cfn-appconfig-deploymentstrategy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[CfnDeploymentStrategy.TagsProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDeploymentStrategyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnEnvironment(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appconfig.CfnEnvironment",
):
    '''A CloudFormation ``AWS::AppConfig::Environment``.

    The ``AWS::AppConfig::Environment`` resource creates an environment, which is a logical deployment group of AWS AppConfig targets, such as applications in a ``Beta`` or ``Production`` environment. You define one or more environments for each AWS AppConfig application. You can also define environments for application subcomponents such as the ``Web`` , ``Mobile`` and ``Back-end`` components for your application. You can configure Amazon CloudWatch alarms for each environment. The system monitors alarms during a configuration deployment. If an alarm is triggered, the system rolls back the configuration.

    AWS AppConfig requires that you create resources and deploy a configuration in the following order:

    - Create an application
    - Create an environment
    - Create a configuration profile
    - Create a deployment strategy
    - Deploy the configuration

    For more information, see `AWS AppConfig <https://docs.aws.amazon.com/appconfig/latest/userguide/what-is-appconfig.html>`_ in the *AWS AppConfig User Guide* .

    :cloudformationResource: AWS::AppConfig::Environment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appconfig as appconfig
        
        cfn_environment = appconfig.CfnEnvironment(self, "MyCfnEnvironment",
            application_id="applicationId",
            name="name",
        
            # the properties below are optional
            description="description",
            monitors=[appconfig.CfnEnvironment.MonitorsProperty(
                alarm_arn="alarmArn",
                alarm_role_arn="alarmRoleArn"
            )],
            tags=[appconfig.CfnEnvironment.TagsProperty(
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
        application_id: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        monitors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnEnvironment.MonitorsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnEnvironment.TagsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AppConfig::Environment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The application ID.
        :param name: A name for the environment.
        :param description: A description of the environment.
        :param monitors: Amazon CloudWatch alarms to monitor during the deployment process.
        :param tags: Metadata to assign to the environment. Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864c2bddbc293a433378c74cd54a1a6ab427a065e6cd0b0280605a2e7e78da4b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEnvironmentProps(
            application_id=application_id,
            name=name,
            description=description,
            monitors=monitors,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e0403ffeace3aff9769f2e6c7a1cdf87e7c425111984de85b3e84197db2f55e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fe2ba4cef80df5f7040fcb2b47e15339b41bd61e3b9e6ddb5cb3eb5be1320f3)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The application ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cea3509a2679257e18607b6f0f646a11a0801d2053196db0d357c01a0a9194d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''A name for the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99b319e463255d9a2657d956bf13a70be88dc381a59de8b6ac8adc62160c7c76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cc971780b1b9efac6dd9f816c704355b86ec94586e685aea2b0625048a10f59)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="monitors")
    def monitors(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEnvironment.MonitorsProperty", _IResolvable_a771d0ef]]]]:
        '''Amazon CloudWatch alarms to monitor during the deployment process.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-monitors
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEnvironment.MonitorsProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "monitors"))

    @monitors.setter
    def monitors(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnEnvironment.MonitorsProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__83431470ec5c8b7f3c80de0eeea68e469b477d7be18b48d981a0edc8d4415b7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "monitors", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["CfnEnvironment.TagsProperty"]]:
        '''Metadata to assign to the environment.

        Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-tags
        '''
        return typing.cast(typing.Optional[typing.List["CfnEnvironment.TagsProperty"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["CfnEnvironment.TagsProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2593e8f8e1f6c35c2f5f9f79cee88b9ff5283441da640eca26919e6b4dafae97)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_appconfig.CfnEnvironment.MonitorsProperty",
        jsii_struct_bases=[],
        name_mapping={"alarm_arn": "alarmArn", "alarm_role_arn": "alarmRoleArn"},
    )
    class MonitorsProperty:
        def __init__(
            self,
            *,
            alarm_arn: typing.Optional[builtins.str] = None,
            alarm_role_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Amazon CloudWatch alarms to monitor during the deployment process.

            :param alarm_arn: Amazon Resource Name (ARN) of the Amazon CloudWatch alarm.
            :param alarm_role_arn: ARN of an AWS Identity and Access Management (IAM) role for AWS AppConfig to monitor ``AlarmArn`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-environment-monitors.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appconfig as appconfig
                
                monitors_property = appconfig.CfnEnvironment.MonitorsProperty(
                    alarm_arn="alarmArn",
                    alarm_role_arn="alarmRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d7923830b26a4b7a1e332348e231a99c4090ea0f636cd2bcf5f2e60a467fe05a)
                check_type(argname="argument alarm_arn", value=alarm_arn, expected_type=type_hints["alarm_arn"])
                check_type(argname="argument alarm_role_arn", value=alarm_role_arn, expected_type=type_hints["alarm_role_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if alarm_arn is not None:
                self._values["alarm_arn"] = alarm_arn
            if alarm_role_arn is not None:
                self._values["alarm_role_arn"] = alarm_role_arn

        @builtins.property
        def alarm_arn(self) -> typing.Optional[builtins.str]:
            '''Amazon Resource Name (ARN) of the Amazon CloudWatch alarm.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-environment-monitors.html#cfn-appconfig-environment-monitors-alarmarn
            '''
            result = self._values.get("alarm_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def alarm_role_arn(self) -> typing.Optional[builtins.str]:
            '''ARN of an AWS Identity and Access Management (IAM) role for AWS AppConfig to monitor ``AlarmArn`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-environment-monitors.html#cfn-appconfig-environment-monitors-alarmrolearn
            '''
            result = self._values.get("alarm_role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MonitorsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_appconfig.CfnEnvironment.TagsProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class TagsProperty:
        def __init__(
            self,
            *,
            key: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Metadata to assign to the environment.

            Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.

            :param key: The key-value string map. The valid character set is ``[a-zA-Z+-=._:/]`` . The tag key can be up to 128 characters and must not start with ``aws:`` .
            :param value: The tag value can be up to 256 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-environment-tags.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_appconfig as appconfig
                
                tags_property = appconfig.CfnEnvironment.TagsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__49d546d90a21e6f46a3a0c36c429a4285157028ca89d90333b6e71620e25bca6)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if key is not None:
                self._values["key"] = key
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> typing.Optional[builtins.str]:
            '''The key-value string map.

            The valid character set is ``[a-zA-Z+-=._:/]`` . The tag key can be up to 128 characters and must not start with ``aws:`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-environment-tags.html#cfn-appconfig-environment-tags-key
            '''
            result = self._values.get("key")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The tag value can be up to 256 characters.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appconfig-environment-tags.html#cfn-appconfig-environment-tags-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TagsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_appconfig.CfnEnvironmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "name": "name",
        "description": "description",
        "monitors": "monitors",
        "tags": "tags",
    },
)
class CfnEnvironmentProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        monitors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEnvironment.MonitorsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[CfnEnvironment.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnEnvironment``.

        :param application_id: The application ID.
        :param name: A name for the environment.
        :param description: A description of the environment.
        :param monitors: Amazon CloudWatch alarms to monitor during the deployment process.
        :param tags: Metadata to assign to the environment. Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appconfig as appconfig
            
            cfn_environment_props = appconfig.CfnEnvironmentProps(
                application_id="applicationId",
                name="name",
            
                # the properties below are optional
                description="description",
                monitors=[appconfig.CfnEnvironment.MonitorsProperty(
                    alarm_arn="alarmArn",
                    alarm_role_arn="alarmRoleArn"
                )],
                tags=[appconfig.CfnEnvironment.TagsProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5116c1197508af7e67777489ba9ef158fbc2d9e5cea3f76bc306f96aaf204141)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument monitors", value=monitors, expected_type=type_hints["monitors"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "name": name,
        }
        if description is not None:
            self._values["description"] = description
        if monitors is not None:
            self._values["monitors"] = monitors
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The application ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''A name for the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def monitors(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnEnvironment.MonitorsProperty, _IResolvable_a771d0ef]]]]:
        '''Amazon CloudWatch alarms to monitor during the deployment process.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-monitors
        '''
        result = self._values.get("monitors")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnEnvironment.MonitorsProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[CfnEnvironment.TagsProperty]]:
        '''Metadata to assign to the environment.

        Tags help organize and categorize your AWS AppConfig resources. Each tag consists of a key and an optional value, both of which you define.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[CfnEnvironment.TagsProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnEnvironmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnHostedConfigurationVersion(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_appconfig.CfnHostedConfigurationVersion",
):
    '''A CloudFormation ``AWS::AppConfig::HostedConfigurationVersion``.

    Create a new configuration in the AWS AppConfig hosted configuration store. Configurations must be 1 MB or smaller. The AWS AppConfig hosted configuration store provides the following benefits over other configuration store options.

    - You don't need to set up and configure other services such as Amazon Simple Storage Service ( Amazon S3 ) or Parameter Store.
    - You don't need to configure AWS Identity and Access Management ( IAM ) permissions to use the configuration store.
    - You can store configurations in any content type.
    - There is no cost to use the store.
    - You can create a configuration and add it to the store when you create a configuration profile.

    :cloudformationResource: AWS::AppConfig::HostedConfigurationVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_appconfig as appconfig
        
        cfn_hosted_configuration_version = appconfig.CfnHostedConfigurationVersion(self, "MyCfnHostedConfigurationVersion",
            application_id="applicationId",
            configuration_profile_id="configurationProfileId",
            content="content",
            content_type="contentType",
        
            # the properties below are optional
            description="description",
            latest_version_number=123
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        application_id: builtins.str,
        configuration_profile_id: builtins.str,
        content: builtins.str,
        content_type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        latest_version_number: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Create a new ``AWS::AppConfig::HostedConfigurationVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_id: The application ID.
        :param configuration_profile_id: The configuration profile ID.
        :param content: The content of the configuration or the configuration data.
        :param content_type: A standard MIME type describing the format of the configuration content. For more information, see `Content-Type <https://docs.aws.amazon.com/https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.17>`_ .
        :param description: A description of the configuration.
        :param latest_version_number: An optional locking token used to prevent race conditions from overwriting configuration updates when creating a new version. To ensure your data is not overwritten when creating multiple hosted configuration versions in rapid succession, specify the version number of the latest hosted configuration version.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0df6089986800d562d6876d1be6e668a29301e83691eb5d6ebebd8f1366558dc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnHostedConfigurationVersionProps(
            application_id=application_id,
            configuration_profile_id=configuration_profile_id,
            content=content,
            content_type=content_type,
            description=description,
            latest_version_number=latest_version_number,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__021c728ec8bbecc13c184579c41a3cb265d61d1a2a7d7eac3d4b33803b82bd88)
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
            type_hints = typing.get_type_hints(_typecheckingstub__afb149dc0b6baa057b512d9a9b80ba809b205a82c0f8ff587b185a4773e20587)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> builtins.str:
        '''The application ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-applicationid
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationId"))

    @application_id.setter
    def application_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c92f7b412f3a9be986e1f1999552eb7bb59e28b2312509693bbaed5aa453486)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationId", value)

    @builtins.property
    @jsii.member(jsii_name="configurationProfileId")
    def configuration_profile_id(self) -> builtins.str:
        '''The configuration profile ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-configurationprofileid
        '''
        return typing.cast(builtins.str, jsii.get(self, "configurationProfileId"))

    @configuration_profile_id.setter
    def configuration_profile_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__676e12cd568a1bba282320dc19ee37d4be09b1e68ff31da64b3177ec82619311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "configurationProfileId", value)

    @builtins.property
    @jsii.member(jsii_name="content")
    def content(self) -> builtins.str:
        '''The content of the configuration or the configuration data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-content
        '''
        return typing.cast(builtins.str, jsii.get(self, "content"))

    @content.setter
    def content(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c360368ff08caf029ce8730d921459be1efb29fe61302510e0a47f052da7cf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "content", value)

    @builtins.property
    @jsii.member(jsii_name="contentType")
    def content_type(self) -> builtins.str:
        '''A standard MIME type describing the format of the configuration content.

        For more information, see `Content-Type <https://docs.aws.amazon.com/https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.17>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-contenttype
        '''
        return typing.cast(builtins.str, jsii.get(self, "contentType"))

    @content_type.setter
    def content_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cb7351c982af53a8828e89a99a50e2da6e1a160f9948c449c01bfb6fc55c5a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "contentType", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__609f6cac53b898116f24dff0db10cf4781f27a2a1e9cf580acabd257fe3c2d14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="latestVersionNumber")
    def latest_version_number(self) -> typing.Optional[jsii.Number]:
        '''An optional locking token used to prevent race conditions from overwriting configuration updates when creating a new version.

        To ensure your data is not overwritten when creating multiple hosted configuration versions in rapid succession, specify the version number of the latest hosted configuration version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-latestversionnumber
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "latestVersionNumber"))

    @latest_version_number.setter
    def latest_version_number(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08cbdac0b541747772353bb13ae899234788e2f1ad36ac75d19cf338b68a4f7b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "latestVersionNumber", value)


@jsii.data_type(
    jsii_type="monocdk.aws_appconfig.CfnHostedConfigurationVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_id": "applicationId",
        "configuration_profile_id": "configurationProfileId",
        "content": "content",
        "content_type": "contentType",
        "description": "description",
        "latest_version_number": "latestVersionNumber",
    },
)
class CfnHostedConfigurationVersionProps:
    def __init__(
        self,
        *,
        application_id: builtins.str,
        configuration_profile_id: builtins.str,
        content: builtins.str,
        content_type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        latest_version_number: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''Properties for defining a ``CfnHostedConfigurationVersion``.

        :param application_id: The application ID.
        :param configuration_profile_id: The configuration profile ID.
        :param content: The content of the configuration or the configuration data.
        :param content_type: A standard MIME type describing the format of the configuration content. For more information, see `Content-Type <https://docs.aws.amazon.com/https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.17>`_ .
        :param description: A description of the configuration.
        :param latest_version_number: An optional locking token used to prevent race conditions from overwriting configuration updates when creating a new version. To ensure your data is not overwritten when creating multiple hosted configuration versions in rapid succession, specify the version number of the latest hosted configuration version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_appconfig as appconfig
            
            cfn_hosted_configuration_version_props = appconfig.CfnHostedConfigurationVersionProps(
                application_id="applicationId",
                configuration_profile_id="configurationProfileId",
                content="content",
                content_type="contentType",
            
                # the properties below are optional
                description="description",
                latest_version_number=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31eca4d11e7b875208e7a7a94ade240d901543683a50879963d311884b144e86)
            check_type(argname="argument application_id", value=application_id, expected_type=type_hints["application_id"])
            check_type(argname="argument configuration_profile_id", value=configuration_profile_id, expected_type=type_hints["configuration_profile_id"])
            check_type(argname="argument content", value=content, expected_type=type_hints["content"])
            check_type(argname="argument content_type", value=content_type, expected_type=type_hints["content_type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument latest_version_number", value=latest_version_number, expected_type=type_hints["latest_version_number"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_id": application_id,
            "configuration_profile_id": configuration_profile_id,
            "content": content,
            "content_type": content_type,
        }
        if description is not None:
            self._values["description"] = description
        if latest_version_number is not None:
            self._values["latest_version_number"] = latest_version_number

    @builtins.property
    def application_id(self) -> builtins.str:
        '''The application ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-applicationid
        '''
        result = self._values.get("application_id")
        assert result is not None, "Required property 'application_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def configuration_profile_id(self) -> builtins.str:
        '''The configuration profile ID.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-configurationprofileid
        '''
        result = self._values.get("configuration_profile_id")
        assert result is not None, "Required property 'configuration_profile_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content(self) -> builtins.str:
        '''The content of the configuration or the configuration data.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-content
        '''
        result = self._values.get("content")
        assert result is not None, "Required property 'content' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def content_type(self) -> builtins.str:
        '''A standard MIME type describing the format of the configuration content.

        For more information, see `Content-Type <https://docs.aws.amazon.com/https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.17>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-contenttype
        '''
        result = self._values.get("content_type")
        assert result is not None, "Required property 'content_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def latest_version_number(self) -> typing.Optional[jsii.Number]:
        '''An optional locking token used to prevent race conditions from overwriting configuration updates when creating a new version.

        To ensure your data is not overwritten when creating multiple hosted configuration versions in rapid succession, specify the version number of the latest hosted configuration version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-hostedconfigurationversion.html#cfn-appconfig-hostedconfigurationversion-latestversionnumber
        '''
        result = self._values.get("latest_version_number")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnHostedConfigurationVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnApplication",
    "CfnApplicationProps",
    "CfnConfigurationProfile",
    "CfnConfigurationProfileProps",
    "CfnDeployment",
    "CfnDeploymentProps",
    "CfnDeploymentStrategy",
    "CfnDeploymentStrategyProps",
    "CfnEnvironment",
    "CfnEnvironmentProps",
    "CfnHostedConfigurationVersion",
    "CfnHostedConfigurationVersionProps",
]

publication.publish()

def _typecheckingstub__ec152a2424059a52defce300feb837353a1ccec3c21563f8fdea009a72b89d73(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnApplication.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c9aae7cdb36122bb6c4ab8463c102a4fb2925d6974c1f59967dc03304d701ab(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa346e99720de56b7ba79900dd51f9351bb8ec09b75e2909c99e0ca83e69dd2e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db03372be65c650c74040bfa9e9373ee2f55a018d5e257613ad1d4d16ae3cba2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec31f469612e1138eedb31c77883512dd32329fda9e02f11eb836ee50cd99a41(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fae9db3331e3c5d64b3a00b60bace9e22e36c8b6f420f6963f2e98a311b164fd(
    value: typing.Optional[typing.List[CfnApplication.TagsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__960b2812ec9fe7b48b718dbac53e02a21b0beb7e275f461a29962ded820f9961(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__357c8ae80f97ad1d610c76688854f27219ad431090a0b9c8e29c1ea65dda0b66(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnApplication.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4bf602951e7752d0034cae15c7747926298a301f74acc64a6c17c88a5e4c410(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_id: builtins.str,
    location_uri: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    retrieval_role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnConfigurationProfile.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
    validators: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnConfigurationProfile.ValidatorsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b6f4977d311db9bfa16e0c5f5a3af46057e8fc1c35f6ac26f73169b8690f6ae(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c13487eeded5b42e89b931e8e4432a2654066ad862e334d1fdd83dcc4e56b9cb(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f5e76a2700709291108cc6e532f1a4393dd43f3921d8c8467968a8a63703952(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff97b168e6f301d1671c26e67d27f4af286d6d3ff4e91ed47e5701e0ae33671(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__096c5799793d92c65fdeffea02afa19ada49b599d590619302db56764d1332f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e108938c05e845d3ad88d8e000dfa8c040d95650f892739963d12d9786d48a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccac18e19ae9b4f17548d1235009136dc600a742ebc38b820f975f4992339a46(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9280488cb4ab8117a46a52344337a74a2231278ebb301fbe899d41cb842fc105(
    value: typing.Optional[typing.List[CfnConfigurationProfile.TagsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f5a28cee2b2da0f0166102ecfa3453dc5b45b225fa94b631af6ae767be8cd6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0c1807f3d918ee8c709b06715b0ca85b5cdac64bbac8602c25c8cb9b4bb38fe(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnConfigurationProfile.ValidatorsProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__284511a37056bcc175d3eee47fa90074831bfde8a7c3167aa7c088924db1290a(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92cb623060f8be207323219f2dfccd6d68490453218828390667c826cd8e0d50(
    *,
    content: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__985557944d583335f64edcaaa04451a0217dfebf6dc1a2b4cc47636249138950(
    *,
    application_id: builtins.str,
    location_uri: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    retrieval_role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnConfigurationProfile.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
    validators: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnConfigurationProfile.ValidatorsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d91590582afbfb0f4740993d3fe5611f9a1fe54d092d86ab4e585607affa20(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_id: builtins.str,
    configuration_profile_id: builtins.str,
    configuration_version: builtins.str,
    deployment_strategy_id: builtins.str,
    environment_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnDeployment.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01ebc720888f69e802f8006a8e194bbaab52fd7d29aaaad1fe569c110bfb49a9(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf93d3aa0dae4949ede1cfc17d4734e2aabe9568d46040f918ba257b9b666640(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f163064b8e69de45a38c3e758c285bd030d58ebcf44412a0b5a0eb20ef15af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__890c0c0edc41cda6e989b94415c3b6f7facfd4d4c981c9094b48d3e05c35d82c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d044d5d42f276984b46b365607ce058c56d47478e79cd981c409e0e44226840(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b035266d2353f73984b59d02f3a01a21621186071ba68921f2e95521aef39f3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8eb3d80e11429b543ddccbae034fa996842840dc4b5e1edfb886b0aee8c6ebf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83e06eec9ab8783bad7282b3a0b8ed548ac168d6c67eb0be8f85b373cb32681c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a92c52a739ce418ade74ef8a53bc13eed4b0c5163f06e1520d7c770961a1e04f(
    value: typing.Optional[typing.List[CfnDeployment.TagsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f039a35888b449375bbb33de09f04b0d89771125367147dd85b1ff70bcd6c560(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd989d75d91d791c870ffcfda42d84192270e9f375c5481f70ba1849f04e2c85(
    *,
    application_id: builtins.str,
    configuration_profile_id: builtins.str,
    configuration_version: builtins.str,
    deployment_strategy_id: builtins.str,
    environment_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnDeployment.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__481342cd0fdd96ab41cc7b15fa403873d1183a0b11928f43ac67f414808f47b5(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    deployment_duration_in_minutes: jsii.Number,
    growth_factor: jsii.Number,
    name: builtins.str,
    replicate_to: builtins.str,
    description: typing.Optional[builtins.str] = None,
    final_bake_time_in_minutes: typing.Optional[jsii.Number] = None,
    growth_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnDeploymentStrategy.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0092b855e91c4ddae7907da4470c73a11dbdadfb9eb5571515ed0ba8d2239e0(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13951255808e5d20c9e446bfa6adbcbee9a243c8b87e62e53b3216bb458bcc1a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce31284d0d46c4c03baf948fbc5d9f4a398546e2f87738e55f48fbf3162d3220(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7aaf39038cddf436fe3343d85881d882a0243cf8a5e6e3cfa6d29f081c8fc50(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4e5d179df7235725bc5fc078fe3ab54d0da987816894a23953fd121a19a8496(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c16dc0767220e0dee71818c7ce4a4b708d1dab4af1bab9d185e7276f50883fae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__099668ee724a39f3667b1f19d2cc3330693512f5f19e4244f7ac57d6cdf3f438(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21f359c44b99ce7aee090ddfc047d6cfb51b962ed3f40c1357315f23166ec231(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b669863584816c4889434ed8e9a692c10794b35ebab75af4cab3946eae97d5b6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebc480a83e8366a4ecd36d27e46ea7bc61602571aabf04f84e626bf52d484dce(
    value: typing.Optional[typing.List[CfnDeploymentStrategy.TagsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b63d0f4461ddf0a02e4819c483ee6a81c1f0bac7b62b29653d5fdd1defddb9dd(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5502d1d82b937060c2b1b8f821c60e2a0fe96416a40e73ee0d4d122add8add8(
    *,
    deployment_duration_in_minutes: jsii.Number,
    growth_factor: jsii.Number,
    name: builtins.str,
    replicate_to: builtins.str,
    description: typing.Optional[builtins.str] = None,
    final_bake_time_in_minutes: typing.Optional[jsii.Number] = None,
    growth_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnDeploymentStrategy.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864c2bddbc293a433378c74cd54a1a6ab427a065e6cd0b0280605a2e7e78da4b(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_id: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    monitors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEnvironment.MonitorsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnEnvironment.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e0403ffeace3aff9769f2e6c7a1cdf87e7c425111984de85b3e84197db2f55e(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe2ba4cef80df5f7040fcb2b47e15339b41bd61e3b9e6ddb5cb3eb5be1320f3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cea3509a2679257e18607b6f0f646a11a0801d2053196db0d357c01a0a9194d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99b319e463255d9a2657d956bf13a70be88dc381a59de8b6ac8adc62160c7c76(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cc971780b1b9efac6dd9f816c704355b86ec94586e685aea2b0625048a10f59(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83431470ec5c8b7f3c80de0eeea68e469b477d7be18b48d981a0edc8d4415b7f(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnEnvironment.MonitorsProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2593e8f8e1f6c35c2f5f9f79cee88b9ff5283441da640eca26919e6b4dafae97(
    value: typing.Optional[typing.List[CfnEnvironment.TagsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7923830b26a4b7a1e332348e231a99c4090ea0f636cd2bcf5f2e60a467fe05a(
    *,
    alarm_arn: typing.Optional[builtins.str] = None,
    alarm_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49d546d90a21e6f46a3a0c36c429a4285157028ca89d90333b6e71620e25bca6(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5116c1197508af7e67777489ba9ef158fbc2d9e5cea3f76bc306f96aaf204141(
    *,
    application_id: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    monitors: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnEnvironment.MonitorsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnEnvironment.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0df6089986800d562d6876d1be6e668a29301e83691eb5d6ebebd8f1366558dc(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    application_id: builtins.str,
    configuration_profile_id: builtins.str,
    content: builtins.str,
    content_type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    latest_version_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__021c728ec8bbecc13c184579c41a3cb265d61d1a2a7d7eac3d4b33803b82bd88(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afb149dc0b6baa057b512d9a9b80ba809b205a82c0f8ff587b185a4773e20587(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c92f7b412f3a9be986e1f1999552eb7bb59e28b2312509693bbaed5aa453486(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__676e12cd568a1bba282320dc19ee37d4be09b1e68ff31da64b3177ec82619311(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c360368ff08caf029ce8730d921459be1efb29fe61302510e0a47f052da7cf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cb7351c982af53a8828e89a99a50e2da6e1a160f9948c449c01bfb6fc55c5a0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__609f6cac53b898116f24dff0db10cf4781f27a2a1e9cf580acabd257fe3c2d14(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08cbdac0b541747772353bb13ae899234788e2f1ad36ac75d19cf338b68a4f7b(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31eca4d11e7b875208e7a7a94ade240d901543683a50879963d311884b144e86(
    *,
    application_id: builtins.str,
    configuration_profile_id: builtins.str,
    content: builtins.str,
    content_type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    latest_version_number: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
