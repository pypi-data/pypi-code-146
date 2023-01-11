'''
# Amazon Route53 Resolver Construct Library

<!--BEGIN STABILITY BANNER-->---


![cfn-resources: Stable](https://img.shields.io/badge/cfn--resources-stable-success.svg?style=for-the-badge)

> All classes with the `Cfn` prefix in this module ([CFN Resources](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) are always stable and safe to use.

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

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
    rules=[route53resolver.FirewallRule(
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
import aws_cdk.aws_ec2 as ec2

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

from ._jsii import *

import aws_cdk.aws_ec2 as _aws_cdk_aws_ec2_67de8e8d
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_55f001a5
import aws_cdk.core as _aws_cdk_core_f4b25747
import constructs as _constructs_77d1e7e8


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnFirewallDomainList(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53resolver.CfnFirewallDomainList",
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
        import aws_cdk.aws_route53resolver as route53resolver
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        domain_file_url: typing.Optional[builtins.str] = None,
        domains: typing.Optional[typing.Sequence[builtins.str]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__555ddf44c52202073669f04898e1d37d30920953457df6c2777354f621bbc1df)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFirewallDomainListProps(
            domain_file_url=domain_file_url, domains=domains, name=name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08e29bb557e2e76340b8cbc1298149289e09169f65b20b0f49bd4ebb52b10e38)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a913e52a37e888ffe82f9861b33ad50d5ef2abae73269f505289e98f52183423)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A list of the tag keys and values that you want to associate with the domain list.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html#cfn-route53resolver-firewalldomainlist-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b6b7ed4d47c8736285ad482281a7b3a1a1e81f2376643f4251ce79ddbde052fa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a11f8fa0dd52a7a6cd1195b3c25648bcaab780b5a3696d85c221646fa1fd89e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__978620f1b5655f35805cd034fc43012d548ff6be263db3b871b140f11dd963d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53resolver.CfnFirewallDomainListProps",
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
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_route53resolver as route53resolver
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__a68481722a8554b1fb0d83ce84d5ca9bda73a49a5bc12894b557efc66d9cbded)
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
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A list of the tag keys and values that you want to associate with the domain list.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewalldomainlist.html#cfn-route53resolver-firewalldomainlist-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFirewallDomainListProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnFirewallRuleGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53resolver.CfnFirewallRuleGroup",
):
    '''A CloudFormation ``AWS::Route53Resolver::FirewallRuleGroup``.

    High-level information for a firewall rule group. A firewall rule group is a collection of rules that DNS Firewall uses to filter DNS network traffic for a VPC. To retrieve the rules for the rule group, call `ListFirewallRules <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_ListFirewallRules.html>`_ .

    :cloudformationResource: AWS::Route53Resolver::FirewallRuleGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_route53resolver as route53resolver
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        firewall_rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union["CfnFirewallRuleGroup.FirewallRuleProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Route53Resolver::FirewallRuleGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param firewall_rules: A list of the rules that you have defined.
        :param name: The name of the rule group.
        :param tags: A list of the tag keys and values that you want to associate with the rule group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c10bd5f5a59548a6fde2daff1a043b2d05a3dbdca2c182e143bc7ba6da166f2b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnFirewallRuleGroupProps(
            firewall_rules=firewall_rules, name=name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12eb1fd98f8c18afc6088fe831fa5fcfd0837476b45a1159e69ed007a6e899df)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e64244c2524e24b6af62cbb286f9e7a5a63d48b4fe367feb6b860163f1fc9495)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A list of the tag keys and values that you want to associate with the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html#cfn-route53resolver-firewallrulegroup-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="firewallRules")
    def firewall_rules(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnFirewallRuleGroup.FirewallRuleProperty", _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''A list of the rules that you have defined.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html#cfn-route53resolver-firewallrulegroup-firewallrules
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnFirewallRuleGroup.FirewallRuleProperty", _aws_cdk_core_f4b25747.IResolvable]]]], jsii.get(self, "firewallRules"))

    @firewall_rules.setter
    def firewall_rules(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnFirewallRuleGroup.FirewallRuleProperty", _aws_cdk_core_f4b25747.IResolvable]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a481a8bc47312623972b69d3087e645728b2f9b78934d5f78ab6203492d26c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__84ebd3fb9929801bc7cb9f22cb9a03f8fc34eda98f48e63b1cee8b5930bcbb21)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-route53resolver.CfnFirewallRuleGroup.FirewallRuleProperty",
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
                import aws_cdk.aws_route53resolver as route53resolver
                
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
                type_hints = typing.get_type_hints(_typecheckingstub__3779e3ea3239883a621bc04756bc0f3df09f8eebecb91da90dc56be9205ae50e)
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnFirewallRuleGroupAssociation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53resolver.CfnFirewallRuleGroupAssociation",
):
    '''A CloudFormation ``AWS::Route53Resolver::FirewallRuleGroupAssociation``.

    An association between a firewall rule group and a VPC, which enables DNS filtering for the VPC.

    :cloudformationResource: AWS::Route53Resolver::FirewallRuleGroupAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_route53resolver as route53resolver
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        firewall_rule_group_id: builtins.str,
        priority: jsii.Number,
        vpc_id: builtins.str,
        mutation_protection: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__0308fe827e6b3a3505bb28772723d284420b4c739e09c3060d8f7f39d6ae42cc)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd042463d0ef7afc78b157b6eb30682902ab9d2344d445ea05af79895dcdc99)
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
            type_hints = typing.get_type_hints(_typecheckingstub__385585373172aa6f61e20137d7c1f935386f3242974798eed9d693d637ceeae8)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''A list of the tag keys and values that you want to associate with the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__9fd218820098418e72092e2ba6ef94e0f11f0c861f6f1dac62098098e4755cff)
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
            type_hints = typing.get_type_hints(_typecheckingstub__1ebf1fc36cdbc20218fac8207f2303ddec5d14aa012bc8d672995aa8d5f40bb2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c5e55a689213e73bb6e6c235b317f32e82c66c292c0b56c3285436a8b8968bad)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59361570296280c2314024828f4a094bfaa38a1aea0076a13a6f77f1561594f4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aefb06222c531912656dfa642f05e71e8a22f8383d2d02b7ae21721529f83ba5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53resolver.CfnFirewallRuleGroupAssociationProps",
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
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_route53resolver as route53resolver
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__b7d6b680ce1909bd9e556e0c8d07ab6ae4fdebc59f24dd7d18991d12a390ebb8)
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
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A list of the tag keys and values that you want to associate with the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroupassociation.html#cfn-route53resolver-firewallrulegroupassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFirewallRuleGroupAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53resolver.CfnFirewallRuleGroupProps",
    jsii_struct_bases=[],
    name_mapping={"firewall_rules": "firewallRules", "name": "name", "tags": "tags"},
)
class CfnFirewallRuleGroupProps:
    def __init__(
        self,
        *,
        firewall_rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnFirewallRuleGroup.FirewallRuleProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_route53resolver as route53resolver
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__998a30eb443c97b4395f3eb88dcd151f4aa7cc24743f30442f96ad8cb02d3e9d)
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
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnFirewallRuleGroup.FirewallRuleProperty, _aws_cdk_core_f4b25747.IResolvable]]]]:
        '''A list of the rules that you have defined.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html#cfn-route53resolver-firewallrulegroup-firewallrules
        '''
        result = self._values.get("firewall_rules")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnFirewallRuleGroup.FirewallRuleProperty, _aws_cdk_core_f4b25747.IResolvable]]]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html#cfn-route53resolver-firewallrulegroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A list of the tag keys and values that you want to associate with the rule group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-firewallrulegroup.html#cfn-route53resolver-firewallrulegroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnFirewallRuleGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResolverConfig(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53resolver.CfnResolverConfig",
):
    '''A CloudFormation ``AWS::Route53Resolver::ResolverConfig``.

    A complex type that contains information about a Resolver configuration for a VPC.

    :cloudformationResource: AWS::Route53Resolver::ResolverConfig
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverconfig.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_route53resolver as route53resolver
        
        cfn_resolver_config = route53resolver.CfnResolverConfig(self, "MyCfnResolverConfig",
            autodefined_reverse_flag="autodefinedReverseFlag",
            resource_id="resourceId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6d3e01eb13ecf3fc6c09139de1f8804ab22038ba2a08712e02cddec75e0547b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResolverConfigProps(
            autodefined_reverse_flag=autodefined_reverse_flag, resource_id=resource_id
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ff6afd670bb17b6410b44928cecd96d8b3137c72236d3e891f52a2f500a575e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d767bbf2f5ebd1cc854d78b1a1125125598aaa0f095e12f069fbae675ea6dd34)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3dbc6a7c7789751dd260c52ff2e78afe6a649ab277d4036f734500536b7a92b7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d61341477aa7e147988292017c7c80c2752ce11cdbfe3f7da2ef3cd56b6cfd8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53resolver.CfnResolverConfigProps",
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
            import aws_cdk.aws_route53resolver as route53resolver
            
            cfn_resolver_config_props = route53resolver.CfnResolverConfigProps(
                autodefined_reverse_flag="autodefinedReverseFlag",
                resource_id="resourceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ee753ccc06b40acc70153c14525b069b3d66517d509ebd5b18ace9d9c824125e)
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResolverDNSSECConfig(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53resolver.CfnResolverDNSSECConfig",
):
    '''A CloudFormation ``AWS::Route53Resolver::ResolverDNSSECConfig``.

    The ``AWS::Route53Resolver::ResolverDNSSECConfig`` resource is a complex type that contains information about a configuration for DNSSEC validation.

    :cloudformationResource: AWS::Route53Resolver::ResolverDNSSECConfig
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverdnssecconfig.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_route53resolver as route53resolver
        
        cfn_resolver_dNSSECConfig = route53resolver.CfnResolverDNSSECConfig(self, "MyCfnResolverDNSSECConfig",
            resource_id="resourceId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__cfcd15a3243b968afe8fa16337f0415ba17445d3954fb52ea95f3e589b892b1f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResolverDNSSECConfigProps(resource_id=resource_id)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__625478d24808c52e1e15238c1169fd1cd2172fd4736f6117ee56647c76f689f6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__364031598a568d1e2a20c6789c9fb23c57fa1726ab70fc40da1fe3980c8b3190)
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
            type_hints = typing.get_type_hints(_typecheckingstub__206998a6ef9b2b46ce0c9a91a46a0da70f9101365fbe8d8b7297ebe2f70bb4dc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53resolver.CfnResolverDNSSECConfigProps",
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
            import aws_cdk.aws_route53resolver as route53resolver
            
            cfn_resolver_dNSSECConfig_props = route53resolver.CfnResolverDNSSECConfigProps(
                resource_id="resourceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3e338f0817ab8ead305559a7d148631ac62f113c42c76c5c4cfe9c7adcf7d87)
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResolverEndpoint(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53resolver.CfnResolverEndpoint",
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
        import aws_cdk.aws_route53resolver as route53resolver
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        direction: builtins.str,
        ip_addresses: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResolverEndpoint.IpAddressRequestProperty", typing.Dict[builtins.str, typing.Any]]]]],
        security_group_ids: typing.Sequence[builtins.str],
        name: typing.Optional[builtins.str] = None,
        outpost_arn: typing.Optional[builtins.str] = None,
        preferred_instance_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__228e1f20142fd9984b3c82b6521decf17f34fc81d79d98c85485f678d145729c)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84bfe3cd1240054055dc29a4fdfc754b3333af826720c64decca9039930c4318)
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
            type_hints = typing.get_type_hints(_typecheckingstub__20a59c29bf5bb6a3d9002aaf6ee9e9f710a4abc168f5cf282569e5e2494b368d)
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
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Route 53 Resolver doesn't support updating tags through CloudFormation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b665109081bf00e85db2eb699f45cb6f55d13d9210ec905b8eb8867e6e245751)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "direction", value)

    @builtins.property
    @jsii.member(jsii_name="ipAddresses")
    def ip_addresses(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResolverEndpoint.IpAddressRequestProperty"]]]:
        '''The subnets and IP addresses in your VPC that DNS queries originate from (for outbound endpoints) or that you forward DNS queries to (for inbound endpoints).

        The subnet ID uniquely identifies a VPC.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-ipaddresses
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResolverEndpoint.IpAddressRequestProperty"]]], jsii.get(self, "ipAddresses"))

    @ip_addresses.setter
    def ip_addresses(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResolverEndpoint.IpAddressRequestProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7d88633eb435aab3516dfa96767c4f8b505d109633de12cd43d3750eb092033)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cefeb21a499e0edf6e954313e30c569992fec8a2de10bc01ffe291f859d7c99a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f9b839ede89a09d1722701e891816be340198e9741ffdee30268f531135c3765)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3b41c01da0809295e4e46099b679cee1337253316f0ca65e603790eb13d1832d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__538e4fe27f851288c87e30ff97dd25de4c72cc10ced2af8bbe42d84669ffca6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "preferredInstanceType", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-route53resolver.CfnResolverEndpoint.IpAddressRequestProperty",
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
                import aws_cdk.aws_route53resolver as route53resolver
                
                ip_address_request_property = route53resolver.CfnResolverEndpoint.IpAddressRequestProperty(
                    subnet_id="subnetId",
                
                    # the properties below are optional
                    ip="ip"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__85d8a364815a9377d601e54826e2e2fdc73a177d1914877aae6e757c33d2feaf)
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
    jsii_type="@aws-cdk/aws-route53resolver.CfnResolverEndpointProps",
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
        ip_addresses: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResolverEndpoint.IpAddressRequestProperty, typing.Dict[builtins.str, typing.Any]]]]],
        security_group_ids: typing.Sequence[builtins.str],
        name: typing.Optional[builtins.str] = None,
        outpost_arn: typing.Optional[builtins.str] = None,
        preferred_instance_type: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
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
            import aws_cdk.aws_route53resolver as route53resolver
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__f32e566319bfc3393a2d03856cc23ffdfe43494882d9e63a553fce46edf9c906)
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
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnResolverEndpoint.IpAddressRequestProperty]]]:
        '''The subnets and IP addresses in your VPC that DNS queries originate from (for outbound endpoints) or that you forward DNS queries to (for inbound endpoints).

        The subnet ID uniquely identifies a VPC.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-ipaddresses
        '''
        result = self._values.get("ip_addresses")
        assert result is not None, "Required property 'ip_addresses' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnResolverEndpoint.IpAddressRequestProperty]]], result)

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
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Route 53 Resolver doesn't support updating tags through CloudFormation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverendpoint.html#cfn-route53resolver-resolverendpoint-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResolverEndpointProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResolverQueryLoggingConfig(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53resolver.CfnResolverQueryLoggingConfig",
):
    '''A CloudFormation ``AWS::Route53Resolver::ResolverQueryLoggingConfig``.

    The AWS::Route53Resolver::ResolverQueryLoggingConfig resource is a complex type that contains settings for one query logging configuration.

    :cloudformationResource: AWS::Route53Resolver::ResolverQueryLoggingConfig
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfig.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_route53resolver as route53resolver
        
        cfn_resolver_query_logging_config = route53resolver.CfnResolverQueryLoggingConfig(self, "MyCfnResolverQueryLoggingConfig",
            destination_arn="destinationArn",
            name="name"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__11aa84a7b17f49d1ae47dfa7c80d4304ea6f866b4fa4ccb531678b5e814f8a0a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResolverQueryLoggingConfigProps(
            destination_arn=destination_arn, name=name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__858410bc936c545afafcf278058f32e3d7f74dcd562577a03d27a6119e843484)
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
            type_hints = typing.get_type_hints(_typecheckingstub__35dc01cfe085dc2b8ccfe401b77a12478b38bccd1383c3282c91ad1e43375bdd)
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
            type_hints = typing.get_type_hints(_typecheckingstub__55931d3f5405909c55b7e03ede2e883abe98ff5aa4a275d0f096c8315286677b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6967f5655e423190514e5b6e0558355c1850433170ee69e13b757cb708a28e73)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResolverQueryLoggingConfigAssociation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53resolver.CfnResolverQueryLoggingConfigAssociation",
):
    '''A CloudFormation ``AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation``.

    The AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation resource is a configuration for DNS query logging. After you create a query logging configuration, Amazon Route 53 begins to publish log data to an Amazon CloudWatch Logs log group.

    :cloudformationResource: AWS::Route53Resolver::ResolverQueryLoggingConfigAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverqueryloggingconfigassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_route53resolver as route53resolver
        
        cfn_resolver_query_logging_config_association = route53resolver.CfnResolverQueryLoggingConfigAssociation(self, "MyCfnResolverQueryLoggingConfigAssociation",
            resolver_query_log_config_id="resolverQueryLogConfigId",
            resource_id="resourceId"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__6223b33a8d4a94764880b3a2abe32bba659e0a35551baf1b0dd1230ebd9e6f50)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResolverQueryLoggingConfigAssociationProps(
            resolver_query_log_config_id=resolver_query_log_config_id,
            resource_id=resource_id,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82529e5f65e65d6234719060e9b03997b923afbf843baf522c2c627562fc30c7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__559e5d28a1616637b787453e13014d00242e98b78be3bc1872d8b2e98a96ab2b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__49eb40f85ee4fce7783a3ef41c04f2f58f486c714fe987efdf5a7850e7bbe1d2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__111d7ae08e2d92dc37a5b780728770324e672ef980439721a63295f43b3eed29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceId", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53resolver.CfnResolverQueryLoggingConfigAssociationProps",
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
            import aws_cdk.aws_route53resolver as route53resolver
            
            cfn_resolver_query_logging_config_association_props = route53resolver.CfnResolverQueryLoggingConfigAssociationProps(
                resolver_query_log_config_id="resolverQueryLogConfigId",
                resource_id="resourceId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__856009a975191ea70f0ffd8eb4c7058978e730cb33bf4fa481054db13c336e49)
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
    jsii_type="@aws-cdk/aws-route53resolver.CfnResolverQueryLoggingConfigProps",
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
            import aws_cdk.aws_route53resolver as route53resolver
            
            cfn_resolver_query_logging_config_props = route53resolver.CfnResolverQueryLoggingConfigProps(
                destination_arn="destinationArn",
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1df63e3e21495930aefcb9e86948e0dd7892a75892ff711eca5f34f2eba9fe76)
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResolverRule(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53resolver.CfnResolverRule",
):
    '''A CloudFormation ``AWS::Route53Resolver::ResolverRule``.

    For DNS queries that originate in your VPCs, specifies which Resolver endpoint the queries pass through, one domain name that you want to forward to your network, and the IP addresses of the DNS resolvers in your network.

    :cloudformationResource: AWS::Route53Resolver::ResolverRule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_route53resolver as route53resolver
        
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
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        domain_name: builtins.str,
        rule_type: builtins.str,
        name: typing.Optional[builtins.str] = None,
        resolver_endpoint_id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_ips: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnResolverRule.TargetAddressProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
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
            type_hints = typing.get_type_hints(_typecheckingstub__784369a87cfbb0af3cd22d3c1e981c2861410755f85de47df12a1918f79b05d7)
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
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec562c10ec566ac141820d4082a801a3c04e3aca636ce5044a4be6c1ca1d04a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d6a3bc53c1fb07f5e65d1da0b60d0027e70ac6161aede74b2bca401bc148e865)
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
    def attr_target_ips(self) -> _aws_cdk_core_f4b25747.IResolvable:
        '''When the value of ``RuleType`` is ``FORWARD`` , the IP addresses that the outbound endpoint forwards DNS queries to, typically the IP addresses for DNS resolvers on your network.

        This value isn't applicable when ``RuleType`` is ``SYSTEM`` .

        :cloudformationAttribute: TargetIps
        '''
        return typing.cast(_aws_cdk_core_f4b25747.IResolvable, jsii.get(self, "attrTargetIps"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''Route 53 Resolver doesn't support updating tags through CloudFormation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__ec8530e8611adc5bf92360527a1581f33a3f01bb7819b8cceae201ed7b71ae09)
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
            type_hints = typing.get_type_hints(_typecheckingstub__54f4b1416e4574b2620f66912e68d15405d3252dcaf4cc699153c96baa271f7c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5127f2596a5d558d46167ce21639ac693ba12a1ac2d3d73566ffc52b6469fdb1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__45bb23b8773b0d9d4f4924ffd181e034fe6423ee815598955854e742cf1d06ae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resolverEndpointId", value)

    @builtins.property
    @jsii.member(jsii_name="targetIps")
    def target_ips(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResolverRule.TargetAddressProperty"]]]]:
        '''An array that contains the IP addresses and ports that an outbound endpoint forwards DNS queries to.

        Typically, these are the IP addresses of DNS resolvers on your network. Specify IPv4 addresses. IPv6 is not supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-targetips
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResolverRule.TargetAddressProperty"]]]], jsii.get(self, "targetIps"))

    @target_ips.setter
    def target_ips(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnResolverRule.TargetAddressProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ed3305ca4fde7368139860be9e498751894a62eaa570cdd7eabb9821780d44c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targetIps", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-route53resolver.CfnResolverRule.TargetAddressProperty",
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
                import aws_cdk.aws_route53resolver as route53resolver
                
                target_address_property = route53resolver.CfnResolverRule.TargetAddressProperty(
                    ip="ip",
                
                    # the properties below are optional
                    port="port"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__dd7184c1f43cb77c810e7889e140dea98437d4b010b9499f01e468f506a41a16)
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


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResolverRuleAssociation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53resolver.CfnResolverRuleAssociation",
):
    '''A CloudFormation ``AWS::Route53Resolver::ResolverRuleAssociation``.

    In the response to an `AssociateResolverRule <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_AssociateResolverRule.html>`_ , `DisassociateResolverRule <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_DisassociateResolverRule.html>`_ , or `ListResolverRuleAssociations <https://docs.aws.amazon.com/Route53/latest/APIReference/API_route53resolver_ListResolverRuleAssociations.html>`_ request, provides information about an association between a resolver rule and a VPC. The association determines which DNS queries that originate in the VPC are forwarded to your network.

    :cloudformationResource: AWS::Route53Resolver::ResolverRuleAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverruleassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_route53resolver as route53resolver
        
        cfn_resolver_rule_association = route53resolver.CfnResolverRuleAssociation(self, "MyCfnResolverRuleAssociation",
            resolver_rule_id="resolverRuleId",
            vpc_id="vpcId",
        
            # the properties below are optional
            name="name"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
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
            type_hints = typing.get_type_hints(_typecheckingstub__8d2424378edf612b301d2786f47264e2d974e854ab15dae8e755f7e6b6d63853)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResolverRuleAssociationProps(
            resolver_rule_id=resolver_rule_id, vpc_id=vpc_id, name=name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a6b375f80ddf1d6b9a8a6de909b3ab1a9a28b34e5767f06232dc151a43f1d4d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ad41e83d189f48c2923759249e93e8e5524fe58590a54dbfcf50da18c58de9d1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__632295079ccdaf5c920b48a7471f91e12ac08c68f0eb21938aa7a0231bd830e7)
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
            type_hints = typing.get_type_hints(_typecheckingstub__85d8313100b4080122bc360f2b159f9b350c5f23b5c80f2cad109c0c34f2da5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cebe42128467c3a054cf6abee4e6a8c1f6213af91a02984fec63d8177696379b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53resolver.CfnResolverRuleAssociationProps",
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
            import aws_cdk.aws_route53resolver as route53resolver
            
            cfn_resolver_rule_association_props = route53resolver.CfnResolverRuleAssociationProps(
                resolver_rule_id="resolverRuleId",
                vpc_id="vpcId",
            
                # the properties below are optional
                name="name"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d571650de0f3ae84e830f15588c90b1273702ede7ba054a7ca83c7b602930cd)
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
    jsii_type="@aws-cdk/aws-route53resolver.CfnResolverRuleProps",
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
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        target_ips: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResolverRule.TargetAddressProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
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
            import aws_cdk.aws_route53resolver as route53resolver
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__42a30067d388e6553fb13a649c28786a7fcae87ba766c22b03c63261b9f02d01)
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
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''Route 53 Resolver doesn't support updating tags through CloudFormation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def target_ips(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnResolverRule.TargetAddressProperty]]]]:
        '''An array that contains the IP addresses and ports that an outbound endpoint forwards DNS queries to.

        Typically, these are the IP addresses of DNS resolvers on your network. Specify IPv4 addresses. IPv6 is not supported.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53resolver-resolverrule.html#cfn-route53resolver-resolverrule-targetips
        '''
        result = self._values.get("target_ips")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnResolverRule.TargetAddressProperty]]]], result)

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
    jsii_type="@aws-cdk/aws-route53resolver.DnsBlockResponse",
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
        ttl: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
    ) -> "DnsBlockResponse":
        '''(experimental) Provides a custom override response to the query.

        :param domain: The custom DNS record to send back in response to the query.
        :param ttl: The recommended amount of time for the DNS resolver or web browser to cache the provided override record.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53d7727018e7c85ce2eed37247b337e71c20f3cfd16cab4fbda93c5b971dd556)
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
    def block_override_ttl(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
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
    def block_override_ttl(self) -> typing.Optional[_aws_cdk_core_f4b25747.Duration]:
        '''(experimental) The recommended amount of time for the DNS resolver or web browser to cache the provided override record.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_aws_cdk_core_f4b25747.Duration], jsii.get(self, "blockOverrideTtl"))

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
    jsii_type="@aws-cdk/aws-route53resolver.DomainsConfig",
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
            import aws_cdk.aws_route53resolver as route53resolver
            
            domains_config = route53resolver.DomainsConfig(
                domain_file_url="domainFileUrl",
                domains=["domains"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63a865a2969790a9d2fec18a240395048da17b33b046654f1f50f09626924c93)
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
    jsii_type="@aws-cdk/aws-route53resolver.FirewallDomainListProps",
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
            type_hints = typing.get_type_hints(_typecheckingstub__46f3704d348876337963bf2319bcfb485f299276572fdc852a740ba1c1d03c1a)
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
    jsii_type="@aws-cdk/aws-route53resolver.FirewallDomains",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6e945cd5e4d2ef258bf7855d82fb839595afcfacfaef38a3af20658417bf448c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__50143eca574a12d3602c84d1a1602d61420c373b78857cba481c96d29687ed97)
            check_type(argname="argument list", value=list, expected_type=type_hints["list"])
        return typing.cast("FirewallDomains", jsii.sinvoke(cls, "fromList", [list]))

    @jsii.member(jsii_name="fromS3")
    @builtins.classmethod
    def from_s3(
        cls,
        bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
        key: builtins.str,
    ) -> "FirewallDomains":
        '''(experimental) Firewall domains created from a file stored in Amazon S3.

        The file must be a text file and must contain a single domain per line.
        The content type of the S3 object must be ``plain/text``.

        :param bucket: S3 bucket.
        :param key: S3 key.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6faf1db81750bb7f1e1fb001cee814dae3ba2cff1de3b49f6eecfe17c3120847)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8c98c991b06c041e792a43558c56236312ec43ea263d06b6fdcd91bf04c11290)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a964d42544ecfca8f3b4e4dab53aa807f73310ba3b7a81c7c5e8171f3d67e34)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(DomainsConfig, jsii.invoke(self, "bind", [scope]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, FirewallDomains).__jsii_proxy_class__ = lambda : _FirewallDomainsProxy


@jsii.data_type(
    jsii_type="@aws-cdk/aws-route53resolver.FirewallRule",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5caae1a7e88f6902a3293e3de2067198d6f96279dffea8e06011d6febcf92c6b)
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
    jsii_type="@aws-cdk/aws-route53resolver.FirewallRuleAction",
):
    '''(experimental) A Firewall Rule.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_block_list: route53resolver.FirewallDomainList
        
        route53resolver.FirewallRuleGroup(self, "RuleGroup",
            rules=[route53resolver.FirewallRule(
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
            type_hints = typing.get_type_hints(_typecheckingstub__b62b11d5411f8429888d1ce6fbb6414de6364cba9b386839b9507f6e48564ae6)
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
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53resolver.FirewallRuleGroupAssociation",
):
    '''(experimental) A Firewall Rule Group Association.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_ec2 as ec2
        import aws_cdk.aws_route53resolver as route53resolver
        
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
        vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
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
            type_hints = typing.get_type_hints(_typecheckingstub__20ededd874bfe603d868639affb4754502c80b3e1d097aad8e5ab3845ed0e2d2)
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
    jsii_type="@aws-cdk/aws-route53resolver.FirewallRuleGroupAssociationOptions",
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
        vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
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

            import aws_cdk.aws_ec2 as ec2
            
            # rule_group: route53resolver.FirewallRuleGroup
            # my_vpc: ec2.Vpc
            
            
            rule_group.associate("Association",
                priority=101,
                vpc=my_vpc
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7fb265ff67f1138c6c732cf1a2849036e4aabfa59508b9ef2bf414610cf024e)
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
    def vpc(self) -> _aws_cdk_aws_ec2_67de8e8d.IVpc:
        '''(experimental) The VPC that to associate with the rule group.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_67de8e8d.IVpc, result)

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
    jsii_type="@aws-cdk/aws-route53resolver.FirewallRuleGroupAssociationProps",
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
        vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
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
            import aws_cdk.aws_ec2 as ec2
            import aws_cdk.aws_route53resolver as route53resolver
            
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
            type_hints = typing.get_type_hints(_typecheckingstub__7ceab2600db7f470a5252983f173d04d328113e021d85c48f35059120ea329fc)
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
    def vpc(self) -> _aws_cdk_aws_ec2_67de8e8d.IVpc:
        '''(experimental) The VPC that to associate with the rule group.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        assert result is not None, "Required property 'vpc' is missing"
        return typing.cast(_aws_cdk_aws_ec2_67de8e8d.IVpc, result)

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
    jsii_type="@aws-cdk/aws-route53resolver.FirewallRuleGroupProps",
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
                rules=[route53resolver.FirewallRule(
                    priority=10,
                    firewall_domain_list=my_block_list,
                    # block and reply with NODATA
                    action=route53resolver.FirewallRuleAction.block()
                )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8373fb60fb443280023a778575116819f92fbfee6dbaf53f0166f3ce39b74506)
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


@jsii.interface(jsii_type="@aws-cdk/aws-route53resolver.IFirewallDomainList")
class IFirewallDomainList(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
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
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''(experimental) A Firewall Domain List.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-route53resolver.IFirewallDomainList"

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


@jsii.interface(jsii_type="@aws-cdk/aws-route53resolver.IFirewallRuleGroup")
class IFirewallRuleGroup(_aws_cdk_core_f4b25747.IResource, typing_extensions.Protocol):
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
    jsii.proxy_for(_aws_cdk_core_f4b25747.IResource), # type: ignore[misc]
):
    '''(experimental) A Firewall Rule Group.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "@aws-cdk/aws-route53resolver.IFirewallRuleGroup"

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
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53resolver.FirewallDomainList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6bdff0411b666f2d5a7b8726994c268714361cbef982501bd84554f9a511c850)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e213f2e0869b302b94cc78cbb468d70c05f97baf192e2655e8446809d932bcc0)
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
    _aws_cdk_core_f4b25747.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-route53resolver.FirewallRuleGroup",
):
    '''(experimental) A Firewall Rule Group.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # my_block_list: route53resolver.FirewallDomainList
        
        route53resolver.FirewallRuleGroup(self, "RuleGroup",
            rules=[route53resolver.FirewallRule(
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
            type_hints = typing.get_type_hints(_typecheckingstub__b130111fced23c2ab5d737b99b11a338606caf3964865731319d824662bcd23b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d844c8b7e4b91f8b4e646b3b823866cfd61547c61bc2ee20ace169e9d5a7873f)
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
        vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
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
            type_hints = typing.get_type_hints(_typecheckingstub__acea5f4208addf0f390b68f783a36233a567be66f053360377e64700778e6d23)
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

def _typecheckingstub__555ddf44c52202073669f04898e1d37d30920953457df6c2777354f621bbc1df(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    domain_file_url: typing.Optional[builtins.str] = None,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08e29bb557e2e76340b8cbc1298149289e09169f65b20b0f49bd4ebb52b10e38(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a913e52a37e888ffe82f9861b33ad50d5ef2abae73269f505289e98f52183423(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b6b7ed4d47c8736285ad482281a7b3a1a1e81f2376643f4251ce79ddbde052fa(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11f8fa0dd52a7a6cd1195b3c25648bcaab780b5a3696d85c221646fa1fd89e7(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__978620f1b5655f35805cd034fc43012d548ff6be263db3b871b140f11dd963d5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a68481722a8554b1fb0d83ce84d5ca9bda73a49a5bc12894b557efc66d9cbded(
    *,
    domain_file_url: typing.Optional[builtins.str] = None,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c10bd5f5a59548a6fde2daff1a043b2d05a3dbdca2c182e143bc7ba6da166f2b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    firewall_rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnFirewallRuleGroup.FirewallRuleProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12eb1fd98f8c18afc6088fe831fa5fcfd0837476b45a1159e69ed007a6e899df(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e64244c2524e24b6af62cbb286f9e7a5a63d48b4fe367feb6b860163f1fc9495(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a481a8bc47312623972b69d3087e645728b2f9b78934d5f78ab6203492d26c(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnFirewallRuleGroup.FirewallRuleProperty, _aws_cdk_core_f4b25747.IResolvable]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84ebd3fb9929801bc7cb9f22cb9a03f8fc34eda98f48e63b1cee8b5930bcbb21(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3779e3ea3239883a621bc04756bc0f3df09f8eebecb91da90dc56be9205ae50e(
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

def _typecheckingstub__0308fe827e6b3a3505bb28772723d284420b4c739e09c3060d8f7f39d6ae42cc(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    firewall_rule_group_id: builtins.str,
    priority: jsii.Number,
    vpc_id: builtins.str,
    mutation_protection: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd042463d0ef7afc78b157b6eb30682902ab9d2344d445ea05af79895dcdc99(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__385585373172aa6f61e20137d7c1f935386f3242974798eed9d693d637ceeae8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fd218820098418e72092e2ba6ef94e0f11f0c861f6f1dac62098098e4755cff(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ebf1fc36cdbc20218fac8207f2303ddec5d14aa012bc8d672995aa8d5f40bb2(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e55a689213e73bb6e6c235b317f32e82c66c292c0b56c3285436a8b8968bad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59361570296280c2314024828f4a094bfaa38a1aea0076a13a6f77f1561594f4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aefb06222c531912656dfa642f05e71e8a22f8383d2d02b7ae21721529f83ba5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7d6b680ce1909bd9e556e0c8d07ab6ae4fdebc59f24dd7d18991d12a390ebb8(
    *,
    firewall_rule_group_id: builtins.str,
    priority: jsii.Number,
    vpc_id: builtins.str,
    mutation_protection: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__998a30eb443c97b4395f3eb88dcd151f4aa7cc24743f30442f96ad8cb02d3e9d(
    *,
    firewall_rules: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnFirewallRuleGroup.FirewallRuleProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6d3e01eb13ecf3fc6c09139de1f8804ab22038ba2a08712e02cddec75e0547b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    autodefined_reverse_flag: builtins.str,
    resource_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ff6afd670bb17b6410b44928cecd96d8b3137c72236d3e891f52a2f500a575e(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d767bbf2f5ebd1cc854d78b1a1125125598aaa0f095e12f069fbae675ea6dd34(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dbc6a7c7789751dd260c52ff2e78afe6a649ab277d4036f734500536b7a92b7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d61341477aa7e147988292017c7c80c2752ce11cdbfe3f7da2ef3cd56b6cfd8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ee753ccc06b40acc70153c14525b069b3d66517d509ebd5b18ace9d9c824125e(
    *,
    autodefined_reverse_flag: builtins.str,
    resource_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfcd15a3243b968afe8fa16337f0415ba17445d3954fb52ea95f3e589b892b1f(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__625478d24808c52e1e15238c1169fd1cd2172fd4736f6117ee56647c76f689f6(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__364031598a568d1e2a20c6789c9fb23c57fa1726ab70fc40da1fe3980c8b3190(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__206998a6ef9b2b46ce0c9a91a46a0da70f9101365fbe8d8b7297ebe2f70bb4dc(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3e338f0817ab8ead305559a7d148631ac62f113c42c76c5c4cfe9c7adcf7d87(
    *,
    resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__228e1f20142fd9984b3c82b6521decf17f34fc81d79d98c85485f678d145729c(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    direction: builtins.str,
    ip_addresses: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResolverEndpoint.IpAddressRequestProperty, typing.Dict[builtins.str, typing.Any]]]]],
    security_group_ids: typing.Sequence[builtins.str],
    name: typing.Optional[builtins.str] = None,
    outpost_arn: typing.Optional[builtins.str] = None,
    preferred_instance_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84bfe3cd1240054055dc29a4fdfc754b3333af826720c64decca9039930c4318(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20a59c29bf5bb6a3d9002aaf6ee9e9f710a4abc168f5cf282569e5e2494b368d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b665109081bf00e85db2eb699f45cb6f55d13d9210ec905b8eb8867e6e245751(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7d88633eb435aab3516dfa96767c4f8b505d109633de12cd43d3750eb092033(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnResolverEndpoint.IpAddressRequestProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cefeb21a499e0edf6e954313e30c569992fec8a2de10bc01ffe291f859d7c99a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9b839ede89a09d1722701e891816be340198e9741ffdee30268f531135c3765(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b41c01da0809295e4e46099b679cee1337253316f0ca65e603790eb13d1832d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__538e4fe27f851288c87e30ff97dd25de4c72cc10ced2af8bbe42d84669ffca6f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d8a364815a9377d601e54826e2e2fdc73a177d1914877aae6e757c33d2feaf(
    *,
    subnet_id: builtins.str,
    ip: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f32e566319bfc3393a2d03856cc23ffdfe43494882d9e63a553fce46edf9c906(
    *,
    direction: builtins.str,
    ip_addresses: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResolverEndpoint.IpAddressRequestProperty, typing.Dict[builtins.str, typing.Any]]]]],
    security_group_ids: typing.Sequence[builtins.str],
    name: typing.Optional[builtins.str] = None,
    outpost_arn: typing.Optional[builtins.str] = None,
    preferred_instance_type: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11aa84a7b17f49d1ae47dfa7c80d4304ea6f866b4fa4ccb531678b5e814f8a0a(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    destination_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__858410bc936c545afafcf278058f32e3d7f74dcd562577a03d27a6119e843484(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35dc01cfe085dc2b8ccfe401b77a12478b38bccd1383c3282c91ad1e43375bdd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55931d3f5405909c55b7e03ede2e883abe98ff5aa4a275d0f096c8315286677b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6967f5655e423190514e5b6e0558355c1850433170ee69e13b757cb708a28e73(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6223b33a8d4a94764880b3a2abe32bba659e0a35551baf1b0dd1230ebd9e6f50(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    resolver_query_log_config_id: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82529e5f65e65d6234719060e9b03997b923afbf843baf522c2c627562fc30c7(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__559e5d28a1616637b787453e13014d00242e98b78be3bc1872d8b2e98a96ab2b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__49eb40f85ee4fce7783a3ef41c04f2f58f486c714fe987efdf5a7850e7bbe1d2(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__111d7ae08e2d92dc37a5b780728770324e672ef980439721a63295f43b3eed29(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__856009a975191ea70f0ffd8eb4c7058978e730cb33bf4fa481054db13c336e49(
    *,
    resolver_query_log_config_id: typing.Optional[builtins.str] = None,
    resource_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1df63e3e21495930aefcb9e86948e0dd7892a75892ff711eca5f34f2eba9fe76(
    *,
    destination_arn: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__784369a87cfbb0af3cd22d3c1e981c2861410755f85de47df12a1918f79b05d7(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    domain_name: builtins.str,
    rule_type: builtins.str,
    name: typing.Optional[builtins.str] = None,
    resolver_endpoint_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_ips: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResolverRule.TargetAddressProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec562c10ec566ac141820d4082a801a3c04e3aca636ce5044a4be6c1ca1d04a(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6a3bc53c1fb07f5e65d1da0b60d0027e70ac6161aede74b2bca401bc148e865(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec8530e8611adc5bf92360527a1581f33a3f01bb7819b8cceae201ed7b71ae09(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f4b1416e4574b2620f66912e68d15405d3252dcaf4cc699153c96baa271f7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5127f2596a5d558d46167ce21639ac693ba12a1ac2d3d73566ffc52b6469fdb1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45bb23b8773b0d9d4f4924ffd181e034fe6423ee815598955854e742cf1d06ae(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ed3305ca4fde7368139860be9e498751894a62eaa570cdd7eabb9821780d44c(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnResolverRule.TargetAddressProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7184c1f43cb77c810e7889e140dea98437d4b010b9499f01e468f506a41a16(
    *,
    ip: builtins.str,
    port: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d2424378edf612b301d2786f47264e2d974e854ab15dae8e755f7e6b6d63853(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    resolver_rule_id: builtins.str,
    vpc_id: builtins.str,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a6b375f80ddf1d6b9a8a6de909b3ab1a9a28b34e5767f06232dc151a43f1d4d(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad41e83d189f48c2923759249e93e8e5524fe58590a54dbfcf50da18c58de9d1(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__632295079ccdaf5c920b48a7471f91e12ac08c68f0eb21938aa7a0231bd830e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85d8313100b4080122bc360f2b159f9b350c5f23b5c80f2cad109c0c34f2da5a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cebe42128467c3a054cf6abee4e6a8c1f6213af91a02984fec63d8177696379b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d571650de0f3ae84e830f15588c90b1273702ede7ba054a7ca83c7b602930cd(
    *,
    resolver_rule_id: builtins.str,
    vpc_id: builtins.str,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42a30067d388e6553fb13a649c28786a7fcae87ba766c22b03c63261b9f02d01(
    *,
    domain_name: builtins.str,
    rule_type: builtins.str,
    name: typing.Optional[builtins.str] = None,
    resolver_endpoint_id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    target_ips: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnResolverRule.TargetAddressProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53d7727018e7c85ce2eed37247b337e71c20f3cfd16cab4fbda93c5b971dd556(
    domain: builtins.str,
    ttl: typing.Optional[_aws_cdk_core_f4b25747.Duration] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63a865a2969790a9d2fec18a240395048da17b33b046654f1f50f09626924c93(
    *,
    domain_file_url: typing.Optional[builtins.str] = None,
    domains: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46f3704d348876337963bf2319bcfb485f299276572fdc852a740ba1c1d03c1a(
    *,
    domains: FirewallDomains,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6e945cd5e4d2ef258bf7855d82fb839595afcfacfaef38a3af20658417bf448c(
    asset_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50143eca574a12d3602c84d1a1602d61420c373b78857cba481c96d29687ed97(
    list: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6faf1db81750bb7f1e1fb001cee814dae3ba2cff1de3b49f6eecfe17c3120847(
    bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
    key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c98c991b06c041e792a43558c56236312ec43ea263d06b6fdcd91bf04c11290(
    url: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a964d42544ecfca8f3b4e4dab53aa807f73310ba3b7a81c7c5e8171f3d67e34(
    scope: _constructs_77d1e7e8.Construct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5caae1a7e88f6902a3293e3de2067198d6f96279dffea8e06011d6febcf92c6b(
    *,
    action: FirewallRuleAction,
    firewall_domain_list: IFirewallDomainList,
    priority: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b62b11d5411f8429888d1ce6fbb6414de6364cba9b386839b9507f6e48564ae6(
    response: typing.Optional[DnsBlockResponse] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20ededd874bfe603d868639affb4754502c80b3e1d097aad8e5ab3845ed0e2d2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    firewall_rule_group: IFirewallRuleGroup,
    priority: jsii.Number,
    vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
    mutation_protection: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7fb265ff67f1138c6c732cf1a2849036e4aabfa59508b9ef2bf414610cf024e(
    *,
    priority: jsii.Number,
    vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
    mutation_protection: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ceab2600db7f470a5252983f173d04d328113e021d85c48f35059120ea329fc(
    *,
    priority: jsii.Number,
    vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
    mutation_protection: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
    firewall_rule_group: IFirewallRuleGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8373fb60fb443280023a778575116819f92fbfee6dbaf53f0166f3ce39b74506(
    *,
    name: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[FirewallRule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6bdff0411b666f2d5a7b8726994c268714361cbef982501bd84554f9a511c850(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    domains: FirewallDomains,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e213f2e0869b302b94cc78cbb468d70c05f97baf192e2655e8446809d932bcc0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    firewall_domain_list_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b130111fced23c2ab5d737b99b11a338606caf3964865731319d824662bcd23b(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    name: typing.Optional[builtins.str] = None,
    rules: typing.Optional[typing.Sequence[typing.Union[FirewallRule, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d844c8b7e4b91f8b4e646b3b823866cfd61547c61bc2ee20ace169e9d5a7873f(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    firewall_rule_group_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__acea5f4208addf0f390b68f783a36233a567be66f053360377e64700778e6d23(
    id: builtins.str,
    *,
    priority: jsii.Number,
    vpc: _aws_cdk_aws_ec2_67de8e8d.IVpc,
    mutation_protection: typing.Optional[builtins.bool] = None,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
