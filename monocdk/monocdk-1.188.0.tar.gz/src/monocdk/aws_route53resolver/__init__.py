'''
# Amazon Route53 Resolver Construct Library

## DNS Firewall

With Route 53 Resolver DNS Firewall, you can filter and regulate outbound DNS traffic for your
virtual private connections (VPCs). To do this, you create reusable collections of filtering rules
in DNS Firewall rule groups and associate the rule groups to your VPC.

DNS Firewall provides protection for outbound DNS requests from your VPCs. These requests route
through Resolver for domain name resolution. A primary use of DNS Firewall protections is to help
prevent DNS exfiltration of your data. DNS exfiltration can happen when a bad actor compromises
an application instance in your VPC and then uses DNS lookup to send data out of the VPC to a domain
that they control. With DNS Firewall, you can monitor and control the domains that your applications
can query. You can deny access to the domains that you know to be bad and allow all other queries
to pass through. Alternately, you can deny access to all domains except for the ones that you
explicitly trust.

### Domain lists

Domain lists can be created using a list of strings, a text file stored in Amazon S3 or a local
text file:

```python
block_list = route53resolver.FirewallDomainList(self, "BlockList",
    domains=route53resolver.FirewallDomains.from_list(["bad-domain.com", "bot-domain.net"])
)

s3_list = route53resolver.FirewallDomainList(self, "S3List",
    domains=route53resolver.FirewallDomains.from_s3_url("s3://bucket/prefix/object")
)

asset_list = route53resolver.FirewallDomainList(self, "AssetList",
    domains=route53resolver.FirewallDomains.from_asset("/path/to/domains.txt")
)
```

The file must be a text file and must contain a single domain per line.

Use `FirewallDomainList.fromFirewallDomainListId()` to import an existing or [AWS managed domain list](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/resolver-dns-firewall-managed-domain-lists.html):

```python
# AWSManagedDomainsMalwareDomainList in us-east-1
malware_list = route53resolver.FirewallDomainList.from_firewall_domain_list_id(self, "Malware", "rslvr-fdl-2c46f2ecbfec4dcc")
```

### Rule group

Create a rule group:

```python
# my_block_list: route53resolver.FirewallDomainList

route53resolver.FirewallRuleGroup(self, "RuleGroup",
    rules=[route53resolver.aws_route53resolver.FirewallRule(
        priority=10,
        firewall_domain_list=my_block_list,
        # block and reply with NODATA
        action=route53resolver.FirewallRuleAction.block()
    )
    ]
)
```

Rules can be added at construction time or using `addRule()`:

```python
# my_block_list: route53resolver.FirewallDomainList
# rule_group: route53resolver.FirewallRuleGroup


rule_group.add_rule(
    priority=10,
    firewall_domain_list=my_block_list,
    # block and reply with NXDOMAIN
    action=route53resolver.FirewallRuleAction.block(route53resolver.DnsBlockResponse.nx_domain())
)

rule_group.add_rule(
    priority=20,
    firewall_domain_list=my_block_list,
    # block and override DNS response with a custom domain
    action=route53resolver.FirewallRuleAction.block(route53resolver.DnsBlockResponse.override("amazon.com"))
)
```

Use `associate()` to associate a rule group with a VPC:

```python
import monocdk as ec2

# rule_group: route53resolver.FirewallRuleGroup
# my_vpc: ec2.Vpc


rule_group.associate("Association",
    priority=101,
    vpc=my_vpc
)
```
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

import constructs as _constructs_77d1e7e8
from .. import (
    CfnResource as _CfnResource_e0a482dc,
    CfnTag as _CfnTag_95fbdc29,
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_ec2 import IVpc as _IVpc_6d1f76c4
from ..aws_s3 import IBucket as _IBucket_73486e29


@jsii.implements(_IInspectable_82c04a63)
class CfnFirewallDomainList(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.CfnFirewallDomainList",
):
    '''A CloudFormation ``AWS::Route53Resolver::FirewallDomainList``.

    High-level information about a list of firewall domains for use in a `AWS::Route53Resolver::FirewallRule <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-rule.html>`_ . This is returned by `GetFirewallDomainList <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_GetFirewallDomainList.html>`_ .

    To retrieve the domains that are defined for this domain list, call `ListFirewallDomains <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_ListFirewallDomains.html>`_ .

    :cloudformationResource: AWS::Route53Resolver::FirewallDomainList
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53resolver as route53resolver
        
        cfn_firewall_domain_list = route53resolver.CfnFirewallDomainList(self, "MyCfnFirewallDomainList",
            domain_file_url="domainFileUrl",
            domains=["domains"],
            name="name",
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
        domain_file_url: typing.Optional[builtins.str] = None,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53Resolver::FirewallDomainList``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param domain_file_url: The fully qualified URL or URI of the file stored in Amazon Simple Storage Service (Amazon S3) that contains the list of domains to import. The file must be in an S3 bucket that's in the same Region as your DNS Firewall. The file must be a text file and must contain a single domain per line.
        :param domains: A list of the domain lists that you have defined.
        :param name: The name of the domain list.
        :param tags: A list of the tag keys and values that you want to associate with the domain list.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9226e89e860d3053edc103ef2b7a6a6bc1014c625375bf8f8e9206d0dd6bf8e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFirewallDomainListProps(
            domain_file_url=domain_file_url, domains=domains, name=name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__432fe92b6c39ad26f62e6dcfe1967fd0387026460efdce456ebff84738882dbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__514bcaed72c16e54daa31d2d7f5589ffda651bb7a26d82de6611dcfe1752ef35)
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
        '''The Amazon Resource Name (ARN) of the firewall domain list.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''The date and time that the domain list was created, in Unix time format and Coordinated Universal Time (UTC).

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatorRequestId")
    def attr_creator_request_id(self) -> builtins.str:
        '''A unique string defined by you to identify the request.

        This allows you to retry failed requests without the risk of running the operation twice. This can be any unique string, for example, a timestamp.

        :cloudformationAttribute: CreatorRequestId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatorRequestId"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainCount")
    def attr_domain_count(self) -> jsii.Number:
        '''The number of domain names that are specified in the domain list.

        :cloudformationAttribute: DomainCount
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrDomainCount"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the domain list.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrManagedOwnerName")
    def attr_managed_owner_name(self) -> builtins.str:
        '''The owner of the list, used only for lists that are not managed by you.

        For example, the managed domain list ``AWSManagedDomainsMalwareDomainList`` has the managed owner name ``Route 53 Resolver DNS Firewall`` .

        :cloudformationAttribute: ManagedOwnerName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrManagedOwnerName"))

    @builtins.property
    @jsii.member(jsii_name="attrModificationTime")
    def attr_modification_time(self) -> builtins.str:
        '''The date and time that the domain list was last modified, in Unix time format and Coordinated Universal Time (UTC).

        :cloudformationAttribute: ModificationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrModificationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the domain list.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusMessage")
    def attr_status_message(self) -> builtins.str:
        '''Additional information about the status of the list, if available.

        :cloudformationAttribute: StatusMessage
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusMessage"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of the tag keys and values that you want to associate with the domain list.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html#cfn-route53resolver-firewalldomainlist-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="domainFileUrl")
    def domain_file_url(self) -> typing.Optional[builtins.str]:
        '''The fully qualified URL or URI of the file stored in Amazon Simple Storage Service (Amazon S3) that contains the list of domains to import.

        The file must be in an S3 bucket that's in the same Region as your DNS Firewall. The file must be a text file and must contain a single domain per line.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html#cfn-route53resolver-firewalldomainlist-domainfileurl
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainFileUrl"))

    @domain_file_url.setter
    def domain_file_url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3076e952c50f9de33664971e14f713b546bb1b1a6a2a786caf510101cc664529)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainFileUrl", value)

    @builtins.property
    @jsii.member(jsii_name="domains")
    def domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the domain lists that you have defined.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html#cfn-route53resolver-firewalldomainlist-domains
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "domains"))

    @domains.setter
    def domains(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93143312ffbb8bb075cb8e6f1377fb2264e3cd58f4df4e2859ffc45ae30ee235)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domains", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the domain list.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html#cfn-route53resolver-firewalldomainlist-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0b3018503235ebe09449b0014355e8db18d7b6181b4f8b10f0994605ce529b2b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.CfnFirewallDomainListProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_file_url": "domainFileUrl",
        "domains": "domains",
        "name": "name",
        "tags": "tags",
    },
)
class CfnFirewallDomainListProps:
    def __init__(
        self,
        *,
        domain_file_url: typing.Optional[builtins.str] = None,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnFirewallDomainList``.

        :param domain_file_url: The fully qualified URL or URI of the file stored in Amazon Simple Storage Service (Amazon S3) that contains the list of domains to import. The file must be in an S3 bucket that's in the same Region as your DNS Firewall. The file must be a text file and must contain a single domain per line.
        :param domains: A list of the domain lists that you have defined.
        :param name: The name of the domain list.
        :param tags: A list of the tag keys and values that you want to associate with the domain list.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_route53resolver as route53resolver
            
            cfn_firewall_domain_list_props = route53resolver.CfnFirewallDomainListProps(
                domain_file_url="domainFileUrl",
                domains=["domains"],
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bfb31349d99e57f0d1b5108c31b489d58bdfcd93b38642dbad81c579d931ae56)
            check_type(argname="argument domain_file_url", value=domain_file_url, expected_type=type_hints["domain_file_url"])
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain_file_url is not None:
            self._values["domain_file_url"] = domain_file_url
        if domains is not None:
            self._values["domains"] = domains
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def domain_file_url(self) -> typing.Optional[builtins.str]:
        '''The fully qualified URL or URI of the file stored in Amazon Simple Storage Service (Amazon S3) that contains the list of domains to import.

        The file must be in an S3 bucket that's in the same Region as your DNS Firewall. The file must be a text file and must contain a single domain per line.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html#cfn-route53resolver-firewalldomainlist-domainfileurl
        '''
        result = self._values.get("domain_file_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of the domain lists that you have defined.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html#cfn-route53resolver-firewalldomainlist-domains
        '''
        result = self._values.get("domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the domain list.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html#cfn-route53resolver-firewalldomainlist-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of the tag keys and values that you want to associate with the domain list.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html#cfn-route53resolver-firewalldomainlist-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFirewallDomainListProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnFirewallRuleGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.CfnFirewallRuleGroup",
):
    '''A CloudFormation ``AWS::Route53Resolver::FirewallRuleGroup``.

    High-level information for a firewall rule group. A firewall rule group is a collection of rules that DNS Firewall uses to filter DNS network traffic for a VPC. To retrieve the rules for the rule group, call `ListFirewallRules <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_ListFirewallRules.html>`_ .

    :cloudformationResource: AWS::Route53Resolver::FirewallRuleGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53resolver as route53resolver
        
        cfn_firewall_rule_group = route53resolver.CfnFirewallRuleGroup(self, "MyCfnFirewallRuleGroup",
            firewall_rules=[route53resolver.CfnFirewallRuleGroup.FirewallRuleProperty(
                action="action",
                firewall_domain_list_id="firewallDomainListId",
                priority=123,
        
                # the properties below are optional
                block_override_dns_type="blockOverrideDnsType",
                block_override_domain="blockOverrideDomain",
                block_override_ttl=123,
                block_response="blockResponse"
            )],
            name="name",
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
        firewall_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnFirewallRuleGroup.FirewallRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53Resolver::FirewallRuleGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param firewall_rules: A list of the rules that you have defined.
        :param name: The name of the rule group.
        :param tags: A list of the tag keys and values that you want to associate with the rule group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78963d0f59dce3be63f966b2e817cf54fa911a8633d79b95420f8ecdad76bbc0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFirewallRuleGroupProps(
            firewall_rules=firewall_rules, name=name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ce870ddbc028e94a8042e6b9b9ba1d59a813a74a47f3211ac520e7d83a33ed7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__146811da39f46bf0f891329d168b61984fbfb756cef2397ce3192ed448def2dd)
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
        '''The ARN (Amazon Resource Name) of the rule group.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''The date and time that the rule group was created, in Unix time format and Coordinated Universal Time (UTC).

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatorRequestId")
    def attr_creator_request_id(self) -> builtins.str:
        '''A unique string defined by you to identify the request.

        This allows you to retry failed requests without the risk of running the operation twice. This can be any unique string, for example, a timestamp.

        :cloudformationAttribute: CreatorRequestId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatorRequestId"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the rule group.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrModificationTime")
    def attr_modification_time(self) -> builtins.str:
        '''The date and time that the rule group was last modified, in Unix time format and Coordinated Universal Time (UTC).

        :cloudformationAttribute: ModificationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrModificationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrOwnerId")
    def attr_owner_id(self) -> builtins.str:
        '''The AWS account ID for the account that created the rule group.

        When a rule group is shared with your account, this is the account that has shared the rule group with you.

        :cloudformationAttribute: OwnerId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOwnerId"))

    @builtins.property
    @jsii.member(jsii_name="attrRuleCount")
    def attr_rule_count(self) -> jsii.Number:
        '''The number of rules in the rule group.

        :cloudformationAttribute: RuleCount
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrRuleCount"))

    @builtins.property
    @jsii.member(jsii_name="attrShareStatus")
    def attr_share_status(self) -> builtins.str:
        '''Whether the rule group is shared with other AWS accounts , or was shared with the current account by another AWS account .

        Sharing is configured through AWS Resource Access Manager ( AWS RAM ).

        :cloudformationAttribute: ShareStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrShareStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the domain list.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusMessage")
    def attr_status_message(self) -> builtins.str:
        '''Additional information about the status of the rule group, if available.

        :cloudformationAttribute: StatusMessage
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusMessage"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of the tag keys and values that you want to associate with the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html#cfn-route53resolver-firewallrulegroup-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="firewallRules")
    def firewall_rules(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallRuleGroup.FirewallRuleProperty", _IResolvable_a771d0ef]]]]:
        '''A list of the rules that you have defined.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html#cfn-route53resolver-firewallrulegroup-firewallrules
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallRuleGroup.FirewallRuleProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "firewallRules"))

    @firewall_rules.setter
    def firewall_rules(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnFirewallRuleGroup.FirewallRuleProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7640cfb1c6b4f15a53834a31ab5702b13b2863d3762fc9383e42c0b8c97d78a3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallRules", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html#cfn-route53resolver-firewallrulegroup-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c33934fbcd24cc426a7f163e3b9f48670c6714a3356e9ed6d0362a18d090a329)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_route53resolver.CfnFirewallRuleGroup.FirewallRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action": "action",
            "firewall_domain_list_id": "firewallDomainListId",
            "priority": "priority",
            "block_override_dns_type": "blockOverrideDnsType",
            "block_override_domain": "blockOverrideDomain",
            "block_override_ttl": "blockOverrideTtl",
            "block_response": "blockResponse",
        },
    )
    class FirewallRuleProperty:
        def __init__(
            self,
            *,
            action: builtins.str,
            firewall_domain_list_id: builtins.str,
            priority: jsii.Number,
            block_override_dns_type: typing.Optional[builtins.str] = None,
            block_override_domain: typing.Optional[builtins.str] = None,
            block_override_ttl: typing.Optional[jsii.Number] = None,
            block_response: typing.Optional[builtins.str] = None,
        ) -> None:
            '''A single firewall rule in a rule group.

            :param action: The action that DNS Firewall should take on a DNS query when it matches one of the domains in the rule's domain list: - ``ALLOW`` - Permit the request to go through. - ``ALERT`` - Permit the request to go through but send an alert to the logs. - ``BLOCK`` - Disallow the request. If this is specified,then ``BlockResponse`` must also be specified. if ``BlockResponse`` is ``OVERRIDE`` , then all of the following ``OVERRIDE`` attributes must be specified: - ``BlockOverrideDnsType`` - ``BlockOverrideDomain`` - ``BlockOverrideTtl``
            :param firewall_domain_list_id: The ID of the domain list that's used in the rule.
            :param priority: The priority of the rule in the rule group. This value must be unique within the rule group. DNS Firewall processes the rules in a rule group by order of priority, starting from the lowest setting.
            :param block_override_dns_type: The DNS record's type. This determines the format of the record value that you provided in ``BlockOverrideDomain`` . Used for the rule action ``BLOCK`` with a ``BlockResponse`` setting of ``OVERRIDE`` .
            :param block_override_domain: The custom DNS record to send back in response to the query. Used for the rule action ``BLOCK`` with a ``BlockResponse`` setting of ``OVERRIDE`` .
            :param block_override_ttl: The recommended amount of time, in seconds, for the DNS resolver or web browser to cache the provided override record. Used for the rule action ``BLOCK`` with a ``BlockResponse`` setting of ``OVERRIDE`` .
            :param block_response: The way that you want DNS Firewall to block the request. Used for the rule action setting ``BLOCK`` . - ``NODATA`` - Respond indicating that the query was successful, but no response is available for it. - ``NXDOMAIN`` - Respond indicating that the domain name that's in the query doesn't exist. - ``OVERRIDE`` - Provide a custom override in the response. This option requires custom handling details in the rule's ``BlockOverride*`` settings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_route53resolver as route53resolver
                
                firewall_rule_property = route53resolver.CfnFirewallRuleGroup.FirewallRuleProperty(
                    action="action",
                    firewall_domain_list_id="firewallDomainListId",
                    priority=123,
                
                    # the properties below are optional
                    block_override_dns_type="blockOverrideDnsType",
                    block_override_domain="blockOverrideDomain",
                    block_override_ttl=123,
                    block_response="blockResponse"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__13c3eaad7971060e0e1744d166fee029f5bbaf6f2842bb7d9fbd9f0f591536b8)
                check_type(argname="argument action", value=action, expected_type=type_hints["action"])
                check_type(argname="argument firewall_domain_list_id", value=firewall_domain_list_id, expected_type=type_hints["firewall_domain_list_id"])
                check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
                check_type(argname="argument block_override_dns_type", value=block_override_dns_type, expected_type=type_hints["block_override_dns_type"])
                check_type(argname="argument block_override_domain", value=block_override_domain, expected_type=type_hints["block_override_domain"])
                check_type(argname="argument block_override_ttl", value=block_override_ttl, expected_type=type_hints["block_override_ttl"])
                check_type(argname="argument block_response", value=block_response, expected_type=type_hints["block_response"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "action": action,
                "firewall_domain_list_id": firewall_domain_list_id,
                "priority": priority,
            }
            if block_override_dns_type is not None:
                self._values["block_override_dns_type"] = block_override_dns_type
            if block_override_domain is not None:
                self._values["block_override_domain"] = block_override_domain
            if block_override_ttl is not None:
                self._values["block_override_ttl"] = block_override_ttl
            if block_response is not None:
                self._values["block_response"] = block_response

        @builtins.property
        def action(self) -> builtins.str:
            '''The action that DNS Firewall should take on a DNS query when it matches one of the domains in the rule's domain list:  - ``ALLOW`` - Permit the request to go through.

            - ``ALERT`` - Permit the request to go through but send an alert to the logs.
            - ``BLOCK`` - Disallow the request. If this is specified,then ``BlockResponse`` must also be specified.

            if ``BlockResponse`` is ``OVERRIDE`` , then all of the following ``OVERRIDE`` attributes must be specified:

            - ``BlockOverrideDnsType``
            - ``BlockOverrideDomain``
            - ``BlockOverrideTtl``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-action
            '''
            result = self._values.get("action")
            assert result is not None, "Required property 'action' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def firewall_domain_list_id(self) -> builtins.str:
            '''The ID of the domain list that's used in the rule.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-firewalldomainlistid
            '''
            result = self._values.get("firewall_domain_list_id")
            assert result is not None, "Required property 'firewall_domain_list_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def priority(self) -> jsii.Number:
            '''The priority of the rule in the rule group.

            This value must be unique within the rule group. DNS Firewall processes the rules in a rule group by order of priority, starting from the lowest setting.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-priority
            '''
            result = self._values.get("priority")
            assert result is not None, "Required property 'priority' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def block_override_dns_type(self) -> typing.Optional[builtins.str]:
            '''The DNS record's type.

            This determines the format of the record value that you provided in ``BlockOverrideDomain`` . Used for the rule action ``BLOCK`` with a ``BlockResponse`` setting of ``OVERRIDE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-blockoverridednstype
            '''
            result = self._values.get("block_override_dns_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def block_override_domain(self) -> typing.Optional[builtins.str]:
            '''The custom DNS record to send back in response to the query.

            Used for the rule action ``BLOCK`` with a ``BlockResponse`` setting of ``OVERRIDE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-blockoverridedomain
            '''
            result = self._values.get("block_override_domain")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def block_override_ttl(self) -> typing.Optional[jsii.Number]:
            '''The recommended amount of time, in seconds, for the DNS resolver or web browser to cache the provided override record.

            Used for the rule action ``BLOCK`` with a ``BlockResponse`` setting of ``OVERRIDE`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-blockoverridettl
            '''
            result = self._values.get("block_override_ttl")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def block_response(self) -> typing.Optional[builtins.str]:
            '''The way that you want DNS Firewall to block the request. Used for the rule action setting ``BLOCK`` .

            - ``NODATA`` - Respond indicating that the query was successful, but no response is available for it.
            - ``NXDOMAIN`` - Respond indicating that the domain name that's in the query doesn't exist.
            - ``OVERRIDE`` - Provide a custom override in the response. This option requires custom handling details in the rule's ``BlockOverride*`` settings.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-firewallrulegroup-firewallrule.html#cfn-route53resolver-firewallrulegroup-firewallrule-blockresponse
            '''
            result = self._values.get("block_response")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FirewallRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnFirewallRuleGroupAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.CfnFirewallRuleGroupAssociation",
):
    '''A CloudFormation ``AWS::Route53Resolver::FirewallRuleGroupAssociation``.

    An association between a firewall rule group and a VPC, which enables DNS filtering for the VPC.

    :cloudformationResource: AWS::Route53Resolver::FirewallRuleGroupAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53resolver as route53resolver
        
        cfn_firewall_rule_group_association = route53resolver.CfnFirewallRuleGroupAssociation(self, "MyCfnFirewallRuleGroupAssociation",
            firewall_rule_group_id="firewallRuleGroupId",
            priority=123,
            vpc_id="vpcId",
        
            # the properties below are optional
            mutation_protection="mutationProtection",
            name="name",
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
        firewall_rule_group_id: builtins.str,
        priority: jsii.Number,
        vpc_id: builtins.str,
        mutation_protection: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53Resolver::FirewallRuleGroupAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param firewall_rule_group_id: The unique identifier of the firewall rule group.
        :param priority: The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC. DNS Firewall filters VPC traffic starting from rule group with the lowest numeric priority setting. You must specify a unique priority for each rule group that you associate with a single VPC. To make it easier to insert rule groups later, leave space between the numbers, for example, use 101, 200, and so on. You can change the priority setting for a rule group association after you create it. The allowed values for ``Priority`` are between 100 and 9900 (excluding 100 and 9900).
        :param vpc_id: The unique identifier of the VPC that is associated with the rule group.
        :param mutation_protection: If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections.
        :param name: The name of the association.
        :param tags: A list of the tag keys and values that you want to associate with the rule group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65e2efaeb3cba1cff1a591cc4af128bd99fb7d0a7d2875a762c76a992abb7022)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFirewallRuleGroupAssociationProps(
            firewall_rule_group_id=firewall_rule_group_id,
            priority=priority,
            vpc_id=vpc_id,
            mutation_protection=mutation_protection,
            name=name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__089b903322965086bdaad22e49308aae6bd1797b01fd9ff782b9c4db726193c6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__29476ebda3c6da62e89cd75239badfab9641f7890167e8fd0beef724513ff219)
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
        '''The Amazon Resource Name (ARN) of the firewall rule group association.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''The date and time that the association was created, in Unix time format and Coordinated Universal Time (UTC).

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatorRequestId")
    def attr_creator_request_id(self) -> builtins.str:
        '''A unique string defined by you to identify the request.

        This allows you to retry failed requests without the risk of running the operation twice. This can be any unique string, for example, a timestamp.

        :cloudformationAttribute: CreatorRequestId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatorRequestId"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The identifier for the association.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrManagedOwnerName")
    def attr_managed_owner_name(self) -> builtins.str:
        '''The owner of the association, used only for associations that are not managed by you.

        If you use AWS Firewall Manager to manage your firewallls from DNS Firewall, then this reports Firewall Manager as the managed owner.

        :cloudformationAttribute: ManagedOwnerName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrManagedOwnerName"))

    @builtins.property
    @jsii.member(jsii_name="attrModificationTime")
    def attr_modification_time(self) -> builtins.str:
        '''The date and time that the association was last modified, in Unix time format and Coordinated Universal Time (UTC).

        :cloudformationAttribute: ModificationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrModificationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The current status of the association.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusMessage")
    def attr_status_message(self) -> builtins.str:
        '''Additional information about the status of the response, if available.

        :cloudformationAttribute: StatusMessage
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusMessage"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of the tag keys and values that you want to associate with the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupId")
    def firewall_rule_group_id(self) -> builtins.str:
        '''The unique identifier of the firewall rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-firewallrulegroupid
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupId"))

    @firewall_rule_group_id.setter
    def firewall_rule_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__869632dd26478eab16a8bbe7ed33b312b7fe791b1fc359c9bf1592f29eab6e26)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallRuleGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        '''The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC.

        DNS Firewall filters VPC traffic starting from rule group with the lowest numeric priority setting.

        You must specify a unique priority for each rule group that you associate with a single VPC. To make it easier to insert rule groups later, leave space between the numbers, for example, use 101, 200, and so on. You can change the priority setting for a rule group association after you create it.

        The allowed values for ``Priority`` are between 100 and 9900 (excluding 100 and 9900).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-priority
        '''
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__567078bedba758549d396bf118ff16b49d4eb6c4c3759e5d76bbeb70457e6063)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        '''The unique identifier of the VPC that is associated with the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-vpcid
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__823bb73cb66838530a67d52bf6dd9e3dbc4574992b77545f6c7bab4965005934)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value)

    @builtins.property
    @jsii.member(jsii_name="mutationProtection")
    def mutation_protection(self) -> typing.Optional[builtins.str]:
        '''If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-mutationprotection
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "mutationProtection"))

    @mutation_protection.setter
    def mutation_protection(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38a0c3c1e8a440cdc1bd36e7c5ccb2b0b5d6a2099f1f7c0e1dfe1e7d49762fc7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mutationProtection", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the association.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fec66f498650b5a588c4893cd3ece39fca209c31f3b139b819ebbfabdea3f50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.CfnFirewallRuleGroupAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "firewall_rule_group_id": "firewallRuleGroupId",
        "priority": "priority",
        "vpc_id": "vpcId",
        "mutation_protection": "mutationProtection",
        "name": "name",
        "tags": "tags",
    },
)
class CfnFirewallRuleGroupAssociationProps:
    def __init__(
        self,
        *,
        firewall_rule_group_id: builtins.str,
        priority: jsii.Number,
        vpc_id: builtins.str,
        mutation_protection: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnFirewallRuleGroupAssociation``.

        :param firewall_rule_group_id: The unique identifier of the firewall rule group.
        :param priority: The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC. DNS Firewall filters VPC traffic starting from rule group with the lowest numeric priority setting. You must specify a unique priority for each rule group that you associate with a single VPC. To make it easier to insert rule groups later, leave space between the numbers, for example, use 101, 200, and so on. You can change the priority setting for a rule group association after you create it. The allowed values for ``Priority`` are between 100 and 9900 (excluding 100 and 9900).
        :param vpc_id: The unique identifier of the VPC that is associated with the rule group.
        :param mutation_protection: If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections.
        :param name: The name of the association.
        :param tags: A list of the tag keys and values that you want to associate with the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_route53resolver as route53resolver
            
            cfn_firewall_rule_group_association_props = route53resolver.CfnFirewallRuleGroupAssociationProps(
                firewall_rule_group_id="firewallRuleGroupId",
                priority=123,
                vpc_id="vpcId",
            
                # the properties below are optional
                mutation_protection="mutationProtection",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e96119dbe51842e9579e97beeefce01a9caab6a034e939a122c19110cfb946ed)
            check_type(argname="argument firewall_rule_group_id", value=firewall_rule_group_id, expected_type=type_hints["firewall_rule_group_id"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument mutation_protection", value=mutation_protection, expected_type=type_hints["mutation_protection"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "firewall_rule_group_id": firewall_rule_group_id,
            "priority": priority,
            "vpc_id": vpc_id,
        }
        if mutation_protection is not None:
            self._values["mutation_protection"] = mutation_protection
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def firewall_rule_group_id(self) -> builtins.str:
        '''The unique identifier of the firewall rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-firewallrulegroupid
        '''
        result = self._values.get("firewall_rule_group_id")
        assert result is not None, "Required property 'firewall_rule_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC.

        DNS Firewall filters VPC traffic starting from rule group with the lowest numeric priority setting.

        You must specify a unique priority for each rule group that you associate with a single VPC. To make it easier to insert rule groups later, leave space between the numbers, for example, use 101, 200, and so on. You can change the priority setting for a rule group association after you create it.

        The allowed values for ``Priority`` are between 100 and 9900 (excluding 100 and 9900).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-priority
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''The unique identifier of the VPC that is associated with the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-vpcid
        '''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mutation_protection(self) -> typing.Optional[builtins.str]:
        '''If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-mutationprotection
        '''
        result = self._values.get("mutation_protection")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the association.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of the tag keys and values that you want to associate with the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFirewallRuleGroupAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.CfnFirewallRuleGroupProps",
    jsii_struct_bases=[],
    name_mapping={"firewall_rules": "firewallRules", "name": "name", "tags": "tags"},
)
class CfnFirewallRuleGroupProps:
    def __init__(
        self,
        *,
        firewall_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFirewallRuleGroup.FirewallRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnFirewallRuleGroup``.

        :param firewall_rules: A list of the rules that you have defined.
        :param name: The name of the rule group.
        :param tags: A list of the tag keys and values that you want to associate with the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_route53resolver as route53resolver
            
            cfn_firewall_rule_group_props = route53resolver.CfnFirewallRuleGroupProps(
                firewall_rules=[route53resolver.CfnFirewallRuleGroup.FirewallRuleProperty(
                    action="action",
                    firewall_domain_list_id="firewallDomainListId",
                    priority=123,
            
                    # the properties below are optional
                    block_override_dns_type="blockOverrideDnsType",
                    block_override_domain="blockOverrideDomain",
                    block_override_ttl=123,
                    block_response="blockResponse"
                )],
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b13410754afd4163093c293e9e89cc17fb278ff118c8d02819d84784a6891bdd)
            check_type(argname="argument firewall_rules", value=firewall_rules, expected_type=type_hints["firewall_rules"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if firewall_rules is not None:
            self._values["firewall_rules"] = firewall_rules
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def firewall_rules(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFirewallRuleGroup.FirewallRuleProperty, _IResolvable_a771d0ef]]]]:
        '''A list of the rules that you have defined.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html#cfn-route53resolver-firewallrulegroup-firewallrules
        '''
        result = self._values.get("firewall_rules")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFirewallRuleGroup.FirewallRuleProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html#cfn-route53resolver-firewallrulegroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of the tag keys and values that you want to associate with the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html#cfn-route53resolver-firewallrulegroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFirewallRuleGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResolverConfig(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.CfnResolverConfig",
):
    '''A CloudFormation ``AWS::Route53Resolver::ResolverConfig``.

    A complex type that contains information about a Resolver configuration for a VPC.

    :cloudformationResource: AWS::Route53Resolver::ResolverConfig
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverconfig.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53resolver as route53resolver
        
        cfn_resolver_config = route53resolver.CfnResolverConfig(self, "MyCfnResolverConfig",
            autodefined_reverse_flag="autodefinedReverseFlag",
            resource_id="resourceId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        autodefined_reverse_flag: builtins.str,
        resource_id: builtins.str,
    ) -> None:
        '''Create a new ``AWS::Route53Resolver::ResolverConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param autodefined_reverse_flag: Represents the desired status of ``AutodefinedReverse`` . The only supported value on creation is ``DISABLE`` . Deletion of this resource will return ``AutodefinedReverse`` to its default value of ``ENABLED`` .
        :param resource_id: The ID of the Amazon Virtual Private Cloud VPC that you're configuring Resolver for.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e08cd0ff1e98eabae1a5efea9e7377d51e6a5349e5fc08eb80eac151ea1dc1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResolverConfigProps(
            autodefined_reverse_flag=autodefined_reverse_flag, resource_id=resource_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__acda34f36454caebc2d7c0f4598eee5cd13e03036b77741874ce193c7899ea92)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e8a0b1b0e9877524306e7849834ed733bf3a70e8832b0c486f47b80a43380e2)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAutodefinedReverse")
    def attr_autodefined_reverse(self) -> builtins.str:
        '''The status of whether or not the Route 53 Resolver will create autodefined rules for reverse DNS lookups.

        This is enabled by default.

        :cloudformationAttribute: AutodefinedReverse
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAutodefinedReverse"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''ID for the Route 53 Resolver configuration.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrOwnerId")
    def attr_owner_id(self) -> builtins.str:
        '''The owner account ID of the Amazon Virtual Private Cloud VPC.

        :cloudformationAttribute: OwnerId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOwnerId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="autodefinedReverseFlag")
    def autodefined_reverse_flag(self) -> builtins.str:
        '''Represents the desired status of ``AutodefinedReverse`` .

        The only supported value on creation is ``DISABLE`` . Deletion of this resource will return ``AutodefinedReverse`` to its default value of ``ENABLED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverconfig.html#cfn-route53resolver-resolverconfig-autodefinedreverseflag
        '''
        return typing.cast(builtins.str, jsii.get(self, "autodefinedReverseFlag"))

    @autodefined_reverse_flag.setter
    def autodefined_reverse_flag(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23b591a5338200171cccfd25fb5719faf82403c7f719df09e668785b79cf649f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autodefinedReverseFlag", value)

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        '''The ID of the Amazon Virtual Private Cloud VPC that you're configuring Resolver for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverconfig.html#cfn-route53resolver-resolverconfig-resourceid
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @resource_id.setter
    def resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__221d5a700b499bc6ec219b6e3020ad6f41051121f3df6bb0b58a7bfa5aad51f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.CfnResolverConfigProps",
    jsii_struct_bases=[],
    name_mapping={
        "autodefined_reverse_flag": "autodefinedReverseFlag",
        "resource_id": "resourceId",
    },
)
class CfnResolverConfigProps:
    def __init__(
        self,
        *,
        autodefined_reverse_flag: builtins.str,
        resource_id: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnResolverConfig``.

        :param autodefined_reverse_flag: Represents the desired status of ``AutodefinedReverse`` . The only supported value on creation is ``DISABLE`` . Deletion of this resource will return ``AutodefinedReverse`` to its default value of ``ENABLED`` .
        :param resource_id: The ID of the Amazon Virtual Private Cloud VPC that you're configuring Resolver for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_route53resolver as route53resolver
            
            cfn_resolver_config_props = route53resolver.CfnResolverConfigProps(
                autodefined_reverse_flag="autodefinedReverseFlag",
                resource_id="resourceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607f67798d5caf456edb05d2aacfbeb716e1d6677768b82071fc05390a6d74f3)
            check_type(argname="argument autodefined_reverse_flag", value=autodefined_reverse_flag, expected_type=type_hints["autodefined_reverse_flag"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "autodefined_reverse_flag": autodefined_reverse_flag,
            "resource_id": resource_id,
        }

    @builtins.property
    def autodefined_reverse_flag(self) -> builtins.str:
        '''Represents the desired status of ``AutodefinedReverse`` .

        The only supported value on creation is ``DISABLE`` . Deletion of this resource will return ``AutodefinedReverse`` to its default value of ``ENABLED`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverconfig.html#cfn-route53resolver-resolverconfig-autodefinedreverseflag
        '''
        result = self._values.get("autodefined_reverse_flag")
        assert result is not None, "Required property 'autodefined_reverse_flag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_id(self) -> builtins.str:
        '''The ID of the Amazon Virtual Private Cloud VPC that you're configuring Resolver for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverconfig.html#cfn-route53resolver-resolverconfig-resourceid
        '''
        result = self._values.get("resource_id")
        assert result is not None, "Required property 'resource_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResolverDNSSECConfig(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.CfnResolverDNSSECConfig",
):
    '''A CloudFormation ``AWS::Route53Resolver::ResolverDNSSECConfig``.

    The ``AWS::Route53Resolver::ResolverDNSSECConfig`` resource is a complex type that contains information about a configuration for DNSSEC validation.

    :cloudformationResource: AWS::Route53Resolver::ResolverDNSSECConfig
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverdnssecconfig.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53resolver as route53resolver
        
        cfn_resolver_dNSSECConfig = route53resolver.CfnResolverDNSSECConfig(self, "MyCfnResolverDNSSECConfig",
            resource_id="resourceId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        resource_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Route53Resolver::ResolverDNSSECConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resource_id: The ID of the virtual private cloud (VPC) that you're configuring the DNSSEC validation status for.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba0b97183f6c675fd5d903d5f953db973478e09b73b38ecbdb3426f961fd0ebe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResolverDNSSECConfigProps(resource_id=resource_id)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc9d8352dbf8366d0ed5a016d104273bdf2b2201748da9d4828cc963041214e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6eeb52eec669df537bfd561bb8d58a8e9f4267010445d23f5ac3a3547e7daeca)
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
        '''The primary identifier of this ``ResolverDNSSECConfig`` resource.

        For example: ``rdsc-689d45d1ae623bf3`` .

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrOwnerId")
    def attr_owner_id(self) -> builtins.str:
        '''The AWS account of the owner.

        For example: ``111122223333`` .

        :cloudformationAttribute: OwnerId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOwnerId"))

    @builtins.property
    @jsii.member(jsii_name="attrValidationStatus")
    def attr_validation_status(self) -> builtins.str:
        '''The current status of this ``ResolverDNSSECConfig`` resource.

        For example: ``Enabled`` .

        :cloudformationAttribute: ValidationStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrValidationStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the virtual private cloud (VPC) that you're configuring the DNSSEC validation status for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverdnssecconfig.html#cfn-route53resolver-resolverdnssecconfig-resourceid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceId"))

    @resource_id.setter
    def resource_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b99470a420546ab85eabe22af61333634275e4204374a9e5083ce0978d9343f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.CfnResolverDNSSECConfigProps",
    jsii_struct_bases=[],
    name_mapping={"resource_id": "resourceId"},
)
class CfnResolverDNSSECConfigProps:
    def __init__(self, *, resource_id: typing.Optional[builtins.str] = None) -> None:
        '''Properties for defining a ``CfnResolverDNSSECConfig``.

        :param resource_id: The ID of the virtual private cloud (VPC) that you're configuring the DNSSEC validation status for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverdnssecconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_route53resolver as route53resolver
            
            cfn_resolver_dNSSECConfig_props = route53resolver.CfnResolverDNSSECConfigProps(
                resource_id="resourceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__860045c80d8c266206341c24dc179fb3b5895c29cba1f40b444dbd8dd1fbef78)
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resource_id is not None:
            self._values["resource_id"] = resource_id

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the virtual private cloud (VPC) that you're configuring the DNSSEC validation status for.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverdnssecconfig.html#cfn-route53resolver-resolverdnssecconfig-resourceid
        '''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverDNSSECConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResolverEndpoint(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.CfnResolverEndpoint",
):
    '''A CloudFormation ``AWS::Route53Resolver::ResolverEndpoint``.

    Creates a Resolver endpoint. There are two types of Resolver endpoints, inbound and outbound:

    - An *inbound Resolver endpoint* forwards DNS queries to the DNS service for a VPC from your network.
    - An *outbound Resolver endpoint* forwards DNS queries from the DNS service for a VPC to your network.

    :cloudformationResource: AWS::Route53Resolver::ResolverEndpoint
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53resolver as route53resolver
        
        cfn_resolver_endpoint = route53resolver.CfnResolverEndpoint(self, "MyCfnResolverEndpoint",
            direction="direction",
            ip_addresses=[route53resolver.CfnResolverEndpoint.IpAddressRequestProperty(
                subnet_id="subnetId",
        
                # the properties below are optional
                ip="ip"
            )],
            security_group_ids=["securityGroupIds"],
        
            # the properties below are optional
            name="name",
            outpost_arn="outpostArn",
            preferred_instance_type="preferredInstanceType",
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
        direction: builtins.str,
        ip_addresses: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnResolverEndpoint.IpAddressRequestProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        security_group_ids: typing.Sequence[builtins.str],
        name: typing.Optional[builtins.str] = None,
        outpost_arn: typing.Optional[builtins.str] = None,
        preferred_instance_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53Resolver::ResolverEndpoint``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param direction: Indicates whether the Resolver endpoint allows inbound or outbound DNS queries:. - ``INBOUND`` : allows DNS queries to your VPC from your network - ``OUTBOUND`` : allows DNS queries from your VPC to your network
        :param ip_addresses: The subnets and IP addresses in your VPC that DNS queries originate from (for outbound endpoints) or that you forward DNS queries to (for inbound endpoints). The subnet ID uniquely identifies a VPC.
        :param security_group_ids: The ID of one or more security groups that control access to this VPC. The security group must include one or more inbound rules (for inbound endpoints) or outbound rules (for outbound endpoints). Inbound and outbound rules must allow TCP and UDP access. For inbound access, open port 53. For outbound access, open the port that you're using for DNS queries on your network.
        :param name: A friendly name that lets you easily find a configuration in the Resolver dashboard in the Route 53 console.
        :param outpost_arn: ``AWS::Route53Resolver::ResolverEndpoint.OutpostArn``.
        :param preferred_instance_type: ``AWS::Route53Resolver::ResolverEndpoint.PreferredInstanceType``.
        :param tags: Route 53 Resolver doesn't support updating tags through CloudFormation.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de3bf2a11e078b4c521538b3b2cfe2efc4e2bed148e848aa95010328fef38d0b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResolverEndpointProps(
            direction=direction,
            ip_addresses=ip_addresses,
            security_group_ids=security_group_ids,
            name=name,
            outpost_arn=outpost_arn,
            preferred_instance_type=preferred_instance_type,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__458ae08d9fd9604cd883d3c4d8552a5358e45e3d1a706198d61fb4152079147d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0d545d4bbab249efadae077e96fbc6fb01ece34a9a034f18de5bb8274692618)
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
        '''The Amazon Resource Name (ARN) of the resolver endpoint, such as ``arn:aws:route53resolver:us-east-1:123456789012:resolver-endpoint/resolver-endpoint-a1bzhi`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrDirection")
    def attr_direction(self) -> builtins.str:
        '''Indicates whether the resolver endpoint allows inbound or outbound DNS queries.

        :cloudformationAttribute: Direction
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDirection"))

    @builtins.property
    @jsii.member(jsii_name="attrHostVpcId")
    def attr_host_vpc_id(self) -> builtins.str:
        '''The ID of the VPC that you want to create the resolver endpoint in.

        :cloudformationAttribute: HostVPCId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrHostVpcId"))

    @builtins.property
    @jsii.member(jsii_name="attrIpAddressCount")
    def attr_ip_address_count(self) -> builtins.str:
        '''The number of IP addresses that the resolver endpoint can use for DNS queries.

        :cloudformationAttribute: IpAddressCount
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrIpAddressCount"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''The name that you assigned to the resolver endpoint when you created the endpoint.

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="attrOutpostArn")
    def attr_outpost_arn(self) -> builtins.str:
        '''
        :cloudformationAttribute: OutpostArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOutpostArn"))

    @builtins.property
    @jsii.member(jsii_name="attrPreferredInstanceType")
    def attr_preferred_instance_type(self) -> builtins.str:
        '''
        :cloudformationAttribute: PreferredInstanceType
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrPreferredInstanceType"))

    @builtins.property
    @jsii.member(jsii_name="attrResolverEndpointId")
    def attr_resolver_endpoint_id(self) -> builtins.str:
        '''The ID of the resolver endpoint.

        :cloudformationAttribute: ResolverEndpointId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResolverEndpointId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Route 53 Resolver doesn't support updating tags through CloudFormation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="direction")
    def direction(self) -> builtins.str:
        '''Indicates whether the Resolver endpoint allows inbound or outbound DNS queries:.

        - ``INBOUND`` : allows DNS queries to your VPC from your network
        - ``OUTBOUND`` : allows DNS queries from your VPC to your network

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-direction
        '''
        return typing.cast(builtins.str, jsii.get(self, "direction"))

    @direction.setter
    def direction(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbf4356f85419d4da784b0d7ff8cdf5badc70333a348dfda516cfa00d05643b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "direction", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnResolverEndpoint.IpAddressRequestProperty", _IResolvable_a771d0ef]]]:
        '''The subnets and IP addresses in your VPC that DNS queries originate from (for outbound endpoints) or that you forward DNS queries to (for inbound endpoints).

        The subnet ID uniquely identifies a VPC.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-ipaddresses
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnResolverEndpoint.IpAddressRequestProperty", _IResolvable_a771d0ef]]], jsii.get(self, "ipAddresses"))

    @ip_addresses.setter
    def ip_addresses(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnResolverEndpoint.IpAddressRequestProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d207dbb161c27d4803c7fe06c88abb6878a39ee2a60a7b87e0a88c8e79482ce)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipAddresses", value)

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.List[builtins.str]:
        '''The ID of one or more security groups that control access to this VPC.

        The security group must include one or more inbound rules (for inbound endpoints) or outbound rules (for outbound endpoints). Inbound and outbound rules must allow TCP and UDP access. For inbound access, open port 53. For outbound access, open the port that you're using for DNS queries on your network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-securitygroupids
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7abd8da97ac62ac614dadf43af442954b68d8bf3218d854df86f6f09e54e09b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''A friendly name that lets you easily find a configuration in the Resolver dashboard in the Route 53 console.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__daf8b9135eae0efddf2609a72a08b6904b7acb2d9348884c9ce0719a6e7e94b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="outpostArn")
    def outpost_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::Route53Resolver::ResolverEndpoint.OutpostArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-outpostarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "outpostArn"))

    @outpost_arn.setter
    def outpost_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee253db2724909e5349fc710cb95e3f66abe09224024fa3851fc28cd6ad4db3a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "outpostArn", value)

    @builtins.property
    @jsii.member(jsii_name="preferredInstanceType")
    def preferred_instance_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::Route53Resolver::ResolverEndpoint.PreferredInstanceType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-preferredinstancetype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "preferredInstanceType"))

    @preferred_instance_type.setter
    def preferred_instance_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a816f84b471984362f5b67fb9937c76745d5edd936f766c0848f020568540245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredInstanceType", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_route53resolver.CfnResolverEndpoint.IpAddressRequestProperty",
        jsii_struct_bases=[],
        name_mapping={"subnet_id": "subnetId", "ip": "ip"},
    )
    class IpAddressRequestProperty:
        def __init__(
            self,
            *,
            subnet_id: builtins.str,
            ip: typing.Optional[builtins.str] = None,
        ) -> None:
            '''In a `CreateResolverEndpoint <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_CreateResolverEndpoint.html>`_ request, the IP address that DNS queries originate from (for outbound endpoints) or that you forward DNS queries to (for inbound endpoints). ``IpAddressRequest`` also includes the ID of the subnet that contains the IP address.

            :param subnet_id: The ID of the subnet that contains the IP address.
            :param ip: The IP address that you want to use for DNS queries.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverendpoint-ipaddressrequest.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_route53resolver as route53resolver
                
                ip_address_request_property = route53resolver.CfnResolverEndpoint.IpAddressRequestProperty(
                    subnet_id="subnetId",
                
                    # the properties below are optional
                    ip="ip"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ac895499b4ec270e952cf22e8cdb0a90ab2bd36e9a1bb2e88e261ac513ac9a9e)
                check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
                check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "subnet_id": subnet_id,
            }
            if ip is not None:
                self._values["ip"] = ip

        @builtins.property
        def subnet_id(self) -> builtins.str:
            '''The ID of the subnet that contains the IP address.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverendpoint-ipaddressrequest.html#cfn-route53resolver-resolverendpoint-ipaddressrequest-subnetid
            '''
            result = self._values.get("subnet_id")
            assert result is not None, "Required property 'subnet_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def ip(self) -> typing.Optional[builtins.str]:
            '''The IP address that you want to use for DNS queries.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverendpoint-ipaddressrequest.html#cfn-route53resolver-resolverendpoint-ipaddressrequest-ip
            '''
            result = self._values.get("ip")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IpAddressRequestProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.CfnResolverEndpointProps",
    jsii_struct_bases=[],
    name_mapping={
        "direction": "direction",
        "ip_addresses": "ipAddresses",
        "security_group_ids": "securityGroupIds",
        "name": "name",
        "outpost_arn": "outpostArn",
        "preferred_instance_type": "preferredInstanceType",
        "tags": "tags",
    },
)
class CfnResolverEndpointProps:
    def __init__(
        self,
        *,
        direction: builtins.str,
        ip_addresses: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnResolverEndpoint.IpAddressRequestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        security_group_ids: typing.Sequence[builtins.str],
        name: typing.Optional[builtins.str] = None,
        outpost_arn: typing.Optional[builtins.str] = None,
        preferred_instance_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnResolverEndpoint``.

        :param direction: Indicates whether the Resolver endpoint allows inbound or outbound DNS queries:. - ``INBOUND`` : allows DNS queries to your VPC from your network - ``OUTBOUND`` : allows DNS queries from your VPC to your network
        :param ip_addresses: The subnets and IP addresses in your VPC that DNS queries originate from (for outbound endpoints) or that you forward DNS queries to (for inbound endpoints). The subnet ID uniquely identifies a VPC.
        :param security_group_ids: The ID of one or more security groups that control access to this VPC. The security group must include one or more inbound rules (for inbound endpoints) or outbound rules (for outbound endpoints). Inbound and outbound rules must allow TCP and UDP access. For inbound access, open port 53. For outbound access, open the port that you're using for DNS queries on your network.
        :param name: A friendly name that lets you easily find a configuration in the Resolver dashboard in the Route 53 console.
        :param outpost_arn: ``AWS::Route53Resolver::ResolverEndpoint.OutpostArn``.
        :param preferred_instance_type: ``AWS::Route53Resolver::ResolverEndpoint.PreferredInstanceType``.
        :param tags: Route 53 Resolver doesn't support updating tags through CloudFormation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_route53resolver as route53resolver
            
            cfn_resolver_endpoint_props = route53resolver.CfnResolverEndpointProps(
                direction="direction",
                ip_addresses=[route53resolver.CfnResolverEndpoint.IpAddressRequestProperty(
                    subnet_id="subnetId",
            
                    # the properties below are optional
                    ip="ip"
                )],
                security_group_ids=["securityGroupIds"],
            
                # the properties below are optional
                name="name",
                outpost_arn="outpostArn",
                preferred_instance_type="preferredInstanceType",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac531b5b2285ee1456c4c3977661ff80c0069882f3bc23903c8d51cdd5d04ef4)
            check_type(argname="argument direction", value=direction, expected_type=type_hints["direction"])
            check_type(argname="argument ip_addresses", value=ip_addresses, expected_type=type_hints["ip_addresses"])
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument outpost_arn", value=outpost_arn, expected_type=type_hints["outpost_arn"])
            check_type(argname="argument preferred_instance_type", value=preferred_instance_type, expected_type=type_hints["preferred_instance_type"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "direction": direction,
            "ip_addresses": ip_addresses,
            "security_group_ids": security_group_ids,
        }
        if name is not None:
            self._values["name"] = name
        if outpost_arn is not None:
            self._values["outpost_arn"] = outpost_arn
        if preferred_instance_type is not None:
            self._values["preferred_instance_type"] = preferred_instance_type
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def direction(self) -> builtins.str:
        '''Indicates whether the Resolver endpoint allows inbound or outbound DNS queries:.

        - ``INBOUND`` : allows DNS queries to your VPC from your network
        - ``OUTBOUND`` : allows DNS queries from your VPC to your network

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-direction
        '''
        result = self._values.get("direction")
        assert result is not None, "Required property 'direction' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ip_addresses(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnResolverEndpoint.IpAddressRequestProperty, _IResolvable_a771d0ef]]]:
        '''The subnets and IP addresses in your VPC that DNS queries originate from (for outbound endpoints) or that you forward DNS queries to (for inbound endpoints).

        The subnet ID uniquely identifies a VPC.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-ipaddresses
        '''
        result = self._values.get("ip_addresses")
        assert result is not None, "Required property 'ip_addresses' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnResolverEndpoint.IpAddressRequestProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def security_group_ids(self) -> typing.List[builtins.str]:
        '''The ID of one or more security groups that control access to this VPC.

        The security group must include one or more inbound rules (for inbound endpoints) or outbound rules (for outbound endpoints). Inbound and outbound rules must allow TCP and UDP access. For inbound access, open port 53. For outbound access, open the port that you're using for DNS queries on your network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        assert result is not None, "Required property 'security_group_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A friendly name that lets you easily find a configuration in the Resolver dashboard in the Route 53 console.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def outpost_arn(self) -> typing.Optional[builtins.str]:
        '''``AWS::Route53Resolver::ResolverEndpoint.OutpostArn``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-outpostarn
        '''
        result = self._values.get("outpost_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def preferred_instance_type(self) -> typing.Optional[builtins.str]:
        '''``AWS::Route53Resolver::ResolverEndpoint.PreferredInstanceType``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-preferredinstancetype
        '''
        result = self._values.get("preferred_instance_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Route 53 Resolver doesn't support updating tags through CloudFormation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResolverQueryLoggingConfig(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.CfnResolverQueryLoggingConfig",
):
    '''A CloudFormation ``AWS::Route53Resolver::ResolverQueryLoggingConfig``.

    The AWS::Route53Resolver::ResolverQueryLoggingConfig resource is a complex type that contains settings for one query logging configuration.

    :cloudformationResource: AWS::Route53Resolver::ResolverQueryLoggingConfig
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53resolver as route53resolver
        
        cfn_resolver_query_logging_config = route53resolver.CfnResolverQueryLoggingConfig(self, "MyCfnResolverQueryLoggingConfig",
            destination_arn="destinationArn",
            name="name"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        destination_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Route53Resolver::ResolverQueryLoggingConfig``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_arn: The ARN of the resource that you want Resolver to send query logs: an Amazon S3 bucket, a CloudWatch Logs log group, or a Kinesis Data Firehose delivery stream.
        :param name: The name of the query logging configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2368f767a41dc1501536d9082acec35144578d8deaaf7b6c35956046f30c5df7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResolverQueryLoggingConfigProps(
            destination_arn=destination_arn, name=name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56c3aba8d5940b75b97df4348cacbc3e2a8a987b671e4dba5f9b44e4d36c43e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85e175feaf01e3cf9a1ee688fe03ed1c02e68f787000d092b39b85c930c7169b)
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
        '''The Amazon Resource Name (ARN) for the query logging configuration.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrAssociationCount")
    def attr_association_count(self) -> jsii.Number:
        '''The number of VPCs that are associated with the query logging configuration.

        :cloudformationAttribute: AssociationCount
        '''
        return typing.cast(jsii.Number, jsii.get(self, "attrAssociationCount"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''The date and time that the query logging configuration was created, in Unix time format and Coordinated Universal Time (UTC).

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatorRequestId")
    def attr_creator_request_id(self) -> builtins.str:
        '''A unique string that identifies the request that created the query logging configuration.

        The ``CreatorRequestId`` allows failed requests to be retried without the risk of running the operation twice.

        :cloudformationAttribute: CreatorRequestId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatorRequestId"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID for the query logging configuration.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrOwnerId")
    def attr_owner_id(self) -> builtins.str:
        '''The AWS account ID for the account that created the query logging configuration.

        :cloudformationAttribute: OwnerId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrOwnerId"))

    @builtins.property
    @jsii.member(jsii_name="attrShareStatus")
    def attr_share_status(self) -> builtins.str:
        '''An indication of whether the query logging configuration is shared with other AWS account s, or was shared with the current account by another AWS account .

        Sharing is configured through AWS Resource Access Manager ( AWS RAM ).

        :cloudformationAttribute: ShareStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrShareStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the specified query logging configuration. Valid values include the following:.

        - ``CREATING`` : Resolver is creating the query logging configuration.
        - ``CREATED`` : The query logging configuration was successfully created. Resolver is logging queries that originate in the specified VPC.
        - ``DELETING`` : Resolver is deleting this query logging configuration.
        - ``FAILED`` : Resolver can't deliver logs to the location that is specified in the query logging configuration. Here are two common causes:
        - The specified destination (for example, an Amazon S3 bucket) was deleted.
        - Permissions don't allow sending logs to the destination.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the resource that you want Resolver to send query logs: an Amazon S3 bucket, a CloudWatch Logs log group, or a Kinesis Data Firehose delivery stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html#cfn-route53resolver-resolverqueryloggingconfig-destinationarn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "destinationArn"))

    @destination_arn.setter
    def destination_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d69e601e14e6db6d199253c056d9bef60f86ae3b1b8f611451a8b98d41f97df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationArn", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the query logging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html#cfn-route53resolver-resolverqueryloggingconfig-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e506a6a41618bfb76c7c4cba8da850d90017114a2ac53fba677812e5a5d1a386)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.implements(_IInspectable_82c04a63)
class CfnResolverQueryLoggingConfigAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.CfnResolverQueryLoggingConfigAssociation",
):
    '''A CloudFormation ``AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation``.

    The AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation resource is a configuration for DNS query logging. After you create a query logging configuration, Amazon Route 53 begins to publish log data to an Amazon CloudWatch Logs log group.

    :cloudformationResource: AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfigassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53resolver as route53resolver
        
        cfn_resolver_query_logging_config_association = route53resolver.CfnResolverQueryLoggingConfigAssociation(self, "MyCfnResolverQueryLoggingConfigAssociation",
            resolver_query_log_config_id="resolverQueryLogConfigId",
            resource_id="resourceId"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        resolver_query_log_config_id: typing.Optional[builtins.str] = None,
        resource_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resolver_query_log_config_id: The ID of the query logging configuration that a VPC is associated with.
        :param resource_id: The ID of the Amazon VPC that is associated with the query logging configuration.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcaa961b5d089a5e914faeb3afcfa59c3325b63c718ad249b5852121418ad05f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResolverQueryLoggingConfigAssociationProps(
            resolver_query_log_config_id=resolver_query_log_config_id,
            resource_id=resource_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99d62f043fb8921187c3aa88146e6a087fd08b4a2f65401e1783daed1f29e4fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__949fbd99378095652a7a493973ab4d8c64b1d536e9922a8e672878aa58187a83)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrCreationTime")
    def attr_creation_time(self) -> builtins.str:
        '''The date and time that the VPC was associated with the query logging configuration, in Unix time format and Coordinated Universal Time (UTC).

        :cloudformationAttribute: CreationTime
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="attrError")
    def attr_error(self) -> builtins.str:
        '''If the value of ``Status`` is ``FAILED`` , the value of ``Error`` indicates the cause:.

        - ``DESTINATION_NOT_FOUND`` : The specified destination (for example, an Amazon S3 bucket) was deleted.
        - ``ACCESS_DENIED`` : Permissions don't allow sending logs to the destination.

        If the value of ``Status`` is a value other than ``FAILED`` , ``Error`` is null.

        :cloudformationAttribute: Error
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrError"))

    @builtins.property
    @jsii.member(jsii_name="attrErrorMessage")
    def attr_error_message(self) -> builtins.str:
        '''Contains additional information about the error.

        If the value or ``Error`` is null, the value of ``ErrorMessage`` is also null.

        :cloudformationAttribute: ErrorMessage
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrErrorMessage"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the query logging association.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the specified query logging association. Valid values include the following:.

        - ``CREATING`` : Resolver is creating an association between an Amazon Virtual Private Cloud (Amazon VPC) and a query logging configuration.
        - ``CREATED`` : The association between an Amazon VPC and a query logging configuration was successfully created. Resolver is logging queries that originate in the specified VPC.
        - ``DELETING`` : Resolver is deleting this query logging association.
        - ``FAILED`` : Resolver either couldn't create or couldn't delete the query logging association.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="resolverQueryLogConfigId")
    def resolver_query_log_config_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the query logging configuration that a VPC is associated with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfigassociation.html#cfn-route53resolver-resolverqueryloggingconfigassociation-resolverquerylogconfigid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resolverQueryLogConfigId"))

    @resolver_query_log_config_id.setter
    def resolver_query_log_config_id(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1924b876c5da76ed19b2faa3dca19ea7f3884fb2af435f2834a21c0cc2c08a25)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolverQueryLogConfigId", value)

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Amazon VPC that is associated with the query logging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfigassociation.html#cfn-route53resolver-resolverqueryloggingconfigassociation-resourceid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceId"))

    @resource_id.setter
    def resource_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecd51c3f59cb73dcc7011a5e959f0ec8956fe097742fc4fafa9d79eee8e76a88)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceId", value)


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.CfnResolverQueryLoggingConfigAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "resolver_query_log_config_id": "resolverQueryLogConfigId",
        "resource_id": "resourceId",
    },
)
class CfnResolverQueryLoggingConfigAssociationProps:
    def __init__(
        self,
        *,
        resolver_query_log_config_id: typing.Optional[builtins.str] = None,
        resource_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnResolverQueryLoggingConfigAssociation``.

        :param resolver_query_log_config_id: The ID of the query logging configuration that a VPC is associated with.
        :param resource_id: The ID of the Amazon VPC that is associated with the query logging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfigassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_route53resolver as route53resolver
            
            cfn_resolver_query_logging_config_association_props = route53resolver.CfnResolverQueryLoggingConfigAssociationProps(
                resolver_query_log_config_id="resolverQueryLogConfigId",
                resource_id="resourceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8911be334a0a764b72a0f0c7c75a1cbe88d002cd63570e106671517b4015fcd2)
            check_type(argname="argument resolver_query_log_config_id", value=resolver_query_log_config_id, expected_type=type_hints["resolver_query_log_config_id"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if resolver_query_log_config_id is not None:
            self._values["resolver_query_log_config_id"] = resolver_query_log_config_id
        if resource_id is not None:
            self._values["resource_id"] = resource_id

    @builtins.property
    def resolver_query_log_config_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the query logging configuration that a VPC is associated with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfigassociation.html#cfn-route53resolver-resolverqueryloggingconfigassociation-resolverquerylogconfigid
        '''
        result = self._values.get("resolver_query_log_config_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the Amazon VPC that is associated with the query logging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfigassociation.html#cfn-route53resolver-resolverqueryloggingconfigassociation-resourceid
        '''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverQueryLoggingConfigAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.CfnResolverQueryLoggingConfigProps",
    jsii_struct_bases=[],
    name_mapping={"destination_arn": "destinationArn", "name": "name"},
)
class CfnResolverQueryLoggingConfigProps:
    def __init__(
        self,
        *,
        destination_arn: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnResolverQueryLoggingConfig``.

        :param destination_arn: The ARN of the resource that you want Resolver to send query logs: an Amazon S3 bucket, a CloudWatch Logs log group, or a Kinesis Data Firehose delivery stream.
        :param name: The name of the query logging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_route53resolver as route53resolver
            
            cfn_resolver_query_logging_config_props = route53resolver.CfnResolverQueryLoggingConfigProps(
                destination_arn="destinationArn",
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__157537cc151e371ffa6dd12360f861fd41a5d3d7521ad9b9bf53d9930a32f026)
            check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if destination_arn is not None:
            self._values["destination_arn"] = destination_arn
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def destination_arn(self) -> typing.Optional[builtins.str]:
        '''The ARN of the resource that you want Resolver to send query logs: an Amazon S3 bucket, a CloudWatch Logs log group, or a Kinesis Data Firehose delivery stream.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html#cfn-route53resolver-resolverqueryloggingconfig-destinationarn
        '''
        result = self._values.get("destination_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the query logging configuration.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html#cfn-route53resolver-resolverqueryloggingconfig-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverQueryLoggingConfigProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnResolverRule(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.CfnResolverRule",
):
    '''A CloudFormation ``AWS::Route53Resolver::ResolverRule``.

    For DNS queries that originate in your VPCs, specifies which Resolver endpoint the queries pass through, one domain name that you want to forward to your network, and the IP addresses of the DNS resolvers in your network.

    :cloudformationResource: AWS::Route53Resolver::ResolverRule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53resolver as route53resolver
        
        cfn_resolver_rule = route53resolver.CfnResolverRule(self, "MyCfnResolverRule",
            domain_name="domainName",
            rule_type="ruleType",
        
            # the properties below are optional
            name="name",
            resolver_endpoint_id="resolverEndpointId",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            target_ips=[route53resolver.CfnResolverRule.TargetAddressProperty(
                ip="ip",
        
                # the properties below are optional
                port="port"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        domain_name: builtins.str,
        rule_type: builtins.str,
        name: typing.Optional[builtins.str] = None,
        resolver_endpoint_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_ips: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnResolverRule.TargetAddressProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53Resolver::ResolverRule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param domain_name: DNS queries for this domain name are forwarded to the IP addresses that are specified in ``TargetIps`` . If a query matches multiple Resolver rules (example.com and www.example.com), the query is routed using the Resolver rule that contains the most specific domain name (www.example.com).
        :param rule_type: When you want to forward DNS queries for specified domain name to resolvers on your network, specify ``FORWARD`` . When you have a forwarding rule to forward DNS queries for a domain to your network and you want Resolver to process queries for a subdomain of that domain, specify ``SYSTEM`` . For example, to forward DNS queries for example.com to resolvers on your network, you create a rule and specify ``FORWARD`` for ``RuleType`` . To then have Resolver process queries for apex.example.com, you create a rule and specify ``SYSTEM`` for ``RuleType`` . Currently, only Resolver can create rules that have a value of ``RECURSIVE`` for ``RuleType`` .
        :param name: The name for the Resolver rule, which you specified when you created the Resolver rule.
        :param resolver_endpoint_id: The ID of the endpoint that the rule is associated with.
        :param tags: Route 53 Resolver doesn't support updating tags through CloudFormation.
        :param target_ips: An array that contains the IP addresses and ports that an outbound endpoint forwards DNS queries to. Typically, these are the IP addresses of DNS resolvers on your network. Specify IPv4 addresses. IPv6 is not supported.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cc486e7bf2b5d6a4bbbd25a103cf389949ba3a68d29d1b087e7773e8831a865)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResolverRuleProps(
            domain_name=domain_name,
            rule_type=rule_type,
            name=name,
            resolver_endpoint_id=resolver_endpoint_id,
            tags=tags,
            target_ips=target_ips,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f9d84504f87cf1bd65dbdb82ed1825b4a209864fe6fe343a56dd098d39b404)
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
            type_hints = typing.get_type_hints(_typecheckingstub__438262d90f3f5c3e8973d645cd7cee74cbd9a36163f25d2289ad3e5005ba33fe)
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
        '''The Amazon Resource Name (ARN) of the resolver rule, such as ``arn:aws:route53resolver:us-east-1:123456789012:resolver-rule/resolver-rule-a1bzhi`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainName")
    def attr_domain_name(self) -> builtins.str:
        '''DNS queries for this domain name are forwarded to the IP addresses that are specified in TargetIps.

        If a query matches multiple resolver rules (example.com and www.example.com), the query is routed using the resolver rule that contains the most specific domain name (www.example.com).

        :cloudformationAttribute: DomainName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDomainName"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''A friendly name that lets you easily find a rule in the Resolver dashboard in the Route 53 console.

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="attrResolverEndpointId")
    def attr_resolver_endpoint_id(self) -> builtins.str:
        '''The ID of the outbound endpoint that the rule is associated with, such as ``rslvr-out-fdc049932dexample`` .

        :cloudformationAttribute: ResolverEndpointId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResolverEndpointId"))

    @builtins.property
    @jsii.member(jsii_name="attrResolverRuleId")
    def attr_resolver_rule_id(self) -> builtins.str:
        '''When the value of ``RuleType`` is ``FORWARD`` , the ID that Resolver assigned to the resolver rule when you created it, such as ``rslvr-rr-5328a0899aexample`` .

        This value isn't applicable when ``RuleType`` is ``SYSTEM`` .

        :cloudformationAttribute: ResolverRuleId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResolverRuleId"))

    @builtins.property
    @jsii.member(jsii_name="attrTargetIps")
    def attr_target_ips(self) -> _IResolvable_a771d0ef:
        '''When the value of ``RuleType`` is ``FORWARD`` , the IP addresses that the outbound endpoint forwards DNS queries to, typically the IP addresses for DNS resolvers on your network.

        This value isn't applicable when ``RuleType`` is ``SYSTEM`` .

        :cloudformationAttribute: TargetIps
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrTargetIps"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''Route 53 Resolver doesn't support updating tags through CloudFormation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''DNS queries for this domain name are forwarded to the IP addresses that are specified in ``TargetIps`` .

        If a query matches multiple Resolver rules (example.com and www.example.com), the query is routed using the Resolver rule that contains the most specific domain name (www.example.com).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-domainname
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54a3110bf5b0c63a2e542c7870cebb6c9bc04f035a883ff0729ee50b4e4bb219)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="ruleType")
    def rule_type(self) -> builtins.str:
        '''When you want to forward DNS queries for specified domain name to resolvers on your network, specify ``FORWARD`` .

        When you have a forwarding rule to forward DNS queries for a domain to your network and you want Resolver to process queries for a subdomain of that domain, specify ``SYSTEM`` .

        For example, to forward DNS queries for example.com to resolvers on your network, you create a rule and specify ``FORWARD`` for ``RuleType`` . To then have Resolver process queries for apex.example.com, you create a rule and specify ``SYSTEM`` for ``RuleType`` .

        Currently, only Resolver can create rules that have a value of ``RECURSIVE`` for ``RuleType`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-ruletype
        '''
        return typing.cast(builtins.str, jsii.get(self, "ruleType"))

    @rule_type.setter
    def rule_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9dc2109cb5e3e425ada0e0603ede5bdc5876141c63596a803c1c1357eb7627e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ruleType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the Resolver rule, which you specified when you created the Resolver rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3a8da420a1f7dfd333cc40a5ad40ff6191331905602d40f0a8156e90a607c02)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resolverEndpointId")
    def resolver_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the endpoint that the rule is associated with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-resolverendpointid
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resolverEndpointId"))

    @resolver_endpoint_id.setter
    def resolver_endpoint_id(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60f58e6a3a317c6541832c7ad6f9860ff25d2db07af88732fc449d644761048b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolverEndpointId", value)

    @builtins.property
    @jsii.member(jsii_name="targetIps")
    def target_ips(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnResolverRule.TargetAddressProperty", _IResolvable_a771d0ef]]]]:
        '''An array that contains the IP addresses and ports that an outbound endpoint forwards DNS queries to.

        Typically, these are the IP addresses of DNS resolvers on your network. Specify IPv4 addresses. IPv6 is not supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-targetips
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnResolverRule.TargetAddressProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "targetIps"))

    @target_ips.setter
    def target_ips(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnResolverRule.TargetAddressProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf23755701aaa60b6c4a30c38ec027835e23e2f863d2be9b9aec7d2510fc0dc8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetIps", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_route53resolver.CfnResolverRule.TargetAddressProperty",
        jsii_struct_bases=[],
        name_mapping={"ip": "ip", "port": "port"},
    )
    class TargetAddressProperty:
        def __init__(
            self,
            *,
            ip: builtins.str,
            port: typing.Optional[builtins.str] = None,
        ) -> None:
            '''In a `CreateResolverRule <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_CreateResolverRule.html>`_ request, an array of the IPs that you want to forward DNS queries to.

            :param ip: One IP address that you want to forward DNS queries to. You can specify only IPv4 addresses.
            :param port: The port at ``Ip`` that you want to forward DNS queries to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverrule-targetaddress.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_route53resolver as route53resolver
                
                target_address_property = route53resolver.CfnResolverRule.TargetAddressProperty(
                    ip="ip",
                
                    # the properties below are optional
                    port="port"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__6becb27622b48e0b972ec85239df0aaa90a0c469df4a79d37cbda23cd9ecd462)
                check_type(argname="argument ip", value=ip, expected_type=type_hints["ip"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "ip": ip,
            }
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def ip(self) -> builtins.str:
            '''One IP address that you want to forward DNS queries to.

            You can specify only IPv4 addresses.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverrule-targetaddress.html#cfn-route53resolver-resolverrule-targetaddress-ip
            '''
            result = self._values.get("ip")
            assert result is not None, "Required property 'ip' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def port(self) -> typing.Optional[builtins.str]:
            '''The port at ``Ip`` that you want to forward DNS queries to.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53resolver-resolverrule-targetaddress.html#cfn-route53resolver-resolverrule-targetaddress-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetAddressProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_IInspectable_82c04a63)
class CfnResolverRuleAssociation(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.CfnResolverRuleAssociation",
):
    '''A CloudFormation ``AWS::Route53Resolver::ResolverRuleAssociation``.

    In the response to an `AssociateResolverRule <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_AssociateResolverRule.html>`_ , `DisassociateResolverRule <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_DisassociateResolverRule.html>`_ , or `ListResolverRuleAssociations <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_ListResolverRuleAssociations.html>`_ request, provides information about an association between a resolver rule and a VPC. The association determines which DNS queries that originate in the VPC are forwarded to your network.

    :cloudformationResource: AWS::Route53Resolver::ResolverRuleAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_route53resolver as route53resolver
        
        cfn_resolver_rule_association = route53resolver.CfnResolverRuleAssociation(self, "MyCfnResolverRuleAssociation",
            resolver_rule_id="resolverRuleId",
            vpc_id="vpcId",
        
            # the properties below are optional
            name="name"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        resolver_rule_id: builtins.str,
        vpc_id: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::Route53Resolver::ResolverRuleAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param resolver_rule_id: The ID of the Resolver rule that you associated with the VPC that is specified by ``VPCId`` .
        :param vpc_id: The ID of the VPC that you associated the Resolver rule with.
        :param name: The name of an association between a Resolver rule and a VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f0ed968b2d4de5305338b6664e23d8c30ac9729836b4a3ed5f0884324568dff)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResolverRuleAssociationProps(
            resolver_rule_id=resolver_rule_id, vpc_id=vpc_id, name=name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be8d0499f1b1d1a16222cddb017b42bf3f111aa7d2e71ad46bad3864438531f2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d5c2a70e87b55aed22bd82e643a3f958720b7768412b1b250e796b33fe668f0)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrName")
    def attr_name(self) -> builtins.str:
        '''The name of an association between a resolver rule and a VPC, such as ``test.example.com in beta VPC`` .

        :cloudformationAttribute: Name
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrName"))

    @builtins.property
    @jsii.member(jsii_name="attrResolverRuleAssociationId")
    def attr_resolver_rule_association_id(self) -> builtins.str:
        '''The ID of the resolver rule association that you want to get information about, such as ``rslvr-rrassoc-97242eaf88example`` .

        :cloudformationAttribute: ResolverRuleAssociationId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResolverRuleAssociationId"))

    @builtins.property
    @jsii.member(jsii_name="attrResolverRuleId")
    def attr_resolver_rule_id(self) -> builtins.str:
        '''The ID of the resolver rule that you associated with the VPC that is specified by ``VPCId`` , such as ``rslvr-rr-5328a0899example`` .

        :cloudformationAttribute: ResolverRuleId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResolverRuleId"))

    @builtins.property
    @jsii.member(jsii_name="attrVpcId")
    def attr_vpc_id(self) -> builtins.str:
        '''The ID of the VPC that you associated the resolver rule with, such as ``vpc-03cf94c75cexample`` .

        :cloudformationAttribute: VPCId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVpcId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="resolverRuleId")
    def resolver_rule_id(self) -> builtins.str:
        '''The ID of the Resolver rule that you associated with the VPC that is specified by ``VPCId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html#cfn-route53resolver-resolverruleassociation-resolverruleid
        '''
        return typing.cast(builtins.str, jsii.get(self, "resolverRuleId"))

    @resolver_rule_id.setter
    def resolver_rule_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5a56b1c14ba23e7322de04dbf2839daa021bc0d14a3821a170af725b7ecde9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolverRuleId", value)

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        '''The ID of the VPC that you associated the Resolver rule with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html#cfn-route53resolver-resolverruleassociation-vpcid
        '''
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b89e366d47ece7eeaf0e1772d4aaedecbd90764c5fb6b7ce204b9d0fb104b8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of an association between a Resolver rule and a VPC.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html#cfn-route53resolver-resolverruleassociation-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2f36585defb7c13628c98741000a39161ed95bbf9294d84c14b034869bed7e9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.CfnResolverRuleAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "resolver_rule_id": "resolverRuleId",
        "vpc_id": "vpcId",
        "name": "name",
    },
)
class CfnResolverRuleAssociationProps:
    def __init__(
        self,
        *,
        resolver_rule_id: builtins.str,
        vpc_id: builtins.str,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnResolverRuleAssociation``.

        :param resolver_rule_id: The ID of the Resolver rule that you associated with the VPC that is specified by ``VPCId`` .
        :param vpc_id: The ID of the VPC that you associated the Resolver rule with.
        :param name: The name of an association between a Resolver rule and a VPC.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_route53resolver as route53resolver
            
            cfn_resolver_rule_association_props = route53resolver.CfnResolverRuleAssociationProps(
                resolver_rule_id="resolverRuleId",
                vpc_id="vpcId",
            
                # the properties below are optional
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c1ee181ebdff79af265cf644305f92d6bd3d6484761f88024c65bd75840e2cb)
            check_type(argname="argument resolver_rule_id", value=resolver_rule_id, expected_type=type_hints["resolver_rule_id"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resolver_rule_id": resolver_rule_id,
            "vpc_id": vpc_id,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def resolver_rule_id(self) -> builtins.str:
        '''The ID of the Resolver rule that you associated with the VPC that is specified by ``VPCId`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html#cfn-route53resolver-resolverruleassociation-resolverruleid
        '''
        result = self._values.get("resolver_rule_id")
        assert result is not None, "Required property 'resolver_rule_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''The ID of the VPC that you associated the Resolver rule with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html#cfn-route53resolver-resolverruleassociation-vpcid
        '''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of an association between a Resolver rule and a VPC.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html#cfn-route53resolver-resolverruleassociation-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverRuleAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.CfnResolverRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "rule_type": "ruleType",
        "name": "name",
        "resolver_endpoint_id": "resolverEndpointId",
        "tags": "tags",
        "target_ips": "targetIps",
    },
)
class CfnResolverRuleProps:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        rule_type: builtins.str,
        name: typing.Optional[builtins.str] = None,
        resolver_endpoint_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_ips: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnResolverRule.TargetAddressProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnResolverRule``.

        :param domain_name: DNS queries for this domain name are forwarded to the IP addresses that are specified in ``TargetIps`` . If a query matches multiple Resolver rules (example.com and www.example.com), the query is routed using the Resolver rule that contains the most specific domain name (www.example.com).
        :param rule_type: When you want to forward DNS queries for specified domain name to resolvers on your network, specify ``FORWARD`` . When you have a forwarding rule to forward DNS queries for a domain to your network and you want Resolver to process queries for a subdomain of that domain, specify ``SYSTEM`` . For example, to forward DNS queries for example.com to resolvers on your network, you create a rule and specify ``FORWARD`` for ``RuleType`` . To then have Resolver process queries for apex.example.com, you create a rule and specify ``SYSTEM`` for ``RuleType`` . Currently, only Resolver can create rules that have a value of ``RECURSIVE`` for ``RuleType`` .
        :param name: The name for the Resolver rule, which you specified when you created the Resolver rule.
        :param resolver_endpoint_id: The ID of the endpoint that the rule is associated with.
        :param tags: Route 53 Resolver doesn't support updating tags through CloudFormation.
        :param target_ips: An array that contains the IP addresses and ports that an outbound endpoint forwards DNS queries to. Typically, these are the IP addresses of DNS resolvers on your network. Specify IPv4 addresses. IPv6 is not supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_route53resolver as route53resolver
            
            cfn_resolver_rule_props = route53resolver.CfnResolverRuleProps(
                domain_name="domainName",
                rule_type="ruleType",
            
                # the properties below are optional
                name="name",
                resolver_endpoint_id="resolverEndpointId",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                target_ips=[route53resolver.CfnResolverRule.TargetAddressProperty(
                    ip="ip",
            
                    # the properties below are optional
                    port="port"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e94dd61877e2550e1b24254b836d4a7978319d65907f9744de6324fd06b9194f)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument rule_type", value=rule_type, expected_type=type_hints["rule_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resolver_endpoint_id", value=resolver_endpoint_id, expected_type=type_hints["resolver_endpoint_id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument target_ips", value=target_ips, expected_type=type_hints["target_ips"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
            "rule_type": rule_type,
        }
        if name is not None:
            self._values["name"] = name
        if resolver_endpoint_id is not None:
            self._values["resolver_endpoint_id"] = resolver_endpoint_id
        if tags is not None:
            self._values["tags"] = tags
        if target_ips is not None:
            self._values["target_ips"] = target_ips

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''DNS queries for this domain name are forwarded to the IP addresses that are specified in ``TargetIps`` .

        If a query matches multiple Resolver rules (example.com and www.example.com), the query is routed using the Resolver rule that contains the most specific domain name (www.example.com).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-domainname
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def rule_type(self) -> builtins.str:
        '''When you want to forward DNS queries for specified domain name to resolvers on your network, specify ``FORWARD`` .

        When you have a forwarding rule to forward DNS queries for a domain to your network and you want Resolver to process queries for a subdomain of that domain, specify ``SYSTEM`` .

        For example, to forward DNS queries for example.com to resolvers on your network, you create a rule and specify ``FORWARD`` for ``RuleType`` . To then have Resolver process queries for apex.example.com, you create a rule and specify ``SYSTEM`` for ``RuleType`` .

        Currently, only Resolver can create rules that have a value of ``RECURSIVE`` for ``RuleType`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-ruletype
        '''
        result = self._values.get("rule_type")
        assert result is not None, "Required property 'rule_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name for the Resolver rule, which you specified when you created the Resolver rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resolver_endpoint_id(self) -> typing.Optional[builtins.str]:
        '''The ID of the endpoint that the rule is associated with.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-resolverendpointid
        '''
        result = self._values.get("resolver_endpoint_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''Route 53 Resolver doesn't support updating tags through CloudFormation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def target_ips(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnResolverRule.TargetAddressProperty, _IResolvable_a771d0ef]]]]:
        '''An array that contains the IP addresses and ports that an outbound endpoint forwards DNS queries to.

        Typically, these are the IP addresses of DNS resolvers on your network. Specify IPv4 addresses. IPv6 is not supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-targetips
        '''
        result = self._values.get("target_ips")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnResolverRule.TargetAddressProperty, _IResolvable_a771d0ef]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DnsBlockResponse(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_route53resolver.DnsBlockResponse",
):
    '''(experimental) The way that you want DNS Firewall to block the request.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_block_list: route53resolver.FirewallDomainList
        # rule_group: route53resolver.FirewallRuleGroup
        
        
        rule_group.add_rule(
            priority=10,
            firewall_domain_list=my_block_list,
            # block and reply with NXDOMAIN
            action=route53resolver.FirewallRuleAction.block(route53resolver.DnsBlockResponse.nx_domain())
        )
        
        rule_group.add_rule(
            priority=20,
            firewall_domain_list=my_block_list,
            # block and override DNS response with a custom domain
            action=route53resolver.FirewallRuleAction.block(route53resolver.DnsBlockResponse.override("amazon.com"))
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="noData")
    @builtins.classmethod
    def no_data(cls) -> "DnsBlockResponse":
        '''(experimental) Respond indicating that the query was successful, but no response is available for it.

        :stability: experimental
        '''
        return typing.cast("DnsBlockResponse", jsii.sinvoke(cls, "noData", []))

    @jsii.member(jsii_name="nxDomain")
    @builtins.classmethod
    def nx_domain(cls) -> "DnsBlockResponse":
        '''(experimental) Respond indicating that the domain name that's in the query doesn't exist.

        :stability: experimental
        '''
        return typing.cast("DnsBlockResponse", jsii.sinvoke(cls, "nxDomain", []))

    @jsii.member(jsii_name="override")
    @builtins.classmethod
    def override(
        cls,
        domain: builtins.str,
        ttl: typing.Optional[_Duration_070aa057] = None,
    ) -> "DnsBlockResponse":
        '''(experimental) Provides a custom override response to the query.

        :param domain: The custom DNS record to send back in response to the query.
        :param ttl: The recommended amount of time for the DNS resolver or web browser to cache the provided override record.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09872892c6856e53f75d075e85d9d716b850fcbb9744c0c6bc246f39f0c643a5)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        return typing.cast("DnsBlockResponse", jsii.sinvoke(cls, "override", [domain, ttl]))

    @builtins.property
    @jsii.member(jsii_name="blockOverrideDnsType")
    @abc.abstractmethod
    def block_override_dns_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) The DNS record's type.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="blockOverrideDomain")
    @abc.abstractmethod
    def block_override_domain(self) -> typing.Optional[builtins.str]:
        '''(experimental) The custom DNS record to send back in response to the query.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="blockOverrideTtl")
    @abc.abstractmethod
    def block_override_ttl(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The recommended amount of time for the DNS resolver or web browser to cache the provided override record.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="blockResponse")
    @abc.abstractmethod
    def block_response(self) -> typing.Optional[builtins.str]:
        '''(experimental) The way that you want DNS Firewall to block the request.

        :stability: experimental
        '''
        ...


class _DnsBlockResponseProxy(DnsBlockResponse):
    @builtins.property
    @jsii.member(jsii_name="blockOverrideDnsType")
    def block_override_dns_type(self) -> typing.Optional[builtins.str]:
        '''(experimental) The DNS record's type.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockOverrideDnsType"))

    @builtins.property
    @jsii.member(jsii_name="blockOverrideDomain")
    def block_override_domain(self) -> typing.Optional[builtins.str]:
        '''(experimental) The custom DNS record to send back in response to the query.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockOverrideDomain"))

    @builtins.property
    @jsii.member(jsii_name="blockOverrideTtl")
    def block_override_ttl(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The recommended amount of time for the DNS resolver or web browser to cache the provided override record.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_Duration_070aa057], jsii.get(self, "blockOverrideTtl"))

    @builtins.property
    @jsii.member(jsii_name="blockResponse")
    def block_response(self) -> typing.Optional[builtins.str]:
        '''(experimental) The way that you want DNS Firewall to block the request.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "blockResponse"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, DnsBlockResponse).__jsii_proxy_class__ = lambda : _DnsBlockResponseProxy


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.DomainsConfig",
    jsii_struct_bases=[],
    name_mapping={"domain_file_url": "domainFileUrl", "domains": "domains"},
)
class DomainsConfig:
    def __init__(
        self,
        *,
        domain_file_url: typing.Optional[builtins.str] = None,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Domains configuration.

        :param domain_file_url: (experimental) The fully qualified URL or URI of the file stored in Amazon S3 that contains the list of domains to import. The file must be a text file and must contain a single domain per line. The content type of the S3 object must be ``plain/text``. Default: - use ``domains``
        :param domains: (experimental) A list of domains. Default: - use ``domainFileUrl``

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_route53resolver as route53resolver
            
            domains_config = route53resolver.DomainsConfig(
                domain_file_url="domainFileUrl",
                domains=["domains"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__52b1a1a0c9263618951f23d6b235ea2b391517272efc2e35fb8e9fc5b4deaea2)
            check_type(argname="argument domain_file_url", value=domain_file_url, expected_type=type_hints["domain_file_url"])
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if domain_file_url is not None:
            self._values["domain_file_url"] = domain_file_url
        if domains is not None:
            self._values["domains"] = domains

    @builtins.property
    def domain_file_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The fully qualified URL or URI of the file stored in Amazon S3 that contains the list of domains to import.

        The file must be a text file and must contain
        a single domain per line. The content type of the S3 object must be ``plain/text``.

        :default: - use ``domains``

        :stability: experimental
        '''
        result = self._values.get("domain_file_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def domains(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of domains.

        :default: - use ``domainFileUrl``

        :stability: experimental
        '''
        result = self._values.get("domains")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainsConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.FirewallDomainListProps",
    jsii_struct_bases=[],
    name_mapping={"domains": "domains", "name": "name"},
)
class FirewallDomainListProps:
    def __init__(
        self,
        *,
        domains: "FirewallDomains",
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a Firewall Domain List.

        :param domains: (experimental) A list of domains.
        :param name: (experimental) A name for the domain list. Default: - a CloudFormation generated name

        :stability: experimental
        :exampleMetadata: infused

        Example::

            block_list = route53resolver.FirewallDomainList(self, "BlockList",
                domains=route53resolver.FirewallDomains.from_list(["bad-domain.com", "bot-domain.net"])
            )
            
            s3_list = route53resolver.FirewallDomainList(self, "S3List",
                domains=route53resolver.FirewallDomains.from_s3_url("s3://bucket/prefix/object")
            )
            
            asset_list = route53resolver.FirewallDomainList(self, "AssetList",
                domains=route53resolver.FirewallDomains.from_asset("/path/to/domains.txt")
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__950fd0fc0371d1b204c7a8a11780a1d24ece068b5ad1b7ef98ff4ba5f7e8f8c3)
            check_type(argname="argument domains", value=domains, expected_type=type_hints["domains"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domains": domains,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def domains(self) -> "FirewallDomains":
        '''(experimental) A list of domains.

        :stability: experimental
        '''
        result = self._values.get("domains")
        assert result is not None, "Required property 'domains' is missing"
        return typing.cast("FirewallDomains", result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the domain list.

        :default: - a CloudFormation generated name

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallDomainListProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirewallDomains(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_route53resolver.FirewallDomains",
):
    '''(experimental) A list of domains.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        block_list = route53resolver.FirewallDomainList(self, "BlockList",
            domains=route53resolver.FirewallDomains.from_list(["bad-domain.com", "bot-domain.net"])
        )
        
        s3_list = route53resolver.FirewallDomainList(self, "S3List",
            domains=route53resolver.FirewallDomains.from_s3_url("s3://bucket/prefix/object")
        )
        
        asset_list = route53resolver.FirewallDomainList(self, "AssetList",
            domains=route53resolver.FirewallDomains.from_asset("/path/to/domains.txt")
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromAsset")
    @builtins.classmethod
    def from_asset(cls, asset_path: builtins.str) -> "FirewallDomains":
        '''(experimental) Firewall domains created from a local disk path to a text file.

        The file must be a text file (``.txt`` extension) and must contain a single
        domain per line. It will be uploaded to S3.

        :param asset_path: path to the text file.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43ec95f8223fd39c65da9e63c8961b662a2979239ad9a7f7caff4220e67da013)
            check_type(argname="argument asset_path", value=asset_path, expected_type=type_hints["asset_path"])
        return typing.cast("FirewallDomains", jsii.sinvoke(cls, "fromAsset", [asset_path]))

    @jsii.member(jsii_name="fromList")
    @builtins.classmethod
    def from_list(cls, list: typing.Sequence[builtins.str]) -> "FirewallDomains":
        '''(experimental) Firewall domains created from a list of domains.

        :param list: the list of domains.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc1791a138243917cbda6d5b5c78ef95acc86c4d5559f3a3db9538a7632b597a)
            check_type(argname="argument list", value=list, expected_type=type_hints["list"])
        return typing.cast("FirewallDomains", jsii.sinvoke(cls, "fromList", [list]))

    @jsii.member(jsii_name="fromS3")
    @builtins.classmethod
    def from_s3(cls, bucket: _IBucket_73486e29, key: builtins.str) -> "FirewallDomains":
        '''(experimental) Firewall domains created from a file stored in Amazon S3.

        The file must be a text file and must contain a single domain per line.
        The content type of the S3 object must be ``plain/text``.

        :param bucket: S3 bucket.
        :param key: S3 key.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__177e814ea37b4186f3201e85deaa8aca1a791acc995f8d3c42d3c696b9f9cd79)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
        return typing.cast("FirewallDomains", jsii.sinvoke(cls, "fromS3", [bucket, key]))

    @jsii.member(jsii_name="fromS3Url")
    @builtins.classmethod
    def from_s3_url(cls, url: builtins.str) -> "FirewallDomains":
        '''(experimental) Firewall domains created from the URL of a file stored in Amazon S3.

        The file must be a text file and must contain a single domain per line.
        The content type of the S3 object must be ``plain/text``.

        :param url: S3 bucket url (s3://bucket/prefix/objet).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ba938fd3eb594c9de4a7e5e9a2aac231658a3c283a92e59d82582fa8c99bef7)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        return typing.cast("FirewallDomains", jsii.sinvoke(cls, "fromS3Url", [url]))

    @jsii.member(jsii_name="bind")
    @abc.abstractmethod
    def bind(self, scope: _constructs_77d1e7e8.Construct) -> DomainsConfig:
        '''(experimental) Binds the domains to a domain list.

        :param scope: -

        :stability: experimental
        '''
        ...


class _FirewallDomainsProxy(FirewallDomains):
    @jsii.member(jsii_name="bind")
    def bind(self, scope: _constructs_77d1e7e8.Construct) -> DomainsConfig:
        '''(experimental) Binds the domains to a domain list.

        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bf61cbd69db53615a75a9fded1569910ec0510dd54ce6687eac495a70b0f2f0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(DomainsConfig, jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, FirewallDomains).__jsii_proxy_class__ = lambda : _FirewallDomainsProxy


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.FirewallRule",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "firewall_domain_list": "firewallDomainList",
        "priority": "priority",
    },
)
class FirewallRule:
    def __init__(
        self,
        *,
        action: "FirewallRuleAction",
        firewall_domain_list: "IFirewallDomainList",
        priority: jsii.Number,
    ) -> None:
        '''(experimental) A Firewall Rule.

        :param action: (experimental) The action for this rule.
        :param firewall_domain_list: (experimental) The domain list for this rule.
        :param priority: (experimental) The priority of the rule in the rule group. This value must be unique within the rule group.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # my_block_list: route53resolver.FirewallDomainList
            # rule_group: route53resolver.FirewallRuleGroup
            
            
            rule_group.add_rule(
                priority=10,
                firewall_domain_list=my_block_list,
                # block and reply with NXDOMAIN
                action=route53resolver.FirewallRuleAction.block(route53resolver.DnsBlockResponse.nx_domain())
            )
            
            rule_group.add_rule(
                priority=20,
                firewall_domain_list=my_block_list,
                # block and override DNS response with a custom domain
                action=route53resolver.FirewallRuleAction.block(route53resolver.DnsBlockResponse.override("amazon.com"))
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b9086409696b42f61714689b15e5b42a6f1025ceea93067a0e3a2fa9797aa485)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument firewall_domain_list", value=firewall_domain_list, expected_type=type_hints["firewall_domain_list"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "firewall_domain_list": firewall_domain_list,
            "priority": priority,
        }

    @builtins.property
    def action(self) -> "FirewallRuleAction":
        '''(experimental) The action for this rule.

        :stability: experimental
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast("FirewallRuleAction", result)

    @builtins.property
    def firewall_domain_list(self) -> "IFirewallDomainList":
        '''(experimental) The domain list for this rule.

        :stability: experimental
        '''
        result = self._values.get("firewall_domain_list")
        assert result is not None, "Required property 'firewall_domain_list' is missing"
        return typing.cast("IFirewallDomainList", result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''(experimental) The priority of the rule in the rule group.

        This value must be unique within
        the rule group.

        :stability: experimental
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class FirewallRuleAction(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_route53resolver.FirewallRuleAction",
):
    '''(experimental) A Firewall Rule.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_block_list: route53resolver.FirewallDomainList
        
        route53resolver.FirewallRuleGroup(self, "RuleGroup",
            rules=[route53resolver.aws_route53resolver.FirewallRule(
                priority=10,
                firewall_domain_list=my_block_list,
                # block and reply with NODATA
                action=route53resolver.FirewallRuleAction.block()
            )
            ]
        )
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="alert")
    @builtins.classmethod
    def alert(cls) -> "FirewallRuleAction":
        '''(experimental) Permit the request to go through but send an alert to the logs.

        :stability: experimental
        '''
        return typing.cast("FirewallRuleAction", jsii.sinvoke(cls, "alert", []))

    @jsii.member(jsii_name="allow")
    @builtins.classmethod
    def allow(cls) -> "FirewallRuleAction":
        '''(experimental) Permit the request to go through.

        :stability: experimental
        '''
        return typing.cast("FirewallRuleAction", jsii.sinvoke(cls, "allow", []))

    @jsii.member(jsii_name="block")
    @builtins.classmethod
    def block(
        cls,
        response: typing.Optional[DnsBlockResponse] = None,
    ) -> "FirewallRuleAction":
        '''(experimental) Disallow the request.

        :param response: The way that you want DNS Firewall to block the request.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cde4f65acd62f6ff12e0834f5e5f8f3ecf454bd9dda5d4838baa4f268857f659)
            check_type(argname="argument response", value=response, expected_type=type_hints["response"])
        return typing.cast("FirewallRuleAction", jsii.sinvoke(cls, "block", [response]))

    @builtins.property
    @jsii.member(jsii_name="action")
    @abc.abstractmethod
    def action(self) -> builtins.str:
        '''(experimental) The action that DNS Firewall should take on a DNS query when it matches one of the domains in the rule's domain list.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="blockResponse")
    @abc.abstractmethod
    def block_response(self) -> typing.Optional[DnsBlockResponse]:
        '''(experimental) The way that you want DNS Firewall to block the request.

        :stability: experimental
        '''
        ...


class _FirewallRuleActionProxy(FirewallRuleAction):
    @builtins.property
    @jsii.member(jsii_name="action")
    def action(self) -> builtins.str:
        '''(experimental) The action that DNS Firewall should take on a DNS query when it matches one of the domains in the rule's domain list.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="blockResponse")
    def block_response(self) -> typing.Optional[DnsBlockResponse]:
        '''(experimental) The way that you want DNS Firewall to block the request.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[DnsBlockResponse], jsii.get(self, "blockResponse"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, FirewallRuleAction).__jsii_proxy_class__ = lambda : _FirewallRuleActionProxy


class FirewallRuleGroupAssociation(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.FirewallRuleGroupAssociation",
):
    '''(experimental) A Firewall Rule Group Association.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_ec2 as ec2
        from monocdk import aws_route53resolver as route53resolver
        
        # firewall_rule_group: route53resolver.FirewallRuleGroup
        # vpc: ec2.Vpc
        
        firewall_rule_group_association = route53resolver.FirewallRuleGroupAssociation(self, "MyFirewallRuleGroupAssociation",
            firewall_rule_group=firewall_rule_group,
            priority=123,
            vpc=vpc,
        
            # the properties below are optional
            mutation_protection=False,
            name="name"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        firewall_rule_group: "IFirewallRuleGroup",
        priority: jsii.Number,
        vpc: _IVpc_6d1f76c4,
        mutation_protection: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param firewall_rule_group: (experimental) The firewall rule group which must be associated.
        :param priority: (experimental) The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC. DNS Firewall filters VPC traffic starting from rule group with the lowest numeric priority setting. This value must be greater than 100 and less than 9,000
        :param vpc: (experimental) The VPC that to associate with the rule group.
        :param mutation_protection: (experimental) If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections. Default: true
        :param name: (experimental) The name of the association. Default: - a CloudFormation generated name

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d33697555a04f173d2de57c6f42bd39bef2dd4f272930b8c871fc9ff978805fe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FirewallRuleGroupAssociationProps(
            firewall_rule_group=firewall_rule_group,
            priority=priority,
            vpc=vpc,
            mutation_protection=mutation_protection,
            name=name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupAssociationArn")
    def firewall_rule_group_association_arn(self) -> builtins.str:
        '''(experimental) The ARN (Amazon Resource Name) of the association.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupAssociationArn"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupAssociationCreationTime")
    def firewall_rule_group_association_creation_time(self) -> builtins.str:
        '''(experimental) The date and time that the association was created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupAssociationCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupAssociationCreatorRequestId")
    def firewall_rule_group_association_creator_request_id(self) -> builtins.str:
        '''(experimental) The creator request ID.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupAssociationCreatorRequestId"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupAssociationId")
    def firewall_rule_group_association_id(self) -> builtins.str:
        '''(experimental) The ID of the association.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupAssociationId"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupAssociationManagedOwnerName")
    def firewall_rule_group_association_managed_owner_name(self) -> builtins.str:
        '''(experimental) The owner of the association, used only for lists that are not managed by you.

        If you use AWS Firewall Manager to manage your firewallls from DNS Firewall,
        then this reports Firewall Manager as the managed owner.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupAssociationManagedOwnerName"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupAssociationModificationTime")
    def firewall_rule_group_association_modification_time(self) -> builtins.str:
        '''(experimental) The date and time that the association was last modified.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupAssociationModificationTime"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupAssociationStatus")
    def firewall_rule_group_association_status(self) -> builtins.str:
        '''(experimental) The status of the association.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupAssociationStatus"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupAssociationStatusMessage")
    def firewall_rule_group_association_status_message(self) -> builtins.str:
        '''(experimental) Additional information about the status of the association.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupAssociationStatusMessage"))


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.FirewallRuleGroupAssociationOptions",
    jsii_struct_bases=[],
    name_mapping={
        "priority": "priority",
        "vpc": "vpc",
        "mutation_protection": "mutationProtection",
        "name": "name",
    },
)
class FirewallRuleGroupAssociationOptions:
    def __init__(
        self,
        *,
        priority: jsii.Number,
        vpc: _IVpc_6d1f76c4,
        mutation_protection: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for a Firewall Rule Group Association.

        :param priority: (experimental) The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC. DNS Firewall filters VPC traffic starting from rule group with the lowest numeric priority setting. This value must be greater than 100 and less than 9,000
        :param vpc: (experimental) The VPC that to associate with the rule group.
        :param mutation_protection: (experimental) If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections. Default: true
        :param name: (experimental) The name of the association. Default: - a CloudFormation generated name

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as ec2
            
            # rule_group: route53resolver.FirewallRuleGroup
            # my_vpc: ec2.Vpc
            
            
            rule_group.associate("Association",
                priority=101,
                vpc=my_vpc
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__27e95f73c11c17cb03984bf35893310b47286d1ab19588e7e4e2a36846f6b02f)
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument mutation_protection", value=mutation_protection, expected_type=type_hints["mutation_protection"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "priority": priority,
            "vpc": vpc,
        }
        if mutation_protection is not None:
            self._values["mutation_protection"] = mutation_protection
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def priority(self) -> jsii.Number:
        '''(experimental) The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC.

        DNS Firewall filters VPC
        traffic starting from rule group with the lowest numeric priority setting.

        This value must be greater than 100 and less than 9,000

        :stability: experimental
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def vpc(self) -> _IVpc_6d1f76c4:
        '''(experimental) The VPC that to associate with the rule group.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_IVpc_6d1f76c4, result)

    @builtins.property
    def mutation_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("mutation_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the association.

        :default: - a CloudFormation generated name

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallRuleGroupAssociationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.FirewallRuleGroupAssociationProps",
    jsii_struct_bases=[FirewallRuleGroupAssociationOptions],
    name_mapping={
        "priority": "priority",
        "vpc": "vpc",
        "mutation_protection": "mutationProtection",
        "name": "name",
        "firewall_rule_group": "firewallRuleGroup",
    },
)
class FirewallRuleGroupAssociationProps(FirewallRuleGroupAssociationOptions):
    def __init__(
        self,
        *,
        priority: jsii.Number,
        vpc: _IVpc_6d1f76c4,
        mutation_protection: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
        firewall_rule_group: "IFirewallRuleGroup",
    ) -> None:
        '''(experimental) Properties for a Firewall Rule Group Association.

        :param priority: (experimental) The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC. DNS Firewall filters VPC traffic starting from rule group with the lowest numeric priority setting. This value must be greater than 100 and less than 9,000
        :param vpc: (experimental) The VPC that to associate with the rule group.
        :param mutation_protection: (experimental) If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections. Default: true
        :param name: (experimental) The name of the association. Default: - a CloudFormation generated name
        :param firewall_rule_group: (experimental) The firewall rule group which must be associated.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_ec2 as ec2
            from monocdk import aws_route53resolver as route53resolver
            
            # firewall_rule_group: route53resolver.FirewallRuleGroup
            # vpc: ec2.Vpc
            
            firewall_rule_group_association_props = route53resolver.FirewallRuleGroupAssociationProps(
                firewall_rule_group=firewall_rule_group,
                priority=123,
                vpc=vpc,
            
                # the properties below are optional
                mutation_protection=False,
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02490a2d8d258f32524d3b5e1119410a5e672c443a9189d41f5d5ad104e60b65)
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument mutation_protection", value=mutation_protection, expected_type=type_hints["mutation_protection"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument firewall_rule_group", value=firewall_rule_group, expected_type=type_hints["firewall_rule_group"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "priority": priority,
            "vpc": vpc,
            "firewall_rule_group": firewall_rule_group,
        }
        if mutation_protection is not None:
            self._values["mutation_protection"] = mutation_protection
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def priority(self) -> jsii.Number:
        '''(experimental) The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC.

        DNS Firewall filters VPC
        traffic starting from rule group with the lowest numeric priority setting.

        This value must be greater than 100 and less than 9,000

        :stability: experimental
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def vpc(self) -> _IVpc_6d1f76c4:
        '''(experimental) The VPC that to associate with the rule group.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_IVpc_6d1f76c4, result)

    @builtins.property
    def mutation_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("mutation_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the association.

        :default: - a CloudFormation generated name

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def firewall_rule_group(self) -> "IFirewallRuleGroup":
        '''(experimental) The firewall rule group which must be associated.

        :stability: experimental
        '''
        result = self._values.get("firewall_rule_group")
        assert result is not None, "Required property 'firewall_rule_group' is missing"
        return typing.cast("IFirewallRuleGroup", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallRuleGroupAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_route53resolver.FirewallRuleGroupProps",
    jsii_struct_bases=[],
    name_mapping={"name": "name", "rules": "rules"},
)
class FirewallRuleGroupProps:
    def __init__(
        self,
        *,
        name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Sequence[typing.Union[FirewallRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Properties for a Firewall Rule Group.

        :param name: (experimental) The name of the rule group. Default: - a CloudFormation generated name
        :param rules: (experimental) A list of rules for this group. Default: - no rules

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # my_block_list: route53resolver.FirewallDomainList
            
            route53resolver.FirewallRuleGroup(self, "RuleGroup",
                rules=[route53resolver.aws_route53resolver.FirewallRule(
                    priority=10,
                    firewall_domain_list=my_block_list,
                    # block and reply with NODATA
                    action=route53resolver.FirewallRuleAction.block()
                )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a986d5b94a70b86cb27049a68bae32782f65d5749eb4e29e1a10b512a657a6e3)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument rules", value=rules, expected_type=type_hints["rules"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if name is not None:
            self._values["name"] = name
        if rules is not None:
            self._values["rules"] = rules

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the rule group.

        :default: - a CloudFormation generated name

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def rules(self) -> typing.Optional[typing.List[FirewallRule]]:
        '''(experimental) A list of rules for this group.

        :default: - no rules

        :stability: experimental
        '''
        result = self._values.get("rules")
        return typing.cast(typing.Optional[typing.List[FirewallRule]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FirewallRuleGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_route53resolver.IFirewallDomainList")
class IFirewallDomainList(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A Firewall Domain List.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListId")
    def firewall_domain_list_id(self) -> builtins.str:
        '''(experimental) The ID of the domain list.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IFirewallDomainListProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) A Firewall Domain List.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_route53resolver.IFirewallDomainList"

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListId")
    def firewall_domain_list_id(self) -> builtins.str:
        '''(experimental) The ID of the domain list.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFirewallDomainList).__jsii_proxy_class__ = lambda : _IFirewallDomainListProxy


@jsii.interface(jsii_type="monocdk.aws_route53resolver.IFirewallRuleGroup")
class IFirewallRuleGroup(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A Firewall Rule Group.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupId")
    def firewall_rule_group_id(self) -> builtins.str:
        '''(experimental) The ID of the rule group.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IFirewallRuleGroupProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) A Firewall Rule Group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_route53resolver.IFirewallRuleGroup"

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupId")
    def firewall_rule_group_id(self) -> builtins.str:
        '''(experimental) The ID of the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFirewallRuleGroup).__jsii_proxy_class__ = lambda : _IFirewallRuleGroupProxy


@jsii.implements(IFirewallDomainList)
class FirewallDomainList(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.FirewallDomainList",
):
    '''(experimental) A Firewall Domain List.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        block_list = route53resolver.FirewallDomainList(self, "BlockList",
            domains=route53resolver.FirewallDomains.from_list(["bad-domain.com", "bot-domain.net"])
        )
        
        s3_list = route53resolver.FirewallDomainList(self, "S3List",
            domains=route53resolver.FirewallDomains.from_s3_url("s3://bucket/prefix/object")
        )
        
        asset_list = route53resolver.FirewallDomainList(self, "AssetList",
            domains=route53resolver.FirewallDomains.from_asset("/path/to/domains.txt")
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        domains: FirewallDomains,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param domains: (experimental) A list of domains.
        :param name: (experimental) A name for the domain list. Default: - a CloudFormation generated name

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f515e736cc6e5ebece2ee53b00b96333077689d30187ef5e80a911a80bbe6ce)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FirewallDomainListProps(domains=domains, name=name)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromFirewallDomainListId")
    @builtins.classmethod
    def from_firewall_domain_list_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        firewall_domain_list_id: builtins.str,
    ) -> IFirewallDomainList:
        '''(experimental) Import an existing Firewall Rule Group.

        :param scope: -
        :param id: -
        :param firewall_domain_list_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__606d646ef77874f69136dcec5f64dc1fd3bf7b603c69c91b0cc1a4ea09bc9f00)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument firewall_domain_list_id", value=firewall_domain_list_id, expected_type=type_hints["firewall_domain_list_id"])
        return typing.cast(IFirewallDomainList, jsii.sinvoke(cls, "fromFirewallDomainListId", [scope, id, firewall_domain_list_id]))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListArn")
    def firewall_domain_list_arn(self) -> builtins.str:
        '''(experimental) The ARN (Amazon Resource Name) of the domain list.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListArn"))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListCreationTime")
    def firewall_domain_list_creation_time(self) -> builtins.str:
        '''(experimental) The date and time that the domain list was created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListCreatorRequestId")
    def firewall_domain_list_creator_request_id(self) -> builtins.str:
        '''(experimental) The creator request ID.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListCreatorRequestId"))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListDomainCount")
    def firewall_domain_list_domain_count(self) -> jsii.Number:
        '''(experimental) The number of domains in the list.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "firewallDomainListDomainCount"))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListId")
    def firewall_domain_list_id(self) -> builtins.str:
        '''(experimental) The ID of the domain list.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListId"))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListManagedOwnerName")
    def firewall_domain_list_managed_owner_name(self) -> builtins.str:
        '''(experimental) The owner of the list, used only for lists that are not managed by you.

        For example, the managed domain list ``AWSManagedDomainsMalwareDomainList``
        has the managed owner name ``Route 53 Resolver DNS Firewall``.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListManagedOwnerName"))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListModificationTime")
    def firewall_domain_list_modification_time(self) -> builtins.str:
        '''(experimental) The date and time that the domain list was last modified.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListModificationTime"))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListStatus")
    def firewall_domain_list_status(self) -> builtins.str:
        '''(experimental) The status of the domain list.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListStatus"))

    @builtins.property
    @jsii.member(jsii_name="firewallDomainListStatusMessage")
    def firewall_domain_list_status_message(self) -> builtins.str:
        '''(experimental) Additional information about the status of the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallDomainListStatusMessage"))


@jsii.implements(IFirewallRuleGroup)
class FirewallRuleGroup(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_route53resolver.FirewallRuleGroup",
):
    '''(experimental) A Firewall Rule Group.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_block_list: route53resolver.FirewallDomainList
        
        route53resolver.FirewallRuleGroup(self, "RuleGroup",
            rules=[route53resolver.aws_route53resolver.FirewallRule(
                priority=10,
                firewall_domain_list=my_block_list,
                # block and reply with NODATA
                action=route53resolver.FirewallRuleAction.block()
            )
            ]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        name: typing.Optional[builtins.str] = None,
        rules: typing.Optional[typing.Sequence[typing.Union[FirewallRule, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param name: (experimental) The name of the rule group. Default: - a CloudFormation generated name
        :param rules: (experimental) A list of rules for this group. Default: - no rules

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60844cea59ac9d103dc6ea4e7ad4de89ffe9020e462a1b147f3153e0f7c9170f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FirewallRuleGroupProps(name=name, rules=rules)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromFirewallRuleGroupId")
    @builtins.classmethod
    def from_firewall_rule_group_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        firewall_rule_group_id: builtins.str,
    ) -> IFirewallRuleGroup:
        '''(experimental) Import an existing Firewall Rule Group.

        :param scope: -
        :param id: -
        :param firewall_rule_group_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__304ed514ae3da1cd2a839e0a1ec9450e326fd9cb28b0c5d96cf99781ae79c604)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument firewall_rule_group_id", value=firewall_rule_group_id, expected_type=type_hints["firewall_rule_group_id"])
        return typing.cast(IFirewallRuleGroup, jsii.sinvoke(cls, "fromFirewallRuleGroupId", [scope, id, firewall_rule_group_id]))

    @jsii.member(jsii_name="addRule")
    def add_rule(
        self,
        *,
        action: FirewallRuleAction,
        firewall_domain_list: IFirewallDomainList,
        priority: jsii.Number,
    ) -> "FirewallRuleGroup":
        '''(experimental) Adds a rule to this group.

        :param action: (experimental) The action for this rule.
        :param firewall_domain_list: (experimental) The domain list for this rule.
        :param priority: (experimental) The priority of the rule in the rule group. This value must be unique within the rule group.

        :stability: experimental
        '''
        rule = FirewallRule(
            action=action, firewall_domain_list=firewall_domain_list, priority=priority
        )

        return typing.cast("FirewallRuleGroup", jsii.invoke(self, "addRule", [rule]))

    @jsii.member(jsii_name="associate")
    def associate(
        self,
        id: builtins.str,
        *,
        priority: jsii.Number,
        vpc: _IVpc_6d1f76c4,
        mutation_protection: typing.Optional[builtins.bool] = None,
        name: typing.Optional[builtins.str] = None,
    ) -> FirewallRuleGroupAssociation:
        '''(experimental) Associates this Firewall Rule Group with a VPC.

        :param id: -
        :param priority: (experimental) The setting that determines the processing order of the rule group among the rule groups that are associated with a single VPC. DNS Firewall filters VPC traffic starting from rule group with the lowest numeric priority setting. This value must be greater than 100 and less than 9,000
        :param vpc: (experimental) The VPC that to associate with the rule group.
        :param mutation_protection: (experimental) If enabled, this setting disallows modification or removal of the association, to help prevent against accidentally altering DNS firewall protections. Default: true
        :param name: (experimental) The name of the association. Default: - a CloudFormation generated name

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e11e9d3940da74434f8b01eb6b3d7b20b74c0cc3a60d1aeb87d415cdca9cbc0)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = FirewallRuleGroupAssociationOptions(
            priority=priority,
            vpc=vpc,
            mutation_protection=mutation_protection,
            name=name,
        )

        return typing.cast(FirewallRuleGroupAssociation, jsii.invoke(self, "associate", [id, props]))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupArn")
    def firewall_rule_group_arn(self) -> builtins.str:
        '''(experimental) The ARN (Amazon Resource Name) of the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupArn"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupCreationTime")
    def firewall_rule_group_creation_time(self) -> builtins.str:
        '''(experimental) The date and time that the rule group was created.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupCreationTime"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupCreatorRequestId")
    def firewall_rule_group_creator_request_id(self) -> builtins.str:
        '''(experimental) The creator request ID.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupCreatorRequestId"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupId")
    def firewall_rule_group_id(self) -> builtins.str:
        '''(experimental) The ID of the rule group.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupId"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupModificationTime")
    def firewall_rule_group_modification_time(self) -> builtins.str:
        '''(experimental) The date and time that the rule group was last modified.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupModificationTime"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupOwnerId")
    def firewall_rule_group_owner_id(self) -> builtins.str:
        '''(experimental) The AWS account ID for the account that created the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupOwnerId"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupRuleCount")
    def firewall_rule_group_rule_count(self) -> jsii.Number:
        '''(experimental) The number of rules in the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(jsii.Number, jsii.get(self, "firewallRuleGroupRuleCount"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupShareStatus")
    def firewall_rule_group_share_status(self) -> builtins.str:
        '''(experimental) Whether the rule group is shared with other AWS accounts, or was shared with the current account by another AWS account.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupShareStatus"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupStatus")
    def firewall_rule_group_status(self) -> builtins.str:
        '''(experimental) The status of the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupStatus"))

    @builtins.property
    @jsii.member(jsii_name="firewallRuleGroupStatusMessage")
    def firewall_rule_group_status_message(self) -> builtins.str:
        '''(experimental) Additional information about the status of the rule group.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "firewallRuleGroupStatusMessage"))


__all__ = [
    "CfnFirewallDomainList",
    "CfnFirewallDomainListProps",
    "CfnFirewallRuleGroup",
    "CfnFirewallRuleGroupAssociation",
    "CfnFirewallRuleGroupAssociationProps",
    "CfnFirewallRuleGroupProps",
    "CfnResolverConfig",
    "CfnResolverConfigProps",
    "CfnResolverDNSSECConfig",
    "CfnResolverDNSSECConfigProps",
    "CfnResolverEndpoint",
    "CfnResolverEndpointProps",
    "CfnResolverQueryLoggingConfig",
    "CfnResolverQueryLoggingConfigAssociation",
    "CfnResolverQueryLoggingConfigAssociationProps",
    "CfnResolverQueryLoggingConfigProps",
    "CfnResolverRule",
    "CfnResolverRuleAssociation",
    "CfnResolverRuleAssociationProps",
    "CfnResolverRuleProps",
    "DnsBlockResponse",
    "DomainsConfig",
    "FirewallDomainList",
    "FirewallDomainListProps",
    "FirewallDomains",
    "FirewallRule",
    "FirewallRuleAction",
    "FirewallRuleGroup",
    "FirewallRuleGroupAssociation",
    "FirewallRuleGroupAssociationOptions",
    "FirewallRuleGroupAssociationProps",
    "FirewallRuleGroupProps",
    "IFirewallDomainList",
    "IFirewallRuleGroup",
]

publication.publish()

def _typecheckingstub__c9226e89e860d3053edc103ef2b7a6a6bc1014c625375bf8f8e9206d0dd6bf8e(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    domain_file_url: typing.Optional[builtins.str] = None,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__432fe92b6c39ad26f62e6dcfe1967fd0387026460efdce456ebff84738882dbe(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__514bcaed72c16e54daa31d2d7f5589ffda651bb7a26d82de6611dcfe1752ef35(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3076e952c50f9de33664971e14f713b546bb1b1a6a2a786caf510101cc664529(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93143312ffbb8bb075cb8e6f1377fb2264e3cd58f4df4e2859ffc45ae30ee235(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b3018503235ebe09449b0014355e8db18d7b6181b4f8b10f0994605ce529b2b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bfb31349d99e57f0d1b5108c31b489d58bdfcd93b38642dbad81c579d931ae56(
    *,
    domain_file_url: typing.Optional[builtins.str] = None,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78963d0f59dce3be63f966b2e817cf54fa911a8633d79b95420f8ecdad76bbc0(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    firewall_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFirewallRuleGroup.FirewallRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ce870ddbc028e94a8042e6b9b9ba1d59a813a74a47f3211ac520e7d83a33ed7(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__146811da39f46bf0f891329d168b61984fbfb756cef2397ce3192ed448def2dd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7640cfb1c6b4f15a53834a31ab5702b13b2863d3762fc9383e42c0b8c97d78a3(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnFirewallRuleGroup.FirewallRuleProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c33934fbcd24cc426a7f163e3b9f48670c6714a3356e9ed6d0362a18d090a329(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13c3eaad7971060e0e1744d166fee029f5bbaf6f2842bb7d9fbd9f0f591536b8(
    *,
    action: builtins.str,
    firewall_domain_list_id: builtins.str,
    priority: jsii.Number,
    block_override_dns_type: typing.Optional[builtins.str] = None,
    block_override_domain: typing.Optional[builtins.str] = None,
    block_override_ttl: typing.Optional[jsii.Number] = None,
    block_response: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65e2efaeb3cba1cff1a591cc4af128bd99fb7d0a7d2875a762c76a992abb7022(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    firewall_rule_group_id: builtins.str,
    priority: jsii.Number,
    vpc_id: builtins.str,
    mutation_protection: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__089b903322965086bdaad22e49308aae6bd1797b01fd9ff782b9c4db726193c6(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29476ebda3c6da62e89cd75239badfab9641f7890167e8fd0beef724513ff219(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__869632dd26478eab16a8bbe7ed33b312b7fe791b1fc359c9bf1592f29eab6e26(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567078bedba758549d396bf118ff16b49d4eb6c4c3759e5d76bbeb70457e6063(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__823bb73cb66838530a67d52bf6dd9e3dbc4574992b77545f6c7bab4965005934(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38a0c3c1e8a440cdc1bd36e7c5ccb2b0b5d6a2099f1f7c0e1dfe1e7d49762fc7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fec66f498650b5a588c4893cd3ece39fca209c31f3b139b819ebbfabdea3f50(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e96119dbe51842e9579e97beeefce01a9caab6a034e939a122c19110cfb946ed(
    *,
    firewall_rule_group_id: builtins.str,
    priority: jsii.Number,
    vpc_id: builtins.str,
    mutation_protection: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b13410754afd4163093c293e9e89cc17fb278ff118c8d02819d84784a6891bdd(
    *,
    firewall_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnFirewallRuleGroup.FirewallRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e08cd0ff1e98eabae1a5efea9e7377d51e6a5349e5fc08eb80eac151ea1dc1(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    autodefined_reverse_flag: builtins.str,
    resource_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acda34f36454caebc2d7c0f4598eee5cd13e03036b77741874ce193c7899ea92(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e8a0b1b0e9877524306e7849834ed733bf3a70e8832b0c486f47b80a43380e2(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23b591a5338200171cccfd25fb5719faf82403c7f719df09e668785b79cf649f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__221d5a700b499bc6ec219b6e3020ad6f41051121f3df6bb0b58a7bfa5aad51f0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607f67798d5caf456edb05d2aacfbeb716e1d6677768b82071fc05390a6d74f3(
    *,
    autodefined_reverse_flag: builtins.str,
    resource_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba0b97183f6c675fd5d903d5f953db973478e09b73b38ecbdb3426f961fd0ebe(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc9d8352dbf8366d0ed5a016d104273bdf2b2201748da9d4828cc963041214e(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6eeb52eec669df537bfd561bb8d58a8e9f4267010445d23f5ac3a3547e7daeca(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b99470a420546ab85eabe22af61333634275e4204374a9e5083ce0978d9343f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__860045c80d8c266206341c24dc179fb3b5895c29cba1f40b444dbd8dd1fbef78(
    *,
    resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de3bf2a11e078b4c521538b3b2cfe2efc4e2bed148e848aa95010328fef38d0b(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    direction: builtins.str,
    ip_addresses: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnResolverEndpoint.IpAddressRequestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    security_group_ids: typing.Sequence[builtins.str],
    name: typing.Optional[builtins.str] = None,
    outpost_arn: typing.Optional[builtins.str] = None,
    preferred_instance_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458ae08d9fd9604cd883d3c4d8552a5358e45e3d1a706198d61fb4152079147d(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0d545d4bbab249efadae077e96fbc6fb01ece34a9a034f18de5bb8274692618(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbf4356f85419d4da784b0d7ff8cdf5badc70333a348dfda516cfa00d05643b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d207dbb161c27d4803c7fe06c88abb6878a39ee2a60a7b87e0a88c8e79482ce(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnResolverEndpoint.IpAddressRequestProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7abd8da97ac62ac614dadf43af442954b68d8bf3218d854df86f6f09e54e09b8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__daf8b9135eae0efddf2609a72a08b6904b7acb2d9348884c9ce0719a6e7e94b6(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee253db2724909e5349fc710cb95e3f66abe09224024fa3851fc28cd6ad4db3a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a816f84b471984362f5b67fb9937c76745d5edd936f766c0848f020568540245(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac895499b4ec270e952cf22e8cdb0a90ab2bd36e9a1bb2e88e261ac513ac9a9e(
    *,
    subnet_id: builtins.str,
    ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac531b5b2285ee1456c4c3977661ff80c0069882f3bc23903c8d51cdd5d04ef4(
    *,
    direction: builtins.str,
    ip_addresses: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnResolverEndpoint.IpAddressRequestProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    security_group_ids: typing.Sequence[builtins.str],
    name: typing.Optional[builtins.str] = None,
    outpost_arn: typing.Optional[builtins.str] = None,
    preferred_instance_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2368f767a41dc1501536d9082acec35144578d8deaaf7b6c35956046f30c5df7(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    destination_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56c3aba8d5940b75b97df4348cacbc3e2a8a987b671e4dba5f9b44e4d36c43e6(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85e175feaf01e3cf9a1ee688fe03ed1c02e68f787000d092b39b85c930c7169b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d69e601e14e6db6d199253c056d9bef60f86ae3b1b8f611451a8b98d41f97df(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e506a6a41618bfb76c7c4cba8da850d90017114a2ac53fba677812e5a5d1a386(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcaa961b5d089a5e914faeb3afcfa59c3325b63c718ad249b5852121418ad05f(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    resolver_query_log_config_id: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99d62f043fb8921187c3aa88146e6a087fd08b4a2f65401e1783daed1f29e4fb(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__949fbd99378095652a7a493973ab4d8c64b1d536e9922a8e672878aa58187a83(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1924b876c5da76ed19b2faa3dca19ea7f3884fb2af435f2834a21c0cc2c08a25(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecd51c3f59cb73dcc7011a5e959f0ec8956fe097742fc4fafa9d79eee8e76a88(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8911be334a0a764b72a0f0c7c75a1cbe88d002cd63570e106671517b4015fcd2(
    *,
    resolver_query_log_config_id: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__157537cc151e371ffa6dd12360f861fd41a5d3d7521ad9b9bf53d9930a32f026(
    *,
    destination_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cc486e7bf2b5d6a4bbbd25a103cf389949ba3a68d29d1b087e7773e8831a865(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    domain_name: builtins.str,
    rule_type: builtins.str,
    name: typing.Optional[builtins.str] = None,
    resolver_endpoint_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_ips: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnResolverRule.TargetAddressProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f9d84504f87cf1bd65dbdb82ed1825b4a209864fe6fe343a56dd098d39b404(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__438262d90f3f5c3e8973d645cd7cee74cbd9a36163f25d2289ad3e5005ba33fe(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54a3110bf5b0c63a2e542c7870cebb6c9bc04f035a883ff0729ee50b4e4bb219(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9dc2109cb5e3e425ada0e0603ede5bdc5876141c63596a803c1c1357eb7627e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3a8da420a1f7dfd333cc40a5ad40ff6191331905602d40f0a8156e90a607c02(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60f58e6a3a317c6541832c7ad6f9860ff25d2db07af88732fc449d644761048b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf23755701aaa60b6c4a30c38ec027835e23e2f863d2be9b9aec7d2510fc0dc8(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnResolverRule.TargetAddressProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6becb27622b48e0b972ec85239df0aaa90a0c469df4a79d37cbda23cd9ecd462(
    *,
    ip: builtins.str,
    port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f0ed968b2d4de5305338b6664e23d8c30ac9729836b4a3ed5f0884324568dff(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    resolver_rule_id: builtins.str,
    vpc_id: builtins.str,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be8d0499f1b1d1a16222cddb017b42bf3f111aa7d2e71ad46bad3864438531f2(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d5c2a70e87b55aed22bd82e643a3f958720b7768412b1b250e796b33fe668f0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5a56b1c14ba23e7322de04dbf2839daa021bc0d14a3821a170af725b7ecde9c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b89e366d47ece7eeaf0e1772d4aaedecbd90764c5fb6b7ce204b9d0fb104b8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f36585defb7c13628c98741000a39161ed95bbf9294d84c14b034869bed7e9b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1ee181ebdff79af265cf644305f92d6bd3d6484761f88024c65bd75840e2cb(
    *,
    resolver_rule_id: builtins.str,
    vpc_id: builtins.str,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e94dd61877e2550e1b24254b836d4a7978319d65907f9744de6324fd06b9194f(
    *,
    domain_name: builtins.str,
    rule_type: builtins.str,
    name: typing.Optional[builtins.str] = None,
    resolver_endpoint_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_ips: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnResolverRule.TargetAddressProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09872892c6856e53f75d075e85d9d716b850fcbb9744c0c6bc246f39f0c643a5(
    domain: builtins.str,
    ttl: typing.Optional[_Duration_070aa057] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__52b1a1a0c9263618951f23d6b235ea2b391517272efc2e35fb8e9fc5b4deaea2(
    *,
    domain_file_url: typing.Optional[builtins.str] = None,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__950fd0fc0371d1b204c7a8a11780a1d24ece068b5ad1b7ef98ff4ba5f7e8f8c3(
    *,
    domains: FirewallDomains,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43ec95f8223fd39c65da9e63c8961b662a2979239ad9a7f7caff4220e67da013(
    asset_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc1791a138243917cbda6d5b5c78ef95acc86c4d5559f3a3db9538a7632b597a(
    list: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__177e814ea37b4186f3201e85deaa8aca1a791acc995f8d3c42d3c696b9f9cd79(
    bucket: _IBucket_73486e29,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ba938fd3eb594c9de4a7e5e9a2aac231658a3c283a92e59d82582fa8c99bef7(
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bf61cbd69db53615a75a9fded1569910ec0510dd54ce6687eac495a70b0f2f0(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b9086409696b42f61714689b15e5b42a6f1025ceea93067a0e3a2fa9797aa485(
    *,
    action: FirewallRuleAction,
    firewall_domain_list: IFirewallDomainList,
    priority: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cde4f65acd62f6ff12e0834f5e5f8f3ecf454bd9dda5d4838baa4f268857f659(
    response: typing.Optional[DnsBlockResponse] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d33697555a04f173d2de57c6f42bd39bef2dd4f272930b8c871fc9ff978805fe(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    firewall_rule_group: IFirewallRuleGroup,
    priority: jsii.Number,
    vpc: _IVpc_6d1f76c4,
    mutation_protection: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__27e95f73c11c17cb03984bf35893310b47286d1ab19588e7e4e2a36846f6b02f(
    *,
    priority: jsii.Number,
    vpc: _IVpc_6d1f76c4,
    mutation_protection: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02490a2d8d258f32524d3b5e1119410a5e672c443a9189d41f5d5ad104e60b65(
    *,
    priority: jsii.Number,
    vpc: _IVpc_6d1f76c4,
    mutation_protection: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
    firewall_rule_group: IFirewallRuleGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a986d5b94a70b86cb27049a68bae32782f65d5749eb4e29e1a10b512a657a6e3(
    *,
    name: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[FirewallRule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f515e736cc6e5ebece2ee53b00b96333077689d30187ef5e80a911a80bbe6ce(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domains: FirewallDomains,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__606d646ef77874f69136dcec5f64dc1fd3bf7b603c69c91b0cc1a4ea09bc9f00(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    firewall_domain_list_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60844cea59ac9d103dc6ea4e7ad4de89ffe9020e462a1b147f3153e0f7c9170f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[FirewallRule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304ed514ae3da1cd2a839e0a1ec9450e326fd9cb28b0c5d96cf99781ae79c604(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    firewall_rule_group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e11e9d3940da74434f8b01eb6b3d7b20b74c0cc3a60d1aeb87d415cdca9cbc0(
    id: builtins.str,
    *,
    priority: jsii.Number,
    vpc: _IVpc_6d1f76c4,
    mutation_protection: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
