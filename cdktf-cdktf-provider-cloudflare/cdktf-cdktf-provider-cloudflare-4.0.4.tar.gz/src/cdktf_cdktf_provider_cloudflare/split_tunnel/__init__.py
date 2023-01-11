'''
# `cloudflare_split_tunnel`

Refer to the Terraform Registory for docs: [`cloudflare_split_tunnel`](https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel).
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


class SplitTunnel(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.splitTunnel.SplitTunnel",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel cloudflare_split_tunnel}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        mode: builtins.str,
        tunnels: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SplitTunnelTunnels", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        policy_id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel cloudflare_split_tunnel} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#account_id SplitTunnel#account_id}
        :param mode: The mode of the split tunnel policy. Available values: ``include``, ``exclude``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#mode SplitTunnel#mode}
        :param tunnels: tunnels block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#tunnels SplitTunnel#tunnels}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#id SplitTunnel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param policy_id: The settings policy for which to configure this split tunnel policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#policy_id SplitTunnel#policy_id}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4466aaf33dea3aaf87cc75e2cbb9f1a1e95f0fa14b5e3e923f85355fec08baa5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = SplitTunnelConfig(
            account_id=account_id,
            mode=mode,
            tunnels=tunnels,
            id=id,
            policy_id=policy_id,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putTunnels")
    def put_tunnels(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SplitTunnelTunnels", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31fcb6a3f8567cd5e46c88299564dda68dfba154c2bfb5fa059528ce61b889e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putTunnels", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetPolicyId")
    def reset_policy_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPolicyId", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="tunnels")
    def tunnels(self) -> "SplitTunnelTunnelsList":
        return typing.cast("SplitTunnelTunnelsList", jsii.get(self, "tunnels"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="modeInput")
    def mode_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "modeInput"))

    @builtins.property
    @jsii.member(jsii_name="policyIdInput")
    def policy_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyIdInput"))

    @builtins.property
    @jsii.member(jsii_name="tunnelsInput")
    def tunnels_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SplitTunnelTunnels"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SplitTunnelTunnels"]]], jsii.get(self, "tunnelsInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d159e5936ba9df18098a31a7c68e9fbee2720ab343aa85267ff3e527efe40b0f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87129457b792e9e0d3778b5288a04cdd7e24d0e77077a9246827782d7620d5bc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="mode")
    def mode(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "mode"))

    @mode.setter
    def mode(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92cddb8d7514d28ef8f34e157cfae7f18fbe32b741b6e2789e30a60272060ccf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mode", value)

    @builtins.property
    @jsii.member(jsii_name="policyId")
    def policy_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "policyId"))

    @policy_id.setter
    def policy_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4de07367fcc3790a60e2055bd24fd0f2724403721d6a15370314b99d064b883d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.splitTunnel.SplitTunnelConfig",
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
        "mode": "mode",
        "tunnels": "tunnels",
        "id": "id",
        "policy_id": "policyId",
    },
)
class SplitTunnelConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        mode: builtins.str,
        tunnels: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["SplitTunnelTunnels", typing.Dict[builtins.str, typing.Any]]]],
        id: typing.Optional[builtins.str] = None,
        policy_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#account_id SplitTunnel#account_id}
        :param mode: The mode of the split tunnel policy. Available values: ``include``, ``exclude``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#mode SplitTunnel#mode}
        :param tunnels: tunnels block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#tunnels SplitTunnel#tunnels}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#id SplitTunnel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param policy_id: The settings policy for which to configure this split tunnel policy. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#policy_id SplitTunnel#policy_id}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c3fa2b828e1d1b5d2703efd7162d8ba899a8c8618dc27e1bc71e7552c1eb648)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument mode", value=mode, expected_type=type_hints["mode"])
            check_type(argname="argument tunnels", value=tunnels, expected_type=type_hints["tunnels"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument policy_id", value=policy_id, expected_type=type_hints["policy_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "mode": mode,
            "tunnels": tunnels,
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
        if policy_id is not None:
            self._values["policy_id"] = policy_id

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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#account_id SplitTunnel#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def mode(self) -> builtins.str:
        '''The mode of the split tunnel policy. Available values: ``include``, ``exclude``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#mode SplitTunnel#mode}
        '''
        result = self._values.get("mode")
        assert result is not None, "Required property 'mode' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tunnels(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SplitTunnelTunnels"]]:
        '''tunnels block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#tunnels SplitTunnel#tunnels}
        '''
        result = self._values.get("tunnels")
        assert result is not None, "Required property 'tunnels' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["SplitTunnelTunnels"]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#id SplitTunnel#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policy_id(self) -> typing.Optional[builtins.str]:
        '''The settings policy for which to configure this split tunnel policy.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#policy_id SplitTunnel#policy_id}
        '''
        result = self._values.get("policy_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SplitTunnelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.splitTunnel.SplitTunnelTunnels",
    jsii_struct_bases=[],
    name_mapping={"address": "address", "description": "description", "host": "host"},
)
class SplitTunnelTunnels:
    def __init__(
        self,
        *,
        address: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        host: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param address: The address for the tunnel. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#address SplitTunnel#address}
        :param description: A description for the tunnel. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#description SplitTunnel#description}
        :param host: The domain name for the tunnel. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#host SplitTunnel#host}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba4efcb7448ab0fd36cb58b4663834f9826358644ea6f35d20cb8f101a70135a)
            check_type(argname="argument address", value=address, expected_type=type_hints["address"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if address is not None:
            self._values["address"] = address
        if description is not None:
            self._values["description"] = description
        if host is not None:
            self._values["host"] = host

    @builtins.property
    def address(self) -> typing.Optional[builtins.str]:
        '''The address for the tunnel.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#address SplitTunnel#address}
        '''
        result = self._values.get("address")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description for the tunnel.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#description SplitTunnel#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def host(self) -> typing.Optional[builtins.str]:
        '''The domain name for the tunnel.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/split_tunnel#host SplitTunnel#host}
        '''
        result = self._values.get("host")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SplitTunnelTunnels(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SplitTunnelTunnelsList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.splitTunnel.SplitTunnelTunnelsList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__6dd23c6f93a9a010a5a5c01de26589a8cf602e845e07295f80ec5c47c5cc748e)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "SplitTunnelTunnelsOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8458b833915ed2d26b8bf3a4d3c5b695bdf384ebf8a6025eb382406140caeae)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("SplitTunnelTunnelsOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b1b2c6c7e702818743b4914b5bd42d703a5b380279f6cb9f99967b1c3a1c83ac)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9066579149ee9aa0c26a926257545b1b4483efd05aa4e3ed8d0c3aa5be33bf5a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fc0fa6f295d775d2b7f76883542183281def977d60960a08e8c301eb04fa6d6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SplitTunnelTunnels]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SplitTunnelTunnels]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SplitTunnelTunnels]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__758109ec609c0074f7dc7b6ea5a17e6a1b974ae3b15735f9bb22279828f61dbf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class SplitTunnelTunnelsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.splitTunnel.SplitTunnelTunnelsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__20e777368b415da736545daece1d1179bd09b004a41112f0f86fb1b7fcc4aaf5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetAddress")
    def reset_address(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAddress", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHost")
    def reset_host(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHost", []))

    @builtins.property
    @jsii.member(jsii_name="addressInput")
    def address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "addressInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="hostInput")
    def host_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "hostInput"))

    @builtins.property
    @jsii.member(jsii_name="address")
    def address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "address"))

    @address.setter
    def address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__032c4d54c88575b74e4be8c143bde602ccfa16d4fc8e6dfc40b84dbaeb1316b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "address", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92d82c195a22507be74de7a82d22373880d07190ea810d8911b23f1ef5952e71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="host")
    def host(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "host"))

    @host.setter
    def host(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1caf74d7a95db17df4b91ffdbcaed45d8e6da4c22f00fba832d2625f3cc6bc6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "host", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[SplitTunnelTunnels, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[SplitTunnelTunnels, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[SplitTunnelTunnels, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7565d42df6287417cddf981e6799f751feaf5d060feb24fd4f7c6c5c0ebd2da0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "SplitTunnel",
    "SplitTunnelConfig",
    "SplitTunnelTunnels",
    "SplitTunnelTunnelsList",
    "SplitTunnelTunnelsOutputReference",
]

publication.publish()

def _typecheckingstub__4466aaf33dea3aaf87cc75e2cbb9f1a1e95f0fa14b5e3e923f85355fec08baa5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    mode: builtins.str,
    tunnels: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SplitTunnelTunnels, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    policy_id: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__31fcb6a3f8567cd5e46c88299564dda68dfba154c2bfb5fa059528ce61b889e9(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SplitTunnelTunnels, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d159e5936ba9df18098a31a7c68e9fbee2720ab343aa85267ff3e527efe40b0f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87129457b792e9e0d3778b5288a04cdd7e24d0e77077a9246827782d7620d5bc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92cddb8d7514d28ef8f34e157cfae7f18fbe32b741b6e2789e30a60272060ccf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4de07367fcc3790a60e2055bd24fd0f2724403721d6a15370314b99d064b883d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c3fa2b828e1d1b5d2703efd7162d8ba899a8c8618dc27e1bc71e7552c1eb648(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    mode: builtins.str,
    tunnels: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[SplitTunnelTunnels, typing.Dict[builtins.str, typing.Any]]]],
    id: typing.Optional[builtins.str] = None,
    policy_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba4efcb7448ab0fd36cb58b4663834f9826358644ea6f35d20cb8f101a70135a(
    *,
    address: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    host: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dd23c6f93a9a010a5a5c01de26589a8cf602e845e07295f80ec5c47c5cc748e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8458b833915ed2d26b8bf3a4d3c5b695bdf384ebf8a6025eb382406140caeae(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1b2c6c7e702818743b4914b5bd42d703a5b380279f6cb9f99967b1c3a1c83ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9066579149ee9aa0c26a926257545b1b4483efd05aa4e3ed8d0c3aa5be33bf5a(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc0fa6f295d775d2b7f76883542183281def977d60960a08e8c301eb04fa6d6c(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__758109ec609c0074f7dc7b6ea5a17e6a1b974ae3b15735f9bb22279828f61dbf(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[SplitTunnelTunnels]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20e777368b415da736545daece1d1179bd09b004a41112f0f86fb1b7fcc4aaf5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__032c4d54c88575b74e4be8c143bde602ccfa16d4fc8e6dfc40b84dbaeb1316b5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92d82c195a22507be74de7a82d22373880d07190ea810d8911b23f1ef5952e71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1caf74d7a95db17df4b91ffdbcaed45d8e6da4c22f00fba832d2625f3cc6bc6b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7565d42df6287417cddf981e6799f751feaf5d060feb24fd4f7c6c5c0ebd2da0(
    value: typing.Optional[typing.Union[SplitTunnelTunnels, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
