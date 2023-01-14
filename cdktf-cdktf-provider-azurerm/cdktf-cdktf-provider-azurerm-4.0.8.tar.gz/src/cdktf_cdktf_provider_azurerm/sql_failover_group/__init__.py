'''
# `azurerm_sql_failover_group`

Refer to the Terraform Registory for docs: [`azurerm_sql_failover_group`](https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group).
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


class SqlFailoverGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sqlFailoverGroup.SqlFailoverGroup",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group azurerm_sql_failover_group}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        partner_servers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SqlFailoverGroupPartnerServers", typing.Dict[builtins.str, typing.Any]]]],
        read_write_endpoint_failover_policy: typing.Union["SqlFailoverGroupReadWriteEndpointFailoverPolicy", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        server_name: builtins.str,
        databases: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        readonly_endpoint_failover_policy: typing.Optional[typing.Union["SqlFailoverGroupReadonlyEndpointFailoverPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SqlFailoverGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group azurerm_sql_failover_group} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#name SqlFailoverGroup#name}.
        :param partner_servers: partner_servers block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#partner_servers SqlFailoverGroup#partner_servers}
        :param read_write_endpoint_failover_policy: read_write_endpoint_failover_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#read_write_endpoint_failover_policy SqlFailoverGroup#read_write_endpoint_failover_policy}
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#resource_group_name SqlFailoverGroup#resource_group_name}.
        :param server_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#server_name SqlFailoverGroup#server_name}.
        :param databases: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#databases SqlFailoverGroup#databases}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#id SqlFailoverGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param readonly_endpoint_failover_policy: readonly_endpoint_failover_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#readonly_endpoint_failover_policy SqlFailoverGroup#readonly_endpoint_failover_policy}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#tags SqlFailoverGroup#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#timeouts SqlFailoverGroup#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f1686c82170ad31900175ccc899eec27ddefd7a547fe4a9dc465e2c0c807eb5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SqlFailoverGroupConfig(
            name=name,
            partner_servers=partner_servers,
            read_write_endpoint_failover_policy=read_write_endpoint_failover_policy,
            resource_group_name=resource_group_name,
            server_name=server_name,
            databases=databases,
            id=id,
            readonly_endpoint_failover_policy=readonly_endpoint_failover_policy,
            tags=tags,
            timeouts=timeouts,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putPartnerServers")
    def put_partner_servers(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SqlFailoverGroupPartnerServers", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa4bf8c2baaa71771d44cf1ffdb05b938af63ae2508124b4dcee11b4d23f2c9c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putPartnerServers", [value]))

    @jsii.member(jsii_name="putReadonlyEndpointFailoverPolicy")
    def put_readonly_endpoint_failover_policy(self, *, mode: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#mode SqlFailoverGroup#mode}.
        '''
        value = SqlFailoverGroupReadonlyEndpointFailoverPolicy(mode=mode)

        return typing.cast(None, jsii.invoke(self, "putReadonlyEndpointFailoverPolicy", [value]))

    @jsii.member(jsii_name="putReadWriteEndpointFailoverPolicy")
    def put_read_write_endpoint_failover_policy(
        self,
        *,
        mode: builtins.str,
        grace_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#mode SqlFailoverGroup#mode}.
        :param grace_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#grace_minutes SqlFailoverGroup#grace_minutes}.
        '''
        value = SqlFailoverGroupReadWriteEndpointFailoverPolicy(
            mode=mode, grace_minutes=grace_minutes
        )

        return typing.cast(None, jsii.invoke(self, "putReadWriteEndpointFailoverPolicy", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#create SqlFailoverGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#delete SqlFailoverGroup#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#read SqlFailoverGroup#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#update SqlFailoverGroup#update}.
        '''
        value = SqlFailoverGroupTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDatabases")
    def reset_databases(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDatabases", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetReadonlyEndpointFailoverPolicy")
    def reset_readonly_endpoint_failover_policy(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReadonlyEndpointFailoverPolicy", []))

    @jsii.member(jsii_name="resetTags")
    def reset_tags(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTags", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="partnerServers")
    def partner_servers(self) -> "SqlFailoverGroupPartnerServersList":
        return typing.cast("SqlFailoverGroupPartnerServersList", jsii.get(self, "partnerServers"))

    @builtins.property
    @jsii.member(jsii_name="readonlyEndpointFailoverPolicy")
    def readonly_endpoint_failover_policy(
        self,
    ) -> "SqlFailoverGroupReadonlyEndpointFailoverPolicyOutputReference":
        return typing.cast("SqlFailoverGroupReadonlyEndpointFailoverPolicyOutputReference", jsii.get(self, "readonlyEndpointFailoverPolicy"))

    @builtins.property
    @jsii.member(jsii_name="readWriteEndpointFailoverPolicy")
    def read_write_endpoint_failover_policy(
        self,
    ) -> "SqlFailoverGroupReadWriteEndpointFailoverPolicyOutputReference":
        return typing.cast("SqlFailoverGroupReadWriteEndpointFailoverPolicyOutputReference", jsii.get(self, "readWriteEndpointFailoverPolicy"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "SqlFailoverGroupTimeoutsOutputReference":
        return typing.cast("SqlFailoverGroupTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="databasesInput")
    def databases_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "databasesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="partnerServersInput")
    def partner_servers_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlFailoverGroupPartnerServers"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlFailoverGroupPartnerServers"]]], jsii.get(self, "partnerServersInput"))

    @builtins.property
    @jsii.member(jsii_name="readonlyEndpointFailoverPolicyInput")
    def readonly_endpoint_failover_policy_input(
        self,
    ) -> typing.Optional["SqlFailoverGroupReadonlyEndpointFailoverPolicy"]:
        return typing.cast(typing.Optional["SqlFailoverGroupReadonlyEndpointFailoverPolicy"], jsii.get(self, "readonlyEndpointFailoverPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="readWriteEndpointFailoverPolicyInput")
    def read_write_endpoint_failover_policy_input(
        self,
    ) -> typing.Optional["SqlFailoverGroupReadWriteEndpointFailoverPolicy"]:
        return typing.cast(typing.Optional["SqlFailoverGroupReadWriteEndpointFailoverPolicy"], jsii.get(self, "readWriteEndpointFailoverPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="serverNameInput")
    def server_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverNameInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["SqlFailoverGroupTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["SqlFailoverGroupTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="databases")
    def databases(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "databases"))

    @databases.setter
    def databases(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b2f70ec4b4b98e4feb41c837b53bec6d1586471389d35a9ffba00dc98e39e1f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "databases", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__810c15c081bc44f0e36c451fb68c162e30fc3f50195f678f2f61653180386868)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68aa46831b372c662bab7fa06f0e28be5b191667da35ee580649e52cbf597534)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__422ebfdf526227324d8774a1fedf7b6847699432950c272eba7f0f28cd27af7f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="serverName")
    def server_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "serverName"))

    @server_name.setter
    def server_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__17ee28535604e4d5fccb78cd98ee5658e38cb0d4aafea44c8b1a7451ad706285)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverName", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__63d09a36b0693530dafd9cca9e9a4194e405018700d095920a14b9dcfdf23edc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sqlFailoverGroup.SqlFailoverGroupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "partner_servers": "partnerServers",
        "read_write_endpoint_failover_policy": "readWriteEndpointFailoverPolicy",
        "resource_group_name": "resourceGroupName",
        "server_name": "serverName",
        "databases": "databases",
        "id": "id",
        "readonly_endpoint_failover_policy": "readonlyEndpointFailoverPolicy",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class SqlFailoverGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        partner_servers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SqlFailoverGroupPartnerServers", typing.Dict[builtins.str, typing.Any]]]],
        read_write_endpoint_failover_policy: typing.Union["SqlFailoverGroupReadWriteEndpointFailoverPolicy", typing.Dict[builtins.str, typing.Any]],
        resource_group_name: builtins.str,
        server_name: builtins.str,
        databases: typing.Optional[typing.Sequence[builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        readonly_endpoint_failover_policy: typing.Optional[typing.Union["SqlFailoverGroupReadonlyEndpointFailoverPolicy", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["SqlFailoverGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#name SqlFailoverGroup#name}.
        :param partner_servers: partner_servers block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#partner_servers SqlFailoverGroup#partner_servers}
        :param read_write_endpoint_failover_policy: read_write_endpoint_failover_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#read_write_endpoint_failover_policy SqlFailoverGroup#read_write_endpoint_failover_policy}
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#resource_group_name SqlFailoverGroup#resource_group_name}.
        :param server_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#server_name SqlFailoverGroup#server_name}.
        :param databases: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#databases SqlFailoverGroup#databases}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#id SqlFailoverGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param readonly_endpoint_failover_policy: readonly_endpoint_failover_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#readonly_endpoint_failover_policy SqlFailoverGroup#readonly_endpoint_failover_policy}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#tags SqlFailoverGroup#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#timeouts SqlFailoverGroup#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(read_write_endpoint_failover_policy, dict):
            read_write_endpoint_failover_policy = SqlFailoverGroupReadWriteEndpointFailoverPolicy(**read_write_endpoint_failover_policy)
        if isinstance(readonly_endpoint_failover_policy, dict):
            readonly_endpoint_failover_policy = SqlFailoverGroupReadonlyEndpointFailoverPolicy(**readonly_endpoint_failover_policy)
        if isinstance(timeouts, dict):
            timeouts = SqlFailoverGroupTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aca604fa236fec579c0ef77e8b1b332a8e41016e5947d703520c5fa5dab754b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument partner_servers", value=partner_servers, expected_type=type_hints["partner_servers"])
            check_type(argname="argument read_write_endpoint_failover_policy", value=read_write_endpoint_failover_policy, expected_type=type_hints["read_write_endpoint_failover_policy"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument server_name", value=server_name, expected_type=type_hints["server_name"])
            check_type(argname="argument databases", value=databases, expected_type=type_hints["databases"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument readonly_endpoint_failover_policy", value=readonly_endpoint_failover_policy, expected_type=type_hints["readonly_endpoint_failover_policy"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "partner_servers": partner_servers,
            "read_write_endpoint_failover_policy": read_write_endpoint_failover_policy,
            "resource_group_name": resource_group_name,
            "server_name": server_name,
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
        if databases is not None:
            self._values["databases"] = databases
        if id is not None:
            self._values["id"] = id
        if readonly_endpoint_failover_policy is not None:
            self._values["readonly_endpoint_failover_policy"] = readonly_endpoint_failover_policy
        if tags is not None:
            self._values["tags"] = tags
        if timeouts is not None:
            self._values["timeouts"] = timeouts

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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#name SqlFailoverGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def partner_servers(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlFailoverGroupPartnerServers"]]:
        '''partner_servers block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#partner_servers SqlFailoverGroup#partner_servers}
        '''
        result = self._values.get("partner_servers")
        assert result is not None, "Required property 'partner_servers' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SqlFailoverGroupPartnerServers"]], result)

    @builtins.property
    def read_write_endpoint_failover_policy(
        self,
    ) -> "SqlFailoverGroupReadWriteEndpointFailoverPolicy":
        '''read_write_endpoint_failover_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#read_write_endpoint_failover_policy SqlFailoverGroup#read_write_endpoint_failover_policy}
        '''
        result = self._values.get("read_write_endpoint_failover_policy")
        assert result is not None, "Required property 'read_write_endpoint_failover_policy' is missing"
        return typing.cast("SqlFailoverGroupReadWriteEndpointFailoverPolicy", result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#resource_group_name SqlFailoverGroup#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def server_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#server_name SqlFailoverGroup#server_name}.'''
        result = self._values.get("server_name")
        assert result is not None, "Required property 'server_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def databases(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#databases SqlFailoverGroup#databases}.'''
        result = self._values.get("databases")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#id SqlFailoverGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def readonly_endpoint_failover_policy(
        self,
    ) -> typing.Optional["SqlFailoverGroupReadonlyEndpointFailoverPolicy"]:
        '''readonly_endpoint_failover_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#readonly_endpoint_failover_policy SqlFailoverGroup#readonly_endpoint_failover_policy}
        '''
        result = self._values.get("readonly_endpoint_failover_policy")
        return typing.cast(typing.Optional["SqlFailoverGroupReadonlyEndpointFailoverPolicy"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#tags SqlFailoverGroup#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["SqlFailoverGroupTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#timeouts SqlFailoverGroup#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["SqlFailoverGroupTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlFailoverGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sqlFailoverGroup.SqlFailoverGroupPartnerServers",
    jsii_struct_bases=[],
    name_mapping={"id": "id"},
)
class SqlFailoverGroupPartnerServers:
    def __init__(self, *, id: builtins.str) -> None:
        '''
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#id SqlFailoverGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3ecb06b3cc31a488e628c8d11c9997807dc08c946865b431c0ccd4e8d7fb0464)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
        }

    @builtins.property
    def id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#id SqlFailoverGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlFailoverGroupPartnerServers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlFailoverGroupPartnerServersList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sqlFailoverGroup.SqlFailoverGroupPartnerServersList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d7689c24c03b99f2bd6ed23652d595ae23bf13d1092f9b84c9a494ea1d173eef)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "SqlFailoverGroupPartnerServersOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__342e748d77a69f61fb3fa0136fc59d7d07f1a60bbd729ce88ed91bc514d1cb3d)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SqlFailoverGroupPartnerServersOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2f643ffd2375d69df49d18f40cf648b9fa3e4b748990d69a2f06de2256e7d6d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__b896af23bf21d5184f21365e8dce55f24342f08f32e79dfa5dee3178eb90c469)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d2b41a69c5ab23132ec99e884fd3754f79bcac45352b21f2b6e6d01195c4b7e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlFailoverGroupPartnerServers]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlFailoverGroupPartnerServers]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlFailoverGroupPartnerServers]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d018b621216817e718dcd675b9e7dc2ce48541ab8728043b8251529845d3261e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SqlFailoverGroupPartnerServersOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sqlFailoverGroup.SqlFailoverGroupPartnerServersOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__698947c40f278006d5cbb745d1c9ee4833fca68135e41b16a864e6a24414d6b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @builtins.property
    @jsii.member(jsii_name="location")
    def location(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "location"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54b8b00336fa552c26a771eae9538e09b2d3d215365fd590ed4af33081dd5ad8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SqlFailoverGroupPartnerServers, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SqlFailoverGroupPartnerServers, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SqlFailoverGroupPartnerServers, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc09f5697d973dbdf6a5d0db1b48c29379ff072703cc2057196c0502add8a94b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sqlFailoverGroup.SqlFailoverGroupReadWriteEndpointFailoverPolicy",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode", "grace_minutes": "graceMinutes"},
)
class SqlFailoverGroupReadWriteEndpointFailoverPolicy:
    def __init__(
        self,
        *,
        mode: builtins.str,
        grace_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#mode SqlFailoverGroup#mode}.
        :param grace_minutes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#grace_minutes SqlFailoverGroup#grace_minutes}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11f006a6d87d8b58b7ea278df0d8af89cc7006655ca1b32c43b16b5eaebc77ff)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument grace_minutes", value=grace_minutes, expected_type=type_hints["grace_minutes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }
        if grace_minutes is not None:
            self._values["grace_minutes"] = grace_minutes

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#mode SqlFailoverGroup#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def grace_minutes(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#grace_minutes SqlFailoverGroup#grace_minutes}.'''
        result = self._values.get("grace_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlFailoverGroupReadWriteEndpointFailoverPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlFailoverGroupReadWriteEndpointFailoverPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sqlFailoverGroup.SqlFailoverGroupReadWriteEndpointFailoverPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__72adff817169d36ce9ac473cd92ba42d384202c4eab52c31b802e10d962a7cae)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetGraceMinutes")
    def reset_grace_minutes(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetGraceMinutes", []))

    @builtins.property
    @jsii.member(jsii_name="graceMinutesInput")
    def grace_minutes_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "graceMinutesInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="graceMinutes")
    def grace_minutes(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "graceMinutes"))

    @grace_minutes.setter
    def grace_minutes(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ce4433d0bda8da0cc064003c75285d66079e690e6c2924c4bd779be4ed40c46)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "graceMinutes", value)

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8fbc641a343081d116d84d3af50ff687b022269bacfdb32f0a54850f4c9e98eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlFailoverGroupReadWriteEndpointFailoverPolicy]:
        return typing.cast(typing.Optional[SqlFailoverGroupReadWriteEndpointFailoverPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlFailoverGroupReadWriteEndpointFailoverPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ca08f0d7ab7679dd60c60d1defcf7aaef5d25b4090109079ac1976ed10cd0c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sqlFailoverGroup.SqlFailoverGroupReadonlyEndpointFailoverPolicy",
    jsii_struct_bases=[],
    name_mapping={"mode": "mode"},
)
class SqlFailoverGroupReadonlyEndpointFailoverPolicy:
    def __init__(self, *, mode: builtins.str) -> None:
        '''
        :param mode: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#mode SqlFailoverGroup#mode}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16a7802097d6f3364bc881998396e0eaf33220616348cb80705ec718f6cf1c27)
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "mode": mode,
        }

    @builtins.property
    def mode(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#mode SqlFailoverGroup#mode}.'''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlFailoverGroupReadonlyEndpointFailoverPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlFailoverGroupReadonlyEndpointFailoverPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sqlFailoverGroup.SqlFailoverGroupReadonlyEndpointFailoverPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2f6a00ceb97330345921ceb09f402871dc6d477837d7ab77f1a8284e817894b4)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__28446294c66c1a80f93252615a99b75ff252b6d65a804a8cafc372de5ecb3dbd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[SqlFailoverGroupReadonlyEndpointFailoverPolicy]:
        return typing.cast(typing.Optional[SqlFailoverGroupReadonlyEndpointFailoverPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[SqlFailoverGroupReadonlyEndpointFailoverPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b805faab05eb8722e3d07a5a0f23d33c5a83558c8656cf9c3e2400a308c9ddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.sqlFailoverGroup.SqlFailoverGroupTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class SqlFailoverGroupTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#create SqlFailoverGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#delete SqlFailoverGroup#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#read SqlFailoverGroup#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#update SqlFailoverGroup#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__583dbf1d605e6fe15f585968061ca9618c59f43766563f2d15898f10b2bcbcd1)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument read", value=read, expected_type=type_hints["read"])
            check_type(argname="argument update", value=update, expected_type=type_hints["update"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if read is not None:
            self._values["read"] = read
        if update is not None:
            self._values["update"] = update

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#create SqlFailoverGroup#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#delete SqlFailoverGroup#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#read SqlFailoverGroup#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/sql_failover_group#update SqlFailoverGroup#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SqlFailoverGroupTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SqlFailoverGroupTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.sqlFailoverGroup.SqlFailoverGroupTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f2df9df993049ec69432f2e7090bbd089679005b24c72d3eaaa27fc5cfac8121)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @jsii.member(jsii_name="resetRead")
    def reset_read(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRead", []))

    @jsii.member(jsii_name="resetUpdate")
    def reset_update(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetUpdate", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="readInput")
    def read_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "readInput"))

    @builtins.property
    @jsii.member(jsii_name="updateInput")
    def update_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "updateInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__792355519abec66579100d34b012ec320e2fd47156562e5946768fb77f3ad620)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3866926bfd7d49fde121b3f9de821eaf324b48168043d40179e314ff8be52d9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d87bf18e57ec811affd84361ff04082ea0fa66a68683f4155bd6d80c5266c871)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b51ddb98b8f28a7312848f1aed3b9e5b3cfa3ad08c69ed1ed40c3d215b55bf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SqlFailoverGroupTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SqlFailoverGroupTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SqlFailoverGroupTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18509afda5cbc136a41d2b8daf8f7b14e2460751cb23a3f80a15ea4e9aedd332)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SqlFailoverGroup",
    "SqlFailoverGroupConfig",
    "SqlFailoverGroupPartnerServers",
    "SqlFailoverGroupPartnerServersList",
    "SqlFailoverGroupPartnerServersOutputReference",
    "SqlFailoverGroupReadWriteEndpointFailoverPolicy",
    "SqlFailoverGroupReadWriteEndpointFailoverPolicyOutputReference",
    "SqlFailoverGroupReadonlyEndpointFailoverPolicy",
    "SqlFailoverGroupReadonlyEndpointFailoverPolicyOutputReference",
    "SqlFailoverGroupTimeouts",
    "SqlFailoverGroupTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__0f1686c82170ad31900175ccc899eec27ddefd7a547fe4a9dc465e2c0c807eb5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    partner_servers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlFailoverGroupPartnerServers, typing.Dict[builtins.str, typing.Any]]]],
    read_write_endpoint_failover_policy: typing.Union[SqlFailoverGroupReadWriteEndpointFailoverPolicy, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    server_name: builtins.str,
    databases: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    readonly_endpoint_failover_policy: typing.Optional[typing.Union[SqlFailoverGroupReadonlyEndpointFailoverPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SqlFailoverGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__aa4bf8c2baaa71771d44cf1ffdb05b938af63ae2508124b4dcee11b4d23f2c9c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlFailoverGroupPartnerServers, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b2f70ec4b4b98e4feb41c837b53bec6d1586471389d35a9ffba00dc98e39e1f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__810c15c081bc44f0e36c451fb68c162e30fc3f50195f678f2f61653180386868(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68aa46831b372c662bab7fa06f0e28be5b191667da35ee580649e52cbf597534(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__422ebfdf526227324d8774a1fedf7b6847699432950c272eba7f0f28cd27af7f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__17ee28535604e4d5fccb78cd98ee5658e38cb0d4aafea44c8b1a7451ad706285(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__63d09a36b0693530dafd9cca9e9a4194e405018700d095920a14b9dcfdf23edc(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aca604fa236fec579c0ef77e8b1b332a8e41016e5947d703520c5fa5dab754b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    partner_servers: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SqlFailoverGroupPartnerServers, typing.Dict[builtins.str, typing.Any]]]],
    read_write_endpoint_failover_policy: typing.Union[SqlFailoverGroupReadWriteEndpointFailoverPolicy, typing.Dict[builtins.str, typing.Any]],
    resource_group_name: builtins.str,
    server_name: builtins.str,
    databases: typing.Optional[typing.Sequence[builtins.str]] = None,
    id: typing.Optional[builtins.str] = None,
    readonly_endpoint_failover_policy: typing.Optional[typing.Union[SqlFailoverGroupReadonlyEndpointFailoverPolicy, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[SqlFailoverGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3ecb06b3cc31a488e628c8d11c9997807dc08c946865b431c0ccd4e8d7fb0464(
    *,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7689c24c03b99f2bd6ed23652d595ae23bf13d1092f9b84c9a494ea1d173eef(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342e748d77a69f61fb3fa0136fc59d7d07f1a60bbd729ce88ed91bc514d1cb3d(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2f643ffd2375d69df49d18f40cf648b9fa3e4b748990d69a2f06de2256e7d6d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b896af23bf21d5184f21365e8dce55f24342f08f32e79dfa5dee3178eb90c469(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d2b41a69c5ab23132ec99e884fd3754f79bcac45352b21f2b6e6d01195c4b7e(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d018b621216817e718dcd675b9e7dc2ce48541ab8728043b8251529845d3261e(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SqlFailoverGroupPartnerServers]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__698947c40f278006d5cbb745d1c9ee4833fca68135e41b16a864e6a24414d6b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54b8b00336fa552c26a771eae9538e09b2d3d215365fd590ed4af33081dd5ad8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc09f5697d973dbdf6a5d0db1b48c29379ff072703cc2057196c0502add8a94b(
    value: typing.Optional[typing.Union[SqlFailoverGroupPartnerServers, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11f006a6d87d8b58b7ea278df0d8af89cc7006655ca1b32c43b16b5eaebc77ff(
    *,
    mode: builtins.str,
    grace_minutes: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72adff817169d36ce9ac473cd92ba42d384202c4eab52c31b802e10d962a7cae(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ce4433d0bda8da0cc064003c75285d66079e690e6c2924c4bd779be4ed40c46(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8fbc641a343081d116d84d3af50ff687b022269bacfdb32f0a54850f4c9e98eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ca08f0d7ab7679dd60c60d1defcf7aaef5d25b4090109079ac1976ed10cd0c2(
    value: typing.Optional[SqlFailoverGroupReadWriteEndpointFailoverPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16a7802097d6f3364bc881998396e0eaf33220616348cb80705ec718f6cf1c27(
    *,
    mode: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2f6a00ceb97330345921ceb09f402871dc6d477837d7ab77f1a8284e817894b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__28446294c66c1a80f93252615a99b75ff252b6d65a804a8cafc372de5ecb3dbd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b805faab05eb8722e3d07a5a0f23d33c5a83558c8656cf9c3e2400a308c9ddf(
    value: typing.Optional[SqlFailoverGroupReadonlyEndpointFailoverPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__583dbf1d605e6fe15f585968061ca9618c59f43766563f2d15898f10b2bcbcd1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2df9df993049ec69432f2e7090bbd089679005b24c72d3eaaa27fc5cfac8121(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__792355519abec66579100d34b012ec320e2fd47156562e5946768fb77f3ad620(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3866926bfd7d49fde121b3f9de821eaf324b48168043d40179e314ff8be52d9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d87bf18e57ec811affd84361ff04082ea0fa66a68683f4155bd6d80c5266c871(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b51ddb98b8f28a7312848f1aed3b9e5b3cfa3ad08c69ed1ed40c3d215b55bf0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18509afda5cbc136a41d2b8daf8f7b14e2460751cb23a3f80a15ea4e9aedd332(
    value: typing.Optional[typing.Union[SqlFailoverGroupTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
