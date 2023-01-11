'''
# AWS::ManagedBlockchain Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as managedblockchain
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for ManagedBlockchain construct libraries](https://constructs.dev/search?q=managedblockchain)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::ManagedBlockchain resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ManagedBlockchain.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::ManagedBlockchain](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_ManagedBlockchain.html).

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
class CfnMember(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_managedblockchain.CfnMember",
):
    '''A CloudFormation ``AWS::ManagedBlockchain::Member``.

    Creates a member within a Managed Blockchain network.

    Applies only to Hyperledger Fabric.

    :cloudformationResource: AWS::ManagedBlockchain::Member
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_managedblockchain as managedblockchain
        
        cfn_member = managedblockchain.CfnMember(self, "MyCfnMember",
            member_configuration=managedblockchain.CfnMember.MemberConfigurationProperty(
                name="name",
        
                # the properties below are optional
                description="description",
                member_framework_configuration=managedblockchain.CfnMember.MemberFrameworkConfigurationProperty(
                    member_fabric_configuration=managedblockchain.CfnMember.MemberFabricConfigurationProperty(
                        admin_password="adminPassword",
                        admin_username="adminUsername"
                    )
                )
            ),
        
            # the properties below are optional
            invitation_id="invitationId",
            network_configuration=managedblockchain.CfnMember.NetworkConfigurationProperty(
                framework="framework",
                framework_version="frameworkVersion",
                name="name",
                voting_policy=managedblockchain.CfnMember.VotingPolicyProperty(
                    approval_threshold_policy=managedblockchain.CfnMember.ApprovalThresholdPolicyProperty(
                        proposal_duration_in_hours=123,
                        threshold_comparator="thresholdComparator",
                        threshold_percentage=123
                    )
                ),
        
                # the properties below are optional
                description="description",
                network_framework_configuration=managedblockchain.CfnMember.NetworkFrameworkConfigurationProperty(
                    network_fabric_configuration=managedblockchain.CfnMember.NetworkFabricConfigurationProperty(
                        edition="edition"
                    )
                )
            ),
            network_id="networkId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        member_configuration: typing.Union[typing.Union["CfnMember.MemberConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        invitation_id: typing.Optional[builtins.str] = None,
        network_configuration: typing.Optional[typing.Union[typing.Union["CfnMember.NetworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ManagedBlockchain::Member``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param member_configuration: Configuration properties of the member.
        :param invitation_id: The unique identifier of the invitation to join the network sent to the account that creates the member.
        :param network_configuration: Configuration properties of the network to which the member belongs.
        :param network_id: The unique identifier of the network to which the member belongs.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8cfee29f1116bb6b509cb5c7cfe1992d32e19937aed0a7de5ecd7b532a5b1cb5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnMemberProps(
            member_configuration=member_configuration,
            invitation_id=invitation_id,
            network_configuration=network_configuration,
            network_id=network_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbedbd659a858c92f1629b1aedabca5a85571fa37897933f5934ce41f8c2767c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a8cccfb6019b43abfa9c19870cca2ef52f9a332d3402026ac415625924b9061a)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrMemberId")
    def attr_member_id(self) -> builtins.str:
        '''The unique identifier of the member.

        :cloudformationAttribute: MemberId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMemberId"))

    @builtins.property
    @jsii.member(jsii_name="attrNetworkId")
    def attr_network_id(self) -> builtins.str:
        '''The unique identifier of the network to which the member belongs.

        :cloudformationAttribute: NetworkId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrNetworkId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="memberConfiguration")
    def member_configuration(
        self,
    ) -> typing.Union["CfnMember.MemberConfigurationProperty", _IResolvable_a771d0ef]:
        '''Configuration properties of the member.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-memberconfiguration
        '''
        return typing.cast(typing.Union["CfnMember.MemberConfigurationProperty", _IResolvable_a771d0ef], jsii.get(self, "memberConfiguration"))

    @member_configuration.setter
    def member_configuration(
        self,
        value: typing.Union["CfnMember.MemberConfigurationProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__264a5d9ede8749202789096ed42559332694c12ea0d15f27deade65d54c1f527)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="invitationId")
    def invitation_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the invitation to join the network sent to the account that creates the member.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-invitationid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "invitationId"))

    @invitation_id.setter
    def invitation_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6421351a23b1a38dd05202341e55c0a07a4c91f360c5c5d1eac99b04b7133945)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "invitationId", value)

    @builtins.property
    @jsii.member(jsii_name="networkConfiguration")
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union["CfnMember.NetworkConfigurationProperty", _IResolvable_a771d0ef]]:
        '''Configuration properties of the network to which the member belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-networkconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union["CfnMember.NetworkConfigurationProperty", _IResolvable_a771d0ef]], jsii.get(self, "networkConfiguration"))

    @network_configuration.setter
    def network_configuration(
        self,
        value: typing.Optional[typing.Union["CfnMember.NetworkConfigurationProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07a21544c4d2785cbb58773e55aa8c6944eeb5250e7f84ba70543d56b39fabea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the network to which the member belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-networkid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "networkId"))

    @network_id.setter
    def network_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cca2ddb844bea04e0a2e47b730a9f24492acd518e6f8b1a0396651d403b5751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkId", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_managedblockchain.CfnMember.ApprovalThresholdPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "proposal_duration_in_hours": "proposalDurationInHours",
            "threshold_comparator": "thresholdComparator",
            "threshold_percentage": "thresholdPercentage",
        },
    )
    class ApprovalThresholdPolicyProperty:
        def __init__(
            self,
            *,
            proposal_duration_in_hours: typing.Optional[jsii.Number] = None,
            threshold_comparator: typing.Optional[builtins.str] = None,
            threshold_percentage: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''A policy type that defines the voting rules for the network.

            The rules decide if a proposal is approved. Approval may be based on criteria such as the percentage of ``YES`` votes and the duration of the proposal. The policy applies to all proposals and is specified when the network is created.

            Applies only to Hyperledger Fabric.

            :param proposal_duration_in_hours: The duration from the time that a proposal is created until it expires. If members cast neither the required number of ``YES`` votes to approve the proposal nor the number of ``NO`` votes required to reject it before the duration expires, the proposal is ``EXPIRED`` and ``ProposalActions`` aren't carried out.
            :param threshold_comparator: Determines whether the vote percentage must be greater than the ``ThresholdPercentage`` or must be greater than or equal to the ``ThreholdPercentage`` to be approved.
            :param threshold_percentage: The percentage of votes among all members that must be ``YES`` for a proposal to be approved. For example, a ``ThresholdPercentage`` value of ``50`` indicates 50%. The ``ThresholdComparator`` determines the precise comparison. If a ``ThresholdPercentage`` value of ``50`` is specified on a network with 10 members, along with a ``ThresholdComparator`` value of ``GREATER_THAN`` , this indicates that 6 ``YES`` votes are required for the proposal to be approved.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-approvalthresholdpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_managedblockchain as managedblockchain
                
                approval_threshold_policy_property = managedblockchain.CfnMember.ApprovalThresholdPolicyProperty(
                    proposal_duration_in_hours=123,
                    threshold_comparator="thresholdComparator",
                    threshold_percentage=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__65d367560b992035e3dc5f58fcefd30b78efe6c515f17db5883f194e2e8969b7)
                check_type(argname="argument proposal_duration_in_hours", value=proposal_duration_in_hours, expected_type=type_hints["proposal_duration_in_hours"])
                check_type(argname="argument threshold_comparator", value=threshold_comparator, expected_type=type_hints["threshold_comparator"])
                check_type(argname="argument threshold_percentage", value=threshold_percentage, expected_type=type_hints["threshold_percentage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if proposal_duration_in_hours is not None:
                self._values["proposal_duration_in_hours"] = proposal_duration_in_hours
            if threshold_comparator is not None:
                self._values["threshold_comparator"] = threshold_comparator
            if threshold_percentage is not None:
                self._values["threshold_percentage"] = threshold_percentage

        @builtins.property
        def proposal_duration_in_hours(self) -> typing.Optional[jsii.Number]:
            '''The duration from the time that a proposal is created until it expires.

            If members cast neither the required number of ``YES`` votes to approve the proposal nor the number of ``NO`` votes required to reject it before the duration expires, the proposal is ``EXPIRED`` and ``ProposalActions`` aren't carried out.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-approvalthresholdpolicy.html#cfn-managedblockchain-member-approvalthresholdpolicy-proposaldurationinhours
            '''
            result = self._values.get("proposal_duration_in_hours")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def threshold_comparator(self) -> typing.Optional[builtins.str]:
            '''Determines whether the vote percentage must be greater than the ``ThresholdPercentage`` or must be greater than or equal to the ``ThreholdPercentage`` to be approved.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-approvalthresholdpolicy.html#cfn-managedblockchain-member-approvalthresholdpolicy-thresholdcomparator
            '''
            result = self._values.get("threshold_comparator")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def threshold_percentage(self) -> typing.Optional[jsii.Number]:
            '''The percentage of votes among all members that must be ``YES`` for a proposal to be approved.

            For example, a ``ThresholdPercentage`` value of ``50`` indicates 50%. The ``ThresholdComparator`` determines the precise comparison. If a ``ThresholdPercentage`` value of ``50`` is specified on a network with 10 members, along with a ``ThresholdComparator`` value of ``GREATER_THAN`` , this indicates that 6 ``YES`` votes are required for the proposal to be approved.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-approvalthresholdpolicy.html#cfn-managedblockchain-member-approvalthresholdpolicy-thresholdpercentage
            '''
            result = self._values.get("threshold_percentage")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ApprovalThresholdPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_managedblockchain.CfnMember.MemberConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "name": "name",
            "description": "description",
            "member_framework_configuration": "memberFrameworkConfiguration",
        },
    )
    class MemberConfigurationProperty:
        def __init__(
            self,
            *,
            name: builtins.str,
            description: typing.Optional[builtins.str] = None,
            member_framework_configuration: typing.Optional[typing.Union[typing.Union["CfnMember.MemberFrameworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Configuration properties of the member.

            Applies only to Hyperledger Fabric.

            :param name: The name of the member.
            :param description: An optional description of the member.
            :param member_framework_configuration: Configuration properties of the blockchain framework relevant to the member.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_managedblockchain as managedblockchain
                
                member_configuration_property = managedblockchain.CfnMember.MemberConfigurationProperty(
                    name="name",
                
                    # the properties below are optional
                    description="description",
                    member_framework_configuration=managedblockchain.CfnMember.MemberFrameworkConfigurationProperty(
                        member_fabric_configuration=managedblockchain.CfnMember.MemberFabricConfigurationProperty(
                            admin_password="adminPassword",
                            admin_username="adminUsername"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__83436c16086aa0d329b5946e650594574915f8d68d9e1795647c45f1f38525fd)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument member_framework_configuration", value=member_framework_configuration, expected_type=type_hints["member_framework_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
            }
            if description is not None:
                self._values["description"] = description
            if member_framework_configuration is not None:
                self._values["member_framework_configuration"] = member_framework_configuration

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the member.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberconfiguration.html#cfn-managedblockchain-member-memberconfiguration-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''An optional description of the member.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberconfiguration.html#cfn-managedblockchain-member-memberconfiguration-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def member_framework_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnMember.MemberFrameworkConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Configuration properties of the blockchain framework relevant to the member.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberconfiguration.html#cfn-managedblockchain-member-memberconfiguration-memberframeworkconfiguration
            '''
            result = self._values.get("member_framework_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnMember.MemberFrameworkConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemberConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_managedblockchain.CfnMember.MemberFabricConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "admin_password": "adminPassword",
            "admin_username": "adminUsername",
        },
    )
    class MemberFabricConfigurationProperty:
        def __init__(
            self,
            *,
            admin_password: builtins.str,
            admin_username: builtins.str,
        ) -> None:
            '''Configuration properties for Hyperledger Fabric for a member in a Managed Blockchain network using the Hyperledger Fabric framework.

            :param admin_password: The password for the member's initial administrative user. The ``AdminPassword`` must be at least eight characters long and no more than 32 characters. It must contain at least one uppercase letter, one lowercase letter, and one digit. It cannot have a single quotation mark (‘), a double quotation marks (“), a forward slash(/), a backward slash(), @, or a space.
            :param admin_username: The user name for the member's initial administrative user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberfabricconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_managedblockchain as managedblockchain
                
                member_fabric_configuration_property = managedblockchain.CfnMember.MemberFabricConfigurationProperty(
                    admin_password="adminPassword",
                    admin_username="adminUsername"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d6ef6d712aba12c35d372d9a6eae99d64b4aabb1e949d0dfc19ac42d3ae75ad9)
                check_type(argname="argument admin_password", value=admin_password, expected_type=type_hints["admin_password"])
                check_type(argname="argument admin_username", value=admin_username, expected_type=type_hints["admin_username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "admin_password": admin_password,
                "admin_username": admin_username,
            }

        @builtins.property
        def admin_password(self) -> builtins.str:
            '''The password for the member's initial administrative user.

            The ``AdminPassword`` must be at least eight characters long and no more than 32 characters. It must contain at least one uppercase letter, one lowercase letter, and one digit. It cannot have a single quotation mark (‘), a double quotation marks (“), a forward slash(/), a backward slash(), @, or a space.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberfabricconfiguration.html#cfn-managedblockchain-member-memberfabricconfiguration-adminpassword
            '''
            result = self._values.get("admin_password")
            assert result is not None, "Required property 'admin_password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def admin_username(self) -> builtins.str:
            '''The user name for the member's initial administrative user.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberfabricconfiguration.html#cfn-managedblockchain-member-memberfabricconfiguration-adminusername
            '''
            result = self._values.get("admin_username")
            assert result is not None, "Required property 'admin_username' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemberFabricConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_managedblockchain.CfnMember.MemberFrameworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"member_fabric_configuration": "memberFabricConfiguration"},
    )
    class MemberFrameworkConfigurationProperty:
        def __init__(
            self,
            *,
            member_fabric_configuration: typing.Optional[typing.Union[typing.Union["CfnMember.MemberFabricConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Configuration properties relevant to a member for the blockchain framework that the Managed Blockchain network uses.

            :param member_fabric_configuration: Configuration properties for Hyperledger Fabric.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberframeworkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_managedblockchain as managedblockchain
                
                member_framework_configuration_property = managedblockchain.CfnMember.MemberFrameworkConfigurationProperty(
                    member_fabric_configuration=managedblockchain.CfnMember.MemberFabricConfigurationProperty(
                        admin_password="adminPassword",
                        admin_username="adminUsername"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1675cc99206bbb6f8171f46a8f286ec13af40659109cc2f410747073f42a2392)
                check_type(argname="argument member_fabric_configuration", value=member_fabric_configuration, expected_type=type_hints["member_fabric_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if member_fabric_configuration is not None:
                self._values["member_fabric_configuration"] = member_fabric_configuration

        @builtins.property
        def member_fabric_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnMember.MemberFabricConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Configuration properties for Hyperledger Fabric.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-memberframeworkconfiguration.html#cfn-managedblockchain-member-memberframeworkconfiguration-memberfabricconfiguration
            '''
            result = self._values.get("member_fabric_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnMember.MemberFabricConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MemberFrameworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_managedblockchain.CfnMember.NetworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "framework": "framework",
            "framework_version": "frameworkVersion",
            "name": "name",
            "voting_policy": "votingPolicy",
            "description": "description",
            "network_framework_configuration": "networkFrameworkConfiguration",
        },
    )
    class NetworkConfigurationProperty:
        def __init__(
            self,
            *,
            framework: builtins.str,
            framework_version: builtins.str,
            name: builtins.str,
            voting_policy: typing.Union[typing.Union["CfnMember.VotingPolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            description: typing.Optional[builtins.str] = None,
            network_framework_configuration: typing.Optional[typing.Union[typing.Union["CfnMember.NetworkFrameworkConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Configuration properties of the network to which the member belongs.

            :param framework: The blockchain framework that the network uses.
            :param framework_version: The version of the blockchain framework that the network uses.
            :param name: The name of the network.
            :param voting_policy: The voting rules for the network to decide if a proposal is accepted.
            :param description: Attributes of the blockchain framework for the network.
            :param network_framework_configuration: Configuration properties relevant to the network for the blockchain framework that the network uses.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_managedblockchain as managedblockchain
                
                network_configuration_property = managedblockchain.CfnMember.NetworkConfigurationProperty(
                    framework="framework",
                    framework_version="frameworkVersion",
                    name="name",
                    voting_policy=managedblockchain.CfnMember.VotingPolicyProperty(
                        approval_threshold_policy=managedblockchain.CfnMember.ApprovalThresholdPolicyProperty(
                            proposal_duration_in_hours=123,
                            threshold_comparator="thresholdComparator",
                            threshold_percentage=123
                        )
                    ),
                
                    # the properties below are optional
                    description="description",
                    network_framework_configuration=managedblockchain.CfnMember.NetworkFrameworkConfigurationProperty(
                        network_fabric_configuration=managedblockchain.CfnMember.NetworkFabricConfigurationProperty(
                            edition="edition"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4777b3391b4ce1f9379908a459118d185619204c9b6cf6b09fa96953caca47a6)
                check_type(argname="argument framework", value=framework, expected_type=type_hints["framework"])
                check_type(argname="argument framework_version", value=framework_version, expected_type=type_hints["framework_version"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument voting_policy", value=voting_policy, expected_type=type_hints["voting_policy"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument network_framework_configuration", value=network_framework_configuration, expected_type=type_hints["network_framework_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "framework": framework,
                "framework_version": framework_version,
                "name": name,
                "voting_policy": voting_policy,
            }
            if description is not None:
                self._values["description"] = description
            if network_framework_configuration is not None:
                self._values["network_framework_configuration"] = network_framework_configuration

        @builtins.property
        def framework(self) -> builtins.str:
            '''The blockchain framework that the network uses.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-framework
            '''
            result = self._values.get("framework")
            assert result is not None, "Required property 'framework' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def framework_version(self) -> builtins.str:
            '''The version of the blockchain framework that the network uses.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-frameworkversion
            '''
            result = self._values.get("framework_version")
            assert result is not None, "Required property 'framework_version' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the network.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def voting_policy(
            self,
        ) -> typing.Union["CfnMember.VotingPolicyProperty", _IResolvable_a771d0ef]:
            '''The voting rules for the network to decide if a proposal is accepted.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-votingpolicy
            '''
            result = self._values.get("voting_policy")
            assert result is not None, "Required property 'voting_policy' is missing"
            return typing.cast(typing.Union["CfnMember.VotingPolicyProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''Attributes of the blockchain framework for the network.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def network_framework_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnMember.NetworkFrameworkConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Configuration properties relevant to the network for the blockchain framework that the network uses.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkconfiguration.html#cfn-managedblockchain-member-networkconfiguration-networkframeworkconfiguration
            '''
            result = self._values.get("network_framework_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnMember.NetworkFrameworkConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_managedblockchain.CfnMember.NetworkFabricConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"edition": "edition"},
    )
    class NetworkFabricConfigurationProperty:
        def __init__(self, *, edition: builtins.str) -> None:
            '''Hyperledger Fabric configuration properties for the network.

            :param edition: The edition of Amazon Managed Blockchain that the network uses. Valid values are ``standard`` and ``starter`` . For more information, see

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkfabricconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_managedblockchain as managedblockchain
                
                network_fabric_configuration_property = managedblockchain.CfnMember.NetworkFabricConfigurationProperty(
                    edition="edition"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__52213b332cf3ec10f949629374ae5ba52a13ff143d7af9694a9dea8695148ad1)
                check_type(argname="argument edition", value=edition, expected_type=type_hints["edition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "edition": edition,
            }

        @builtins.property
        def edition(self) -> builtins.str:
            '''The edition of Amazon Managed Blockchain that the network uses.

            Valid values are ``standard`` and ``starter`` . For more information, see

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkfabricconfiguration.html#cfn-managedblockchain-member-networkfabricconfiguration-edition
            '''
            result = self._values.get("edition")
            assert result is not None, "Required property 'edition' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkFabricConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_managedblockchain.CfnMember.NetworkFrameworkConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"network_fabric_configuration": "networkFabricConfiguration"},
    )
    class NetworkFrameworkConfigurationProperty:
        def __init__(
            self,
            *,
            network_fabric_configuration: typing.Optional[typing.Union[typing.Union["CfnMember.NetworkFabricConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Configuration properties relevant to the network for the blockchain framework that the network uses.

            :param network_fabric_configuration: Configuration properties for Hyperledger Fabric for a member in a Managed Blockchain network using the Hyperledger Fabric framework.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkframeworkconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_managedblockchain as managedblockchain
                
                network_framework_configuration_property = managedblockchain.CfnMember.NetworkFrameworkConfigurationProperty(
                    network_fabric_configuration=managedblockchain.CfnMember.NetworkFabricConfigurationProperty(
                        edition="edition"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3cb328d4b11543a2173f5eaa042655196c21021c3f11497f9526bd3d420d4679)
                check_type(argname="argument network_fabric_configuration", value=network_fabric_configuration, expected_type=type_hints["network_fabric_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if network_fabric_configuration is not None:
                self._values["network_fabric_configuration"] = network_fabric_configuration

        @builtins.property
        def network_fabric_configuration(
            self,
        ) -> typing.Optional[typing.Union["CfnMember.NetworkFabricConfigurationProperty", _IResolvable_a771d0ef]]:
            '''Configuration properties for Hyperledger Fabric for a member in a Managed Blockchain network using the Hyperledger Fabric framework.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-networkframeworkconfiguration.html#cfn-managedblockchain-member-networkframeworkconfiguration-networkfabricconfiguration
            '''
            result = self._values.get("network_fabric_configuration")
            return typing.cast(typing.Optional[typing.Union["CfnMember.NetworkFabricConfigurationProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkFrameworkConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_managedblockchain.CfnMember.VotingPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"approval_threshold_policy": "approvalThresholdPolicy"},
    )
    class VotingPolicyProperty:
        def __init__(
            self,
            *,
            approval_threshold_policy: typing.Optional[typing.Union[typing.Union["CfnMember.ApprovalThresholdPolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''The voting rules for the network to decide if a proposal is accepted.

            Applies only to Hyperledger Fabric.

            :param approval_threshold_policy: Defines the rules for the network for voting on proposals, such as the percentage of ``YES`` votes required for the proposal to be approved and the duration of the proposal. The policy applies to all proposals and is specified when the network is created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-votingpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_managedblockchain as managedblockchain
                
                voting_policy_property = managedblockchain.CfnMember.VotingPolicyProperty(
                    approval_threshold_policy=managedblockchain.CfnMember.ApprovalThresholdPolicyProperty(
                        proposal_duration_in_hours=123,
                        threshold_comparator="thresholdComparator",
                        threshold_percentage=123
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a2ff786c308fa0073228b5b8564124f27f65b283be2c73e43b22186fccfdda04)
                check_type(argname="argument approval_threshold_policy", value=approval_threshold_policy, expected_type=type_hints["approval_threshold_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if approval_threshold_policy is not None:
                self._values["approval_threshold_policy"] = approval_threshold_policy

        @builtins.property
        def approval_threshold_policy(
            self,
        ) -> typing.Optional[typing.Union["CfnMember.ApprovalThresholdPolicyProperty", _IResolvable_a771d0ef]]:
            '''Defines the rules for the network for voting on proposals, such as the percentage of ``YES`` votes required for the proposal to be approved and the duration of the proposal.

            The policy applies to all proposals and is specified when the network is created.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-member-votingpolicy.html#cfn-managedblockchain-member-votingpolicy-approvalthresholdpolicy
            '''
            result = self._values.get("approval_threshold_policy")
            return typing.cast(typing.Optional[typing.Union["CfnMember.ApprovalThresholdPolicyProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "VotingPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_managedblockchain.CfnMemberProps",
    jsii_struct_bases=[],
    name_mapping={
        "member_configuration": "memberConfiguration",
        "invitation_id": "invitationId",
        "network_configuration": "networkConfiguration",
        "network_id": "networkId",
    },
)
class CfnMemberProps:
    def __init__(
        self,
        *,
        member_configuration: typing.Union[typing.Union[CfnMember.MemberConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        invitation_id: typing.Optional[builtins.str] = None,
        network_configuration: typing.Optional[typing.Union[typing.Union[CfnMember.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        network_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnMember``.

        :param member_configuration: Configuration properties of the member.
        :param invitation_id: The unique identifier of the invitation to join the network sent to the account that creates the member.
        :param network_configuration: Configuration properties of the network to which the member belongs.
        :param network_id: The unique identifier of the network to which the member belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_managedblockchain as managedblockchain
            
            cfn_member_props = managedblockchain.CfnMemberProps(
                member_configuration=managedblockchain.CfnMember.MemberConfigurationProperty(
                    name="name",
            
                    # the properties below are optional
                    description="description",
                    member_framework_configuration=managedblockchain.CfnMember.MemberFrameworkConfigurationProperty(
                        member_fabric_configuration=managedblockchain.CfnMember.MemberFabricConfigurationProperty(
                            admin_password="adminPassword",
                            admin_username="adminUsername"
                        )
                    )
                ),
            
                # the properties below are optional
                invitation_id="invitationId",
                network_configuration=managedblockchain.CfnMember.NetworkConfigurationProperty(
                    framework="framework",
                    framework_version="frameworkVersion",
                    name="name",
                    voting_policy=managedblockchain.CfnMember.VotingPolicyProperty(
                        approval_threshold_policy=managedblockchain.CfnMember.ApprovalThresholdPolicyProperty(
                            proposal_duration_in_hours=123,
                            threshold_comparator="thresholdComparator",
                            threshold_percentage=123
                        )
                    ),
            
                    # the properties below are optional
                    description="description",
                    network_framework_configuration=managedblockchain.CfnMember.NetworkFrameworkConfigurationProperty(
                        network_fabric_configuration=managedblockchain.CfnMember.NetworkFabricConfigurationProperty(
                            edition="edition"
                        )
                    )
                ),
                network_id="networkId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c94af3f35408bdaae0f4edeec602bdc350aa0d69fd1d1a9f0b933510cf48ef26)
            check_type(argname="argument member_configuration", value=member_configuration, expected_type=type_hints["member_configuration"])
            check_type(argname="argument invitation_id", value=invitation_id, expected_type=type_hints["invitation_id"])
            check_type(argname="argument network_configuration", value=network_configuration, expected_type=type_hints["network_configuration"])
            check_type(argname="argument network_id", value=network_id, expected_type=type_hints["network_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "member_configuration": member_configuration,
        }
        if invitation_id is not None:
            self._values["invitation_id"] = invitation_id
        if network_configuration is not None:
            self._values["network_configuration"] = network_configuration
        if network_id is not None:
            self._values["network_id"] = network_id

    @builtins.property
    def member_configuration(
        self,
    ) -> typing.Union[CfnMember.MemberConfigurationProperty, _IResolvable_a771d0ef]:
        '''Configuration properties of the member.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-memberconfiguration
        '''
        result = self._values.get("member_configuration")
        assert result is not None, "Required property 'member_configuration' is missing"
        return typing.cast(typing.Union[CfnMember.MemberConfigurationProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def invitation_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the invitation to join the network sent to the account that creates the member.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-invitationid
        '''
        result = self._values.get("invitation_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_configuration(
        self,
    ) -> typing.Optional[typing.Union[CfnMember.NetworkConfigurationProperty, _IResolvable_a771d0ef]]:
        '''Configuration properties of the network to which the member belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-networkconfiguration
        '''
        result = self._values.get("network_configuration")
        return typing.cast(typing.Optional[typing.Union[CfnMember.NetworkConfigurationProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def network_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the network to which the member belongs.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-member.html#cfn-managedblockchain-member-networkid
        '''
        result = self._values.get("network_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnMemberProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnNode(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_managedblockchain.CfnNode",
):
    '''A CloudFormation ``AWS::ManagedBlockchain::Node``.

    Creates a node on the specified blockchain network.

    Applies to Hyperledger Fabric and Ethereum.

    :cloudformationResource: AWS::ManagedBlockchain::Node
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_managedblockchain as managedblockchain
        
        cfn_node = managedblockchain.CfnNode(self, "MyCfnNode",
            network_id="networkId",
            node_configuration=managedblockchain.CfnNode.NodeConfigurationProperty(
                availability_zone="availabilityZone",
                instance_type="instanceType"
            ),
        
            # the properties below are optional
            member_id="memberId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        network_id: builtins.str,
        node_configuration: typing.Union[typing.Union["CfnNode.NodeConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        member_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::ManagedBlockchain::Node``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param network_id: The unique identifier of the network for the node. Ethereum public networks have the following ``NetworkId`` s: - ``n-ethereum-mainnet`` - ``n-ethereum-goerli`` - ``n-ethereum-rinkeby`` - ``n-ethereum-ropsten``
        :param node_configuration: Configuration properties of a peer node.
        :param member_id: The unique identifier of the member to which the node belongs. Applies only to Hyperledger Fabric.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cd4926d9a6a7b2576ca5d2a8bd85fb98de1a38002bcecf7d160f6f83b41def4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnNodeProps(
            network_id=network_id,
            node_configuration=node_configuration,
            member_id=member_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2fda544d717da097c01d18594df46fd8f44589ce56d9cf8de7172747befc741)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3bf5310208a3a0ff843c1aa06b3f58c131c1742f93fd86fa8ba78c1fad95efad)
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
        '''The Amazon Resource Name (ARN) of the node.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrMemberId")
    def attr_member_id(self) -> builtins.str:
        '''The unique identifier of the member in which the node is created.

        Applies only to Hyperledger Fabric.

        :cloudformationAttribute: MemberId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrMemberId"))

    @builtins.property
    @jsii.member(jsii_name="attrNetworkId")
    def attr_network_id(self) -> builtins.str:
        '''The unique identifier of the network that the node is in.

        :cloudformationAttribute: NetworkId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrNetworkId"))

    @builtins.property
    @jsii.member(jsii_name="attrNodeId")
    def attr_node_id(self) -> builtins.str:
        '''The unique identifier of the node.

        :cloudformationAttribute: NodeId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrNodeId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="networkId")
    def network_id(self) -> builtins.str:
        '''The unique identifier of the network for the node.

        Ethereum public networks have the following ``NetworkId`` s:

        - ``n-ethereum-mainnet``
        - ``n-ethereum-goerli``
        - ``n-ethereum-rinkeby``
        - ``n-ethereum-ropsten``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html#cfn-managedblockchain-node-networkid
        '''
        return typing.cast(builtins.str, jsii.get(self, "networkId"))

    @network_id.setter
    def network_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32a8c73530f5c1d357455bb71c64ea235ec26adc036b638b1336132f967a35c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "networkId", value)

    @builtins.property
    @jsii.member(jsii_name="nodeConfiguration")
    def node_configuration(
        self,
    ) -> typing.Union["CfnNode.NodeConfigurationProperty", _IResolvable_a771d0ef]:
        '''Configuration properties of a peer node.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html#cfn-managedblockchain-node-nodeconfiguration
        '''
        return typing.cast(typing.Union["CfnNode.NodeConfigurationProperty", _IResolvable_a771d0ef], jsii.get(self, "nodeConfiguration"))

    @node_configuration.setter
    def node_configuration(
        self,
        value: typing.Union["CfnNode.NodeConfigurationProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ee820e59563987094ad1797c831d0e0f44cb9bf83d2837ed169f52a462ad0fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "nodeConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="memberId")
    def member_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the member to which the node belongs.

        Applies only to Hyperledger Fabric.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html#cfn-managedblockchain-node-memberid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "memberId"))

    @member_id.setter
    def member_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be5805f480504385ec7817467e29411741f8788846daa70986842c0a1723cc1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "memberId", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_managedblockchain.CfnNode.NodeConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "availability_zone": "availabilityZone",
            "instance_type": "instanceType",
        },
    )
    class NodeConfigurationProperty:
        def __init__(
            self,
            *,
            availability_zone: builtins.str,
            instance_type: builtins.str,
        ) -> None:
            '''Configuration properties of a peer node within a membership.

            :param availability_zone: The Availability Zone in which the node exists. Required for Ethereum nodes.
            :param instance_type: The Amazon Managed Blockchain instance type for the node.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-node-nodeconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_managedblockchain as managedblockchain
                
                node_configuration_property = managedblockchain.CfnNode.NodeConfigurationProperty(
                    availability_zone="availabilityZone",
                    instance_type="instanceType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__80b4acab77e57c970ae95d3ac96c1215b2207998deb925a73b39f17bc6cad44c)
                check_type(argname="argument availability_zone", value=availability_zone, expected_type=type_hints["availability_zone"])
                check_type(argname="argument instance_type", value=instance_type, expected_type=type_hints["instance_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "availability_zone": availability_zone,
                "instance_type": instance_type,
            }

        @builtins.property
        def availability_zone(self) -> builtins.str:
            '''The Availability Zone in which the node exists.

            Required for Ethereum nodes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-node-nodeconfiguration.html#cfn-managedblockchain-node-nodeconfiguration-availabilityzone
            '''
            result = self._values.get("availability_zone")
            assert result is not None, "Required property 'availability_zone' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def instance_type(self) -> builtins.str:
            '''The Amazon Managed Blockchain instance type for the node.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-managedblockchain-node-nodeconfiguration.html#cfn-managedblockchain-node-nodeconfiguration-instancetype
            '''
            result = self._values.get("instance_type")
            assert result is not None, "Required property 'instance_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NodeConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_managedblockchain.CfnNodeProps",
    jsii_struct_bases=[],
    name_mapping={
        "network_id": "networkId",
        "node_configuration": "nodeConfiguration",
        "member_id": "memberId",
    },
)
class CfnNodeProps:
    def __init__(
        self,
        *,
        network_id: builtins.str,
        node_configuration: typing.Union[typing.Union[CfnNode.NodeConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        member_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnNode``.

        :param network_id: The unique identifier of the network for the node. Ethereum public networks have the following ``NetworkId`` s: - ``n-ethereum-mainnet`` - ``n-ethereum-goerli`` - ``n-ethereum-rinkeby`` - ``n-ethereum-ropsten``
        :param node_configuration: Configuration properties of a peer node.
        :param member_id: The unique identifier of the member to which the node belongs. Applies only to Hyperledger Fabric.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_managedblockchain as managedblockchain
            
            cfn_node_props = managedblockchain.CfnNodeProps(
                network_id="networkId",
                node_configuration=managedblockchain.CfnNode.NodeConfigurationProperty(
                    availability_zone="availabilityZone",
                    instance_type="instanceType"
                ),
            
                # the properties below are optional
                member_id="memberId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3fbb2a52dddb90d47f0d9dd09abf78d6a5802e5af111598a72f9671a7d54a66c)
            check_type(argname="argument network_id", value=network_id, expected_type=type_hints["network_id"])
            check_type(argname="argument node_configuration", value=node_configuration, expected_type=type_hints["node_configuration"])
            check_type(argname="argument member_id", value=member_id, expected_type=type_hints["member_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "network_id": network_id,
            "node_configuration": node_configuration,
        }
        if member_id is not None:
            self._values["member_id"] = member_id

    @builtins.property
    def network_id(self) -> builtins.str:
        '''The unique identifier of the network for the node.

        Ethereum public networks have the following ``NetworkId`` s:

        - ``n-ethereum-mainnet``
        - ``n-ethereum-goerli``
        - ``n-ethereum-rinkeby``
        - ``n-ethereum-ropsten``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html#cfn-managedblockchain-node-networkid
        '''
        result = self._values.get("network_id")
        assert result is not None, "Required property 'network_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def node_configuration(
        self,
    ) -> typing.Union[CfnNode.NodeConfigurationProperty, _IResolvable_a771d0ef]:
        '''Configuration properties of a peer node.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html#cfn-managedblockchain-node-nodeconfiguration
        '''
        result = self._values.get("node_configuration")
        assert result is not None, "Required property 'node_configuration' is missing"
        return typing.cast(typing.Union[CfnNode.NodeConfigurationProperty, _IResolvable_a771d0ef], result)

    @builtins.property
    def member_id(self) -> typing.Optional[builtins.str]:
        '''The unique identifier of the member to which the node belongs.

        Applies only to Hyperledger Fabric.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-managedblockchain-node.html#cfn-managedblockchain-node-memberid
        '''
        result = self._values.get("member_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNodeProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnMember",
    "CfnMemberProps",
    "CfnNode",
    "CfnNodeProps",
]

publication.publish()

def _typecheckingstub__8cfee29f1116bb6b509cb5c7cfe1992d32e19937aed0a7de5ecd7b532a5b1cb5(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    member_configuration: typing.Union[typing.Union[CfnMember.MemberConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    invitation_id: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[typing.Union[CfnMember.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbedbd659a858c92f1629b1aedabca5a85571fa37897933f5934ce41f8c2767c(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8cccfb6019b43abfa9c19870cca2ef52f9a332d3402026ac415625924b9061a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__264a5d9ede8749202789096ed42559332694c12ea0d15f27deade65d54c1f527(
    value: typing.Union[CfnMember.MemberConfigurationProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6421351a23b1a38dd05202341e55c0a07a4c91f360c5c5d1eac99b04b7133945(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07a21544c4d2785cbb58773e55aa8c6944eeb5250e7f84ba70543d56b39fabea(
    value: typing.Optional[typing.Union[CfnMember.NetworkConfigurationProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cca2ddb844bea04e0a2e47b730a9f24492acd518e6f8b1a0396651d403b5751(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65d367560b992035e3dc5f58fcefd30b78efe6c515f17db5883f194e2e8969b7(
    *,
    proposal_duration_in_hours: typing.Optional[jsii.Number] = None,
    threshold_comparator: typing.Optional[builtins.str] = None,
    threshold_percentage: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__83436c16086aa0d329b5946e650594574915f8d68d9e1795647c45f1f38525fd(
    *,
    name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    member_framework_configuration: typing.Optional[typing.Union[typing.Union[CfnMember.MemberFrameworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ef6d712aba12c35d372d9a6eae99d64b4aabb1e949d0dfc19ac42d3ae75ad9(
    *,
    admin_password: builtins.str,
    admin_username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1675cc99206bbb6f8171f46a8f286ec13af40659109cc2f410747073f42a2392(
    *,
    member_fabric_configuration: typing.Optional[typing.Union[typing.Union[CfnMember.MemberFabricConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4777b3391b4ce1f9379908a459118d185619204c9b6cf6b09fa96953caca47a6(
    *,
    framework: builtins.str,
    framework_version: builtins.str,
    name: builtins.str,
    voting_policy: typing.Union[typing.Union[CfnMember.VotingPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    description: typing.Optional[builtins.str] = None,
    network_framework_configuration: typing.Optional[typing.Union[typing.Union[CfnMember.NetworkFrameworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52213b332cf3ec10f949629374ae5ba52a13ff143d7af9694a9dea8695148ad1(
    *,
    edition: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cb328d4b11543a2173f5eaa042655196c21021c3f11497f9526bd3d420d4679(
    *,
    network_fabric_configuration: typing.Optional[typing.Union[typing.Union[CfnMember.NetworkFabricConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2ff786c308fa0073228b5b8564124f27f65b283be2c73e43b22186fccfdda04(
    *,
    approval_threshold_policy: typing.Optional[typing.Union[typing.Union[CfnMember.ApprovalThresholdPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c94af3f35408bdaae0f4edeec602bdc350aa0d69fd1d1a9f0b933510cf48ef26(
    *,
    member_configuration: typing.Union[typing.Union[CfnMember.MemberConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    invitation_id: typing.Optional[builtins.str] = None,
    network_configuration: typing.Optional[typing.Union[typing.Union[CfnMember.NetworkConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    network_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cd4926d9a6a7b2576ca5d2a8bd85fb98de1a38002bcecf7d160f6f83b41def4(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    network_id: builtins.str,
    node_configuration: typing.Union[typing.Union[CfnNode.NodeConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    member_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2fda544d717da097c01d18594df46fd8f44589ce56d9cf8de7172747befc741(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bf5310208a3a0ff843c1aa06b3f58c131c1742f93fd86fa8ba78c1fad95efad(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32a8c73530f5c1d357455bb71c64ea235ec26adc036b638b1336132f967a35c5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ee820e59563987094ad1797c831d0e0f44cb9bf83d2837ed169f52a462ad0fb(
    value: typing.Union[CfnNode.NodeConfigurationProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be5805f480504385ec7817467e29411741f8788846daa70986842c0a1723cc1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80b4acab77e57c970ae95d3ac96c1215b2207998deb925a73b39f17bc6cad44c(
    *,
    availability_zone: builtins.str,
    instance_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3fbb2a52dddb90d47f0d9dd09abf78d6a5802e5af111598a72f9671a7d54a66c(
    *,
    network_id: builtins.str,
    node_configuration: typing.Union[typing.Union[CfnNode.NodeConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    member_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
