'''
# `cloudflare_gre_tunnel`

Refer to the Terraform Registory for docs: [`cloudflare_gre_tunnel`](https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel).
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


class GreTunnel(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.greTunnel.GreTunnel",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel cloudflare_gre_tunnel}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        cloudflare_gre_endpoint: builtins.str,
        customer_gre_endpoint: builtins.str,
        interface_address: builtins.str,
        name: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        health_check_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        health_check_target: typing.Optional[builtins.str] = None,
        health_check_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        mtu: typing.Optional[jsii.Number] = None,
        ttl: typing.Optional[jsii.Number] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel cloudflare_gre_tunnel} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param cloudflare_gre_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#cloudflare_gre_endpoint GreTunnel#cloudflare_gre_endpoint}.
        :param customer_gre_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#customer_gre_endpoint GreTunnel#customer_gre_endpoint}.
        :param interface_address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#interface_address GreTunnel#interface_address}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#name GreTunnel#name}.
        :param account_id: The account identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#account_id GreTunnel#account_id}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#description GreTunnel#description}.
        :param health_check_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#health_check_enabled GreTunnel#health_check_enabled}.
        :param health_check_target: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#health_check_target GreTunnel#health_check_target}.
        :param health_check_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#health_check_type GreTunnel#health_check_type}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#id GreTunnel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mtu: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#mtu GreTunnel#mtu}.
        :param ttl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#ttl GreTunnel#ttl}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__efd4b924ab6bc422791cdfda4df2818704d267c5712619d16c20f9eff861b892)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = GreTunnelConfig(
            cloudflare_gre_endpoint=cloudflare_gre_endpoint,
            customer_gre_endpoint=customer_gre_endpoint,
            interface_address=interface_address,
            name=name,
            account_id=account_id,
            description=description,
            health_check_enabled=health_check_enabled,
            health_check_target=health_check_target,
            health_check_type=health_check_type,
            id=id,
            mtu=mtu,
            ttl=ttl,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="resetAccountId")
    def reset_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAccountId", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetHealthCheckEnabled")
    def reset_health_check_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckEnabled", []))

    @jsii.member(jsii_name="resetHealthCheckTarget")
    def reset_health_check_target(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckTarget", []))

    @jsii.member(jsii_name="resetHealthCheckType")
    def reset_health_check_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetHealthCheckType", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetMtu")
    def reset_mtu(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMtu", []))

    @jsii.member(jsii_name="resetTtl")
    def reset_ttl(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTtl", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="cloudflareGreEndpointInput")
    def cloudflare_gre_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "cloudflareGreEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="customerGreEndpointInput")
    def customer_gre_endpoint_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerGreEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckEnabledInput")
    def health_check_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "healthCheckEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckTargetInput")
    def health_check_target_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckTargetInput"))

    @builtins.property
    @jsii.member(jsii_name="healthCheckTypeInput")
    def health_check_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "healthCheckTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="interfaceAddressInput")
    def interface_address_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "interfaceAddressInput"))

    @builtins.property
    @jsii.member(jsii_name="mtuInput")
    def mtu_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "mtuInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="ttlInput")
    def ttl_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "ttlInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50a28a48473304743b00128c526c38c96ac58281e721e2ea215aa89eef81cbae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="cloudflareGreEndpoint")
    def cloudflare_gre_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "cloudflareGreEndpoint"))

    @cloudflare_gre_endpoint.setter
    def cloudflare_gre_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5997f34db9bcac8714fec2ea28e0dc3130e1e5568ea28824356983199dfe7f2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "cloudflareGreEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="customerGreEndpoint")
    def customer_gre_endpoint(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerGreEndpoint"))

    @customer_gre_endpoint.setter
    def customer_gre_endpoint(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a55c9d0bfb6aa56dcc1ef3735a5c39b30f5f46d208d148486e9d4e243d2e554f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerGreEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adfc3058c323966db34819c46f5f8ccf7926407198e87a81926359f6eea65fe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckEnabled")
    def health_check_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "healthCheckEnabled"))

    @health_check_enabled.setter
    def health_check_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__304692b41b7c1c3bea92e66cb6024c731f64617f3b865c5b6cb638058bfaec6c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckTarget")
    def health_check_target(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckTarget"))

    @health_check_target.setter
    def health_check_target(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd9eadf1a2bdcd908952f5e4eba90f66e77ea48f5386b9f3cd07bbd31d1bb7b9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckTarget", value)

    @builtins.property
    @jsii.member(jsii_name="healthCheckType")
    def health_check_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "healthCheckType"))

    @health_check_type.setter
    def health_check_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__460edd34e8f7d99d64f6c43471c9a60d6db31bbd17e6ab0da932d4999b450e56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "healthCheckType", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d404d9b13eca87500dc34b911374d1e815801da7ef2e68cb1cd3cb2fae9a7861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="interfaceAddress")
    def interface_address(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interfaceAddress"))

    @interface_address.setter
    def interface_address(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7aefad654e0204f1c91ccd0088a0ef549465e10bc13dcb1e1ebcbca987e183a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interfaceAddress", value)

    @builtins.property
    @jsii.member(jsii_name="mtu")
    def mtu(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "mtu"))

    @mtu.setter
    def mtu(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfbf9470d4ab5a8c74f8fabe27351a24a0c190dc133a3d41b13d7c51f5cc5976)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "mtu", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7c6c60c1547ea5f9f754853892778fa28b425ef0ea9782cb523dfe9c38d678e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="ttl")
    def ttl(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "ttl"))

    @ttl.setter
    def ttl(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6615a8c976a1706bcad938ef94977a21987e1b82df9ba578b20709945a5dbc22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ttl", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.greTunnel.GreTunnelConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "cloudflare_gre_endpoint": "cloudflareGreEndpoint",
        "customer_gre_endpoint": "customerGreEndpoint",
        "interface_address": "interfaceAddress",
        "name": "name",
        "account_id": "accountId",
        "description": "description",
        "health_check_enabled": "healthCheckEnabled",
        "health_check_target": "healthCheckTarget",
        "health_check_type": "healthCheckType",
        "id": "id",
        "mtu": "mtu",
        "ttl": "ttl",
    },
)
class GreTunnelConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        cloudflare_gre_endpoint: builtins.str,
        customer_gre_endpoint: builtins.str,
        interface_address: builtins.str,
        name: builtins.str,
        account_id: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        health_check_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        health_check_target: typing.Optional[builtins.str] = None,
        health_check_type: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        mtu: typing.Optional[jsii.Number] = None,
        ttl: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param cloudflare_gre_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#cloudflare_gre_endpoint GreTunnel#cloudflare_gre_endpoint}.
        :param customer_gre_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#customer_gre_endpoint GreTunnel#customer_gre_endpoint}.
        :param interface_address: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#interface_address GreTunnel#interface_address}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#name GreTunnel#name}.
        :param account_id: The account identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#account_id GreTunnel#account_id}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#description GreTunnel#description}.
        :param health_check_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#health_check_enabled GreTunnel#health_check_enabled}.
        :param health_check_target: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#health_check_target GreTunnel#health_check_target}.
        :param health_check_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#health_check_type GreTunnel#health_check_type}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#id GreTunnel#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param mtu: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#mtu GreTunnel#mtu}.
        :param ttl: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#ttl GreTunnel#ttl}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c352fece82cc57ed3a5bc7ddff95f30d9880f3cf566e1482e32b4137dc82823f)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument cloudflare_gre_endpoint", value=cloudflare_gre_endpoint, expected_type=type_hints["cloudflare_gre_endpoint"])
            check_type(argname="argument customer_gre_endpoint", value=customer_gre_endpoint, expected_type=type_hints["customer_gre_endpoint"])
            check_type(argname="argument interface_address", value=interface_address, expected_type=type_hints["interface_address"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument health_check_enabled", value=health_check_enabled, expected_type=type_hints["health_check_enabled"])
            check_type(argname="argument health_check_target", value=health_check_target, expected_type=type_hints["health_check_target"])
            check_type(argname="argument health_check_type", value=health_check_type, expected_type=type_hints["health_check_type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument mtu", value=mtu, expected_type=type_hints["mtu"])
            check_type(argname="argument ttl", value=ttl, expected_type=type_hints["ttl"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloudflare_gre_endpoint": cloudflare_gre_endpoint,
            "customer_gre_endpoint": customer_gre_endpoint,
            "interface_address": interface_address,
            "name": name,
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
        if account_id is not None:
            self._values["account_id"] = account_id
        if description is not None:
            self._values["description"] = description
        if health_check_enabled is not None:
            self._values["health_check_enabled"] = health_check_enabled
        if health_check_target is not None:
            self._values["health_check_target"] = health_check_target
        if health_check_type is not None:
            self._values["health_check_type"] = health_check_type
        if id is not None:
            self._values["id"] = id
        if mtu is not None:
            self._values["mtu"] = mtu
        if ttl is not None:
            self._values["ttl"] = ttl

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
    def cloudflare_gre_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#cloudflare_gre_endpoint GreTunnel#cloudflare_gre_endpoint}.'''
        result = self._values.get("cloudflare_gre_endpoint")
        assert result is not None, "Required property 'cloudflare_gre_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def customer_gre_endpoint(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#customer_gre_endpoint GreTunnel#customer_gre_endpoint}.'''
        result = self._values.get("customer_gre_endpoint")
        assert result is not None, "Required property 'customer_gre_endpoint' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def interface_address(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#interface_address GreTunnel#interface_address}.'''
        result = self._values.get("interface_address")
        assert result is not None, "Required property 'interface_address' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#name GreTunnel#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account_id(self) -> typing.Optional[builtins.str]:
        '''The account identifier to target for the resource. **Modifying this attribute will force creation of a new resource.**.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#account_id GreTunnel#account_id}
        '''
        result = self._values.get("account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#description GreTunnel#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#health_check_enabled GreTunnel#health_check_enabled}.'''
        result = self._values.get("health_check_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def health_check_target(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#health_check_target GreTunnel#health_check_target}.'''
        result = self._values.get("health_check_target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def health_check_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#health_check_type GreTunnel#health_check_type}.'''
        result = self._values.get("health_check_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#id GreTunnel#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def mtu(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#mtu GreTunnel#mtu}.'''
        result = self._values.get("mtu")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def ttl(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/gre_tunnel#ttl GreTunnel#ttl}.'''
        result = self._values.get("ttl")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GreTunnelConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "GreTunnel",
    "GreTunnelConfig",
]

publication.publish()

def _typecheckingstub__efd4b924ab6bc422791cdfda4df2818704d267c5712619d16c20f9eff861b892(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    cloudflare_gre_endpoint: builtins.str,
    customer_gre_endpoint: builtins.str,
    interface_address: builtins.str,
    name: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    health_check_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    health_check_target: typing.Optional[builtins.str] = None,
    health_check_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    mtu: typing.Optional[jsii.Number] = None,
    ttl: typing.Optional[jsii.Number] = None,
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

def _typecheckingstub__50a28a48473304743b00128c526c38c96ac58281e721e2ea215aa89eef81cbae(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5997f34db9bcac8714fec2ea28e0dc3130e1e5568ea28824356983199dfe7f2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a55c9d0bfb6aa56dcc1ef3735a5c39b30f5f46d208d148486e9d4e243d2e554f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adfc3058c323966db34819c46f5f8ccf7926407198e87a81926359f6eea65fe7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__304692b41b7c1c3bea92e66cb6024c731f64617f3b865c5b6cb638058bfaec6c(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd9eadf1a2bdcd908952f5e4eba90f66e77ea48f5386b9f3cd07bbd31d1bb7b9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__460edd34e8f7d99d64f6c43471c9a60d6db31bbd17e6ab0da932d4999b450e56(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d404d9b13eca87500dc34b911374d1e815801da7ef2e68cb1cd3cb2fae9a7861(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7aefad654e0204f1c91ccd0088a0ef549465e10bc13dcb1e1ebcbca987e183a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfbf9470d4ab5a8c74f8fabe27351a24a0c190dc133a3d41b13d7c51f5cc5976(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7c6c60c1547ea5f9f754853892778fa28b425ef0ea9782cb523dfe9c38d678e5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6615a8c976a1706bcad938ef94977a21987e1b82df9ba578b20709945a5dbc22(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c352fece82cc57ed3a5bc7ddff95f30d9880f3cf566e1482e32b4137dc82823f(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    cloudflare_gre_endpoint: builtins.str,
    customer_gre_endpoint: builtins.str,
    interface_address: builtins.str,
    name: builtins.str,
    account_id: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    health_check_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    health_check_target: typing.Optional[builtins.str] = None,
    health_check_type: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    mtu: typing.Optional[jsii.Number] = None,
    ttl: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass
