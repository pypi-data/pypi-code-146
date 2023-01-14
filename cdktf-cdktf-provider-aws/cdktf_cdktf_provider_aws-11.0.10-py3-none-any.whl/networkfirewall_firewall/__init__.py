'''
# `aws_networkfirewall_firewall`

Refer to the Terraform Registory for docs: [`aws_networkfirewall_firewall`](https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall).
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

import cdktf as _cdktf_9a9027ec
import constructs as _constructs_77d1e7e8


class NetworkfirewallFirewall(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.networkfirewallFirewall.NetworkfirewallFirewall",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall aws_networkfirewall_firewall}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        firewall_policy_arn: builtins.str,
        name: builtins.str,
        subnet_mapping: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkfirewallFirewallSubnetMapping", typing.Dict[builtins.str, typing.Any]]]],
        vpc_id: builtins.str,
        delete_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_configuration: typing.Optional[typing.Union["NetworkfirewallFirewallEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        firewall_policy_change_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        subnet_change_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall aws_networkfirewall_firewall} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param firewall_policy_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#firewall_policy_arn NetworkfirewallFirewall#firewall_policy_arn}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#name NetworkfirewallFirewall#name}.
        :param subnet_mapping: subnet_mapping block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#subnet_mapping NetworkfirewallFirewall#subnet_mapping}
        :param vpc_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#vpc_id NetworkfirewallFirewall#vpc_id}.
        :param delete_protection: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#delete_protection NetworkfirewallFirewall#delete_protection}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#description NetworkfirewallFirewall#description}.
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#encryption_configuration NetworkfirewallFirewall#encryption_configuration}
        :param firewall_policy_change_protection: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#firewall_policy_change_protection NetworkfirewallFirewall#firewall_policy_change_protection}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#id NetworkfirewallFirewall#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param subnet_change_protection: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#subnet_change_protection NetworkfirewallFirewall#subnet_change_protection}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#tags NetworkfirewallFirewall#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#tags_all NetworkfirewallFirewall#tags_all}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4df79298a403bbe89bcce45294cd2cef752ab819b09aa7c705835855392f469d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = NetworkfirewallFirewallConfig(
            firewall_policy_arn=firewall_policy_arn,
            name=name,
            subnet_mapping=subnet_mapping,
            vpc_id=vpc_id,
            delete_protection=delete_protection,
            description=description,
            encryption_configuration=encryption_configuration,
            firewall_policy_change_protection=firewall_policy_change_protection,
            id=id,
            subnet_change_protection=subnet_change_protection,
            tags=tags,
            tags_all=tags_all,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putEncryptionConfiguration")
    def put_encryption_configuration(
        self,
        *,
        type: builtins.str,
        key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#type NetworkfirewallFirewall#type}.
        :param key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#key_id NetworkfirewallFirewall#key_id}.
        '''
        value = NetworkfirewallFirewallEncryptionConfiguration(
            type=type, key_id=key_id
        )

        return typing.cast(None, jsii.invoke(self, "putEncryptionConfiguration", [value]))

    @jsii.member(jsii_name="putSubnetMapping")
    def put_subnet_mapping(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkfirewallFirewallSubnetMapping", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c40d12ed03db2812ea3d779f0627430d5be989ee789eb9e8c34a40705ec9ad43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putSubnetMapping", [value]))

    @jsii.member(jsii_name="resetDeleteProtection")
    def reset_delete_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDeleteProtection", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEncryptionConfiguration")
    def reset_encryption_configuration(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEncryptionConfiguration", []))

    @jsii.member(jsii_name="resetFirewallPolicyChangeProtection")
    def reset_firewall_policy_change_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetFirewallPolicyChangeProtection", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetSubnetChangeProtection")
    def reset_subnet_change_protection(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubnetChangeProtection", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTagsAll")
    def reset_tags_all(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTagsAll", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfiguration")
    def encryption_configuration(
        self,
    ) -> "NetworkfirewallFirewallEncryptionConfigurationOutputReference":
        return typing.cast("NetworkfirewallFirewallEncryptionConfigurationOutputReference", jsii.get(self, "encryptionConfiguration"))

    @builtins.property
    @jsii.member(jsii_name="firewallStatus")
    def firewall_status(self) -> "NetworkfirewallFirewallFirewallStatusList":
        return typing.cast("NetworkfirewallFirewallFirewallStatusList", jsii.get(self, "firewallStatus"))

    @builtins.property
    @jsii.member(jsii_name="subnetMapping")
    def subnet_mapping(self) -> "NetworkfirewallFirewallSubnetMappingList":
        return typing.cast("NetworkfirewallFirewallSubnetMappingList", jsii.get(self, "subnetMapping"))

    @builtins.property
    @jsii.member(jsii_name="updateToken")
    def update_token(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "updateToken"))

    @builtins.property
    @jsii.member(jsii_name="deleteProtectionInput")
    def delete_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "deleteProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="encryptionConfigurationInput")
    def encryption_configuration_input(
        self,
    ) -> typing.Optional["NetworkfirewallFirewallEncryptionConfiguration"]:
        return typing.cast(typing.Optional["NetworkfirewallFirewallEncryptionConfiguration"], jsii.get(self, "encryptionConfigurationInput"))

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyArnInput")
    def firewall_policy_arn_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "firewallPolicyArnInput"))

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyChangeProtectionInput")
    def firewall_policy_change_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "firewallPolicyChangeProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetChangeProtectionInput")
    def subnet_change_protection_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "subnetChangeProtectionInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetMappingInput")
    def subnet_mapping_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkfirewallFirewallSubnetMapping"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkfirewallFirewallSubnetMapping"]]], jsii.get(self, "subnetMappingInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsAllInput")
    def tags_all_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsAllInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="vpcIdInput")
    def vpc_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteProtection")
    def delete_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "deleteProtection"))

    @delete_protection.setter
    def delete_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__832eb09d6d943d1effbdbd58523e082896d2e88dc3c36df1784f88018a83d2b2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteProtection", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10dd7a04fc4c42cd6c5c8bb65a91e4f940fc451a5258ff90ad65c99091ec65b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyArn")
    def firewall_policy_arn(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "firewallPolicyArn"))

    @firewall_policy_arn.setter
    def firewall_policy_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca7f6bbf3dd4527bb9cb8c4a33a7880796afae7bc7528ca52d31d852ffeeae6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallPolicyArn", value)

    @builtins.property
    @jsii.member(jsii_name="firewallPolicyChangeProtection")
    def firewall_policy_change_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "firewallPolicyChangeProtection"))

    @firewall_policy_change_protection.setter
    def firewall_policy_change_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfac85d3329ef009dadee5980129e87ad2a51c60cfa4f27d274db34365584b20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "firewallPolicyChangeProtection", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ada83a2d080c91ac27234ecdd8a6a9e15cb8440e3c1070ff4c5cdbb143059dd0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2df3c152242a5eb4af53b20459011bf1e8f8396e0add6f79a3545396586abe8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="subnetChangeProtection")
    def subnet_change_protection(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "subnetChangeProtection"))

    @subnet_change_protection.setter
    def subnet_change_protection(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20b3bb0afd8dc74894d70541f43a8b19a8a7c784de374b0dd1f6f59e8f8e816a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetChangeProtection", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecee0fa97eebe472cf1f9d1989ab510162d1a1d506d202b71123c97cfb04cec1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @builtins.property
    @jsii.member(jsii_name="tagsAll")
    def tags_all(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tagsAll"))

    @tags_all.setter
    def tags_all(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce618a695a6e552e629b9822dad387f09f1fb63ea5cb629605aebddce677a550)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tagsAll", value)

    @builtins.property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "vpcId"))

    @vpc_id.setter
    def vpc_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5adddf58740714142356f0e3182791bb89b6cd15cb5efd78ac09ea12efdffef1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.networkfirewallFirewall.NetworkfirewallFirewallConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "firewall_policy_arn": "firewallPolicyArn",
        "name": "name",
        "subnet_mapping": "subnetMapping",
        "vpc_id": "vpcId",
        "delete_protection": "deleteProtection",
        "description": "description",
        "encryption_configuration": "encryptionConfiguration",
        "firewall_policy_change_protection": "firewallPolicyChangeProtection",
        "id": "id",
        "subnet_change_protection": "subnetChangeProtection",
        "tags": "tags",
        "tags_all": "tagsAll",
    },
)
class NetworkfirewallFirewallConfig(_cdktf_9a9027ec.TerraformMetaArguments):
    def __init__(
        self,
        *,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
        firewall_policy_arn: builtins.str,
        name: builtins.str,
        subnet_mapping: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["NetworkfirewallFirewallSubnetMapping", typing.Dict[builtins.str, typing.Any]]]],
        vpc_id: builtins.str,
        delete_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        description: typing.Optional[builtins.str] = None,
        encryption_configuration: typing.Optional[typing.Union["NetworkfirewallFirewallEncryptionConfiguration", typing.Dict[builtins.str, typing.Any]]] = None,
        firewall_policy_change_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        subnet_change_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param firewall_policy_arn: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#firewall_policy_arn NetworkfirewallFirewall#firewall_policy_arn}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#name NetworkfirewallFirewall#name}.
        :param subnet_mapping: subnet_mapping block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#subnet_mapping NetworkfirewallFirewall#subnet_mapping}
        :param vpc_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#vpc_id NetworkfirewallFirewall#vpc_id}.
        :param delete_protection: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#delete_protection NetworkfirewallFirewall#delete_protection}.
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#description NetworkfirewallFirewall#description}.
        :param encryption_configuration: encryption_configuration block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#encryption_configuration NetworkfirewallFirewall#encryption_configuration}
        :param firewall_policy_change_protection: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#firewall_policy_change_protection NetworkfirewallFirewall#firewall_policy_change_protection}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#id NetworkfirewallFirewall#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param subnet_change_protection: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#subnet_change_protection NetworkfirewallFirewall#subnet_change_protection}.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#tags NetworkfirewallFirewall#tags}.
        :param tags_all: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#tags_all NetworkfirewallFirewall#tags_all}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(encryption_configuration, dict):
            encryption_configuration = NetworkfirewallFirewallEncryptionConfiguration(**encryption_configuration)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c31ae442b68278894c5ef8b24fecf770de2697e692f9c171f9539a6f21497502)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument firewall_policy_arn", value=firewall_policy_arn, expected_type=type_hints["firewall_policy_arn"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument subnet_mapping", value=subnet_mapping, expected_type=type_hints["subnet_mapping"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
            check_type(argname="argument delete_protection", value=delete_protection, expected_type=type_hints["delete_protection"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument encryption_configuration", value=encryption_configuration, expected_type=type_hints["encryption_configuration"])
            check_type(argname="argument firewall_policy_change_protection", value=firewall_policy_change_protection, expected_type=type_hints["firewall_policy_change_protection"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument subnet_change_protection", value=subnet_change_protection, expected_type=type_hints["subnet_change_protection"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument tags_all", value=tags_all, expected_type=type_hints["tags_all"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "firewall_policy_arn": firewall_policy_arn,
            "name": name,
            "subnet_mapping": subnet_mapping,
            "vpc_id": vpc_id,
        }
        if connection is not None:
            self._values["connection"] = connection
        if count is not None:
            self._values["count"] = count
        if depends_on is not None:
            self._values["depends_on"] = depends_on
        if for_each is not None:
            self._values["for_each"] = for_each
        if lifecycle is not None:
            self._values["lifecycle"] = lifecycle
        if provider is not None:
            self._values["provider"] = provider
        if provisioners is not None:
            self._values["provisioners"] = provisioners
        if delete_protection is not None:
            self._values["delete_protection"] = delete_protection
        if description is not None:
            self._values["description"] = description
        if encryption_configuration is not None:
            self._values["encryption_configuration"] = encryption_configuration
        if firewall_policy_change_protection is not None:
            self._values["firewall_policy_change_protection"] = firewall_policy_change_protection
        if id is not None:
            self._values["id"] = id
        if subnet_change_protection is not None:
            self._values["subnet_change_protection"] = subnet_change_protection
        if tags is not None:
            self._values["tags"] = tags
        if tags_all is not None:
            self._values["tags_all"] = tags_all

    @builtins.property
    def connection(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("connection")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, _cdktf_9a9027ec.WinrmProvisionerConnection]], result)

    @builtins.property
    def count(self) -> typing.Optional[jsii.Number]:
        '''
        :stability: experimental
        '''
        result = self._values.get("count")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def depends_on(
        self,
    ) -> typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("depends_on")
        return typing.cast(typing.Optional[typing.List[_cdktf_9a9027ec.ITerraformDependable]], result)

    @builtins.property
    def for_each(self) -> typing.Optional[_cdktf_9a9027ec.ITerraformIterator]:
        '''
        :stability: experimental
        '''
        result = self._values.get("for_each")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.ITerraformIterator], result)

    @builtins.property
    def lifecycle(self) -> typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle]:
        '''
        :stability: experimental
        '''
        result = self._values.get("lifecycle")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformResourceLifecycle], result)

    @builtins.property
    def provider(self) -> typing.Optional[_cdktf_9a9027ec.TerraformProvider]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[_cdktf_9a9027ec.TerraformProvider], result)

    @builtins.property
    def provisioners(
        self,
    ) -> typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]]:
        '''
        :stability: experimental
        '''
        result = self._values.get("provisioners")
        return typing.cast(typing.Optional[typing.List[typing.Union[_cdktf_9a9027ec.FileProvisioner, _cdktf_9a9027ec.LocalExecProvisioner, _cdktf_9a9027ec.RemoteExecProvisioner]]], result)

    @builtins.property
    def firewall_policy_arn(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#firewall_policy_arn NetworkfirewallFirewall#firewall_policy_arn}.'''
        result = self._values.get("firewall_policy_arn")
        assert result is not None, "Required property 'firewall_policy_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#name NetworkfirewallFirewall#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def subnet_mapping(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkfirewallFirewallSubnetMapping"]]:
        '''subnet_mapping block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#subnet_mapping NetworkfirewallFirewall#subnet_mapping}
        '''
        result = self._values.get("subnet_mapping")
        assert result is not None, "Required property 'subnet_mapping' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["NetworkfirewallFirewallSubnetMapping"]], result)

    @builtins.property
    def vpc_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#vpc_id NetworkfirewallFirewall#vpc_id}.'''
        result = self._values.get("vpc_id")
        assert result is not None, "Required property 'vpc_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def delete_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#delete_protection NetworkfirewallFirewall#delete_protection}.'''
        result = self._values.get("delete_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#description NetworkfirewallFirewall#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def encryption_configuration(
        self,
    ) -> typing.Optional["NetworkfirewallFirewallEncryptionConfiguration"]:
        '''encryption_configuration block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#encryption_configuration NetworkfirewallFirewall#encryption_configuration}
        '''
        result = self._values.get("encryption_configuration")
        return typing.cast(typing.Optional["NetworkfirewallFirewallEncryptionConfiguration"], result)

    @builtins.property
    def firewall_policy_change_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#firewall_policy_change_protection NetworkfirewallFirewall#firewall_policy_change_protection}.'''
        result = self._values.get("firewall_policy_change_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#id NetworkfirewallFirewall#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_change_protection(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#subnet_change_protection NetworkfirewallFirewall#subnet_change_protection}.'''
        result = self._values.get("subnet_change_protection")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#tags NetworkfirewallFirewall#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def tags_all(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#tags_all NetworkfirewallFirewall#tags_all}.'''
        result = self._values.get("tags_all")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkfirewallFirewallConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.networkfirewallFirewall.NetworkfirewallFirewallEncryptionConfiguration",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "key_id": "keyId"},
)
class NetworkfirewallFirewallEncryptionConfiguration:
    def __init__(
        self,
        *,
        type: builtins.str,
        key_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#type NetworkfirewallFirewall#type}.
        :param key_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#key_id NetworkfirewallFirewall#key_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b5f799416c9418e0ec3df93e2d7ac56e61eb1a22066c33fcd81ec5437a8c4ae)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument key_id", value=key_id, expected_type=type_hints["key_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if key_id is not None:
            self._values["key_id"] = key_id

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#type NetworkfirewallFirewall#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def key_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#key_id NetworkfirewallFirewall#key_id}.'''
        result = self._values.get("key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkfirewallFirewallEncryptionConfiguration(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkfirewallFirewallEncryptionConfigurationOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.networkfirewallFirewall.NetworkfirewallFirewallEncryptionConfigurationOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd3aaeef9e2b3b31bb25bf2089711f8bd3f3ed5266ec17c5cb4e580a222f33c5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetKeyId")
    def reset_key_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeyId", []))

    @builtins.property
    @jsii.member(jsii_name="keyIdInput")
    def key_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="keyId")
    def key_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keyId"))

    @key_id.setter
    def key_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__510b331788cc87b19d467ef62c52536bdfcc659e2772555dc579a6f185ea3bc6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keyId", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab19953d3854a8dca2ccec95011441b669d8c7a2f2c56f83ca341f3554d8f6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkfirewallFirewallEncryptionConfiguration]:
        return typing.cast(typing.Optional[NetworkfirewallFirewallEncryptionConfiguration], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkfirewallFirewallEncryptionConfiguration],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__93d399dac855dea58aaaeee7f81e585b7aa0af4204a7b12e5d2c61cd578a74b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.networkfirewallFirewall.NetworkfirewallFirewallFirewallStatus",
    jsii_struct_bases=[],
    name_mapping={},
)
class NetworkfirewallFirewallFirewallStatus:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkfirewallFirewallFirewallStatus(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkfirewallFirewallFirewallStatusList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.networkfirewallFirewall.NetworkfirewallFirewallFirewallStatusList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ae67244bcfa305f7c33c563a8a51355a95b651933c6d7db9772ef18096ba088)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkfirewallFirewallFirewallStatusOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b53fd94ecb0183523e7adf1c020b6020e7950b6b529d5296253a2cff1d1f7940)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkfirewallFirewallFirewallStatusOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9247cf5a6fc029df554930a0e85c6926add203a20941c09a2e6a4cf68c264bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40ada02c56148634184f5b8201303093ca539fb6623e922e34fb19e0040532bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbbf9f72142e2f431c14550263718d8fd24065afc09eb0262d03c242cdbe3397)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class NetworkfirewallFirewallFirewallStatusOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.networkfirewallFirewall.NetworkfirewallFirewallFirewallStatusOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f762487b949b0a77adcf9de8b7d3a2ca2d735f7f11fd6b7300d856fdad1bd35)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="syncStates")
    def sync_states(self) -> "NetworkfirewallFirewallFirewallStatusSyncStatesList":
        return typing.cast("NetworkfirewallFirewallFirewallStatusSyncStatesList", jsii.get(self, "syncStates"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[NetworkfirewallFirewallFirewallStatus]:
        return typing.cast(typing.Optional[NetworkfirewallFirewallFirewallStatus], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkfirewallFirewallFirewallStatus],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5ae188cd8cd33ac433843d72fa71b33d03b25968038e93478731e338902f7c0e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.networkfirewallFirewall.NetworkfirewallFirewallFirewallStatusSyncStates",
    jsii_struct_bases=[],
    name_mapping={},
)
class NetworkfirewallFirewallFirewallStatusSyncStates:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkfirewallFirewallFirewallStatusSyncStates(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.networkfirewallFirewall.NetworkfirewallFirewallFirewallStatusSyncStatesAttachment",
    jsii_struct_bases=[],
    name_mapping={},
)
class NetworkfirewallFirewallFirewallStatusSyncStatesAttachment:
    def __init__(self) -> None:
        self._values: typing.Dict[builtins.str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkfirewallFirewallFirewallStatusSyncStatesAttachment(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkfirewallFirewallFirewallStatusSyncStatesAttachmentList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.networkfirewallFirewall.NetworkfirewallFirewallFirewallStatusSyncStatesAttachmentList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1bd082c322efae0427d3b3614894f2a86dce5b93f8ba703bc669bafae9cb34ec)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkfirewallFirewallFirewallStatusSyncStatesAttachmentOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56bf64f2cf11abda3def928f4dbd596c63655308fb2cb09d5f95a5db2f8eb7d2)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkfirewallFirewallFirewallStatusSyncStatesAttachmentOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fcdc311a09850bbc4ff02778e31af423bcc27d6677bb55bf256a7638a215b74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24a2e8324a564eb7eb6078f46cf438fe9c116b39c0c46d8beb54540d70fae9df)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b0584caafa8d5844f4d674383709a814eb40baac74002951279ebdef9fc253e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class NetworkfirewallFirewallFirewallStatusSyncStatesAttachmentOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.networkfirewallFirewall.NetworkfirewallFirewallFirewallStatusSyncStatesAttachmentOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a97df21a10e2a321340493161049997fb3da6eab82c35f71118b1dac23397cc)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="endpointId")
    def endpoint_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endpointId"))

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkfirewallFirewallFirewallStatusSyncStatesAttachment]:
        return typing.cast(typing.Optional[NetworkfirewallFirewallFirewallStatusSyncStatesAttachment], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkfirewallFirewallFirewallStatusSyncStatesAttachment],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30bbd8ee118fc4a86c1408d9657dbe2c807125acf1fe6b27ff44ca99b418cb62)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NetworkfirewallFirewallFirewallStatusSyncStatesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.networkfirewallFirewall.NetworkfirewallFirewallFirewallStatusSyncStatesList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__02d18e586b0c56b4716515c295564556619d21bb1110452a607824dda21149ea)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkfirewallFirewallFirewallStatusSyncStatesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8735609b12685306450c34d19ab33ef4919f7ad8a21e79791bcdd78a59026c7)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkfirewallFirewallFirewallStatusSyncStatesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad6c8069144d45e1bd93b29aa771c08a5baec84a4ae89169ac32c00b0efb668d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0cb6ce194a66d7de1e47673e2826670e6ae7d6d40d62b058586763fc5d2ae3c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6fb3b40780f4cba6afd6528475c262d48c800e24fae2f714da6594f6a5f79817)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)


class NetworkfirewallFirewallFirewallStatusSyncStatesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.networkfirewallFirewall.NetworkfirewallFirewallFirewallStatusSyncStatesOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3594d90fd2728013c25e15835b47d470202c4c3c562627540554606f3e262e7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="attachment")
    def attachment(
        self,
    ) -> NetworkfirewallFirewallFirewallStatusSyncStatesAttachmentList:
        return typing.cast(NetworkfirewallFirewallFirewallStatusSyncStatesAttachmentList, jsii.get(self, "attachment"))

    @builtins.property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "availabilityZone"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[NetworkfirewallFirewallFirewallStatusSyncStates]:
        return typing.cast(typing.Optional[NetworkfirewallFirewallFirewallStatusSyncStates], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[NetworkfirewallFirewallFirewallStatusSyncStates],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03248c62efcdc40475d4cde552fd7f48241d02a041d82095b28cacb81e3ef0c3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.networkfirewallFirewall.NetworkfirewallFirewallSubnetMapping",
    jsii_struct_bases=[],
    name_mapping={"subnet_id": "subnetId"},
)
class NetworkfirewallFirewallSubnetMapping:
    def __init__(self, *, subnet_id: builtins.str) -> None:
        '''
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#subnet_id NetworkfirewallFirewall#subnet_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bae1a2d5a18725a57a33c75e10f52b1da44a3a7810d7c0c13219c5dfd8f0dbee)
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_id": subnet_id,
        }

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/networkfirewall_firewall#subnet_id NetworkfirewallFirewall#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NetworkfirewallFirewallSubnetMapping(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class NetworkfirewallFirewallSubnetMappingList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.networkfirewallFirewall.NetworkfirewallFirewallSubnetMappingList",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        wraps_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param wraps_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6023f660f4533a04895d6d8867881502e5010e0f60d0d663e50fe61cd83cd662)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "NetworkfirewallFirewallSubnetMappingOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26de0b9c853ccfe9010191d64f623c20b93cb89737cf6ba52b6120bf11da3d73)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("NetworkfirewallFirewallSubnetMappingOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd8977d8c4d853025263050471170fd47d3e5992c28c893b56748b16df1f8bd9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformAttribute", value)

    @builtins.property
    @jsii.member(jsii_name="terraformResource")
    def _terraform_resource(self) -> _cdktf_9a9027ec.IInterpolatingParent:
        '''The parent resource.'''
        return typing.cast(_cdktf_9a9027ec.IInterpolatingParent, jsii.get(self, "terraformResource"))

    @_terraform_resource.setter
    def _terraform_resource(self, value: _cdktf_9a9027ec.IInterpolatingParent) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5826701f251a282eca8bec337b913ecf8e0e2cda21ad0b78f7b477bcb0c7e95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "terraformResource", value)

    @builtins.property
    @jsii.member(jsii_name="wrapsSet")
    def _wraps_set(self) -> builtins.bool:
        '''whether the list is wrapping a set (will add tolist() to be able to access an item via an index).'''
        return typing.cast(builtins.bool, jsii.get(self, "wrapsSet"))

    @_wraps_set.setter
    def _wraps_set(self, value: builtins.bool) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__297aea38a5f803355475e4839a492874054946b0e819bee3f4df527b293ef972)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkfirewallFirewallSubnetMapping]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkfirewallFirewallSubnetMapping]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkfirewallFirewallSubnetMapping]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a802683cc56ee5e7cf9dc8bd3b7bfdef31a430a1f2982dd8467150a6433eb7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class NetworkfirewallFirewallSubnetMappingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.networkfirewallFirewall.NetworkfirewallFirewallSubnetMappingOutputReference",
):
    def __init__(
        self,
        terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
        terraform_attribute: builtins.str,
        complex_object_index: jsii.Number,
        complex_object_is_from_set: builtins.bool,
    ) -> None:
        '''
        :param terraform_resource: The parent resource.
        :param terraform_attribute: The attribute on the parent resource this class is referencing.
        :param complex_object_index: the index of this item in the list.
        :param complex_object_is_from_set: whether the list is wrapping a set (will add tolist() to be able to access an item via an index).
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__166500aed4ddd110cb8e22e116e0b91f2fcf8795e43be927180d5d4d58095b9e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aebbe0e4befd055a9efae05efd52415bb8878b93299f868f33daf12d63e376d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[NetworkfirewallFirewallSubnetMapping, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[NetworkfirewallFirewallSubnetMapping, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[NetworkfirewallFirewallSubnetMapping, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9c12e28a839892058235aa42f5ee178b5be4b9b6416090a8bb7c516246eaf9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "NetworkfirewallFirewall",
    "NetworkfirewallFirewallConfig",
    "NetworkfirewallFirewallEncryptionConfiguration",
    "NetworkfirewallFirewallEncryptionConfigurationOutputReference",
    "NetworkfirewallFirewallFirewallStatus",
    "NetworkfirewallFirewallFirewallStatusList",
    "NetworkfirewallFirewallFirewallStatusOutputReference",
    "NetworkfirewallFirewallFirewallStatusSyncStates",
    "NetworkfirewallFirewallFirewallStatusSyncStatesAttachment",
    "NetworkfirewallFirewallFirewallStatusSyncStatesAttachmentList",
    "NetworkfirewallFirewallFirewallStatusSyncStatesAttachmentOutputReference",
    "NetworkfirewallFirewallFirewallStatusSyncStatesList",
    "NetworkfirewallFirewallFirewallStatusSyncStatesOutputReference",
    "NetworkfirewallFirewallSubnetMapping",
    "NetworkfirewallFirewallSubnetMappingList",
    "NetworkfirewallFirewallSubnetMappingOutputReference",
]

publication.publish()

def _typecheckingstub__4df79298a403bbe89bcce45294cd2cef752ab819b09aa7c705835855392f469d(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    firewall_policy_arn: builtins.str,
    name: builtins.str,
    subnet_mapping: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkfirewallFirewallSubnetMapping, typing.Dict[builtins.str, typing.Any]]]],
    vpc_id: builtins.str,
    delete_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_configuration: typing.Optional[typing.Union[NetworkfirewallFirewallEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    firewall_policy_change_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    subnet_change_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c40d12ed03db2812ea3d779f0627430d5be989ee789eb9e8c34a40705ec9ad43(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkfirewallFirewallSubnetMapping, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__832eb09d6d943d1effbdbd58523e082896d2e88dc3c36df1784f88018a83d2b2(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10dd7a04fc4c42cd6c5c8bb65a91e4f940fc451a5258ff90ad65c99091ec65b1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca7f6bbf3dd4527bb9cb8c4a33a7880796afae7bc7528ca52d31d852ffeeae6c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfac85d3329ef009dadee5980129e87ad2a51c60cfa4f27d274db34365584b20(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ada83a2d080c91ac27234ecdd8a6a9e15cb8440e3c1070ff4c5cdbb143059dd0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2df3c152242a5eb4af53b20459011bf1e8f8396e0add6f79a3545396586abe8c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20b3bb0afd8dc74894d70541f43a8b19a8a7c784de374b0dd1f6f59e8f8e816a(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecee0fa97eebe472cf1f9d1989ab510162d1a1d506d202b71123c97cfb04cec1(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce618a695a6e552e629b9822dad387f09f1fb63ea5cb629605aebddce677a550(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5adddf58740714142356f0e3182791bb89b6cd15cb5efd78ac09ea12efdffef1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c31ae442b68278894c5ef8b24fecf770de2697e692f9c171f9539a6f21497502(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    firewall_policy_arn: builtins.str,
    name: builtins.str,
    subnet_mapping: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[NetworkfirewallFirewallSubnetMapping, typing.Dict[builtins.str, typing.Any]]]],
    vpc_id: builtins.str,
    delete_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    description: typing.Optional[builtins.str] = None,
    encryption_configuration: typing.Optional[typing.Union[NetworkfirewallFirewallEncryptionConfiguration, typing.Dict[builtins.str, typing.Any]]] = None,
    firewall_policy_change_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    subnet_change_protection: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    tags_all: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b5f799416c9418e0ec3df93e2d7ac56e61eb1a22066c33fcd81ec5437a8c4ae(
    *,
    type: builtins.str,
    key_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd3aaeef9e2b3b31bb25bf2089711f8bd3f3ed5266ec17c5cb4e580a222f33c5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__510b331788cc87b19d467ef62c52536bdfcc659e2772555dc579a6f185ea3bc6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab19953d3854a8dca2ccec95011441b669d8c7a2f2c56f83ca341f3554d8f6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__93d399dac855dea58aaaeee7f81e585b7aa0af4204a7b12e5d2c61cd578a74b8(
    value: typing.Optional[NetworkfirewallFirewallEncryptionConfiguration],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ae67244bcfa305f7c33c563a8a51355a95b651933c6d7db9772ef18096ba088(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b53fd94ecb0183523e7adf1c020b6020e7950b6b529d5296253a2cff1d1f7940(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9247cf5a6fc029df554930a0e85c6926add203a20941c09a2e6a4cf68c264bf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40ada02c56148634184f5b8201303093ca539fb6623e922e34fb19e0040532bf(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbbf9f72142e2f431c14550263718d8fd24065afc09eb0262d03c242cdbe3397(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f762487b949b0a77adcf9de8b7d3a2ca2d735f7f11fd6b7300d856fdad1bd35(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5ae188cd8cd33ac433843d72fa71b33d03b25968038e93478731e338902f7c0e(
    value: typing.Optional[NetworkfirewallFirewallFirewallStatus],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1bd082c322efae0427d3b3614894f2a86dce5b93f8ba703bc669bafae9cb34ec(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56bf64f2cf11abda3def928f4dbd596c63655308fb2cb09d5f95a5db2f8eb7d2(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fcdc311a09850bbc4ff02778e31af423bcc27d6677bb55bf256a7638a215b74(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24a2e8324a564eb7eb6078f46cf438fe9c116b39c0c46d8beb54540d70fae9df(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b0584caafa8d5844f4d674383709a814eb40baac74002951279ebdef9fc253e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a97df21a10e2a321340493161049997fb3da6eab82c35f71118b1dac23397cc(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30bbd8ee118fc4a86c1408d9657dbe2c807125acf1fe6b27ff44ca99b418cb62(
    value: typing.Optional[NetworkfirewallFirewallFirewallStatusSyncStatesAttachment],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__02d18e586b0c56b4716515c295564556619d21bb1110452a607824dda21149ea(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8735609b12685306450c34d19ab33ef4919f7ad8a21e79791bcdd78a59026c7(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad6c8069144d45e1bd93b29aa771c08a5baec84a4ae89169ac32c00b0efb668d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0cb6ce194a66d7de1e47673e2826670e6ae7d6d40d62b058586763fc5d2ae3c(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6fb3b40780f4cba6afd6528475c262d48c800e24fae2f714da6594f6a5f79817(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3594d90fd2728013c25e15835b47d470202c4c3c562627540554606f3e262e7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03248c62efcdc40475d4cde552fd7f48241d02a041d82095b28cacb81e3ef0c3(
    value: typing.Optional[NetworkfirewallFirewallFirewallStatusSyncStates],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae1a2d5a18725a57a33c75e10f52b1da44a3a7810d7c0c13219c5dfd8f0dbee(
    *,
    subnet_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6023f660f4533a04895d6d8867881502e5010e0f60d0d663e50fe61cd83cd662(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26de0b9c853ccfe9010191d64f623c20b93cb89737cf6ba52b6120bf11da3d73(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd8977d8c4d853025263050471170fd47d3e5992c28c893b56748b16df1f8bd9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5826701f251a282eca8bec337b913ecf8e0e2cda21ad0b78f7b477bcb0c7e95(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__297aea38a5f803355475e4839a492874054946b0e819bee3f4df527b293ef972(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a802683cc56ee5e7cf9dc8bd3b7bfdef31a430a1f2982dd8467150a6433eb7c(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[NetworkfirewallFirewallSubnetMapping]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__166500aed4ddd110cb8e22e116e0b91f2fcf8795e43be927180d5d4d58095b9e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aebbe0e4befd055a9efae05efd52415bb8878b93299f868f33daf12d63e376d3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9c12e28a839892058235aa42f5ee178b5be4b9b6416090a8bb7c516246eaf9(
    value: typing.Optional[typing.Union[NetworkfirewallFirewallSubnetMapping, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
