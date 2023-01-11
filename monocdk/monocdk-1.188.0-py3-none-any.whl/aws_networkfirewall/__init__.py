'''
# AWS::NetworkFirewall Construct Library

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import monocdk as networkfirewall
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
class CfnFirewall(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_networkfirewall.CfnFirewall",
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
        from monocdk import aws_networkfirewall as networkfirewall
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        firewall_name: builtins.str,
        firewall_policy_arn: builtins.str,
        subnet_mappings: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnFirewall.SubnetMappingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        vpc_id: builtins.str,
        delete_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        firewall_policy_change_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        subnet_change_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5a22488e4c01b6b5fade41b1398022a78a3674b4c5c4f3b9c92e735b5502ecb)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a718365ef6e1fd2b274429f35544f343ec702399015d9c68f32ae8d24d17d47)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d74877286e28bb6d0e69fccc14e305be54536c26edf6c158e6b817abfefb71ec)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__69e9b5fab90f5dd9516357a3e43fdd279b5564c7dccfcf89ab1a0ed9c606259d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa9a51143758b1b2fc454d7a2d25a58e3f63e59faea9ef774f72d0c5f208b37b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallPolicyArn", value)

    @builtins.property
    @jsii.member(jsii_name="subnetMappings")
    def subnet_mappings(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewall.SubnetMappingProperty", _IResolvable_a771d0ef]]]:
        '''The public subnets that Network Firewall is using for the firewall.

        Each subnet must belong to a different Availability Zone.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-subnetmappings
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewall.SubnetMappingProperty", _IResolvable_a771d0ef]]], jsii.get(self, "subnetMappings"))

    @subnet_mappings.setter
    def subnet_mappings(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewall.SubnetMappingProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e20fb31a4db964e790ffb4b782dd32a5922c0c076898963c42d5c500579d421)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c52d80cebda5aa58e04b88f445af7053ce7ba44e78963a351700aaeb38d4de9a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value)

    @builtins.property
    @jsii.member(jsii_name="deleteProtection")
    def delete_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A flag indicating whether it is possible to delete the firewall.

        A setting of ``TRUE`` indicates that the firewall is protected against deletion. Use this setting to protect against accidentally deleting a firewall that is in use. When you create a firewall, the operation initializes this flag to ``TRUE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-deleteprotection
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "deleteProtection"))

    @delete_protection.setter
    def delete_protection(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__edb444907dfc24c0cd22de0c6d809f1afa6573e25e343d2912fd00ee5711cee1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__026a543db95167cfb7c92b6a5dcd3a8dd6d552d6a8adec454486a2ba17b6101a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyChangeProtection")
    def firewall_policy_change_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A setting indicating whether the firewall is protected against a change to the firewall policy association.

        Use this setting to protect against accidentally modifying the firewall policy for a firewall that is in use. When you create a firewall, the operation initializes this setting to ``TRUE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-firewallpolicychangeprotection
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "firewallPolicyChangeProtection"))

    @firewall_policy_change_protection.setter
    def firewall_policy_change_protection(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5efe82326c7e86c6cc8eae1981d6efe931e96778dfc7a662e3e33685011a446)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallPolicyChangeProtection", value)

    @builtins.property
    @jsii.member(jsii_name="subnetChangeProtection")
    def subnet_change_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A setting indicating whether the firewall is protected against changes to the subnet associations.

        Use this setting to protect against accidentally modifying the subnet associations for a firewall that is in use. When you create a firewall, the operation initializes this setting to ``TRUE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-subnetchangeprotection
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "subnetChangeProtection"))

    @subnet_change_protection.setter
    def subnet_change_protection(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b902d164604a830ff141412abbe14d57f69d9884417d7fccf1f104a09b44678d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetChangeProtection", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewall.SubnetMappingProperty",
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
                from monocdk import aws_networkfirewall as networkfirewall
                
                subnet_mapping_property = networkfirewall.CfnFirewall.SubnetMappingProperty(
                    subnet_id="subnetId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1eeb36e441597c5f0a5612959627e85d50460535ea9f4b0b804a479f40a733e7)
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


@jsii.implements(_IInspectable_82c04a63)
class CfnFirewallPolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy",
):
    '''A CloudFormation ``AWS::NetworkFirewall::FirewallPolicy``.

    Use the ``FirewallPolicy`` to define the stateless and stateful network traffic filtering behavior for your ``Firewall`` . You can use one firewall policy for multiple firewalls.

    :cloudformationResource: AWS::NetworkFirewall::FirewallPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_networkfirewall as networkfirewall
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        firewall_policy: typing.Union[typing.Union["CfnFirewallPolicy.FirewallPolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        firewall_policy_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e5cf81dc5b3c0c79cfd117daa614f09713c75f03d1009f2a0d4e63ffb345fb2)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0fc996265bc356580e65dcd9748d967b3c6d4baf5bff2cd2762a04a9d18386a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e5663e0a87e11ea378a7ea0bf9af8eba172e4f0138c841356fd59b51ec790b9b)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="firewallPolicy")
    def firewall_policy(
        self,
    ) -> typing.Union["CfnFirewallPolicy.FirewallPolicyProperty", _IResolvable_a771d0ef]:
        '''The traffic filtering behavior of a firewall policy, defined in a collection of stateless and stateful rule groups and other settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy
        '''
        return typing.cast(typing.Union["CfnFirewallPolicy.FirewallPolicyProperty", _IResolvable_a771d0ef], jsii.get(self, "firewallPolicy"))

    @firewall_policy.setter
    def firewall_policy(
        self,
        value: typing.Union["CfnFirewallPolicy.FirewallPolicyProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ec9bdaf3f5496c9723b7f8c6b4e7e0bc9b426848560c1cb18d44d41aad428d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__28f46abd426ac5ed8e396ae788317737a9b8eabde4b499a311274944fac646d8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bbb07b3a16e5a056528b0d4e7f6dc4999d3c20ffec865de7c61b69d3a46593e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.ActionDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"publish_metric_action": "publishMetricAction"},
    )
    class ActionDefinitionProperty:
        def __init__(
            self,
            *,
            publish_metric_action: typing.Optional[typing.Union[typing.Union["CfnFirewallPolicy.PublishMetricActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''A custom action to use in stateless rule actions settings.

            :param publish_metric_action: Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet. This setting defines a CloudWatch dimension value to be published. You can pair this custom action with any of the standard stateless rule actions. For example, you could pair this in a rule action with the standard action that forwards the packet for stateful inspection. Then, when a packet matches the rule, Network Firewall publishes metrics for the packet and forwards it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-actiondefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_networkfirewall as networkfirewall
                
                action_definition_property = networkfirewall.CfnFirewallPolicy.ActionDefinitionProperty(
                    publish_metric_action=networkfirewall.CfnFirewallPolicy.PublishMetricActionProperty(
                        dimensions=[networkfirewall.CfnFirewallPolicy.DimensionProperty(
                            value="value"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f0c017f9e7cf856a002f96fa20d25d38ab1785e65b51f6e43e92421defb7e801)
                check_type(argname="argument publish_metric_action", value=publish_metric_action, expected_type=type_hints["publish_metric_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if publish_metric_action is not None:
                self._values["publish_metric_action"] = publish_metric_action

        @builtins.property
        def publish_metric_action(
            self,
        ) -> typing.Optional[typing.Union["CfnFirewallPolicy.PublishMetricActionProperty", _IResolvable_a771d0ef]]:
            '''Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet.

            This setting defines a CloudWatch dimension value to be published.

            You can pair this custom action with any of the standard stateless rule actions. For example, you could pair this in a rule action with the standard action that forwards the packet for stateful inspection. Then, when a packet matches the rule, Network Firewall publishes metrics for the packet and forwards it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-actiondefinition.html#cfn-networkfirewall-firewallpolicy-actiondefinition-publishmetricaction
            '''
            result = self._values.get("publish_metric_action")
            return typing.cast(typing.Optional[typing.Union["CfnFirewallPolicy.PublishMetricActionProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.CustomActionProperty",
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
            action_definition: typing.Union[typing.Union["CfnFirewallPolicy.ActionDefinitionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
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
                from monocdk import aws_networkfirewall as networkfirewall
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__87d3d6959bc2139add1a2e760c70df3f4188d17e4cae4b12c932c9fb2deaaad3)
                check_type(argname="argument action_definition", value=action_definition, expected_type=type_hints["action_definition"])
                check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "action_definition": action_definition,
                "action_name": action_name,
            }

        @builtins.property
        def action_definition(
            self,
        ) -> typing.Union["CfnFirewallPolicy.ActionDefinitionProperty", _IResolvable_a771d0ef]:
            '''The custom action associated with the action name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-customaction.html#cfn-networkfirewall-firewallpolicy-customaction-actiondefinition
            '''
            result = self._values.get("action_definition")
            assert result is not None, "Required property 'action_definition' is missing"
            return typing.cast(typing.Union["CfnFirewallPolicy.ActionDefinitionProperty", _IResolvable_a771d0ef], result)

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
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.DimensionProperty",
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
                from monocdk import aws_networkfirewall as networkfirewall
                
                dimension_property = networkfirewall.CfnFirewallPolicy.DimensionProperty(
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__53d02ba4c9ee231acd4a7bf330b1c4c40d13a26480e8e8df2adef97df4bcb8cf)
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
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.FirewallPolicyProperty",
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
            stateful_engine_options: typing.Optional[typing.Union[typing.Union["CfnFirewallPolicy.StatefulEngineOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            stateful_rule_group_references: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnFirewallPolicy.StatefulRuleGroupReferenceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            stateless_custom_actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnFirewallPolicy.CustomActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            stateless_rule_group_references: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnFirewallPolicy.StatelessRuleGroupReferenceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
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
                from monocdk import aws_networkfirewall as networkfirewall
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__8340106462060bf77272cd0a679e97144c80f7e165c13ba45318a9506284399c)
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
        ) -> typing.Optional[typing.Union["CfnFirewallPolicy.StatefulEngineOptionsProperty", _IResolvable_a771d0ef]]:
            '''Additional options governing how Network Firewall handles stateful rules.

            The stateful rule groups that you use in your policy must have stateful rule options settings that are compatible with these settings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statefulengineoptions
            '''
            result = self._values.get("stateful_engine_options")
            return typing.cast(typing.Optional[typing.Union["CfnFirewallPolicy.StatefulEngineOptionsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def stateful_rule_group_references(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallPolicy.StatefulRuleGroupReferenceProperty", _IResolvable_a771d0ef]]]]:
            '''References to the stateful rule groups that are used in the policy.

            These define the inspection criteria in stateful rules.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statefulrulegroupreferences
            '''
            result = self._values.get("stateful_rule_group_references")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallPolicy.StatefulRuleGroupReferenceProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def stateless_custom_actions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallPolicy.CustomActionProperty", _IResolvable_a771d0ef]]]]:
            '''The custom action definitions that are available for use in the firewall policy's ``StatelessDefaultActions`` setting.

            You name each custom action that you define, and then you can use it by name in your default actions specifications.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statelesscustomactions
            '''
            result = self._values.get("stateless_custom_actions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallPolicy.CustomActionProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def stateless_rule_group_references(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallPolicy.StatelessRuleGroupReferenceProperty", _IResolvable_a771d0ef]]]]:
            '''References to the stateless rule groups that are used in the policy.

            These define the matching criteria in stateless rules.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy-statelessrulegroupreferences
            '''
            result = self._values.get("stateless_rule_group_references")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallPolicy.StatelessRuleGroupReferenceProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirewallPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.PublishMetricActionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimensions": "dimensions"},
    )
    class PublishMetricActionProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnFirewallPolicy.DimensionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        ) -> None:
            '''Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet.

            This setting defines a CloudWatch dimension value to be published.

            :param dimensions: ``CfnFirewallPolicy.PublishMetricActionProperty.Dimensions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-publishmetricaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_networkfirewall as networkfirewall
                
                publish_metric_action_property = networkfirewall.CfnFirewallPolicy.PublishMetricActionProperty(
                    dimensions=[networkfirewall.CfnFirewallPolicy.DimensionProperty(
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__052be66cc8181cc1639f90a5221eb25382dddf26b2edd5f236e879d091ea2420)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "dimensions": dimensions,
            }

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallPolicy.DimensionProperty", _IResolvable_a771d0ef]]]:
            '''``CfnFirewallPolicy.PublishMetricActionProperty.Dimensions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-publishmetricaction.html#cfn-networkfirewall-firewallpolicy-publishmetricaction-dimensions
            '''
            result = self._values.get("dimensions")
            assert result is not None, "Required property 'dimensions' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallPolicy.DimensionProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublishMetricActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.StatefulEngineOptionsProperty",
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
                from monocdk import aws_networkfirewall as networkfirewall
                
                stateful_engine_options_property = networkfirewall.CfnFirewallPolicy.StatefulEngineOptionsProperty(
                    rule_order="ruleOrder",
                    stream_exception_policy="streamExceptionPolicy"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7c78c0db88ca0621551e63ccc2ad00b4b8bc9bd84a828a98fc1b4db305204d9d)
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
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.StatefulRuleGroupOverrideProperty",
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
                from monocdk import aws_networkfirewall as networkfirewall
                
                stateful_rule_group_override_property = networkfirewall.CfnFirewallPolicy.StatefulRuleGroupOverrideProperty(
                    action="action"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__1792c044a8183899977c1c759b0dc4809733af4b515a87239cda2dbdd919aebd)
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
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.StatefulRuleGroupReferenceProperty",
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
            override: typing.Optional[typing.Union[typing.Union["CfnFirewallPolicy.StatefulRuleGroupOverrideProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_networkfirewall as networkfirewall
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__7d113bff3112ac3b16e2d039908c10d639ebf0d4f0cbca4fa605391b37140f02)
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
        ) -> typing.Optional[typing.Union["CfnFirewallPolicy.StatefulRuleGroupOverrideProperty", _IResolvable_a771d0ef]]:
            '''The action that allows the policy owner to override the behavior of the rule group within a policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-firewallpolicy-statefulrulegroupreference.html#cfn-networkfirewall-firewallpolicy-statefulrulegroupreference-override
            '''
            result = self._values.get("override")
            return typing.cast(typing.Optional[typing.Union["CfnFirewallPolicy.StatefulRuleGroupOverrideProperty", _IResolvable_a771d0ef]], result)

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
        jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicy.StatelessRuleGroupReferenceProperty",
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
                from monocdk import aws_networkfirewall as networkfirewall
                
                stateless_rule_group_reference_property = networkfirewall.CfnFirewallPolicy.StatelessRuleGroupReferenceProperty(
                    priority=123,
                    resource_arn="resourceArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2eeb3b63c924fca739287a5c61341c6548c17f155d48bf5a13eb73c39aa21407)
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
    jsii_type="monocdk.aws_networkfirewall.CfnFirewallPolicyProps",
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
        firewall_policy: typing.Union[typing.Union[CfnFirewallPolicy.FirewallPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
        firewall_policy_name: builtins.str,
        description: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_networkfirewall as networkfirewall
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__5ce4336ad7eadbfc713ba89ef6185365f6f76ec8c82d066f9feb597c1a91e695)
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
    ) -> typing.Union[CfnFirewallPolicy.FirewallPolicyProperty, _IResolvable_a771d0ef]:
        '''The traffic filtering behavior of a firewall policy, defined in a collection of stateless and stateful rule groups and other settings.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-firewallpolicy
        '''
        result = self._values.get("firewall_policy")
        assert result is not None, "Required property 'firewall_policy' is missing"
        return typing.cast(typing.Union[CfnFirewallPolicy.FirewallPolicyProperty, _IResolvable_a771d0ef], result)

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
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewallpolicy.html#cfn-networkfirewall-firewallpolicy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFirewallPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_networkfirewall.CfnFirewallProps",
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
        subnet_mappings: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFirewall.SubnetMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        vpc_id: builtins.str,
        delete_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        description: typing.Optional[builtins.str] = None,
        firewall_policy_change_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        subnet_change_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_networkfirewall as networkfirewall
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__e14d1bcf8aef5c042ad76c2672af34c8c8d3b1914e8c46c4b7c7a21c0322f090)
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
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFirewall.SubnetMappingProperty, _IResolvable_a771d0ef]]]:
        '''The public subnets that Network Firewall is using for the firewall.

        Each subnet must belong to a different Availability Zone.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-subnetmappings
        '''
        result = self._values.get("subnet_mappings")
        assert result is not None, "Required property 'subnet_mappings' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFirewall.SubnetMappingProperty, _IResolvable_a771d0ef]]], result)

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
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A flag indicating whether it is possible to delete the firewall.

        A setting of ``TRUE`` indicates that the firewall is protected against deletion. Use this setting to protect against accidentally deleting a firewall that is in use. When you create a firewall, the operation initializes this flag to ``TRUE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-deleteprotection
        '''
        result = self._values.get("delete_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

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
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A setting indicating whether the firewall is protected against a change to the firewall policy association.

        Use this setting to protect against accidentally modifying the firewall policy for a firewall that is in use. When you create a firewall, the operation initializes this setting to ``TRUE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-firewallpolicychangeprotection
        '''
        result = self._values.get("firewall_policy_change_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def subnet_change_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''A setting indicating whether the firewall is protected against changes to the subnet associations.

        Use this setting to protect against accidentally modifying the subnet associations for a firewall that is in use. When you create a firewall, the operation initializes this setting to ``TRUE`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-subnetchangeprotection
        '''
        result = self._values.get("subnet_change_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-firewall.html#cfn-networkfirewall-firewall-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFirewallProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnLoggingConfiguration(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_networkfirewall.CfnLoggingConfiguration",
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
        from monocdk import aws_networkfirewall as networkfirewall
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        firewall_arn: builtins.str,
        logging_configuration: typing.Union[typing.Union["CfnLoggingConfiguration.LoggingConfigurationProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
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
            type_hints = typing.get_type_hints(_typecheckingstub__4e572189805198c8c599ff0b949c501aece926b783946b760a214bd87e608ca1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnLoggingConfigurationProps(
            firewall_arn=firewall_arn,
            logging_configuration=logging_configuration,
            firewall_name=firewall_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c66e7a57ffde7b81ac81b5d5f626bd560920bf6e0173fcad26d858a3fbbd9c4c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fbba926e175fa1ef861a299cea9a09bdf9795c2646bf2ef660e3b7d3e767e4ab)
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
            type_hints = typing.get_type_hints(_typecheckingstub__525b7863f62db1ade26d04627bc175926fe4d76844a9fd200a6a91dae9779771)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallArn", value)

    @builtins.property
    @jsii.member(jsii_name="loggingConfiguration")
    def logging_configuration(
        self,
    ) -> typing.Union["CfnLoggingConfiguration.LoggingConfigurationProperty", _IResolvable_a771d0ef]:
        '''Defines how AWS Network Firewall performs logging for a ``Firewall`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-loggingconfiguration
        '''
        return typing.cast(typing.Union["CfnLoggingConfiguration.LoggingConfigurationProperty", _IResolvable_a771d0ef], jsii.get(self, "loggingConfiguration"))

    @logging_configuration.setter
    def logging_configuration(
        self,
        value: typing.Union["CfnLoggingConfiguration.LoggingConfigurationProperty", _IResolvable_a771d0ef],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e798b456052b8c2086351677c114e00b0942d94f1de9de37300042c024460d20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef8303cdaae819b067bd9e5ded8ff20f086a3df175087ad976959456564a256b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnLoggingConfiguration.LogDestinationConfigProperty",
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
            log_destination: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]],
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
                from monocdk import aws_networkfirewall as networkfirewall
                
                log_destination_config_property = networkfirewall.CfnLoggingConfiguration.LogDestinationConfigProperty(
                    log_destination={
                        "log_destination_key": "logDestination"
                    },
                    log_destination_type="logDestinationType",
                    log_type="logType"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5fad0a980a3ab04ab0824eb8d27178b187cbb8849bf318abdcbf141b7464841f)
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
        ) -> typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]]:
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
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]], result)

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
        jsii_type="monocdk.aws_networkfirewall.CfnLoggingConfiguration.LoggingConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_destination_configs": "logDestinationConfigs"},
    )
    class LoggingConfigurationProperty:
        def __init__(
            self,
            *,
            log_destination_configs: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnLoggingConfiguration.LogDestinationConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        ) -> None:
            '''Defines how AWS Network Firewall performs logging for a ``Firewall`` .

            :param log_destination_configs: Defines the logging destinations for the logs for a firewall. Network Firewall generates logs for stateful rule groups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-loggingconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_networkfirewall as networkfirewall
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__9024539f8288f951b649de8d18b2be532319092e5773573379d8e68f54d2e158)
                check_type(argname="argument log_destination_configs", value=log_destination_configs, expected_type=type_hints["log_destination_configs"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "log_destination_configs": log_destination_configs,
            }

        @builtins.property
        def log_destination_configs(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLoggingConfiguration.LogDestinationConfigProperty", _IResolvable_a771d0ef]]]:
            '''Defines the logging destinations for the logs for a firewall.

            Network Firewall generates logs for stateful rule groups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-loggingconfiguration-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-loggingconfiguration-logdestinationconfigs
            '''
            result = self._values.get("log_destination_configs")
            assert result is not None, "Required property 'log_destination_configs' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnLoggingConfiguration.LogDestinationConfigProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoggingConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_networkfirewall.CfnLoggingConfigurationProps",
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
        logging_configuration: typing.Union[typing.Union[CfnLoggingConfiguration.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
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
            from monocdk import aws_networkfirewall as networkfirewall
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__b86ec82b24a76909141b464905dc9c1cceece8775cde4cb1dfca29feccf04bfd)
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
    ) -> typing.Union[CfnLoggingConfiguration.LoggingConfigurationProperty, _IResolvable_a771d0ef]:
        '''Defines how AWS Network Firewall performs logging for a ``Firewall`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-loggingconfiguration.html#cfn-networkfirewall-loggingconfiguration-loggingconfiguration
        '''
        result = self._values.get("logging_configuration")
        assert result is not None, "Required property 'logging_configuration' is missing"
        return typing.cast(typing.Union[CfnLoggingConfiguration.LoggingConfigurationProperty, _IResolvable_a771d0ef], result)

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


@jsii.implements(_IInspectable_82c04a63)
class CfnRuleGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup",
):
    '''A CloudFormation ``AWS::NetworkFirewall::RuleGroup``.

    Use the ``RuleGroup`` to define a reusable collection of stateless or stateful network traffic filtering rules. You use rule groups in an ``FirewallPolicy`` to specify the filtering behavior of an ``Firewall`` .

    :cloudformationResource: AWS::NetworkFirewall::RuleGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_networkfirewall as networkfirewall
        
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
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        capacity: jsii.Number,
        rule_group_name: builtins.str,
        type: builtins.str,
        description: typing.Optional[builtins.str] = None,
        rule_group: typing.Optional[typing.Union[typing.Union["CfnRuleGroup.RuleGroupProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__983ddd00cbc6193f212da53ba594e872a8bd378850163c7502d8bbb179c1a0d4)
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
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42bb558ba1abce8970d4ddd52590a3f607fb40fbbf1081e4e704717e618cf2ba)
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
            type_hints = typing.get_type_hints(_typecheckingstub__874114f82bf805fa2503ca54b18b7c746c000d2971b534d541ee8790c865b73b)
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
    def tags(self) -> _TagManager_0b7ab120:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__944cc27004f5f6e87349c201195bbfa14ed555a8c2b80e0d10c8afb771492a3d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a8a7c922dcdd1a8f481bbdaceea9919e32d99023b98646b689d222c41ec70a2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1bbfb8f405a34a90e601801aab6e1f6d2559ce27bbe06465dd14786159daee94)
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
            type_hints = typing.get_type_hints(_typecheckingstub__720d692516e3bdedd057d2e65252900e618c65d648b49c48564cf38a51a9b8a2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="ruleGroup")
    def rule_group(
        self,
    ) -> typing.Optional[typing.Union["CfnRuleGroup.RuleGroupProperty", _IResolvable_a771d0ef]]:
        '''An object that defines the rule group rules.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup
        '''
        return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.RuleGroupProperty", _IResolvable_a771d0ef]], jsii.get(self, "ruleGroup"))

    @rule_group.setter
    def rule_group(
        self,
        value: typing.Optional[typing.Union["CfnRuleGroup.RuleGroupProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__927b7a010d209242cb9bf5ae1d58c5b1266e00003f183311f4c241a1cbc56d5a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleGroup", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.ActionDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"publish_metric_action": "publishMetricAction"},
    )
    class ActionDefinitionProperty:
        def __init__(
            self,
            *,
            publish_metric_action: typing.Optional[typing.Union[typing.Union["CfnRuleGroup.PublishMetricActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''A custom action to use in stateless rule actions settings.

            :param publish_metric_action: Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet. This setting defines a CloudWatch dimension value to be published. You can pair this custom action with any of the standard stateless rule actions. For example, you could pair this in a rule action with the standard action that forwards the packet for stateful inspection. Then, when a packet matches the rule, Network Firewall publishes metrics for the packet and forwards it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-actiondefinition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_networkfirewall as networkfirewall
                
                action_definition_property = networkfirewall.CfnRuleGroup.ActionDefinitionProperty(
                    publish_metric_action=networkfirewall.CfnRuleGroup.PublishMetricActionProperty(
                        dimensions=[networkfirewall.CfnRuleGroup.DimensionProperty(
                            value="value"
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__57a61ec8df6b02ce17665ab7c72d51beb1af279b08cf757008923d8de63f5121)
                check_type(argname="argument publish_metric_action", value=publish_metric_action, expected_type=type_hints["publish_metric_action"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if publish_metric_action is not None:
                self._values["publish_metric_action"] = publish_metric_action

        @builtins.property
        def publish_metric_action(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.PublishMetricActionProperty", _IResolvable_a771d0ef]]:
            '''Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet.

            This setting defines a CloudWatch dimension value to be published.

            You can pair this custom action with any of the standard stateless rule actions. For example, you could pair this in a rule action with the standard action that forwards the packet for stateful inspection. Then, when a packet matches the rule, Network Firewall publishes metrics for the packet and forwards it.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-actiondefinition.html#cfn-networkfirewall-rulegroup-actiondefinition-publishmetricaction
            '''
            result = self._values.get("publish_metric_action")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.PublishMetricActionProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.AddressProperty",
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
                from monocdk import aws_networkfirewall as networkfirewall
                
                address_property = networkfirewall.CfnRuleGroup.AddressProperty(
                    address_definition="addressDefinition"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bfa7eb306ac4e8737176a63ef0efc3f1ae0f9c0abc078a55d94b47a807b6c372)
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
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.CustomActionProperty",
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
            action_definition: typing.Union[typing.Union["CfnRuleGroup.ActionDefinitionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
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
                from monocdk import aws_networkfirewall as networkfirewall
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__c66d63a97717f01292acaeb21ebc21fa2ed05d7d54b60793e4c0b0b05879dc23)
                check_type(argname="argument action_definition", value=action_definition, expected_type=type_hints["action_definition"])
                check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "action_definition": action_definition,
                "action_name": action_name,
            }

        @builtins.property
        def action_definition(
            self,
        ) -> typing.Union["CfnRuleGroup.ActionDefinitionProperty", _IResolvable_a771d0ef]:
            '''The custom action associated with the action name.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-customaction.html#cfn-networkfirewall-rulegroup-customaction-actiondefinition
            '''
            result = self._values.get("action_definition")
            assert result is not None, "Required property 'action_definition' is missing"
            return typing.cast(typing.Union["CfnRuleGroup.ActionDefinitionProperty", _IResolvable_a771d0ef], result)

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
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.DimensionProperty",
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
                from monocdk import aws_networkfirewall as networkfirewall
                
                dimension_property = networkfirewall.CfnRuleGroup.DimensionProperty(
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2e25770eb2f264d7e1a1a272324545eb43d22857c168fe7f0c61714a037afdc9)
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
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.HeaderProperty",
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
                from monocdk import aws_networkfirewall as networkfirewall
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__9291f0d336e789862d1b21fa57da829eeeb686c7511d88b16b7b9c061a15dc54)
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
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.IPSetProperty",
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
                from monocdk import aws_networkfirewall as networkfirewall
                
                i_pSet_property = {
                    "definition": ["definition"]
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__455575987c18e7759807d2ebb4076371230813c651be3ff558735eb457c9855d)
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
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.IPSetReferenceProperty",
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
                from monocdk import aws_networkfirewall as networkfirewall
                
                i_pSet_reference_property = {
                    "reference_arn": "referenceArn"
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bcfa6c3068c864391b1853461edef15e06c23bdafa3c810609ab64bd0e2d6d08)
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
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.MatchAttributesProperty",
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
            destination_ports: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRuleGroup.PortRangeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            destinations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRuleGroup.AddressProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            protocols: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[jsii.Number]]] = None,
            source_ports: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRuleGroup.PortRangeProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            sources: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRuleGroup.AddressProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            tcp_flags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRuleGroup.TCPFlagFieldProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
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
                from monocdk import aws_networkfirewall as networkfirewall
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__048acb95a5f6d246c909fb03611d1591f6eb7b24a42befaa072404a0204272f1)
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
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.PortRangeProperty", _IResolvable_a771d0ef]]]]:
            '''The destination ports to inspect for.

            If not specified, this matches with any destination port. This setting is only used for protocols 6 (TCP) and 17 (UDP).

            You can specify individual ports, for example ``1994`` and you can specify port ranges, for example ``1990:1994`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-destinationports
            '''
            result = self._values.get("destination_ports")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.PortRangeProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def destinations(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.AddressProperty", _IResolvable_a771d0ef]]]]:
            '''The destination IP addresses and address ranges to inspect for, in CIDR notation.

            If not specified, this matches with any destination address.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-destinations
            '''
            result = self._values.get("destinations")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.AddressProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def protocols(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[jsii.Number]]]:
            '''The protocols to inspect for, specified using each protocol's assigned internet protocol number (IANA).

            If not specified, this matches with any protocol.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-protocols
            '''
            result = self._values.get("protocols")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[jsii.Number]]], result)

        @builtins.property
        def source_ports(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.PortRangeProperty", _IResolvable_a771d0ef]]]]:
            '''The source ports to inspect for.

            If not specified, this matches with any source port. This setting is only used for protocols 6 (TCP) and 17 (UDP).

            You can specify individual ports, for example ``1994`` and you can specify port ranges, for example ``1990:1994`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-sourceports
            '''
            result = self._values.get("source_ports")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.PortRangeProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def sources(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.AddressProperty", _IResolvable_a771d0ef]]]]:
            '''The source IP addresses and address ranges to inspect for, in CIDR notation.

            If not specified, this matches with any source address.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-sources
            '''
            result = self._values.get("sources")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.AddressProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def tcp_flags(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TCPFlagFieldProperty", _IResolvable_a771d0ef]]]]:
            '''The TCP flags and masks to inspect for.

            If not specified, this matches with any settings. This setting is only used for protocol 6 (TCP).

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-matchattributes.html#cfn-networkfirewall-rulegroup-matchattributes-tcpflags
            '''
            result = self._values.get("tcp_flags")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.TCPFlagFieldProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatchAttributesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.PortRangeProperty",
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
                from monocdk import aws_networkfirewall as networkfirewall
                
                port_range_property = networkfirewall.CfnRuleGroup.PortRangeProperty(
                    from_port=123,
                    to_port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c53637ab6bc55106a61a28687b8782a2d46a8d1941d17ac691c1d9136d84b19c)
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
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.PortSetProperty",
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
                from monocdk import aws_networkfirewall as networkfirewall
                
                port_set_property = networkfirewall.CfnRuleGroup.PortSetProperty(
                    definition=["definition"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__953a1c2dbe78764d91ac1ba1885334c2cd851b4317dd08f929aea348425461b6)
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
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.PublishMetricActionProperty",
        jsii_struct_bases=[],
        name_mapping={"dimensions": "dimensions"},
    )
    class PublishMetricActionProperty:
        def __init__(
            self,
            *,
            dimensions: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRuleGroup.DimensionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        ) -> None:
            '''Stateless inspection criteria that publishes the specified metrics to Amazon CloudWatch for the matching packet.

            This setting defines a CloudWatch dimension value to be published.

            :param dimensions: ``CfnRuleGroup.PublishMetricActionProperty.Dimensions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-publishmetricaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_networkfirewall as networkfirewall
                
                publish_metric_action_property = networkfirewall.CfnRuleGroup.PublishMetricActionProperty(
                    dimensions=[networkfirewall.CfnRuleGroup.DimensionProperty(
                        value="value"
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9973571f9acb159728bd56d9c1e9b7839352de51bb546f5281abf952b0aeebfe)
                check_type(argname="argument dimensions", value=dimensions, expected_type=type_hints["dimensions"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "dimensions": dimensions,
            }

        @builtins.property
        def dimensions(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.DimensionProperty", _IResolvable_a771d0ef]]]:
            '''``CfnRuleGroup.PublishMetricActionProperty.Dimensions``.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-publishmetricaction.html#cfn-networkfirewall-rulegroup-publishmetricaction-dimensions
            '''
            result = self._values.get("dimensions")
            assert result is not None, "Required property 'dimensions' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.DimensionProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PublishMetricActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.ReferenceSetsProperty",
        jsii_struct_bases=[],
        name_mapping={"ip_set_references": "ipSetReferences"},
    )
    class ReferenceSetsProperty:
        def __init__(
            self,
            *,
            ip_set_references: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnRuleGroup.IPSetReferenceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''Configures the ``ReferenceSets`` for a stateful rule group.

            For more information, see the `Using IP set references in Suricata compatible rule groups <https://docs.aws.amazon.com/network-firewall/latest/developerguide/rule-groups-ip-set-references.html>`_ in the *Network Firewall User Guide* .

            :param ip_set_references: The IP set references to use in the stateful rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-referencesets.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_networkfirewall as networkfirewall
                
                reference_sets_property = networkfirewall.CfnRuleGroup.ReferenceSetsProperty(
                    ip_set_references={
                        "ip_set_references_key": {
                            "reference_arn": "referenceArn"
                        }
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ee4f19b32f3c7d602be0d28747b4103323664dd794da9b9657cb08a053f4edf3)
                check_type(argname="argument ip_set_references", value=ip_set_references, expected_type=type_hints["ip_set_references"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if ip_set_references is not None:
                self._values["ip_set_references"] = ip_set_references

        @builtins.property
        def ip_set_references(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnRuleGroup.IPSetReferenceProperty", _IResolvable_a771d0ef]]]]:
            '''The IP set references to use in the stateful rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-referencesets.html#cfn-networkfirewall-rulegroup-referencesets-ipsetreferences
            '''
            result = self._values.get("ip_set_references")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnRuleGroup.IPSetReferenceProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ReferenceSetsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.RuleDefinitionProperty",
        jsii_struct_bases=[],
        name_mapping={"actions": "actions", "match_attributes": "matchAttributes"},
    )
    class RuleDefinitionProperty:
        def __init__(
            self,
            *,
            actions: typing.Sequence[builtins.str],
            match_attributes: typing.Union[typing.Union["CfnRuleGroup.MatchAttributesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
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
                from monocdk import aws_networkfirewall as networkfirewall
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__22c7f9dab75a20e73b108b1af44fd9d79a80a014fe4068bce1a3ab407dc27fcf)
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
        ) -> typing.Union["CfnRuleGroup.MatchAttributesProperty", _IResolvable_a771d0ef]:
            '''Criteria for Network Firewall to use to inspect an individual packet in stateless rule inspection.

            Each match attributes set can include one or more items such as IP address, CIDR range, port number, protocol, and TCP flags.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-ruledefinition.html#cfn-networkfirewall-rulegroup-ruledefinition-matchattributes
            '''
            result = self._values.get("match_attributes")
            assert result is not None, "Required property 'match_attributes' is missing"
            return typing.cast(typing.Union["CfnRuleGroup.MatchAttributesProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleDefinitionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.RuleGroupProperty",
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
            rules_source: typing.Union[typing.Union["CfnRuleGroup.RulesSourceProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            reference_sets: typing.Optional[typing.Union[typing.Union["CfnRuleGroup.ReferenceSetsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            rule_variables: typing.Optional[typing.Union[typing.Union["CfnRuleGroup.RuleVariablesProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            stateful_rule_options: typing.Optional[typing.Union[typing.Union["CfnRuleGroup.StatefulRuleOptionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_networkfirewall as networkfirewall
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__459f40129bea183e20ed7540e7155a804f8dbab704a170831290bbae46b0a973)
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
        ) -> typing.Union["CfnRuleGroup.RulesSourceProperty", _IResolvable_a771d0ef]:
            '''The stateful rules or stateless rules for the rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup-rulessource
            '''
            result = self._values.get("rules_source")
            assert result is not None, "Required property 'rules_source' is missing"
            return typing.cast(typing.Union["CfnRuleGroup.RulesSourceProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def reference_sets(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.ReferenceSetsProperty", _IResolvable_a771d0ef]]:
            '''The reference sets for the stateful rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup-referencesets
            '''
            result = self._values.get("reference_sets")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.ReferenceSetsProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def rule_variables(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.RuleVariablesProperty", _IResolvable_a771d0ef]]:
            '''Settings that are available for use in the rules in the rule group.

            You can only use these for stateful rule groups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup-rulevariables
            '''
            result = self._values.get("rule_variables")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.RuleVariablesProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def stateful_rule_options(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.StatefulRuleOptionsProperty", _IResolvable_a771d0ef]]:
            '''Additional options governing how Network Firewall handles stateful rules.

            The policies where you use your stateful rule group must have stateful rule options settings that are compatible with these settings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup-statefulruleoptions
            '''
            result = self._values.get("stateful_rule_options")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.StatefulRuleOptionsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.RuleOptionProperty",
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
                from monocdk import aws_networkfirewall as networkfirewall
                
                rule_option_property = networkfirewall.CfnRuleGroup.RuleOptionProperty(
                    keyword="keyword",
                
                    # the properties below are optional
                    settings=["settings"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__c92f4b353b5d21e869cffb30f0e4851e88a5337cba66d95afe9f2119bdd3f9b1)
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
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.RuleVariablesProperty",
        jsii_struct_bases=[],
        name_mapping={"ip_sets": "ipSets", "port_sets": "portSets"},
    )
    class RuleVariablesProperty:
        def __init__(
            self,
            *,
            ip_sets: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnRuleGroup.IPSetProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            port_sets: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union["CfnRuleGroup.PortSetProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        ) -> None:
            '''Settings that are available for use in the rules in the ``RuleGroup`` where this is defined.

            :param ip_sets: A list of IP addresses and address ranges, in CIDR notation.
            :param port_sets: A list of port ranges.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulevariables.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_networkfirewall as networkfirewall
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__d59ef28a39e53b26fe7231efdb462a0e3451f72a3deb30a34bdc922ea424af9f)
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
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnRuleGroup.IPSetProperty", _IResolvable_a771d0ef]]]]:
            '''A list of IP addresses and address ranges, in CIDR notation.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulevariables.html#cfn-networkfirewall-rulegroup-rulevariables-ipsets
            '''
            result = self._values.get("ip_sets")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnRuleGroup.IPSetProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def port_sets(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnRuleGroup.PortSetProperty", _IResolvable_a771d0ef]]]]:
            '''A list of port ranges.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulevariables.html#cfn-networkfirewall-rulegroup-rulevariables-portsets
            '''
            result = self._values.get("port_sets")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union["CfnRuleGroup.PortSetProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RuleVariablesProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.RulesSourceListProperty",
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
                from monocdk import aws_networkfirewall as networkfirewall
                
                rules_source_list_property = networkfirewall.CfnRuleGroup.RulesSourceListProperty(
                    generated_rules_type="generatedRulesType",
                    targets=["targets"],
                    target_types=["targetTypes"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__60fa924e28f618b9ccf9e51f519835b16d9d536e9609354eccd5a13d327ebb92)
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
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.RulesSourceProperty",
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
            rules_source_list: typing.Optional[typing.Union[typing.Union["CfnRuleGroup.RulesSourceListProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            rules_string: typing.Optional[builtins.str] = None,
            stateful_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRuleGroup.StatefulRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            stateless_rules_and_custom_actions: typing.Optional[typing.Union[typing.Union["CfnRuleGroup.StatelessRulesAndCustomActionsProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
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
                from monocdk import aws_networkfirewall as networkfirewall
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__3943f68e627f69b2a88a3b02dadd23b899188912bb3cdc30cbc57632aec6908b)
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
        ) -> typing.Optional[typing.Union["CfnRuleGroup.RulesSourceListProperty", _IResolvable_a771d0ef]]:
            '''Stateful inspection criteria for a domain list rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html#cfn-networkfirewall-rulegroup-rulessource-rulessourcelist
            '''
            result = self._values.get("rules_source_list")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.RulesSourceListProperty", _IResolvable_a771d0ef]], result)

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
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatefulRuleProperty", _IResolvable_a771d0ef]]]]:
            '''An array of individual stateful rules inspection criteria to be used together in a stateful rule group.

            Use this option to specify simple Suricata rules with protocol, source and destination, ports, direction, and rule options. For information about the Suricata ``Rules`` format, see `Rules Format <https://docs.aws.amazon.com/https://suricata.readthedocs.io/rules/intro.html#>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html#cfn-networkfirewall-rulegroup-rulessource-statefulrules
            '''
            result = self._values.get("stateful_rules")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatefulRuleProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def stateless_rules_and_custom_actions(
            self,
        ) -> typing.Optional[typing.Union["CfnRuleGroup.StatelessRulesAndCustomActionsProperty", _IResolvable_a771d0ef]]:
            '''Stateless inspection criteria to be used in a stateless rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-rulessource.html#cfn-networkfirewall-rulegroup-rulessource-statelessrulesandcustomactions
            '''
            result = self._values.get("stateless_rules_and_custom_actions")
            return typing.cast(typing.Optional[typing.Union["CfnRuleGroup.StatelessRulesAndCustomActionsProperty", _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "RulesSourceProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.StatefulRuleOptionsProperty",
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
                from monocdk import aws_networkfirewall as networkfirewall
                
                stateful_rule_options_property = networkfirewall.CfnRuleGroup.StatefulRuleOptionsProperty(
                    rule_order="ruleOrder"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ce2f0cfbdf85aea8b7d8c41c74061818229fcdbae95b2e60cdd4f17c5da9b807)
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
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.StatefulRuleProperty",
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
            header: typing.Union[typing.Union["CfnRuleGroup.HeaderProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
            rule_options: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRuleGroup.RuleOptionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
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
                from monocdk import aws_networkfirewall as networkfirewall
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__6f9813846b53a1e37323a376971bdafc878b968e231d3e66db9c71fe3cd14274)
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
        ) -> typing.Union["CfnRuleGroup.HeaderProperty", _IResolvable_a771d0ef]:
            '''The stateful inspection criteria for this rule, used to inspect traffic flows.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulrule.html#cfn-networkfirewall-rulegroup-statefulrule-header
            '''
            result = self._values.get("header")
            assert result is not None, "Required property 'header' is missing"
            return typing.cast(typing.Union["CfnRuleGroup.HeaderProperty", _IResolvable_a771d0ef], result)

        @builtins.property
        def rule_options(
            self,
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.RuleOptionProperty", _IResolvable_a771d0ef]]]:
            '''Additional settings for a stateful rule, provided as keywords and settings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statefulrule.html#cfn-networkfirewall-rulegroup-statefulrule-ruleoptions
            '''
            result = self._values.get("rule_options")
            assert result is not None, "Required property 'rule_options' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.RuleOptionProperty", _IResolvable_a771d0ef]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatefulRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.StatelessRuleProperty",
        jsii_struct_bases=[],
        name_mapping={"priority": "priority", "rule_definition": "ruleDefinition"},
    )
    class StatelessRuleProperty:
        def __init__(
            self,
            *,
            priority: jsii.Number,
            rule_definition: typing.Union[typing.Union["CfnRuleGroup.RuleDefinitionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
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
                from monocdk import aws_networkfirewall as networkfirewall
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__6d12bec9e2947d23e5d3c82f547eacd5b7e4e85e85fb3351591f9ae134eb0192)
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
        ) -> typing.Union["CfnRuleGroup.RuleDefinitionProperty", _IResolvable_a771d0ef]:
            '''Defines the stateless 5-tuple packet inspection criteria and the action to take on a packet that matches the criteria.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrule.html#cfn-networkfirewall-rulegroup-statelessrule-ruledefinition
            '''
            result = self._values.get("rule_definition")
            assert result is not None, "Required property 'rule_definition' is missing"
            return typing.cast(typing.Union["CfnRuleGroup.RuleDefinitionProperty", _IResolvable_a771d0ef], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatelessRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.StatelessRulesAndCustomActionsProperty",
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
            stateless_rules: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRuleGroup.StatelessRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
            custom_actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRuleGroup.CustomActionProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
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
                from monocdk import aws_networkfirewall as networkfirewall
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__9cad60ff3c5504650174283859bcbac1132ad2ab1488edf1d944cf7b83554233)
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
        ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatelessRuleProperty", _IResolvable_a771d0ef]]]:
            '''Defines the set of stateless rules for use in a stateless rule group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrulesandcustomactions.html#cfn-networkfirewall-rulegroup-statelessrulesandcustomactions-statelessrules
            '''
            result = self._values.get("stateless_rules")
            assert result is not None, "Required property 'stateless_rules' is missing"
            return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.StatelessRuleProperty", _IResolvable_a771d0ef]]], result)

        @builtins.property
        def custom_actions(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.CustomActionProperty", _IResolvable_a771d0ef]]]]:
            '''Defines an array of individual custom action definitions that are available for use by the stateless rules in this ``StatelessRulesAndCustomActions`` specification.

            You name each custom action that you define, and then you can use it by name in your stateless rule ``RuleGroup.RuleDefinition`` ``Actions`` specification.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-networkfirewall-rulegroup-statelessrulesandcustomactions.html#cfn-networkfirewall-rulegroup-statelessrulesandcustomactions-customactions
            '''
            result = self._values.get("custom_actions")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRuleGroup.CustomActionProperty", _IResolvable_a771d0ef]]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "StatelessRulesAndCustomActionsProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_networkfirewall.CfnRuleGroup.TCPFlagFieldProperty",
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
                from monocdk import aws_networkfirewall as networkfirewall
                
                t_cPFlag_field_property = networkfirewall.CfnRuleGroup.TCPFlagFieldProperty(
                    flags=["flags"],
                
                    # the properties below are optional
                    masks=["masks"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__2d02937fbc62a87d6b051b94e68696a4659cc3fe6babf5262854818d6a0f6b71)
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
    jsii_type="monocdk.aws_networkfirewall.CfnRuleGroupProps",
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
        rule_group: typing.Optional[typing.Union[typing.Union[CfnRuleGroup.RuleGroupProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            from monocdk import aws_networkfirewall as networkfirewall
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__ce0205187b645d6fa1463e1dceac1435e629c188ab96298d071064dec6198a2a)
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
    ) -> typing.Optional[typing.Union[CfnRuleGroup.RuleGroupProperty, _IResolvable_a771d0ef]]:
        '''An object that defines the rule group rules.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-rulegroup
        '''
        result = self._values.get("rule_group")
        return typing.cast(typing.Optional[typing.Union[CfnRuleGroup.RuleGroupProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''An array of key-value pairs to apply to this resource.

        For more information, see `Tag <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-resource-tags.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-networkfirewall-rulegroup.html#cfn-networkfirewall-rulegroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

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

def _typecheckingstub__a5a22488e4c01b6b5fade41b1398022a78a3674b4c5c4f3b9c92e735b5502ecb(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    firewall_name: builtins.str,
    firewall_policy_arn: builtins.str,
    subnet_mappings: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFirewall.SubnetMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    vpc_id: builtins.str,
    delete_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    firewall_policy_change_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    subnet_change_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a718365ef6e1fd2b274429f35544f343ec702399015d9c68f32ae8d24d17d47(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d74877286e28bb6d0e69fccc14e305be54536c26edf6c158e6b817abfefb71ec(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69e9b5fab90f5dd9516357a3e43fdd279b5564c7dccfcf89ab1a0ed9c606259d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9a51143758b1b2fc454d7a2d25a58e3f63e59faea9ef774f72d0c5f208b37b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e20fb31a4db964e790ffb4b782dd32a5922c0c076898963c42d5c500579d421(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFirewall.SubnetMappingProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c52d80cebda5aa58e04b88f445af7053ce7ba44e78963a351700aaeb38d4de9a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__edb444907dfc24c0cd22de0c6d809f1afa6573e25e343d2912fd00ee5711cee1(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__026a543db95167cfb7c92b6a5dcd3a8dd6d552d6a8adec454486a2ba17b6101a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5efe82326c7e86c6cc8eae1981d6efe931e96778dfc7a662e3e33685011a446(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b902d164604a830ff141412abbe14d57f69d9884417d7fccf1f104a09b44678d(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eeb36e441597c5f0a5612959627e85d50460535ea9f4b0b804a479f40a733e7(
    *,
    subnet_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e5cf81dc5b3c0c79cfd117daa614f09713c75f03d1009f2a0d4e63ffb345fb2(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    firewall_policy: typing.Union[typing.Union[CfnFirewallPolicy.FirewallPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    firewall_policy_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0fc996265bc356580e65dcd9748d967b3c6d4baf5bff2cd2762a04a9d18386a(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5663e0a87e11ea378a7ea0bf9af8eba172e4f0138c841356fd59b51ec790b9b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ec9bdaf3f5496c9723b7f8c6b4e7e0bc9b426848560c1cb18d44d41aad428d1(
    value: typing.Union[CfnFirewallPolicy.FirewallPolicyProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28f46abd426ac5ed8e396ae788317737a9b8eabde4b499a311274944fac646d8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bbb07b3a16e5a056528b0d4e7f6dc4999d3c20ffec865de7c61b69d3a46593e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0c017f9e7cf856a002f96fa20d25d38ab1785e65b51f6e43e92421defb7e801(
    *,
    publish_metric_action: typing.Optional[typing.Union[typing.Union[CfnFirewallPolicy.PublishMetricActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87d3d6959bc2139add1a2e760c70df3f4188d17e4cae4b12c932c9fb2deaaad3(
    *,
    action_definition: typing.Union[typing.Union[CfnFirewallPolicy.ActionDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    action_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d02ba4c9ee231acd4a7bf330b1c4c40d13a26480e8e8df2adef97df4bcb8cf(
    *,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8340106462060bf77272cd0a679e97144c80f7e165c13ba45318a9506284399c(
    *,
    stateless_default_actions: typing.Sequence[builtins.str],
    stateless_fragment_default_actions: typing.Sequence[builtins.str],
    stateful_default_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stateful_engine_options: typing.Optional[typing.Union[typing.Union[CfnFirewallPolicy.StatefulEngineOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    stateful_rule_group_references: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFirewallPolicy.StatefulRuleGroupReferenceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    stateless_custom_actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFirewallPolicy.CustomActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    stateless_rule_group_references: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFirewallPolicy.StatelessRuleGroupReferenceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__052be66cc8181cc1639f90a5221eb25382dddf26b2edd5f236e879d091ea2420(
    *,
    dimensions: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFirewallPolicy.DimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c78c0db88ca0621551e63ccc2ad00b4b8bc9bd84a828a98fc1b4db305204d9d(
    *,
    rule_order: typing.Optional[builtins.str] = None,
    stream_exception_policy: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1792c044a8183899977c1c759b0dc4809733af4b515a87239cda2dbdd919aebd(
    *,
    action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d113bff3112ac3b16e2d039908c10d639ebf0d4f0cbca4fa605391b37140f02(
    *,
    resource_arn: builtins.str,
    override: typing.Optional[typing.Union[typing.Union[CfnFirewallPolicy.StatefulRuleGroupOverrideProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    priority: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eeb3b63c924fca739287a5c61341c6548c17f155d48bf5a13eb73c39aa21407(
    *,
    priority: jsii.Number,
    resource_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ce4336ad7eadbfc713ba89ef6185365f6f76ec8c82d066f9feb597c1a91e695(
    *,
    firewall_policy: typing.Union[typing.Union[CfnFirewallPolicy.FirewallPolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    firewall_policy_name: builtins.str,
    description: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e14d1bcf8aef5c042ad76c2672af34c8c8d3b1914e8c46c4b7c7a21c0322f090(
    *,
    firewall_name: builtins.str,
    firewall_policy_arn: builtins.str,
    subnet_mappings: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFirewall.SubnetMappingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    vpc_id: builtins.str,
    delete_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    description: typing.Optional[builtins.str] = None,
    firewall_policy_change_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    subnet_change_protection: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e572189805198c8c599ff0b949c501aece926b783946b760a214bd87e608ca1(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    firewall_arn: builtins.str,
    logging_configuration: typing.Union[typing.Union[CfnLoggingConfiguration.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    firewall_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66e7a57ffde7b81ac81b5d5f626bd560920bf6e0173fcad26d858a3fbbd9c4c(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbba926e175fa1ef861a299cea9a09bdf9795c2646bf2ef660e3b7d3e767e4ab(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__525b7863f62db1ade26d04627bc175926fe4d76844a9fd200a6a91dae9779771(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e798b456052b8c2086351677c114e00b0942d94f1de9de37300042c024460d20(
    value: typing.Union[CfnLoggingConfiguration.LoggingConfigurationProperty, _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef8303cdaae819b067bd9e5ded8ff20f086a3df175087ad976959456564a256b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fad0a980a3ab04ab0824eb8d27178b187cbb8849bf318abdcbf141b7464841f(
    *,
    log_destination: typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, builtins.str]],
    log_destination_type: builtins.str,
    log_type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9024539f8288f951b649de8d18b2be532319092e5773573379d8e68f54d2e158(
    *,
    log_destination_configs: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnLoggingConfiguration.LogDestinationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b86ec82b24a76909141b464905dc9c1cceece8775cde4cb1dfca29feccf04bfd(
    *,
    firewall_arn: builtins.str,
    logging_configuration: typing.Union[typing.Union[CfnLoggingConfiguration.LoggingConfigurationProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    firewall_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__983ddd00cbc6193f212da53ba594e872a8bd378850163c7502d8bbb179c1a0d4(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    capacity: jsii.Number,
    rule_group_name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    rule_group: typing.Optional[typing.Union[typing.Union[CfnRuleGroup.RuleGroupProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42bb558ba1abce8970d4ddd52590a3f607fb40fbbf1081e4e704717e618cf2ba(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__874114f82bf805fa2503ca54b18b7c746c000d2971b534d541ee8790c865b73b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__944cc27004f5f6e87349c201195bbfa14ed555a8c2b80e0d10c8afb771492a3d(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a8a7c922dcdd1a8f481bbdaceea9919e32d99023b98646b689d222c41ec70a2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bbfb8f405a34a90e601801aab6e1f6d2559ce27bbe06465dd14786159daee94(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__720d692516e3bdedd057d2e65252900e618c65d648b49c48564cf38a51a9b8a2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__927b7a010d209242cb9bf5ae1d58c5b1266e00003f183311f4c241a1cbc56d5a(
    value: typing.Optional[typing.Union[CfnRuleGroup.RuleGroupProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57a61ec8df6b02ce17665ab7c72d51beb1af279b08cf757008923d8de63f5121(
    *,
    publish_metric_action: typing.Optional[typing.Union[typing.Union[CfnRuleGroup.PublishMetricActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfa7eb306ac4e8737176a63ef0efc3f1ae0f9c0abc078a55d94b47a807b6c372(
    *,
    address_definition: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c66d63a97717f01292acaeb21ebc21fa2ed05d7d54b60793e4c0b0b05879dc23(
    *,
    action_definition: typing.Union[typing.Union[CfnRuleGroup.ActionDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    action_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e25770eb2f264d7e1a1a272324545eb43d22857c168fe7f0c61714a037afdc9(
    *,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9291f0d336e789862d1b21fa57da829eeeb686c7511d88b16b7b9c061a15dc54(
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

def _typecheckingstub__455575987c18e7759807d2ebb4076371230813c651be3ff558735eb457c9855d(
    *,
    definition: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcfa6c3068c864391b1853461edef15e06c23bdafa3c810609ab64bd0e2d6d08(
    *,
    reference_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__048acb95a5f6d246c909fb03611d1591f6eb7b24a42befaa072404a0204272f1(
    *,
    destination_ports: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRuleGroup.PortRangeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    destinations: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRuleGroup.AddressProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    protocols: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[jsii.Number]]] = None,
    source_ports: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRuleGroup.PortRangeProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    sources: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRuleGroup.AddressProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tcp_flags: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRuleGroup.TCPFlagFieldProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c53637ab6bc55106a61a28687b8782a2d46a8d1941d17ac691c1d9136d84b19c(
    *,
    from_port: jsii.Number,
    to_port: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__953a1c2dbe78764d91ac1ba1885334c2cd851b4317dd08f929aea348425461b6(
    *,
    definition: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9973571f9acb159728bd56d9c1e9b7839352de51bb546f5281abf952b0aeebfe(
    *,
    dimensions: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRuleGroup.DimensionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee4f19b32f3c7d602be0d28747b4103323664dd794da9b9657cb08a053f4edf3(
    *,
    ip_set_references: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnRuleGroup.IPSetReferenceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22c7f9dab75a20e73b108b1af44fd9d79a80a014fe4068bce1a3ab407dc27fcf(
    *,
    actions: typing.Sequence[builtins.str],
    match_attributes: typing.Union[typing.Union[CfnRuleGroup.MatchAttributesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__459f40129bea183e20ed7540e7155a804f8dbab704a170831290bbae46b0a973(
    *,
    rules_source: typing.Union[typing.Union[CfnRuleGroup.RulesSourceProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    reference_sets: typing.Optional[typing.Union[typing.Union[CfnRuleGroup.ReferenceSetsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    rule_variables: typing.Optional[typing.Union[typing.Union[CfnRuleGroup.RuleVariablesProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    stateful_rule_options: typing.Optional[typing.Union[typing.Union[CfnRuleGroup.StatefulRuleOptionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92f4b353b5d21e869cffb30f0e4851e88a5337cba66d95afe9f2119bdd3f9b1(
    *,
    keyword: builtins.str,
    settings: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d59ef28a39e53b26fe7231efdb462a0e3451f72a3deb30a34bdc922ea424af9f(
    *,
    ip_sets: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnRuleGroup.IPSetProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    port_sets: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Mapping[builtins.str, typing.Union[typing.Union[CfnRuleGroup.PortSetProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60fa924e28f618b9ccf9e51f519835b16d9d536e9609354eccd5a13d327ebb92(
    *,
    generated_rules_type: builtins.str,
    targets: typing.Sequence[builtins.str],
    target_types: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3943f68e627f69b2a88a3b02dadd23b899188912bb3cdc30cbc57632aec6908b(
    *,
    rules_source_list: typing.Optional[typing.Union[typing.Union[CfnRuleGroup.RulesSourceListProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    rules_string: typing.Optional[builtins.str] = None,
    stateful_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRuleGroup.StatefulRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    stateless_rules_and_custom_actions: typing.Optional[typing.Union[typing.Union[CfnRuleGroup.StatelessRulesAndCustomActionsProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce2f0cfbdf85aea8b7d8c41c74061818229fcdbae95b2e60cdd4f17c5da9b807(
    *,
    rule_order: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f9813846b53a1e37323a376971bdafc878b968e231d3e66db9c71fe3cd14274(
    *,
    action: builtins.str,
    header: typing.Union[typing.Union[CfnRuleGroup.HeaderProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
    rule_options: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRuleGroup.RuleOptionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d12bec9e2947d23e5d3c82f547eacd5b7e4e85e85fb3351591f9ae134eb0192(
    *,
    priority: jsii.Number,
    rule_definition: typing.Union[typing.Union[CfnRuleGroup.RuleDefinitionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9cad60ff3c5504650174283859bcbac1132ad2ab1488edf1d944cf7b83554233(
    *,
    stateless_rules: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRuleGroup.StatelessRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    custom_actions: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRuleGroup.CustomActionProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d02937fbc62a87d6b051b94e68696a4659cc3fe6babf5262854818d6a0f6b71(
    *,
    flags: typing.Sequence[builtins.str],
    masks: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce0205187b645d6fa1463e1dceac1435e629c188ab96298d071064dec6198a2a(
    *,
    capacity: jsii.Number,
    rule_group_name: builtins.str,
    type: builtins.str,
    description: typing.Optional[builtins.str] = None,
    rule_group: typing.Optional[typing.Union[typing.Union[CfnRuleGroup.RuleGroupProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
