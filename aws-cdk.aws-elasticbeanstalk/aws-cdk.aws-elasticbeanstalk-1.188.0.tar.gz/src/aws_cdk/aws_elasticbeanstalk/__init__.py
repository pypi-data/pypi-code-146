'''
# AWS Elastic Beanstalk Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for ElasticBeanstalk construct libraries](https://constructs.dev/search?q=elasticbeanstalk)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::ElasticBeanstalk resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ElasticBeanstalk.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::ElasticBeanstalk](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ElasticBeanstalk.html).

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
    jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication",
):
    '''A CloudFormation ``AWS::ElasticBeanstalk::Application``.

    Specify an AWS Elastic Beanstalk application by using the AWS::ElasticBeanstalk::Application resource in an AWS CloudFormation template.

    The AWS::ElasticBeanstalk::Application resource is an AWS Elastic Beanstalk Beanstalk resource type that specifies an Elastic Beanstalk application.

    :cloudformationResource: AWS::ElasticBeanstalk::Application
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-application.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
        
        cfn_application = elasticbeanstalk.CfnApplication(self, "MyCfnApplication",
            application_name="applicationName",
            description="description",
            resource_lifecycle_config=elasticbeanstalk.CfnApplication.ApplicationResourceLifecycleConfigProperty(
                service_role="serviceRole",
                version_lifecycle_config=elasticbeanstalk.CfnApplication.ApplicationVersionLifecycleConfigProperty(
                    max_age_rule=elasticbeanstalk.CfnApplication.MaxAgeRuleProperty(
                        delete_source_from_s3=False,
                        enabled=False,
                        max_age_in_days=123
                    ),
                    max_count_rule=elasticbeanstalk.CfnApplication.MaxCountRuleProperty(
                        delete_source_from_s3=False,
                        enabled=False,
                        max_count=123
                    )
                )
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        resource_lifecycle_config: typing.Optional[typing.Union[typing.Union["CfnApplication.ApplicationResourceLifecycleConfigProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Create a new ``AWS::ElasticBeanstalk::Application``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: A name for the Elastic Beanstalk application. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the application name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param description: Your description of the application.
        :param resource_lifecycle_config: Specifies an application resource lifecycle configuration to prevent your application from accumulating too many versions.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__034105bd0cefe052895f317e28891c732c15652c08f71b0c275d1038aa1e3458)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationProps(
            application_name=application_name,
            description=description,
            resource_lifecycle_config=resource_lifecycle_config,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47e1e7cf51bdc9ea6861173db70e678eeb3285de55a8a515a7cf0d3f01ab165a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8e12f018b5d1cf84349164323ec91f760fb50747650c5b8cb89896d6f15d802b)
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
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> typing.Optional[builtins.str]:
        '''A name for the Elastic Beanstalk application.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the application name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-application.html#cfn-elasticbeanstalk-application-applicationname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "applicationName"))

    @application_name.setter
    def application_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ce93feb3c7bf7ad89cc9985bbf659227ad9ff6c1bfebfc597ead0370aafdd67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''Your description of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-application.html#cfn-elasticbeanstalk-application-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf8d7e3d580f006280c47743dfd2397d50e82a3353c666d7cd249ca431c9521c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="resourceLifecycleConfig")
    def resource_lifecycle_config(
        self,
    ) -> typing.Optional[typing.Union["CfnApplication.ApplicationResourceLifecycleConfigProperty", _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies an application resource lifecycle configuration to prevent your application from accumulating too many versions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-application.html#cfn-elasticbeanstalk-application-resourcelifecycleconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApplication.ApplicationResourceLifecycleConfigProperty", _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "resourceLifecycleConfig"))

    @resource_lifecycle_config.setter
    def resource_lifecycle_config(
        self,
        value: typing.Optional[typing.Union["CfnApplication.ApplicationResourceLifecycleConfigProperty", _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9b53d79a6cc8d489f18e895c643da8a6ecf2a916701b5054eefdf0d464e1886)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceLifecycleConfig", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication.ApplicationResourceLifecycleConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "service_role": "serviceRole",
            "version_lifecycle_config": "versionLifecycleConfig",
        },
    )
    class ApplicationResourceLifecycleConfigProperty:
        def __init__(
            self,
            *,
            service_role: typing.Optional[builtins.str] = None,
            version_lifecycle_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApplication.ApplicationVersionLifecycleConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Use the ``ApplicationResourceLifecycleConfig`` property type to specify lifecycle settings for resources that belong to an AWS Elastic Beanstalk application when defining an AWS::ElasticBeanstalk::Application resource in an AWS CloudFormation template.

            The resource lifecycle configuration for an application. Defines lifecycle settings for resources that belong to the application, and the service role that Elastic Beanstalk assumes in order to apply lifecycle settings. The version lifecycle configuration defines lifecycle settings for application versions.

            ``ApplicationResourceLifecycleConfig`` is a property of the `AWS::ElasticBeanstalk::Application <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk.html>`_ resource.

            :param service_role: The ARN of an IAM service role that Elastic Beanstalk has permission to assume. The ``ServiceRole`` property is required the first time that you provide a ``ResourceLifecycleConfig`` for the application. After you provide it once, Elastic Beanstalk persists the Service Role with the application, and you don't need to specify it again. You can, however, specify it in subsequent updates to change the Service Role to another value.
            :param version_lifecycle_config: Defines lifecycle settings for application versions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationresourcelifecycleconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
                
                application_resource_lifecycle_config_property = elasticbeanstalk.CfnApplication.ApplicationResourceLifecycleConfigProperty(
                    service_role="serviceRole",
                    version_lifecycle_config=elasticbeanstalk.CfnApplication.ApplicationVersionLifecycleConfigProperty(
                        max_age_rule=elasticbeanstalk.CfnApplication.MaxAgeRuleProperty(
                            delete_source_from_s3=False,
                            enabled=False,
                            max_age_in_days=123
                        ),
                        max_count_rule=elasticbeanstalk.CfnApplication.MaxCountRuleProperty(
                            delete_source_from_s3=False,
                            enabled=False,
                            max_count=123
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__72472b75c094b78f2cedf0f4e7b8ccdccdc8ffa87143fe834efd5aebffb11548)
                check_type(argname="argument service_role", value=service_role, expected_type=type_hints["service_role"])
                check_type(argname="argument version_lifecycle_config", value=version_lifecycle_config, expected_type=type_hints["version_lifecycle_config"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if service_role is not None:
                self._values["service_role"] = service_role
            if version_lifecycle_config is not None:
                self._values["version_lifecycle_config"] = version_lifecycle_config

        @builtins.property
        def service_role(self) -> typing.Optional[builtins.str]:
            '''The ARN of an IAM service role that Elastic Beanstalk has permission to assume.

            The ``ServiceRole`` property is required the first time that you provide a ``ResourceLifecycleConfig`` for the application. After you provide it once, Elastic Beanstalk persists the Service Role with the application, and you don't need to specify it again. You can, however, specify it in subsequent updates to change the Service Role to another value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationresourcelifecycleconfig.html#cfn-elasticbeanstalk-application-applicationresourcelifecycleconfig-servicerole
            '''
            result = self._values.get("service_role")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version_lifecycle_config(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.ApplicationVersionLifecycleConfigProperty"]]:
            '''Defines lifecycle settings for application versions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationresourcelifecycleconfig.html#cfn-elasticbeanstalk-application-applicationresourcelifecycleconfig-versionlifecycleconfig
            '''
            result = self._values.get("version_lifecycle_config")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.ApplicationVersionLifecycleConfigProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationResourceLifecycleConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication.ApplicationVersionLifecycleConfigProperty",
        jsii_struct_bases=[],
        name_mapping={"max_age_rule": "maxAgeRule", "max_count_rule": "maxCountRule"},
    )
    class ApplicationVersionLifecycleConfigProperty:
        def __init__(
            self,
            *,
            max_age_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApplication.MaxAgeRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            max_count_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApplication.MaxCountRuleProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Use the ``ApplicationVersionLifecycleConfig`` property type to specify application version lifecycle settings for an AWS Elastic Beanstalk application when defining an AWS::ElasticBeanstalk::Application resource in an AWS CloudFormation template.

            The application version lifecycle settings for an application. Defines the rules that Elastic Beanstalk applies to an application's versions in order to avoid hitting the per-region limit for application versions.

            When Elastic Beanstalk deletes an application version from its database, you can no longer deploy that version to an environment. The source bundle remains in S3 unless you configure the rule to delete it.

            ``ApplicationVersionLifecycleConfig`` is a property of the `ApplicationResourceLifecycleConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationresourcelifecycleconfig.html>`_ property type.

            :param max_age_rule: Specify a max age rule to restrict the length of time that application versions are retained for an application.
            :param max_count_rule: Specify a max count rule to restrict the number of application versions that are retained for an application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationversionlifecycleconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
                
                application_version_lifecycle_config_property = elasticbeanstalk.CfnApplication.ApplicationVersionLifecycleConfigProperty(
                    max_age_rule=elasticbeanstalk.CfnApplication.MaxAgeRuleProperty(
                        delete_source_from_s3=False,
                        enabled=False,
                        max_age_in_days=123
                    ),
                    max_count_rule=elasticbeanstalk.CfnApplication.MaxCountRuleProperty(
                        delete_source_from_s3=False,
                        enabled=False,
                        max_count=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9e98bafdfb57cc5a70f564ca23681288e262b3b593732da552e0e9b134f19644)
                check_type(argname="argument max_age_rule", value=max_age_rule, expected_type=type_hints["max_age_rule"])
                check_type(argname="argument max_count_rule", value=max_count_rule, expected_type=type_hints["max_count_rule"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if max_age_rule is not None:
                self._values["max_age_rule"] = max_age_rule
            if max_count_rule is not None:
                self._values["max_count_rule"] = max_count_rule

        @builtins.property
        def max_age_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.MaxAgeRuleProperty"]]:
            '''Specify a max age rule to restrict the length of time that application versions are retained for an application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationversionlifecycleconfig.html#cfn-elasticbeanstalk-application-applicationversionlifecycleconfig-maxagerule
            '''
            result = self._values.get("max_age_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.MaxAgeRuleProperty"]], result)

        @builtins.property
        def max_count_rule(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.MaxCountRuleProperty"]]:
            '''Specify a max count rule to restrict the number of application versions that are retained for an application.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationversionlifecycleconfig.html#cfn-elasticbeanstalk-application-applicationversionlifecycleconfig-maxcountrule
            '''
            result = self._values.get("max_count_rule")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplication.MaxCountRuleProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApplicationVersionLifecycleConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication.MaxAgeRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delete_source_from_s3": "deleteSourceFromS3",
            "enabled": "enabled",
            "max_age_in_days": "maxAgeInDays",
        },
    )
    class MaxAgeRuleProperty:
        def __init__(
            self,
            *,
            delete_source_from_s3: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            max_age_in_days: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Use the ``MaxAgeRule`` property type to specify a max age rule to restrict the length of time that application versions are retained for an AWS Elastic Beanstalk application when defining an AWS::ElasticBeanstalk::Application resource in an AWS CloudFormation template.

            A lifecycle rule that deletes application versions after the specified number of days.

            ``MaxAgeRule`` is a property of the `ApplicationVersionLifecycleConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationversionlifecycleconfig.html>`_ property type.

            :param delete_source_from_s3: Set to ``true`` to delete a version's source bundle from Amazon S3 when Elastic Beanstalk deletes the application version.
            :param enabled: Specify ``true`` to apply the rule, or ``false`` to disable it.
            :param max_age_in_days: Specify the number of days to retain an application versions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxagerule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
                
                max_age_rule_property = elasticbeanstalk.CfnApplication.MaxAgeRuleProperty(
                    delete_source_from_s3=False,
                    enabled=False,
                    max_age_in_days=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c5cd4098968a38f97924ebb79570bf55af9105bcc4b67d4ec0137fd6d3009f04)
                check_type(argname="argument delete_source_from_s3", value=delete_source_from_s3, expected_type=type_hints["delete_source_from_s3"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument max_age_in_days", value=max_age_in_days, expected_type=type_hints["max_age_in_days"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delete_source_from_s3 is not None:
                self._values["delete_source_from_s3"] = delete_source_from_s3
            if enabled is not None:
                self._values["enabled"] = enabled
            if max_age_in_days is not None:
                self._values["max_age_in_days"] = max_age_in_days

        @builtins.property
        def delete_source_from_s3(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Set to ``true`` to delete a version's source bundle from Amazon S3 when Elastic Beanstalk deletes the application version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxagerule.html#cfn-elasticbeanstalk-application-maxagerule-deletesourcefroms3
            '''
            result = self._values.get("delete_source_from_s3")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Specify ``true`` to apply the rule, or ``false`` to disable it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxagerule.html#cfn-elasticbeanstalk-application-maxagerule-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def max_age_in_days(self) -> typing.Optional[jsii.Number]:
            '''Specify the number of days to retain an application versions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxagerule.html#cfn-elasticbeanstalk-application-maxagerule-maxageindays
            '''
            result = self._values.get("max_age_in_days")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaxAgeRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplication.MaxCountRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "delete_source_from_s3": "deleteSourceFromS3",
            "enabled": "enabled",
            "max_count": "maxCount",
        },
    )
    class MaxCountRuleProperty:
        def __init__(
            self,
            *,
            delete_source_from_s3: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            max_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Use the ``MaxAgeRule`` property type to specify a max count rule to restrict the number of application versions that are retained for an AWS Elastic Beanstalk application when defining an AWS::ElasticBeanstalk::Application resource in an AWS CloudFormation template.

            A lifecycle rule that deletes the oldest application version when the maximum count is exceeded.

            ``MaxCountRule`` is a property of the `ApplicationVersionLifecycleConfig <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-applicationversionlifecycleconfig.html>`_ property type.

            :param delete_source_from_s3: Set to ``true`` to delete a version's source bundle from Amazon S3 when Elastic Beanstalk deletes the application version.
            :param enabled: Specify ``true`` to apply the rule, or ``false`` to disable it.
            :param max_count: Specify the maximum number of application versions to retain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxcountrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
                
                max_count_rule_property = elasticbeanstalk.CfnApplication.MaxCountRuleProperty(
                    delete_source_from_s3=False,
                    enabled=False,
                    max_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__109bde59813451cf34d1c65e04d22aee5232c87265e53eae42a0f06a462c27e2)
                check_type(argname="argument delete_source_from_s3", value=delete_source_from_s3, expected_type=type_hints["delete_source_from_s3"])
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument max_count", value=max_count, expected_type=type_hints["max_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if delete_source_from_s3 is not None:
                self._values["delete_source_from_s3"] = delete_source_from_s3
            if enabled is not None:
                self._values["enabled"] = enabled
            if max_count is not None:
                self._values["max_count"] = max_count

        @builtins.property
        def delete_source_from_s3(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Set to ``true`` to delete a version's source bundle from Amazon S3 when Elastic Beanstalk deletes the application version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxcountrule.html#cfn-elasticbeanstalk-application-maxcountrule-deletesourcefroms3
            '''
            result = self._values.get("delete_source_from_s3")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Specify ``true`` to apply the rule, or ``false`` to disable it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxcountrule.html#cfn-elasticbeanstalk-application-maxcountrule-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def max_count(self) -> typing.Optional[jsii.Number]:
            '''Specify the maximum number of application versions to retain.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-application-maxcountrule.html#cfn-elasticbeanstalk-application-maxcountrule-maxcount
            '''
            result = self._values.get("max_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MaxCountRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplicationProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "description": "description",
        "resource_lifecycle_config": "resourceLifecycleConfig",
    },
)
class CfnApplicationProps:
    def __init__(
        self,
        *,
        application_name: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        resource_lifecycle_config: typing.Optional[typing.Union[typing.Union[CfnApplication.ApplicationResourceLifecycleConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApplication``.

        :param application_name: A name for the Elastic Beanstalk application. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the application name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param description: Your description of the application.
        :param resource_lifecycle_config: Specifies an application resource lifecycle configuration to prevent your application from accumulating too many versions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-application.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
            
            cfn_application_props = elasticbeanstalk.CfnApplicationProps(
                application_name="applicationName",
                description="description",
                resource_lifecycle_config=elasticbeanstalk.CfnApplication.ApplicationResourceLifecycleConfigProperty(
                    service_role="serviceRole",
                    version_lifecycle_config=elasticbeanstalk.CfnApplication.ApplicationVersionLifecycleConfigProperty(
                        max_age_rule=elasticbeanstalk.CfnApplication.MaxAgeRuleProperty(
                            delete_source_from_s3=False,
                            enabled=False,
                            max_age_in_days=123
                        ),
                        max_count_rule=elasticbeanstalk.CfnApplication.MaxCountRuleProperty(
                            delete_source_from_s3=False,
                            enabled=False,
                            max_count=123
                        )
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a40c3bb2c0b1ec12fd0f7c123f331e2c43b51e25c47d0f6638eceaa3467cb5)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument resource_lifecycle_config", value=resource_lifecycle_config, expected_type=type_hints["resource_lifecycle_config"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if application_name is not None:
            self._values["application_name"] = application_name
        if description is not None:
            self._values["description"] = description
        if resource_lifecycle_config is not None:
            self._values["resource_lifecycle_config"] = resource_lifecycle_config

    @builtins.property
    def application_name(self) -> typing.Optional[builtins.str]:
        '''A name for the Elastic Beanstalk application.

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the application name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-application.html#cfn-elasticbeanstalk-application-applicationname
        '''
        result = self._values.get("application_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Your description of the application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-application.html#cfn-elasticbeanstalk-application-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_lifecycle_config(
        self,
    ) -> typing.Optional[typing.Union[CfnApplication.ApplicationResourceLifecycleConfigProperty, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Specifies an application resource lifecycle configuration to prevent your application from accumulating too many versions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-application.html#cfn-elasticbeanstalk-application-resourcelifecycleconfig
        '''
        result = self._values.get("resource_lifecycle_config")
        return typing.cast(typing.Optional[typing.Union[CfnApplication.ApplicationResourceLifecycleConfigProperty, _aws_cdk_core_f4b25747.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnApplicationVersion(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplicationVersion",
):
    '''A CloudFormation ``AWS::ElasticBeanstalk::ApplicationVersion``.

    Specify an AWS Elastic Beanstalk application version by using the AWS::ElasticBeanstalk::ApplicationVersion resource in an AWS CloudFormation template.

    The AWS::ElasticBeanstalk::ApplicationVersion resource is an AWS Elastic Beanstalk resource type that specifies an application version, an iteration of deployable code, for an Elastic Beanstalk application.
    .. epigraph::

       After you create an application version with a specified Amazon S3 bucket and key location, you can't change that Amazon S3 location. If you change the Amazon S3 location, an attempt to launch an environment from the application version will fail.

    :cloudformationResource: AWS::ElasticBeanstalk::ApplicationVersion
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-applicationversion.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
        
        cfn_application_version = elasticbeanstalk.CfnApplicationVersion(self, "MyCfnApplicationVersion",
            application_name="applicationName",
            source_bundle=elasticbeanstalk.CfnApplicationVersion.SourceBundleProperty(
                s3_bucket="s3Bucket",
                s3_key="s3Key"
            ),
        
            # the properties below are optional
            description="description"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_name: builtins.str,
        source_bundle: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnApplicationVersion.SourceBundleProperty", typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ElasticBeanstalk::ApplicationVersion``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: The name of the Elastic Beanstalk application that is associated with this application version.
        :param source_bundle: The Amazon S3 bucket and key that identify the location of the source bundle for this version. .. epigraph:: The Amazon S3 bucket must be in the same region as the environment.
        :param description: A description of this application version.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7c1a7d7f27ecf5d3f16e76851c4186826da354d92e1ce8b6abe31f30583dcf8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnApplicationVersionProps(
            application_name=application_name,
            source_bundle=source_bundle,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__662fc9c7a217e4e1568491fd70d10889489ccd8d3a994280639adcf78e088aef)
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
            type_hints = typing.get_type_hints(_typecheckingstub__672a989ccfd7a09a8fa5b959034ecbdef6446449b20f58d9830cac44c6c2a6bc)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''
        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''The name of the Elastic Beanstalk application that is associated with this application version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-applicationversion.html#cfn-elasticbeanstalk-applicationversion-applicationname
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))

    @application_name.setter
    def application_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b4f4db14743af26f27cf782a662ae30ee0938b589cc23c168c0f549afd1c4afa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationName", value)

    @builtins.property
    @jsii.member(jsii_name="sourceBundle")
    def source_bundle(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplicationVersion.SourceBundleProperty"]:
        '''The Amazon S3 bucket and key that identify the location of the source bundle for this version.

        .. epigraph::

           The Amazon S3 bucket must be in the same region as the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-applicationversion.html#cfn-elasticbeanstalk-applicationversion-sourcebundle
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplicationVersion.SourceBundleProperty"], jsii.get(self, "sourceBundle"))

    @source_bundle.setter
    def source_bundle(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnApplicationVersion.SourceBundleProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36d1e8f49e32d13b6276359e1c22975fbe188870d8a3b7620f992d6e3ba1d2ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceBundle", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of this application version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-applicationversion.html#cfn-elasticbeanstalk-applicationversion-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acf73c9d98c5a6f70d8785eab5fe8479e840180d0c144a0d0bbd8c8cfd344215)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplicationVersion.SourceBundleProperty",
        jsii_struct_bases=[],
        name_mapping={"s3_bucket": "s3Bucket", "s3_key": "s3Key"},
    )
    class SourceBundleProperty:
        def __init__(self, *, s3_bucket: builtins.str, s3_key: builtins.str) -> None:
            '''Use the ``SourceBundle`` property type to specify the Amazon S3 location of the source bundle for an AWS Elastic Beanstalk application version when defining an AWS::ElasticBeanstalk::ApplicationVersion resource in an AWS CloudFormation template.

            The ``SourceBundle`` property is an embedded property of the `AWS::ElasticBeanstalk::ApplicationVersion <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-sourcebundle.html>`_ resource. It specifies the Amazon S3 location of the source bundle for an AWS Elastic Beanstalk application version.

            :param s3_bucket: The Amazon S3 bucket where the data is located.
            :param s3_key: The Amazon S3 key where the data is located.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-applicationversion-sourcebundle.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
                
                source_bundle_property = elasticbeanstalk.CfnApplicationVersion.SourceBundleProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e12e1dd170d479c5a0df103ec6c5ffedfbaeb9b515fce23e0fce2a2767591862)
                check_type(argname="argument s3_bucket", value=s3_bucket, expected_type=type_hints["s3_bucket"])
                check_type(argname="argument s3_key", value=s3_key, expected_type=type_hints["s3_key"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "s3_bucket": s3_bucket,
                "s3_key": s3_key,
            }

        @builtins.property
        def s3_bucket(self) -> builtins.str:
            '''The Amazon S3 bucket where the data is located.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-applicationversion-sourcebundle.html#cfn-elasticbeanstalk-applicationversion-sourcebundle-s3bucket
            '''
            result = self._values.get("s3_bucket")
            assert result is not None, "Required property 's3_bucket' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def s3_key(self) -> builtins.str:
            '''The Amazon S3 key where the data is located.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-applicationversion-sourcebundle.html#cfn-elasticbeanstalk-applicationversion-sourcebundle-s3key
            '''
            result = self._values.get("s3_key")
            assert result is not None, "Required property 's3_key' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceBundleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnApplicationVersionProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "source_bundle": "sourceBundle",
        "description": "description",
    },
)
class CfnApplicationVersionProps:
    def __init__(
        self,
        *,
        application_name: builtins.str,
        source_bundle: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplicationVersion.SourceBundleProperty, typing.Dict[builtins.str, typing.Any]]],
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnApplicationVersion``.

        :param application_name: The name of the Elastic Beanstalk application that is associated with this application version.
        :param source_bundle: The Amazon S3 bucket and key that identify the location of the source bundle for this version. .. epigraph:: The Amazon S3 bucket must be in the same region as the environment.
        :param description: A description of this application version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-applicationversion.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
            
            cfn_application_version_props = elasticbeanstalk.CfnApplicationVersionProps(
                application_name="applicationName",
                source_bundle=elasticbeanstalk.CfnApplicationVersion.SourceBundleProperty(
                    s3_bucket="s3Bucket",
                    s3_key="s3Key"
                ),
            
                # the properties below are optional
                description="description"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11337e3be6c4f378c37f54cf366f6fa18de148aa667f2772ac816b9161c7fe29)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument source_bundle", value=source_bundle, expected_type=type_hints["source_bundle"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_name": application_name,
            "source_bundle": source_bundle,
        }
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def application_name(self) -> builtins.str:
        '''The name of the Elastic Beanstalk application that is associated with this application version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-applicationversion.html#cfn-elasticbeanstalk-applicationversion-applicationname
        '''
        result = self._values.get("application_name")
        assert result is not None, "Required property 'application_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_bundle(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplicationVersion.SourceBundleProperty]:
        '''The Amazon S3 bucket and key that identify the location of the source bundle for this version.

        .. epigraph::

           The Amazon S3 bucket must be in the same region as the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-applicationversion.html#cfn-elasticbeanstalk-applicationversion-sourcebundle
        '''
        result = self._values.get("source_bundle")
        assert result is not None, "Required property 'source_bundle' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplicationVersion.SourceBundleProperty], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of this application version.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-applicationversion.html#cfn-elasticbeanstalk-applicationversion-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnApplicationVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnConfigurationTemplate(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnConfigurationTemplate",
):
    '''A CloudFormation ``AWS::ElasticBeanstalk::ConfigurationTemplate``.

    Specify an AWS Elastic Beanstalk configuration template by using the AWS::ElasticBeanstalk::ConfigurationTemplate resource in an AWS CloudFormation template.

    The AWS::ElasticBeanstalk::ConfigurationTemplate resource is an AWS Elastic Beanstalk resource type that specifies an Elastic Beanstalk configuration template, associated with a specific Elastic Beanstalk application. You define application configuration settings in a configuration template. You can then use the configuration template to deploy different versions of the application with the same configuration settings.
    .. epigraph::

       The Elastic Beanstalk console and documentation often refer to configuration templates as *saved configurations* . When you set configuration options in a saved configuration (configuration template), Elastic Beanstalk applies them with a particular precedence as part of applying options from multiple sources. For more information, see `Configuration Options <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .

    :cloudformationResource: AWS::ElasticBeanstalk::ConfigurationTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
        
        cfn_configuration_template = elasticbeanstalk.CfnConfigurationTemplate(self, "MyCfnConfigurationTemplate",
            application_name="applicationName",
        
            # the properties below are optional
            description="description",
            environment_id="environmentId",
            option_settings=[elasticbeanstalk.CfnConfigurationTemplate.ConfigurationOptionSettingProperty(
                namespace="namespace",
                option_name="optionName",
        
                # the properties below are optional
                resource_name="resourceName",
                value="value"
            )],
            platform_arn="platformArn",
            solution_stack_name="solutionStackName",
            source_configuration=elasticbeanstalk.CfnConfigurationTemplate.SourceConfigurationProperty(
                application_name="applicationName",
                template_name="templateName"
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        environment_id: typing.Optional[builtins.str] = None,
        option_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfigurationTemplate.ConfigurationOptionSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        platform_arn: typing.Optional[builtins.str] = None,
        solution_stack_name: typing.Optional[builtins.str] = None,
        source_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnConfigurationTemplate.SourceConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::ElasticBeanstalk::ConfigurationTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: The name of the Elastic Beanstalk application to associate with this configuration template.
        :param description: An optional description for this configuration.
        :param environment_id: The ID of an environment whose settings you want to use to create the configuration template. You must specify ``EnvironmentId`` if you don't specify ``PlatformArn`` , ``SolutionStackName`` , or ``SourceConfiguration`` .
        :param option_settings: Option values for the Elastic Beanstalk configuration, such as the instance type. If specified, these values override the values obtained from the solution stack or the source configuration template. For a complete list of Elastic Beanstalk configuration options, see `Option Values <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .
        :param platform_arn: The Amazon Resource Name (ARN) of the custom platform. For more information, see `Custom Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/custom-platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* . .. epigraph:: If you specify ``PlatformArn`` , then don't specify ``SolutionStackName`` .
        :param solution_stack_name: The name of an Elastic Beanstalk solution stack (platform version) that this configuration uses. For example, ``64bit Amazon Linux 2013.09 running Tomcat 7 Java 7`` . A solution stack specifies the operating system, runtime, and application server for a configuration template. It also determines the set of configuration options as well as the possible and default values. For more information, see `Supported Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* . You must specify ``SolutionStackName`` if you don't specify ``PlatformArn`` , ``EnvironmentId`` , or ``SourceConfiguration`` . Use the ```ListAvailableSolutionStacks`` <https://docs.aws.amazon.com/elasticbeanstalk/latest/api/API_ListAvailableSolutionStacks.html>`_ API to obtain a list of available solution stacks.
        :param source_configuration: An Elastic Beanstalk configuration template to base this one on. If specified, Elastic Beanstalk uses the configuration values from the specified configuration template to create a new configuration. Values specified in ``OptionSettings`` override any values obtained from the ``SourceConfiguration`` . You must specify ``SourceConfiguration`` if you don't specify ``PlatformArn`` , ``EnvironmentId`` , or ``SolutionStackName`` . Constraint: If both solution stack name and source configuration are specified, the solution stack of the source configuration template must match the specified solution stack name.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb0e2c832e2ae2d269f27d0c11de12693f64bffa03e9d84b14b0856a530b31ee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnConfigurationTemplateProps(
            application_name=application_name,
            description=description,
            environment_id=environment_id,
            option_settings=option_settings,
            platform_arn=platform_arn,
            solution_stack_name=solution_stack_name,
            source_configuration=source_configuration,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bc320ee136dc067cd69a63bfbadaa5e097d79c96319e5f0d52a5f5a8bae0c75)
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
            type_hints = typing.get_type_hints(_typecheckingstub__be68f04ba4f61ee79f7d9b15c5e761ed331e27e14fe548ed5e71faeeec0f707a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrTemplateName")
    def attr_template_name(self) -> builtins.str:
        '''
        :cloudformationAttribute: TemplateName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrTemplateName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''The name of the Elastic Beanstalk application to associate with this configuration template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-applicationname
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))

    @application_name.setter
    def application_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8312fd6f68ad9e28182493201b59f28fd20e2e1dd242712cc9ddf05a84545fc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for this configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdd820e03b05ca5bae8070bf3e8c770eb870c68802f0e1cd5ccac14888d3031c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="environmentId")
    def environment_id(self) -> typing.Optional[builtins.str]:
        '''The ID of an environment whose settings you want to use to create the configuration template.

        You must specify ``EnvironmentId`` if you don't specify ``PlatformArn`` , ``SolutionStackName`` , or ``SourceConfiguration`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-environmentid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentId"))

    @environment_id.setter
    def environment_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa3345b8469826494180ae6e655e7214fc514c2fc9aed05ff036036be24ca72c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentId", value)

    @builtins.property
    @jsii.member(jsii_name="optionSettings")
    def option_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationTemplate.ConfigurationOptionSettingProperty"]]]]:
        '''Option values for the Elastic Beanstalk configuration, such as the instance type.

        If specified, these values override the values obtained from the solution stack or the source configuration template. For a complete list of Elastic Beanstalk configuration options, see `Option Values <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-optionsettings
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationTemplate.ConfigurationOptionSettingProperty"]]]], jsii.get(self, "optionSettings"))

    @option_settings.setter
    def option_settings(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationTemplate.ConfigurationOptionSettingProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a792131360cca96fb2cdbf9d168ee6eecd891195c7cfbaf0c41e3d23074b7efe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optionSettings", value)

    @builtins.property
    @jsii.member(jsii_name="platformArn")
    def platform_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the custom platform.

        For more information, see `Custom Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/custom-platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .
        .. epigraph::

           If you specify ``PlatformArn`` , then don't specify ``SolutionStackName`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-platformarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformArn"))

    @platform_arn.setter
    def platform_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5107f81bb2bc4835153729deab03ef79945fcc425899076627eb08c1b7943dee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platformArn", value)

    @builtins.property
    @jsii.member(jsii_name="solutionStackName")
    def solution_stack_name(self) -> typing.Optional[builtins.str]:
        '''The name of an Elastic Beanstalk solution stack (platform version) that this configuration uses.

        For example, ``64bit Amazon Linux 2013.09 running Tomcat 7 Java 7`` . A solution stack specifies the operating system, runtime, and application server for a configuration template. It also determines the set of configuration options as well as the possible and default values. For more information, see `Supported Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .

        You must specify ``SolutionStackName`` if you don't specify ``PlatformArn`` , ``EnvironmentId`` , or ``SourceConfiguration`` .

        Use the ```ListAvailableSolutionStacks`` <https://docs.aws.amazon.com/elasticbeanstalk/latest/api/API_ListAvailableSolutionStacks.html>`_ API to obtain a list of available solution stacks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-solutionstackname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "solutionStackName"))

    @solution_stack_name.setter
    def solution_stack_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70ffccfa2b69adb799007fbaca9c7ef40f9680321b2dc855dbf1e65109526d29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "solutionStackName", value)

    @builtins.property
    @jsii.member(jsii_name="sourceConfiguration")
    def source_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationTemplate.SourceConfigurationProperty"]]:
        '''An Elastic Beanstalk configuration template to base this one on.

        If specified, Elastic Beanstalk uses the configuration values from the specified configuration template to create a new configuration.

        Values specified in ``OptionSettings`` override any values obtained from the ``SourceConfiguration`` .

        You must specify ``SourceConfiguration`` if you don't specify ``PlatformArn`` , ``EnvironmentId`` , or ``SolutionStackName`` .

        Constraint: If both solution stack name and source configuration are specified, the solution stack of the source configuration template must match the specified solution stack name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-sourceconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationTemplate.SourceConfigurationProperty"]], jsii.get(self, "sourceConfiguration"))

    @source_configuration.setter
    def source_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnConfigurationTemplate.SourceConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76315e1c70da13be202fc33b80a3e41586e44aa2a482ce6123efcac01fe384f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sourceConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnConfigurationTemplate.ConfigurationOptionSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "namespace": "namespace",
            "option_name": "optionName",
            "resource_name": "resourceName",
            "value": "value",
        },
    )
    class ConfigurationOptionSettingProperty:
        def __init__(
            self,
            *,
            namespace: builtins.str,
            option_name: builtins.str,
            resource_name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the ``ConfigurationOptionSetting`` property type to specify an option for an AWS Elastic Beanstalk configuration template when defining an AWS::ElasticBeanstalk::ConfigurationTemplate resource in an AWS CloudFormation template.

            The ``ConfigurationOptionSetting`` property type specifies an option for an AWS Elastic Beanstalk configuration template.

            The ``OptionSettings`` property of the `AWS::ElasticBeanstalk::ConfigurationTemplate <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-beanstalk-configurationtemplate.html>`_ resource contains a list of ``ConfigurationOptionSetting`` property types.

            For a list of possible namespaces and option values, see `Option Values <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .

            :param namespace: A unique namespace that identifies the option's associated AWS resource.
            :param option_name: The name of the configuration option.
            :param resource_name: A unique resource name for the option setting. Use it for a time–based scaling configuration option.
            :param value: The current value for the configuration option.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
                
                configuration_option_setting_property = elasticbeanstalk.CfnConfigurationTemplate.ConfigurationOptionSettingProperty(
                    namespace="namespace",
                    option_name="optionName",
                
                    # the properties below are optional
                    resource_name="resourceName",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e7ed9bd915c392f2ba90ef87a4fd320bb34f5875de958c92b73d38ddd712721d)
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                check_type(argname="argument option_name", value=option_name, expected_type=type_hints["option_name"])
                check_type(argname="argument resource_name", value=resource_name, expected_type=type_hints["resource_name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "namespace": namespace,
                "option_name": option_name,
            }
            if resource_name is not None:
                self._values["resource_name"] = resource_name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def namespace(self) -> builtins.str:
            '''A unique namespace that identifies the option's associated AWS resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html#cfn-elasticbeanstalk-configurationtemplate-configurationoptionsetting-namespace
            '''
            result = self._values.get("namespace")
            assert result is not None, "Required property 'namespace' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def option_name(self) -> builtins.str:
            '''The name of the configuration option.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html#cfn-elasticbeanstalk-configurationtemplate-configurationoptionsetting-optionname
            '''
            result = self._values.get("option_name")
            assert result is not None, "Required property 'option_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def resource_name(self) -> typing.Optional[builtins.str]:
            '''A unique resource name for the option setting.

            Use it for a time–based scaling configuration option.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html#cfn-elasticbeanstalk-configurationtemplate-configurationoptionsetting-resourcename
            '''
            result = self._values.get("resource_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The current value for the configuration option.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-configurationoptionsetting.html#cfn-elasticbeanstalk-configurationtemplate-configurationoptionsetting-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ConfigurationOptionSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnConfigurationTemplate.SourceConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "application_name": "applicationName",
            "template_name": "templateName",
        },
    )
    class SourceConfigurationProperty:
        def __init__(
            self,
            *,
            application_name: builtins.str,
            template_name: builtins.str,
        ) -> None:
            '''Use the ``SourceConfiguration`` property type to specify another AWS Elastic Beanstalk configuration template as the base to creating a new AWS::ElasticBeanstalk::ConfigurationTemplate resource in an AWS CloudFormation template.

            An AWS Elastic Beanstalk configuration template to base a new one on. You can use it to define a `AWS::ElasticBeanstalk::ConfigurationTemplate <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-beanstalk-configurationtemplate.html>`_ resource.

            :param application_name: The name of the application associated with the configuration.
            :param template_name: The name of the configuration template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-sourceconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
                
                source_configuration_property = elasticbeanstalk.CfnConfigurationTemplate.SourceConfigurationProperty(
                    application_name="applicationName",
                    template_name="templateName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__516a51140dc59ce14236f442e109153f2f4b06ac35c0aed1940ef70ec03104ff)
                check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
                check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "application_name": application_name,
                "template_name": template_name,
            }

        @builtins.property
        def application_name(self) -> builtins.str:
            '''The name of the application associated with the configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-sourceconfiguration.html#cfn-elasticbeanstalk-configurationtemplate-sourceconfiguration-applicationname
            '''
            result = self._values.get("application_name")
            assert result is not None, "Required property 'application_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def template_name(self) -> builtins.str:
            '''The name of the configuration template.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-configurationtemplate-sourceconfiguration.html#cfn-elasticbeanstalk-configurationtemplate-sourceconfiguration-templatename
            '''
            result = self._values.get("template_name")
            assert result is not None, "Required property 'template_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SourceConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnConfigurationTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "description": "description",
        "environment_id": "environmentId",
        "option_settings": "optionSettings",
        "platform_arn": "platformArn",
        "solution_stack_name": "solutionStackName",
        "source_configuration": "sourceConfiguration",
    },
)
class CfnConfigurationTemplateProps:
    def __init__(
        self,
        *,
        application_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        environment_id: typing.Optional[builtins.str] = None,
        option_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationTemplate.ConfigurationOptionSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        platform_arn: typing.Optional[builtins.str] = None,
        solution_stack_name: typing.Optional[builtins.str] = None,
        source_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationTemplate.SourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnConfigurationTemplate``.

        :param application_name: The name of the Elastic Beanstalk application to associate with this configuration template.
        :param description: An optional description for this configuration.
        :param environment_id: The ID of an environment whose settings you want to use to create the configuration template. You must specify ``EnvironmentId`` if you don't specify ``PlatformArn`` , ``SolutionStackName`` , or ``SourceConfiguration`` .
        :param option_settings: Option values for the Elastic Beanstalk configuration, such as the instance type. If specified, these values override the values obtained from the solution stack or the source configuration template. For a complete list of Elastic Beanstalk configuration options, see `Option Values <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .
        :param platform_arn: The Amazon Resource Name (ARN) of the custom platform. For more information, see `Custom Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/custom-platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* . .. epigraph:: If you specify ``PlatformArn`` , then don't specify ``SolutionStackName`` .
        :param solution_stack_name: The name of an Elastic Beanstalk solution stack (platform version) that this configuration uses. For example, ``64bit Amazon Linux 2013.09 running Tomcat 7 Java 7`` . A solution stack specifies the operating system, runtime, and application server for a configuration template. It also determines the set of configuration options as well as the possible and default values. For more information, see `Supported Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* . You must specify ``SolutionStackName`` if you don't specify ``PlatformArn`` , ``EnvironmentId`` , or ``SourceConfiguration`` . Use the ```ListAvailableSolutionStacks`` <https://docs.aws.amazon.com/elasticbeanstalk/latest/api/API_ListAvailableSolutionStacks.html>`_ API to obtain a list of available solution stacks.
        :param source_configuration: An Elastic Beanstalk configuration template to base this one on. If specified, Elastic Beanstalk uses the configuration values from the specified configuration template to create a new configuration. Values specified in ``OptionSettings`` override any values obtained from the ``SourceConfiguration`` . You must specify ``SourceConfiguration`` if you don't specify ``PlatformArn`` , ``EnvironmentId`` , or ``SolutionStackName`` . Constraint: If both solution stack name and source configuration are specified, the solution stack of the source configuration template must match the specified solution stack name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
            
            cfn_configuration_template_props = elasticbeanstalk.CfnConfigurationTemplateProps(
                application_name="applicationName",
            
                # the properties below are optional
                description="description",
                environment_id="environmentId",
                option_settings=[elasticbeanstalk.CfnConfigurationTemplate.ConfigurationOptionSettingProperty(
                    namespace="namespace",
                    option_name="optionName",
            
                    # the properties below are optional
                    resource_name="resourceName",
                    value="value"
                )],
                platform_arn="platformArn",
                solution_stack_name="solutionStackName",
                source_configuration=elasticbeanstalk.CfnConfigurationTemplate.SourceConfigurationProperty(
                    application_name="applicationName",
                    template_name="templateName"
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__673eaabace306f1ca5c40ef9ff4bc35f465e4d5583a7a4c771c8b26d4c260c4e)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment_id", value=environment_id, expected_type=type_hints["environment_id"])
            check_type(argname="argument option_settings", value=option_settings, expected_type=type_hints["option_settings"])
            check_type(argname="argument platform_arn", value=platform_arn, expected_type=type_hints["platform_arn"])
            check_type(argname="argument solution_stack_name", value=solution_stack_name, expected_type=type_hints["solution_stack_name"])
            check_type(argname="argument source_configuration", value=source_configuration, expected_type=type_hints["source_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_name": application_name,
        }
        if description is not None:
            self._values["description"] = description
        if environment_id is not None:
            self._values["environment_id"] = environment_id
        if option_settings is not None:
            self._values["option_settings"] = option_settings
        if platform_arn is not None:
            self._values["platform_arn"] = platform_arn
        if solution_stack_name is not None:
            self._values["solution_stack_name"] = solution_stack_name
        if source_configuration is not None:
            self._values["source_configuration"] = source_configuration

    @builtins.property
    def application_name(self) -> builtins.str:
        '''The name of the Elastic Beanstalk application to associate with this configuration template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-applicationname
        '''
        result = self._values.get("application_name")
        assert result is not None, "Required property 'application_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''An optional description for this configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_id(self) -> typing.Optional[builtins.str]:
        '''The ID of an environment whose settings you want to use to create the configuration template.

        You must specify ``EnvironmentId`` if you don't specify ``PlatformArn`` , ``SolutionStackName`` , or ``SourceConfiguration`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-environmentid
        '''
        result = self._values.get("environment_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def option_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationTemplate.ConfigurationOptionSettingProperty]]]]:
        '''Option values for the Elastic Beanstalk configuration, such as the instance type.

        If specified, these values override the values obtained from the solution stack or the source configuration template. For a complete list of Elastic Beanstalk configuration options, see `Option Values <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-optionsettings
        '''
        result = self._values.get("option_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationTemplate.ConfigurationOptionSettingProperty]]]], result)

    @builtins.property
    def platform_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the custom platform.

        For more information, see `Custom Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/custom-platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .
        .. epigraph::

           If you specify ``PlatformArn`` , then don't specify ``SolutionStackName`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-platformarn
        '''
        result = self._values.get("platform_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def solution_stack_name(self) -> typing.Optional[builtins.str]:
        '''The name of an Elastic Beanstalk solution stack (platform version) that this configuration uses.

        For example, ``64bit Amazon Linux 2013.09 running Tomcat 7 Java 7`` . A solution stack specifies the operating system, runtime, and application server for a configuration template. It also determines the set of configuration options as well as the possible and default values. For more information, see `Supported Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/concepts.platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .

        You must specify ``SolutionStackName`` if you don't specify ``PlatformArn`` , ``EnvironmentId`` , or ``SourceConfiguration`` .

        Use the ```ListAvailableSolutionStacks`` <https://docs.aws.amazon.com/elasticbeanstalk/latest/api/API_ListAvailableSolutionStacks.html>`_ API to obtain a list of available solution stacks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-solutionstackname
        '''
        result = self._values.get("solution_stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def source_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationTemplate.SourceConfigurationProperty]]:
        '''An Elastic Beanstalk configuration template to base this one on.

        If specified, Elastic Beanstalk uses the configuration values from the specified configuration template to create a new configuration.

        Values specified in ``OptionSettings`` override any values obtained from the ``SourceConfiguration`` .

        You must specify ``SourceConfiguration`` if you don't specify ``PlatformArn`` , ``EnvironmentId`` , or ``SolutionStackName`` .

        Constraint: If both solution stack name and source configuration are specified, the solution stack of the source configuration template must match the specified solution stack name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-configurationtemplate.html#cfn-elasticbeanstalk-configurationtemplate-sourceconfiguration
        '''
        result = self._values.get("source_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationTemplate.SourceConfigurationProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnConfigurationTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnEnvironment(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnEnvironment",
):
    '''A CloudFormation ``AWS::ElasticBeanstalk::Environment``.

    Specify an AWS Elastic Beanstalk environment by using the AWS::ElasticBeanstalk::Environment resource in an AWS CloudFormation template.

    The AWS::ElasticBeanstalk::Environment resource is an AWS Elastic Beanstalk resource type that specifies an Elastic Beanstalk environment.

    :cloudformationResource: AWS::ElasticBeanstalk::Environment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
        
        cfn_environment = elasticbeanstalk.CfnEnvironment(self, "MyCfnEnvironment",
            application_name="applicationName",
        
            # the properties below are optional
            cname_prefix="cnamePrefix",
            description="description",
            environment_name="environmentName",
            operations_role="operationsRole",
            option_settings=[elasticbeanstalk.CfnEnvironment.OptionSettingProperty(
                namespace="namespace",
                option_name="optionName",
        
                # the properties below are optional
                resource_name="resourceName",
                value="value"
            )],
            platform_arn="platformArn",
            solution_stack_name="solutionStackName",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            template_name="templateName",
            tier=elasticbeanstalk.CfnEnvironment.TierProperty(
                name="name",
                type="type",
                version="version"
            ),
            version_label="versionLabel"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        application_name: builtins.str,
        cname_prefix: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        environment_name: typing.Optional[builtins.str] = None,
        operations_role: typing.Optional[builtins.str] = None,
        option_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEnvironment.OptionSettingProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        platform_arn: typing.Optional[builtins.str] = None,
        solution_stack_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        template_name: typing.Optional[builtins.str] = None,
        tier: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnEnvironment.TierProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        version_label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ElasticBeanstalk::Environment``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param application_name: The name of the application that is associated with this environment.
        :param cname_prefix: If specified, the environment attempts to use this value as the prefix for the CNAME in your Elastic Beanstalk environment URL. If not specified, the CNAME is generated automatically by appending a random alphanumeric string to the environment name.
        :param description: Your description for this environment.
        :param environment_name: A unique name for the environment. Constraint: Must be from 4 to 40 characters in length. The name can contain only letters, numbers, and hyphens. It can't start or end with a hyphen. This name must be unique within a region in your account. If you don't specify the ``CNAMEPrefix`` parameter, the environment name becomes part of the CNAME, and therefore part of the visible URL for your application. If you don't specify an environment name, AWS CloudFormation generates a unique physical ID and uses that ID for the environment name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param operations_role: .. epigraph:: The operations role feature of AWS Elastic Beanstalk is in beta release and is subject to change. The Amazon Resource Name (ARN) of an existing IAM role to be used as the environment's operations role. If specified, Elastic Beanstalk uses the operations role for permissions to downstream services during this call and during subsequent calls acting on this environment. To specify an operations role, you must have the ``iam:PassRole`` permission for the role.
        :param option_settings: Key-value pairs defining configuration options for this environment, such as the instance type. These options override the values that are defined in the solution stack or the `configuration template <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-beanstalk-configurationtemplate.html>`_ . If you remove any options during a stack update, the removed options retain their current values.
        :param platform_arn: The Amazon Resource Name (ARN) of the custom platform to use with the environment. For more information, see `Custom Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/custom-platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* . .. epigraph:: If you specify ``PlatformArn`` , don't specify ``SolutionStackName`` .
        :param solution_stack_name: The name of an Elastic Beanstalk solution stack (platform version) to use with the environment. If specified, Elastic Beanstalk sets the configuration values to the default values associated with the specified solution stack. For a list of current solution stacks, see `Elastic Beanstalk Supported Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/platforms/platforms-supported.html>`_ in the *AWS Elastic Beanstalk Platforms* guide. .. epigraph:: If you specify ``SolutionStackName`` , don't specify ``PlatformArn`` or ``TemplateName`` .
        :param tags: Specifies the tags applied to resources in the environment.
        :param template_name: The name of the Elastic Beanstalk configuration template to use with the environment. .. epigraph:: If you specify ``TemplateName`` , then don't specify ``SolutionStackName`` .
        :param tier: Specifies the tier to use in creating this environment. The environment tier that you choose determines whether Elastic Beanstalk provisions resources to support a web application that handles HTTP(S) requests or a web application that handles background-processing tasks.
        :param version_label: The name of the application version to deploy. Default: If not specified, Elastic Beanstalk attempts to deploy the sample application.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd82bdb939ddb300d8cae67b7a415095eb46d5ead6b633c4a41e3bb306a9b0c4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnEnvironmentProps(
            application_name=application_name,
            cname_prefix=cname_prefix,
            description=description,
            environment_name=environment_name,
            operations_role=operations_role,
            option_settings=option_settings,
            platform_arn=platform_arn,
            solution_stack_name=solution_stack_name,
            tags=tags,
            template_name=template_name,
            tier=tier,
            version_label=version_label,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eff692e81664cbd12ada06eb6aa8641b77155d01b241e2350e04210871e3d260)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f6bdc36f82f312095553c8af004dd9a1399e7fd10f15aba9c57718ac9bdb4f77)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrEndpointUrl")
    def attr_endpoint_url(self) -> builtins.str:
        '''For load-balanced, autoscaling environments, the URL to the load balancer. For single-instance environments, the IP address of the instance.

        Example load balancer URL:

        Example instance IP address:

        ``192.0.2.0``

        :cloudformationAttribute: EndpointURL
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrEndpointUrl"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Specifies the tags applied to resources in the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="applicationName")
    def application_name(self) -> builtins.str:
        '''The name of the application that is associated with this environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-applicationname
        '''
        return typing.cast(builtins.str, jsii.get(self, "applicationName"))

    @application_name.setter
    def application_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d7ff5cc1c64e13202db8d14b80d23a7c4ee46b7c9b6c5887631e5c6f38427a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "applicationName", value)

    @builtins.property
    @jsii.member(jsii_name="cnamePrefix")
    def cname_prefix(self) -> typing.Optional[builtins.str]:
        '''If specified, the environment attempts to use this value as the prefix for the CNAME in your Elastic Beanstalk environment URL.

        If not specified, the CNAME is generated automatically by appending a random alphanumeric string to the environment name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-cnameprefix
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cnamePrefix"))

    @cname_prefix.setter
    def cname_prefix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19cf417b5549ebe7f3adff69f8ef2a067477e9863edbcc991ad7863cd3d1f6df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cnamePrefix", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''Your description for this environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b590d39715a042f69b3f11afdd78670622b676821fd5b30363667d02207ee03c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="environmentName")
    def environment_name(self) -> typing.Optional[builtins.str]:
        '''A unique name for the environment.

        Constraint: Must be from 4 to 40 characters in length. The name can contain only letters, numbers, and hyphens. It can't start or end with a hyphen. This name must be unique within a region in your account.

        If you don't specify the ``CNAMEPrefix`` parameter, the environment name becomes part of the CNAME, and therefore part of the visible URL for your application.

        If you don't specify an environment name, AWS CloudFormation generates a unique physical ID and uses that ID for the environment name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-environmentname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "environmentName"))

    @environment_name.setter
    def environment_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__589b899b691b9aaffd26e0d6099bdd2bb01504b4f27f0c70df7bab3723fe71a4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentName", value)

    @builtins.property
    @jsii.member(jsii_name="operationsRole")
    def operations_role(self) -> typing.Optional[builtins.str]:
        '''.. epigraph::

   The operations role feature of AWS Elastic Beanstalk is in beta release and is subject to change.

        The Amazon Resource Name (ARN) of an existing IAM role to be used as the environment's operations role. If specified, Elastic Beanstalk uses the operations role for permissions to downstream services during this call and during subsequent calls acting on this environment. To specify an operations role, you must have the ``iam:PassRole`` permission for the role.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-operationsrole
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationsRole"))

    @operations_role.setter
    def operations_role(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7669b58d9564fb4dec7bb17602126e4a581bc6e5bdfbcf5a0e883905b43c6dfa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationsRole", value)

    @builtins.property
    @jsii.member(jsii_name="optionSettings")
    def option_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.OptionSettingProperty"]]]]:
        '''Key-value pairs defining configuration options for this environment, such as the instance type.

        These options override the values that are defined in the solution stack or the `configuration template <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-beanstalk-configurationtemplate.html>`_ . If you remove any options during a stack update, the removed options retain their current values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-optionsettings
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.OptionSettingProperty"]]]], jsii.get(self, "optionSettings"))

    @option_settings.setter
    def option_settings(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.OptionSettingProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c22949fd6a589bb469af7a02ca95ca40bea094a74306215a6fc583c2fa0ed60e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "optionSettings", value)

    @builtins.property
    @jsii.member(jsii_name="platformArn")
    def platform_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the custom platform to use with the environment.

        For more information, see `Custom Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/custom-platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .
        .. epigraph::

           If you specify ``PlatformArn`` , don't specify ``SolutionStackName`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-platformarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platformArn"))

    @platform_arn.setter
    def platform_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e2d2818a7075f3215cca2a26f103f38b040f0d3bba4eb7c0c8bc201574a00fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platformArn", value)

    @builtins.property
    @jsii.member(jsii_name="solutionStackName")
    def solution_stack_name(self) -> typing.Optional[builtins.str]:
        '''The name of an Elastic Beanstalk solution stack (platform version) to use with the environment.

        If specified, Elastic Beanstalk sets the configuration values to the default values associated with the specified solution stack. For a list of current solution stacks, see `Elastic Beanstalk Supported Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/platforms/platforms-supported.html>`_ in the *AWS Elastic Beanstalk Platforms* guide.
        .. epigraph::

           If you specify ``SolutionStackName`` , don't specify ``PlatformArn`` or ``TemplateName`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-solutionstackname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "solutionStackName"))

    @solution_stack_name.setter
    def solution_stack_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b83fe792c163a2a7a3ba99cdf8378f0b4cb5b017f3a0aaa4838a6df2d82af0e2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "solutionStackName", value)

    @builtins.property
    @jsii.member(jsii_name="templateName")
    def template_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Elastic Beanstalk configuration template to use with the environment.

        .. epigraph::

           If you specify ``TemplateName`` , then don't specify ``SolutionStackName`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-templatename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateName"))

    @template_name.setter
    def template_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30aead1d0fd60a43759e5007c3169feb4e1c4da1ba204ee0ee709c35780b115d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "templateName", value)

    @builtins.property
    @jsii.member(jsii_name="tier")
    def tier(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.TierProperty"]]:
        '''Specifies the tier to use in creating this environment.

        The environment tier that you choose determines whether Elastic Beanstalk provisions resources to support a web application that handles HTTP(S) requests or a web application that handles background-processing tasks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-tier
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.TierProperty"]], jsii.get(self, "tier"))

    @tier.setter
    def tier(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnEnvironment.TierProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d3770e268f2afcbf3c05eaaf0a4c1514a60bf11120bf94b7bd6440c2d2246c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tier", value)

    @builtins.property
    @jsii.member(jsii_name="versionLabel")
    def version_label(self) -> typing.Optional[builtins.str]:
        '''The name of the application version to deploy.

        Default: If not specified, Elastic Beanstalk attempts to deploy the sample application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-versionlabel
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "versionLabel"))

    @version_label.setter
    def version_label(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44a22efa88f05b193bdc1b3835196a712cab2cc124faf3d3bb6ea5ffbf26d99e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "versionLabel", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnEnvironment.OptionSettingProperty",
        jsii_struct_bases=[],
        name_mapping={
            "namespace": "namespace",
            "option_name": "optionName",
            "resource_name": "resourceName",
            "value": "value",
        },
    )
    class OptionSettingProperty:
        def __init__(
            self,
            *,
            namespace: builtins.str,
            option_name: builtins.str,
            resource_name: typing.Optional[builtins.str] = None,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the ``OptionSetting`` property type to specify an option for an AWS Elastic Beanstalk environment when defining an AWS::ElasticBeanstalk::Environment resource in an AWS CloudFormation template.

            The ``OptionSetting`` property type specifies an option for an AWS Elastic Beanstalk environment.

            The ``OptionSettings`` property of the `AWS::ElasticBeanstalk::Environment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html>`_ resource contains a list of ``OptionSetting`` property types.

            For a list of possible namespaces and option values, see `Option Values <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/command-options.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .

            :param namespace: A unique namespace that identifies the option's associated AWS resource.
            :param option_name: The name of the configuration option.
            :param resource_name: A unique resource name for the option setting. Use it for a time–based scaling configuration option.
            :param value: The current value for the configuration option.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-optionsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
                
                option_setting_property = elasticbeanstalk.CfnEnvironment.OptionSettingProperty(
                    namespace="namespace",
                    option_name="optionName",
                
                    # the properties below are optional
                    resource_name="resourceName",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3caa421814ab1ec8baa106bb0ad5fe9058caffa54e416d71a3f78a5d7baf8fa)
                check_type(argname="argument namespace", value=namespace, expected_type=type_hints["namespace"])
                check_type(argname="argument option_name", value=option_name, expected_type=type_hints["option_name"])
                check_type(argname="argument resource_name", value=resource_name, expected_type=type_hints["resource_name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "namespace": namespace,
                "option_name": option_name,
            }
            if resource_name is not None:
                self._values["resource_name"] = resource_name
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def namespace(self) -> builtins.str:
            '''A unique namespace that identifies the option's associated AWS resource.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-optionsetting.html#cfn-elasticbeanstalk-environment-optionsetting-namespace
            '''
            result = self._values.get("namespace")
            assert result is not None, "Required property 'namespace' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def option_name(self) -> builtins.str:
            '''The name of the configuration option.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-optionsetting.html#cfn-elasticbeanstalk-environment-optionsetting-optionname
            '''
            result = self._values.get("option_name")
            assert result is not None, "Required property 'option_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def resource_name(self) -> typing.Optional[builtins.str]:
            '''A unique resource name for the option setting.

            Use it for a time–based scaling configuration option.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-optionsetting.html#cfn-elasticbeanstalk-environment-optionsetting-resourcename
            '''
            result = self._values.get("resource_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The current value for the configuration option.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-optionsetting.html#cfn-elasticbeanstalk-environment-optionsetting-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "OptionSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnEnvironment.TierProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "type": "type", "version": "version"},
    )
    class TierProperty:
        def __init__(
            self,
            *,
            name: typing.Optional[builtins.str] = None,
            type: typing.Optional[builtins.str] = None,
            version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the ``Tier`` property type to specify the environment tier for an AWS Elastic Beanstalk environment when defining an AWS::ElasticBeanstalk::Environment resource in an AWS CloudFormation template.

            Describes the environment tier for an `AWS::ElasticBeanstalk::Environment <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-beanstalk-environment.html>`_ resource. For more information, see `Environment Tiers <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/using-features-managing-env-tiers.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .

            :param name: The name of this environment tier. Valid values: - For *Web server tier* – ``WebServer`` - For *Worker tier* – ``Worker``
            :param type: The type of this environment tier. Valid values: - For *Web server tier* – ``Standard`` - For *Worker tier* – ``SQS/HTTP``
            :param version: The version of this environment tier. When you don't set a value to it, Elastic Beanstalk uses the latest compatible worker tier version. .. epigraph:: This member is deprecated. Any specific version that you set may become out of date. We recommend leaving it unspecified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-tier.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
                
                tier_property = elasticbeanstalk.CfnEnvironment.TierProperty(
                    name="name",
                    type="type",
                    version="version"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__354beba4ff35b61b32b06405242acc05952f32f8fffe367cb3c0826de338fba5)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if name is not None:
                self._values["name"] = name
            if type is not None:
                self._values["type"] = type
            if version is not None:
                self._values["version"] = version

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of this environment tier.

            Valid values:

            - For *Web server tier* – ``WebServer``
            - For *Worker tier* – ``Worker``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-tier.html#cfn-elasticbeanstalk-environment-tier-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def type(self) -> typing.Optional[builtins.str]:
            '''The type of this environment tier.

            Valid values:

            - For *Web server tier* – ``Standard``
            - For *Worker tier* – ``SQS/HTTP``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-tier.html#cfn-elasticbeanstalk-environment-tier-type
            '''
            result = self._values.get("type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def version(self) -> typing.Optional[builtins.str]:
            '''The version of this environment tier.

            When you don't set a value to it, Elastic Beanstalk uses the latest compatible worker tier version.
            .. epigraph::

               This member is deprecated. Any specific version that you set may become out of date. We recommend leaving it unspecified.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticbeanstalk-environment-tier.html#cfn-elasticbeanstalk-environment-tier-version
            '''
            result = self._values.get("version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TierProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-elasticbeanstalk.CfnEnvironmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "application_name": "applicationName",
        "cname_prefix": "cnamePrefix",
        "description": "description",
        "environment_name": "environmentName",
        "operations_role": "operationsRole",
        "option_settings": "optionSettings",
        "platform_arn": "platformArn",
        "solution_stack_name": "solutionStackName",
        "tags": "tags",
        "template_name": "templateName",
        "tier": "tier",
        "version_label": "versionLabel",
    },
)
class CfnEnvironmentProps:
    def __init__(
        self,
        *,
        application_name: builtins.str,
        cname_prefix: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        environment_name: typing.Optional[builtins.str] = None,
        operations_role: typing.Optional[builtins.str] = None,
        option_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEnvironment.OptionSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        platform_arn: typing.Optional[builtins.str] = None,
        solution_stack_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        template_name: typing.Optional[builtins.str] = None,
        tier: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEnvironment.TierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        version_label: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnEnvironment``.

        :param application_name: The name of the application that is associated with this environment.
        :param cname_prefix: If specified, the environment attempts to use this value as the prefix for the CNAME in your Elastic Beanstalk environment URL. If not specified, the CNAME is generated automatically by appending a random alphanumeric string to the environment name.
        :param description: Your description for this environment.
        :param environment_name: A unique name for the environment. Constraint: Must be from 4 to 40 characters in length. The name can contain only letters, numbers, and hyphens. It can't start or end with a hyphen. This name must be unique within a region in your account. If you don't specify the ``CNAMEPrefix`` parameter, the environment name becomes part of the CNAME, and therefore part of the visible URL for your application. If you don't specify an environment name, AWS CloudFormation generates a unique physical ID and uses that ID for the environment name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ . .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.
        :param operations_role: .. epigraph:: The operations role feature of AWS Elastic Beanstalk is in beta release and is subject to change. The Amazon Resource Name (ARN) of an existing IAM role to be used as the environment's operations role. If specified, Elastic Beanstalk uses the operations role for permissions to downstream services during this call and during subsequent calls acting on this environment. To specify an operations role, you must have the ``iam:PassRole`` permission for the role.
        :param option_settings: Key-value pairs defining configuration options for this environment, such as the instance type. These options override the values that are defined in the solution stack or the `configuration template <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-beanstalk-configurationtemplate.html>`_ . If you remove any options during a stack update, the removed options retain their current values.
        :param platform_arn: The Amazon Resource Name (ARN) of the custom platform to use with the environment. For more information, see `Custom Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/custom-platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* . .. epigraph:: If you specify ``PlatformArn`` , don't specify ``SolutionStackName`` .
        :param solution_stack_name: The name of an Elastic Beanstalk solution stack (platform version) to use with the environment. If specified, Elastic Beanstalk sets the configuration values to the default values associated with the specified solution stack. For a list of current solution stacks, see `Elastic Beanstalk Supported Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/platforms/platforms-supported.html>`_ in the *AWS Elastic Beanstalk Platforms* guide. .. epigraph:: If you specify ``SolutionStackName`` , don't specify ``PlatformArn`` or ``TemplateName`` .
        :param tags: Specifies the tags applied to resources in the environment.
        :param template_name: The name of the Elastic Beanstalk configuration template to use with the environment. .. epigraph:: If you specify ``TemplateName`` , then don't specify ``SolutionStackName`` .
        :param tier: Specifies the tier to use in creating this environment. The environment tier that you choose determines whether Elastic Beanstalk provisions resources to support a web application that handles HTTP(S) requests or a web application that handles background-processing tasks.
        :param version_label: The name of the application version to deploy. Default: If not specified, Elastic Beanstalk attempts to deploy the sample application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_elasticbeanstalk as elasticbeanstalk
            
            cfn_environment_props = elasticbeanstalk.CfnEnvironmentProps(
                application_name="applicationName",
            
                # the properties below are optional
                cname_prefix="cnamePrefix",
                description="description",
                environment_name="environmentName",
                operations_role="operationsRole",
                option_settings=[elasticbeanstalk.CfnEnvironment.OptionSettingProperty(
                    namespace="namespace",
                    option_name="optionName",
            
                    # the properties below are optional
                    resource_name="resourceName",
                    value="value"
                )],
                platform_arn="platformArn",
                solution_stack_name="solutionStackName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                template_name="templateName",
                tier=elasticbeanstalk.CfnEnvironment.TierProperty(
                    name="name",
                    type="type",
                    version="version"
                ),
                version_label="versionLabel"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72169ac4e7bfb32f629dfa419bb5b2e89c9996ad0a8980ca0f0fe39a19a68a64)
            check_type(argname="argument application_name", value=application_name, expected_type=type_hints["application_name"])
            check_type(argname="argument cname_prefix", value=cname_prefix, expected_type=type_hints["cname_prefix"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment_name", value=environment_name, expected_type=type_hints["environment_name"])
            check_type(argname="argument operations_role", value=operations_role, expected_type=type_hints["operations_role"])
            check_type(argname="argument option_settings", value=option_settings, expected_type=type_hints["option_settings"])
            check_type(argname="argument platform_arn", value=platform_arn, expected_type=type_hints["platform_arn"])
            check_type(argname="argument solution_stack_name", value=solution_stack_name, expected_type=type_hints["solution_stack_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_name", value=template_name, expected_type=type_hints["template_name"])
            check_type(argname="argument tier", value=tier, expected_type=type_hints["tier"])
            check_type(argname="argument version_label", value=version_label, expected_type=type_hints["version_label"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "application_name": application_name,
        }
        if cname_prefix is not None:
            self._values["cname_prefix"] = cname_prefix
        if description is not None:
            self._values["description"] = description
        if environment_name is not None:
            self._values["environment_name"] = environment_name
        if operations_role is not None:
            self._values["operations_role"] = operations_role
        if option_settings is not None:
            self._values["option_settings"] = option_settings
        if platform_arn is not None:
            self._values["platform_arn"] = platform_arn
        if solution_stack_name is not None:
            self._values["solution_stack_name"] = solution_stack_name
        if tags is not None:
            self._values["tags"] = tags
        if template_name is not None:
            self._values["template_name"] = template_name
        if tier is not None:
            self._values["tier"] = tier
        if version_label is not None:
            self._values["version_label"] = version_label

    @builtins.property
    def application_name(self) -> builtins.str:
        '''The name of the application that is associated with this environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-applicationname
        '''
        result = self._values.get("application_name")
        assert result is not None, "Required property 'application_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cname_prefix(self) -> typing.Optional[builtins.str]:
        '''If specified, the environment attempts to use this value as the prefix for the CNAME in your Elastic Beanstalk environment URL.

        If not specified, the CNAME is generated automatically by appending a random alphanumeric string to the environment name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-cnameprefix
        '''
        result = self._values.get("cname_prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Your description for this environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_name(self) -> typing.Optional[builtins.str]:
        '''A unique name for the environment.

        Constraint: Must be from 4 to 40 characters in length. The name can contain only letters, numbers, and hyphens. It can't start or end with a hyphen. This name must be unique within a region in your account.

        If you don't specify the ``CNAMEPrefix`` parameter, the environment name becomes part of the CNAME, and therefore part of the visible URL for your application.

        If you don't specify an environment name, AWS CloudFormation generates a unique physical ID and uses that ID for the environment name. For more information, see `Name Type <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-name.html>`_ .
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-environmentname
        '''
        result = self._values.get("environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operations_role(self) -> typing.Optional[builtins.str]:
        '''.. epigraph::

   The operations role feature of AWS Elastic Beanstalk is in beta release and is subject to change.

        The Amazon Resource Name (ARN) of an existing IAM role to be used as the environment's operations role. If specified, Elastic Beanstalk uses the operations role for permissions to downstream services during this call and during subsequent calls acting on this environment. To specify an operations role, you must have the ``iam:PassRole`` permission for the role.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-operationsrole
        '''
        result = self._values.get("operations_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def option_settings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEnvironment.OptionSettingProperty]]]]:
        '''Key-value pairs defining configuration options for this environment, such as the instance type.

        These options override the values that are defined in the solution stack or the `configuration template <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-beanstalk-configurationtemplate.html>`_ . If you remove any options during a stack update, the removed options retain their current values.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-optionsettings
        '''
        result = self._values.get("option_settings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEnvironment.OptionSettingProperty]]]], result)

    @builtins.property
    def platform_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the custom platform to use with the environment.

        For more information, see `Custom Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/custom-platforms.html>`_ in the *AWS Elastic Beanstalk Developer Guide* .
        .. epigraph::

           If you specify ``PlatformArn`` , don't specify ``SolutionStackName`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-platformarn
        '''
        result = self._values.get("platform_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def solution_stack_name(self) -> typing.Optional[builtins.str]:
        '''The name of an Elastic Beanstalk solution stack (platform version) to use with the environment.

        If specified, Elastic Beanstalk sets the configuration values to the default values associated with the specified solution stack. For a list of current solution stacks, see `Elastic Beanstalk Supported Platforms <https://docs.aws.amazon.com/elasticbeanstalk/latest/platforms/platforms-supported.html>`_ in the *AWS Elastic Beanstalk Platforms* guide.
        .. epigraph::

           If you specify ``SolutionStackName`` , don't specify ``PlatformArn`` or ``TemplateName`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-solutionstackname
        '''
        result = self._values.get("solution_stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Specifies the tags applied to resources in the environment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def template_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Elastic Beanstalk configuration template to use with the environment.

        .. epigraph::

           If you specify ``TemplateName`` , then don't specify ``SolutionStackName`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-templatename
        '''
        result = self._values.get("template_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tier(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEnvironment.TierProperty]]:
        '''Specifies the tier to use in creating this environment.

        The environment tier that you choose determines whether Elastic Beanstalk provisions resources to support a web application that handles HTTP(S) requests or a web application that handles background-processing tasks.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-tier
        '''
        result = self._values.get("tier")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEnvironment.TierProperty]], result)

    @builtins.property
    def version_label(self) -> typing.Optional[builtins.str]:
        '''The name of the application version to deploy.

        Default: If not specified, Elastic Beanstalk attempts to deploy the sample application.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticbeanstalk-environment.html#cfn-elasticbeanstalk-environment-versionlabel
        '''
        result = self._values.get("version_label")
        return typing.cast(typing.Optional[builtins.str], result)

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
    "CfnApplicationVersion",
    "CfnApplicationVersionProps",
    "CfnConfigurationTemplate",
    "CfnConfigurationTemplateProps",
    "CfnEnvironment",
    "CfnEnvironmentProps",
]

publication.publish()

def _typecheckingstub__034105bd0cefe052895f317e28891c732c15652c08f71b0c275d1038aa1e3458(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    resource_lifecycle_config: typing.Optional[typing.Union[typing.Union[CfnApplication.ApplicationResourceLifecycleConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47e1e7cf51bdc9ea6861173db70e678eeb3285de55a8a515a7cf0d3f01ab165a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e12f018b5d1cf84349164323ec91f760fb50747650c5b8cb89896d6f15d802b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ce93feb3c7bf7ad89cc9985bbf659227ad9ff6c1bfebfc597ead0370aafdd67(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf8d7e3d580f006280c47743dfd2397d50e82a3353c666d7cd249ca431c9521c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9b53d79a6cc8d489f18e895c643da8a6ecf2a916701b5054eefdf0d464e1886(
    value: typing.Optional[typing.Union[CfnApplication.ApplicationResourceLifecycleConfigProperty, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72472b75c094b78f2cedf0f4e7b8ccdccdc8ffa87143fe834efd5aebffb11548(
    *,
    service_role: typing.Optional[builtins.str] = None,
    version_lifecycle_config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.ApplicationVersionLifecycleConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e98bafdfb57cc5a70f564ca23681288e262b3b593732da552e0e9b134f19644(
    *,
    max_age_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.MaxAgeRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    max_count_rule: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplication.MaxCountRuleProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5cd4098968a38f97924ebb79570bf55af9105bcc4b67d4ec0137fd6d3009f04(
    *,
    delete_source_from_s3: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    max_age_in_days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__109bde59813451cf34d1c65e04d22aee5232c87265e53eae42a0f06a462c27e2(
    *,
    delete_source_from_s3: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    max_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a40c3bb2c0b1ec12fd0f7c123f331e2c43b51e25c47d0f6638eceaa3467cb5(
    *,
    application_name: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    resource_lifecycle_config: typing.Optional[typing.Union[typing.Union[CfnApplication.ApplicationResourceLifecycleConfigProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7c1a7d7f27ecf5d3f16e76851c4186826da354d92e1ce8b6abe31f30583dcf8(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_name: builtins.str,
    source_bundle: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplicationVersion.SourceBundleProperty, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662fc9c7a217e4e1568491fd70d10889489ccd8d3a994280639adcf78e088aef(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__672a989ccfd7a09a8fa5b959034ecbdef6446449b20f58d9830cac44c6c2a6bc(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b4f4db14743af26f27cf782a662ae30ee0938b589cc23c168c0f549afd1c4afa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36d1e8f49e32d13b6276359e1c22975fbe188870d8a3b7620f992d6e3ba1d2ac(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnApplicationVersion.SourceBundleProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acf73c9d98c5a6f70d8785eab5fe8479e840180d0c144a0d0bbd8c8cfd344215(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e12e1dd170d479c5a0df103ec6c5ffedfbaeb9b515fce23e0fce2a2767591862(
    *,
    s3_bucket: builtins.str,
    s3_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11337e3be6c4f378c37f54cf366f6fa18de148aa667f2772ac816b9161c7fe29(
    *,
    application_name: builtins.str,
    source_bundle: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnApplicationVersion.SourceBundleProperty, typing.Dict[builtins.str, typing.Any]]],
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0e2c832e2ae2d269f27d0c11de12693f64bffa03e9d84b14b0856a530b31ee(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    environment_id: typing.Optional[builtins.str] = None,
    option_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationTemplate.ConfigurationOptionSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    platform_arn: typing.Optional[builtins.str] = None,
    solution_stack_name: typing.Optional[builtins.str] = None,
    source_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationTemplate.SourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bc320ee136dc067cd69a63bfbadaa5e097d79c96319e5f0d52a5f5a8bae0c75(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be68f04ba4f61ee79f7d9b15c5e761ed331e27e14fe548ed5e71faeeec0f707a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8312fd6f68ad9e28182493201b59f28fd20e2e1dd242712cc9ddf05a84545fc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdd820e03b05ca5bae8070bf3e8c770eb870c68802f0e1cd5ccac14888d3031c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa3345b8469826494180ae6e655e7214fc514c2fc9aed05ff036036be24ca72c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a792131360cca96fb2cdbf9d168ee6eecd891195c7cfbaf0c41e3d23074b7efe(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationTemplate.ConfigurationOptionSettingProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5107f81bb2bc4835153729deab03ef79945fcc425899076627eb08c1b7943dee(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70ffccfa2b69adb799007fbaca9c7ef40f9680321b2dc855dbf1e65109526d29(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76315e1c70da13be202fc33b80a3e41586e44aa2a482ce6123efcac01fe384f1(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnConfigurationTemplate.SourceConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7ed9bd915c392f2ba90ef87a4fd320bb34f5875de958c92b73d38ddd712721d(
    *,
    namespace: builtins.str,
    option_name: builtins.str,
    resource_name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__516a51140dc59ce14236f442e109153f2f4b06ac35c0aed1940ef70ec03104ff(
    *,
    application_name: builtins.str,
    template_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__673eaabace306f1ca5c40ef9ff4bc35f465e4d5583a7a4c771c8b26d4c260c4e(
    *,
    application_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    environment_id: typing.Optional[builtins.str] = None,
    option_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationTemplate.ConfigurationOptionSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    platform_arn: typing.Optional[builtins.str] = None,
    solution_stack_name: typing.Optional[builtins.str] = None,
    source_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnConfigurationTemplate.SourceConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd82bdb939ddb300d8cae67b7a415095eb46d5ead6b633c4a41e3bb306a9b0c4(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    application_name: builtins.str,
    cname_prefix: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    environment_name: typing.Optional[builtins.str] = None,
    operations_role: typing.Optional[builtins.str] = None,
    option_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEnvironment.OptionSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    platform_arn: typing.Optional[builtins.str] = None,
    solution_stack_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    template_name: typing.Optional[builtins.str] = None,
    tier: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEnvironment.TierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    version_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eff692e81664cbd12ada06eb6aa8641b77155d01b241e2350e04210871e3d260(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6bdc36f82f312095553c8af004dd9a1399e7fd10f15aba9c57718ac9bdb4f77(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d7ff5cc1c64e13202db8d14b80d23a7c4ee46b7c9b6c5887631e5c6f38427a3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19cf417b5549ebe7f3adff69f8ef2a067477e9863edbcc991ad7863cd3d1f6df(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b590d39715a042f69b3f11afdd78670622b676821fd5b30363667d02207ee03c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__589b899b691b9aaffd26e0d6099bdd2bb01504b4f27f0c70df7bab3723fe71a4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7669b58d9564fb4dec7bb17602126e4a581bc6e5bdfbcf5a0e883905b43c6dfa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c22949fd6a589bb469af7a02ca95ca40bea094a74306215a6fc583c2fa0ed60e(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEnvironment.OptionSettingProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e2d2818a7075f3215cca2a26f103f38b040f0d3bba4eb7c0c8bc201574a00fd(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b83fe792c163a2a7a3ba99cdf8378f0b4cb5b017f3a0aaa4838a6df2d82af0e2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30aead1d0fd60a43759e5007c3169feb4e1c4da1ba204ee0ee709c35780b115d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d3770e268f2afcbf3c05eaaf0a4c1514a60bf11120bf94b7bd6440c2d2246c1(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnEnvironment.TierProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44a22efa88f05b193bdc1b3835196a712cab2cc124faf3d3bb6ea5ffbf26d99e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3caa421814ab1ec8baa106bb0ad5fe9058caffa54e416d71a3f78a5d7baf8fa(
    *,
    namespace: builtins.str,
    option_name: builtins.str,
    resource_name: typing.Optional[builtins.str] = None,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__354beba4ff35b61b32b06405242acc05952f32f8fffe367cb3c0826de338fba5(
    *,
    name: typing.Optional[builtins.str] = None,
    type: typing.Optional[builtins.str] = None,
    version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72169ac4e7bfb32f629dfa419bb5b2e89c9996ad0a8980ca0f0fe39a19a68a64(
    *,
    application_name: builtins.str,
    cname_prefix: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    environment_name: typing.Optional[builtins.str] = None,
    operations_role: typing.Optional[builtins.str] = None,
    option_settings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEnvironment.OptionSettingProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    platform_arn: typing.Optional[builtins.str] = None,
    solution_stack_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    template_name: typing.Optional[builtins.str] = None,
    tier: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnEnvironment.TierProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    version_label: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
