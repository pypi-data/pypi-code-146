'''
# AWS::AuditManager Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as auditmanager
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for AuditManager construct libraries](https://constructs.dev/search?q=auditmanager)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::AuditManager resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AuditManager.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::AuditManager](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_AuditManager.html).

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
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.implements(_IInspectable_82c04a63)
class CfnAssessment(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_auditmanager.CfnAssessment",
):
    '''A CloudFormation ``AWS::AuditManager::Assessment``.

    The ``AWS::AuditManager::Assessment`` resource is an Audit Manager resource type that defines the scope of audit evidence collected by Audit Manager . An Audit Manager assessment is an implementation of an Audit Manager framework.

    :cloudformationResource: AWS::AuditManager::Assessment
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_auditmanager as auditmanager
        
        cfn_assessment = auditmanager.CfnAssessment(self, "MyCfnAssessment",
            assessment_reports_destination=auditmanager.CfnAssessment.AssessmentReportsDestinationProperty(
                destination="destination",
                destination_type="destinationType"
            ),
            aws_account=auditmanager.CfnAssessment.AWSAccountProperty(
                email_address="emailAddress",
                id="id",
                name="name"
            ),
            description="description",
            framework_id="frameworkId",
            name="name",
            roles=[auditmanager.CfnAssessment.RoleProperty(
                role_arn="roleArn",
                role_type="roleType"
            )],
            scope=auditmanager.CfnAssessment.ScopeProperty(
                aws_accounts=[auditmanager.CfnAssessment.AWSAccountProperty(
                    email_address="emailAddress",
                    id="id",
                    name="name"
                )],
                aws_services=[auditmanager.CfnAssessment.AWSServiceProperty(
                    service_name="serviceName"
                )]
            ),
            status="status",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope_: _Construct_e78e779f,
        id: builtins.str,
        *,
        assessment_reports_destination: typing.Optional[typing.Union[typing.Union["CfnAssessment.AssessmentReportsDestinationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        aws_account: typing.Optional[typing.Union[typing.Union["CfnAssessment.AWSAccountProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        framework_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAssessment.RoleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        scope: typing.Optional[typing.Union[typing.Union["CfnAssessment.ScopeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::AuditManager::Assessment``.

        :param scope_: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param assessment_reports_destination: The destination that evidence reports are stored in for the assessment.
        :param aws_account: The AWS account that's associated with the assessment.
        :param description: The description of the assessment.
        :param framework_id: The unique identifier for the framework.
        :param name: The name of the assessment.
        :param roles: The roles that are associated with the assessment.
        :param scope: The wrapper of AWS accounts and services that are in scope for the assessment.
        :param status: The overall status of the assessment. When you create a new assessment, the initial ``Status`` value is always ``ACTIVE`` . When you create an assessment, even if you specify the value as ``INACTIVE`` , the value overrides to ``ACTIVE`` . After you create an assessment, you can change the value of the ``Status`` property at any time. For example, when you want to stop collecting evidence for your assessment, you can change the assessment status to ``INACTIVE`` .
        :param tags: The tags that are associated with the assessment.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ddc2a7c4c5e4c8fe005067bda7510cf9bdda6f1f4c2a08372c4ea5523861bb7)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAssessmentProps(
            assessment_reports_destination=assessment_reports_destination,
            aws_account=aws_account,
            description=description,
            framework_id=framework_id,
            name=name,
            roles=roles,
            scope=scope,
            status=status,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope_, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fe2b355e2afecd8c5fc82f7b521a4ead8b07f8c3feb8a9066d35291486704ee)
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
            type_hints = typing.get_type_hints(_typecheckingstub__90693076e36d722051123d286fb1b21e9c79f8b4c0cd7d71cc68d283b901ab4a)
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
        '''The Amazon Resource Name (ARN) of the assessment.

        For example, ``arn:aws:auditmanager:us-east-1:123456789012:assessment/111A1A1A-22B2-33C3-DDD4-55E5E5E555E5`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrAssessmentId")
    def attr_assessment_id(self) -> builtins.str:
        '''The unique identifier for the assessment.

        For example, ``111A1A1A-22B2-33C3-DDD4-55E5E5E555E5`` .

        :cloudformationAttribute: AssessmentId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAssessmentId"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> _IResolvable_a771d0ef:
        '''The time when the assessment was created.

        For example, ``1607582033.373`` .

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrDelegations")
    def attr_delegations(self) -> _IResolvable_a771d0ef:
        '''The delegations that are associated with the assessment.

        :cloudformationAttribute: Delegations
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrDelegations"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tags that are associated with the assessment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="assessmentReportsDestination")
    def assessment_reports_destination(
        self,
    ) -> typing.Optional[typing.Union["CfnAssessment.AssessmentReportsDestinationProperty", _IResolvable_a771d0ef]]:
        '''The destination that evidence reports are stored in for the assessment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-assessmentreportsdestination
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAssessment.AssessmentReportsDestinationProperty", _IResolvable_a771d0ef]], jsii.get(self, "assessmentReportsDestination"))

    @assessment_reports_destination.setter
    def assessment_reports_destination(
        self,
        value: typing.Optional[typing.Union["CfnAssessment.AssessmentReportsDestinationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd5af7541ac62627ea1e707bb60488ac21e64300ae54967ae86dfeda91c6b5d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assessmentReportsDestination", value)

    @builtins.property
    @jsii.member(jsii_name="awsAccount")
    def aws_account(
        self,
    ) -> typing.Optional[typing.Union["CfnAssessment.AWSAccountProperty", _IResolvable_a771d0ef]]:
        '''The AWS account that's associated with the assessment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-awsaccount
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAssessment.AWSAccountProperty", _IResolvable_a771d0ef]], jsii.get(self, "awsAccount"))

    @aws_account.setter
    def aws_account(
        self,
        value: typing.Optional[typing.Union["CfnAssessment.AWSAccountProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c39869dec454d6f66ea603119acea3e3b4f9d68386052226dd18ba44f5652162)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsAccount", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the assessment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__373ca6f23f142bad03d21e2dfba76a274b4925d137e11d03bdb06c4955c59ee4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="frameworkId")
    def framework_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the framework.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-frameworkid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "frameworkId"))

    @framework_id.setter
    def framework_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c98ad941eb061a54360897b49b8f7143f9d94673f7f047d810afad58791af63d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "frameworkId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the assessment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afe450a63abcf98098577db0135eee8dcab6e21f93cc3ee21557d0a1464db5f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssessment.RoleProperty", _IResolvable_a771d0ef]]]]:
        '''The roles that are associated with the assessment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-roles
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssessment.RoleProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "roles"))

    @roles.setter
    def roles(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssessment.RoleProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dabcee863f0953ab3e9f1eedf1414381a6f14b022f6044405c57bcd18b31e31f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value)

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(
        self,
    ) -> typing.Optional[typing.Union["CfnAssessment.ScopeProperty", _IResolvable_a771d0ef]]:
        '''The wrapper of AWS accounts and services that are in scope for the assessment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-scope
        '''
        return typing.cast(typing.Optional[typing.Union["CfnAssessment.ScopeProperty", _IResolvable_a771d0ef]], jsii.get(self, "scope"))

    @scope.setter
    def scope(
        self,
        value: typing.Optional[typing.Union["CfnAssessment.ScopeProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0d6161d9f1dd28e675997e14b8ade668a3e93111500da1de7b947620b8ae3ada)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scope", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''The overall status of the assessment.

        When you create a new assessment, the initial ``Status`` value is always ``ACTIVE`` . When you create an assessment, even if you specify the value as ``INACTIVE`` , the value overrides to ``ACTIVE`` .

        After you create an assessment, you can change the value of the ``Status`` property at any time. For example, when you want to stop collecting evidence for your assessment, you can change the assessment status to ``INACTIVE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4207f3bb11242bae9f8cc66c065c655417eb9645b21c7f70faa41d4bf6be057d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_auditmanager.CfnAssessment.AWSAccountProperty",
        jsii_struct_bases=[],
        name_mapping={"email_address": "emailAddress", "id": "id", "name": "name"},
    )
    class AWSAccountProperty:
        def __init__(
            self,
            *,
            email_address: typing.Optional[builtins.str] = None,
            id: typing.Optional[builtins.str] = None,
            name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AWSAccount`` property type specifies the wrapper of the AWS account details, such as account ID, email address, and so on.

            :param email_address: The email address that's associated with the AWS account .
            :param id: The identifier for the AWS account .
            :param name: The name of the AWS account .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsaccount.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_auditmanager as auditmanager
                
                a_wSAccount_property = auditmanager.CfnAssessment.AWSAccountProperty(
                    email_address="emailAddress",
                    id="id",
                    name="name"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0f3d53c1a8253a3e6c1e05be11ad2c49a968187f1008deb4911b1ef7beb01a85)
                check_type(argname="argument email_address", value=email_address, expected_type=type_hints["email_address"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if email_address is not None:
                self._values["email_address"] = email_address
            if id is not None:
                self._values["id"] = id
            if name is not None:
                self._values["name"] = name

        @builtins.property
        def email_address(self) -> typing.Optional[builtins.str]:
            '''The email address that's associated with the AWS account .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsaccount.html#cfn-auditmanager-assessment-awsaccount-emailaddress
            '''
            result = self._values.get("email_address")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the AWS account .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsaccount.html#cfn-auditmanager-assessment-awsaccount-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def name(self) -> typing.Optional[builtins.str]:
            '''The name of the AWS account .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsaccount.html#cfn-auditmanager-assessment-awsaccount-name
            '''
            result = self._values.get("name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AWSAccountProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_auditmanager.CfnAssessment.AWSServiceProperty",
        jsii_struct_bases=[],
        name_mapping={"service_name": "serviceName"},
    )
    class AWSServiceProperty:
        def __init__(
            self,
            *,
            service_name: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AWSService`` property type specifies an AWS service such as Amazon S3 , AWS CloudTrail , and so on.

            :param service_name: The name of the AWS service .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsservice.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_auditmanager as auditmanager
                
                a_wSService_property = auditmanager.CfnAssessment.AWSServiceProperty(
                    service_name="serviceName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2c3efde75d6cc746097bd7036a863960aaaff1a61b025c9a88a13a123c225f83)
                check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if service_name is not None:
                self._values["service_name"] = service_name

        @builtins.property
        def service_name(self) -> typing.Optional[builtins.str]:
            '''The name of the AWS service .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-awsservice.html#cfn-auditmanager-assessment-awsservice-servicename
            '''
            result = self._values.get("service_name")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AWSServiceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_auditmanager.CfnAssessment.AssessmentReportsDestinationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination": "destination",
            "destination_type": "destinationType",
        },
    )
    class AssessmentReportsDestinationProperty:
        def __init__(
            self,
            *,
            destination: typing.Optional[builtins.str] = None,
            destination_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``AssessmentReportsDestination`` property type specifies the location in which AWS Audit Manager saves assessment reports for the given assessment.

            :param destination: The destination of the assessment report.
            :param destination_type: The destination type, such as Amazon S3.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-assessmentreportsdestination.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_auditmanager as auditmanager
                
                assessment_reports_destination_property = auditmanager.CfnAssessment.AssessmentReportsDestinationProperty(
                    destination="destination",
                    destination_type="destinationType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__698d1ce4f172d51d79190336a4ddb24e8d0613290a32c45e3d362bde187f800d)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument destination_type", value=destination_type, expected_type=type_hints["destination_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination is not None:
                self._values["destination"] = destination
            if destination_type is not None:
                self._values["destination_type"] = destination_type

        @builtins.property
        def destination(self) -> typing.Optional[builtins.str]:
            '''The destination of the assessment report.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-assessmentreportsdestination.html#cfn-auditmanager-assessment-assessmentreportsdestination-destination
            '''
            result = self._values.get("destination")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def destination_type(self) -> typing.Optional[builtins.str]:
            '''The destination type, such as Amazon S3.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-assessmentreportsdestination.html#cfn-auditmanager-assessment-assessmentreportsdestination-destinationtype
            '''
            result = self._values.get("destination_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AssessmentReportsDestinationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_auditmanager.CfnAssessment.DelegationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "assessment_id": "assessmentId",
            "assessment_name": "assessmentName",
            "comment": "comment",
            "control_set_id": "controlSetId",
            "created_by": "createdBy",
            "creation_time": "creationTime",
            "id": "id",
            "last_updated": "lastUpdated",
            "role_arn": "roleArn",
            "role_type": "roleType",
            "status": "status",
        },
    )
    class DelegationProperty:
        def __init__(
            self,
            *,
            assessment_id: typing.Optional[builtins.str] = None,
            assessment_name: typing.Optional[builtins.str] = None,
            comment: typing.Optional[builtins.str] = None,
            control_set_id: typing.Optional[builtins.str] = None,
            created_by: typing.Optional[builtins.str] = None,
            creation_time: typing.Optional[jsii.Number] = None,
            id: typing.Optional[builtins.str] = None,
            last_updated: typing.Optional[jsii.Number] = None,
            role_arn: typing.Optional[builtins.str] = None,
            role_type: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``Delegation`` property type specifies the assignment of a control set to a delegate for review.

            :param assessment_id: The identifier for the assessment that's associated with the delegation.
            :param assessment_name: The name of the assessment that's associated with the delegation.
            :param comment: The comment that's related to the delegation.
            :param control_set_id: The identifier for the control set that's associated with the delegation.
            :param created_by: The IAM user or role that created the delegation. *Minimum* : ``1`` *Maximum* : ``100`` *Pattern* : ``^[a-zA-Z0-9-_()\\\\[\\\\]\\\\s]+$``
            :param creation_time: Specifies when the delegation was created.
            :param id: The unique identifier for the delegation.
            :param last_updated: Specifies when the delegation was last updated.
            :param role_arn: The Amazon Resource Name (ARN) of the IAM role.
            :param role_type: The type of customer persona. .. epigraph:: In ``CreateAssessment`` , ``roleType`` can only be ``PROCESS_OWNER`` . In ``UpdateSettings`` , ``roleType`` can only be ``PROCESS_OWNER`` . In ``BatchCreateDelegationByAssessment`` , ``roleType`` can only be ``RESOURCE_OWNER`` .
            :param status: The status of the delegation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_auditmanager as auditmanager
                
                delegation_property = auditmanager.CfnAssessment.DelegationProperty(
                    assessment_id="assessmentId",
                    assessment_name="assessmentName",
                    comment="comment",
                    control_set_id="controlSetId",
                    created_by="createdBy",
                    creation_time=123,
                    id="id",
                    last_updated=123,
                    role_arn="roleArn",
                    role_type="roleType",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__db2bace9243eace15e234ec8dec072be1999d574d64fb49f1309344c371dd44d)
                check_type(argname="argument assessment_id", value=assessment_id, expected_type=type_hints["assessment_id"])
                check_type(argname="argument assessment_name", value=assessment_name, expected_type=type_hints["assessment_name"])
                check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
                check_type(argname="argument control_set_id", value=control_set_id, expected_type=type_hints["control_set_id"])
                check_type(argname="argument created_by", value=created_by, expected_type=type_hints["created_by"])
                check_type(argname="argument creation_time", value=creation_time, expected_type=type_hints["creation_time"])
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument last_updated", value=last_updated, expected_type=type_hints["last_updated"])
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument role_type", value=role_type, expected_type=type_hints["role_type"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if assessment_id is not None:
                self._values["assessment_id"] = assessment_id
            if assessment_name is not None:
                self._values["assessment_name"] = assessment_name
            if comment is not None:
                self._values["comment"] = comment
            if control_set_id is not None:
                self._values["control_set_id"] = control_set_id
            if created_by is not None:
                self._values["created_by"] = created_by
            if creation_time is not None:
                self._values["creation_time"] = creation_time
            if id is not None:
                self._values["id"] = id
            if last_updated is not None:
                self._values["last_updated"] = last_updated
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if role_type is not None:
                self._values["role_type"] = role_type
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def assessment_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the assessment that's associated with the delegation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-assessmentid
            '''
            result = self._values.get("assessment_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def assessment_name(self) -> typing.Optional[builtins.str]:
            '''The name of the assessment that's associated with the delegation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-assessmentname
            '''
            result = self._values.get("assessment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def comment(self) -> typing.Optional[builtins.str]:
            '''The comment that's related to the delegation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-comment
            '''
            result = self._values.get("comment")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def control_set_id(self) -> typing.Optional[builtins.str]:
            '''The identifier for the control set that's associated with the delegation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-controlsetid
            '''
            result = self._values.get("control_set_id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def created_by(self) -> typing.Optional[builtins.str]:
            '''The IAM user or role that created the delegation.

            *Minimum* : ``1``

            *Maximum* : ``100``

            *Pattern* : ``^[a-zA-Z0-9-_()\\\\[\\\\]\\\\s]+$``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-createdby
            '''
            result = self._values.get("created_by")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def creation_time(self) -> typing.Optional[jsii.Number]:
            '''Specifies when the delegation was created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-creationtime
            '''
            result = self._values.get("creation_time")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def id(self) -> typing.Optional[builtins.str]:
            '''The unique identifier for the delegation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-id
            '''
            result = self._values.get("id")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def last_updated(self) -> typing.Optional[jsii.Number]:
            '''Specifies when the delegation was last updated.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-lastupdated
            '''
            result = self._values.get("last_updated")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_type(self) -> typing.Optional[builtins.str]:
            '''The type of customer persona.

            .. epigraph::

               In ``CreateAssessment`` , ``roleType`` can only be ``PROCESS_OWNER`` .

               In ``UpdateSettings`` , ``roleType`` can only be ``PROCESS_OWNER`` .

               In ``BatchCreateDelegationByAssessment`` , ``roleType`` can only be ``RESOURCE_OWNER`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-roletype
            '''
            result = self._values.get("role_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status of the delegation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-delegation.html#cfn-auditmanager-assessment-delegation-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DelegationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_auditmanager.CfnAssessment.RoleProperty",
        jsii_struct_bases=[],
        name_mapping={"role_arn": "roleArn", "role_type": "roleType"},
    )
    class RoleProperty:
        def __init__(
            self,
            *,
            role_arn: typing.Optional[builtins.str] = None,
            role_type: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The ``Role`` property type specifies the wrapper that contains AWS Audit Manager role information, such as the role type and IAM Amazon Resource Name (ARN).

            :param role_arn: The Amazon Resource Name (ARN) of the IAM role.
            :param role_type: The type of customer persona. .. epigraph:: In ``CreateAssessment`` , ``roleType`` can only be ``PROCESS_OWNER`` . In ``UpdateSettings`` , ``roleType`` can only be ``PROCESS_OWNER`` . In ``BatchCreateDelegationByAssessment`` , ``roleType`` can only be ``RESOURCE_OWNER`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-role.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_auditmanager as auditmanager
                
                role_property = auditmanager.CfnAssessment.RoleProperty(
                    role_arn="roleArn",
                    role_type="roleType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e105064bde8034172321edae88674f09521694a7bb7f1e1a6df9dbd2ca987ec0)
                check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
                check_type(argname="argument role_type", value=role_type, expected_type=type_hints["role_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if role_arn is not None:
                self._values["role_arn"] = role_arn
            if role_type is not None:
                self._values["role_type"] = role_type

        @builtins.property
        def role_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the IAM role.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-role.html#cfn-auditmanager-assessment-role-rolearn
            '''
            result = self._values.get("role_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def role_type(self) -> typing.Optional[builtins.str]:
            '''The type of customer persona.

            .. epigraph::

               In ``CreateAssessment`` , ``roleType`` can only be ``PROCESS_OWNER`` .

               In ``UpdateSettings`` , ``roleType`` can only be ``PROCESS_OWNER`` .

               In ``BatchCreateDelegationByAssessment`` , ``roleType`` can only be ``RESOURCE_OWNER`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-role.html#cfn-auditmanager-assessment-role-roletype
            '''
            result = self._values.get("role_type")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RoleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_auditmanager.CfnAssessment.ScopeProperty",
        jsii_struct_bases=[],
        name_mapping={"aws_accounts": "awsAccounts", "aws_services": "awsServices"},
    )
    class ScopeProperty:
        def __init__(
            self,
            *,
            aws_accounts: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAssessment.AWSAccountProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            aws_services: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnAssessment.AWSServiceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''The ``Scope`` property type specifies the wrapper that contains the AWS accounts and services that are in scope for the assessment.

            :param aws_accounts: The AWS accounts that are included in the scope of the assessment.
            :param aws_services: The AWS services that are included in the scope of the assessment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-scope.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_auditmanager as auditmanager
                
                scope_property = auditmanager.CfnAssessment.ScopeProperty(
                    aws_accounts=[auditmanager.CfnAssessment.AWSAccountProperty(
                        email_address="emailAddress",
                        id="id",
                        name="name"
                    )],
                    aws_services=[auditmanager.CfnAssessment.AWSServiceProperty(
                        service_name="serviceName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59d7f15efdaf6c609c1995ba40aed7122761b80061e0fc3918e33393844ab0be)
                check_type(argname="argument aws_accounts", value=aws_accounts, expected_type=type_hints["aws_accounts"])
                check_type(argname="argument aws_services", value=aws_services, expected_type=type_hints["aws_services"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if aws_accounts is not None:
                self._values["aws_accounts"] = aws_accounts
            if aws_services is not None:
                self._values["aws_services"] = aws_services

        @builtins.property
        def aws_accounts(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssessment.AWSAccountProperty", _IResolvable_a771d0ef]]]]:
            '''The AWS accounts that are included in the scope of the assessment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-scope.html#cfn-auditmanager-assessment-scope-awsaccounts
            '''
            result = self._values.get("aws_accounts")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssessment.AWSAccountProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def aws_services(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssessment.AWSServiceProperty", _IResolvable_a771d0ef]]]]:
            '''The AWS services that are included in the scope of the assessment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-auditmanager-assessment-scope.html#cfn-auditmanager-assessment-scope-awsservices
            '''
            result = self._values.get("aws_services")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnAssessment.AWSServiceProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ScopeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_auditmanager.CfnAssessmentProps",
    jsii_struct_bases=[],
    name_mapping={
        "assessment_reports_destination": "assessmentReportsDestination",
        "aws_account": "awsAccount",
        "description": "description",
        "framework_id": "frameworkId",
        "name": "name",
        "roles": "roles",
        "scope": "scope",
        "status": "status",
        "tags": "tags",
    },
)
class CfnAssessmentProps:
    def __init__(
        self,
        *,
        assessment_reports_destination: typing.Optional[typing.Union[typing.Union[CfnAssessment.AssessmentReportsDestinationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        aws_account: typing.Optional[typing.Union[typing.Union[CfnAssessment.AWSAccountProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        framework_id: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAssessment.RoleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        scope: typing.Optional[typing.Union[typing.Union[CfnAssessment.ScopeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        status: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAssessment``.

        :param assessment_reports_destination: The destination that evidence reports are stored in for the assessment.
        :param aws_account: The AWS account that's associated with the assessment.
        :param description: The description of the assessment.
        :param framework_id: The unique identifier for the framework.
        :param name: The name of the assessment.
        :param roles: The roles that are associated with the assessment.
        :param scope: The wrapper of AWS accounts and services that are in scope for the assessment.
        :param status: The overall status of the assessment. When you create a new assessment, the initial ``Status`` value is always ``ACTIVE`` . When you create an assessment, even if you specify the value as ``INACTIVE`` , the value overrides to ``ACTIVE`` . After you create an assessment, you can change the value of the ``Status`` property at any time. For example, when you want to stop collecting evidence for your assessment, you can change the assessment status to ``INACTIVE`` .
        :param tags: The tags that are associated with the assessment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_auditmanager as auditmanager
            
            cfn_assessment_props = auditmanager.CfnAssessmentProps(
                assessment_reports_destination=auditmanager.CfnAssessment.AssessmentReportsDestinationProperty(
                    destination="destination",
                    destination_type="destinationType"
                ),
                aws_account=auditmanager.CfnAssessment.AWSAccountProperty(
                    email_address="emailAddress",
                    id="id",
                    name="name"
                ),
                description="description",
                framework_id="frameworkId",
                name="name",
                roles=[auditmanager.CfnAssessment.RoleProperty(
                    role_arn="roleArn",
                    role_type="roleType"
                )],
                scope=auditmanager.CfnAssessment.ScopeProperty(
                    aws_accounts=[auditmanager.CfnAssessment.AWSAccountProperty(
                        email_address="emailAddress",
                        id="id",
                        name="name"
                    )],
                    aws_services=[auditmanager.CfnAssessment.AWSServiceProperty(
                        service_name="serviceName"
                    )]
                ),
                status="status",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3fc7049eb68864442349bebdc3c029af660b53c05bc24074a1bbc7bdd4ce2e5)
            check_type(argname="argument assessment_reports_destination", value=assessment_reports_destination, expected_type=type_hints["assessment_reports_destination"])
            check_type(argname="argument aws_account", value=aws_account, expected_type=type_hints["aws_account"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument framework_id", value=framework_id, expected_type=type_hints["framework_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assessment_reports_destination is not None:
            self._values["assessment_reports_destination"] = assessment_reports_destination
        if aws_account is not None:
            self._values["aws_account"] = aws_account
        if description is not None:
            self._values["description"] = description
        if framework_id is not None:
            self._values["framework_id"] = framework_id
        if name is not None:
            self._values["name"] = name
        if roles is not None:
            self._values["roles"] = roles
        if scope is not None:
            self._values["scope"] = scope
        if status is not None:
            self._values["status"] = status
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def assessment_reports_destination(
        self,
    ) -> typing.Optional[typing.Union[CfnAssessment.AssessmentReportsDestinationProperty, _IResolvable_a771d0ef]]:
        '''The destination that evidence reports are stored in for the assessment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-assessmentreportsdestination
        '''
        result = self._values.get("assessment_reports_destination")
        return typing.cast(typing.Optional[typing.Union[CfnAssessment.AssessmentReportsDestinationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def aws_account(
        self,
    ) -> typing.Optional[typing.Union[CfnAssessment.AWSAccountProperty, _IResolvable_a771d0ef]]:
        '''The AWS account that's associated with the assessment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-awsaccount
        '''
        result = self._values.get("aws_account")
        return typing.cast(typing.Optional[typing.Union[CfnAssessment.AWSAccountProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the assessment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def framework_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier for the framework.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-frameworkid
        '''
        result = self._values.get("framework_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the assessment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def roles(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssessment.RoleProperty, _IResolvable_a771d0ef]]]]:
        '''The roles that are associated with the assessment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-roles
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssessment.RoleProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def scope(
        self,
    ) -> typing.Optional[typing.Union[CfnAssessment.ScopeProperty, _IResolvable_a771d0ef]]:
        '''The wrapper of AWS accounts and services that are in scope for the assessment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-scope
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[typing.Union[CfnAssessment.ScopeProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The overall status of the assessment.

        When you create a new assessment, the initial ``Status`` value is always ``ACTIVE`` . When you create an assessment, even if you specify the value as ``INACTIVE`` , the value overrides to ``ACTIVE`` .

        After you create an assessment, you can change the value of the ``Status`` property at any time. For example, when you want to stop collecting evidence for your assessment, you can change the assessment status to ``INACTIVE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tags that are associated with the assessment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-auditmanager-assessment.html#cfn-auditmanager-assessment-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAssessmentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAssessment",
    "CfnAssessmentProps",
]

publication.publish()

def _typecheckingstub__5ddc2a7c4c5e4c8fe005067bda7510cf9bdda6f1f4c2a08372c4ea5523861bb7(
    scope_: _Construct_e78e779f,
    id: builtins.str,
    *,
    assessment_reports_destination: typing.Optional[typing.Union[typing.Union[CfnAssessment.AssessmentReportsDestinationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    aws_account: typing.Optional[typing.Union[typing.Union[CfnAssessment.AWSAccountProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    framework_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    roles: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAssessment.RoleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    scope: typing.Optional[typing.Union[typing.Union[CfnAssessment.ScopeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fe2b355e2afecd8c5fc82f7b521a4ead8b07f8c3feb8a9066d35291486704ee(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90693076e36d722051123d286fb1b21e9c79f8b4c0cd7d71cc68d283b901ab4a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd5af7541ac62627ea1e707bb60488ac21e64300ae54967ae86dfeda91c6b5d1(
    value: typing.Optional[typing.Union[CfnAssessment.AssessmentReportsDestinationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c39869dec454d6f66ea603119acea3e3b4f9d68386052226dd18ba44f5652162(
    value: typing.Optional[typing.Union[CfnAssessment.AWSAccountProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__373ca6f23f142bad03d21e2dfba76a274b4925d137e11d03bdb06c4955c59ee4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c98ad941eb061a54360897b49b8f7143f9d94673f7f047d810afad58791af63d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afe450a63abcf98098577db0135eee8dcab6e21f93cc3ee21557d0a1464db5f4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dabcee863f0953ab3e9f1eedf1414381a6f14b022f6044405c57bcd18b31e31f(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnAssessment.RoleProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0d6161d9f1dd28e675997e14b8ade668a3e93111500da1de7b947620b8ae3ada(
    value: typing.Optional[typing.Union[CfnAssessment.ScopeProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4207f3bb11242bae9f8cc66c065c655417eb9645b21c7f70faa41d4bf6be057d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f3d53c1a8253a3e6c1e05be11ad2c49a968187f1008deb4911b1ef7beb01a85(
    *,
    email_address: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c3efde75d6cc746097bd7036a863960aaaff1a61b025c9a88a13a123c225f83(
    *,
    service_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698d1ce4f172d51d79190336a4ddb24e8d0613290a32c45e3d362bde187f800d(
    *,
    destination: typing.Optional[builtins.str] = None,
    destination_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db2bace9243eace15e234ec8dec072be1999d574d64fb49f1309344c371dd44d(
    *,
    assessment_id: typing.Optional[builtins.str] = None,
    assessment_name: typing.Optional[builtins.str] = None,
    comment: typing.Optional[builtins.str] = None,
    control_set_id: typing.Optional[builtins.str] = None,
    created_by: typing.Optional[builtins.str] = None,
    creation_time: typing.Optional[jsii.Number] = None,
    id: typing.Optional[builtins.str] = None,
    last_updated: typing.Optional[jsii.Number] = None,
    role_arn: typing.Optional[builtins.str] = None,
    role_type: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e105064bde8034172321edae88674f09521694a7bb7f1e1a6df9dbd2ca987ec0(
    *,
    role_arn: typing.Optional[builtins.str] = None,
    role_type: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59d7f15efdaf6c609c1995ba40aed7122761b80061e0fc3918e33393844ab0be(
    *,
    aws_accounts: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAssessment.AWSAccountProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    aws_services: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAssessment.AWSServiceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3fc7049eb68864442349bebdc3c029af660b53c05bc24074a1bbc7bdd4ce2e5(
    *,
    assessment_reports_destination: typing.Optional[typing.Union[typing.Union[CfnAssessment.AssessmentReportsDestinationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    aws_account: typing.Optional[typing.Union[typing.Union[CfnAssessment.AWSAccountProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    framework_id: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    roles: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnAssessment.RoleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    scope: typing.Optional[typing.Union[typing.Union[CfnAssessment.ScopeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    status: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
