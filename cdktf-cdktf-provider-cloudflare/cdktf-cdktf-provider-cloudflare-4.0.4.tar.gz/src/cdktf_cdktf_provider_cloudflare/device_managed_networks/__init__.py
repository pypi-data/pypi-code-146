'''
# `cloudflare_device_managed_networks`

Refer to the Terraform Registory for docs: [`cloudflare_device_managed_networks`](https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks).
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


class DeviceManagedNetworks(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.deviceManagedNetworks.DeviceManagedNetworks",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks cloudflare_device_managed_networks}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        config: typing.Union["DeviceManagedNetworksConfigA", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        type: builtins.str,
        id: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks cloudflare_device_managed_networks} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#account_id DeviceManagedNetworks#account_id}
        :param config: config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#config DeviceManagedNetworks#config}
        :param name: The name of the Device Managed Network. Must be unique. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#name DeviceManagedNetworks#name}
        :param type: The type of Device Managed Network. Available values: ``tls``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#type DeviceManagedNetworks#type}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#id DeviceManagedNetworks#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0190c1eb89db7824ca630c7f120e2487b0a855a0204794f1ac09aa47e654c9d4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = DeviceManagedNetworksConfig(
            account_id=account_id,
            config=config,
            name=name,
            type=type,
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
    def put_config(self, *, sha256: builtins.str, tls_sockaddr: builtins.str) -> None:
        '''
        :param sha256: The SHA-256 hash of the TLS certificate presented by the host found at tls_sockaddr. If absent, regular certificate verification (trusted roots, valid timestamp, etc) will be used to validate the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#sha256 DeviceManagedNetworks#sha256}
        :param tls_sockaddr: A network address of the form "host:port" that the WARP client will use to detect the presence of a TLS host. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#tls_sockaddr DeviceManagedNetworks#tls_sockaddr}
        '''
        value = DeviceManagedNetworksConfigA(sha256=sha256, tls_sockaddr=tls_sockaddr)

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
    def config(self) -> "DeviceManagedNetworksConfigAOutputReference":
        return typing.cast("DeviceManagedNetworksConfigAOutputReference", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(self) -> typing.Optional["DeviceManagedNetworksConfigA"]:
        return typing.cast(typing.Optional["DeviceManagedNetworksConfigA"], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "accountId"))

    @account_id.setter
    def account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca1d04c60c0763616afce6a7611657ed62cfe7db2ab785e5fa6c7d3fb35eb879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0996d4bbfd533525bb67d56c02b4d97d903e3392fc2c5bb97888a80818fd6b8a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc063c73457861e6c02c3b76e216640c690c1ef8bab8d18fa2118b50fed70a71)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0fe88b123609901a8e578281d0b3106e7e494f42668366165402bab69741a3c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.deviceManagedNetworks.DeviceManagedNetworksConfig",
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
        "name": "name",
        "type": "type",
        "id": "id",
    },
)
class DeviceManagedNetworksConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        config: typing.Union["DeviceManagedNetworksConfigA", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        type: builtins.str,
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
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#account_id DeviceManagedNetworks#account_id}
        :param config: config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#config DeviceManagedNetworks#config}
        :param name: The name of the Device Managed Network. Must be unique. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#name DeviceManagedNetworks#name}
        :param type: The type of Device Managed Network. Available values: ``tls``. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#type DeviceManagedNetworks#type}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#id DeviceManagedNetworks#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(config, dict):
            config = DeviceManagedNetworksConfigA(**config)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e6b6e479f62e852510ca81bf85c59bb5f327d04180643ff0e1b5cce1466f0df)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
            "config": config,
            "name": name,
            "type": type,
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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#account_id DeviceManagedNetworks#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(self) -> "DeviceManagedNetworksConfigA":
        '''config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#config DeviceManagedNetworks#config}
        '''
        result = self._values.get("config")
        assert result is not None, "Required property 'config' is missing"
        return typing.cast("DeviceManagedNetworksConfigA", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''The name of the Device Managed Network. Must be unique.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#name DeviceManagedNetworks#name}
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of Device Managed Network. Available values: ``tls``.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#type DeviceManagedNetworks#type}
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#id DeviceManagedNetworks#id}.

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
        return "DeviceManagedNetworksConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.deviceManagedNetworks.DeviceManagedNetworksConfigA",
    jsii_struct_bases=[],
    name_mapping={"sha256": "sha256", "tls_sockaddr": "tlsSockaddr"},
)
class DeviceManagedNetworksConfigA:
    def __init__(self, *, sha256: builtins.str, tls_sockaddr: builtins.str) -> None:
        '''
        :param sha256: The SHA-256 hash of the TLS certificate presented by the host found at tls_sockaddr. If absent, regular certificate verification (trusted roots, valid timestamp, etc) will be used to validate the certificate. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#sha256 DeviceManagedNetworks#sha256}
        :param tls_sockaddr: A network address of the form "host:port" that the WARP client will use to detect the presence of a TLS host. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#tls_sockaddr DeviceManagedNetworks#tls_sockaddr}
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b23eb9ae324f12261eba645a263ba2e96c819167333f9d806286e024ec64c12e)
            check_type(argname="argument sha256", value=sha256, expected_type=type_hints["sha256"])
            check_type(argname="argument tls_sockaddr", value=tls_sockaddr, expected_type=type_hints["tls_sockaddr"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sha256": sha256,
            "tls_sockaddr": tls_sockaddr,
        }

    @builtins.property
    def sha256(self) -> builtins.str:
        '''The SHA-256 hash of the TLS certificate presented by the host found at tls_sockaddr.

        If absent, regular certificate verification (trusted roots, valid timestamp, etc) will be used to validate the certificate.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#sha256 DeviceManagedNetworks#sha256}
        '''
        result = self._values.get("sha256")
        assert result is not None, "Required property 'sha256' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def tls_sockaddr(self) -> builtins.str:
        '''A network address of the form "host:port" that the WARP client will use to detect the presence of a TLS host.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_managed_networks#tls_sockaddr DeviceManagedNetworks#tls_sockaddr}
        '''
        result = self._values.get("tls_sockaddr")
        assert result is not None, "Required property 'tls_sockaddr' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeviceManagedNetworksConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DeviceManagedNetworksConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.deviceManagedNetworks.DeviceManagedNetworksConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6c21cf56f544c09bdfe6cb9052f6047337cc70538127c31176f1ee91dae6ce5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="sha256Input")
    def sha256_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sha256Input"))

    @builtins.property
    @jsii.member(jsii_name="tlsSockaddrInput")
    def tls_sockaddr_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "tlsSockaddrInput"))

    @builtins.property
    @jsii.member(jsii_name="sha256")
    def sha256(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "sha256"))

    @sha256.setter
    def sha256(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a68cdfd83eb4db1797233bcf7f44b51c842d1faa87ec39fdb5c56ecdb39fc4b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sha256", value)

    @builtins.property
    @jsii.member(jsii_name="tlsSockaddr")
    def tls_sockaddr(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "tlsSockaddr"))

    @tls_sockaddr.setter
    def tls_sockaddr(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6572d96953ef96adc7b2ac7a566afa944d011db3e6d598cfb35fc2183b113f85)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tlsSockaddr", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[DeviceManagedNetworksConfigA]:
        return typing.cast(typing.Optional[DeviceManagedNetworksConfigA], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[DeviceManagedNetworksConfigA],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af35b4cefb34427034d0031785defb4d3ba0cc0ca799778dd94ad4f50ce955f6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DeviceManagedNetworks",
    "DeviceManagedNetworksConfig",
    "DeviceManagedNetworksConfigA",
    "DeviceManagedNetworksConfigAOutputReference",
]

publication.publish()

def _typecheckingstub__0190c1eb89db7824ca630c7f120e2487b0a855a0204794f1ac09aa47e654c9d4(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    config: typing.Union[DeviceManagedNetworksConfigA, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    type: builtins.str,
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

def _typecheckingstub__ca1d04c60c0763616afce6a7611657ed62cfe7db2ab785e5fa6c7d3fb35eb879(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0996d4bbfd533525bb67d56c02b4d97d903e3392fc2c5bb97888a80818fd6b8a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc063c73457861e6c02c3b76e216640c690c1ef8bab8d18fa2118b50fed70a71(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0fe88b123609901a8e578281d0b3106e7e494f42668366165402bab69741a3c0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e6b6e479f62e852510ca81bf85c59bb5f327d04180643ff0e1b5cce1466f0df(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    config: typing.Union[DeviceManagedNetworksConfigA, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    type: builtins.str,
    id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b23eb9ae324f12261eba645a263ba2e96c819167333f9d806286e024ec64c12e(
    *,
    sha256: builtins.str,
    tls_sockaddr: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6c21cf56f544c09bdfe6cb9052f6047337cc70538127c31176f1ee91dae6ce5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a68cdfd83eb4db1797233bcf7f44b51c842d1faa87ec39fdb5c56ecdb39fc4b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6572d96953ef96adc7b2ac7a566afa944d011db3e6d598cfb35fc2183b113f85(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af35b4cefb34427034d0031785defb4d3ba0cc0ca799778dd94ad4f50ce955f6(
    value: typing.Optional[DeviceManagedNetworksConfigA],
) -> None:
    """Type checking stubs"""
    pass
