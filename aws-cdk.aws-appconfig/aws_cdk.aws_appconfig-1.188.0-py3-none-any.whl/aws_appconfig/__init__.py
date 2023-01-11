'''
# AWS::AppConfig Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_appconfig as appconfig
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

from ._jsii import *

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnApplication(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appconfig.CfnApplication",
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
        import aws_cdk.aws_appconfig as appconfig
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__a78f51b1cb9d9974084f7e05c461d6e9ee478ff2abdebd56901df412b038f3b2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationProps(name=name, description=description, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5599e5220ce9ac1ddc8deea4d5b16618acfb820647d2d98d3da23df70e50bbdc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d0139f5bdfdcc09fed44a37ba65158383ccfd1cc45403d62d98dc049fec116b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7851ebf997cd25b0045cc057d86521c62f04a8e9f7eee1243ad9fb5de7cd043e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b132f708ecae562efba95113509d8f4f81fa9cf8d164558870b36c116c068827)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fc2a7d6e6304655ff518ecb2fc297b3582adad17ebf9bf0287f3d7299717d16)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appconfig.CfnApplication.TagsProperty",
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
                import aws_cdk.aws_appconfig as appconfig
                
                tags_property = appconfig.CfnApplication.TagsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__be346a86115540ba9703d27a482308a5da6e31f277941cdff95e2b7906caeee2)
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
    jsii_type="@aws-cdk/aws-appconfig.CfnApplicationProps",
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
            import aws_cdk.aws_appconfig as appconfig
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__a66847b69fbf020573af0440fa8efb86baaf53fcda58c007ec06b2e97784069d)
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnConfigurationProfile(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appconfig.CfnConfigurationProfile",
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
        import aws_cdk.aws_appconfig as appconfig
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        location_uri: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        retrieval_role_arn: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnConfigurationProfile.TagsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        type: typing.Optional[builtins.str] = None,
        validators: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union["CfnConfigurationProfile.ValidatorsProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__d44a59eaeb0872e6693b92acc1914baf26e353ae790631e15a0fcd3127600d0b)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af3419ac9cf5425f174a499eb07dcaccda397c34e7d72a2e7ca2a5b4e615c5ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cf7d7553ce1925ffd06c35c48ecdb065091166b911f5a4df278b7842d7732a24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1d195c3676d604c283269248f63b652525ae8c4883385c95ee6a7fb8034dff83)
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
            type_hints = typing.get_type_hints(_typecheckingstub__37fd96ff8da96c40956bcf6e3c83b7fb8f997299d311620b0989581406e2ff3c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f80937d6eda53fcb97096cf4dd3d9b64723c5604df8a284d89bcacb877d1f1e9)
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
            type_hints = typing.get_type_hints(_typecheckingstub__10db54daa6632bb08909870dd5a4f7213f42208de75035e9e1f89be8fd80c36d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__33e0fdcb0c931bf8d2f0030714fb92433ea6ada51befa3616f5dc89f798f5564)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2924d2186a4c19d50d409257b9ed8786b6e81b59d2a093f23d093e7e9afc4ea2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a3b86c2fc57f3ca3f71553a0a519f7c850e3ec7c82b2a98d886e7aa12e1bc92b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="validators")
    def validators(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnConfigurationProfile.ValidatorsProperty", _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''A list of methods for validating the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-validators
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnConfigurationProfile.ValidatorsProperty", _aws_cdk_core_f4b25747.IResolvable]]]], jsii.get(self, "validators"))

    @validators.setter
    def validators(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnConfigurationProfile.ValidatorsProperty", _aws_cdk_core_f4b25747.IResolvable]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49b8cf6475691cba9103a338b743fe6379d133f8f3418fe85ec23e48a526d77a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "validators", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appconfig.CfnConfigurationProfile.TagsProperty",
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
                import aws_cdk.aws_appconfig as appconfig
                
                tags_property = appconfig.CfnConfigurationProfile.TagsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__57720f152e0721e132963b92b7092465967a0301be2e3fb7e9bbb0a606b61f38)
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
        jsii_type="@aws-cdk/aws-appconfig.CfnConfigurationProfile.ValidatorsProperty",
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
                import aws_cdk.aws_appconfig as appconfig
                
                validators_property = appconfig.CfnConfigurationProfile.ValidatorsProperty(
                    content="content",
                    type="type"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8654dbede16101e4bbb8067fa8269e053b64b735f61c6bc3a5ed4b27c07e11ea)
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
    jsii_type="@aws-cdk/aws-appconfig.CfnConfigurationProfileProps",
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
        validators: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnConfigurationProfile.ValidatorsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
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
            import aws_cdk.aws_appconfig as appconfig
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__23c07899461b88536b791a3d465b56b48de65f5735b4a0163a9fdf7630454313)
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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnConfigurationProfile.ValidatorsProperty, _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''A list of methods for validating the configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-configurationprofile.html#cfn-appconfig-configurationprofile-validators
        '''
        result = self._values.get("validators")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnConfigurationProfile.ValidatorsProperty, _aws_cdk_core_f4b25747.IResolvable]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDeployment(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appconfig.CfnDeployment",
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
        import aws_cdk.aws_appconfig as appconfig
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__362c3c91b85240e58a8a472dadd5a3af744b05f4b719914461149beca92ac0f1)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3882a56feec82ee77c0f8ac11b78e0c315ad9dc1187a45fff003aa7fcd53eeb5)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3fe6147543e61f1509198b75975aa944b63bcfbfea135bb95ea0177e63931f0e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__01a5e928cf53e4126c9462727d35ce9c7ea0ebda654fe49498c57431d9709c5b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9637bd17e39acdd50993c2f0fd18ef514ee8cd77d008b85d19405d629c19667)
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
            type_hints = typing.get_type_hints(_typecheckingstub__14f4fb424ee09d91ca28dccebb9fa0762c42f82f9df7822e7e59718594ef7d86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84a445edac86321a26a8a12b4ae09739557a5537cbbd1d64d3d5be8cd104796d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72a3bad813db62982608be194140105a7b44979b4d15a75ea014b37106d8fa41)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f8459d04bb6af9cb3157a5eef35eaf7ccf68672e819d8b4b9114e2b6cc3054ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__12efb9e690e873a3f15619e96fe78da9628917402dca1e424b8cc12085b11f87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appconfig.CfnDeployment.TagsProperty",
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
                import aws_cdk.aws_appconfig as appconfig
                
                tags_property = appconfig.CfnDeployment.TagsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9a79b938d5300e721426a31a906407811dc7a23db0fc6485cfa8e10ff86b973f)
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
    jsii_type="@aws-cdk/aws-appconfig.CfnDeploymentProps",
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
            import aws_cdk.aws_appconfig as appconfig
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__393f13d039519c069c8bc9d8b8c27444a6fb20134459a4d20271d87b1232c78b)
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnDeploymentStrategy(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appconfig.CfnDeploymentStrategy",
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
        import aws_cdk.aws_appconfig as appconfig
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__5f76909a39b00566845c513f60aa336b11e3230419fe8b75d458e88c695de75d)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0bd3604637fd3cd41a0fa91eeccbc5f1cd63c717719c96d2edef537926c69d06)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d6cd618342939a9a39303ecd1d444ab5714773953937aa4f8b4f46b55008078)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c3dc17e5a7ae1f3051bffec4bea65b00f93099bfaf2dba7f6f2bf6be6897e50)
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
            type_hints = typing.get_type_hints(_typecheckingstub__736fbb4b4fee58bc79f70e9663c561b69e8d2a7c469d3b07add0de4687e6ab3f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e8c25f344b47adc4c1648cda9192c3dd9e2df6aab6b017bbf59d043033fa577)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3c2d6b10e825f6310e4dc368a8929dfe90fcba4c09ddb68ab5cc7aa8e599131a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__31d987d555ec94080313e63f07d3ce711d2534f01fff73c6c394ff32bca6c55b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__92334f80c05bf7ddf72bd5062b77a919044f6ddee41146f476ad060b5fabe536)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4000eab962ebfbe84738cf0581268af4df3771728e03ea9f2a640cee9948bd62)
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
            type_hints = typing.get_type_hints(_typecheckingstub__819892530959b45038912cd9b586c956b67c6861a8302086270f7b83980d777c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appconfig.CfnDeploymentStrategy.TagsProperty",
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
                import aws_cdk.aws_appconfig as appconfig
                
                tags_property = appconfig.CfnDeploymentStrategy.TagsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__68965f122266aa6e48e511a98380de724485094251f90acde19ac9a78b827a24)
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
    jsii_type="@aws-cdk/aws-appconfig.CfnDeploymentStrategyProps",
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
            import aws_cdk.aws_appconfig as appconfig
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__9a492ef2cf63cd25e75d5439521ec447a2d6e6196e5f98d41da723b7df849dae)
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnEnvironment(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appconfig.CfnEnvironment",
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
        import aws_cdk.aws_appconfig as appconfig
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_id: builtins.str,
        name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        monitors: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEnvironment.MonitorsProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__f32abffd548b05067e8d4a55cc6338a98c9536df7bd301dd73bafb8d35d666c5)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e732c2333e8daf2af05356ca5fe68512709d67099d49520a5d8822f7efddb24)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3f6b0527c64ef8021cd34024511f285cad41854bc4df0b42f674adfd936d2d43)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8cf71d044ad6c1e0447699cd16bbb05f05d4015f72d1d484dd9ececcf0bade96)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cdc172fcb55fb94500a4f0327475ae8fd2fbb9bffc5d958c38a3fb2ff6fff0ce)
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
            type_hints = typing.get_type_hints(_typecheckingstub__47f44f4c5110524e5cb6b7f7a2289a910ebb22acde5c39bbe2a12baed32ead58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="monitors")
    def monitors(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.MonitorsProperty"]]]]:
        '''Amazon CloudWatch alarms to monitor during the deployment process.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-monitors
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.MonitorsProperty"]]]], jsii.get(self, "monitors"))

    @monitors.setter
    def monitors(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.MonitorsProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9493d0b55d5534b36e0b05f10e83842ba07ff64ad40444c038bf40c206d602ec)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4d1b92bba83f510a16756ac4bfdc58a44f5c6981f43d2f62423533ec21d4ec8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-appconfig.CfnEnvironment.MonitorsProperty",
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
                import aws_cdk.aws_appconfig as appconfig
                
                monitors_property = appconfig.CfnEnvironment.MonitorsProperty(
                    alarm_arn="alarmArn",
                    alarm_role_arn="alarmRoleArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d64428859d43a2164fe35708999e9f957752b9f36601181a4e04ff4383e27419)
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
        jsii_type="@aws-cdk/aws-appconfig.CfnEnvironment.TagsProperty",
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
                import aws_cdk.aws_appconfig as appconfig
                
                tags_property = appconfig.CfnEnvironment.TagsProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8aeac3630caf968fca32a2aeaaa297d218d80974abaacb6ecc7476c7d916010f)
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
    jsii_type="@aws-cdk/aws-appconfig.CfnEnvironmentProps",
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
        monitors: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEnvironment.MonitorsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
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
            import aws_cdk.aws_appconfig as appconfig
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d2b9a9a2af342cf5817eda924117632192a5a1f36c8e9c8b4476a39dc13bce7)
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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEnvironment.MonitorsProperty]]]]:
        '''Amazon CloudWatch alarms to monitor during the deployment process.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appconfig-environment.html#cfn-appconfig-environment-monitors
        '''
        result = self._values.get("monitors")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEnvironment.MonitorsProperty]]]], result)

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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnHostedConfigurationVersion(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-appconfig.CfnHostedConfigurationVersion",
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
        import aws_cdk.aws_appconfig as appconfig
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__5d34d2a910ad4c020b01cef5eac5cf05f67641e547de7fb2a1d62ea166589411)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f04de4e25709e8f605f21e21b0d990976b6d8e4dee8f29083193665b9cb6ae08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f021eac5b1a47bbd603ebb5f1cea73263823d2cb3713b30ad7525452a5a39fbc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f19ee6facd7ad9d660766cec336684f174249ee606d9bd71197c411e61536147)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d589ba590ab05d1962a088a92ac79bba6f7b2565ff5a0979a89a96af354ad74d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc3c64a95768d8f782de4992f615e59137a821b5a5d14a1621c10b9b6e53e622)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0c547e8521de75c4dbd83992f1844c29576af86106eb43be3e0edfdd51c06d26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4df507e33c587f513c5685dbd6ac830638753cbad00a24d683bf2df735784575)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28276b6dae64a366fcaa1d568e285b1dc7291d06fdb1e2584f55965e86c9f807)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "latestVersionNumber", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-appconfig.CfnHostedConfigurationVersionProps",
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
            import aws_cdk.aws_appconfig as appconfig
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__f117397e5f8558434a0316b263b429cc26c53314d80531ac54c1802d7d0b135e)
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

def _typecheckingstub__a78f51b1cb9d9974084f7e05c461d6e9ee478ff2abdebd56901df412b038f3b2(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnApplication.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5599e5220ce9ac1ddc8deea4d5b16618acfb820647d2d98d3da23df70e50bbdc(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d0139f5bdfdcc09fed44a37ba65158383ccfd1cc45403d62d98dc049fec116b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7851ebf997cd25b0045cc057d86521c62f04a8e9f7eee1243ad9fb5de7cd043e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b132f708ecae562efba95113509d8f4f81fa9cf8d164558870b36c116c068827(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fc2a7d6e6304655ff518ecb2fc297b3582adad17ebf9bf0287f3d7299717d16(
    value: typing.Optional[typing.List[CfnApplication.TagsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be346a86115540ba9703d27a482308a5da6e31f277941cdff95e2b7906caeee2(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a66847b69fbf020573af0440fa8efb86baaf53fcda58c007ec06b2e97784069d(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnApplication.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d44a59eaeb0872e6693b92acc1914baf26e353ae790631e15a0fcd3127600d0b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_id: builtins.str,
    location_uri: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    retrieval_role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnConfigurationProfile.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
    validators: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnConfigurationProfile.ValidatorsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af3419ac9cf5425f174a499eb07dcaccda397c34e7d72a2e7ca2a5b4e615c5ac(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf7d7553ce1925ffd06c35c48ecdb065091166b911f5a4df278b7842d7732a24(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d195c3676d604c283269248f63b652525ae8c4883385c95ee6a7fb8034dff83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37fd96ff8da96c40956bcf6e3c83b7fb8f997299d311620b0989581406e2ff3c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f80937d6eda53fcb97096cf4dd3d9b64723c5604df8a284d89bcacb877d1f1e9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10db54daa6632bb08909870dd5a4f7213f42208de75035e9e1f89be8fd80c36d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33e0fdcb0c931bf8d2f0030714fb92433ea6ada51befa3616f5dc89f798f5564(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2924d2186a4c19d50d409257b9ed8786b6e81b59d2a093f23d093e7e9afc4ea2(
    value: typing.Optional[typing.List[CfnConfigurationProfile.TagsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3b86c2fc57f3ca3f71553a0a519f7c850e3ec7c82b2a98d886e7aa12e1bc92b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49b8cf6475691cba9103a338b743fe6379d133f8f3418fe85ec23e48a526d77a(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnConfigurationProfile.ValidatorsProperty, _aws_cdk_core_f4b25747.IResolvable]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57720f152e0721e132963b92b7092465967a0301be2e3fb7e9bbb0a606b61f38(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8654dbede16101e4bbb8067fa8269e053b64b735f61c6bc3a5ed4b27c07e11ea(
    *,
    content: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23c07899461b88536b791a3d465b56b48de65f5735b4a0163a9fdf7630454313(
    *,
    application_id: builtins.str,
    location_uri: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    retrieval_role_arn: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnConfigurationProfile.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    type: typing.Optional[builtins.str] = None,
    validators: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnConfigurationProfile.ValidatorsProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__362c3c91b85240e58a8a472dadd5a3af744b05f4b719914461149beca92ac0f1(
    scope: _aws_cdk_core_f4b25747.Construct,
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

def _typecheckingstub__3882a56feec82ee77c0f8ac11b78e0c315ad9dc1187a45fff003aa7fcd53eeb5(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fe6147543e61f1509198b75975aa944b63bcfbfea135bb95ea0177e63931f0e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a5e928cf53e4126c9462727d35ce9c7ea0ebda654fe49498c57431d9709c5b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9637bd17e39acdd50993c2f0fd18ef514ee8cd77d008b85d19405d629c19667(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14f4fb424ee09d91ca28dccebb9fa0762c42f82f9df7822e7e59718594ef7d86(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84a445edac86321a26a8a12b4ae09739557a5537cbbd1d64d3d5be8cd104796d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72a3bad813db62982608be194140105a7b44979b4d15a75ea014b37106d8fa41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8459d04bb6af9cb3157a5eef35eaf7ccf68672e819d8b4b9114e2b6cc3054ac(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12efb9e690e873a3f15619e96fe78da9628917402dca1e424b8cc12085b11f87(
    value: typing.Optional[typing.List[CfnDeployment.TagsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a79b938d5300e721426a31a906407811dc7a23db0fc6485cfa8e10ff86b973f(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__393f13d039519c069c8bc9d8b8c27444a6fb20134459a4d20271d87b1232c78b(
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

def _typecheckingstub__5f76909a39b00566845c513f60aa336b11e3230419fe8b75d458e88c695de75d(
    scope: _aws_cdk_core_f4b25747.Construct,
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

def _typecheckingstub__0bd3604637fd3cd41a0fa91eeccbc5f1cd63c717719c96d2edef537926c69d06(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d6cd618342939a9a39303ecd1d444ab5714773953937aa4f8b4f46b55008078(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c3dc17e5a7ae1f3051bffec4bea65b00f93099bfaf2dba7f6f2bf6be6897e50(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__736fbb4b4fee58bc79f70e9663c561b69e8d2a7c469d3b07add0de4687e6ab3f(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e8c25f344b47adc4c1648cda9192c3dd9e2df6aab6b017bbf59d043033fa577(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c2d6b10e825f6310e4dc368a8929dfe90fcba4c09ddb68ab5cc7aa8e599131a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31d987d555ec94080313e63f07d3ce711d2534f01fff73c6c394ff32bca6c55b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92334f80c05bf7ddf72bd5062b77a919044f6ddee41146f476ad060b5fabe536(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4000eab962ebfbe84738cf0581268af4df3771728e03ea9f2a640cee9948bd62(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__819892530959b45038912cd9b586c956b67c6861a8302086270f7b83980d777c(
    value: typing.Optional[typing.List[CfnDeploymentStrategy.TagsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68965f122266aa6e48e511a98380de724485094251f90acde19ac9a78b827a24(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a492ef2cf63cd25e75d5439521ec447a2d6e6196e5f98d41da723b7df849dae(
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

def _typecheckingstub__f32abffd548b05067e8d4a55cc6338a98c9536df7bd301dd73bafb8d35d666c5(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_id: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    monitors: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEnvironment.MonitorsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnEnvironment.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e732c2333e8daf2af05356ca5fe68512709d67099d49520a5d8822f7efddb24(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f6b0527c64ef8021cd34024511f285cad41854bc4df0b42f674adfd936d2d43(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8cf71d044ad6c1e0447699cd16bbb05f05d4015f72d1d484dd9ececcf0bade96(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc172fcb55fb94500a4f0327475ae8fd2fbb9bffc5d958c38a3fb2ff6fff0ce(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47f44f4c5110524e5cb6b7f7a2289a910ebb22acde5c39bbe2a12baed32ead58(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9493d0b55d5534b36e0b05f10e83842ba07ff64ad40444c038bf40c206d602ec(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEnvironment.MonitorsProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d1b92bba83f510a16756ac4bfdc58a44f5c6981f43d2f62423533ec21d4ec8a(
    value: typing.Optional[typing.List[CfnEnvironment.TagsProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d64428859d43a2164fe35708999e9f957752b9f36601181a4e04ff4383e27419(
    *,
    alarm_arn: typing.Optional[builtins.str] = None,
    alarm_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8aeac3630caf968fca32a2aeaaa297d218d80974abaacb6ecc7476c7d916010f(
    *,
    key: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2b9a9a2af342cf5817eda924117632192a5a1f36c8e9c8b4476a39dc13bce7(
    *,
    application_id: builtins.str,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    monitors: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEnvironment.MonitorsProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnEnvironment.TagsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5d34d2a910ad4c020b01cef5eac5cf05f67641e547de7fb2a1d62ea166589411(
    scope: _aws_cdk_core_f4b25747.Construct,
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

def _typecheckingstub__f04de4e25709e8f605f21e21b0d990976b6d8e4dee8f29083193665b9cb6ae08(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f021eac5b1a47bbd603ebb5f1cea73263823d2cb3713b30ad7525452a5a39fbc(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19ee6facd7ad9d660766cec336684f174249ee606d9bd71197c411e61536147(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d589ba590ab05d1962a088a92ac79bba6f7b2565ff5a0979a89a96af354ad74d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc3c64a95768d8f782de4992f615e59137a821b5a5d14a1621c10b9b6e53e622(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c547e8521de75c4dbd83992f1844c29576af86106eb43be3e0edfdd51c06d26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4df507e33c587f513c5685dbd6ac830638753cbad00a24d683bf2df735784575(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28276b6dae64a366fcaa1d568e285b1dc7291d06fdb1e2584f55965e86c9f807(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f117397e5f8558434a0316b263b429cc26c53314d80531ac54c1802d7d0b135e(
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
