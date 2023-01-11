'''
# AWS::NetworkFirewall Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_networkfirewall as networkfirewall
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for NetworkFirewall construct libraries](https://constructs.dev/search?q=networkfirewall)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::NetworkFirewall resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_NetworkFirewall.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::NetworkFirewall](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_NetworkFirewall.html).

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
class CfnFirewall(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-networkfirewall.CfnFirewall",
):
    '''A CloudFormation ``AWS::NetworkFirewall::Firewall``.

    Use the ``Firewall`` to provide stateful, managed, network firewall and intrusion detection and prevention filtering for your VPCs in Amazon VPC .

    The firewall defines the configuration settings for an AWS Network Firewall firewall. The settings include the firewall policy, the subnets in your VPC to use for the firewall endpoints, and any tags that are attached to the firewall AWS resource.

    :cloudformationResource: AWS::NetworkFirewall::Firewall
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_networkfirewall as networkfirewall
        
        cfn_firewall = networkfirewall.CfnFirewall(self, "MyCfnFirewall",
            firewall_name="firewallName",
            firewall_policy_arn="firewallPolicyArn",
            subnet_mappings=[networkfirewall.CfnFirewall.SubnetMappingProperty(
                subnet_id="subnetId"
            )],
            vpc_id="vpcId",
        
            # the properties below are optional
            delete_protection=False,
            description="description",
            firewall_policy_change_protection=False,
            subnet_change_protection=False,
            tags=[CfnTag(
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
        firewall_name: builtins.str,
        firewall_policy_arn: builtins.str,
        subnet_mappings: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union["CfnFirewall.SubnetMappingProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
        vpc_id: builtins.str,
        delete_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        firewall_policy_change_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        subnet_change_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkFirewall::Firewall``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param firewall_name: The descriptive name of the firewall. You can't change the name of a firewall after you create it.
        :param firewall_policy_arn: The Amazon Resource Name (ARN) of the firewall policy. The relationship of firewall to firewall policy is many to one. Each firewall requires one firewall policy association, and you can use the same firewall policy for multiple firewalls.
        :param subnet_mappings: The public subnets that Network Firewall is using for the firewall. Each subnet must belong to a different Availability Zone.
        :param vpc_id: The unique identifier of the VPC where the firewall is in use. You can't change the VPC of a firewall after you create the firewall.
        :param delete_protection: A flag indicating whether it is possible to delete the firewall. A setting of ``TRUE`` indicates that the firewall is protected against deletion. Use this setting to protect against accidentally deleting a firewall that is in use. When you create a firewall, the operation initializes this flag to ``TRUE`` .
        :param description: A description of the firewall.
        :param firewall_policy_change_protection: A setting indicating whether the firewall is protected against a change to the firewall policy association. Use this setting to protect against accidentally modifying the firewall policy for a firewall that is in use. When you create a firewall, the operation initializes this setting to ``TRUE`` .
        :param subnet_change_protection: A setting indicating whether the firewall is protected against changes to the subnet associations. Use this setting to protect against accidentally modifying the subnet associations for a firewall that is in use. When you create a firewall, the operation initializes this setting to ``TRUE`` .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__19d1d1eee1029ee159736360c524335747587f0f06999a2fe85acfdb0f97da6c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFirewallProps(
            firewall_name=firewall_name,
            firewall_policy_arn=firewall_policy_arn,
            subnet_mappings=subnet_mappings,
            vpc_id=vpc_id,
            delete_protection=delete_protection,
            description=description,
            firewall_policy_change_protection=firewall_policy_change_protection,
            subnet_change_protection=subnet_change_protection,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59869aa0bb6cb97fdfebb8430ed49c0dd929451968db1070f7db79b00a647e69)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8b58d5426c70f688b592df1cd1b4b386c5623585eb75d076ab4ac87bfda30205)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrEndpointIds")
    def attr_endpoint_ids(self) -> typing.List[builtins.str]:
        '''The unique IDs of the firewall endpoints for all of the subnets that you attached to the firewall.

        The subnets are not listed in any particular order. For example: ``["us-west-2c:vpce-111122223333", "us-west-2a:vpce-987654321098", "us-west-2b:vpce-012345678901"]`` .

        :cloudformationAttribute: EndpointIds
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrEndpointIds"))

    @builtins.property
    @jsii.member(jsii_name="attrFirewallArn")
    def attr_firewall_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the ``Firewall`` .

        :cloudformationAttribute: FirewallArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFirewallArn"))

    @builtins.property
    @jsii.member(jsii_name="attrFirewallId")
    def attr_firewall_id(self) -> builtins.str:
        '''The name of the ``Firewall`` resource.

        :cloudformationAttribute: FirewallId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFirewallId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="firewallName")
    def firewall_name(self) -> builtins.str:
        '''The descriptive name of the firewall.

        You can't change the name of a firewall after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-firewallname
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallName"))

    @firewall_name.setter
    def firewall_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__270fafa0dd3c45e8305ece4b7d2580f9f2d9dabc51b155173d7d3cce8314fabc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallName", value)

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyArn")
    def firewall_policy_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the firewall policy.

        The relationship of firewall to firewall policy is many to one. Each firewall requires one firewall policy association, and you can use the same firewall policy for multiple firewalls.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-firewallpolicyarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallPolicyArn"))

    @firewall_policy_arn.setter
    def firewall_policy_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d06ea77cc12b80c2243d61f1c6fd8d9a144ef47da68e8acddbcb9fca72a8ec41)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallPolicyArn", value)

    @builtins.property
    @jsii.member(jsii_name="subnetMappings")
    def subnet_mappings(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnFirewall.SubnetMappingProperty", _aws_cdk_core_f4b25747.IResolvable]]]:
        '''The public subnets that Network Firewall is using for the firewall.

        Each subnet must belong to a different Availability Zone.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-subnetmappings
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnFirewall.SubnetMappingProperty", _aws_cdk_core_f4b25747.IResolvable]]], jsii.get(self, "subnetMappings"))

    @subnet_mappings.setter
    def subnet_mappings(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnFirewall.SubnetMappingProperty", _aws_cdk_core_f4b25747.IResolvable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0784dbac3cb684531ab5e0f68e51ee4bb7997ca40d9b6ad52f6b488e1c98c660)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetMappings", value)

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        '''The unique identifier of the VPC where the firewall is in use.

        You can't change the VPC of a firewall after you create the firewall.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-vpcid
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f549b9972ef4d527dbcb28beea2a346fcee8adcee9bc7079806cb32744b9da19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value)

    @builtins.property
    @jsii.member(jsii_name="deleteProtection")
    def delete_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''A flag indicating whether it is possible to delete the firewall.

        A setting of ``TRUE`` indicates that the firewall is protected against deletion. Use this setting to protect against accidentally deleting a firewall that is in use. When you create a firewall, the operation initializes this flag to ``TRUE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-deleteprotection
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "deleteProtection"))

    @delete_protection.setter
    def delete_protection(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ae0b59abc26acde625ceee70fa3cdd0d5ff5b631ea712f67aea20cf2082c433)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteProtection", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the firewall.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf7634dca0aec6a62b59436b6ff00333298e3404f37eef3ef0bc7a3225632200)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyChangeProtection")
    def firewall_policy_change_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''A setting indicating whether the firewall is protected against a change to the firewall policy association.

        Use this setting to protect against accidentally modifying the firewall policy for a firewall that is in use. When you create a firewall, the operation initializes this setting to ``TRUE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-firewallpolicychangeprotection
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "firewallPolicyChangeProtection"))

    @firewall_policy_change_protection.setter
    def firewall_policy_change_protection(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e97b4dfb5e46a42c6315101168e51b198161a393d126ecfee07b26cb98a5e805)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallPolicyChangeProtection", value)

    @builtins.property
    @jsii.member(jsii_name="subnetChangeProtection")
    def subnet_change_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''A setting indicating whether the firewall is protected against changes to the subnet associations.

        Use this setting to protect against accidentally modifying the subnet associations for a firewall that is in use. When you create a firewall, the operation initializes this setting to ``TRUE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-subnetchangeprotection
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "subnetChangeProtection"))

    @subnet_change_protection.setter
    def subnet_change_protection(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9cad9ad5362c6ca517e24ac92741c48aaf518578649900b13a9ca4b6658626b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetChangeProtection", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnFirewall.SubnetMappingProperty",
        jsii_struct_bases=[],
        name_mapping={"subnet_id": "subnetId"},
    )
    class SubnetMappingProperty:
        def __init__(self, *, subnet_id: builtins.str) -> None:
            '''The ID for a subnet that you want to associate with the firewall.

            AWS Network Firewall creates an instance of the associated firewall in each subnet that you specify, to filter traffic in the subnet's Availability Zone.

            :param subnet_id: The unique identifier for the subnet.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewall-subnetmapping.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                subnet_mapping_property = networkfirewall.CfnFirewall.SubnetMappingProperty(
                    subnet_id="subnetId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7599efdcdea45818b0009300a6f64aaa52b61f6b9cf3984a185f8db10c981d65)
                check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "subnet_id": subnet_id,
            }

        @builtins.property
        def subnet_id(self) -> builtins.str:
            '''The unique identifier for the subnet.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewall-subnetmapping.html#cfn-networkfirewall-firewall-subnetmapping-subnetid
            '''
            result = self._values.get("subnet_id")
            assert result is not None, "Required property 'subnet_id' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubnetMappingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnFirewallPolicy(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-networkfirewall.CfnFirewallPolicy",
):
    '''A CloudFormation ``AWS::NetworkFirewall::FirewallPolicy``.

    Use the ``FirewallPolicy`` to define the stateless and stateful network traffic filtering behavior for your ``Firewall`` . You can use one firewall policy for multiple firewalls.

    :cloudformationResource: AWS::NetworkFirewall::FirewallPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_networkfirewall as networkfirewall
        
        cfn_firewall_policy = networkfirewall.CfnFirewallPolicy(self, "MyCfnFirewallPolicy",
            firewall_policy=networkfirewall.CfnFirewallPolicy.FirewallPolicyProperty(
                stateless_default_actions=["statelessDefaultActions"],
                stateless_fragment_default_actions=["statelessFragmentDefaultActions"],
        
                # the properties below are optional
                stateful_default_actions=["statefulDefaultActions"],
                stateful_engine_options=networkfirewall.CfnFirewallPolicy.StatefulEngineOptionsProperty(
                    rule_order="ruleOrder",
                    stream_exception_policy="streamExceptionPolicy"
                ),
                stateful_rule_group_references=[networkfirewall.CfnFirewallPolicy.StatefulRuleGroupReferenceProperty(
                    resource_arn="resourceArn",
        
                    # the properties below are optional
                    override=networkfirewall.CfnFirewallPolicy.StatefulRuleGroupOverrideProperty(
                        action="action"
                    ),
                    priority=123
                )],
                stateless_custom_actions=[networkfirewall.CfnFirewallPolicy.CustomActionProperty(
                    action_definition=networkfirewall.CfnFirewallPolicy.ActionDefinitionProperty(
                        publish_metric_action=networkfirewall.CfnFirewallPolicy.PublishMetricActionProperty(
                            dimensions=[networkfirewall.CfnFirewallPolicy.DimensionProperty(
                                value="value"
                            )]
                        )
                    ),
                    action_name="actionName"
                )],
                stateless_rule_group_references=[networkfirewall.CfnFirewallPolicy.StatelessRuleGroupReferenceProperty(
                    priority=123,
                    resource_arn="resourceArn"
                )]
            ),
            firewall_policy_name="firewallPolicyName",
        
            # the properties below are optional
            description="description",
            tags=[CfnTag(
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
        firewall_policy: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFirewallPolicy.FirewallPolicyProperty", typing.Dict[builtins.str, typing.Any]]],
        firewall_policy_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkFirewall::FirewallPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param firewall_policy: The traffic filtering behavior of a firewall policy, defined in a collection of stateless and stateful rule groups and other settings.
        :param firewall_policy_name: The descriptive name of the firewall policy. You can't change the name of a firewall policy after you create it.
        :param description: A description of the firewall policy.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b50ce469ced2a642ad4c361981694880624b599cc8abac970b7ee5b0bf63b011)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFirewallPolicyProps(
            firewall_policy=firewall_policy,
            firewall_policy_name=firewall_policy_name,
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
            type_hints = typing.get_type_hints(_typecheckingstub__93918d09ff74a9b97c3243bcbd856a48fcd724b357eabc34fbdf05bdfcba8117)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50c894ee14c2a382e5f121cac1190bef4af46dbe84bafa65ef5902e376ba497f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrFirewallPolicyArn")
    def attr_firewall_policy_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the ``FirewallPolicy`` .

        :cloudformationAttribute: FirewallPolicyArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFirewallPolicyArn"))

    @builtins.property
    @jsii.member(jsii_name="attrFirewallPolicyId")
    def attr_firewall_policy_id(self) -> builtins.str:
        '''The unique ID of the ``FirewallPolicy`` resource.

        :cloudformationAttribute: FirewallPolicyId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrFirewallPolicyId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="firewallPolicy")
    def firewall_policy(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.FirewallPolicyProperty"]:
        '''The traffic filtering behavior of a firewall policy, defined in a collection of stateless and stateful rule groups and other settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.FirewallPolicyProperty"], jsii.get(self, "firewallPolicy"))

    @firewall_policy.setter
    def firewall_policy(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.FirewallPolicyProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f7b6a772ab37dca4dd31b3de0b4dd025d0a7c4186c0bf04033e3a2a8df835de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallPolicy", value)

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyName")
    def firewall_policy_name(self) -> builtins.str:
        '''The descriptive name of the firewall policy.

        You can't change the name of a firewall policy after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicyname
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallPolicyName"))

    @firewall_policy_name.setter
    def firewall_policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__756abcaf831c4294911d34c322c5175f7a47aa1a5d79763e55436ddc8a1d609c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallPolicyName", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the firewall policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__262499097d8e373436a55d05286c5de0c1b66bbcaf3fe7861ed2cfdbc5665de6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnFirewallPolicy.ActionDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"publish_metric_action": "publishMetricAction"},
    )
    class ActionDefinitionProperty:
        def __init__(
            self,
            *,
            publish_metric_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFirewallPolicy.PublishMetricActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A custom action to use in stateless rule actions settings.

            :param publish_metric_action: Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet. This setting defines a CloudWatch dimension value to be published. You can pair this custom action with any of the standard stateless rule actions. For example, you could pair this in a rule action with the standard action that forwards the packet for stateful inspection. Then, when a packet matches the rule, Network Firewall publishes metrics for the packet and forwards it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-actiondefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                action_definition_property = networkfirewall.CfnFirewallPolicy.ActionDefinitionProperty(
                    publish_metric_action=networkfirewall.CfnFirewallPolicy.PublishMetricActionProperty(
                        dimensions=[networkfirewall.CfnFirewallPolicy.DimensionProperty(
                            value="value"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__11547f1811f763d991008c49b2105f605a1e6d202145f1701a8043d9d43799d1)
                check_type(argname="argument publish_metric_action", value=publish_metric_action, expected_type=type_hints["publish_metric_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if publish_metric_action is not None:
                self._values["publish_metric_action"] = publish_metric_action

        @builtins.property
        def publish_metric_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.PublishMetricActionProperty"]]:
            '''Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet.

            This setting defines a CloudWatch dimension value to be published.

            You can pair this custom action with any of the standard stateless rule actions. For example, you could pair this in a rule action with the standard action that forwards the packet for stateful inspection. Then, when a packet matches the rule, Network Firewall publishes metrics for the packet and forwards it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-actiondefinition.html#cfn-networkfirewall-firewallpolicy-actiondefinition-publishmetricaction
            '''
            result = self._values.get("publish_metric_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.PublishMetricActionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnFirewallPolicy.CustomActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_definition": "actionDefinition",
            "action_name": "actionName",
        },
    )
    class CustomActionProperty:
        def __init__(
            self,
            *,
            action_definition: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFirewallPolicy.ActionDefinitionProperty", typing.Dict[builtins.str, typing.Any]]],
            action_name: builtins.str,
        ) -> None:
            '''An optional, non-standard action to use for stateless packet handling.

            You can define this in addition to the standard action that you must specify.

            You define and name the custom actions that you want to be able to use, and then you reference them by name in your actions settings.

            You can use custom actions in the following places:

            - In an ``RuleGroup.StatelessRulesAndCustomActions`` . The custom actions are available for use by name inside the ``StatelessRulesAndCustomActions`` where you define them. You can use them for your stateless rule actions to specify what to do with a packet that matches the rule's match attributes.
            - In an ``FirewallPolicy`` specification, in ``StatelessCustomActions`` . The custom actions are available for use inside the policy where you define them. You can use them for the policy's default stateless actions settings to specify what to do with packets that don't match any of the policy's stateless rules.

            :param action_definition: The custom action associated with the action name.
            :param action_name: The descriptive name of the custom action. You can't change the name of a custom action after you create it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-customaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                custom_action_property = networkfirewall.CfnFirewallPolicy.CustomActionProperty(
                    action_definition=networkfirewall.CfnFirewallPolicy.ActionDefinitionProperty(
                        publish_metric_action=networkfirewall.CfnFirewallPolicy.PublishMetricActionProperty(
                            dimensions=[networkfirewall.CfnFirewallPolicy.DimensionProperty(
                                value="value"
                            )]
                        )
                    ),
                    action_name="actionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8b9ce10ab0d6b6438ef8ea640cbe4ed46c49f9896fd22f401ba2879b26b25e11)
                check_type(argname="argument action_definition", value=action_definition, expected_type=type_hints["action_definition"])
                check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "action_definition": action_definition,
                "action_name": action_name,
            }

        @builtins.property
        def action_definition(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.ActionDefinitionProperty"]:
            '''The custom action associated with the action name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-customaction.html#cfn-networkfirewall-firewallpolicy-customaction-actiondefinition
            '''
            result = self._values.get("action_definition")
            assert result is not None, "Required property 'action_definition' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.ActionDefinitionProperty"], result)

        @builtins.property
        def action_name(self) -> builtins.str:
            '''The descriptive name of the custom action.

            You can't change the name of a custom action after you create it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-customaction.html#cfn-networkfirewall-firewallpolicy-customaction-actionname
            '''
            result = self._values.get("action_name")
            assert result is not None, "Required property 'action_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnFirewallPolicy.DimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class DimensionProperty:
        def __init__(self, *, value: builtins.str) -> None:
            '''The value to use in an Amazon CloudWatch custom metric dimension.

            This is used in the ``PublishMetrics`` custom action. A CloudWatch custom metric dimension is a name/value pair that's part of the identity of a metric.

            AWS Network Firewall sets the dimension name to ``CustomAction`` and you provide the dimension value.

            For more information about CloudWatch custom metric dimensions, see `Publishing Custom Metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html#usingDimensions>`_ in the `Amazon CloudWatch User Guide <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html>`_ .

            :param value: The value to use in the custom metric dimension.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-dimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                dimension_property = networkfirewall.CfnFirewallPolicy.DimensionProperty(
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0a1c6debb532cadac4392a092e05dcab35b9e445b2f53b7c3394ded2aac0a7b1)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "value": value,
            }

        @builtins.property
        def value(self) -> builtins.str:
            '''The value to use in the custom metric dimension.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-dimension.html#cfn-networkfirewall-firewallpolicy-dimension-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnFirewallPolicy.FirewallPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "stateless_default_actions": "statelessDefaultActions",
            "stateless_fragment_default_actions": "statelessFragmentDefaultActions",
            "stateful_default_actions": "statefulDefaultActions",
            "stateful_engine_options": "statefulEngineOptions",
            "stateful_rule_group_references": "statefulRuleGroupReferences",
            "stateless_custom_actions": "statelessCustomActions",
            "stateless_rule_group_references": "statelessRuleGroupReferences",
        },
    )
    class FirewallPolicyProperty:
        def __init__(
            self,
            *,
            stateless_default_actions: typing.Sequence[builtins.str],
            stateless_fragment_default_actions: typing.Sequence[builtins.str],
            stateful_default_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
            stateful_engine_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFirewallPolicy.StatefulEngineOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            stateful_rule_group_references: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFirewallPolicy.StatefulRuleGroupReferenceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            stateless_custom_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFirewallPolicy.CustomActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            stateless_rule_group_references: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFirewallPolicy.StatelessRuleGroupReferenceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''The traffic filtering behavior of a firewall policy, defined in a collection of stateless and stateful rule groups and other settings.

            :param stateless_default_actions: The actions to take on a packet if it doesn't match any of the stateless rules in the policy. If you want non-matching packets to be forwarded for stateful inspection, specify ``aws:forward_to_sfe`` . You must specify one of the standard actions: ``aws:pass`` , ``aws:drop`` , or ``aws:forward_to_sfe`` . In addition, you can specify custom actions that are compatible with your standard section choice. For example, you could specify ``["aws:pass"]`` or you could specify ``["aws:pass", “customActionName”]`` . For information about compatibility, see the custom action descriptions.
            :param stateless_fragment_default_actions: The actions to take on a fragmented packet if it doesn't match any of the stateless rules in the policy. If you want non-matching fragmented packets to be forwarded for stateful inspection, specify ``aws:forward_to_sfe`` . You must specify one of the standard actions: ``aws:pass`` , ``aws:drop`` , or ``aws:forward_to_sfe`` . In addition, you can specify custom actions that are compatible with your standard section choice. For example, you could specify ``["aws:pass"]`` or you could specify ``["aws:pass", “customActionName”]`` . For information about compatibility, see the custom action descriptions.
            :param stateful_default_actions: The default actions to take on a packet that doesn't match any stateful rules. The stateful default action is optional, and is only valid when using the strict rule order. Valid values of the stateful default action: - aws:drop_strict - aws:drop_established - aws:alert_strict - aws:alert_established For more information, see `Strict evaluation order <https://docs.aws.amazon.com/network-firewall/latest/developerguide/suricata-rule-evaluation-order.html#suricata-strict-rule-evaluation-order.html>`_ in the *AWS Network Firewall Developer Guide* .
            :param stateful_engine_options: Additional options governing how Network Firewall handles stateful rules. The stateful rule groups that you use in your policy must have stateful rule options settings that are compatible with these settings.
            :param stateful_rule_group_references: References to the stateful rule groups that are used in the policy. These define the inspection criteria in stateful rules.
            :param stateless_custom_actions: The custom action definitions that are available for use in the firewall policy's ``StatelessDefaultActions`` setting. You name each custom action that you define, and then you can use it by name in your default actions specifications.
            :param stateless_rule_group_references: References to the stateless rule groups that are used in the policy. These define the matching criteria in stateless rules.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                firewall_policy_property = networkfirewall.CfnFirewallPolicy.FirewallPolicyProperty(
                    stateless_default_actions=["statelessDefaultActions"],
                    stateless_fragment_default_actions=["statelessFragmentDefaultActions"],
                
                    # the properties below are optional
                    stateful_default_actions=["statefulDefaultActions"],
                    stateful_engine_options=networkfirewall.CfnFirewallPolicy.StatefulEngineOptionsProperty(
                        rule_order="ruleOrder",
                        stream_exception_policy="streamExceptionPolicy"
                    ),
                    stateful_rule_group_references=[networkfirewall.CfnFirewallPolicy.StatefulRuleGroupReferenceProperty(
                        resource_arn="resourceArn",
                
                        # the properties below are optional
                        override=networkfirewall.CfnFirewallPolicy.StatefulRuleGroupOverrideProperty(
                            action="action"
                        ),
                        priority=123
                    )],
                    stateless_custom_actions=[networkfirewall.CfnFirewallPolicy.CustomActionProperty(
                        action_definition=networkfirewall.CfnFirewallPolicy.ActionDefinitionProperty(
                            publish_metric_action=networkfirewall.CfnFirewallPolicy.PublishMetricActionProperty(
                                dimensions=[networkfirewall.CfnFirewallPolicy.DimensionProperty(
                                    value="value"
                                )]
                            )
                        ),
                        action_name="actionName"
                    )],
                    stateless_rule_group_references=[networkfirewall.CfnFirewallPolicy.StatelessRuleGroupReferenceProperty(
                        priority=123,
                        resource_arn="resourceArn"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0efae29543f839fb2f4b74d28d3e8bd2f76ce46c31cff67d4bcb435eac193d7e)
                check_type(argname="argument stateless_default_actions", value=stateless_default_actions, expected_type=type_hints["stateless_default_actions"])
                check_type(argname="argument stateless_fragment_default_actions", value=stateless_fragment_default_actions, expected_type=type_hints["stateless_fragment_default_actions"])
                check_type(argname="argument stateful_default_actions", value=stateful_default_actions, expected_type=type_hints["stateful_default_actions"])
                check_type(argname="argument stateful_engine_options", value=stateful_engine_options, expected_type=type_hints["stateful_engine_options"])
                check_type(argname="argument stateful_rule_group_references", value=stateful_rule_group_references, expected_type=type_hints["stateful_rule_group_references"])
                check_type(argname="argument stateless_custom_actions", value=stateless_custom_actions, expected_type=type_hints["stateless_custom_actions"])
                check_type(argname="argument stateless_rule_group_references", value=stateless_rule_group_references, expected_type=type_hints["stateless_rule_group_references"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "stateless_default_actions": stateless_default_actions,
                "stateless_fragment_default_actions": stateless_fragment_default_actions,
            }
            if stateful_default_actions is not None:
                self._values["stateful_default_actions"] = stateful_default_actions
            if stateful_engine_options is not None:
                self._values["stateful_engine_options"] = stateful_engine_options
            if stateful_rule_group_references is not None:
                self._values["stateful_rule_group_references"] = stateful_rule_group_references
            if stateless_custom_actions is not None:
                self._values["stateless_custom_actions"] = stateless_custom_actions
            if stateless_rule_group_references is not None:
                self._values["stateless_rule_group_references"] = stateless_rule_group_references

        @builtins.property
        def stateless_default_actions(self) -> typing.List[builtins.str]:
            '''The actions to take on a packet if it doesn't match any of the stateless rules in the policy.

            If you want non-matching packets to be forwarded for stateful inspection, specify ``aws:forward_to_sfe`` .

            You must specify one of the standard actions: ``aws:pass`` , ``aws:drop`` , or ``aws:forward_to_sfe`` . In addition, you can specify custom actions that are compatible with your standard section choice.

            For example, you could specify ``["aws:pass"]`` or you could specify ``["aws:pass", “customActionName”]`` . For information about compatibility, see the custom action descriptions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statelessdefaultactions
            '''
            result = self._values.get("stateless_default_actions")
            assert result is not None, "Required property 'stateless_default_actions' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def stateless_fragment_default_actions(self) -> typing.List[builtins.str]:
            '''The actions to take on a fragmented packet if it doesn't match any of the stateless rules in the policy.

            If you want non-matching fragmented packets to be forwarded for stateful inspection, specify ``aws:forward_to_sfe`` .

            You must specify one of the standard actions: ``aws:pass`` , ``aws:drop`` , or ``aws:forward_to_sfe`` . In addition, you can specify custom actions that are compatible with your standard section choice.

            For example, you could specify ``["aws:pass"]`` or you could specify ``["aws:pass", “customActionName”]`` . For information about compatibility, see the custom action descriptions.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statelessfragmentdefaultactions
            '''
            result = self._values.get("stateless_fragment_default_actions")
            assert result is not None, "Required property 'stateless_fragment_default_actions' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def stateful_default_actions(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''The default actions to take on a packet that doesn't match any stateful rules.

            The stateful default action is optional, and is only valid when using the strict rule order.

            Valid values of the stateful default action:

            - aws:drop_strict
            - aws:drop_established
            - aws:alert_strict
            - aws:alert_established

            For more information, see `Strict evaluation order <https://docs.aws.amazon.com/network-firewall/latest/developerguide/suricata-rule-evaluation-order.html#suricata-strict-rule-evaluation-order.html>`_ in the *AWS Network Firewall Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statefuldefaultactions
            '''
            result = self._values.get("stateful_default_actions")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def stateful_engine_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.StatefulEngineOptionsProperty"]]:
            '''Additional options governing how Network Firewall handles stateful rules.

            The stateful rule groups that you use in your policy must have stateful rule options settings that are compatible with these settings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statefulengineoptions
            '''
            result = self._values.get("stateful_engine_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.StatefulEngineOptionsProperty"]], result)

        @builtins.property
        def stateful_rule_group_references(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.StatefulRuleGroupReferenceProperty"]]]]:
            '''References to the stateful rule groups that are used in the policy.

            These define the inspection criteria in stateful rules.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statefulrulegroupreferences
            '''
            result = self._values.get("stateful_rule_group_references")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.StatefulRuleGroupReferenceProperty"]]]], result)

        @builtins.property
        def stateless_custom_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.CustomActionProperty"]]]]:
            '''The custom action definitions that are available for use in the firewall policy's ``StatelessDefaultActions`` setting.

            You name each custom action that you define, and then you can use it by name in your default actions specifications.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statelesscustomactions
            '''
            result = self._values.get("stateless_custom_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.CustomActionProperty"]]]], result)

        @builtins.property
        def stateless_rule_group_references(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.StatelessRuleGroupReferenceProperty"]]]]:
            '''References to the stateless rule groups that are used in the policy.

            These define the matching criteria in stateless rules.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statelessrulegroupreferences
            '''
            result = self._values.get("stateless_rule_group_references")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.StatelessRuleGroupReferenceProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirewallPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnFirewallPolicy.PublishMetricActionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimensions": "dimensions"},
    )
    class PublishMetricActionProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFirewallPolicy.DimensionProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet.

            This setting defines a CloudWatch dimension value to be published.

            :param dimensions: ``CfnFirewallPolicy.PublishMetricActionProperty.Dimensions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-publishmetricaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                publish_metric_action_property = networkfirewall.CfnFirewallPolicy.PublishMetricActionProperty(
                    dimensions=[networkfirewall.CfnFirewallPolicy.DimensionProperty(
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3f8dee6a5e3ddc081940a60cdbba5126c0d9c8ecfad560b470a71b23ab60b6f)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "dimensions": dimensions,
            }

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.DimensionProperty"]]]:
            '''``CfnFirewallPolicy.PublishMetricActionProperty.Dimensions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-publishmetricaction.html#cfn-networkfirewall-firewallpolicy-publishmetricaction-dimensions
            '''
            result = self._values.get("dimensions")
            assert result is not None, "Required property 'dimensions' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.DimensionProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublishMetricActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnFirewallPolicy.StatefulEngineOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "rule_order": "ruleOrder",
            "stream_exception_policy": "streamExceptionPolicy",
        },
    )
    class StatefulEngineOptionsProperty:
        def __init__(
            self,
            *,
            rule_order: typing.Optional[builtins.str] = None,
            stream_exception_policy: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configuration settings for the handling of the stateful rule groups in a firewall policy.

            :param rule_order: Indicates how to manage the order of stateful rule evaluation for the policy. ``DEFAULT_ACTION_ORDER`` is the default behavior. Stateful rules are provided to the rule engine as Suricata compatible strings, and Suricata evaluates them based on certain settings. For more information, see `Evaluation order for stateful rules <https://docs.aws.amazon.com/network-firewall/latest/developerguide/suricata-rule-evaluation-order.html>`_ in the *AWS Network Firewall Developer Guide* .
            :param stream_exception_policy: Configures how Network Firewall processes traffic when a network connection breaks midstream. Network connections can break due to disruptions in external networks or within the firewall itself. - ``DROP`` - Network Firewall fails closed and drops all subsequent traffic going to the firewall. This is the default behavior. - ``CONTINUE`` - Network Firewall continues to apply rules to the subsequent traffic without context from traffic before the break. This impacts the behavior of rules that depend on this context. For example, if you have a stateful rule to ``drop http`` traffic, Network Firewall won't match the traffic for this rule because the service won't have the context from session initialization defining the application layer protocol as HTTP. However, this behavior is rule dependent—a TCP-layer rule using a ``flow:stateless`` rule would still match, as would the ``aws:drop_strict`` default action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulengineoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                stateful_engine_options_property = networkfirewall.CfnFirewallPolicy.StatefulEngineOptionsProperty(
                    rule_order="ruleOrder",
                    stream_exception_policy="streamExceptionPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eea2f5432221bdcc5b6fabcb38879b7ff807ec52e4123fc01e5d59556113a630)
                check_type(argname="argument rule_order", value=rule_order, expected_type=type_hints["rule_order"])
                check_type(argname="argument stream_exception_policy", value=stream_exception_policy, expected_type=type_hints["stream_exception_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rule_order is not None:
                self._values["rule_order"] = rule_order
            if stream_exception_policy is not None:
                self._values["stream_exception_policy"] = stream_exception_policy

        @builtins.property
        def rule_order(self) -> typing.Optional[builtins.str]:
            '''Indicates how to manage the order of stateful rule evaluation for the policy.

            ``DEFAULT_ACTION_ORDER`` is the default behavior. Stateful rules are provided to the rule engine as Suricata compatible strings, and Suricata evaluates them based on certain settings. For more information, see `Evaluation order for stateful rules <https://docs.aws.amazon.com/network-firewall/latest/developerguide/suricata-rule-evaluation-order.html>`_ in the *AWS Network Firewall Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulengineoptions.html#cfn-networkfirewall-firewallpolicy-statefulengineoptions-ruleorder
            '''
            result = self._values.get("rule_order")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stream_exception_policy(self) -> typing.Optional[builtins.str]:
            '''Configures how Network Firewall processes traffic when a network connection breaks midstream.

            Network connections can break due to disruptions in external networks or within the firewall itself.

            - ``DROP`` - Network Firewall fails closed and drops all subsequent traffic going to the firewall. This is the default behavior.
            - ``CONTINUE`` - Network Firewall continues to apply rules to the subsequent traffic without context from traffic before the break. This impacts the behavior of rules that depend on this context. For example, if you have a stateful rule to ``drop http`` traffic, Network Firewall won't match the traffic for this rule because the service won't have the context from session initialization defining the application layer protocol as HTTP. However, this behavior is rule dependent—a TCP-layer rule using a ``flow:stateless`` rule would still match, as would the ``aws:drop_strict`` default action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulengineoptions.html#cfn-networkfirewall-firewallpolicy-statefulengineoptions-streamexceptionpolicy
            '''
            result = self._values.get("stream_exception_policy")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatefulEngineOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnFirewallPolicy.StatefulRuleGroupOverrideProperty",
        jsii_struct_bases=[],
        name_mapping={"action": "action"},
    )
    class StatefulRuleGroupOverrideProperty:
        def __init__(self, *, action: typing.Optional[builtins.str] = None) -> None:
            '''The setting that allows the policy owner to change the behavior of the rule group within a policy.

            :param action: The action that changes the rule group from ``DROP`` to ``ALERT`` . This only applies to managed rule groups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupoverride.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                stateful_rule_group_override_property = networkfirewall.CfnFirewallPolicy.StatefulRuleGroupOverrideProperty(
                    action="action"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cfa8ad1569623359c8ef26112c0e6543aead4d60a62f344875f1f853eff72d5a)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if action is not None:
                self._values["action"] = action

        @builtins.property
        def action(self) -> typing.Optional[builtins.str]:
            '''The action that changes the rule group from ``DROP`` to ``ALERT`` .

            This only applies to managed rule groups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupoverride.html#cfn-networkfirewall-firewallpolicy-statefulrulegroupoverride-action
            '''
            result = self._values.get("action")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatefulRuleGroupOverrideProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnFirewallPolicy.StatefulRuleGroupReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "resource_arn": "resourceArn",
            "override": "override",
            "priority": "priority",
        },
    )
    class StatefulRuleGroupReferenceProperty:
        def __init__(
            self,
            *,
            resource_arn: builtins.str,
            override: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnFirewallPolicy.StatefulRuleGroupOverrideProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            priority: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Identifier for a single stateful rule group, used in a firewall policy to refer to a rule group.

            :param resource_arn: The Amazon Resource Name (ARN) of the stateful rule group.
            :param override: The action that allows the policy owner to override the behavior of the rule group within a policy.
            :param priority: An integer setting that indicates the order in which to run the stateful rule groups in a single ``FirewallPolicy`` . This setting only applies to firewall policies that specify the ``STRICT_ORDER`` rule order in the stateful engine options settings. Network Firewall evalutes each stateful rule group against a packet starting with the group that has the lowest priority setting. You must ensure that the priority settings are unique within each policy. You can change the priority settings of your rule groups at any time. To make it easier to insert rule groups later, number them so there's a wide range in between, for example use 100, 200, and so on.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupreference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                stateful_rule_group_reference_property = networkfirewall.CfnFirewallPolicy.StatefulRuleGroupReferenceProperty(
                    resource_arn="resourceArn",
                
                    # the properties below are optional
                    override=networkfirewall.CfnFirewallPolicy.StatefulRuleGroupOverrideProperty(
                        action="action"
                    ),
                    priority=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fa2d356e374a606507927fa1e79e01673325a1ca2611b60e756a13cafaee9594)
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
                check_type(argname="argument override", value=override, expected_type=type_hints["override"])
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "resource_arn": resource_arn,
            }
            if override is not None:
                self._values["override"] = override
            if priority is not None:
                self._values["priority"] = priority

        @builtins.property
        def resource_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the stateful rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupreference.html#cfn-networkfirewall-firewallpolicy-statefulrulegroupreference-resourcearn
            '''
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def override(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.StatefulRuleGroupOverrideProperty"]]:
            '''The action that allows the policy owner to override the behavior of the rule group within a policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupreference.html#cfn-networkfirewall-firewallpolicy-statefulrulegroupreference-override
            '''
            result = self._values.get("override")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnFirewallPolicy.StatefulRuleGroupOverrideProperty"]], result)

        @builtins.property
        def priority(self) -> typing.Optional[jsii.Number]:
            '''An integer setting that indicates the order in which to run the stateful rule groups in a single ``FirewallPolicy`` .

            This setting only applies to firewall policies that specify the ``STRICT_ORDER`` rule order in the stateful engine options settings.

            Network Firewall evalutes each stateful rule group against a packet starting with the group that has the lowest priority setting. You must ensure that the priority settings are unique within each policy.

            You can change the priority settings of your rule groups at any time. To make it easier to insert rule groups later, number them so there's a wide range in between, for example use 100, 200, and so on.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupreference.html#cfn-networkfirewall-firewallpolicy-statefulrulegroupreference-priority
            '''
            result = self._values.get("priority")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatefulRuleGroupReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnFirewallPolicy.StatelessRuleGroupReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={"priority": "priority", "resource_arn": "resourceArn"},
    )
    class StatelessRuleGroupReferenceProperty:
        def __init__(
            self,
            *,
            priority: jsii.Number,
            resource_arn: builtins.str,
        ) -> None:
            '''Identifier for a single stateless rule group, used in a firewall policy to refer to the rule group.

            :param priority: An integer setting that indicates the order in which to run the stateless rule groups in a single ``FirewallPolicy`` . Network Firewall applies each stateless rule group to a packet starting with the group that has the lowest priority setting. You must ensure that the priority settings are unique within each policy.
            :param resource_arn: The Amazon Resource Name (ARN) of the stateless rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statelessrulegroupreference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                stateless_rule_group_reference_property = networkfirewall.CfnFirewallPolicy.StatelessRuleGroupReferenceProperty(
                    priority=123,
                    resource_arn="resourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1bb980e9a4423f160aa1057a7280ab44a1d401cbeba4e3deaefe784f9a94b65b)
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "priority": priority,
                "resource_arn": resource_arn,
            }

        @builtins.property
        def priority(self) -> jsii.Number:
            '''An integer setting that indicates the order in which to run the stateless rule groups in a single ``FirewallPolicy`` .

            Network Firewall applies each stateless rule group to a packet starting with the group that has the lowest priority setting. You must ensure that the priority settings are unique within each policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statelessrulegroupreference.html#cfn-networkfirewall-firewallpolicy-statelessrulegroupreference-priority
            '''
            result = self._values.get("priority")
            assert result is not None, "Required property 'priority' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def resource_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the stateless rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statelessrulegroupreference.html#cfn-networkfirewall-firewallpolicy-statelessrulegroupreference-resourcearn
            '''
            result = self._values.get("resource_arn")
            assert result is not None, "Required property 'resource_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatelessRuleGroupReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-networkfirewall.CfnFirewallPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "firewall_policy": "firewallPolicy",
        "firewall_policy_name": "firewallPolicyName",
        "description": "description",
        "tags": "tags",
    },
)
class CfnFirewallPolicyProps:
    def __init__(
        self,
        *,
        firewall_policy: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFirewallPolicy.FirewallPolicyProperty, typing.Dict[builtins.str, typing.Any]]],
        firewall_policy_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnFirewallPolicy``.

        :param firewall_policy: The traffic filtering behavior of a firewall policy, defined in a collection of stateless and stateful rule groups and other settings.
        :param firewall_policy_name: The descriptive name of the firewall policy. You can't change the name of a firewall policy after you create it.
        :param description: A description of the firewall policy.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_networkfirewall as networkfirewall
            
            cfn_firewall_policy_props = networkfirewall.CfnFirewallPolicyProps(
                firewall_policy=networkfirewall.CfnFirewallPolicy.FirewallPolicyProperty(
                    stateless_default_actions=["statelessDefaultActions"],
                    stateless_fragment_default_actions=["statelessFragmentDefaultActions"],
            
                    # the properties below are optional
                    stateful_default_actions=["statefulDefaultActions"],
                    stateful_engine_options=networkfirewall.CfnFirewallPolicy.StatefulEngineOptionsProperty(
                        rule_order="ruleOrder",
                        stream_exception_policy="streamExceptionPolicy"
                    ),
                    stateful_rule_group_references=[networkfirewall.CfnFirewallPolicy.StatefulRuleGroupReferenceProperty(
                        resource_arn="resourceArn",
            
                        # the properties below are optional
                        override=networkfirewall.CfnFirewallPolicy.StatefulRuleGroupOverrideProperty(
                            action="action"
                        ),
                        priority=123
                    )],
                    stateless_custom_actions=[networkfirewall.CfnFirewallPolicy.CustomActionProperty(
                        action_definition=networkfirewall.CfnFirewallPolicy.ActionDefinitionProperty(
                            publish_metric_action=networkfirewall.CfnFirewallPolicy.PublishMetricActionProperty(
                                dimensions=[networkfirewall.CfnFirewallPolicy.DimensionProperty(
                                    value="value"
                                )]
                            )
                        ),
                        action_name="actionName"
                    )],
                    stateless_rule_group_references=[networkfirewall.CfnFirewallPolicy.StatelessRuleGroupReferenceProperty(
                        priority=123,
                        resource_arn="resourceArn"
                    )]
                ),
                firewall_policy_name="firewallPolicyName",
            
                # the properties below are optional
                description="description",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7cabcce3c29168bced4cffc4f4993707cebb8d88f7e93b1815f5206bdd6e2bfa)
            check_type(argname="argument firewall_policy", value=firewall_policy, expected_type=type_hints["firewall_policy"])
            check_type(argname="argument firewall_policy_name", value=firewall_policy_name, expected_type=type_hints["firewall_policy_name"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "firewall_policy": firewall_policy,
            "firewall_policy_name": firewall_policy_name,
        }
        if description is not None:
            self._values["description"] = description
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def firewall_policy(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFirewallPolicy.FirewallPolicyProperty]:
        '''The traffic filtering behavior of a firewall policy, defined in a collection of stateless and stateful rule groups and other settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy
        '''
        result = self._values.get("firewall_policy")
        assert result is not None, "Required property 'firewall_policy' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFirewallPolicy.FirewallPolicyProperty], result)

    @builtins.property
    def firewall_policy_name(self) -> builtins.str:
        '''The descriptive name of the firewall policy.

        You can't change the name of a firewall policy after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicyname
        '''
        result = self._values.get("firewall_policy_name")
        assert result is not None, "Required property 'firewall_policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the firewall policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFirewallPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-networkfirewall.CfnFirewallProps",
    jsii_struct_bases=[],
    name_mapping={
        "firewall_name": "firewallName",
        "firewall_policy_arn": "firewallPolicyArn",
        "subnet_mappings": "subnetMappings",
        "vpc_id": "vpcId",
        "delete_protection": "deleteProtection",
        "description": "description",
        "firewall_policy_change_protection": "firewallPolicyChangeProtection",
        "subnet_change_protection": "subnetChangeProtection",
        "tags": "tags",
    },
)
class CfnFirewallProps:
    def __init__(
        self,
        *,
        firewall_name: builtins.str,
        firewall_policy_arn: builtins.str,
        subnet_mappings: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnFirewall.SubnetMappingProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
        vpc_id: builtins.str,
        delete_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        firewall_policy_change_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        subnet_change_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnFirewall``.

        :param firewall_name: The descriptive name of the firewall. You can't change the name of a firewall after you create it.
        :param firewall_policy_arn: The Amazon Resource Name (ARN) of the firewall policy. The relationship of firewall to firewall policy is many to one. Each firewall requires one firewall policy association, and you can use the same firewall policy for multiple firewalls.
        :param subnet_mappings: The public subnets that Network Firewall is using for the firewall. Each subnet must belong to a different Availability Zone.
        :param vpc_id: The unique identifier of the VPC where the firewall is in use. You can't change the VPC of a firewall after you create the firewall.
        :param delete_protection: A flag indicating whether it is possible to delete the firewall. A setting of ``TRUE`` indicates that the firewall is protected against deletion. Use this setting to protect against accidentally deleting a firewall that is in use. When you create a firewall, the operation initializes this flag to ``TRUE`` .
        :param description: A description of the firewall.
        :param firewall_policy_change_protection: A setting indicating whether the firewall is protected against a change to the firewall policy association. Use this setting to protect against accidentally modifying the firewall policy for a firewall that is in use. When you create a firewall, the operation initializes this setting to ``TRUE`` .
        :param subnet_change_protection: A setting indicating whether the firewall is protected against changes to the subnet associations. Use this setting to protect against accidentally modifying the subnet associations for a firewall that is in use. When you create a firewall, the operation initializes this setting to ``TRUE`` .
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_networkfirewall as networkfirewall
            
            cfn_firewall_props = networkfirewall.CfnFirewallProps(
                firewall_name="firewallName",
                firewall_policy_arn="firewallPolicyArn",
                subnet_mappings=[networkfirewall.CfnFirewall.SubnetMappingProperty(
                    subnet_id="subnetId"
                )],
                vpc_id="vpcId",
            
                # the properties below are optional
                delete_protection=False,
                description="description",
                firewall_policy_change_protection=False,
                subnet_change_protection=False,
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a32c93a11a0b99fa163ad3694fa3a8b6eba91ee67b8312e65199caffb65739e1)
            check_type(argname="argument firewall_name", value=firewall_name, expected_type=type_hints["firewall_name"])
            check_type(argname="argument firewall_policy_arn", value=firewall_policy_arn, expected_type=type_hints["firewall_policy_arn"])
            check_type(argname="argument subnet_mappings", value=subnet_mappings, expected_type=type_hints["subnet_mappings"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument delete_protection", value=delete_protection, expected_type=type_hints["delete_protection"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument firewall_policy_change_protection", value=firewall_policy_change_protection, expected_type=type_hints["firewall_policy_change_protection"])
            check_type(argname="argument subnet_change_protection", value=subnet_change_protection, expected_type=type_hints["subnet_change_protection"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "firewall_name": firewall_name,
            "firewall_policy_arn": firewall_policy_arn,
            "subnet_mappings": subnet_mappings,
            "vpc_id": vpc_id,
        }
        if delete_protection is not None:
            self._values["delete_protection"] = delete_protection
        if description is not None:
            self._values["description"] = description
        if firewall_policy_change_protection is not None:
            self._values["firewall_policy_change_protection"] = firewall_policy_change_protection
        if subnet_change_protection is not None:
            self._values["subnet_change_protection"] = subnet_change_protection
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def firewall_name(self) -> builtins.str:
        '''The descriptive name of the firewall.

        You can't change the name of a firewall after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-firewallname
        '''
        result = self._values.get("firewall_name")
        assert result is not None, "Required property 'firewall_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def firewall_policy_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the firewall policy.

        The relationship of firewall to firewall policy is many to one. Each firewall requires one firewall policy association, and you can use the same firewall policy for multiple firewalls.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-firewallpolicyarn
        '''
        result = self._values.get("firewall_policy_arn")
        assert result is not None, "Required property 'firewall_policy_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_mappings(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnFirewall.SubnetMappingProperty, _aws_cdk_core_f4b25747.IResolvable]]]:
        '''The public subnets that Network Firewall is using for the firewall.

        Each subnet must belong to a different Availability Zone.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-subnetmappings
        '''
        result = self._values.get("subnet_mappings")
        assert result is not None, "Required property 'subnet_mappings' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnFirewall.SubnetMappingProperty, _aws_cdk_core_f4b25747.IResolvable]]], result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''The unique identifier of the VPC where the firewall is in use.

        You can't change the VPC of a firewall after you create the firewall.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-vpcid
        '''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delete_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''A flag indicating whether it is possible to delete the firewall.

        A setting of ``TRUE`` indicates that the firewall is protected against deletion. Use this setting to protect against accidentally deleting a firewall that is in use. When you create a firewall, the operation initializes this flag to ``TRUE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-deleteprotection
        '''
        result = self._values.get("delete_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the firewall.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firewall_policy_change_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''A setting indicating whether the firewall is protected against a change to the firewall policy association.

        Use this setting to protect against accidentally modifying the firewall policy for a firewall that is in use. When you create a firewall, the operation initializes this setting to ``TRUE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-firewallpolicychangeprotection
        '''
        result = self._values.get("firewall_policy_change_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def subnet_change_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''A setting indicating whether the firewall is protected against changes to the subnet associations.

        Use this setting to protect against accidentally modifying the subnet associations for a firewall that is in use. When you create a firewall, the operation initializes this setting to ``TRUE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-subnetchangeprotection
        '''
        result = self._values.get("subnet_change_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFirewallProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnLoggingConfiguration(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-networkfirewall.CfnLoggingConfiguration",
):
    '''A CloudFormation ``AWS::NetworkFirewall::LoggingConfiguration``.

    Use the ``LoggingConfiguration`` to define the destinations and logging options for an ``Firewall`` .

    You must change the logging configuration by changing one ``LogDestinationConfig`` setting at a time in your ``LogDestinationConfigs`` .

    You can make only one of the following changes to your ``LoggingConfiguration`` resource:

    - Create a new log destination object by adding a single ``LogDestinationConfig`` array element to ``LogDestinationConfigs`` .
    - Delete a log destination object by removing a single ``LogDestinationConfig`` array element from ``LogDestinationConfigs`` .
    - Change the ``LogDestination`` setting in a single ``LogDestinationConfig`` array element.

    You can't change the ``LogDestinationType`` or ``LogType`` in a ``LogDestinationConfig`` . To change these settings, delete the existing ``LogDestinationConfig`` object and create a new one, in two separate modifications.

    :cloudformationResource: AWS::NetworkFirewall::LoggingConfiguration
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_networkfirewall as networkfirewall
        
        cfn_logging_configuration = networkfirewall.CfnLoggingConfiguration(self, "MyCfnLoggingConfiguration",
            firewall_arn="firewallArn",
            logging_configuration=networkfirewall.CfnLoggingConfiguration.LoggingConfigurationProperty(
                log_destination_configs=[networkfirewall.CfnLoggingConfiguration.LogDestinationConfigProperty(
                    log_destination={
                        "log_destination_key": "logDestination"
                    },
                    log_destination_type="logDestinationType",
                    log_type="logType"
                )]
            ),
        
            # the properties below are optional
            firewall_name="firewallName"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        firewall_arn: builtins.str,
        logging_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLoggingConfiguration.LoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]]],
        firewall_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkFirewall::LoggingConfiguration``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param firewall_arn: The Amazon Resource Name (ARN) of the ``Firewall`` that the logging configuration is associated with. You can't change the firewall specification after you create the logging configuration.
        :param logging_configuration: Defines how AWS Network Firewall performs logging for a ``Firewall`` .
        :param firewall_name: The name of the firewall that the logging configuration is associated with. You can't change the firewall specification after you create the logging configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__328c6f8768a9a38ee9905a29aeefc0e96e426f719b062bf4b4f96a6861402fc6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLoggingConfigurationProps(
            firewall_arn=firewall_arn,
            logging_configuration=logging_configuration,
            firewall_name=firewall_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__631baaaf383c322aa1a190eb585d070ef632969047928f26c37f36ba813a65f8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__2d5fead774da4d88b73c332b964397d6961c4afaafe062caf5d3519c46ddd178)
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
    @jsii.member(jsii_name="firewallArn")
    def firewall_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the ``Firewall`` that the logging configuration is associated with.

        You can't change the firewall specification after you create the logging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-firewallarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallArn"))

    @firewall_arn.setter
    def firewall_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67d675231d241a54cc0d6bc0a21335561d53c21bf6ce50b7491c4109ba056308)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallArn", value)

    @builtins.property
    @jsii.member(jsii_name="loggingConfiguration")
    def logging_configuration(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggingConfiguration.LoggingConfigurationProperty"]:
        '''Defines how AWS Network Firewall performs logging for a ``Firewall`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-loggingconfiguration
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggingConfiguration.LoggingConfigurationProperty"], jsii.get(self, "loggingConfiguration"))

    @logging_configuration.setter
    def logging_configuration(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggingConfiguration.LoggingConfigurationProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da205a6d2f4d3dbca2ca6d68bd310872e4fe3c060c38384d357900e7dd870dbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loggingConfiguration", value)

    @builtins.property
    @jsii.member(jsii_name="firewallName")
    def firewall_name(self) -> typing.Optional[builtins.str]:
        '''The name of the firewall that the logging configuration is associated with.

        You can't change the firewall specification after you create the logging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-firewallname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firewallName"))

    @firewall_name.setter
    def firewall_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b518275b3169c503d207df887486befbb188dad67eab8e3edceac0fbe75e6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallName", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnLoggingConfiguration.LogDestinationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "log_destination": "logDestination",
            "log_destination_type": "logDestinationType",
            "log_type": "logType",
        },
    )
    class LogDestinationConfigProperty:
        def __init__(
            self,
            *,
            log_destination: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]],
            log_destination_type: builtins.str,
            log_type: builtins.str,
        ) -> None:
            '''Defines where AWS Network Firewall sends logs for the firewall for one log type.

            This is used in ``LoggingConfiguration`` . You can send each type of log to an Amazon S3 bucket, a CloudWatch log group, or a Kinesis Data Firehose delivery stream.

            Network Firewall generates logs for stateful rule groups. You can save alert and flow log types. The stateful rules engine records flow logs for all network traffic that it receives. It records alert logs for traffic that matches stateful rules that have the rule action set to ``DROP`` or ``ALERT`` .

            :param log_destination: The named location for the logs, provided in a key:value mapping that is specific to the chosen destination type. - For an Amazon S3 bucket, provide the name of the bucket, with key ``bucketName`` , and optionally provide a prefix, with key ``prefix`` . The following example specifies an Amazon S3 bucket named ``DOC-EXAMPLE-BUCKET`` and the prefix ``alerts`` : ``"LogDestination": { "bucketName": "DOC-EXAMPLE-BUCKET", "prefix": "alerts" }`` - For a CloudWatch log group, provide the name of the CloudWatch log group, with key ``logGroup`` . The following example specifies a log group named ``alert-log-group`` : ``"LogDestination": { "logGroup": "alert-log-group" }`` - For a Kinesis Data Firehose delivery stream, provide the name of the delivery stream, with key ``deliveryStream`` . The following example specifies a delivery stream named ``alert-delivery-stream`` : ``"LogDestination": { "deliveryStream": "alert-delivery-stream" }``
            :param log_destination_type: The type of storage destination to send these logs to. You can send logs to an Amazon S3 bucket, a CloudWatch log group, or a Kinesis Data Firehose delivery stream.
            :param log_type: The type of log to send. Alert logs report traffic that matches a stateful rule with an action setting that sends an alert log message. Flow logs are standard network traffic flow logs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-logdestinationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                log_destination_config_property = networkfirewall.CfnLoggingConfiguration.LogDestinationConfigProperty(
                    log_destination={
                        "log_destination_key": "logDestination"
                    },
                    log_destination_type="logDestinationType",
                    log_type="logType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cf57403e164680766143d1ceaee3fca20ba2cd4df58572ea0d55a73889ef1437)
                check_type(argname="argument log_destination", value=log_destination, expected_type=type_hints["log_destination"])
                check_type(argname="argument log_destination_type", value=log_destination_type, expected_type=type_hints["log_destination_type"])
                check_type(argname="argument log_type", value=log_type, expected_type=type_hints["log_type"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "log_destination": log_destination,
                "log_destination_type": log_destination_type,
                "log_type": log_type,
            }

        @builtins.property
        def log_destination(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]:
            '''The named location for the logs, provided in a key:value mapping that is specific to the chosen destination type.

            - For an Amazon S3 bucket, provide the name of the bucket, with key ``bucketName`` , and optionally provide a prefix, with key ``prefix`` . The following example specifies an Amazon S3 bucket named ``DOC-EXAMPLE-BUCKET`` and the prefix ``alerts`` :

            ``"LogDestination": { "bucketName": "DOC-EXAMPLE-BUCKET", "prefix": "alerts" }``

            - For a CloudWatch log group, provide the name of the CloudWatch log group, with key ``logGroup`` . The following example specifies a log group named ``alert-log-group`` :

            ``"LogDestination": { "logGroup": "alert-log-group" }``

            - For a Kinesis Data Firehose delivery stream, provide the name of the delivery stream, with key ``deliveryStream`` . The following example specifies a delivery stream named ``alert-delivery-stream`` :

            ``"LogDestination": { "deliveryStream": "alert-delivery-stream" }``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-logdestinationconfig.html#cfn-networkfirewall-loggingconfiguration-logdestinationconfig-logdestination
            '''
            result = self._values.get("log_destination")
            assert result is not None, "Required property 'log_destination' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]], result)

        @builtins.property
        def log_destination_type(self) -> builtins.str:
            '''The type of storage destination to send these logs to.

            You can send logs to an Amazon S3 bucket, a CloudWatch log group, or a Kinesis Data Firehose delivery stream.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-logdestinationconfig.html#cfn-networkfirewall-loggingconfiguration-logdestinationconfig-logdestinationtype
            '''
            result = self._values.get("log_destination_type")
            assert result is not None, "Required property 'log_destination_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def log_type(self) -> builtins.str:
            '''The type of log to send.

            Alert logs report traffic that matches a stateful rule with an action setting that sends an alert log message. Flow logs are standard network traffic flow logs.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-logdestinationconfig.html#cfn-networkfirewall-loggingconfiguration-logdestinationconfig-logtype
            '''
            result = self._values.get("log_type")
            assert result is not None, "Required property 'log_type' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LogDestinationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnLoggingConfiguration.LoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_destination_configs": "logDestinationConfigs"},
    )
    class LoggingConfigurationProperty:
        def __init__(
            self,
            *,
            log_destination_configs: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnLoggingConfiguration.LogDestinationConfigProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''Defines how AWS Network Firewall performs logging for a ``Firewall`` .

            :param log_destination_configs: Defines the logging destinations for the logs for a firewall. Network Firewall generates logs for stateful rule groups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-loggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                logging_configuration_property = networkfirewall.CfnLoggingConfiguration.LoggingConfigurationProperty(
                    log_destination_configs=[networkfirewall.CfnLoggingConfiguration.LogDestinationConfigProperty(
                        log_destination={
                            "log_destination_key": "logDestination"
                        },
                        log_destination_type="logDestinationType",
                        log_type="logType"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__59b11c20b52bf275d1bce8e9d30b42195a2d4e42b98b229018eeeeb4f06b812d)
                check_type(argname="argument log_destination_configs", value=log_destination_configs, expected_type=type_hints["log_destination_configs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "log_destination_configs": log_destination_configs,
            }

        @builtins.property
        def log_destination_configs(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggingConfiguration.LogDestinationConfigProperty"]]]:
            '''Defines the logging destinations for the logs for a firewall.

            Network Firewall generates logs for stateful rule groups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-loggingconfiguration-logdestinationconfigs
            '''
            result = self._values.get("log_destination_configs")
            assert result is not None, "Required property 'log_destination_configs' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnLoggingConfiguration.LogDestinationConfigProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-networkfirewall.CfnLoggingConfigurationProps",
    jsii_struct_bases=[],
    name_mapping={
        "firewall_arn": "firewallArn",
        "logging_configuration": "loggingConfiguration",
        "firewall_name": "firewallName",
    },
)
class CfnLoggingConfigurationProps:
    def __init__(
        self,
        *,
        firewall_arn: builtins.str,
        logging_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLoggingConfiguration.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
        firewall_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnLoggingConfiguration``.

        :param firewall_arn: The Amazon Resource Name (ARN) of the ``Firewall`` that the logging configuration is associated with. You can't change the firewall specification after you create the logging configuration.
        :param logging_configuration: Defines how AWS Network Firewall performs logging for a ``Firewall`` .
        :param firewall_name: The name of the firewall that the logging configuration is associated with. You can't change the firewall specification after you create the logging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_networkfirewall as networkfirewall
            
            cfn_logging_configuration_props = networkfirewall.CfnLoggingConfigurationProps(
                firewall_arn="firewallArn",
                logging_configuration=networkfirewall.CfnLoggingConfiguration.LoggingConfigurationProperty(
                    log_destination_configs=[networkfirewall.CfnLoggingConfiguration.LogDestinationConfigProperty(
                        log_destination={
                            "log_destination_key": "logDestination"
                        },
                        log_destination_type="logDestinationType",
                        log_type="logType"
                    )]
                ),
            
                # the properties below are optional
                firewall_name="firewallName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f34101af25cb28e6793d92ca9946d43f82323a561b65e7f05de32322235ed50e)
            check_type(argname="argument firewall_arn", value=firewall_arn, expected_type=type_hints["firewall_arn"])
            check_type(argname="argument logging_configuration", value=logging_configuration, expected_type=type_hints["logging_configuration"])
            check_type(argname="argument firewall_name", value=firewall_name, expected_type=type_hints["firewall_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "firewall_arn": firewall_arn,
            "logging_configuration": logging_configuration,
        }
        if firewall_name is not None:
            self._values["firewall_name"] = firewall_name

    @builtins.property
    def firewall_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the ``Firewall`` that the logging configuration is associated with.

        You can't change the firewall specification after you create the logging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-firewallarn
        '''
        result = self._values.get("firewall_arn")
        assert result is not None, "Required property 'firewall_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def logging_configuration(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLoggingConfiguration.LoggingConfigurationProperty]:
        '''Defines how AWS Network Firewall performs logging for a ``Firewall`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-loggingconfiguration
        '''
        result = self._values.get("logging_configuration")
        assert result is not None, "Required property 'logging_configuration' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLoggingConfiguration.LoggingConfigurationProperty], result)

    @builtins.property
    def firewall_name(self) -> typing.Optional[builtins.str]:
        '''The name of the firewall that the logging configuration is associated with.

        You can't change the firewall specification after you create the logging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-firewallname
        '''
        result = self._values.get("firewall_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnLoggingConfigurationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRuleGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup",
):
    '''A CloudFormation ``AWS::NetworkFirewall::RuleGroup``.

    Use the ``RuleGroup`` to define a reusable collection of stateless or stateful network traffic filtering rules. You use rule groups in an ``FirewallPolicy`` to specify the filtering behavior of an ``Firewall`` .

    :cloudformationResource: AWS::NetworkFirewall::RuleGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_networkfirewall as networkfirewall
        
        cfn_rule_group = networkfirewall.CfnRuleGroup(self, "MyCfnRuleGroup",
            capacity=123,
            rule_group_name="ruleGroupName",
            type="type",
        
            # the properties below are optional
            description="description",
            rule_group=networkfirewall.CfnRuleGroup.RuleGroupProperty(
                rules_source=networkfirewall.CfnRuleGroup.RulesSourceProperty(
                    rules_source_list=networkfirewall.CfnRuleGroup.RulesSourceListProperty(
                        generated_rules_type="generatedRulesType",
                        targets=["targets"],
                        target_types=["targetTypes"]
                    ),
                    rules_string="rulesString",
                    stateful_rules=[networkfirewall.CfnRuleGroup.StatefulRuleProperty(
                        action="action",
                        header=networkfirewall.CfnRuleGroup.HeaderProperty(
                            destination="destination",
                            destination_port="destinationPort",
                            direction="direction",
                            protocol="protocol",
                            source="source",
                            source_port="sourcePort"
                        ),
                        rule_options=[networkfirewall.CfnRuleGroup.RuleOptionProperty(
                            keyword="keyword",
        
                            # the properties below are optional
                            settings=["settings"]
                        )]
                    )],
                    stateless_rules_and_custom_actions=networkfirewall.CfnRuleGroup.StatelessRulesAndCustomActionsProperty(
                        stateless_rules=[networkfirewall.CfnRuleGroup.StatelessRuleProperty(
                            priority=123,
                            rule_definition=networkfirewall.CfnRuleGroup.RuleDefinitionProperty(
                                actions=["actions"],
                                match_attributes=networkfirewall.CfnRuleGroup.MatchAttributesProperty(
                                    destination_ports=[networkfirewall.CfnRuleGroup.PortRangeProperty(
                                        from_port=123,
                                        to_port=123
                                    )],
                                    destinations=[networkfirewall.CfnRuleGroup.AddressProperty(
                                        address_definition="addressDefinition"
                                    )],
                                    protocols=[123],
                                    source_ports=[networkfirewall.CfnRuleGroup.PortRangeProperty(
                                        from_port=123,
                                        to_port=123
                                    )],
                                    sources=[networkfirewall.CfnRuleGroup.AddressProperty(
                                        address_definition="addressDefinition"
                                    )],
                                    tcp_flags=[networkfirewall.CfnRuleGroup.TCPFlagFieldProperty(
                                        flags=["flags"],
        
                                        # the properties below are optional
                                        masks=["masks"]
                                    )]
                                )
                            )
                        )],
        
                        # the properties below are optional
                        custom_actions=[networkfirewall.CfnRuleGroup.CustomActionProperty(
                            action_definition=networkfirewall.CfnRuleGroup.ActionDefinitionProperty(
                                publish_metric_action=networkfirewall.CfnRuleGroup.PublishMetricActionProperty(
                                    dimensions=[networkfirewall.CfnRuleGroup.DimensionProperty(
                                        value="value"
                                    )]
                                )
                            ),
                            action_name="actionName"
                        )]
                    )
                ),
        
                # the properties below are optional
                reference_sets=networkfirewall.CfnRuleGroup.ReferenceSetsProperty(
                    ip_set_references={
                        "ip_set_references_key": {
                            "reference_arn": "referenceArn"
                        }
                    }
                ),
                rule_variables=networkfirewall.CfnRuleGroup.RuleVariablesProperty(
                    ip_sets={
                        "ip_sets_key": {
                            "definition": ["definition"]
                        }
                    },
                    port_sets={
                        "port_sets_key": networkfirewall.CfnRuleGroup.PortSetProperty(
                            definition=["definition"]
                        )
                    }
                ),
                stateful_rule_options=networkfirewall.CfnRuleGroup.StatefulRuleOptionsProperty(
                    rule_order="ruleOrder"
                )
            ),
            tags=[CfnTag(
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
        capacity: jsii.Number,
        rule_group_name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        rule_group: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.RuleGroupProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::NetworkFirewall::RuleGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param capacity: The maximum operating resources that this rule group can use. You can't change a rule group's capacity setting after you create the rule group. When you update a rule group, you are limited to this capacity. When you reference a rule group from a firewall policy, Network Firewall reserves this capacity for the rule group.
        :param rule_group_name: The descriptive name of the rule group. You can't change the name of a rule group after you create it.
        :param type: Indicates whether the rule group is stateless or stateful. If the rule group is stateless, it contains stateless rules. If it is stateful, it contains stateful rules.
        :param description: A description of the rule group.
        :param rule_group: An object that defines the rule group rules.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2bed744c295734a9a31b12cdfa346e8e1a3faa7c1769cf2ae9d419c14f766bb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRuleGroupProps(
            capacity=capacity,
            rule_group_name=rule_group_name,
            type=type,
            description=description,
            rule_group=rule_group,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e9cfbbb9f560049c546c48ee14b258134c81fa07e078eff4bc8ce83f9ebcd71)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6d6407999ccd0ca7716cb84bebc040d294700858d002f62493ec63b90e805a6)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrRuleGroupArn")
    def attr_rule_group_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the ``RuleGroup`` .

        :cloudformationAttribute: RuleGroupArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRuleGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="attrRuleGroupId")
    def attr_rule_group_id(self) -> builtins.str:
        '''The unique ID of the ``RuleGroup`` resource.

        :cloudformationAttribute: RuleGroupId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRuleGroupId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="capacity")
    def capacity(self) -> jsii.Number:
        '''The maximum operating resources that this rule group can use.

        You can't change a rule group's capacity setting after you create the rule group. When you update a rule group, you are limited to this capacity. When you reference a rule group from a firewall policy, Network Firewall reserves this capacity for the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-capacity
        '''
        return typing.cast(jsii.Number, jsii.get(self, "capacity"))

    @capacity.setter
    def capacity(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2163e04eacfa0b18ca7e0ac22f7c794c26eff7c9717a4423cde5a1b95cab5439)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "capacity", value)

    @builtins.property
    @jsii.member(jsii_name="ruleGroupName")
    def rule_group_name(self) -> builtins.str:
        '''The descriptive name of the rule group.

        You can't change the name of a rule group after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleGroupName"))

    @rule_group_name.setter
    def rule_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8eef3e13e88ed9b5c3b1b0f92c0c230b40549c9f23eb5fc5a4c3921d8e149bb4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''Indicates whether the rule group is stateless or stateful.

        If the rule group is stateless, it contains
        stateless rules. If it is stateful, it contains stateful rules.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__681ae21bef43ebe64a227fca78b5efbaab91b3dfe2a02d66a3cd17f7faff538d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f2b03115ff3fc828c883937c6eb6123daa7fee8c419643091ff0a4144b16023)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="ruleGroup")
    def rule_group(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.RuleGroupProperty"]]:
        '''An object that defines the rule group rules.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.RuleGroupProperty"]], jsii.get(self, "ruleGroup"))

    @rule_group.setter
    def rule_group(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.RuleGroupProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c275f2557feddfa95030136eb9095c9ad1ead606a07ab9a65bd18ee74ccd9d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleGroup", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.ActionDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"publish_metric_action": "publishMetricAction"},
    )
    class ActionDefinitionProperty:
        def __init__(
            self,
            *,
            publish_metric_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.PublishMetricActionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''A custom action to use in stateless rule actions settings.

            :param publish_metric_action: Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet. This setting defines a CloudWatch dimension value to be published. You can pair this custom action with any of the standard stateless rule actions. For example, you could pair this in a rule action with the standard action that forwards the packet for stateful inspection. Then, when a packet matches the rule, Network Firewall publishes metrics for the packet and forwards it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-actiondefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                action_definition_property = networkfirewall.CfnRuleGroup.ActionDefinitionProperty(
                    publish_metric_action=networkfirewall.CfnRuleGroup.PublishMetricActionProperty(
                        dimensions=[networkfirewall.CfnRuleGroup.DimensionProperty(
                            value="value"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6372dd81c78c3500e1a4daff7629d3a1cc5b52770dedb29375245227e8246bc4)
                check_type(argname="argument publish_metric_action", value=publish_metric_action, expected_type=type_hints["publish_metric_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if publish_metric_action is not None:
                self._values["publish_metric_action"] = publish_metric_action

        @builtins.property
        def publish_metric_action(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.PublishMetricActionProperty"]]:
            '''Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet.

            This setting defines a CloudWatch dimension value to be published.

            You can pair this custom action with any of the standard stateless rule actions. For example, you could pair this in a rule action with the standard action that forwards the packet for stateful inspection. Then, when a packet matches the rule, Network Firewall publishes metrics for the packet and forwards it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-actiondefinition.html#cfn-networkfirewall-rulegroup-actiondefinition-publishmetricaction
            '''
            result = self._values.get("publish_metric_action")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.PublishMetricActionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.AddressProperty",
        jsii_struct_bases=[],
        name_mapping={"address_definition": "addressDefinition"},
    )
    class AddressProperty:
        def __init__(self, *, address_definition: builtins.str) -> None:
            '''A single IP address specification.

            This is used in the ``RuleGroup.MatchAttributes`` source and destination specifications.

            :param address_definition: Specify an IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Network Firewall supports all address ranges for IPv4. Examples: - To configure Network Firewall to inspect for the IP address 192.0.2.44, specify ``192.0.2.44/32`` . - To configure Network Firewall to inspect for IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` . For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-address.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                address_property = networkfirewall.CfnRuleGroup.AddressProperty(
                    address_definition="addressDefinition"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__29e078ac8466a97701aba834401dcb7198d690a79691f9464fecb557d85e3d05)
                check_type(argname="argument address_definition", value=address_definition, expected_type=type_hints["address_definition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "address_definition": address_definition,
            }

        @builtins.property
        def address_definition(self) -> builtins.str:
            '''Specify an IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation.

            Network Firewall supports all address ranges for IPv4.

            Examples:

            - To configure Network Firewall to inspect for the IP address 192.0.2.44, specify ``192.0.2.44/32`` .
            - To configure Network Firewall to inspect for IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` .

            For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-address.html#cfn-networkfirewall-rulegroup-address-addressdefinition
            '''
            result = self._values.get("address_definition")
            assert result is not None, "Required property 'address_definition' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AddressProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.CustomActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_definition": "actionDefinition",
            "action_name": "actionName",
        },
    )
    class CustomActionProperty:
        def __init__(
            self,
            *,
            action_definition: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.ActionDefinitionProperty", typing.Dict[builtins.str, typing.Any]]],
            action_name: builtins.str,
        ) -> None:
            '''An optional, non-standard action to use for stateless packet handling.

            You can define this in addition to the standard action that you must specify.

            You define and name the custom actions that you want to be able to use, and then you reference them by name in your actions settings.

            You can use custom actions in the following places:

            - In an ``RuleGroup.StatelessRulesAndCustomActions`` . The custom actions are available for use by name inside the ``StatelessRulesAndCustomActions`` where you define them. You can use them for your stateless rule actions to specify what to do with a packet that matches the rule's match attributes.
            - In an ``FirewallPolicy`` specification, in ``StatelessCustomActions`` . The custom actions are available for use inside the policy where you define them. You can use them for the policy's default stateless actions settings to specify what to do with packets that don't match any of the policy's stateless rules.

            :param action_definition: The custom action associated with the action name.
            :param action_name: The descriptive name of the custom action. You can't change the name of a custom action after you create it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-customaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                custom_action_property = networkfirewall.CfnRuleGroup.CustomActionProperty(
                    action_definition=networkfirewall.CfnRuleGroup.ActionDefinitionProperty(
                        publish_metric_action=networkfirewall.CfnRuleGroup.PublishMetricActionProperty(
                            dimensions=[networkfirewall.CfnRuleGroup.DimensionProperty(
                                value="value"
                            )]
                        )
                    ),
                    action_name="actionName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__98c730adebe9500c157c649f6e0172b2fa3b95baaae1da1502ba37132abc0fe2)
                check_type(argname="argument action_definition", value=action_definition, expected_type=type_hints["action_definition"])
                check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "action_definition": action_definition,
                "action_name": action_name,
            }

        @builtins.property
        def action_definition(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.ActionDefinitionProperty"]:
            '''The custom action associated with the action name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-customaction.html#cfn-networkfirewall-rulegroup-customaction-actiondefinition
            '''
            result = self._values.get("action_definition")
            assert result is not None, "Required property 'action_definition' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.ActionDefinitionProperty"], result)

        @builtins.property
        def action_name(self) -> builtins.str:
            '''The descriptive name of the custom action.

            You can't change the name of a custom action after you create it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-customaction.html#cfn-networkfirewall-rulegroup-customaction-actionname
            '''
            result = self._values.get("action_name")
            assert result is not None, "Required property 'action_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.DimensionProperty",
        jsii_struct_bases=[],
        name_mapping={"value": "value"},
    )
    class DimensionProperty:
        def __init__(self, *, value: builtins.str) -> None:
            '''The value to use in an Amazon CloudWatch custom metric dimension.

            This is used in the ``PublishMetrics`` custom action. A CloudWatch custom metric dimension is a name/value pair that's part of the identity of a metric.

            AWS Network Firewall sets the dimension name to ``CustomAction`` and you provide the dimension value.

            For more information about CloudWatch custom metric dimensions, see `Publishing Custom Metrics <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/publishingMetrics.html#usingDimensions>`_ in the `Amazon CloudWatch User Guide <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html>`_ .

            :param value: The value to use in the custom metric dimension.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-dimension.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                dimension_property = networkfirewall.CfnRuleGroup.DimensionProperty(
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d17f0084c420cf17e184f0ea6bd9d55eb5ba57c9593d4f80927ab7c2ac130823)
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "value": value,
            }

        @builtins.property
        def value(self) -> builtins.str:
            '''The value to use in the custom metric dimension.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-dimension.html#cfn-networkfirewall-rulegroup-dimension-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DimensionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.HeaderProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination": "destination",
            "destination_port": "destinationPort",
            "direction": "direction",
            "protocol": "protocol",
            "source": "source",
            "source_port": "sourcePort",
        },
    )
    class HeaderProperty:
        def __init__(
            self,
            *,
            destination: builtins.str,
            destination_port: builtins.str,
            direction: builtins.str,
            protocol: builtins.str,
            source: builtins.str,
            source_port: builtins.str,
        ) -> None:
            '''The 5-tuple criteria for AWS Network Firewall to use to inspect packet headers in stateful traffic flow inspection.

            Traffic flows that match the criteria are a match for the corresponding stateful rule.

            :param destination: The destination IP address or address range to inspect for, in CIDR notation. To match with any address, specify ``ANY`` . Specify an IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Network Firewall supports all address ranges for IPv4. Examples: - To configure Network Firewall to inspect for the IP address 192.0.2.44, specify ``192.0.2.44/32`` . - To configure Network Firewall to inspect for IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` . For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .
            :param destination_port: The destination port to inspect for. You can specify an individual port, for example ``1994`` and you can specify a port range, for example ``1990:1994`` . To match with any port, specify ``ANY`` .
            :param direction: The direction of traffic flow to inspect. If set to ``ANY`` , the inspection matches bidirectional traffic, both from the source to the destination and from the destination to the source. If set to ``FORWARD`` , the inspection only matches traffic going from the source to the destination.
            :param protocol: The protocol to inspect for. To specify all, you can use ``IP`` , because all traffic on AWS and on the internet is IP.
            :param source: The source IP address or address range to inspect for, in CIDR notation. To match with any address, specify ``ANY`` . Specify an IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Network Firewall supports all address ranges for IPv4. Examples: - To configure Network Firewall to inspect for the IP address 192.0.2.44, specify ``192.0.2.44/32`` . - To configure Network Firewall to inspect for IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` . For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .
            :param source_port: The source port to inspect for. You can specify an individual port, for example ``1994`` and you can specify a port range, for example ``1990:1994`` . To match with any port, specify ``ANY`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                header_property = networkfirewall.CfnRuleGroup.HeaderProperty(
                    destination="destination",
                    destination_port="destinationPort",
                    direction="direction",
                    protocol="protocol",
                    source="source",
                    source_port="sourcePort"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f41645f51d939972848dc88c2c84fa11a33468a4f5a569c2d3c57a7de1238d6d)
                check_type(argname="argument destination", value=destination, expected_type=type_hints["destination"])
                check_type(argname="argument destination_port", value=destination_port, expected_type=type_hints["destination_port"])
                check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument source_port", value=source_port, expected_type=type_hints["source_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "destination": destination,
                "destination_port": destination_port,
                "direction": direction,
                "protocol": protocol,
                "source": source,
                "source_port": source_port,
            }

        @builtins.property
        def destination(self) -> builtins.str:
            '''The destination IP address or address range to inspect for, in CIDR notation.

            To match with any address, specify ``ANY`` .

            Specify an IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Network Firewall supports all address ranges for IPv4.

            Examples:

            - To configure Network Firewall to inspect for the IP address 192.0.2.44, specify ``192.0.2.44/32`` .
            - To configure Network Firewall to inspect for IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` .

            For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-destination
            '''
            result = self._values.get("destination")
            assert result is not None, "Required property 'destination' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def destination_port(self) -> builtins.str:
            '''The destination port to inspect for.

            You can specify an individual port, for example ``1994`` and you can specify a port range, for example ``1990:1994`` . To match with any port, specify ``ANY`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-destinationport
            '''
            result = self._values.get("destination_port")
            assert result is not None, "Required property 'destination_port' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def direction(self) -> builtins.str:
            '''The direction of traffic flow to inspect.

            If set to ``ANY`` , the inspection matches bidirectional traffic, both from the source to the destination and from the destination to the source. If set to ``FORWARD`` , the inspection only matches traffic going from the source to the destination.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-direction
            '''
            result = self._values.get("direction")
            assert result is not None, "Required property 'direction' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def protocol(self) -> builtins.str:
            '''The protocol to inspect for.

            To specify all, you can use ``IP`` , because all traffic on AWS and on the internet is IP.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-protocol
            '''
            result = self._values.get("protocol")
            assert result is not None, "Required property 'protocol' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def source(self) -> builtins.str:
            '''The source IP address or address range to inspect for, in CIDR notation.

            To match with any address, specify ``ANY`` .

            Specify an IP address or a block of IP addresses in Classless Inter-Domain Routing (CIDR) notation. Network Firewall supports all address ranges for IPv4.

            Examples:

            - To configure Network Firewall to inspect for the IP address 192.0.2.44, specify ``192.0.2.44/32`` .
            - To configure Network Firewall to inspect for IP addresses from 192.0.2.0 to 192.0.2.255, specify ``192.0.2.0/24`` .

            For more information about CIDR notation, see the Wikipedia entry `Classless Inter-Domain Routing <https://docs.aws.amazon.com/https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-source
            '''
            result = self._values.get("source")
            assert result is not None, "Required property 'source' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def source_port(self) -> builtins.str:
            '''The source port to inspect for.

            You can specify an individual port, for example ``1994`` and you can specify a port range, for example ``1990:1994`` . To match with any port, specify ``ANY`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-header.html#cfn-networkfirewall-rulegroup-header-sourceport
            '''
            result = self._values.get("source_port")
            assert result is not None, "Required property 'source_port' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeaderProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.IPSetProperty",
        jsii_struct_bases=[],
        name_mapping={"definition": "definition"},
    )
    class IPSetProperty:
        def __init__(
            self,
            *,
            definition: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A list of IP addresses and address ranges, in CIDR notation.

            This is part of a ``RuleGroup.RuleVariables`` .

            :param definition: The list of IP addresses and address ranges, in CIDR notation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ipset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                i_pSet_property = {
                    "definition": ["definition"]
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a4f33b066cc14f1cc6c8679aab02ce640b84221a523cde9f3c7635f61d3ae066)
                check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if definition is not None:
                self._values["definition"] = definition

        @builtins.property
        def definition(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The list of IP addresses and address ranges, in CIDR notation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ipset.html#cfn-networkfirewall-rulegroup-ipset-definition
            '''
            result = self._values.get("definition")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IPSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.IPSetReferenceProperty",
        jsii_struct_bases=[],
        name_mapping={"reference_arn": "referenceArn"},
    )
    class IPSetReferenceProperty:
        def __init__(
            self,
            *,
            reference_arn: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Configures one or more ``IPSetReferences`` for a Suricata-compatible rule group.

            An IP set reference is a rule variable that references a resource that you create and manage in another AWS service, such as an Amazon VPC prefix list. Network Firewall IP set references enable you to dynamically update the contents of your rules. When you create, update, or delete the IP set you are referencing in your rule, Network Firewall automatically updates the rule's content with the changes. For more information about IP set references in Network Firewall , see `Using IP set references <https://docs.aws.amazon.com/network-firewall/latest/developerguide/rule-groups-ip-set-references.html>`_ in the *Network Firewall Developer Guide* .

            :param reference_arn: The Amazon Resource Name (ARN) of the resource to include in the ``RuleGroup.IPSetReference`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ipsetreference.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                i_pSet_reference_property = {
                    "reference_arn": "referenceArn"
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__662b3cfba2f4d1f368fc454475f3e9b13fab670d101cf4b34f429a717c7c04f7)
                check_type(argname="argument reference_arn", value=reference_arn, expected_type=type_hints["reference_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if reference_arn is not None:
                self._values["reference_arn"] = reference_arn

        @builtins.property
        def reference_arn(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the resource to include in the ``RuleGroup.IPSetReference`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ipsetreference.html#cfn-networkfirewall-rulegroup-ipsetreference-referencearn
            '''
            result = self._values.get("reference_arn")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IPSetReferenceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.MatchAttributesProperty",
        jsii_struct_bases=[],
        name_mapping={
            "destination_ports": "destinationPorts",
            "destinations": "destinations",
            "protocols": "protocols",
            "source_ports": "sourcePorts",
            "sources": "sources",
            "tcp_flags": "tcpFlags",
        },
    )
    class MatchAttributesProperty:
        def __init__(
            self,
            *,
            destination_ports: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.PortRangeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            destinations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.AddressProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            protocols: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[jsii.Number]]] = None,
            source_ports: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.PortRangeProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            sources: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.AddressProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            tcp_flags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.TCPFlagFieldProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Criteria for Network Firewall to use to inspect an individual packet in stateless rule inspection.

            Each match attributes set can include one or more items such as IP address, CIDR range, port number, protocol, and TCP flags.

            :param destination_ports: The destination ports to inspect for. If not specified, this matches with any destination port. This setting is only used for protocols 6 (TCP) and 17 (UDP). You can specify individual ports, for example ``1994`` and you can specify port ranges, for example ``1990:1994`` .
            :param destinations: The destination IP addresses and address ranges to inspect for, in CIDR notation. If not specified, this matches with any destination address.
            :param protocols: The protocols to inspect for, specified using each protocol's assigned internet protocol number (IANA). If not specified, this matches with any protocol.
            :param source_ports: The source ports to inspect for. If not specified, this matches with any source port. This setting is only used for protocols 6 (TCP) and 17 (UDP). You can specify individual ports, for example ``1994`` and you can specify port ranges, for example ``1990:1994`` .
            :param sources: The source IP addresses and address ranges to inspect for, in CIDR notation. If not specified, this matches with any source address.
            :param tcp_flags: The TCP flags and masks to inspect for. If not specified, this matches with any settings. This setting is only used for protocol 6 (TCP).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                match_attributes_property = networkfirewall.CfnRuleGroup.MatchAttributesProperty(
                    destination_ports=[networkfirewall.CfnRuleGroup.PortRangeProperty(
                        from_port=123,
                        to_port=123
                    )],
                    destinations=[networkfirewall.CfnRuleGroup.AddressProperty(
                        address_definition="addressDefinition"
                    )],
                    protocols=[123],
                    source_ports=[networkfirewall.CfnRuleGroup.PortRangeProperty(
                        from_port=123,
                        to_port=123
                    )],
                    sources=[networkfirewall.CfnRuleGroup.AddressProperty(
                        address_definition="addressDefinition"
                    )],
                    tcp_flags=[networkfirewall.CfnRuleGroup.TCPFlagFieldProperty(
                        flags=["flags"],
                
                        # the properties below are optional
                        masks=["masks"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__cfca8d9a633e425515babc1b91dc0118449c0c4d43ae95cdd3c68c688a5526b6)
                check_type(argname="argument destination_ports", value=destination_ports, expected_type=type_hints["destination_ports"])
                check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
                check_type(argname="argument protocols", value=protocols, expected_type=type_hints["protocols"])
                check_type(argname="argument source_ports", value=source_ports, expected_type=type_hints["source_ports"])
                check_type(argname="argument sources", value=sources, expected_type=type_hints["sources"])
                check_type(argname="argument tcp_flags", value=tcp_flags, expected_type=type_hints["tcp_flags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if destination_ports is not None:
                self._values["destination_ports"] = destination_ports
            if destinations is not None:
                self._values["destinations"] = destinations
            if protocols is not None:
                self._values["protocols"] = protocols
            if source_ports is not None:
                self._values["source_ports"] = source_ports
            if sources is not None:
                self._values["sources"] = sources
            if tcp_flags is not None:
                self._values["tcp_flags"] = tcp_flags

        @builtins.property
        def destination_ports(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.PortRangeProperty"]]]]:
            '''The destination ports to inspect for.

            If not specified, this matches with any destination port. This setting is only used for protocols 6 (TCP) and 17 (UDP).

            You can specify individual ports, for example ``1994`` and you can specify port ranges, for example ``1990:1994`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-destinationports
            '''
            result = self._values.get("destination_ports")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.PortRangeProperty"]]]], result)

        @builtins.property
        def destinations(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.AddressProperty"]]]]:
            '''The destination IP addresses and address ranges to inspect for, in CIDR notation.

            If not specified, this matches with any destination address.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-destinations
            '''
            result = self._values.get("destinations")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.AddressProperty"]]]], result)

        @builtins.property
        def protocols(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[jsii.Number]]]:
            '''The protocols to inspect for, specified using each protocol's assigned internet protocol number (IANA).

            If not specified, this matches with any protocol.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-protocols
            '''
            result = self._values.get("protocols")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[jsii.Number]]], result)

        @builtins.property
        def source_ports(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.PortRangeProperty"]]]]:
            '''The source ports to inspect for.

            If not specified, this matches with any source port. This setting is only used for protocols 6 (TCP) and 17 (UDP).

            You can specify individual ports, for example ``1994`` and you can specify port ranges, for example ``1990:1994`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-sourceports
            '''
            result = self._values.get("source_ports")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.PortRangeProperty"]]]], result)

        @builtins.property
        def sources(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.AddressProperty"]]]]:
            '''The source IP addresses and address ranges to inspect for, in CIDR notation.

            If not specified, this matches with any source address.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-sources
            '''
            result = self._values.get("sources")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.AddressProperty"]]]], result)

        @builtins.property
        def tcp_flags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.TCPFlagFieldProperty"]]]]:
            '''The TCP flags and masks to inspect for.

            If not specified, this matches with any settings. This setting is only used for protocol 6 (TCP).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-tcpflags
            '''
            result = self._values.get("tcp_flags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.TCPFlagFieldProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatchAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.PortRangeProperty",
        jsii_struct_bases=[],
        name_mapping={"from_port": "fromPort", "to_port": "toPort"},
    )
    class PortRangeProperty:
        def __init__(self, *, from_port: jsii.Number, to_port: jsii.Number) -> None:
            '''A single port range specification.

            This is used for source and destination port ranges in the stateless ``RuleGroup.MatchAttributes`` .

            :param from_port: The lower limit of the port range. This must be less than or equal to the ``ToPort`` specification.
            :param to_port: The upper limit of the port range. This must be greater than or equal to the ``FromPort`` specification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-portrange.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                port_range_property = networkfirewall.CfnRuleGroup.PortRangeProperty(
                    from_port=123,
                    to_port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a83182100058e2dc63b44857786bdfc9719f204dbc2d3480ff24661d4968a4a2)
                check_type(argname="argument from_port", value=from_port, expected_type=type_hints["from_port"])
                check_type(argname="argument to_port", value=to_port, expected_type=type_hints["to_port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "from_port": from_port,
                "to_port": to_port,
            }

        @builtins.property
        def from_port(self) -> jsii.Number:
            '''The lower limit of the port range.

            This must be less than or equal to the ``ToPort`` specification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-portrange.html#cfn-networkfirewall-rulegroup-portrange-fromport
            '''
            result = self._values.get("from_port")
            assert result is not None, "Required property 'from_port' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def to_port(self) -> jsii.Number:
            '''The upper limit of the port range.

            This must be greater than or equal to the ``FromPort`` specification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-portrange.html#cfn-networkfirewall-rulegroup-portrange-toport
            '''
            result = self._values.get("to_port")
            assert result is not None, "Required property 'to_port' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortRangeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.PortSetProperty",
        jsii_struct_bases=[],
        name_mapping={"definition": "definition"},
    )
    class PortSetProperty:
        def __init__(
            self,
            *,
            definition: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''A set of port ranges for use in the rules in a rule group.

            :param definition: The set of port ranges.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-portset.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                port_set_property = networkfirewall.CfnRuleGroup.PortSetProperty(
                    definition=["definition"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__411ce5f7e2a84f8c6b7e30dc9dc68cfd28775fadff74f37f724e87f5f662c40f)
                check_type(argname="argument definition", value=definition, expected_type=type_hints["definition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if definition is not None:
                self._values["definition"] = definition

        @builtins.property
        def definition(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The set of port ranges.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-portset.html#cfn-networkfirewall-rulegroup-portset-definition
            '''
            result = self._values.get("definition")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PortSetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.PublishMetricActionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimensions": "dimensions"},
    )
    class PublishMetricActionProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.DimensionProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet.

            This setting defines a CloudWatch dimension value to be published.

            :param dimensions: ``CfnRuleGroup.PublishMetricActionProperty.Dimensions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-publishmetricaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                publish_metric_action_property = networkfirewall.CfnRuleGroup.PublishMetricActionProperty(
                    dimensions=[networkfirewall.CfnRuleGroup.DimensionProperty(
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__879ffb0bb9984ae218137d5110b0e7fa519e7be74f7c38725b3b376b1e1efbd5)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "dimensions": dimensions,
            }

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.DimensionProperty"]]]:
            '''``CfnRuleGroup.PublishMetricActionProperty.Dimensions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-publishmetricaction.html#cfn-networkfirewall-rulegroup-publishmetricaction-dimensions
            '''
            result = self._values.get("dimensions")
            assert result is not None, "Required property 'dimensions' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.DimensionProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublishMetricActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.ReferenceSetsProperty",
        jsii_struct_bases=[],
        name_mapping={"ip_set_references": "ipSetReferences"},
    )
    class ReferenceSetsProperty:
        def __init__(
            self,
            *,
            ip_set_references: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.IPSetReferenceProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Configures the ``ReferenceSets`` for a stateful rule group.

            For more information, see the `Using IP set references in Suricata compatible rule groups <https://docs.aws.amazon.com/network-firewall/latest/developerguide/rule-groups-ip-set-references.html>`_ in the *Network Firewall User Guide* .

            :param ip_set_references: The IP set references to use in the stateful rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-referencesets.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                reference_sets_property = networkfirewall.CfnRuleGroup.ReferenceSetsProperty(
                    ip_set_references={
                        "ip_set_references_key": {
                            "reference_arn": "referenceArn"
                        }
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9abebd8d84f9a8a9bab75307896e9ddc7e0aeed3f5c4f4370f5f538641675cdc)
                check_type(argname="argument ip_set_references", value=ip_set_references, expected_type=type_hints["ip_set_references"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip_set_references is not None:
                self._values["ip_set_references"] = ip_set_references

        @builtins.property
        def ip_set_references(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.IPSetReferenceProperty"]]]]:
            '''The IP set references to use in the stateful rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-referencesets.html#cfn-networkfirewall-rulegroup-referencesets-ipsetreferences
            '''
            result = self._values.get("ip_set_references")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.IPSetReferenceProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReferenceSetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.RuleDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"actions": "actions", "match_attributes": "matchAttributes"},
    )
    class RuleDefinitionProperty:
        def __init__(
            self,
            *,
            actions: typing.Sequence[builtins.str],
            match_attributes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.MatchAttributesProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''The inspection criteria and action for a single stateless rule.

            AWS Network Firewall inspects each packet for the specified matching criteria. When a packet matches the criteria, Network Firewall performs the rule's actions on the packet.

            :param actions: The actions to take on a packet that matches one of the stateless rule definition's match attributes. You must specify a standard action and you can add custom actions. .. epigraph:: Network Firewall only forwards a packet for stateful rule inspection if you specify ``aws:forward_to_sfe`` for a rule that the packet matches, or if the packet doesn't match any stateless rule and you specify ``aws:forward_to_sfe`` for the ``StatelessDefaultActions`` setting for the ``FirewallPolicy`` . For every rule, you must specify exactly one of the following standard actions. - *aws:pass* - Discontinues all inspection of the packet and permits it to go to its intended destination. - *aws:drop* - Discontinues all inspection of the packet and blocks it from going to its intended destination. - *aws:forward_to_sfe* - Discontinues stateless inspection of the packet and forwards it to the stateful rule engine for inspection. Additionally, you can specify a custom action. To do this, you define a custom action by name and type, then provide the name you've assigned to the action in this ``Actions`` setting. To provide more than one action in this setting, separate the settings with a comma. For example, if you have a publish metrics custom action that you've named ``MyMetricsAction`` , then you could specify the standard action ``aws:pass`` combined with the custom action using ``[“aws:pass”, “MyMetricsAction”]`` .
            :param match_attributes: Criteria for Network Firewall to use to inspect an individual packet in stateless rule inspection. Each match attributes set can include one or more items such as IP address, CIDR range, port number, protocol, and TCP flags.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruledefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                rule_definition_property = networkfirewall.CfnRuleGroup.RuleDefinitionProperty(
                    actions=["actions"],
                    match_attributes=networkfirewall.CfnRuleGroup.MatchAttributesProperty(
                        destination_ports=[networkfirewall.CfnRuleGroup.PortRangeProperty(
                            from_port=123,
                            to_port=123
                        )],
                        destinations=[networkfirewall.CfnRuleGroup.AddressProperty(
                            address_definition="addressDefinition"
                        )],
                        protocols=[123],
                        source_ports=[networkfirewall.CfnRuleGroup.PortRangeProperty(
                            from_port=123,
                            to_port=123
                        )],
                        sources=[networkfirewall.CfnRuleGroup.AddressProperty(
                            address_definition="addressDefinition"
                        )],
                        tcp_flags=[networkfirewall.CfnRuleGroup.TCPFlagFieldProperty(
                            flags=["flags"],
                
                            # the properties below are optional
                            masks=["masks"]
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__43c19f099b082af7510e0d7df1fa00fbf7164c679af42b11277d118596c81d44)
                check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
                check_type(argname="argument match_attributes", value=match_attributes, expected_type=type_hints["match_attributes"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "actions": actions,
                "match_attributes": match_attributes,
            }

        @builtins.property
        def actions(self) -> typing.List[builtins.str]:
            '''The actions to take on a packet that matches one of the stateless rule definition's match attributes.

            You must specify a standard action and you can add custom actions.
            .. epigraph::

               Network Firewall only forwards a packet for stateful rule inspection if you specify ``aws:forward_to_sfe`` for a rule that the packet matches, or if the packet doesn't match any stateless rule and you specify ``aws:forward_to_sfe`` for the ``StatelessDefaultActions`` setting for the ``FirewallPolicy`` .

            For every rule, you must specify exactly one of the following standard actions.

            - *aws:pass* - Discontinues all inspection of the packet and permits it to go to its intended destination.
            - *aws:drop* - Discontinues all inspection of the packet and blocks it from going to its intended destination.
            - *aws:forward_to_sfe* - Discontinues stateless inspection of the packet and forwards it to the stateful rule engine for inspection.

            Additionally, you can specify a custom action. To do this, you define a custom action by name and type, then provide the name you've assigned to the action in this ``Actions`` setting.

            To provide more than one action in this setting, separate the settings with a comma. For example, if you have a publish metrics custom action that you've named ``MyMetricsAction`` , then you could specify the standard action ``aws:pass`` combined with the custom action using ``[“aws:pass”, “MyMetricsAction”]`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruledefinition.html#cfn-networkfirewall-rulegroup-ruledefinition-actions
            '''
            result = self._values.get("actions")
            assert result is not None, "Required property 'actions' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def match_attributes(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.MatchAttributesProperty"]:
            '''Criteria for Network Firewall to use to inspect an individual packet in stateless rule inspection.

            Each match attributes set can include one or more items such as IP address, CIDR range, port number, protocol, and TCP flags.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruledefinition.html#cfn-networkfirewall-rulegroup-ruledefinition-matchattributes
            '''
            result = self._values.get("match_attributes")
            assert result is not None, "Required property 'match_attributes' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.MatchAttributesProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.RuleGroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "rules_source": "rulesSource",
            "reference_sets": "referenceSets",
            "rule_variables": "ruleVariables",
            "stateful_rule_options": "statefulRuleOptions",
        },
    )
    class RuleGroupProperty:
        def __init__(
            self,
            *,
            rules_source: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.RulesSourceProperty", typing.Dict[builtins.str, typing.Any]]],
            reference_sets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.ReferenceSetsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rule_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.RuleVariablesProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            stateful_rule_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.StatefulRuleOptionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The object that defines the rules in a rule group.

            AWS Network Firewall uses a rule group to inspect and control network traffic. You define stateless rule groups to inspect individual packets and you define stateful rule groups to inspect packets in the context of their traffic flow.

            To use a rule group, you include it by reference in an Network Firewall firewall policy, then you use the policy in a firewall. You can reference a rule group from more than one firewall policy, and you can use a firewall policy in more than one firewall.

            :param rules_source: The stateful rules or stateless rules for the rule group.
            :param reference_sets: The reference sets for the stateful rule group.
            :param rule_variables: Settings that are available for use in the rules in the rule group. You can only use these for stateful rule groups.
            :param stateful_rule_options: Additional options governing how Network Firewall handles stateful rules. The policies where you use your stateful rule group must have stateful rule options settings that are compatible with these settings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulegroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                rule_group_property = networkfirewall.CfnRuleGroup.RuleGroupProperty(
                    rules_source=networkfirewall.CfnRuleGroup.RulesSourceProperty(
                        rules_source_list=networkfirewall.CfnRuleGroup.RulesSourceListProperty(
                            generated_rules_type="generatedRulesType",
                            targets=["targets"],
                            target_types=["targetTypes"]
                        ),
                        rules_string="rulesString",
                        stateful_rules=[networkfirewall.CfnRuleGroup.StatefulRuleProperty(
                            action="action",
                            header=networkfirewall.CfnRuleGroup.HeaderProperty(
                                destination="destination",
                                destination_port="destinationPort",
                                direction="direction",
                                protocol="protocol",
                                source="source",
                                source_port="sourcePort"
                            ),
                            rule_options=[networkfirewall.CfnRuleGroup.RuleOptionProperty(
                                keyword="keyword",
                
                                # the properties below are optional
                                settings=["settings"]
                            )]
                        )],
                        stateless_rules_and_custom_actions=networkfirewall.CfnRuleGroup.StatelessRulesAndCustomActionsProperty(
                            stateless_rules=[networkfirewall.CfnRuleGroup.StatelessRuleProperty(
                                priority=123,
                                rule_definition=networkfirewall.CfnRuleGroup.RuleDefinitionProperty(
                                    actions=["actions"],
                                    match_attributes=networkfirewall.CfnRuleGroup.MatchAttributesProperty(
                                        destination_ports=[networkfirewall.CfnRuleGroup.PortRangeProperty(
                                            from_port=123,
                                            to_port=123
                                        )],
                                        destinations=[networkfirewall.CfnRuleGroup.AddressProperty(
                                            address_definition="addressDefinition"
                                        )],
                                        protocols=[123],
                                        source_ports=[networkfirewall.CfnRuleGroup.PortRangeProperty(
                                            from_port=123,
                                            to_port=123
                                        )],
                                        sources=[networkfirewall.CfnRuleGroup.AddressProperty(
                                            address_definition="addressDefinition"
                                        )],
                                        tcp_flags=[networkfirewall.CfnRuleGroup.TCPFlagFieldProperty(
                                            flags=["flags"],
                
                                            # the properties below are optional
                                            masks=["masks"]
                                        )]
                                    )
                                )
                            )],
                
                            # the properties below are optional
                            custom_actions=[networkfirewall.CfnRuleGroup.CustomActionProperty(
                                action_definition=networkfirewall.CfnRuleGroup.ActionDefinitionProperty(
                                    publish_metric_action=networkfirewall.CfnRuleGroup.PublishMetricActionProperty(
                                        dimensions=[networkfirewall.CfnRuleGroup.DimensionProperty(
                                            value="value"
                                        )]
                                    )
                                ),
                                action_name="actionName"
                            )]
                        )
                    ),
                
                    # the properties below are optional
                    reference_sets=networkfirewall.CfnRuleGroup.ReferenceSetsProperty(
                        ip_set_references={
                            "ip_set_references_key": {
                                "reference_arn": "referenceArn"
                            }
                        }
                    ),
                    rule_variables=networkfirewall.CfnRuleGroup.RuleVariablesProperty(
                        ip_sets={
                            "ip_sets_key": {
                                "definition": ["definition"]
                            }
                        },
                        port_sets={
                            "port_sets_key": networkfirewall.CfnRuleGroup.PortSetProperty(
                                definition=["definition"]
                            )
                        }
                    ),
                    stateful_rule_options=networkfirewall.CfnRuleGroup.StatefulRuleOptionsProperty(
                        rule_order="ruleOrder"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2af100bf042e6e4899857646cfd5c613ed122be76f69b4f12f4c7a32ba06c1a7)
                check_type(argname="argument rules_source", value=rules_source, expected_type=type_hints["rules_source"])
                check_type(argname="argument reference_sets", value=reference_sets, expected_type=type_hints["reference_sets"])
                check_type(argname="argument rule_variables", value=rule_variables, expected_type=type_hints["rule_variables"])
                check_type(argname="argument stateful_rule_options", value=stateful_rule_options, expected_type=type_hints["stateful_rule_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "rules_source": rules_source,
            }
            if reference_sets is not None:
                self._values["reference_sets"] = reference_sets
            if rule_variables is not None:
                self._values["rule_variables"] = rule_variables
            if stateful_rule_options is not None:
                self._values["stateful_rule_options"] = stateful_rule_options

        @builtins.property
        def rules_source(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.RulesSourceProperty"]:
            '''The stateful rules or stateless rules for the rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup-rulessource
            '''
            result = self._values.get("rules_source")
            assert result is not None, "Required property 'rules_source' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.RulesSourceProperty"], result)

        @builtins.property
        def reference_sets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.ReferenceSetsProperty"]]:
            '''The reference sets for the stateful rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup-referencesets
            '''
            result = self._values.get("reference_sets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.ReferenceSetsProperty"]], result)

        @builtins.property
        def rule_variables(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.RuleVariablesProperty"]]:
            '''Settings that are available for use in the rules in the rule group.

            You can only use these for stateful rule groups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup-rulevariables
            '''
            result = self._values.get("rule_variables")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.RuleVariablesProperty"]], result)

        @builtins.property
        def stateful_rule_options(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.StatefulRuleOptionsProperty"]]:
            '''Additional options governing how Network Firewall handles stateful rules.

            The policies where you use your stateful rule group must have stateful rule options settings that are compatible with these settings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup-statefulruleoptions
            '''
            result = self._values.get("stateful_rule_options")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.StatefulRuleOptionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.RuleOptionProperty",
        jsii_struct_bases=[],
        name_mapping={"keyword": "keyword", "settings": "settings"},
    )
    class RuleOptionProperty:
        def __init__(
            self,
            *,
            keyword: builtins.str,
            settings: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Additional settings for a stateful rule.

            :param keyword: ``CfnRuleGroup.RuleOptionProperty.Keyword``.
            :param settings: ``CfnRuleGroup.RuleOptionProperty.Settings``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruleoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                rule_option_property = networkfirewall.CfnRuleGroup.RuleOptionProperty(
                    keyword="keyword",
                
                    # the properties below are optional
                    settings=["settings"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e59f27890737d73ab1365709d4946bb82d72498e645ec26af2adb967d671bf1c)
                check_type(argname="argument keyword", value=keyword, expected_type=type_hints["keyword"])
                check_type(argname="argument settings", value=settings, expected_type=type_hints["settings"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "keyword": keyword,
            }
            if settings is not None:
                self._values["settings"] = settings

        @builtins.property
        def keyword(self) -> builtins.str:
            '''``CfnRuleGroup.RuleOptionProperty.Keyword``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruleoption.html#cfn-networkfirewall-rulegroup-ruleoption-keyword
            '''
            result = self._values.get("keyword")
            assert result is not None, "Required property 'keyword' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def settings(self) -> typing.Optional[typing.List[builtins.str]]:
            '''``CfnRuleGroup.RuleOptionProperty.Settings``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruleoption.html#cfn-networkfirewall-rulegroup-ruleoption-settings
            '''
            result = self._values.get("settings")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.RuleVariablesProperty",
        jsii_struct_bases=[],
        name_mapping={"ip_sets": "ipSets", "port_sets": "portSets"},
    )
    class RuleVariablesProperty:
        def __init__(
            self,
            *,
            ip_sets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.IPSetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            port_sets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.PortSetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Settings that are available for use in the rules in the ``RuleGroup`` where this is defined.

            :param ip_sets: A list of IP addresses and address ranges, in CIDR notation.
            :param port_sets: A list of port ranges.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulevariables.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                rule_variables_property = networkfirewall.CfnRuleGroup.RuleVariablesProperty(
                    ip_sets={
                        "ip_sets_key": {
                            "definition": ["definition"]
                        }
                    },
                    port_sets={
                        "port_sets_key": networkfirewall.CfnRuleGroup.PortSetProperty(
                            definition=["definition"]
                        )
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b3e5a0766b0fab0549e421f523823541e0e2a813c3c425cbb5f23477773c04e1)
                check_type(argname="argument ip_sets", value=ip_sets, expected_type=type_hints["ip_sets"])
                check_type(argname="argument port_sets", value=port_sets, expected_type=type_hints["port_sets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip_sets is not None:
                self._values["ip_sets"] = ip_sets
            if port_sets is not None:
                self._values["port_sets"] = port_sets

        @builtins.property
        def ip_sets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.IPSetProperty"]]]]:
            '''A list of IP addresses and address ranges, in CIDR notation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulevariables.html#cfn-networkfirewall-rulegroup-rulevariables-ipsets
            '''
            result = self._values.get("ip_sets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.IPSetProperty"]]]], result)

        @builtins.property
        def port_sets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.PortSetProperty"]]]]:
            '''A list of port ranges.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulevariables.html#cfn-networkfirewall-rulegroup-rulevariables-portsets
            '''
            result = self._values.get("port_sets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.PortSetProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleVariablesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.RulesSourceListProperty",
        jsii_struct_bases=[],
        name_mapping={
            "generated_rules_type": "generatedRulesType",
            "targets": "targets",
            "target_types": "targetTypes",
        },
    )
    class RulesSourceListProperty:
        def __init__(
            self,
            *,
            generated_rules_type: builtins.str,
            targets: typing.Sequence[builtins.str],
            target_types: typing.Sequence[builtins.str],
        ) -> None:
            '''Stateful inspection criteria for a domain list rule group.

            For HTTPS traffic, domain filtering is SNI-based. It uses the server name indicator extension of the TLS handshake.

            By default, Network Firewall domain list inspection only includes traffic coming from the VPC where you deploy the firewall. To inspect traffic from IP addresses outside of the deployment VPC, you set the ``HOME_NET`` rule variable to include the CIDR range of the deployment VPC plus the other CIDR ranges. For more information, see ``RuleGroup.RuleVariables`` in this guide and `Stateful domain list rule groups in AWS Network Firewall <https://docs.aws.amazon.com/network-firewall/latest/developerguide/stateful-rule-groups-domain-names.html>`_ in the *Network Firewall Developer Guide*

            :param generated_rules_type: Whether you want to allow or deny access to the domains in your target list.
            :param targets: The domains that you want to inspect for in your traffic flows. Valid domain specifications are the following:. - Explicit names. For example, ``abc.example.com`` matches only the domain ``abc.example.com`` . - Names that use a domain wildcard, which you indicate with an initial ' ``.`` '. For example, ``.example.com`` matches ``example.com`` and matches all subdomains of ``example.com`` , such as ``abc.example.com`` and ``www.example.com`` .
            :param target_types: The types of targets to inspect for. Valid values are ``TLS_SNI`` and ``HTTP_HOST`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessourcelist.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                rules_source_list_property = networkfirewall.CfnRuleGroup.RulesSourceListProperty(
                    generated_rules_type="generatedRulesType",
                    targets=["targets"],
                    target_types=["targetTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ecd3667810dac8d7236225216210e341701118d222d35fc12db68c33227b053a)
                check_type(argname="argument generated_rules_type", value=generated_rules_type, expected_type=type_hints["generated_rules_type"])
                check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
                check_type(argname="argument target_types", value=target_types, expected_type=type_hints["target_types"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "generated_rules_type": generated_rules_type,
                "targets": targets,
                "target_types": target_types,
            }

        @builtins.property
        def generated_rules_type(self) -> builtins.str:
            '''Whether you want to allow or deny access to the domains in your target list.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessourcelist.html#cfn-networkfirewall-rulegroup-rulessourcelist-generatedrulestype
            '''
            result = self._values.get("generated_rules_type")
            assert result is not None, "Required property 'generated_rules_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def targets(self) -> typing.List[builtins.str]:
            '''The domains that you want to inspect for in your traffic flows. Valid domain specifications are the following:.

            - Explicit names. For example, ``abc.example.com`` matches only the domain ``abc.example.com`` .
            - Names that use a domain wildcard, which you indicate with an initial ' ``.`` '. For example, ``.example.com`` matches ``example.com`` and matches all subdomains of ``example.com`` , such as ``abc.example.com`` and ``www.example.com`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessourcelist.html#cfn-networkfirewall-rulegroup-rulessourcelist-targets
            '''
            result = self._values.get("targets")
            assert result is not None, "Required property 'targets' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def target_types(self) -> typing.List[builtins.str]:
            '''The types of targets to inspect for.

            Valid values are ``TLS_SNI`` and ``HTTP_HOST`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessourcelist.html#cfn-networkfirewall-rulegroup-rulessourcelist-targettypes
            '''
            result = self._values.get("target_types")
            assert result is not None, "Required property 'target_types' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RulesSourceListProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.RulesSourceProperty",
        jsii_struct_bases=[],
        name_mapping={
            "rules_source_list": "rulesSourceList",
            "rules_string": "rulesString",
            "stateful_rules": "statefulRules",
            "stateless_rules_and_custom_actions": "statelessRulesAndCustomActions",
        },
    )
    class RulesSourceProperty:
        def __init__(
            self,
            *,
            rules_source_list: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.RulesSourceListProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            rules_string: typing.Optional[builtins.str] = None,
            stateful_rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.StatefulRuleProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            stateless_rules_and_custom_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.StatelessRulesAndCustomActionsProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The stateless or stateful rules definitions for use in a single rule group.

            Each rule group requires a single ``RulesSource`` . You can use an instance of this for either stateless rules or stateful rules.

            :param rules_source_list: Stateful inspection criteria for a domain list rule group.
            :param rules_string: Stateful inspection criteria, provided in Suricata compatible intrusion prevention system (IPS) rules. Suricata is an open-source network IPS that includes a standard rule-based language for network traffic inspection. These rules contain the inspection criteria and the action to take for traffic that matches the criteria, so this type of rule group doesn't have a separate action setting.
            :param stateful_rules: An array of individual stateful rules inspection criteria to be used together in a stateful rule group. Use this option to specify simple Suricata rules with protocol, source and destination, ports, direction, and rule options. For information about the Suricata ``Rules`` format, see `Rules Format <https://docs.aws.amazon.com/https://suricata.readthedocs.io/rules/intro.html#>`_ .
            :param stateless_rules_and_custom_actions: Stateless inspection criteria to be used in a stateless rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                rules_source_property = networkfirewall.CfnRuleGroup.RulesSourceProperty(
                    rules_source_list=networkfirewall.CfnRuleGroup.RulesSourceListProperty(
                        generated_rules_type="generatedRulesType",
                        targets=["targets"],
                        target_types=["targetTypes"]
                    ),
                    rules_string="rulesString",
                    stateful_rules=[networkfirewall.CfnRuleGroup.StatefulRuleProperty(
                        action="action",
                        header=networkfirewall.CfnRuleGroup.HeaderProperty(
                            destination="destination",
                            destination_port="destinationPort",
                            direction="direction",
                            protocol="protocol",
                            source="source",
                            source_port="sourcePort"
                        ),
                        rule_options=[networkfirewall.CfnRuleGroup.RuleOptionProperty(
                            keyword="keyword",
                
                            # the properties below are optional
                            settings=["settings"]
                        )]
                    )],
                    stateless_rules_and_custom_actions=networkfirewall.CfnRuleGroup.StatelessRulesAndCustomActionsProperty(
                        stateless_rules=[networkfirewall.CfnRuleGroup.StatelessRuleProperty(
                            priority=123,
                            rule_definition=networkfirewall.CfnRuleGroup.RuleDefinitionProperty(
                                actions=["actions"],
                                match_attributes=networkfirewall.CfnRuleGroup.MatchAttributesProperty(
                                    destination_ports=[networkfirewall.CfnRuleGroup.PortRangeProperty(
                                        from_port=123,
                                        to_port=123
                                    )],
                                    destinations=[networkfirewall.CfnRuleGroup.AddressProperty(
                                        address_definition="addressDefinition"
                                    )],
                                    protocols=[123],
                                    source_ports=[networkfirewall.CfnRuleGroup.PortRangeProperty(
                                        from_port=123,
                                        to_port=123
                                    )],
                                    sources=[networkfirewall.CfnRuleGroup.AddressProperty(
                                        address_definition="addressDefinition"
                                    )],
                                    tcp_flags=[networkfirewall.CfnRuleGroup.TCPFlagFieldProperty(
                                        flags=["flags"],
                
                                        # the properties below are optional
                                        masks=["masks"]
                                    )]
                                )
                            )
                        )],
                
                        # the properties below are optional
                        custom_actions=[networkfirewall.CfnRuleGroup.CustomActionProperty(
                            action_definition=networkfirewall.CfnRuleGroup.ActionDefinitionProperty(
                                publish_metric_action=networkfirewall.CfnRuleGroup.PublishMetricActionProperty(
                                    dimensions=[networkfirewall.CfnRuleGroup.DimensionProperty(
                                        value="value"
                                    )]
                                )
                            ),
                            action_name="actionName"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d4c5e11af1b4c815b7fd6a4d48bd91a4c2b4ade3a07175d32fc1c252a2f5e3a9)
                check_type(argname="argument rules_source_list", value=rules_source_list, expected_type=type_hints["rules_source_list"])
                check_type(argname="argument rules_string", value=rules_string, expected_type=type_hints["rules_string"])
                check_type(argname="argument stateful_rules", value=stateful_rules, expected_type=type_hints["stateful_rules"])
                check_type(argname="argument stateless_rules_and_custom_actions", value=stateless_rules_and_custom_actions, expected_type=type_hints["stateless_rules_and_custom_actions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rules_source_list is not None:
                self._values["rules_source_list"] = rules_source_list
            if rules_string is not None:
                self._values["rules_string"] = rules_string
            if stateful_rules is not None:
                self._values["stateful_rules"] = stateful_rules
            if stateless_rules_and_custom_actions is not None:
                self._values["stateless_rules_and_custom_actions"] = stateless_rules_and_custom_actions

        @builtins.property
        def rules_source_list(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.RulesSourceListProperty"]]:
            '''Stateful inspection criteria for a domain list rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html#cfn-networkfirewall-rulegroup-rulessource-rulessourcelist
            '''
            result = self._values.get("rules_source_list")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.RulesSourceListProperty"]], result)

        @builtins.property
        def rules_string(self) -> typing.Optional[builtins.str]:
            '''Stateful inspection criteria, provided in Suricata compatible intrusion prevention system (IPS) rules.

            Suricata is an open-source network IPS that includes a standard rule-based language for network traffic inspection.

            These rules contain the inspection criteria and the action to take for traffic that matches the criteria, so this type of rule group doesn't have a separate action setting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html#cfn-networkfirewall-rulegroup-rulessource-rulesstring
            '''
            result = self._values.get("rules_string")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stateful_rules(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.StatefulRuleProperty"]]]]:
            '''An array of individual stateful rules inspection criteria to be used together in a stateful rule group.

            Use this option to specify simple Suricata rules with protocol, source and destination, ports, direction, and rule options. For information about the Suricata ``Rules`` format, see `Rules Format <https://docs.aws.amazon.com/https://suricata.readthedocs.io/rules/intro.html#>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html#cfn-networkfirewall-rulegroup-rulessource-statefulrules
            '''
            result = self._values.get("stateful_rules")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.StatefulRuleProperty"]]]], result)

        @builtins.property
        def stateless_rules_and_custom_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.StatelessRulesAndCustomActionsProperty"]]:
            '''Stateless inspection criteria to be used in a stateless rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html#cfn-networkfirewall-rulegroup-rulessource-statelessrulesandcustomactions
            '''
            result = self._values.get("stateless_rules_and_custom_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.StatelessRulesAndCustomActionsProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RulesSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.StatefulRuleOptionsProperty",
        jsii_struct_bases=[],
        name_mapping={"rule_order": "ruleOrder"},
    )
    class StatefulRuleOptionsProperty:
        def __init__(self, *, rule_order: typing.Optional[builtins.str] = None) -> None:
            '''Additional options governing how Network Firewall handles the rule group.

            You can only use these for stateful rule groups.

            :param rule_order: Indicates how to manage the order of the rule evaluation for the rule group. ``DEFAULT_ACTION_ORDER`` is the default behavior. Stateful rules are provided to the rule engine as Suricata compatible strings, and Suricata evaluates them based on certain settings. For more information, see `Evaluation order for stateful rules <https://docs.aws.amazon.com/network-firewall/latest/developerguide/suricata-rule-evaluation-order.html>`_ in the *AWS Network Firewall Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulruleoptions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                stateful_rule_options_property = networkfirewall.CfnRuleGroup.StatefulRuleOptionsProperty(
                    rule_order="ruleOrder"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__8eb14b3c3d091145bbda5a1faccc8e5651d9f7213c1b9da465252d3a564924f1)
                check_type(argname="argument rule_order", value=rule_order, expected_type=type_hints["rule_order"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if rule_order is not None:
                self._values["rule_order"] = rule_order

        @builtins.property
        def rule_order(self) -> typing.Optional[builtins.str]:
            '''Indicates how to manage the order of the rule evaluation for the rule group.

            ``DEFAULT_ACTION_ORDER`` is the default behavior. Stateful rules are provided to the rule engine as Suricata compatible strings, and Suricata evaluates them based on certain settings. For more information, see `Evaluation order for stateful rules <https://docs.aws.amazon.com/network-firewall/latest/developerguide/suricata-rule-evaluation-order.html>`_ in the *AWS Network Firewall Developer Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulruleoptions.html#cfn-networkfirewall-rulegroup-statefulruleoptions-ruleorder
            '''
            result = self._values.get("rule_order")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatefulRuleOptionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.StatefulRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "header": "header",
            "rule_options": "ruleOptions",
        },
    )
    class StatefulRuleProperty:
        def __init__(
            self,
            *,
            action: builtins.str,
            header: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.HeaderProperty", typing.Dict[builtins.str, typing.Any]]],
            rule_options: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.RuleOptionProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''A single Suricata rules specification, for use in a stateful rule group.

            Use this option to specify a simple Suricata rule with protocol, source and destination, ports, direction, and rule options. For information about the Suricata ``Rules`` format, see `Rules Format <https://docs.aws.amazon.com/https://suricata.readthedocs.io/rules/intro.html#>`_ .

            :param action: Defines what Network Firewall should do with the packets in a traffic flow when the flow matches the stateful rule criteria. For all actions, Network Firewall performs the specified action and discontinues stateful inspection of the traffic flow. The actions for a stateful rule are defined as follows: - *PASS* - Permits the packets to go to the intended destination. - *DROP* - Blocks the packets from going to the intended destination and sends an alert log message, if alert logging is configured in the ``Firewall`` ``LoggingConfiguration`` . - *ALERT* - Permits the packets to go to the intended destination and sends an alert log message, if alert logging is configured in the ``Firewall`` ``LoggingConfiguration`` . You can use this action to test a rule that you intend to use to drop traffic. You can enable the rule with ``ALERT`` action, verify in the logs that the rule is filtering as you want, then change the action to ``DROP`` .
            :param header: The stateful inspection criteria for this rule, used to inspect traffic flows.
            :param rule_options: Additional settings for a stateful rule, provided as keywords and settings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                stateful_rule_property = networkfirewall.CfnRuleGroup.StatefulRuleProperty(
                    action="action",
                    header=networkfirewall.CfnRuleGroup.HeaderProperty(
                        destination="destination",
                        destination_port="destinationPort",
                        direction="direction",
                        protocol="protocol",
                        source="source",
                        source_port="sourcePort"
                    ),
                    rule_options=[networkfirewall.CfnRuleGroup.RuleOptionProperty(
                        keyword="keyword",
                
                        # the properties below are optional
                        settings=["settings"]
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__3b3ffd30e1527c1391554953822f4cd5033aa7f40a689fd5e0041be8a0814885)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument header", value=header, expected_type=type_hints["header"])
                check_type(argname="argument rule_options", value=rule_options, expected_type=type_hints["rule_options"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "action": action,
                "header": header,
                "rule_options": rule_options,
            }

        @builtins.property
        def action(self) -> builtins.str:
            '''Defines what Network Firewall should do with the packets in a traffic flow when the flow matches the stateful rule criteria.

            For all actions, Network Firewall performs the specified action and discontinues stateful inspection of the traffic flow.

            The actions for a stateful rule are defined as follows:

            - *PASS* - Permits the packets to go to the intended destination.
            - *DROP* - Blocks the packets from going to the intended destination and sends an alert log message, if alert logging is configured in the ``Firewall`` ``LoggingConfiguration`` .
            - *ALERT* - Permits the packets to go to the intended destination and sends an alert log message, if alert logging is configured in the ``Firewall`` ``LoggingConfiguration`` .

            You can use this action to test a rule that you intend to use to drop traffic. You can enable the rule with ``ALERT`` action, verify in the logs that the rule is filtering as you want, then change the action to ``DROP`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulrule.html#cfn-networkfirewall-rulegroup-statefulrule-action
            '''
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def header(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.HeaderProperty"]:
            '''The stateful inspection criteria for this rule, used to inspect traffic flows.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulrule.html#cfn-networkfirewall-rulegroup-statefulrule-header
            '''
            result = self._values.get("header")
            assert result is not None, "Required property 'header' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.HeaderProperty"], result)

        @builtins.property
        def rule_options(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.RuleOptionProperty"]]]:
            '''Additional settings for a stateful rule, provided as keywords and settings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulrule.html#cfn-networkfirewall-rulegroup-statefulrule-ruleoptions
            '''
            result = self._values.get("rule_options")
            assert result is not None, "Required property 'rule_options' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.RuleOptionProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatefulRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.StatelessRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"priority": "priority", "rule_definition": "ruleDefinition"},
    )
    class StatelessRuleProperty:
        def __init__(
            self,
            *,
            priority: jsii.Number,
            rule_definition: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.RuleDefinitionProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''A single stateless rule.

            This is used in ``RuleGroup.StatelessRulesAndCustomActions`` .

            :param priority: Indicates the order in which to run this rule relative to all of the rules that are defined for a stateless rule group. Network Firewall evaluates the rules in a rule group starting with the lowest priority setting. You must ensure that the priority settings are unique for the rule group. Each stateless rule group uses exactly one ``StatelessRulesAndCustomActions`` object, and each ``StatelessRulesAndCustomActions`` contains exactly one ``StatelessRules`` object. To ensure unique priority settings for your rule groups, set unique priorities for the stateless rules that you define inside any single ``StatelessRules`` object. You can change the priority settings of your rules at any time. To make it easier to insert rules later, number them so there's a wide range in between, for example use 100, 200, and so on.
            :param rule_definition: Defines the stateless 5-tuple packet inspection criteria and the action to take on a packet that matches the criteria.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                stateless_rule_property = networkfirewall.CfnRuleGroup.StatelessRuleProperty(
                    priority=123,
                    rule_definition=networkfirewall.CfnRuleGroup.RuleDefinitionProperty(
                        actions=["actions"],
                        match_attributes=networkfirewall.CfnRuleGroup.MatchAttributesProperty(
                            destination_ports=[networkfirewall.CfnRuleGroup.PortRangeProperty(
                                from_port=123,
                                to_port=123
                            )],
                            destinations=[networkfirewall.CfnRuleGroup.AddressProperty(
                                address_definition="addressDefinition"
                            )],
                            protocols=[123],
                            source_ports=[networkfirewall.CfnRuleGroup.PortRangeProperty(
                                from_port=123,
                                to_port=123
                            )],
                            sources=[networkfirewall.CfnRuleGroup.AddressProperty(
                                address_definition="addressDefinition"
                            )],
                            tcp_flags=[networkfirewall.CfnRuleGroup.TCPFlagFieldProperty(
                                flags=["flags"],
                
                                # the properties below are optional
                                masks=["masks"]
                            )]
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2e0f1282bb53fa7742fa0f209cabcdfb9bc549df520661cbb81c20e8de19211c)
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument rule_definition", value=rule_definition, expected_type=type_hints["rule_definition"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "priority": priority,
                "rule_definition": rule_definition,
            }

        @builtins.property
        def priority(self) -> jsii.Number:
            '''Indicates the order in which to run this rule relative to all of the rules that are defined for a stateless rule group.

            Network Firewall evaluates the rules in a rule group starting with the lowest priority setting. You must ensure that the priority settings are unique for the rule group.

            Each stateless rule group uses exactly one ``StatelessRulesAndCustomActions`` object, and each ``StatelessRulesAndCustomActions`` contains exactly one ``StatelessRules`` object. To ensure unique priority settings for your rule groups, set unique priorities for the stateless rules that you define inside any single ``StatelessRules`` object.

            You can change the priority settings of your rules at any time. To make it easier to insert rules later, number them so there's a wide range in between, for example use 100, 200, and so on.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrule.html#cfn-networkfirewall-rulegroup-statelessrule-priority
            '''
            result = self._values.get("priority")
            assert result is not None, "Required property 'priority' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def rule_definition(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.RuleDefinitionProperty"]:
            '''Defines the stateless 5-tuple packet inspection criteria and the action to take on a packet that matches the criteria.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrule.html#cfn-networkfirewall-rulegroup-statelessrule-ruledefinition
            '''
            result = self._values.get("rule_definition")
            assert result is not None, "Required property 'rule_definition' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.RuleDefinitionProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatelessRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.StatelessRulesAndCustomActionsProperty",
        jsii_struct_bases=[],
        name_mapping={
            "stateless_rules": "statelessRules",
            "custom_actions": "customActions",
        },
    )
    class StatelessRulesAndCustomActionsProperty:
        def __init__(
            self,
            *,
            stateless_rules: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.StatelessRuleProperty", typing.Dict[builtins.str, typing.Any]]]]],
            custom_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRuleGroup.CustomActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        ) -> None:
            '''Stateless inspection criteria.

            Each stateless rule group uses exactly one of these data types to define its stateless rules.

            :param stateless_rules: Defines the set of stateless rules for use in a stateless rule group.
            :param custom_actions: Defines an array of individual custom action definitions that are available for use by the stateless rules in this ``StatelessRulesAndCustomActions`` specification. You name each custom action that you define, and then you can use it by name in your stateless rule ``RuleGroup.RuleDefinition`` ``Actions`` specification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrulesandcustomactions.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                stateless_rules_and_custom_actions_property = networkfirewall.CfnRuleGroup.StatelessRulesAndCustomActionsProperty(
                    stateless_rules=[networkfirewall.CfnRuleGroup.StatelessRuleProperty(
                        priority=123,
                        rule_definition=networkfirewall.CfnRuleGroup.RuleDefinitionProperty(
                            actions=["actions"],
                            match_attributes=networkfirewall.CfnRuleGroup.MatchAttributesProperty(
                                destination_ports=[networkfirewall.CfnRuleGroup.PortRangeProperty(
                                    from_port=123,
                                    to_port=123
                                )],
                                destinations=[networkfirewall.CfnRuleGroup.AddressProperty(
                                    address_definition="addressDefinition"
                                )],
                                protocols=[123],
                                source_ports=[networkfirewall.CfnRuleGroup.PortRangeProperty(
                                    from_port=123,
                                    to_port=123
                                )],
                                sources=[networkfirewall.CfnRuleGroup.AddressProperty(
                                    address_definition="addressDefinition"
                                )],
                                tcp_flags=[networkfirewall.CfnRuleGroup.TCPFlagFieldProperty(
                                    flags=["flags"],
                
                                    # the properties below are optional
                                    masks=["masks"]
                                )]
                            )
                        )
                    )],
                
                    # the properties below are optional
                    custom_actions=[networkfirewall.CfnRuleGroup.CustomActionProperty(
                        action_definition=networkfirewall.CfnRuleGroup.ActionDefinitionProperty(
                            publish_metric_action=networkfirewall.CfnRuleGroup.PublishMetricActionProperty(
                                dimensions=[networkfirewall.CfnRuleGroup.DimensionProperty(
                                    value="value"
                                )]
                            )
                        ),
                        action_name="actionName"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dfc4ee05340befc6bf8c9802b1fbff290e85f4a60b9ea9486b8921cd9e903d13)
                check_type(argname="argument stateless_rules", value=stateless_rules, expected_type=type_hints["stateless_rules"])
                check_type(argname="argument custom_actions", value=custom_actions, expected_type=type_hints["custom_actions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "stateless_rules": stateless_rules,
            }
            if custom_actions is not None:
                self._values["custom_actions"] = custom_actions

        @builtins.property
        def stateless_rules(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.StatelessRuleProperty"]]]:
            '''Defines the set of stateless rules for use in a stateless rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrulesandcustomactions.html#cfn-networkfirewall-rulegroup-statelessrulesandcustomactions-statelessrules
            '''
            result = self._values.get("stateless_rules")
            assert result is not None, "Required property 'stateless_rules' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.StatelessRuleProperty"]]], result)

        @builtins.property
        def custom_actions(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.CustomActionProperty"]]]]:
            '''Defines an array of individual custom action definitions that are available for use by the stateless rules in this ``StatelessRulesAndCustomActions`` specification.

            You name each custom action that you define, and then you can use it by name in your stateless rule ``RuleGroup.RuleDefinition`` ``Actions`` specification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrulesandcustomactions.html#cfn-networkfirewall-rulegroup-statelessrulesandcustomactions-customactions
            '''
            result = self._values.get("custom_actions")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRuleGroup.CustomActionProperty"]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatelessRulesAndCustomActionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroup.TCPFlagFieldProperty",
        jsii_struct_bases=[],
        name_mapping={"flags": "flags", "masks": "masks"},
    )
    class TCPFlagFieldProperty:
        def __init__(
            self,
            *,
            flags: typing.Sequence[builtins.str],
            masks: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''TCP flags and masks to inspect packets for. This is used in the ``RuleGroup.MatchAttributes`` specification.

            For example:

            ``"TCPFlags": [ { "Flags": [ "ECE", "SYN" ], "Masks": [ "SYN", "ECE" ] } ]``

            :param flags: Used in conjunction with the ``Masks`` setting to define the flags that must be set and flags that must not be set in order for the packet to match. This setting can only specify values that are also specified in the ``Masks`` setting. For the flags that are specified in the masks setting, the following must be true for the packet to match: - The ones that are set in this flags setting must be set in the packet. - The ones that are not set in this flags setting must also not be set in the packet.
            :param masks: The set of flags to consider in the inspection. To inspect all flags in the valid values list, leave this with no setting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-tcpflagfield.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_networkfirewall as networkfirewall
                
                t_cPFlag_field_property = networkfirewall.CfnRuleGroup.TCPFlagFieldProperty(
                    flags=["flags"],
                
                    # the properties below are optional
                    masks=["masks"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5fd749938d283873633c678fdcd8a6b5c126638fbe33eae58cd77cc7d6bf3c95)
                check_type(argname="argument flags", value=flags, expected_type=type_hints["flags"])
                check_type(argname="argument masks", value=masks, expected_type=type_hints["masks"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "flags": flags,
            }
            if masks is not None:
                self._values["masks"] = masks

        @builtins.property
        def flags(self) -> typing.List[builtins.str]:
            '''Used in conjunction with the ``Masks`` setting to define the flags that must be set and flags that must not be set in order for the packet to match.

            This setting can only specify values that are also specified in the ``Masks`` setting.

            For the flags that are specified in the masks setting, the following must be true for the packet to match:

            - The ones that are set in this flags setting must be set in the packet.
            - The ones that are not set in this flags setting must also not be set in the packet.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-tcpflagfield.html#cfn-networkfirewall-rulegroup-tcpflagfield-flags
            '''
            result = self._values.get("flags")
            assert result is not None, "Required property 'flags' is missing"
            return typing.cast(typing.List[builtins.str], result)

        @builtins.property
        def masks(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The set of flags to consider in the inspection.

            To inspect all flags in the valid values list, leave this with no setting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-tcpflagfield.html#cfn-networkfirewall-rulegroup-tcpflagfield-masks
            '''
            result = self._values.get("masks")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TCPFlagFieldProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-networkfirewall.CfnRuleGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "capacity": "capacity",
        "rule_group_name": "ruleGroupName",
        "type": "type",
        "description": "description",
        "rule_group": "ruleGroup",
        "tags": "tags",
    },
)
class CfnRuleGroupProps:
    def __init__(
        self,
        *,
        capacity: jsii.Number,
        rule_group_name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        rule_group: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.RuleGroupProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRuleGroup``.

        :param capacity: The maximum operating resources that this rule group can use. You can't change a rule group's capacity setting after you create the rule group. When you update a rule group, you are limited to this capacity. When you reference a rule group from a firewall policy, Network Firewall reserves this capacity for the rule group.
        :param rule_group_name: The descriptive name of the rule group. You can't change the name of a rule group after you create it.
        :param type: Indicates whether the rule group is stateless or stateful. If the rule group is stateless, it contains stateless rules. If it is stateful, it contains stateful rules.
        :param description: A description of the rule group.
        :param rule_group: An object that defines the rule group rules.
        :param tags: An array of key-value pairs to apply to this resource. For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_networkfirewall as networkfirewall
            
            cfn_rule_group_props = networkfirewall.CfnRuleGroupProps(
                capacity=123,
                rule_group_name="ruleGroupName",
                type="type",
            
                # the properties below are optional
                description="description",
                rule_group=networkfirewall.CfnRuleGroup.RuleGroupProperty(
                    rules_source=networkfirewall.CfnRuleGroup.RulesSourceProperty(
                        rules_source_list=networkfirewall.CfnRuleGroup.RulesSourceListProperty(
                            generated_rules_type="generatedRulesType",
                            targets=["targets"],
                            target_types=["targetTypes"]
                        ),
                        rules_string="rulesString",
                        stateful_rules=[networkfirewall.CfnRuleGroup.StatefulRuleProperty(
                            action="action",
                            header=networkfirewall.CfnRuleGroup.HeaderProperty(
                                destination="destination",
                                destination_port="destinationPort",
                                direction="direction",
                                protocol="protocol",
                                source="source",
                                source_port="sourcePort"
                            ),
                            rule_options=[networkfirewall.CfnRuleGroup.RuleOptionProperty(
                                keyword="keyword",
            
                                # the properties below are optional
                                settings=["settings"]
                            )]
                        )],
                        stateless_rules_and_custom_actions=networkfirewall.CfnRuleGroup.StatelessRulesAndCustomActionsProperty(
                            stateless_rules=[networkfirewall.CfnRuleGroup.StatelessRuleProperty(
                                priority=123,
                                rule_definition=networkfirewall.CfnRuleGroup.RuleDefinitionProperty(
                                    actions=["actions"],
                                    match_attributes=networkfirewall.CfnRuleGroup.MatchAttributesProperty(
                                        destination_ports=[networkfirewall.CfnRuleGroup.PortRangeProperty(
                                            from_port=123,
                                            to_port=123
                                        )],
                                        destinations=[networkfirewall.CfnRuleGroup.AddressProperty(
                                            address_definition="addressDefinition"
                                        )],
                                        protocols=[123],
                                        source_ports=[networkfirewall.CfnRuleGroup.PortRangeProperty(
                                            from_port=123,
                                            to_port=123
                                        )],
                                        sources=[networkfirewall.CfnRuleGroup.AddressProperty(
                                            address_definition="addressDefinition"
                                        )],
                                        tcp_flags=[networkfirewall.CfnRuleGroup.TCPFlagFieldProperty(
                                            flags=["flags"],
            
                                            # the properties below are optional
                                            masks=["masks"]
                                        )]
                                    )
                                )
                            )],
            
                            # the properties below are optional
                            custom_actions=[networkfirewall.CfnRuleGroup.CustomActionProperty(
                                action_definition=networkfirewall.CfnRuleGroup.ActionDefinitionProperty(
                                    publish_metric_action=networkfirewall.CfnRuleGroup.PublishMetricActionProperty(
                                        dimensions=[networkfirewall.CfnRuleGroup.DimensionProperty(
                                            value="value"
                                        )]
                                    )
                                ),
                                action_name="actionName"
                            )]
                        )
                    ),
            
                    # the properties below are optional
                    reference_sets=networkfirewall.CfnRuleGroup.ReferenceSetsProperty(
                        ip_set_references={
                            "ip_set_references_key": {
                                "reference_arn": "referenceArn"
                            }
                        }
                    ),
                    rule_variables=networkfirewall.CfnRuleGroup.RuleVariablesProperty(
                        ip_sets={
                            "ip_sets_key": {
                                "definition": ["definition"]
                            }
                        },
                        port_sets={
                            "port_sets_key": networkfirewall.CfnRuleGroup.PortSetProperty(
                                definition=["definition"]
                            )
                        }
                    ),
                    stateful_rule_options=networkfirewall.CfnRuleGroup.StatefulRuleOptionsProperty(
                        rule_order="ruleOrder"
                    )
                ),
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be8f0f860b8764fa4bc50995af13ad4a4a06aa04867ce65d537e003da5842e1d)
            check_type(argname="argument capacity", value=capacity, expected_type=type_hints["capacity"])
            check_type(argname="argument rule_group_name", value=rule_group_name, expected_type=type_hints["rule_group_name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument rule_group", value=rule_group, expected_type=type_hints["rule_group"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "capacity": capacity,
            "rule_group_name": rule_group_name,
            "type": type,
        }
        if description is not None:
            self._values["description"] = description
        if rule_group is not None:
            self._values["rule_group"] = rule_group
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def capacity(self) -> jsii.Number:
        '''The maximum operating resources that this rule group can use.

        You can't change a rule group's capacity setting after you create the rule group. When you update a rule group, you are limited to this capacity. When you reference a rule group from a firewall policy, Network Firewall reserves this capacity for the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-capacity
        '''
        result = self._values.get("capacity")
        assert result is not None, "Required property 'capacity' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def rule_group_name(self) -> builtins.str:
        '''The descriptive name of the rule group.

        You can't change the name of a rule group after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroupname
        '''
        result = self._values.get("rule_group_name")
        assert result is not None, "Required property 'rule_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Indicates whether the rule group is stateless or stateful.

        If the rule group is stateless, it contains
        stateless rules. If it is stateful, it contains stateful rules.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rule_group(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRuleGroup.RuleGroupProperty]]:
        '''An object that defines the rule group rules.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup
        '''
        result = self._values.get("rule_group")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRuleGroup.RuleGroupProperty]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnFirewall",
    "CfnFirewallPolicy",
    "CfnFirewallPolicyProps",
    "CfnFirewallProps",
    "CfnLoggingConfiguration",
    "CfnLoggingConfigurationProps",
    "CfnRuleGroup",
    "CfnRuleGroupProps",
]

publication.publish()

def _typecheckingstub__19d1d1eee1029ee159736360c524335747587f0f06999a2fe85acfdb0f97da6c(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    firewall_name: builtins.str,
    firewall_policy_arn: builtins.str,
    subnet_mappings: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnFirewall.SubnetMappingProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
    vpc_id: builtins.str,
    delete_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    firewall_policy_change_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    subnet_change_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59869aa0bb6cb97fdfebb8430ed49c0dd929451968db1070f7db79b00a647e69(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b58d5426c70f688b592df1cd1b4b386c5623585eb75d076ab4ac87bfda30205(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__270fafa0dd3c45e8305ece4b7d2580f9f2d9dabc51b155173d7d3cce8314fabc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d06ea77cc12b80c2243d61f1c6fd8d9a144ef47da68e8acddbcb9fca72a8ec41(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0784dbac3cb684531ab5e0f68e51ee4bb7997ca40d9b6ad52f6b488e1c98c660(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnFirewall.SubnetMappingProperty, _aws_cdk_core_f4b25747.IResolvable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f549b9972ef4d527dbcb28beea2a346fcee8adcee9bc7079806cb32744b9da19(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ae0b59abc26acde625ceee70fa3cdd0d5ff5b631ea712f67aea20cf2082c433(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf7634dca0aec6a62b59436b6ff00333298e3404f37eef3ef0bc7a3225632200(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97b4dfb5e46a42c6315101168e51b198161a393d126ecfee07b26cb98a5e805(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cad9ad5362c6ca517e24ac92741c48aaf518578649900b13a9ca4b6658626b0(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7599efdcdea45818b0009300a6f64aaa52b61f6b9cf3984a185f8db10c981d65(
    *,
    subnet_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b50ce469ced2a642ad4c361981694880624b599cc8abac970b7ee5b0bf63b011(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    firewall_policy: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFirewallPolicy.FirewallPolicyProperty, typing.Dict[builtins.str, typing.Any]]],
    firewall_policy_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93918d09ff74a9b97c3243bcbd856a48fcd724b357eabc34fbdf05bdfcba8117(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50c894ee14c2a382e5f121cac1190bef4af46dbe84bafa65ef5902e376ba497f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f7b6a772ab37dca4dd31b3de0b4dd025d0a7c4186c0bf04033e3a2a8df835de(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnFirewallPolicy.FirewallPolicyProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__756abcaf831c4294911d34c322c5175f7a47aa1a5d79763e55436ddc8a1d609c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__262499097d8e373436a55d05286c5de0c1b66bbcaf3fe7861ed2cfdbc5665de6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11547f1811f763d991008c49b2105f605a1e6d202145f1701a8043d9d43799d1(
    *,
    publish_metric_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFirewallPolicy.PublishMetricActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b9ce10ab0d6b6438ef8ea640cbe4ed46c49f9896fd22f401ba2879b26b25e11(
    *,
    action_definition: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFirewallPolicy.ActionDefinitionProperty, typing.Dict[builtins.str, typing.Any]]],
    action_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a1c6debb532cadac4392a092e05dcab35b9e445b2f53b7c3394ded2aac0a7b1(
    *,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0efae29543f839fb2f4b74d28d3e8bd2f76ce46c31cff67d4bcb435eac193d7e(
    *,
    stateless_default_actions: typing.Sequence[builtins.str],
    stateless_fragment_default_actions: typing.Sequence[builtins.str],
    stateful_default_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stateful_engine_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFirewallPolicy.StatefulEngineOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stateful_rule_group_references: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFirewallPolicy.StatefulRuleGroupReferenceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    stateless_custom_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFirewallPolicy.CustomActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    stateless_rule_group_references: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFirewallPolicy.StatelessRuleGroupReferenceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f8dee6a5e3ddc081940a60cdbba5126c0d9c8ecfad560b470a71b23ab60b6f(
    *,
    dimensions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFirewallPolicy.DimensionProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea2f5432221bdcc5b6fabcb38879b7ff807ec52e4123fc01e5d59556113a630(
    *,
    rule_order: typing.Optional[builtins.str] = None,
    stream_exception_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfa8ad1569623359c8ef26112c0e6543aead4d60a62f344875f1f853eff72d5a(
    *,
    action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa2d356e374a606507927fa1e79e01673325a1ca2611b60e756a13cafaee9594(
    *,
    resource_arn: builtins.str,
    override: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFirewallPolicy.StatefulRuleGroupOverrideProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    priority: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bb980e9a4423f160aa1057a7280ab44a1d401cbeba4e3deaefe784f9a94b65b(
    *,
    priority: jsii.Number,
    resource_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7cabcce3c29168bced4cffc4f4993707cebb8d88f7e93b1815f5206bdd6e2bfa(
    *,
    firewall_policy: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnFirewallPolicy.FirewallPolicyProperty, typing.Dict[builtins.str, typing.Any]]],
    firewall_policy_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a32c93a11a0b99fa163ad3694fa3a8b6eba91ee67b8312e65199caffb65739e1(
    *,
    firewall_name: builtins.str,
    firewall_policy_arn: builtins.str,
    subnet_mappings: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnFirewall.SubnetMappingProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
    vpc_id: builtins.str,
    delete_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    firewall_policy_change_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    subnet_change_protection: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328c6f8768a9a38ee9905a29aeefc0e96e426f719b062bf4b4f96a6861402fc6(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    firewall_arn: builtins.str,
    logging_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLoggingConfiguration.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    firewall_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__631baaaf383c322aa1a190eb585d070ef632969047928f26c37f36ba813a65f8(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d5fead774da4d88b73c332b964397d6961c4afaafe062caf5d3519c46ddd178(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67d675231d241a54cc0d6bc0a21335561d53c21bf6ce50b7491c4109ba056308(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da205a6d2f4d3dbca2ca6d68bd310872e4fe3c060c38384d357900e7dd870dbf(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnLoggingConfiguration.LoggingConfigurationProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b518275b3169c503d207df887486befbb188dad67eab8e3edceac0fbe75e6e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf57403e164680766143d1ceaee3fca20ba2cd4df58572ea0d55a73889ef1437(
    *,
    log_destination: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]],
    log_destination_type: builtins.str,
    log_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59b11c20b52bf275d1bce8e9d30b42195a2d4e42b98b229018eeeeb4f06b812d(
    *,
    log_destination_configs: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLoggingConfiguration.LogDestinationConfigProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f34101af25cb28e6793d92ca9946d43f82323a561b65e7f05de32322235ed50e(
    *,
    firewall_arn: builtins.str,
    logging_configuration: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnLoggingConfiguration.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]]],
    firewall_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2bed744c295734a9a31b12cdfa346e8e1a3faa7c1769cf2ae9d419c14f766bb(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    capacity: jsii.Number,
    rule_group_name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    rule_group: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.RuleGroupProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e9cfbbb9f560049c546c48ee14b258134c81fa07e078eff4bc8ce83f9ebcd71(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6d6407999ccd0ca7716cb84bebc040d294700858d002f62493ec63b90e805a6(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2163e04eacfa0b18ca7e0ac22f7c794c26eff7c9717a4423cde5a1b95cab5439(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eef3e13e88ed9b5c3b1b0f92c0c230b40549c9f23eb5fc5a4c3921d8e149bb4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__681ae21bef43ebe64a227fca78b5efbaab91b3dfe2a02d66a3cd17f7faff538d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f2b03115ff3fc828c883937c6eb6123daa7fee8c419643091ff0a4144b16023(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c275f2557feddfa95030136eb9095c9ad1ead606a07ab9a65bd18ee74ccd9d1(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRuleGroup.RuleGroupProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6372dd81c78c3500e1a4daff7629d3a1cc5b52770dedb29375245227e8246bc4(
    *,
    publish_metric_action: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.PublishMetricActionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e078ac8466a97701aba834401dcb7198d690a79691f9464fecb557d85e3d05(
    *,
    address_definition: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c730adebe9500c157c649f6e0172b2fa3b95baaae1da1502ba37132abc0fe2(
    *,
    action_definition: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.ActionDefinitionProperty, typing.Dict[builtins.str, typing.Any]]],
    action_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d17f0084c420cf17e184f0ea6bd9d55eb5ba57c9593d4f80927ab7c2ac130823(
    *,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f41645f51d939972848dc88c2c84fa11a33468a4f5a569c2d3c57a7de1238d6d(
    *,
    destination: builtins.str,
    destination_port: builtins.str,
    direction: builtins.str,
    protocol: builtins.str,
    source: builtins.str,
    source_port: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4f33b066cc14f1cc6c8679aab02ce640b84221a523cde9f3c7635f61d3ae066(
    *,
    definition: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__662b3cfba2f4d1f368fc454475f3e9b13fab670d101cf4b34f429a717c7c04f7(
    *,
    reference_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfca8d9a633e425515babc1b91dc0118449c0c4d43ae95cdd3c68c688a5526b6(
    *,
    destination_ports: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.PortRangeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    destinations: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.AddressProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    protocols: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[jsii.Number]]] = None,
    source_ports: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.PortRangeProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    sources: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.AddressProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    tcp_flags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.TCPFlagFieldProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a83182100058e2dc63b44857786bdfc9719f204dbc2d3480ff24661d4968a4a2(
    *,
    from_port: jsii.Number,
    to_port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__411ce5f7e2a84f8c6b7e30dc9dc68cfd28775fadff74f37f724e87f5f662c40f(
    *,
    definition: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__879ffb0bb9984ae218137d5110b0e7fa519e7be74f7c38725b3b376b1e1efbd5(
    *,
    dimensions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.DimensionProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9abebd8d84f9a8a9bab75307896e9ddc7e0aeed3f5c4f4370f5f538641675cdc(
    *,
    ip_set_references: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.IPSetReferenceProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43c19f099b082af7510e0d7df1fa00fbf7164c679af42b11277d118596c81d44(
    *,
    actions: typing.Sequence[builtins.str],
    match_attributes: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.MatchAttributesProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2af100bf042e6e4899857646cfd5c613ed122be76f69b4f12f4c7a32ba06c1a7(
    *,
    rules_source: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.RulesSourceProperty, typing.Dict[builtins.str, typing.Any]]],
    reference_sets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.ReferenceSetsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rule_variables: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    stateful_rule_options: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.StatefulRuleOptionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e59f27890737d73ab1365709d4946bb82d72498e645ec26af2adb967d671bf1c(
    *,
    keyword: builtins.str,
    settings: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e5a0766b0fab0549e421f523823541e0e2a813c3c425cbb5f23477773c04e1(
    *,
    ip_sets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.IPSetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    port_sets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.PortSetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd3667810dac8d7236225216210e341701118d222d35fc12db68c33227b053a(
    *,
    generated_rules_type: builtins.str,
    targets: typing.Sequence[builtins.str],
    target_types: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4c5e11af1b4c815b7fd6a4d48bd91a4c2b4ade3a07175d32fc1c252a2f5e3a9(
    *,
    rules_source_list: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.RulesSourceListProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    rules_string: typing.Optional[builtins.str] = None,
    stateful_rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.StatefulRuleProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    stateless_rules_and_custom_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.StatelessRulesAndCustomActionsProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8eb14b3c3d091145bbda5a1faccc8e5651d9f7213c1b9da465252d3a564924f1(
    *,
    rule_order: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b3ffd30e1527c1391554953822f4cd5033aa7f40a689fd5e0041be8a0814885(
    *,
    action: builtins.str,
    header: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.HeaderProperty, typing.Dict[builtins.str, typing.Any]]],
    rule_options: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.RuleOptionProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e0f1282bb53fa7742fa0f209cabcdfb9bc549df520661cbb81c20e8de19211c(
    *,
    priority: jsii.Number,
    rule_definition: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.RuleDefinitionProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfc4ee05340befc6bf8c9802b1fbff290e85f4a60b9ea9486b8921cd9e903d13(
    *,
    stateless_rules: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.StatelessRuleProperty, typing.Dict[builtins.str, typing.Any]]]]],
    custom_actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.CustomActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd749938d283873633c678fdcd8a6b5c126638fbe33eae58cd77cc7d6bf3c95(
    *,
    flags: typing.Sequence[builtins.str],
    masks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be8f0f860b8764fa4bc50995af13ad4a4a06aa04867ce65d537e003da5842e1d(
    *,
    capacity: jsii.Number,
    rule_group_name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    rule_group: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRuleGroup.RuleGroupProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
