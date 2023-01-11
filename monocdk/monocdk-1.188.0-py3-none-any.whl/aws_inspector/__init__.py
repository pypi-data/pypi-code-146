'''
# Amazon Inspector Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as inspector
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

from .._jsii import *

from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnAssessmentTarget(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_inspector.CfnAssessmentTarget",
):
    '''A CloudFormation ``AWS::Inspector::AssessmentTarget``.

    The ``AWS::Inspector::AssessmentTarget`` resource is used to create Amazon Inspector assessment targets, which specify the Amazon EC2 instances that will be analyzed during an assessment run.

    :cloudformationResource: AWS::Inspector::AssessmentTarget
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttarget.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_inspector as inspector
        
        cfn_assessment_target = inspector.CfnAssessmentTarget(self, "MyCfnAssessmentTarget",
            assessment_target_name="assessmentTargetName",
            resource_group_arn="resourceGroupArn"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
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
            type_hints = typing.get_type_hints(_typecheckingstub__e7743e54dacb5da1e76de8a0c77c1615527c269409e1c6d994e6888f419e8019)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAssessmentTargetProps(
            assessment_target_name=assessment_target_name,
            resource_group_arn=resource_group_arn,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d66a3aa7b8d5eacacf4dc8fc9adcad2606538e98cc5015a26d4a35a4f6045c80)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ed8196f3117027ef9539280a41578a5662a005895df3a38bbd4b7c3f314b1b6f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__295175eb3a1907151c0c5b6e1c587f9aa01d3ed6720f53efdc1c3641e8e5df51)
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
            type_hints = typing.get_type_hints(_typecheckingstub__4fabf6c8728aaa7ac4c818ebf93605fabdedca55402231ea18aec66cac788fe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupArn", value)


@jsii.data_type(
    jsii_type="monocdk.aws_inspector.CfnAssessmentTargetProps",
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
            from monocdk import aws_inspector as inspector
            
            cfn_assessment_target_props = inspector.CfnAssessmentTargetProps(
                assessment_target_name="assessmentTargetName",
                resource_group_arn="resourceGroupArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__49ffd8bfe242120115dc4123def98cbfb46ef66ca33c8f1a7195f2bec75a4aa2)
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


@jsii.implements(_IInspectable_82c04a63)
class CfnAssessmentTemplate(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_inspector.CfnAssessmentTemplate",
):
    '''A CloudFormation ``AWS::Inspector::AssessmentTemplate``.

    The ``AWS::Inspector::AssessmentTemplate`` resource creates an Amazon Inspector assessment template, which specifies the Inspector assessment targets that will be evaluated by an assessment run and its related configurations.

    :cloudformationResource: AWS::Inspector::AssessmentTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_inspector as inspector
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        assessment_target_arn: builtins.str,
        duration_in_seconds: jsii.Number,
        rules_package_arns: typing.Sequence[builtins.str],
        assessment_template_name: typing.Optional[builtins.str] = None,
        user_attributes_for_findings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6babe229ddd946797d141495db867961590a25ba92590c07259e31da527044a)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3241c896fc3c221d80da8743c8de861869e129205486e315b31c1e02813d5ab1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e6e1517ab9e29a29f6f8a372ca6e070ad962aad1f0f49f1b2c9377e76e99574)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64c68a233862a9b099599092fdb2bd98be1cc69ffc93a0f2872e92181adde49d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b2e8b9b55803325904faa0bb16c7a5a581cb75a28aac23da8d6b879573e84a0b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9ee9b8cdcaaca89991b53da2f0b5592472cdb76a6918c5a5907341e726acb509)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3122c09366aed4ef599c9bef740e704127f7cd51baef727c2d5521d85dfb5849)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assessmentTemplateName", value)

    @builtins.property
    @jsii.member(jsii_name="userAttributesForFindings")
    def user_attributes_for_findings(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]]:
        '''The user-defined attributes that are assigned to every finding that is generated by the assessment run that uses this assessment template.

        Within an assessment template, each key must be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-userattributesforfindings
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]], jsii.get(self, "userAttributesForFindings"))

    @user_attributes_for_findings.setter
    def user_attributes_for_findings(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad0b071af510fe526e4af147000237a0a4d3ff4e9887347ac45f3959658fde67)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userAttributesForFindings", value)


@jsii.data_type(
    jsii_type="monocdk.aws_inspector.CfnAssessmentTemplateProps",
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
        user_attributes_for_findings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
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
            from monocdk import aws_inspector as inspector
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__ee3864ae57be391ade6c966920721c3d6da1d87d6121643330939ce268e516d1)
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
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]]:
        '''The user-defined attributes that are assigned to every finding that is generated by the assessment run that uses this assessment template.

        Within an assessment template, each key must be unique.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-assessmenttemplate.html#cfn-inspector-assessmenttemplate-userattributesforfindings
        '''
        result = self._values.get("user_attributes_for_findings")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssessmentTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResourceGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_inspector.CfnResourceGroup",
):
    '''A CloudFormation ``AWS::Inspector::ResourceGroup``.

    The ``AWS::Inspector::ResourceGroup`` resource is used to create Amazon Inspector resource groups. A resource group defines a set of tags that, when queried, identify the AWS resources that make up the assessment target.

    :cloudformationResource: AWS::Inspector::ResourceGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-resourcegroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_inspector as inspector
        
        cfn_resource_group = inspector.CfnResourceGroup(self, "MyCfnResourceGroup",
            resource_group_tags=[CfnTag(
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
        resource_group_tags: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Create a new ``AWS::Inspector::ResourceGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resource_group_tags: The tags (key and value pairs) that will be associated with the resource group. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f8d49ea7c65a595eac78fadf78b48f0e7053a4b7f26c0d7cf247f6a20931f8d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourceGroupProps(resource_group_tags=resource_group_tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78a6dea16ccb20df47ec36875f1dc013622d9743a833b8caa7e5e62e396f57de)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e2fea159bddf6526b8c1d414f752e868b17a94c0a7f9c4fb7c240ba5b2f4e27a)
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
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]:
        '''The tags (key and value pairs) that will be associated with the resource group.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-resourcegroup.html#cfn-inspector-resourcegroup-resourcegrouptags
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]], jsii.get(self, "resourceGroupTags"))

    @resource_group_tags.setter
    def resource_group_tags(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ddb88c4611c033fb9555603887dbb5a25571b89733a861b763d6e0b50f1b33f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupTags", value)


@jsii.data_type(
    jsii_type="monocdk.aws_inspector.CfnResourceGroupProps",
    jsii_struct_bases=[],
    name_mapping={"resource_group_tags": "resourceGroupTags"},
)
class CfnResourceGroupProps:
    def __init__(
        self,
        *,
        resource_group_tags: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]],
    ) -> None:
        '''Properties for defining a ``CfnResourceGroup``.

        :param resource_group_tags: The tags (key and value pairs) that will be associated with the resource group. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-resourcegroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_inspector as inspector
            
            cfn_resource_group_props = inspector.CfnResourceGroupProps(
                resource_group_tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f40d1d0570f2230c028d34099a98e1c38667f8ed7339b25e2466707d1817d65)
            check_type(argname="argument resource_group_tags", value=resource_group_tags, expected_type=type_hints["resource_group_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_group_tags": resource_group_tags,
        }

    @builtins.property
    def resource_group_tags(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]:
        '''The tags (key and value pairs) that will be associated with the resource group.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-inspector-resourcegroup.html#cfn-inspector-resourcegroup-resourcegrouptags
        '''
        result = self._values.get("resource_group_tags")
        assert result is not None, "Required property 'resource_group_tags' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]], result)

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

def _typecheckingstub__e7743e54dacb5da1e76de8a0c77c1615527c269409e1c6d994e6888f419e8019(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    assessment_target_name: typing.Optional[builtins.str] = None,
    resource_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d66a3aa7b8d5eacacf4dc8fc9adcad2606538e98cc5015a26d4a35a4f6045c80(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed8196f3117027ef9539280a41578a5662a005895df3a38bbd4b7c3f314b1b6f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__295175eb3a1907151c0c5b6e1c587f9aa01d3ed6720f53efdc1c3641e8e5df51(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fabf6c8728aaa7ac4c818ebf93605fabdedca55402231ea18aec66cac788fe0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49ffd8bfe242120115dc4123def98cbfb46ef66ca33c8f1a7195f2bec75a4aa2(
    *,
    assessment_target_name: typing.Optional[builtins.str] = None,
    resource_group_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6babe229ddd946797d141495db867961590a25ba92590c07259e31da527044a(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    assessment_target_arn: builtins.str,
    duration_in_seconds: jsii.Number,
    rules_package_arns: typing.Sequence[builtins.str],
    assessment_template_name: typing.Optional[builtins.str] = None,
    user_attributes_for_findings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3241c896fc3c221d80da8743c8de861869e129205486e315b31c1e02813d5ab1(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e6e1517ab9e29a29f6f8a372ca6e070ad962aad1f0f49f1b2c9377e76e99574(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64c68a233862a9b099599092fdb2bd98be1cc69ffc93a0f2872e92181adde49d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2e8b9b55803325904faa0bb16c7a5a581cb75a28aac23da8d6b879573e84a0b(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee9b8cdcaaca89991b53da2f0b5592472cdb76a6918c5a5907341e726acb509(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3122c09366aed4ef599c9bef740e704127f7cd51baef727c2d5521d85dfb5849(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad0b071af510fe526e4af147000237a0a4d3ff4e9887347ac45f3959658fde67(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee3864ae57be391ade6c966920721c3d6da1d87d6121643330939ce268e516d1(
    *,
    assessment_target_arn: builtins.str,
    duration_in_seconds: jsii.Number,
    rules_package_arns: typing.Sequence[builtins.str],
    assessment_template_name: typing.Optional[builtins.str] = None,
    user_attributes_for_findings: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f8d49ea7c65a595eac78fadf78b48f0e7053a4b7f26c0d7cf247f6a20931f8d(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    resource_group_tags: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78a6dea16ccb20df47ec36875f1dc013622d9743a833b8caa7e5e62e396f57de(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2fea159bddf6526b8c1d414f752e868b17a94c0a7f9c4fb7c240ba5b2f4e27a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ddb88c4611c033fb9555603887dbb5a25571b89733a861b763d6e0b50f1b33f4(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[_IResolvable_a771d0ef, _CfnTag_95fbdc29]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f40d1d0570f2230c028d34099a98e1c38667f8ed7339b25e2466707d1817d65(
    *,
    resource_group_tags: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[_IResolvable_a771d0ef, typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass
