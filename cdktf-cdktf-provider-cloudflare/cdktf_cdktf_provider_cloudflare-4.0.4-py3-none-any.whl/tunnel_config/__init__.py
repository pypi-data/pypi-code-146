'''
# `cloudflare_tunnel_config`

Refer to the Terraform Registory for docs: [`cloudflare_tunnel_config`](https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config).
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


class TunnelConfig(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.tunnelConfig.TunnelConfig",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config cloudflare_tunnel_config}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        config: typing.Union["TunnelConfigConfigA", typing.Dict[builtins.str, typing.Any]],
        tunnel_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config cloudflare_tunnel_config} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#account_id TunnelConfig#account_id}
        :param config: config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#config TunnelConfig#config}
        :param tunnel_id: Identifier of the Tunnel to target for this configuration. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#tunnel_id TunnelConfig#tunnel_id}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#id TunnelConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2873365409e9b0df1eb65ecca8b7d0e340aa776b9cdc673e4e91393741f048d7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = TunnelConfigConfig(
            account_id=account_id,
            config=config,
            tunnel_id=tunnel_id,
            id=id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config_])

    @jsii.member(jsii_name="putConfig")
    def put_config(
        self,
        *,
        ingress_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TunnelConfigConfigIngressRule", typing.Dict[builtins.str, typing.Any]]]],
        origin_request: typing.Optional[typing.Union["TunnelConfigConfigOriginRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        warp_routing: typing.Optional[typing.Union["TunnelConfigConfigWarpRouting", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ingress_rule: ingress_rule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#ingress_rule TunnelConfig#ingress_rule}
        :param origin_request: origin_request block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#origin_request TunnelConfig#origin_request}
        :param warp_routing: warp_routing block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#warp_routing TunnelConfig#warp_routing}
        '''
        value = TunnelConfigConfigA(
            ingress_rule=ingress_rule,
            origin_request=origin_request,
            warp_routing=warp_routing,
        )

        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> "TunnelConfigConfigAOutputReference":
        return typing.cast("TunnelConfigConfigAOutputReference", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["TunnelConfigConfigA"]:
        return typing.cast(typing.Optional["TunnelConfigConfigA"], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnelIdInput")
    def tunnel_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tunnelIdInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adb64d7a88764d46b57b3f8bd001f0647479596de59a89afc234368b39240c83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f2a7465e6d2d402ecc8d9e71bf1494c9dd8d79db479ca9a2abcbb6a816f9b760)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="tunnelId")
    def tunnel_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tunnelId"))

    @tunnel_id.setter
    def tunnel_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cf19b9c6b6ba52e5a0a9d677e429b7b49790e4cc54cffc6d0419798f666c45d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tunnelId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.tunnelConfig.TunnelConfigConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "account_id": "accountId",
        "config": "config",
        "tunnel_id": "tunnelId",
        "id": "id",
    },
)
class TunnelConfigConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        account_id: builtins.str,
        config: typing.Union["TunnelConfigConfigA", typing.Dict[builtins.str, typing.Any]],
        tunnel_id: builtins.str,
        id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#account_id TunnelConfig#account_id}
        :param config: config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#config TunnelConfig#config}
        :param tunnel_id: Identifier of the Tunnel to target for this configuration. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#tunnel_id TunnelConfig#tunnel_id}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#id TunnelConfig#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config, dict):
            config = TunnelConfigConfigA(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a11ad4e4a4b647bc24252bfaa47dee610de616c2f841dc9eae4739106074652b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument tunnel_id", value=tunnel_id, expected_type=type_hints["tunnel_id"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "config": config,
            "tunnel_id": tunnel_id,
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
    def account_id(self) -> builtins.str:
        '''The account identifier to target for the resource.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#account_id TunnelConfig#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> "TunnelConfigConfigA":
        '''config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#config TunnelConfig#config}
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast("TunnelConfigConfigA", result)

    @builtins.property
    def tunnel_id(self) -> builtins.str:
        '''Identifier of the Tunnel to target for this configuration.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#tunnel_id TunnelConfig#tunnel_id}
        '''
        result = self._values.get("tunnel_id")
        assert result is not None, "Required property 'tunnel_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#id TunnelConfig#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TunnelConfigConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.tunnelConfig.TunnelConfigConfigA",
    jsii_struct_bases=[],
    name_mapping={
        "ingress_rule": "ingressRule",
        "origin_request": "originRequest",
        "warp_routing": "warpRouting",
    },
)
class TunnelConfigConfigA:
    def __init__(
        self,
        *,
        ingress_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TunnelConfigConfigIngressRule", typing.Dict[builtins.str, typing.Any]]]],
        origin_request: typing.Optional[typing.Union["TunnelConfigConfigOriginRequest", typing.Dict[builtins.str, typing.Any]]] = None,
        warp_routing: typing.Optional[typing.Union["TunnelConfigConfigWarpRouting", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param ingress_rule: ingress_rule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#ingress_rule TunnelConfig#ingress_rule}
        :param origin_request: origin_request block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#origin_request TunnelConfig#origin_request}
        :param warp_routing: warp_routing block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#warp_routing TunnelConfig#warp_routing}
        '''
        if isinstance(origin_request, dict):
            origin_request = TunnelConfigConfigOriginRequest(**origin_request)
        if isinstance(warp_routing, dict):
            warp_routing = TunnelConfigConfigWarpRouting(**warp_routing)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89cc5d0e9e1d5a1b6a864bc0e3744349186961ca4a2ded60c0fa08fcb54e1e59)
            check_type(argname="argument ingress_rule", value=ingress_rule, expected_type=type_hints["ingress_rule"])
            check_type(argname="argument origin_request", value=origin_request, expected_type=type_hints["origin_request"])
            check_type(argname="argument warp_routing", value=warp_routing, expected_type=type_hints["warp_routing"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "ingress_rule": ingress_rule,
        }
        if origin_request is not None:
            self._values["origin_request"] = origin_request
        if warp_routing is not None:
            self._values["warp_routing"] = warp_routing

    @builtins.property
    def ingress_rule(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TunnelConfigConfigIngressRule"]]:
        '''ingress_rule block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#ingress_rule TunnelConfig#ingress_rule}
        '''
        result = self._values.get("ingress_rule")
        assert result is not None, "Required property 'ingress_rule' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TunnelConfigConfigIngressRule"]], result)

    @builtins.property
    def origin_request(self) -> typing.Optional["TunnelConfigConfigOriginRequest"]:
        '''origin_request block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#origin_request TunnelConfig#origin_request}
        '''
        result = self._values.get("origin_request")
        return typing.cast(typing.Optional["TunnelConfigConfigOriginRequest"], result)

    @builtins.property
    def warp_routing(self) -> typing.Optional["TunnelConfigConfigWarpRouting"]:
        '''warp_routing block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#warp_routing TunnelConfig#warp_routing}
        '''
        result = self._values.get("warp_routing")
        return typing.cast(typing.Optional["TunnelConfigConfigWarpRouting"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TunnelConfigConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TunnelConfigConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.tunnelConfig.TunnelConfigConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3a18286199845bfde0d2fb0f3bbde7f424d6d88d46430c7ae02485b8cab7874c)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIngressRule")
    def put_ingress_rule(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TunnelConfigConfigIngressRule", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19c81e6e5ad52082f0a35703b5a6525f44eecb24cb0fcdd6911ae4d4b9d6b19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIngressRule", [value]))

    @jsii.member(jsii_name="putOriginRequest")
    def put_origin_request(
        self,
        *,
        bastion_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ca_pool: typing.Optional[builtins.str] = None,
        connect_timeout: typing.Optional[builtins.str] = None,
        disable_chunked_encoding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_host_header: typing.Optional[builtins.str] = None,
        ip_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TunnelConfigConfigOriginRequestIpRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        keep_alive_connections: typing.Optional[jsii.Number] = None,
        keep_alive_timeout: typing.Optional[builtins.str] = None,
        no_happy_eyeballs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        no_tls_verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        origin_server_name: typing.Optional[builtins.str] = None,
        proxy_address: typing.Optional[builtins.str] = None,
        proxy_port: typing.Optional[jsii.Number] = None,
        proxy_type: typing.Optional[builtins.str] = None,
        tcp_keep_alive: typing.Optional[builtins.str] = None,
        tls_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bastion_mode: Runs as jump host. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#bastion_mode TunnelConfig#bastion_mode}
        :param ca_pool: Path to the certificate authority (CA) for the certificate of your origin. This option should be used only if your certificate is not signed by Cloudflare. Defaults to ``""``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#ca_pool TunnelConfig#ca_pool}
        :param connect_timeout: Timeout for establishing a new TCP connection to your origin server. This excludes the time taken to establish TLS, which is controlled by ``tlsTimeout``. Defaults to ``30s``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#connect_timeout TunnelConfig#connect_timeout}
        :param disable_chunked_encoding: Disables chunked transfer encoding. Useful if you are running a Web Server Gateway Interface (WSGI) server. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#disable_chunked_encoding TunnelConfig#disable_chunked_encoding}
        :param http_host_header: Sets the HTTP Host header on requests sent to the local service. Defaults to ``""``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#http_host_header TunnelConfig#http_host_header}
        :param ip_rules: ip_rules block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#ip_rules TunnelConfig#ip_rules}
        :param keep_alive_connections: Maximum number of idle keepalive connections between Tunnel and your origin. This does not restrict the total number of concurrent connections. Defaults to ``100``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#keep_alive_connections TunnelConfig#keep_alive_connections}
        :param keep_alive_timeout: Timeout after which an idle keepalive connection can be discarded. Defaults to ``1m30s``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#keep_alive_timeout TunnelConfig#keep_alive_timeout}
        :param no_happy_eyeballs: Disable the “happy eyeballs” algorithm for IPv4/IPv6 fallback if your local network has misconfigured one of the protocols. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#no_happy_eyeballs TunnelConfig#no_happy_eyeballs}
        :param no_tls_verify: Disables TLS verification of the certificate presented by your origin. Will allow any certificate from the origin to be accepted. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#no_tls_verify TunnelConfig#no_tls_verify}
        :param origin_server_name: Hostname that cloudflared should expect from your origin server certificate. Defaults to ``""``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#origin_server_name TunnelConfig#origin_server_name}
        :param proxy_address: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures the listen address for that proxy. Defaults to ``127.0.0.1``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#proxy_address TunnelConfig#proxy_address}
        :param proxy_port: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures the listen port for that proxy. If set to zero, an unused port will randomly be chosen. Defaults to ``0``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#proxy_port TunnelConfig#proxy_port}
        :param proxy_type: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures what type of proxy will be started. Available values: ``, ``socks``. Defaults to ``""``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#proxy_type TunnelConfig#proxy_type}
        :param tcp_keep_alive: The timeout after which a TCP keepalive packet is sent on a connection between Tunnel and the origin server. Defaults to ``30s``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#tcp_keep_alive TunnelConfig#tcp_keep_alive}
        :param tls_timeout: Timeout for completing a TLS handshake to your origin server, if you have chosen to connect Tunnel to an HTTPS server. Defaults to ``10s``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#tls_timeout TunnelConfig#tls_timeout}
        '''
        value = TunnelConfigConfigOriginRequest(
            bastion_mode=bastion_mode,
            ca_pool=ca_pool,
            connect_timeout=connect_timeout,
            disable_chunked_encoding=disable_chunked_encoding,
            http_host_header=http_host_header,
            ip_rules=ip_rules,
            keep_alive_connections=keep_alive_connections,
            keep_alive_timeout=keep_alive_timeout,
            no_happy_eyeballs=no_happy_eyeballs,
            no_tls_verify=no_tls_verify,
            origin_server_name=origin_server_name,
            proxy_address=proxy_address,
            proxy_port=proxy_port,
            proxy_type=proxy_type,
            tcp_keep_alive=tcp_keep_alive,
            tls_timeout=tls_timeout,
        )

        return typing.cast(None, jsii.invoke(self, "putOriginRequest", [value]))

    @jsii.member(jsii_name="putWarpRouting")
    def put_warp_routing(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether WARP routing is enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#enabled TunnelConfig#enabled}
        '''
        value = TunnelConfigConfigWarpRouting(enabled=enabled)

        return typing.cast(None, jsii.invoke(self, "putWarpRouting", [value]))

    @jsii.member(jsii_name="resetOriginRequest")
    def reset_origin_request(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginRequest", []))

    @jsii.member(jsii_name="resetWarpRouting")
    def reset_warp_routing(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWarpRouting", []))

    @builtins.property
    @jsii.member(jsii_name="ingressRule")
    def ingress_rule(self) -> "TunnelConfigConfigIngressRuleList":
        return typing.cast("TunnelConfigConfigIngressRuleList", jsii.get(self, "ingressRule"))

    @builtins.property
    @jsii.member(jsii_name="originRequest")
    def origin_request(self) -> "TunnelConfigConfigOriginRequestOutputReference":
        return typing.cast("TunnelConfigConfigOriginRequestOutputReference", jsii.get(self, "originRequest"))

    @builtins.property
    @jsii.member(jsii_name="warpRouting")
    def warp_routing(self) -> "TunnelConfigConfigWarpRoutingOutputReference":
        return typing.cast("TunnelConfigConfigWarpRoutingOutputReference", jsii.get(self, "warpRouting"))

    @builtins.property
    @jsii.member(jsii_name="ingressRuleInput")
    def ingress_rule_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TunnelConfigConfigIngressRule"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TunnelConfigConfigIngressRule"]]], jsii.get(self, "ingressRuleInput"))

    @builtins.property
    @jsii.member(jsii_name="originRequestInput")
    def origin_request_input(
        self,
    ) -> typing.Optional["TunnelConfigConfigOriginRequest"]:
        return typing.cast(typing.Optional["TunnelConfigConfigOriginRequest"], jsii.get(self, "originRequestInput"))

    @builtins.property
    @jsii.member(jsii_name="warpRoutingInput")
    def warp_routing_input(self) -> typing.Optional["TunnelConfigConfigWarpRouting"]:
        return typing.cast(typing.Optional["TunnelConfigConfigWarpRouting"], jsii.get(self, "warpRoutingInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TunnelConfigConfigA]:
        return typing.cast(typing.Optional[TunnelConfigConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(self, value: typing.Optional[TunnelConfigConfigA]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3b4e14650ef3046fef1a9800d21683a014baf2cd9e146c2618e3f7cd3bee57d5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.tunnelConfig.TunnelConfigConfigIngressRule",
    jsii_struct_bases=[],
    name_mapping={"service": "service", "hostname": "hostname", "path": "path"},
)
class TunnelConfigConfigIngressRule:
    def __init__(
        self,
        *,
        service: builtins.str,
        hostname: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service: Name of the service to which the request will be sent. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#service TunnelConfig#service}
        :param hostname: Hostname to match the incoming request with. If the hostname matches, the request will be sent to the service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#hostname TunnelConfig#hostname}
        :param path: Path of the incoming request. If the path matches, the request will be sent to the local service. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#path TunnelConfig#path}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f784430427980cd04622c33b458a1739196ae77ba23cd7ff09f73edf2c91daec)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
            check_type(argname="argument hostname", value=hostname, expected_type=type_hints["hostname"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "service": service,
        }
        if hostname is not None:
            self._values["hostname"] = hostname
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def service(self) -> builtins.str:
        '''Name of the service to which the request will be sent.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#service TunnelConfig#service}
        '''
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def hostname(self) -> typing.Optional[builtins.str]:
        '''Hostname to match the incoming request with. If the hostname matches, the request will be sent to the service.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#hostname TunnelConfig#hostname}
        '''
        result = self._values.get("hostname")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''Path of the incoming request. If the path matches, the request will be sent to the local service.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#path TunnelConfig#path}
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TunnelConfigConfigIngressRule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TunnelConfigConfigIngressRuleList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.tunnelConfig.TunnelConfigConfigIngressRuleList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f377c3fb53b1c0341f8815f6329d66d94a7865301059721ee21cf43010c3f1d)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "TunnelConfigConfigIngressRuleOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e5396bfe0289e2d8da8f7cfe76da6a0680e5ee4271e526c4fe273ac5a4a4f49)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TunnelConfigConfigIngressRuleOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7210eb5bc056760ec57e2a67541da5773dd1ae357752df0d17fae0747060e51f)
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
            type_hints = typing.get_type_hints(_typecheckingstub__72bdf067dadc4373b039c8c0b152ea2fdb0bb94c675a85a252d6eb10976167fb)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05f636658f86ff607dbdf2bf673de030fa316ce87180f476da18a403e5ce99b8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TunnelConfigConfigIngressRule]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TunnelConfigConfigIngressRule]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TunnelConfigConfigIngressRule]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8d9d386b1ebcc606b18815a8153fdf7edd834ef8d7461e904bc73281b8cb73a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class TunnelConfigConfigIngressRuleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.tunnelConfig.TunnelConfigConfigIngressRuleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bdbfd200b4436bc42193e0aa1e24bf92a29ee35e99c190937f159162b54612a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetHostname")
    def reset_hostname(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHostname", []))

    @jsii.member(jsii_name="resetPath")
    def reset_path(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPath", []))

    @builtins.property
    @jsii.member(jsii_name="hostnameInput")
    def hostname_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostnameInput"))

    @builtins.property
    @jsii.member(jsii_name="pathInput")
    def path_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pathInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceInput")
    def service_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceInput"))

    @builtins.property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "hostname"))

    @hostname.setter
    def hostname(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f52d850e07ba2514a13c6129dfa4a901c8dccaa191ca46fd824b5153bd70ad6f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "hostname", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "path"))

    @path.setter
    def path(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f4579d4c27fdf7b5ae7ccebfd1fefd6890f8342f83958aee7d28c10d6529ede)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "service"))

    @service.setter
    def service(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b74bbdd6192fcf35358a1b9c96f9550d5ba8ad4f443f3f5904bc4faaf0fedcf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "service", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[TunnelConfigConfigIngressRule, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[TunnelConfigConfigIngressRule, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[TunnelConfigConfigIngressRule, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f3dfaffb8afa2e91a1b6efe8506d1564d707031637fcf078ce246107b331e33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.tunnelConfig.TunnelConfigConfigOriginRequest",
    jsii_struct_bases=[],
    name_mapping={
        "bastion_mode": "bastionMode",
        "ca_pool": "caPool",
        "connect_timeout": "connectTimeout",
        "disable_chunked_encoding": "disableChunkedEncoding",
        "http_host_header": "httpHostHeader",
        "ip_rules": "ipRules",
        "keep_alive_connections": "keepAliveConnections",
        "keep_alive_timeout": "keepAliveTimeout",
        "no_happy_eyeballs": "noHappyEyeballs",
        "no_tls_verify": "noTlsVerify",
        "origin_server_name": "originServerName",
        "proxy_address": "proxyAddress",
        "proxy_port": "proxyPort",
        "proxy_type": "proxyType",
        "tcp_keep_alive": "tcpKeepAlive",
        "tls_timeout": "tlsTimeout",
    },
)
class TunnelConfigConfigOriginRequest:
    def __init__(
        self,
        *,
        bastion_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ca_pool: typing.Optional[builtins.str] = None,
        connect_timeout: typing.Optional[builtins.str] = None,
        disable_chunked_encoding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        http_host_header: typing.Optional[builtins.str] = None,
        ip_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["TunnelConfigConfigOriginRequestIpRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        keep_alive_connections: typing.Optional[jsii.Number] = None,
        keep_alive_timeout: typing.Optional[builtins.str] = None,
        no_happy_eyeballs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        no_tls_verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        origin_server_name: typing.Optional[builtins.str] = None,
        proxy_address: typing.Optional[builtins.str] = None,
        proxy_port: typing.Optional[jsii.Number] = None,
        proxy_type: typing.Optional[builtins.str] = None,
        tcp_keep_alive: typing.Optional[builtins.str] = None,
        tls_timeout: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param bastion_mode: Runs as jump host. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#bastion_mode TunnelConfig#bastion_mode}
        :param ca_pool: Path to the certificate authority (CA) for the certificate of your origin. This option should be used only if your certificate is not signed by Cloudflare. Defaults to ``""``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#ca_pool TunnelConfig#ca_pool}
        :param connect_timeout: Timeout for establishing a new TCP connection to your origin server. This excludes the time taken to establish TLS, which is controlled by ``tlsTimeout``. Defaults to ``30s``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#connect_timeout TunnelConfig#connect_timeout}
        :param disable_chunked_encoding: Disables chunked transfer encoding. Useful if you are running a Web Server Gateway Interface (WSGI) server. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#disable_chunked_encoding TunnelConfig#disable_chunked_encoding}
        :param http_host_header: Sets the HTTP Host header on requests sent to the local service. Defaults to ``""``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#http_host_header TunnelConfig#http_host_header}
        :param ip_rules: ip_rules block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#ip_rules TunnelConfig#ip_rules}
        :param keep_alive_connections: Maximum number of idle keepalive connections between Tunnel and your origin. This does not restrict the total number of concurrent connections. Defaults to ``100``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#keep_alive_connections TunnelConfig#keep_alive_connections}
        :param keep_alive_timeout: Timeout after which an idle keepalive connection can be discarded. Defaults to ``1m30s``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#keep_alive_timeout TunnelConfig#keep_alive_timeout}
        :param no_happy_eyeballs: Disable the “happy eyeballs” algorithm for IPv4/IPv6 fallback if your local network has misconfigured one of the protocols. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#no_happy_eyeballs TunnelConfig#no_happy_eyeballs}
        :param no_tls_verify: Disables TLS verification of the certificate presented by your origin. Will allow any certificate from the origin to be accepted. Defaults to ``false``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#no_tls_verify TunnelConfig#no_tls_verify}
        :param origin_server_name: Hostname that cloudflared should expect from your origin server certificate. Defaults to ``""``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#origin_server_name TunnelConfig#origin_server_name}
        :param proxy_address: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures the listen address for that proxy. Defaults to ``127.0.0.1``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#proxy_address TunnelConfig#proxy_address}
        :param proxy_port: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures the listen port for that proxy. If set to zero, an unused port will randomly be chosen. Defaults to ``0``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#proxy_port TunnelConfig#proxy_port}
        :param proxy_type: cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP. This configures what type of proxy will be started. Available values: ``, ``socks``. Defaults to ``""``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#proxy_type TunnelConfig#proxy_type}
        :param tcp_keep_alive: The timeout after which a TCP keepalive packet is sent on a connection between Tunnel and the origin server. Defaults to ``30s``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#tcp_keep_alive TunnelConfig#tcp_keep_alive}
        :param tls_timeout: Timeout for completing a TLS handshake to your origin server, if you have chosen to connect Tunnel to an HTTPS server. Defaults to ``10s``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#tls_timeout TunnelConfig#tls_timeout}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75a6b4e932c816ecccf74e50b0998f8c8050bd0f3f66896930e9ebd86b451a0a)
            check_type(argname="argument bastion_mode", value=bastion_mode, expected_type=type_hints["bastion_mode"])
            check_type(argname="argument ca_pool", value=ca_pool, expected_type=type_hints["ca_pool"])
            check_type(argname="argument connect_timeout", value=connect_timeout, expected_type=type_hints["connect_timeout"])
            check_type(argname="argument disable_chunked_encoding", value=disable_chunked_encoding, expected_type=type_hints["disable_chunked_encoding"])
            check_type(argname="argument http_host_header", value=http_host_header, expected_type=type_hints["http_host_header"])
            check_type(argname="argument ip_rules", value=ip_rules, expected_type=type_hints["ip_rules"])
            check_type(argname="argument keep_alive_connections", value=keep_alive_connections, expected_type=type_hints["keep_alive_connections"])
            check_type(argname="argument keep_alive_timeout", value=keep_alive_timeout, expected_type=type_hints["keep_alive_timeout"])
            check_type(argname="argument no_happy_eyeballs", value=no_happy_eyeballs, expected_type=type_hints["no_happy_eyeballs"])
            check_type(argname="argument no_tls_verify", value=no_tls_verify, expected_type=type_hints["no_tls_verify"])
            check_type(argname="argument origin_server_name", value=origin_server_name, expected_type=type_hints["origin_server_name"])
            check_type(argname="argument proxy_address", value=proxy_address, expected_type=type_hints["proxy_address"])
            check_type(argname="argument proxy_port", value=proxy_port, expected_type=type_hints["proxy_port"])
            check_type(argname="argument proxy_type", value=proxy_type, expected_type=type_hints["proxy_type"])
            check_type(argname="argument tcp_keep_alive", value=tcp_keep_alive, expected_type=type_hints["tcp_keep_alive"])
            check_type(argname="argument tls_timeout", value=tls_timeout, expected_type=type_hints["tls_timeout"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if bastion_mode is not None:
            self._values["bastion_mode"] = bastion_mode
        if ca_pool is not None:
            self._values["ca_pool"] = ca_pool
        if connect_timeout is not None:
            self._values["connect_timeout"] = connect_timeout
        if disable_chunked_encoding is not None:
            self._values["disable_chunked_encoding"] = disable_chunked_encoding
        if http_host_header is not None:
            self._values["http_host_header"] = http_host_header
        if ip_rules is not None:
            self._values["ip_rules"] = ip_rules
        if keep_alive_connections is not None:
            self._values["keep_alive_connections"] = keep_alive_connections
        if keep_alive_timeout is not None:
            self._values["keep_alive_timeout"] = keep_alive_timeout
        if no_happy_eyeballs is not None:
            self._values["no_happy_eyeballs"] = no_happy_eyeballs
        if no_tls_verify is not None:
            self._values["no_tls_verify"] = no_tls_verify
        if origin_server_name is not None:
            self._values["origin_server_name"] = origin_server_name
        if proxy_address is not None:
            self._values["proxy_address"] = proxy_address
        if proxy_port is not None:
            self._values["proxy_port"] = proxy_port
        if proxy_type is not None:
            self._values["proxy_type"] = proxy_type
        if tcp_keep_alive is not None:
            self._values["tcp_keep_alive"] = tcp_keep_alive
        if tls_timeout is not None:
            self._values["tls_timeout"] = tls_timeout

    @builtins.property
    def bastion_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Runs as jump host.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#bastion_mode TunnelConfig#bastion_mode}
        '''
        result = self._values.get("bastion_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ca_pool(self) -> typing.Optional[builtins.str]:
        '''Path to the certificate authority (CA) for the certificate of your origin.

        This option should be used only if your certificate is not signed by Cloudflare. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#ca_pool TunnelConfig#ca_pool}
        '''
        result = self._values.get("ca_pool")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def connect_timeout(self) -> typing.Optional[builtins.str]:
        '''Timeout for establishing a new TCP connection to your origin server.

        This excludes the time taken to establish TLS, which is controlled by ``tlsTimeout``. Defaults to ``30s``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#connect_timeout TunnelConfig#connect_timeout}
        '''
        result = self._values.get("connect_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def disable_chunked_encoding(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disables chunked transfer encoding. Useful if you are running a Web Server Gateway Interface (WSGI) server. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#disable_chunked_encoding TunnelConfig#disable_chunked_encoding}
        '''
        result = self._values.get("disable_chunked_encoding")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def http_host_header(self) -> typing.Optional[builtins.str]:
        '''Sets the HTTP Host header on requests sent to the local service. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#http_host_header TunnelConfig#http_host_header}
        '''
        result = self._values.get("http_host_header")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TunnelConfigConfigOriginRequestIpRules"]]]:
        '''ip_rules block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#ip_rules TunnelConfig#ip_rules}
        '''
        result = self._values.get("ip_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["TunnelConfigConfigOriginRequestIpRules"]]], result)

    @builtins.property
    def keep_alive_connections(self) -> typing.Optional[jsii.Number]:
        '''Maximum number of idle keepalive connections between Tunnel and your origin.

        This does not restrict the total number of concurrent connections. Defaults to ``100``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#keep_alive_connections TunnelConfig#keep_alive_connections}
        '''
        result = self._values.get("keep_alive_connections")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def keep_alive_timeout(self) -> typing.Optional[builtins.str]:
        '''Timeout after which an idle keepalive connection can be discarded. Defaults to ``1m30s``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#keep_alive_timeout TunnelConfig#keep_alive_timeout}
        '''
        result = self._values.get("keep_alive_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def no_happy_eyeballs(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disable the “happy eyeballs” algorithm for IPv4/IPv6 fallback if your local network has misconfigured one of the protocols.

        Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#no_happy_eyeballs TunnelConfig#no_happy_eyeballs}
        '''
        result = self._values.get("no_happy_eyeballs")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def no_tls_verify(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Disables TLS verification of the certificate presented by your origin.

        Will allow any certificate from the origin to be accepted. Defaults to ``false``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#no_tls_verify TunnelConfig#no_tls_verify}
        '''
        result = self._values.get("no_tls_verify")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def origin_server_name(self) -> typing.Optional[builtins.str]:
        '''Hostname that cloudflared should expect from your origin server certificate. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#origin_server_name TunnelConfig#origin_server_name}
        '''
        result = self._values.get("origin_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_address(self) -> typing.Optional[builtins.str]:
        '''cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP.

        This configures the listen address for that proxy. Defaults to ``127.0.0.1``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#proxy_address TunnelConfig#proxy_address}
        '''
        result = self._values.get("proxy_address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy_port(self) -> typing.Optional[jsii.Number]:
        '''cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP.

        This configures the listen port for that proxy. If set to zero, an unused port will randomly be chosen. Defaults to ``0``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#proxy_port TunnelConfig#proxy_port}
        '''
        result = self._values.get("proxy_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def proxy_type(self) -> typing.Optional[builtins.str]:
        '''cloudflared starts a proxy server to translate HTTP traffic into TCP when proxying, for example, SSH or RDP.

        This configures what type of proxy will be started. Available values: ``, ``socks``. Defaults to ``""``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#proxy_type TunnelConfig#proxy_type}
        '''
        result = self._values.get("proxy_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tcp_keep_alive(self) -> typing.Optional[builtins.str]:
        '''The timeout after which a TCP keepalive packet is sent on a connection between Tunnel and the origin server.

        Defaults to ``30s``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#tcp_keep_alive TunnelConfig#tcp_keep_alive}
        '''
        result = self._values.get("tcp_keep_alive")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tls_timeout(self) -> typing.Optional[builtins.str]:
        '''Timeout for completing a TLS handshake to your origin server, if you have chosen to connect Tunnel to an HTTPS server.

        Defaults to ``10s``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#tls_timeout TunnelConfig#tls_timeout}
        '''
        result = self._values.get("tls_timeout")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TunnelConfigConfigOriginRequest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.tunnelConfig.TunnelConfigConfigOriginRequestIpRules",
    jsii_struct_bases=[],
    name_mapping={"allow": "allow", "ports": "ports", "prefix": "prefix"},
)
class TunnelConfigConfigOriginRequestIpRules:
    def __init__(
        self,
        *,
        allow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param allow: Whether to allow the IP prefix. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#allow TunnelConfig#allow}
        :param ports: Ports to use within the IP rule. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#ports TunnelConfig#ports}
        :param prefix: IP rule prefix. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#prefix TunnelConfig#prefix}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2303abf8905cd3b23743d0700d618409badb75a58225cfc2aa3c22283f84f309)
            check_type(argname="argument allow", value=allow, expected_type=type_hints["allow"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow is not None:
            self._values["allow"] = allow
        if ports is not None:
            self._values["ports"] = ports
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def allow(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether to allow the IP prefix.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#allow TunnelConfig#allow}
        '''
        result = self._values.get("allow")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Ports to use within the IP rule.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#ports TunnelConfig#ports}
        '''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''IP rule prefix.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#prefix TunnelConfig#prefix}
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TunnelConfigConfigOriginRequestIpRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TunnelConfigConfigOriginRequestIpRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.tunnelConfig.TunnelConfigConfigOriginRequestIpRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__14872396128c13233f32f7ab2a74dbf60a74bcfe51d721ec8eef2ae6a782a404)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "TunnelConfigConfigOriginRequestIpRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__361f424421b66515f19834e31ef0b557d7c8d97af78cc8a248451389aa19daeb)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("TunnelConfigConfigOriginRequestIpRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15ecd8d3046f6c70bec99e34eed7b249cb3ac4b4a0d0e7c66f31140705095ced)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb24f3658526eb73f9bf9b7364179198151edfe1497921cdd414c55394792a0a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__05786c0d219923c85d0ba6414d850d400ca2613ad38e616d9f86dd115585a96d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TunnelConfigConfigOriginRequestIpRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TunnelConfigConfigOriginRequestIpRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TunnelConfigConfigOriginRequestIpRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__342c0c94d0fb1a0ff9e84a882d670b337fba4fa022023f3a9973e4bf1046e66f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class TunnelConfigConfigOriginRequestIpRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.tunnelConfig.TunnelConfigConfigOriginRequestIpRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4a9c96546c8cdbfdd349d807be72cbb9d6d996d928fd863f08af24548e43922a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAllow")
    def reset_allow(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAllow", []))

    @jsii.member(jsii_name="resetPorts")
    def reset_ports(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPorts", []))

    @jsii.member(jsii_name="resetPrefix")
    def reset_prefix(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrefix", []))

    @builtins.property
    @jsii.member(jsii_name="allowInput")
    def allow_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "allowInput"))

    @builtins.property
    @jsii.member(jsii_name="portsInput")
    def ports_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "portsInput"))

    @builtins.property
    @jsii.member(jsii_name="prefixInput")
    def prefix_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "prefixInput"))

    @builtins.property
    @jsii.member(jsii_name="allow")
    def allow(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "allow"))

    @allow.setter
    def allow(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c8bc0428e8f2377ec0131aa90f51b51291b5be6db469a7216d2c20b66b333311)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "allow", value)

    @builtins.property
    @jsii.member(jsii_name="ports")
    def ports(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "ports"))

    @ports.setter
    def ports(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d56127894a6ba484b70f886e363134a86b699b7760f1dd201d341c6fd985ecf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ports", value)

    @builtins.property
    @jsii.member(jsii_name="prefix")
    def prefix(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "prefix"))

    @prefix.setter
    def prefix(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66e458be25a6430564455c68f75320f2c02085f1e6b1c15c3758a0ef4133d17c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "prefix", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[TunnelConfigConfigOriginRequestIpRules, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[TunnelConfigConfigOriginRequestIpRules, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[TunnelConfigConfigOriginRequestIpRules, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c756736688b11202cdd6a631fe39f7b17996dec1ae7feb780c2de89cd40f164b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class TunnelConfigConfigOriginRequestOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.tunnelConfig.TunnelConfigConfigOriginRequestOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d179b8176d7ecd6ba317c4ed505fddda2fcc1d4fa554c94ba3333bbc3ca7aed7)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putIpRules")
    def put_ip_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TunnelConfigConfigOriginRequestIpRules, typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0573b99701a51b4e9ce6d6805cbf0404fab324af81cb902e07814101213795b1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putIpRules", [value]))

    @jsii.member(jsii_name="resetBastionMode")
    def reset_bastion_mode(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetBastionMode", []))

    @jsii.member(jsii_name="resetCaPool")
    def reset_ca_pool(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaPool", []))

    @jsii.member(jsii_name="resetConnectTimeout")
    def reset_connect_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConnectTimeout", []))

    @jsii.member(jsii_name="resetDisableChunkedEncoding")
    def reset_disable_chunked_encoding(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDisableChunkedEncoding", []))

    @jsii.member(jsii_name="resetHttpHostHeader")
    def reset_http_host_header(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHttpHostHeader", []))

    @jsii.member(jsii_name="resetIpRules")
    def reset_ip_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpRules", []))

    @jsii.member(jsii_name="resetKeepAliveConnections")
    def reset_keep_alive_connections(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepAliveConnections", []))

    @jsii.member(jsii_name="resetKeepAliveTimeout")
    def reset_keep_alive_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetKeepAliveTimeout", []))

    @jsii.member(jsii_name="resetNoHappyEyeballs")
    def reset_no_happy_eyeballs(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoHappyEyeballs", []))

    @jsii.member(jsii_name="resetNoTlsVerify")
    def reset_no_tls_verify(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNoTlsVerify", []))

    @jsii.member(jsii_name="resetOriginServerName")
    def reset_origin_server_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOriginServerName", []))

    @jsii.member(jsii_name="resetProxyAddress")
    def reset_proxy_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyAddress", []))

    @jsii.member(jsii_name="resetProxyPort")
    def reset_proxy_port(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyPort", []))

    @jsii.member(jsii_name="resetProxyType")
    def reset_proxy_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetProxyType", []))

    @jsii.member(jsii_name="resetTcpKeepAlive")
    def reset_tcp_keep_alive(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTcpKeepAlive", []))

    @jsii.member(jsii_name="resetTlsTimeout")
    def reset_tls_timeout(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTlsTimeout", []))

    @builtins.property
    @jsii.member(jsii_name="ipRules")
    def ip_rules(self) -> TunnelConfigConfigOriginRequestIpRulesList:
        return typing.cast(TunnelConfigConfigOriginRequestIpRulesList, jsii.get(self, "ipRules"))

    @builtins.property
    @jsii.member(jsii_name="bastionModeInput")
    def bastion_mode_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "bastionModeInput"))

    @builtins.property
    @jsii.member(jsii_name="caPoolInput")
    def ca_pool_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "caPoolInput"))

    @builtins.property
    @jsii.member(jsii_name="connectTimeoutInput")
    def connect_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "connectTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="disableChunkedEncodingInput")
    def disable_chunked_encoding_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "disableChunkedEncodingInput"))

    @builtins.property
    @jsii.member(jsii_name="httpHostHeaderInput")
    def http_host_header_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "httpHostHeaderInput"))

    @builtins.property
    @jsii.member(jsii_name="ipRulesInput")
    def ip_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TunnelConfigConfigOriginRequestIpRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TunnelConfigConfigOriginRequestIpRules]]], jsii.get(self, "ipRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="keepAliveConnectionsInput")
    def keep_alive_connections_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "keepAliveConnectionsInput"))

    @builtins.property
    @jsii.member(jsii_name="keepAliveTimeoutInput")
    def keep_alive_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "keepAliveTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="noHappyEyeballsInput")
    def no_happy_eyeballs_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noHappyEyeballsInput"))

    @builtins.property
    @jsii.member(jsii_name="noTlsVerifyInput")
    def no_tls_verify_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "noTlsVerifyInput"))

    @builtins.property
    @jsii.member(jsii_name="originServerNameInput")
    def origin_server_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "originServerNameInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyAddressInput")
    def proxy_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proxyAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyPortInput")
    def proxy_port_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "proxyPortInput"))

    @builtins.property
    @jsii.member(jsii_name="proxyTypeInput")
    def proxy_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "proxyTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="tcpKeepAliveInput")
    def tcp_keep_alive_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tcpKeepAliveInput"))

    @builtins.property
    @jsii.member(jsii_name="tlsTimeoutInput")
    def tls_timeout_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsTimeoutInput"))

    @builtins.property
    @jsii.member(jsii_name="bastionMode")
    def bastion_mode(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "bastionMode"))

    @bastion_mode.setter
    def bastion_mode(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8f2feb44eb924b9aff00f5b9af79a6bf6377b5c40d95e587830a65ce3b77d9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "bastionMode", value)

    @builtins.property
    @jsii.member(jsii_name="caPool")
    def ca_pool(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caPool"))

    @ca_pool.setter
    def ca_pool(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36f9210912262ac939002fd7948da9a6087bd3ad7dee69a34aa9e75d68768636)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caPool", value)

    @builtins.property
    @jsii.member(jsii_name="connectTimeout")
    def connect_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "connectTimeout"))

    @connect_timeout.setter
    def connect_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a19d2486d7d71151142c8e6e2bca4eedb4215393a547e5baa0f9ffee86006585)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="disableChunkedEncoding")
    def disable_chunked_encoding(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "disableChunkedEncoding"))

    @disable_chunked_encoding.setter
    def disable_chunked_encoding(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9beb9a4ea10bad01158a720f74b002eeffab2af4e13cd4fe9ad79664b8c52327)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "disableChunkedEncoding", value)

    @builtins.property
    @jsii.member(jsii_name="httpHostHeader")
    def http_host_header(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "httpHostHeader"))

    @http_host_header.setter
    def http_host_header(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__607ba1756de072b7c394e4e98214fc2534ef392fd112c3baf63792bc4c5075c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpHostHeader", value)

    @builtins.property
    @jsii.member(jsii_name="keepAliveConnections")
    def keep_alive_connections(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "keepAliveConnections"))

    @keep_alive_connections.setter
    def keep_alive_connections(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57f18017bfa3cf480fa5c11f431c8094e27eef7e9bb308fa9430bfdaf7b69d6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepAliveConnections", value)

    @builtins.property
    @jsii.member(jsii_name="keepAliveTimeout")
    def keep_alive_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "keepAliveTimeout"))

    @keep_alive_timeout.setter
    def keep_alive_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df0be6c3e82e5b7fdb88116f86dbff039679761b60e5e46ef291fd46929febb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "keepAliveTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="noHappyEyeballs")
    def no_happy_eyeballs(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noHappyEyeballs"))

    @no_happy_eyeballs.setter
    def no_happy_eyeballs(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__79f76ac8b44e7cde731d7d02267f25d813de2a7d4f9859623e6c4a093efc67c6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noHappyEyeballs", value)

    @builtins.property
    @jsii.member(jsii_name="noTlsVerify")
    def no_tls_verify(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "noTlsVerify"))

    @no_tls_verify.setter
    def no_tls_verify(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__525966fb654548313bfddd2ecb7dbe08e1721b816a69ab5392f5da20387c38fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "noTlsVerify", value)

    @builtins.property
    @jsii.member(jsii_name="originServerName")
    def origin_server_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "originServerName"))

    @origin_server_name.setter
    def origin_server_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a374f851e35ae0a4bdb6174c266bc4fcc9b4c26989721f1fffbba0e0ef1b513)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "originServerName", value)

    @builtins.property
    @jsii.member(jsii_name="proxyAddress")
    def proxy_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyAddress"))

    @proxy_address.setter
    def proxy_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__254dfd19ffa9f40b64ec3d04d9d3659c701756f85b4d063d065c2288225ce611)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyAddress", value)

    @builtins.property
    @jsii.member(jsii_name="proxyPort")
    def proxy_port(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "proxyPort"))

    @proxy_port.setter
    def proxy_port(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__55159cf74d93c2d35f936be821fe841e502fa99c2569db5347558efe98da71bf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyPort", value)

    @builtins.property
    @jsii.member(jsii_name="proxyType")
    def proxy_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "proxyType"))

    @proxy_type.setter
    def proxy_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38e1a356104f346dfc5ee926e28832508323951ae6867998836c74847858b58a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "proxyType", value)

    @builtins.property
    @jsii.member(jsii_name="tcpKeepAlive")
    def tcp_keep_alive(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tcpKeepAlive"))

    @tcp_keep_alive.setter
    def tcp_keep_alive(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__612668130196db69c3ffc4e257bdee3a3e19871e6c004e865428ccd6ad24a743)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tcpKeepAlive", value)

    @builtins.property
    @jsii.member(jsii_name="tlsTimeout")
    def tls_timeout(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsTimeout"))

    @tls_timeout.setter
    def tls_timeout(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb252eb6bde1557c510106bd52af704f3054dfad604dfff9e931c7d6850611be)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsTimeout", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TunnelConfigConfigOriginRequest]:
        return typing.cast(typing.Optional[TunnelConfigConfigOriginRequest], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TunnelConfigConfigOriginRequest],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dfae1b7446bc382e4f8ac258308bebbf4505ec4d24c38a9eb033b211dd9f21b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.tunnelConfig.TunnelConfigConfigWarpRouting",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled"},
)
class TunnelConfigConfigWarpRouting:
    def __init__(
        self,
        *,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param enabled: Whether WARP routing is enabled. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#enabled TunnelConfig#enabled}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01395259fc84f472a80b3861da9bd9f865286e7051cf2d8180ad4e83ba0e635e)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Whether WARP routing is enabled.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/tunnel_config#enabled TunnelConfig#enabled}
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TunnelConfigConfigWarpRouting(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class TunnelConfigConfigWarpRoutingOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.tunnelConfig.TunnelConfigConfigWarpRoutingOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__5c878743fda1a75b34060e07ea4e434b9be32ad9e412ff47c97297d5f6f8d226)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="enabled")
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "enabled"))

    @enabled.setter
    def enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a9ddf2c206f380a4bfd1e0cfe9cba788b940e3687fbfac3faaa53873a0c3ba3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[TunnelConfigConfigWarpRouting]:
        return typing.cast(typing.Optional[TunnelConfigConfigWarpRouting], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[TunnelConfigConfigWarpRouting],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb71137343aa8a0d3b7f6a148a2cd3d94349ece0ee2e26a2e1c4615d6ea8e4a6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "TunnelConfig",
    "TunnelConfigConfig",
    "TunnelConfigConfigA",
    "TunnelConfigConfigAOutputReference",
    "TunnelConfigConfigIngressRule",
    "TunnelConfigConfigIngressRuleList",
    "TunnelConfigConfigIngressRuleOutputReference",
    "TunnelConfigConfigOriginRequest",
    "TunnelConfigConfigOriginRequestIpRules",
    "TunnelConfigConfigOriginRequestIpRulesList",
    "TunnelConfigConfigOriginRequestIpRulesOutputReference",
    "TunnelConfigConfigOriginRequestOutputReference",
    "TunnelConfigConfigWarpRouting",
    "TunnelConfigConfigWarpRoutingOutputReference",
]

publication.publish()

def _typecheckingstub__2873365409e9b0df1eb65ecca8b7d0e340aa776b9cdc673e4e91393741f048d7(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    config: typing.Union[TunnelConfigConfigA, typing.Dict[builtins.str, typing.Any]],
    tunnel_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__adb64d7a88764d46b57b3f8bd001f0647479596de59a89afc234368b39240c83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f2a7465e6d2d402ecc8d9e71bf1494c9dd8d79db479ca9a2abcbb6a816f9b760(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cf19b9c6b6ba52e5a0a9d677e429b7b49790e4cc54cffc6d0419798f666c45d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a11ad4e4a4b647bc24252bfaa47dee610de616c2f841dc9eae4739106074652b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    config: typing.Union[TunnelConfigConfigA, typing.Dict[builtins.str, typing.Any]],
    tunnel_id: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89cc5d0e9e1d5a1b6a864bc0e3744349186961ca4a2ded60c0fa08fcb54e1e59(
    *,
    ingress_rule: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TunnelConfigConfigIngressRule, typing.Dict[builtins.str, typing.Any]]]],
    origin_request: typing.Optional[typing.Union[TunnelConfigConfigOriginRequest, typing.Dict[builtins.str, typing.Any]]] = None,
    warp_routing: typing.Optional[typing.Union[TunnelConfigConfigWarpRouting, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a18286199845bfde0d2fb0f3bbde7f424d6d88d46430c7ae02485b8cab7874c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19c81e6e5ad52082f0a35703b5a6525f44eecb24cb0fcdd6911ae4d4b9d6b19(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TunnelConfigConfigIngressRule, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3b4e14650ef3046fef1a9800d21683a014baf2cd9e146c2618e3f7cd3bee57d5(
    value: typing.Optional[TunnelConfigConfigA],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f784430427980cd04622c33b458a1739196ae77ba23cd7ff09f73edf2c91daec(
    *,
    service: builtins.str,
    hostname: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f377c3fb53b1c0341f8815f6329d66d94a7865301059721ee21cf43010c3f1d(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e5396bfe0289e2d8da8f7cfe76da6a0680e5ee4271e526c4fe273ac5a4a4f49(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7210eb5bc056760ec57e2a67541da5773dd1ae357752df0d17fae0747060e51f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72bdf067dadc4373b039c8c0b152ea2fdb0bb94c675a85a252d6eb10976167fb(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05f636658f86ff607dbdf2bf673de030fa316ce87180f476da18a403e5ce99b8(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8d9d386b1ebcc606b18815a8153fdf7edd834ef8d7461e904bc73281b8cb73a(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TunnelConfigConfigIngressRule]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdbfd200b4436bc42193e0aa1e24bf92a29ee35e99c190937f159162b54612a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f52d850e07ba2514a13c6129dfa4a901c8dccaa191ca46fd824b5153bd70ad6f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f4579d4c27fdf7b5ae7ccebfd1fefd6890f8342f83958aee7d28c10d6529ede(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b74bbdd6192fcf35358a1b9c96f9550d5ba8ad4f443f3f5904bc4faaf0fedcf4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f3dfaffb8afa2e91a1b6efe8506d1564d707031637fcf078ce246107b331e33(
    value: typing.Optional[typing.Union[TunnelConfigConfigIngressRule, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75a6b4e932c816ecccf74e50b0998f8c8050bd0f3f66896930e9ebd86b451a0a(
    *,
    bastion_mode: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ca_pool: typing.Optional[builtins.str] = None,
    connect_timeout: typing.Optional[builtins.str] = None,
    disable_chunked_encoding: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    http_host_header: typing.Optional[builtins.str] = None,
    ip_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TunnelConfigConfigOriginRequestIpRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    keep_alive_connections: typing.Optional[jsii.Number] = None,
    keep_alive_timeout: typing.Optional[builtins.str] = None,
    no_happy_eyeballs: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    no_tls_verify: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    origin_server_name: typing.Optional[builtins.str] = None,
    proxy_address: typing.Optional[builtins.str] = None,
    proxy_port: typing.Optional[jsii.Number] = None,
    proxy_type: typing.Optional[builtins.str] = None,
    tcp_keep_alive: typing.Optional[builtins.str] = None,
    tls_timeout: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2303abf8905cd3b23743d0700d618409badb75a58225cfc2aa3c22283f84f309(
    *,
    allow: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14872396128c13233f32f7ab2a74dbf60a74bcfe51d721ec8eef2ae6a782a404(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__361f424421b66515f19834e31ef0b557d7c8d97af78cc8a248451389aa19daeb(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15ecd8d3046f6c70bec99e34eed7b249cb3ac4b4a0d0e7c66f31140705095ced(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb24f3658526eb73f9bf9b7364179198151edfe1497921cdd414c55394792a0a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05786c0d219923c85d0ba6414d850d400ca2613ad38e616d9f86dd115585a96d(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__342c0c94d0fb1a0ff9e84a882d670b337fba4fa022023f3a9973e4bf1046e66f(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[TunnelConfigConfigOriginRequestIpRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a9c96546c8cdbfdd349d807be72cbb9d6d996d928fd863f08af24548e43922a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c8bc0428e8f2377ec0131aa90f51b51291b5be6db469a7216d2c20b66b333311(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d56127894a6ba484b70f886e363134a86b699b7760f1dd201d341c6fd985ecf(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66e458be25a6430564455c68f75320f2c02085f1e6b1c15c3758a0ef4133d17c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c756736688b11202cdd6a631fe39f7b17996dec1ae7feb780c2de89cd40f164b(
    value: typing.Optional[typing.Union[TunnelConfigConfigOriginRequestIpRules, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d179b8176d7ecd6ba317c4ed505fddda2fcc1d4fa554c94ba3333bbc3ca7aed7(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0573b99701a51b4e9ce6d6805cbf0404fab324af81cb902e07814101213795b1(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[TunnelConfigConfigOriginRequestIpRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8f2feb44eb924b9aff00f5b9af79a6bf6377b5c40d95e587830a65ce3b77d9f(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36f9210912262ac939002fd7948da9a6087bd3ad7dee69a34aa9e75d68768636(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a19d2486d7d71151142c8e6e2bca4eedb4215393a547e5baa0f9ffee86006585(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9beb9a4ea10bad01158a720f74b002eeffab2af4e13cd4fe9ad79664b8c52327(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__607ba1756de072b7c394e4e98214fc2534ef392fd112c3baf63792bc4c5075c4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57f18017bfa3cf480fa5c11f431c8094e27eef7e9bb308fa9430bfdaf7b69d6a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df0be6c3e82e5b7fdb88116f86dbff039679761b60e5e46ef291fd46929febb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__79f76ac8b44e7cde731d7d02267f25d813de2a7d4f9859623e6c4a093efc67c6(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__525966fb654548313bfddd2ecb7dbe08e1721b816a69ab5392f5da20387c38fc(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a374f851e35ae0a4bdb6174c266bc4fcc9b4c26989721f1fffbba0e0ef1b513(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__254dfd19ffa9f40b64ec3d04d9d3659c701756f85b4d063d065c2288225ce611(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__55159cf74d93c2d35f936be821fe841e502fa99c2569db5347558efe98da71bf(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38e1a356104f346dfc5ee926e28832508323951ae6867998836c74847858b58a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__612668130196db69c3ffc4e257bdee3a3e19871e6c004e865428ccd6ad24a743(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb252eb6bde1557c510106bd52af704f3054dfad604dfff9e931c7d6850611be(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dfae1b7446bc382e4f8ac258308bebbf4505ec4d24c38a9eb033b211dd9f21b(
    value: typing.Optional[TunnelConfigConfigOriginRequest],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01395259fc84f472a80b3861da9bd9f865286e7051cf2d8180ad4e83ba0e635e(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c878743fda1a75b34060e07ea4e434b9be32ad9e412ff47c97297d5f6f8d226(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a9ddf2c206f380a4bfd1e0cfe9cba788b940e3687fbfac3faaa53873a0c3ba3(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb71137343aa8a0d3b7f6a148a2cd3d94349ece0ee2e26a2e1c4615d6ea8e4a6(
    value: typing.Optional[TunnelConfigConfigWarpRouting],
) -> None:
    """Type checking stubs"""
    pass
