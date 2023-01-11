'''
# Amazon Inspector Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_inspector as inspector
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for Inspector construct libraries](https://constructs.dev/search?q=inspector)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::Inspector resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Inspector.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::Inspector](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_Inspector.html).

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
class CfnAssessmentTarget(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-inspector.CfnAssessmentTarget",
):
    '''A CloudFormation ``AWS::Inspector::AssessmentTarget``.

    The ``AWS::Inspector::AssessmentTarget`` resource is used to create Amazon Inspector assessment targets, which specify the Amazon EC2 instances that will be analyzed during an assessment run.

    :cloudformationResource: AWS::Inspector::AssessmentTarget
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_inspector as inspector
        
        cfn_assessment_target = inspector.CfnAssessmentTarget(self, "MyCfnAssessmentTarget",
            assessment_target_name="assessmentTargetName",
            resource_group_arn="resourceGroupArn"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        assessment_target_name: typing.Optional[builtins.str] = None,
        resource_group_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Inspector::AssessmentTarget``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param assessment_target_name: The name of the Amazon Inspector assessment target. The name must be unique within the AWS account .
        :param resource_group_arn: The ARN that specifies the resource group that is used to create the assessment target. If ``resourceGroupArn`` is not specified, all EC2 instances in the current AWS account and Region are included in the assessment target.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2098595cd6e90804bdf42e9aaa8581983888e5f21789e5e8055df2f6d457c11)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAssessmentTargetProps(
            assessment_target_name=assessment_target_name,
            resource_group_arn=resource_group_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f81e73f2178b215f62b276482081748ebaeb68fe1cc3cbe771495fafbf327f90)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cc7b08bdfe2eccdb2ef287f8c16d3a0dd28150b726350efa7da0bb51c69e621c)
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
        '''The Amazon Resource Name (ARN) that specifies the assessment target that is created.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="assessmentTargetName")
    def assessment_target_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Amazon Inspector assessment target.

        The name must be unique within the AWS account .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html#cfn-inspector-assessmenttarget-assessmenttargetname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assessmentTargetName"))

    @assessment_target_name.setter
    def assessment_target_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7329abd3af99641d83b7c3e1dbeeaca9c88f9ac6c6a898b5c604044294f1f30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assessmentTargetName", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupArn")
    def resource_group_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN that specifies the resource group that is used to create the assessment target.

        If ``resourceGroupArn`` is not specified, all EC2 instances in the current AWS account and Region are included in the assessment target.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html#cfn-inspector-assessmenttarget-resourcegrouparn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupArn"))

    @resource_group_arn.setter
    def resource_group_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2fc1d57cd88a11ace756d43a8aeb82e27e7d7c7c3365c4dec25225304fb0505)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-inspector.CfnAssessmentTargetProps",
    jsii_struct_bases=[],
    name_mapping={
        "assessment_target_name": "assessmentTargetName",
        "resource_group_arn": "resourceGroupArn",
    },
)
class CfnAssessmentTargetProps:
    def __init__(
        self,
        *,
        assessment_target_name: typing.Optional[builtins.str] = None,
        resource_group_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAssessmentTarget``.

        :param assessment_target_name: The name of the Amazon Inspector assessment target. The name must be unique within the AWS account .
        :param resource_group_arn: The ARN that specifies the resource group that is used to create the assessment target. If ``resourceGroupArn`` is not specified, all EC2 instances in the current AWS account and Region are included in the assessment target.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_inspector as inspector
            
            cfn_assessment_target_props = inspector.CfnAssessmentTargetProps(
                assessment_target_name="assessmentTargetName",
                resource_group_arn="resourceGroupArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc040fcd82b39830f14359d83805deb3988865b167a8a1819ddc863ab1387eeb)
            check_type(argname="argument assessment_target_name", value=assessment_target_name, expected_type=type_hints["assessment_target_name"])
            check_type(argname="argument resource_group_arn", value=resource_group_arn, expected_type=type_hints["resource_group_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assessment_target_name is not None:
            self._values["assessment_target_name"] = assessment_target_name
        if resource_group_arn is not None:
            self._values["resource_group_arn"] = resource_group_arn

    @builtins.property
    def assessment_target_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Amazon Inspector assessment target.

        The name must be unique within the AWS account .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html#cfn-inspector-assessmenttarget-assessmenttargetname
        '''
        result = self._values.get("assessment_target_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_group_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN that specifies the resource group that is used to create the assessment target.

        If ``resourceGroupArn`` is not specified, all EC2 instances in the current AWS account and Region are included in the assessment target.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html#cfn-inspector-assessmenttarget-resourcegrouparn
        '''
        result = self._values.get("resource_group_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssessmentTargetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnAssessmentTemplate(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-inspector.CfnAssessmentTemplate",
):
    '''A CloudFormation ``AWS::Inspector::AssessmentTemplate``.

    The ``AWS::Inspector::AssessmentTemplate`` resource creates an Amazon Inspector assessment template, which specifies the Inspector assessment targets that will be evaluated by an assessment run and its related configurations.

    :cloudformationResource: AWS::Inspector::AssessmentTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_inspector as inspector
        
        cfn_assessment_template = inspector.CfnAssessmentTemplate(self, "MyCfnAssessmentTemplate",
            assessment_target_arn="assessmentTargetArn",
            duration_in_seconds=123,
            rules_package_arns=["rulesPackageArns"],
        
            # the properties below are optional
            assessment_template_name="assessmentTemplateName",
            user_attributes_for_findings=[CfnTag(
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
        assessment_target_arn: builtins.str,
        duration_in_seconds: jsii.Number,
        rules_package_arns: typing.Sequence[builtins.str],
        assessment_template_name: typing.Optional[builtins.str] = None,
        user_attributes_for_findings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Inspector::AssessmentTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param assessment_target_arn: The ARN of the assessment target to be included in the assessment template.
        :param duration_in_seconds: The duration of the assessment run in seconds.
        :param rules_package_arns: The ARNs of the rules packages that you want to use in the assessment template.
        :param assessment_template_name: The user-defined name that identifies the assessment template that you want to create. You can create several assessment templates for the same assessment target. The names of the assessment templates that correspond to a particular assessment target must be unique.
        :param user_attributes_for_findings: The user-defined attributes that are assigned to every finding that is generated by the assessment run that uses this assessment template. Within an assessment template, each key must be unique.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f59a8780edce05e519d96973b653e98489aa3eb6d7160735c2284340c527fe3c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAssessmentTemplateProps(
            assessment_target_arn=assessment_target_arn,
            duration_in_seconds=duration_in_seconds,
            rules_package_arns=rules_package_arns,
            assessment_template_name=assessment_template_name,
            user_attributes_for_findings=user_attributes_for_findings,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4b60638290181d9b0f7e6e97e976b7090c8c432c8d85f46d065af9261a962c6b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__46372697450a2fcb53bfa35a1e5a3a1fe6eb4eb10e9eff4d4b3c169b66faf279)
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
        '''The Amazon Resource Name (ARN) that specifies the assessment template that is created.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="assessmentTargetArn")
    def assessment_target_arn(self) -> builtins.str:
        '''The ARN of the assessment target to be included in the assessment template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-assessmenttargetarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "assessmentTargetArn"))

    @assessment_target_arn.setter
    def assessment_target_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9075088b656dceeb7e00df92879b830f02411b97fe085aacabed6f613d36d7e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assessmentTargetArn", value)

    @builtins.property
    @jsii.member(jsii_name="durationInSeconds")
    def duration_in_seconds(self) -> jsii.Number:
        '''The duration of the assessment run in seconds.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-durationinseconds
        '''
        return typing.cast(jsii.Number, jsii.get(self, "durationInSeconds"))

    @duration_in_seconds.setter
    def duration_in_seconds(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6ea31286f9831971b958f098eb9d18921b90141ab659af59856378192437a68)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "durationInSeconds", value)

    @builtins.property
    @jsii.member(jsii_name="rulesPackageArns")
    def rules_package_arns(self) -> typing.List[builtins.str]:
        '''The ARNs of the rules packages that you want to use in the assessment template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-rulespackagearns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "rulesPackageArns"))

    @rules_package_arns.setter
    def rules_package_arns(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4670e4fa01140ec3a54705fa5f092a8c9345d30781d33a5f767ecb6c2fa8c11b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "rulesPackageArns", value)

    @builtins.property
    @jsii.member(jsii_name="assessmentTemplateName")
    def assessment_template_name(self) -> typing.Optional[builtins.str]:
        '''The user-defined name that identifies the assessment template that you want to create.

        You can create several assessment templates for the same assessment target. The names of the assessment templates that correspond to a particular assessment target must be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-assessmenttemplatename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assessmentTemplateName"))

    @assessment_template_name.setter
    def assessment_template_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4212b784218e6d86b9b78a8fbd8849f98c749d79d231ea68288a5689abbaff30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assessmentTemplateName", value)

    @builtins.property
    @jsii.member(jsii_name="userAttributesForFindings")
    def user_attributes_for_findings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.CfnTag, _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''The user-defined attributes that are assigned to every finding that is generated by the assessment run that uses this assessment template.

        Within an assessment template, each key must be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-userattributesforfindings
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.CfnTag, _aws_cdk_core_f4b25747.IResolvable]]]], jsii.get(self, "userAttributesForFindings"))

    @user_attributes_for_findings.setter
    def user_attributes_for_findings(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.CfnTag, _aws_cdk_core_f4b25747.IResolvable]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf7033b7f983f15a29eaafa409431979b55d08fbe8d771dda8bf3bb3b027b138)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAttributesForFindings", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-inspector.CfnAssessmentTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "assessment_target_arn": "assessmentTargetArn",
        "duration_in_seconds": "durationInSeconds",
        "rules_package_arns": "rulesPackageArns",
        "assessment_template_name": "assessmentTemplateName",
        "user_attributes_for_findings": "userAttributesForFindings",
    },
)
class CfnAssessmentTemplateProps:
    def __init__(
        self,
        *,
        assessment_target_arn: builtins.str,
        duration_in_seconds: jsii.Number,
        rules_package_arns: typing.Sequence[builtins.str],
        assessment_template_name: typing.Optional[builtins.str] = None,
        user_attributes_for_findings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAssessmentTemplate``.

        :param assessment_target_arn: The ARN of the assessment target to be included in the assessment template.
        :param duration_in_seconds: The duration of the assessment run in seconds.
        :param rules_package_arns: The ARNs of the rules packages that you want to use in the assessment template.
        :param assessment_template_name: The user-defined name that identifies the assessment template that you want to create. You can create several assessment templates for the same assessment target. The names of the assessment templates that correspond to a particular assessment target must be unique.
        :param user_attributes_for_findings: The user-defined attributes that are assigned to every finding that is generated by the assessment run that uses this assessment template. Within an assessment template, each key must be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_inspector as inspector
            
            cfn_assessment_template_props = inspector.CfnAssessmentTemplateProps(
                assessment_target_arn="assessmentTargetArn",
                duration_in_seconds=123,
                rules_package_arns=["rulesPackageArns"],
            
                # the properties below are optional
                assessment_template_name="assessmentTemplateName",
                user_attributes_for_findings=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93553e8a370884ce597ed97c24bbf3cdfd293017fd9e4593a82945e872b1abc0)
            check_type(argname="argument assessment_target_arn", value=assessment_target_arn, expected_type=type_hints["assessment_target_arn"])
            check_type(argname="argument duration_in_seconds", value=duration_in_seconds, expected_type=type_hints["duration_in_seconds"])
            check_type(argname="argument rules_package_arns", value=rules_package_arns, expected_type=type_hints["rules_package_arns"])
            check_type(argname="argument assessment_template_name", value=assessment_template_name, expected_type=type_hints["assessment_template_name"])
            check_type(argname="argument user_attributes_for_findings", value=user_attributes_for_findings, expected_type=type_hints["user_attributes_for_findings"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assessment_target_arn": assessment_target_arn,
            "duration_in_seconds": duration_in_seconds,
            "rules_package_arns": rules_package_arns,
        }
        if assessment_template_name is not None:
            self._values["assessment_template_name"] = assessment_template_name
        if user_attributes_for_findings is not None:
            self._values["user_attributes_for_findings"] = user_attributes_for_findings

    @builtins.property
    def assessment_target_arn(self) -> builtins.str:
        '''The ARN of the assessment target to be included in the assessment template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-assessmenttargetarn
        '''
        result = self._values.get("assessment_target_arn")
        assert result is not None, "Required property 'assessment_target_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def duration_in_seconds(self) -> jsii.Number:
        '''The duration of the assessment run in seconds.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-durationinseconds
        '''
        result = self._values.get("duration_in_seconds")
        assert result is not None, "Required property 'duration_in_seconds' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def rules_package_arns(self) -> typing.List[builtins.str]:
        '''The ARNs of the rules packages that you want to use in the assessment template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-rulespackagearns
        '''
        result = self._values.get("rules_package_arns")
        assert result is not None, "Required property 'rules_package_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def assessment_template_name(self) -> typing.Optional[builtins.str]:
        '''The user-defined name that identifies the assessment template that you want to create.

        You can create several assessment templates for the same assessment target. The names of the assessment templates that correspond to a particular assessment target must be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-assessmenttemplatename
        '''
        result = self._values.get("assessment_template_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def user_attributes_for_findings(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.CfnTag, _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''The user-defined attributes that are assigned to every finding that is generated by the assessment run that uses this assessment template.

        Within an assessment template, each key must be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-userattributesforfindings
        '''
        result = self._values.get("user_attributes_for_findings")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.CfnTag, _aws_cdk_core_f4b25747.IResolvable]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssessmentTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResourceGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-inspector.CfnResourceGroup",
):
    '''A CloudFormation ``AWS::Inspector::ResourceGroup``.

    The ``AWS::Inspector::ResourceGroup`` resource is used to create Amazon Inspector resource groups. A resource group defines a set of tags that, when queried, identify the AWS resources that make up the assessment target.

    :cloudformationResource: AWS::Inspector::ResourceGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-resourcegroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_inspector as inspector
        
        cfn_resource_group = inspector.CfnResourceGroup(self, "MyCfnResourceGroup",
            resource_group_tags=[CfnTag(
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
        resource_group_tags: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
    ) -> None:
        '''Create a new ``AWS::Inspector::ResourceGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resource_group_tags: The tags (key and value pairs) that will be associated with the resource group. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a231fc73a0657b95b4108eef97b03c19691feaa0cf047ab75af340cdbf7b58f6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourceGroupProps(resource_group_tags=resource_group_tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f416c8587bd734b0d07d03dc9224ebfdc3c1f06108535cebfcad67956ea713f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b3345f3a714cb178197a3468775bf7142b060b9848937d66029b8a0740cc2c0)
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
        '''The Amazon Resource Name (ARN) that specifies the resource group that is created.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupTags")
    def resource_group_tags(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.CfnTag, _aws_cdk_core_f4b25747.IResolvable]]]:
        '''The tags (key and value pairs) that will be associated with the resource group.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-resourcegroup.html#cfn-inspector-resourcegroup-resourcegrouptags
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.CfnTag, _aws_cdk_core_f4b25747.IResolvable]]], jsii.get(self, "resourceGroupTags"))

    @resource_group_tags.setter
    def resource_group_tags(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.CfnTag, _aws_cdk_core_f4b25747.IResolvable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb9aac1d05f9d528ffa204c5148bd2f91c4aa2c7b199dbeadc55828b5585346)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupTags", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-inspector.CfnResourceGroupProps",
    jsii_struct_bases=[],
    name_mapping={"resource_group_tags": "resourceGroupTags"},
)
class CfnResourceGroupProps:
    def __init__(
        self,
        *,
        resource_group_tags: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
    ) -> None:
        '''Properties for defining a ``CfnResourceGroup``.

        :param resource_group_tags: The tags (key and value pairs) that will be associated with the resource group. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-resourcegroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_inspector as inspector
            
            cfn_resource_group_props = inspector.CfnResourceGroupProps(
                resource_group_tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af7e165b3d05a0f9efb1ddcc91981da12e22bd51f66bff43ad71033823bd1d0)
            check_type(argname="argument resource_group_tags", value=resource_group_tags, expected_type=type_hints["resource_group_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_group_tags": resource_group_tags,
        }

    @builtins.property
    def resource_group_tags(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.CfnTag, _aws_cdk_core_f4b25747.IResolvable]]]:
        '''The tags (key and value pairs) that will be associated with the resource group.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-resourcegroup.html#cfn-inspector-resourcegroup-resourcegrouptags
        '''
        result = self._values.get("resource_group_tags")
        assert result is not None, "Required property 'resource_group_tags' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.CfnTag, _aws_cdk_core_f4b25747.IResolvable]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAssessmentTarget",
    "CfnAssessmentTargetProps",
    "CfnAssessmentTemplate",
    "CfnAssessmentTemplateProps",
    "CfnResourceGroup",
    "CfnResourceGroupProps",
]

publication.publish()

def _typecheckingstub__c2098595cd6e90804bdf42e9aaa8581983888e5f21789e5e8055df2f6d457c11(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    assessment_target_name: typing.Optional[builtins.str] = None,
    resource_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f81e73f2178b215f62b276482081748ebaeb68fe1cc3cbe771495fafbf327f90(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc7b08bdfe2eccdb2ef287f8c16d3a0dd28150b726350efa7da0bb51c69e621c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7329abd3af99641d83b7c3e1dbeeaca9c88f9ac6c6a898b5c604044294f1f30(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2fc1d57cd88a11ace756d43a8aeb82e27e7d7c7c3365c4dec25225304fb0505(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc040fcd82b39830f14359d83805deb3988865b167a8a1819ddc863ab1387eeb(
    *,
    assessment_target_name: typing.Optional[builtins.str] = None,
    resource_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f59a8780edce05e519d96973b653e98489aa3eb6d7160735c2284340c527fe3c(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    assessment_target_arn: builtins.str,
    duration_in_seconds: jsii.Number,
    rules_package_arns: typing.Sequence[builtins.str],
    assessment_template_name: typing.Optional[builtins.str] = None,
    user_attributes_for_findings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4b60638290181d9b0f7e6e97e976b7090c8c432c8d85f46d065af9261a962c6b(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46372697450a2fcb53bfa35a1e5a3a1fe6eb4eb10e9eff4d4b3c169b66faf279(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9075088b656dceeb7e00df92879b830f02411b97fe085aacabed6f613d36d7e1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ea31286f9831971b958f098eb9d18921b90141ab659af59856378192437a68(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4670e4fa01140ec3a54705fa5f092a8c9345d30781d33a5f767ecb6c2fa8c11b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4212b784218e6d86b9b78a8fbd8849f98c749d79d231ea68288a5689abbaff30(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf7033b7f983f15a29eaafa409431979b55d08fbe8d771dda8bf3bb3b027b138(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.CfnTag, _aws_cdk_core_f4b25747.IResolvable]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93553e8a370884ce597ed97c24bbf3cdfd293017fd9e4593a82945e872b1abc0(
    *,
    assessment_target_arn: builtins.str,
    duration_in_seconds: jsii.Number,
    rules_package_arns: typing.Sequence[builtins.str],
    assessment_template_name: typing.Optional[builtins.str] = None,
    user_attributes_for_findings: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a231fc73a0657b95b4108eef97b03c19691feaa0cf047ab75af340cdbf7b58f6(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    resource_group_tags: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f416c8587bd734b0d07d03dc9224ebfdc3c1f06108535cebfcad67956ea713f(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b3345f3a714cb178197a3468775bf7142b060b9848937d66029b8a0740cc2c0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb9aac1d05f9d528ffa204c5148bd2f91c4aa2c7b199dbeadc55828b5585346(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.CfnTag, _aws_cdk_core_f4b25747.IResolvable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af7e165b3d05a0f9efb1ddcc91981da12e22bd51f66bff43ad71033823bd1d0(
    *,
    resource_group_tags: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
) -> None:
    """Type checking stubs"""
    pass
