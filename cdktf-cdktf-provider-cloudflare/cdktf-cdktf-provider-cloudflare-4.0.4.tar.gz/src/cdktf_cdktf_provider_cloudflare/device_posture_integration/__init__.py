'''
# `cloudflare_device_posture_integration`

Refer to the Terraform Registory for docs: [`cloudflare_device_posture_integration`](https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration).
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


class DevicePostureIntegration(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.devicePostureIntegration.DevicePostureIntegration",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration cloudflare_device_posture_integration}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        account_id: builtins.str,
        name: builtins.str,
        type: builtins.str,
        config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DevicePostureIntegrationConfigA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        identifier: typing.Optional[builtins.str] = None,
        interval: typing.Optional[builtins.str] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration cloudflare_device_posture_integration} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#account_id DevicePostureIntegration#account_id}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#name DevicePostureIntegration#name}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#type DevicePostureIntegration#type}.
        :param config: config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#config DevicePostureIntegration#config}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#id DevicePostureIntegration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#identifier DevicePostureIntegration#identifier}.
        :param interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#interval DevicePostureIntegration#interval}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7aba768dd21a851e51193a48d7baf6c8ae1359b405b003f910a602bcb5c37be3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config_ = DevicePostureIntegrationConfig(
            account_id=account_id,
            name=name,
            type=type,
            config=config,
            id=id,
            identifier=identifier,
            interval=interval,
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
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DevicePostureIntegrationConfigA", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5114cfe686d5bd0d029cec55aa53c70901dfe28691da4ec3b42478c6f16b761c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putConfig", [value]))

    @jsii.member(jsii_name="resetConfig")
    def reset_config(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetConfig", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIdentifier")
    def reset_identifier(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIdentifier", []))

    @jsii.member(jsii_name="resetInterval")
    def reset_interval(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetInterval", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(self) -> "DevicePostureIntegrationConfigAList":
        return typing.cast("DevicePostureIntegrationConfigAList", jsii.get(self, "config"))

    @builtins.property
    @jsii.member(jsii_name="accountIdInput")
    def account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="configInput")
    def config_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureIntegrationConfigA"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureIntegrationConfigA"]]], jsii.get(self, "configInput"))

    @builtins.property
    @jsii.member(jsii_name="identifierInput")
    def identifier_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "identifierInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="intervalInput")
    def interval_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "intervalInput"))

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
            type_hints = typing.get_type_hints(_typecheckingstub__c0d1241a21aed25d5a63b5a5eb18981582f1d2697235b893c503c79379a38351)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accountId", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89aee580eb7399cadf45a147086c1ddc87de073be18873e1226ed0ea20962511)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="identifier")
    def identifier(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "identifier"))

    @identifier.setter
    def identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6ae5897fb19e006fc6557294e2f71cd7bb08e47b02ed791fbdd83defde62250)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "identifier", value)

    @builtins.property
    @jsii.member(jsii_name="interval")
    def interval(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "interval"))

    @interval.setter
    def interval(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ba2704edd21b14d8bb16d2c07cd62303bf32af4de4bbb73a0beb5483af1ef9f1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "interval", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__579565124be1adee53ae8e727d52891b26bada089c37318ebe44ca51d7143051)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eab841c10949cf633d0acdb4ed0da031e67ef84e104884685bc2a7080fff9ffb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.devicePostureIntegration.DevicePostureIntegrationConfig",
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
        "name": "name",
        "type": "type",
        "config": "config",
        "id": "id",
        "identifier": "identifier",
        "interval": "interval",
    },
)
class DevicePostureIntegrationConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        type: builtins.str,
        config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["DevicePostureIntegrationConfigA", typing.Dict[builtins.str, typing.Any]]]]] = None,
        id: typing.Optional[builtins.str] = None,
        identifier: typing.Optional[builtins.str] = None,
        interval: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param account_id: The account identifier to target for the resource. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#account_id DevicePostureIntegration#account_id}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#name DevicePostureIntegration#name}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#type DevicePostureIntegration#type}.
        :param config: config block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#config DevicePostureIntegration#config}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#id DevicePostureIntegration#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param identifier: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#identifier DevicePostureIntegration#identifier}.
        :param interval: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#interval DevicePostureIntegration#interval}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__640651d09ae3d12d644978d3f8ac665d591fd2dd034ece370f45a79040e2793b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument identifier", value=identifier, expected_type=type_hints["identifier"])
            check_type(argname="argument interval", value=interval, expected_type=type_hints["interval"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account_id": account_id,
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
        if config is not None:
            self._values["config"] = config
        if id is not None:
            self._values["id"] = id
        if identifier is not None:
            self._values["identifier"] = identifier
        if interval is not None:
            self._values["interval"] = interval

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

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#account_id DevicePostureIntegration#account_id}
        '''
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#name DevicePostureIntegration#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#type DevicePostureIntegration#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureIntegrationConfigA"]]]:
        '''config block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#config DevicePostureIntegration#config}
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["DevicePostureIntegrationConfigA"]]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#id DevicePostureIntegration#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def identifier(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#identifier DevicePostureIntegration#identifier}.'''
        result = self._values.get("identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def interval(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#interval DevicePostureIntegration#interval}.'''
        result = self._values.get("interval")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevicePostureIntegrationConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-cloudflare.devicePostureIntegration.DevicePostureIntegrationConfigA",
    jsii_struct_bases=[],
    name_mapping={
        "api_url": "apiUrl",
        "auth_url": "authUrl",
        "client_id": "clientId",
        "client_key": "clientKey",
        "client_secret": "clientSecret",
        "customer_id": "customerId",
    },
)
class DevicePostureIntegrationConfigA:
    def __init__(
        self,
        *,
        api_url: typing.Optional[builtins.str] = None,
        auth_url: typing.Optional[builtins.str] = None,
        client_id: typing.Optional[builtins.str] = None,
        client_key: typing.Optional[builtins.str] = None,
        client_secret: typing.Optional[builtins.str] = None,
        customer_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param api_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#api_url DevicePostureIntegration#api_url}.
        :param auth_url: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#auth_url DevicePostureIntegration#auth_url}.
        :param client_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#client_id DevicePostureIntegration#client_id}.
        :param client_key: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#client_key DevicePostureIntegration#client_key}.
        :param client_secret: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#client_secret DevicePostureIntegration#client_secret}.
        :param customer_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#customer_id DevicePostureIntegration#customer_id}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e091a76bdcf5908119c693f5a7c3e96fc9a71b8ed338d4ff497fbe487964e21)
            check_type(argname="argument api_url", value=api_url, expected_type=type_hints["api_url"])
            check_type(argname="argument auth_url", value=auth_url, expected_type=type_hints["auth_url"])
            check_type(argname="argument client_id", value=client_id, expected_type=type_hints["client_id"])
            check_type(argname="argument client_key", value=client_key, expected_type=type_hints["client_key"])
            check_type(argname="argument client_secret", value=client_secret, expected_type=type_hints["client_secret"])
            check_type(argname="argument customer_id", value=customer_id, expected_type=type_hints["customer_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if api_url is not None:
            self._values["api_url"] = api_url
        if auth_url is not None:
            self._values["auth_url"] = auth_url
        if client_id is not None:
            self._values["client_id"] = client_id
        if client_key is not None:
            self._values["client_key"] = client_key
        if client_secret is not None:
            self._values["client_secret"] = client_secret
        if customer_id is not None:
            self._values["customer_id"] = customer_id

    @builtins.property
    def api_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#api_url DevicePostureIntegration#api_url}.'''
        result = self._values.get("api_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auth_url(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#auth_url DevicePostureIntegration#auth_url}.'''
        result = self._values.get("auth_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#client_id DevicePostureIntegration#client_id}.'''
        result = self._values.get("client_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_key(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#client_key DevicePostureIntegration#client_key}.'''
        result = self._values.get("client_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def client_secret(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#client_secret DevicePostureIntegration#client_secret}.'''
        result = self._values.get("client_secret")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def customer_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/cloudflare/r/device_posture_integration#customer_id DevicePostureIntegration#customer_id}.'''
        result = self._values.get("customer_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DevicePostureIntegrationConfigA(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DevicePostureIntegrationConfigAList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.devicePostureIntegration.DevicePostureIntegrationConfigAList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9d8814a1cfffff4e7953a02d914b0ad3cdccd77e9b78d108d2d2352f1d75e457)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "DevicePostureIntegrationConfigAOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26c2c1c681c9d714ae23c7cb245e91d91cf4e8fa734d1c8bc01c6aacd65182a0)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("DevicePostureIntegrationConfigAOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1b313362b98f0aca2f627d6349c1f2d3aeda93b35de44c25ada64fe5ef11d9e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__19cce64d83f60f52db6708779388c6c7c8adaa3a0fb804c49f0b277f1334b07b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__fd0e11a76807a0cb9381dc59455a70e37fd545623d8075c2de152c15ad6a0897)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureIntegrationConfigA]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureIntegrationConfigA]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureIntegrationConfigA]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b7bfa5c0ced9185a4c0e5caa7dbd81443f2dd1422c39374f7aac02f82dfbaacc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class DevicePostureIntegrationConfigAOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-cloudflare.devicePostureIntegration.DevicePostureIntegrationConfigAOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9319b9afd2ebb0a2707fe60b8023542cc3aa07342d7fef73fd8c60938c62734b)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetApiUrl")
    def reset_api_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetApiUrl", []))

    @jsii.member(jsii_name="resetAuthUrl")
    def reset_auth_url(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAuthUrl", []))

    @jsii.member(jsii_name="resetClientId")
    def reset_client_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientId", []))

    @jsii.member(jsii_name="resetClientKey")
    def reset_client_key(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientKey", []))

    @jsii.member(jsii_name="resetClientSecret")
    def reset_client_secret(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetClientSecret", []))

    @jsii.member(jsii_name="resetCustomerId")
    def reset_customer_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCustomerId", []))

    @builtins.property
    @jsii.member(jsii_name="apiUrlInput")
    def api_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "apiUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="authUrlInput")
    def auth_url_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authUrlInput"))

    @builtins.property
    @jsii.member(jsii_name="clientIdInput")
    def client_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientIdInput"))

    @builtins.property
    @jsii.member(jsii_name="clientKeyInput")
    def client_key_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientKeyInput"))

    @builtins.property
    @jsii.member(jsii_name="clientSecretInput")
    def client_secret_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "clientSecretInput"))

    @builtins.property
    @jsii.member(jsii_name="customerIdInput")
    def customer_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customerIdInput"))

    @builtins.property
    @jsii.member(jsii_name="apiUrl")
    def api_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "apiUrl"))

    @api_url.setter
    def api_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__731238196ce3ae3622461624a8534ac4a0b51fe209d714ee4e65c6516ed8b27c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "apiUrl", value)

    @builtins.property
    @jsii.member(jsii_name="authUrl")
    def auth_url(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "authUrl"))

    @auth_url.setter
    def auth_url(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739a16b84197bb853702b2cefebc3d5d7e2fb4cd0f015237c9f0d9c1c0b9ea15)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authUrl", value)

    @builtins.property
    @jsii.member(jsii_name="clientId")
    def client_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientId"))

    @client_id.setter
    def client_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__31f604c6602b42afb2f38843e0fdcf23610c87156a7c7b22cbcaad2664f6478f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientId", value)

    @builtins.property
    @jsii.member(jsii_name="clientKey")
    def client_key(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientKey"))

    @client_key.setter
    def client_key(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a86d5cfff55dfe5a35715ed06f8aefd0b7a9a626275ee6c86642710beabf5da1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientKey", value)

    @builtins.property
    @jsii.member(jsii_name="clientSecret")
    def client_secret(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "clientSecret"))

    @client_secret.setter
    def client_secret(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8080269d55ea91b98168d14b909fb07e02238efec7045db76ef23ff3310dcbe1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientSecret", value)

    @builtins.property
    @jsii.member(jsii_name="customerId")
    def customer_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "customerId"))

    @customer_id.setter
    def customer_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cf28e58d736a0b343bb3f1c87496fa28bc4dd8be8573ba341a17e1e7738560d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customerId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[DevicePostureIntegrationConfigA, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[DevicePostureIntegrationConfigA, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[DevicePostureIntegrationConfigA, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef8d5dca6398aa83ecb957f7d6805c21a8004580b84472a3c07285128f888d6e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "DevicePostureIntegration",
    "DevicePostureIntegrationConfig",
    "DevicePostureIntegrationConfigA",
    "DevicePostureIntegrationConfigAList",
    "DevicePostureIntegrationConfigAOutputReference",
]

publication.publish()

def _typecheckingstub__7aba768dd21a851e51193a48d7baf6c8ae1359b405b003f910a602bcb5c37be3(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    account_id: builtins.str,
    name: builtins.str,
    type: builtins.str,
    config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureIntegrationConfigA, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    identifier: typing.Optional[builtins.str] = None,
    interval: typing.Optional[builtins.str] = None,
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

def _typecheckingstub__5114cfe686d5bd0d029cec55aa53c70901dfe28691da4ec3b42478c6f16b761c(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureIntegrationConfigA, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0d1241a21aed25d5a63b5a5eb18981582f1d2697235b893c503c79379a38351(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89aee580eb7399cadf45a147086c1ddc87de073be18873e1226ed0ea20962511(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6ae5897fb19e006fc6557294e2f71cd7bb08e47b02ed791fbdd83defde62250(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ba2704edd21b14d8bb16d2c07cd62303bf32af4de4bbb73a0beb5483af1ef9f1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__579565124be1adee53ae8e727d52891b26bada089c37318ebe44ca51d7143051(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eab841c10949cf633d0acdb4ed0da031e67ef84e104884685bc2a7080fff9ffb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__640651d09ae3d12d644978d3f8ac665d591fd2dd034ece370f45a79040e2793b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    account_id: builtins.str,
    name: builtins.str,
    type: builtins.str,
    config: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[DevicePostureIntegrationConfigA, typing.Dict[builtins.str, typing.Any]]]]] = None,
    id: typing.Optional[builtins.str] = None,
    identifier: typing.Optional[builtins.str] = None,
    interval: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e091a76bdcf5908119c693f5a7c3e96fc9a71b8ed338d4ff497fbe487964e21(
    *,
    api_url: typing.Optional[builtins.str] = None,
    auth_url: typing.Optional[builtins.str] = None,
    client_id: typing.Optional[builtins.str] = None,
    client_key: typing.Optional[builtins.str] = None,
    client_secret: typing.Optional[builtins.str] = None,
    customer_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d8814a1cfffff4e7953a02d914b0ad3cdccd77e9b78d108d2d2352f1d75e457(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26c2c1c681c9d714ae23c7cb245e91d91cf4e8fa734d1c8bc01c6aacd65182a0(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1b313362b98f0aca2f627d6349c1f2d3aeda93b35de44c25ada64fe5ef11d9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__19cce64d83f60f52db6708779388c6c7c8adaa3a0fb804c49f0b277f1334b07b(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd0e11a76807a0cb9381dc59455a70e37fd545623d8075c2de152c15ad6a0897(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b7bfa5c0ced9185a4c0e5caa7dbd81443f2dd1422c39374f7aac02f82dfbaacc(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[DevicePostureIntegrationConfigA]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9319b9afd2ebb0a2707fe60b8023542cc3aa07342d7fef73fd8c60938c62734b(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__731238196ce3ae3622461624a8534ac4a0b51fe209d714ee4e65c6516ed8b27c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739a16b84197bb853702b2cefebc3d5d7e2fb4cd0f015237c9f0d9c1c0b9ea15(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__31f604c6602b42afb2f38843e0fdcf23610c87156a7c7b22cbcaad2664f6478f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a86d5cfff55dfe5a35715ed06f8aefd0b7a9a626275ee6c86642710beabf5da1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8080269d55ea91b98168d14b909fb07e02238efec7045db76ef23ff3310dcbe1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cf28e58d736a0b343bb3f1c87496fa28bc4dd8be8573ba341a17e1e7738560d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef8d5dca6398aa83ecb957f7d6805c21a8004580b84472a3c07285128f888d6e(
    value: typing.Optional[typing.Union[DevicePostureIntegrationConfigA, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
