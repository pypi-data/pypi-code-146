'''
# `aws_opensearch_outbound_connection`

Refer to the Terraform Registory for docs: [`aws_opensearch_outbound_connection`](https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection).
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


class OpensearchOutboundConnection(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.opensearchOutboundConnection.OpensearchOutboundConnection",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection aws_opensearch_outbound_connection}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        connection_alias: builtins.str,
        local_domain_info: typing.Union["OpensearchOutboundConnectionLocalDomainInfo", typing.Dict[builtins.str, typing.Any]],
        remote_domain_info: typing.Union["OpensearchOutboundConnectionRemoteDomainInfo", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["OpensearchOutboundConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection aws_opensearch_outbound_connection} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param connection_alias: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#connection_alias OpensearchOutboundConnection#connection_alias}.
        :param local_domain_info: local_domain_info block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#local_domain_info OpensearchOutboundConnection#local_domain_info}
        :param remote_domain_info: remote_domain_info block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#remote_domain_info OpensearchOutboundConnection#remote_domain_info}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#id OpensearchOutboundConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#timeouts OpensearchOutboundConnection#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50e38de307442d52e5fb0cc8716c325807006693eebe4f3ab35d909d343e9acb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = OpensearchOutboundConnectionConfig(
            connection_alias=connection_alias,
            local_domain_info=local_domain_info,
            remote_domain_info=remote_domain_info,
            id=id,
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

    @jsii.member(jsii_name="putLocalDomainInfo")
    def put_local_domain_info(
        self,
        *,
        domain_name: builtins.str,
        owner_id: builtins.str,
        region: builtins.str,
    ) -> None:
        '''
        :param domain_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#domain_name OpensearchOutboundConnection#domain_name}.
        :param owner_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#owner_id OpensearchOutboundConnection#owner_id}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#region OpensearchOutboundConnection#region}.
        '''
        value = OpensearchOutboundConnectionLocalDomainInfo(
            domain_name=domain_name, owner_id=owner_id, region=region
        )

        return typing.cast(None, jsii.invoke(self, "putLocalDomainInfo", [value]))

    @jsii.member(jsii_name="putRemoteDomainInfo")
    def put_remote_domain_info(
        self,
        *,
        domain_name: builtins.str,
        owner_id: builtins.str,
        region: builtins.str,
    ) -> None:
        '''
        :param domain_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#domain_name OpensearchOutboundConnection#domain_name}.
        :param owner_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#owner_id OpensearchOutboundConnection#owner_id}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#region OpensearchOutboundConnection#region}.
        '''
        value = OpensearchOutboundConnectionRemoteDomainInfo(
            domain_name=domain_name, owner_id=owner_id, region=region
        )

        return typing.cast(None, jsii.invoke(self, "putRemoteDomainInfo", [value]))

    @jsii.member(jsii_name="putTimeouts")
    def put_timeouts(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#create OpensearchOutboundConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#delete OpensearchOutboundConnection#delete}.
        '''
        value = OpensearchOutboundConnectionTimeouts(create=create, delete=delete)

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="connectionStatus")
    def connection_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionStatus"))

    @builtins.property
    @jsii.member(jsii_name="localDomainInfo")
    def local_domain_info(
        self,
    ) -> "OpensearchOutboundConnectionLocalDomainInfoOutputReference":
        return typing.cast("OpensearchOutboundConnectionLocalDomainInfoOutputReference", jsii.get(self, "localDomainInfo"))

    @builtins.property
    @jsii.member(jsii_name="remoteDomainInfo")
    def remote_domain_info(
        self,
    ) -> "OpensearchOutboundConnectionRemoteDomainInfoOutputReference":
        return typing.cast("OpensearchOutboundConnectionRemoteDomainInfoOutputReference", jsii.get(self, "remoteDomainInfo"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "OpensearchOutboundConnectionTimeoutsOutputReference":
        return typing.cast("OpensearchOutboundConnectionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="connectionAliasInput")
    def connection_alias_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectionAliasInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="localDomainInfoInput")
    def local_domain_info_input(
        self,
    ) -> typing.Optional["OpensearchOutboundConnectionLocalDomainInfo"]:
        return typing.cast(typing.Optional["OpensearchOutboundConnectionLocalDomainInfo"], jsii.get(self, "localDomainInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="remoteDomainInfoInput")
    def remote_domain_info_input(
        self,
    ) -> typing.Optional["OpensearchOutboundConnectionRemoteDomainInfo"]:
        return typing.cast(typing.Optional["OpensearchOutboundConnectionRemoteDomainInfo"], jsii.get(self, "remoteDomainInfoInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["OpensearchOutboundConnectionTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["OpensearchOutboundConnectionTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="connectionAlias")
    def connection_alias(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectionAlias"))

    @connection_alias.setter
    def connection_alias(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3db974cab328400704e37c9211c18e03ae5ba6fad2263650330f80f5592a379f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionAlias", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__821240609447c6eda7852cde0e385827ffe143cd4dc000f07d163f45944590d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.opensearchOutboundConnection.OpensearchOutboundConnectionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "connection_alias": "connectionAlias",
        "local_domain_info": "localDomainInfo",
        "remote_domain_info": "remoteDomainInfo",
        "id": "id",
        "timeouts": "timeouts",
    },
)
class OpensearchOutboundConnectionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        connection_alias: builtins.str,
        local_domain_info: typing.Union["OpensearchOutboundConnectionLocalDomainInfo", typing.Dict[builtins.str, typing.Any]],
        remote_domain_info: typing.Union["OpensearchOutboundConnectionRemoteDomainInfo", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["OpensearchOutboundConnectionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param connection_alias: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#connection_alias OpensearchOutboundConnection#connection_alias}.
        :param local_domain_info: local_domain_info block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#local_domain_info OpensearchOutboundConnection#local_domain_info}
        :param remote_domain_info: remote_domain_info block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#remote_domain_info OpensearchOutboundConnection#remote_domain_info}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#id OpensearchOutboundConnection#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#timeouts OpensearchOutboundConnection#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(local_domain_info, dict):
            local_domain_info = OpensearchOutboundConnectionLocalDomainInfo(**local_domain_info)
        if isinstance(remote_domain_info, dict):
            remote_domain_info = OpensearchOutboundConnectionRemoteDomainInfo(**remote_domain_info)
        if isinstance(timeouts, dict):
            timeouts = OpensearchOutboundConnectionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26079f48208580d2a1ecbe81e3dd9ace6fe26cf1363bb26486b4d86ddff0ae39)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument connection_alias", value=connection_alias, expected_type=type_hints["connection_alias"])
            check_type(argname="argument local_domain_info", value=local_domain_info, expected_type=type_hints["local_domain_info"])
            check_type(argname="argument remote_domain_info", value=remote_domain_info, expected_type=type_hints["remote_domain_info"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_alias": connection_alias,
            "local_domain_info": local_domain_info,
            "remote_domain_info": remote_domain_info,
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
        if id is not None:
            self._values["id"] = id
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
    def connection_alias(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#connection_alias OpensearchOutboundConnection#connection_alias}.'''
        result = self._values.get("connection_alias")
        assert result is not None, "Required property 'connection_alias' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def local_domain_info(self) -> "OpensearchOutboundConnectionLocalDomainInfo":
        '''local_domain_info block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#local_domain_info OpensearchOutboundConnection#local_domain_info}
        '''
        result = self._values.get("local_domain_info")
        assert result is not None, "Required property 'local_domain_info' is missing"
        return typing.cast("OpensearchOutboundConnectionLocalDomainInfo", result)

    @builtins.property
    def remote_domain_info(self) -> "OpensearchOutboundConnectionRemoteDomainInfo":
        '''remote_domain_info block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#remote_domain_info OpensearchOutboundConnection#remote_domain_info}
        '''
        result = self._values.get("remote_domain_info")
        assert result is not None, "Required property 'remote_domain_info' is missing"
        return typing.cast("OpensearchOutboundConnectionRemoteDomainInfo", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#id OpensearchOutboundConnection#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["OpensearchOutboundConnectionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#timeouts OpensearchOutboundConnection#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["OpensearchOutboundConnectionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpensearchOutboundConnectionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.opensearchOutboundConnection.OpensearchOutboundConnectionLocalDomainInfo",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "owner_id": "ownerId",
        "region": "region",
    },
)
class OpensearchOutboundConnectionLocalDomainInfo:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        owner_id: builtins.str,
        region: builtins.str,
    ) -> None:
        '''
        :param domain_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#domain_name OpensearchOutboundConnection#domain_name}.
        :param owner_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#owner_id OpensearchOutboundConnection#owner_id}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#region OpensearchOutboundConnection#region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42695aa92f80a58a555b98208ee1edf76d2ad72bb4d865a882ba640413686206)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument owner_id", value=owner_id, expected_type=type_hints["owner_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
            "owner_id": owner_id,
            "region": region,
        }

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#domain_name OpensearchOutboundConnection#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def owner_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#owner_id OpensearchOutboundConnection#owner_id}.'''
        result = self._values.get("owner_id")
        assert result is not None, "Required property 'owner_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#region OpensearchOutboundConnection#region}.'''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpensearchOutboundConnectionLocalDomainInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OpensearchOutboundConnectionLocalDomainInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.opensearchOutboundConnection.OpensearchOutboundConnectionLocalDomainInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__368563ef0a5b09941674c619a09bbc055c38a80dff996ccf225580eef1623825)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerIdInput")
    def owner_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4da34328f19bb501b8ab8838d19b2ce0d3fff2f90548b61a6fa4b0da176ab134)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="ownerId")
    def owner_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerId"))

    @owner_id.setter
    def owner_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1bd58c5d3d14cceed0f46442388dc2be42f41262a500cd885e1edb14b847383)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ownerId", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86290f05c46e46227f9b91d1bfd35bd8bf41aa9f207f794497d693f006c3196a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OpensearchOutboundConnectionLocalDomainInfo]:
        return typing.cast(typing.Optional[OpensearchOutboundConnectionLocalDomainInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OpensearchOutboundConnectionLocalDomainInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b4e605a45921c3e8d4697fc78f6084c0a570d1d93b1b280eed6da014aa95a14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.opensearchOutboundConnection.OpensearchOutboundConnectionRemoteDomainInfo",
    jsii_struct_bases=[],
    name_mapping={
        "domain_name": "domainName",
        "owner_id": "ownerId",
        "region": "region",
    },
)
class OpensearchOutboundConnectionRemoteDomainInfo:
    def __init__(
        self,
        *,
        domain_name: builtins.str,
        owner_id: builtins.str,
        region: builtins.str,
    ) -> None:
        '''
        :param domain_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#domain_name OpensearchOutboundConnection#domain_name}.
        :param owner_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#owner_id OpensearchOutboundConnection#owner_id}.
        :param region: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#region OpensearchOutboundConnection#region}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32f30c5e1cf3631e8e6b152b6e430a0942b860be95c61169c21fdeb7d51f9ab1)
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument owner_id", value=owner_id, expected_type=type_hints["owner_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "domain_name": domain_name,
            "owner_id": owner_id,
            "region": region,
        }

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#domain_name OpensearchOutboundConnection#domain_name}.'''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def owner_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#owner_id OpensearchOutboundConnection#owner_id}.'''
        result = self._values.get("owner_id")
        assert result is not None, "Required property 'owner_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#region OpensearchOutboundConnection#region}.'''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpensearchOutboundConnectionRemoteDomainInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OpensearchOutboundConnectionRemoteDomainInfoOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.opensearchOutboundConnection.OpensearchOutboundConnectionRemoteDomainInfoOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8ea7d335355d4e07634445f3159079ef0bbf89402852ea21fa9f08b58ffc9b61)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="domainNameInput")
    def domain_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "domainNameInput"))

    @builtins.property
    @jsii.member(jsii_name="ownerIdInput")
    def owner_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "ownerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="regionInput")
    def region_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "regionInput"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3e60a1681e14abed955fcf388d1960347d3f27d4db5dfe3e5151c695b8713d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="ownerId")
    def owner_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "ownerId"))

    @owner_id.setter
    def owner_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__29e4d0c4a3d543045797e110d6f5dad09ef16603194babe859c03263de1c29c8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ownerId", value)

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "region"))

    @region.setter
    def region(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f19a405398b2448b590b9974401cfeb63897a4c251157055edb1c88ef84639af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "region", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[OpensearchOutboundConnectionRemoteDomainInfo]:
        return typing.cast(typing.Optional[OpensearchOutboundConnectionRemoteDomainInfo], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[OpensearchOutboundConnectionRemoteDomainInfo],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__80cb1637a752362f036cb1aa337ed1baa163b774540a00d3b2a43c1709fc7eb3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-aws.opensearchOutboundConnection.OpensearchOutboundConnectionTimeouts",
    jsii_struct_bases=[],
    name_mapping={"create": "create", "delete": "delete"},
)
class OpensearchOutboundConnectionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#create OpensearchOutboundConnection#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#delete OpensearchOutboundConnection#delete}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca03a750188b355d812923238944a953312d3b85d0f03d739d69048bce4cd256)
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete

    @builtins.property
    def create(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#create OpensearchOutboundConnection#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/aws/r/opensearch_outbound_connection#delete OpensearchOutboundConnection#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpensearchOutboundConnectionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class OpensearchOutboundConnectionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-aws.opensearchOutboundConnection.OpensearchOutboundConnectionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__42ec7f737cee7d9dc81ada6932722fd6d5deb4cacbb318014513f60d1862bfab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetCreate")
    def reset_create(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCreate", []))

    @jsii.member(jsii_name="resetDelete")
    def reset_delete(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDelete", []))

    @builtins.property
    @jsii.member(jsii_name="createInput")
    def create_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "createInput"))

    @builtins.property
    @jsii.member(jsii_name="deleteInput")
    def delete_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "deleteInput"))

    @builtins.property
    @jsii.member(jsii_name="create")
    def create(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "create"))

    @create.setter
    def create(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcb61b71d50c76a06f84693e15790147a2d769815e85ed7a6dff05d2725e8753)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1eb79086c78d76a5564e7a438cabe30d7a145cf20dcbb78264cc903649f16b15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[OpensearchOutboundConnectionTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[OpensearchOutboundConnectionTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[OpensearchOutboundConnectionTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7162b75c12abe92b8b2fe434c9ebd68c0de064debdff010e47a08c723dc88b0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "OpensearchOutboundConnection",
    "OpensearchOutboundConnectionConfig",
    "OpensearchOutboundConnectionLocalDomainInfo",
    "OpensearchOutboundConnectionLocalDomainInfoOutputReference",
    "OpensearchOutboundConnectionRemoteDomainInfo",
    "OpensearchOutboundConnectionRemoteDomainInfoOutputReference",
    "OpensearchOutboundConnectionTimeouts",
    "OpensearchOutboundConnectionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__50e38de307442d52e5fb0cc8716c325807006693eebe4f3ab35d909d343e9acb(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    connection_alias: builtins.str,
    local_domain_info: typing.Union[OpensearchOutboundConnectionLocalDomainInfo, typing.Dict[builtins.str, typing.Any]],
    remote_domain_info: typing.Union[OpensearchOutboundConnectionRemoteDomainInfo, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[OpensearchOutboundConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__3db974cab328400704e37c9211c18e03ae5ba6fad2263650330f80f5592a379f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__821240609447c6eda7852cde0e385827ffe143cd4dc000f07d163f45944590d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26079f48208580d2a1ecbe81e3dd9ace6fe26cf1363bb26486b4d86ddff0ae39(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    connection_alias: builtins.str,
    local_domain_info: typing.Union[OpensearchOutboundConnectionLocalDomainInfo, typing.Dict[builtins.str, typing.Any]],
    remote_domain_info: typing.Union[OpensearchOutboundConnectionRemoteDomainInfo, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[OpensearchOutboundConnectionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42695aa92f80a58a555b98208ee1edf76d2ad72bb4d865a882ba640413686206(
    *,
    domain_name: builtins.str,
    owner_id: builtins.str,
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__368563ef0a5b09941674c619a09bbc055c38a80dff996ccf225580eef1623825(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4da34328f19bb501b8ab8838d19b2ce0d3fff2f90548b61a6fa4b0da176ab134(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1bd58c5d3d14cceed0f46442388dc2be42f41262a500cd885e1edb14b847383(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86290f05c46e46227f9b91d1bfd35bd8bf41aa9f207f794497d693f006c3196a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b4e605a45921c3e8d4697fc78f6084c0a570d1d93b1b280eed6da014aa95a14(
    value: typing.Optional[OpensearchOutboundConnectionLocalDomainInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f30c5e1cf3631e8e6b152b6e430a0942b860be95c61169c21fdeb7d51f9ab1(
    *,
    domain_name: builtins.str,
    owner_id: builtins.str,
    region: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8ea7d335355d4e07634445f3159079ef0bbf89402852ea21fa9f08b58ffc9b61(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e60a1681e14abed955fcf388d1960347d3f27d4db5dfe3e5151c695b8713d5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__29e4d0c4a3d543045797e110d6f5dad09ef16603194babe859c03263de1c29c8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f19a405398b2448b590b9974401cfeb63897a4c251157055edb1c88ef84639af(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__80cb1637a752362f036cb1aa337ed1baa163b774540a00d3b2a43c1709fc7eb3(
    value: typing.Optional[OpensearchOutboundConnectionRemoteDomainInfo],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca03a750188b355d812923238944a953312d3b85d0f03d739d69048bce4cd256(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42ec7f737cee7d9dc81ada6932722fd6d5deb4cacbb318014513f60d1862bfab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcb61b71d50c76a06f84693e15790147a2d769815e85ed7a6dff05d2725e8753(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1eb79086c78d76a5564e7a438cabe30d7a145cf20dcbb78264cc903649f16b15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7162b75c12abe92b8b2fe434c9ebd68c0de064debdff010e47a08c723dc88b0(
    value: typing.Optional[typing.Union[OpensearchOutboundConnectionTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
