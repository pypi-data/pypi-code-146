'''
# `azurerm_monitor_log_profile`

Refer to the Terraform Registory for docs: [`azurerm_monitor_log_profile`](https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile).
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


class MonitorLogProfile(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorLogProfile.MonitorLogProfile",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile azurerm_monitor_log_profile}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        categories: typing.Sequence[builtins.str],
        locations: typing.Sequence[builtins.str],
        name: builtins.str,
        retention_policy: typing.Union["MonitorLogProfileRetentionPolicy", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        servicebus_rule_id: typing.Optional[builtins.str] = None,
        storage_account_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["MonitorLogProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile azurerm_monitor_log_profile} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param categories: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#categories MonitorLogProfile#categories}.
        :param locations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#locations MonitorLogProfile#locations}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#name MonitorLogProfile#name}.
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#retention_policy MonitorLogProfile#retention_policy}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#id MonitorLogProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param servicebus_rule_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#servicebus_rule_id MonitorLogProfile#servicebus_rule_id}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#storage_account_id MonitorLogProfile#storage_account_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#timeouts MonitorLogProfile#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f02b971740187832c3f674f0c727ac64e1fead010e1393579cd5dfc837808bf0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitorLogProfileConfig(
            categories=categories,
            locations=locations,
            name=name,
            retention_policy=retention_policy,
            id=id,
            servicebus_rule_id=servicebus_rule_id,
            storage_account_id=storage_account_id,
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

    @jsii.member(jsii_name="putRetentionPolicy")
    def put_retention_policy(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#enabled MonitorLogProfile#enabled}.
        :param days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#days MonitorLogProfile#days}.
        '''
        value = MonitorLogProfileRetentionPolicy(enabled=enabled, days=days)

        return typing.cast(None, jsii.invoke(self, "putRetentionPolicy", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#create MonitorLogProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#delete MonitorLogProfile#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#read MonitorLogProfile#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#update MonitorLogProfile#update}.
        '''
        value = MonitorLogProfileTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetServicebusRuleId")
    def reset_servicebus_rule_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServicebusRuleId", []))

    @jsii.member(jsii_name="resetStorageAccountId")
    def reset_storage_account_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStorageAccountId", []))

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
    @jsii.member(jsii_name="retentionPolicy")
    def retention_policy(self) -> "MonitorLogProfileRetentionPolicyOutputReference":
        return typing.cast("MonitorLogProfileRetentionPolicyOutputReference", jsii.get(self, "retentionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MonitorLogProfileTimeoutsOutputReference":
        return typing.cast("MonitorLogProfileTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="categoriesInput")
    def categories_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "categoriesInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="locationsInput")
    def locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "locationsInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyInput")
    def retention_policy_input(
        self,
    ) -> typing.Optional["MonitorLogProfileRetentionPolicy"]:
        return typing.cast(typing.Optional["MonitorLogProfileRetentionPolicy"], jsii.get(self, "retentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="servicebusRuleIdInput")
    def servicebus_rule_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "servicebusRuleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountIdInput")
    def storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["MonitorLogProfileTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["MonitorLogProfileTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="categories")
    def categories(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "categories"))

    @categories.setter
    def categories(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__090c26b37865f9ca31ca8b3e7825f1323d73f9bbcc07e03825d8df1ddd569a8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "categories", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39635073893c43f3cafd066dd61f160baf28f487bb38205dd5e6fe28dc325a23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="locations")
    def locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "locations"))

    @locations.setter
    def locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5b64a84990262f9114876833f7150f0f59904dba25a85b436e7962800f1c335)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e89cc38df8268f2c7592b973a3a3c466598066821111d4b6edebcac94f5b72d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="servicebusRuleId")
    def servicebus_rule_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "servicebusRuleId"))

    @servicebus_rule_id.setter
    def servicebus_rule_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6498d9b333b0365531dcb828cb6b0a2c3f69f8dc5d6abff5b8c5b9e266da224)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "servicebusRuleId", value)

    @builtins.property
    @jsii.member(jsii_name="storageAccountId")
    def storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountId"))

    @storage_account_id.setter
    def storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c14c35e78c04bb02a6c7f0415252b1d78af7cc45ecdc1f71307042713f3d9ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorLogProfile.MonitorLogProfileConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "categories": "categories",
        "locations": "locations",
        "name": "name",
        "retention_policy": "retentionPolicy",
        "id": "id",
        "servicebus_rule_id": "servicebusRuleId",
        "storage_account_id": "storageAccountId",
        "timeouts": "timeouts",
    },
)
class MonitorLogProfileConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        categories: typing.Sequence[builtins.str],
        locations: typing.Sequence[builtins.str],
        name: builtins.str,
        retention_policy: typing.Union["MonitorLogProfileRetentionPolicy", typing.Dict[builtins.str, typing.Any]],
        id: typing.Optional[builtins.str] = None,
        servicebus_rule_id: typing.Optional[builtins.str] = None,
        storage_account_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["MonitorLogProfileTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param categories: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#categories MonitorLogProfile#categories}.
        :param locations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#locations MonitorLogProfile#locations}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#name MonitorLogProfile#name}.
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#retention_policy MonitorLogProfile#retention_policy}
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#id MonitorLogProfile#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param servicebus_rule_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#servicebus_rule_id MonitorLogProfile#servicebus_rule_id}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#storage_account_id MonitorLogProfile#storage_account_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#timeouts MonitorLogProfile#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(retention_policy, dict):
            retention_policy = MonitorLogProfileRetentionPolicy(**retention_policy)
        if isinstance(timeouts, dict):
            timeouts = MonitorLogProfileTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b0079ea9cc317390fa1c96989bae0114ff8a8e5b089c14b4fd3e2529b79ecc)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument categories", value=categories, expected_type=type_hints["categories"])
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument retention_policy", value=retention_policy, expected_type=type_hints["retention_policy"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument servicebus_rule_id", value=servicebus_rule_id, expected_type=type_hints["servicebus_rule_id"])
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "categories": categories,
            "locations": locations,
            "name": name,
            "retention_policy": retention_policy,
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
        if servicebus_rule_id is not None:
            self._values["servicebus_rule_id"] = servicebus_rule_id
        if storage_account_id is not None:
            self._values["storage_account_id"] = storage_account_id
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
    def categories(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#categories MonitorLogProfile#categories}.'''
        result = self._values.get("categories")
        assert result is not None, "Required property 'categories' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def locations(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#locations MonitorLogProfile#locations}.'''
        result = self._values.get("locations")
        assert result is not None, "Required property 'locations' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#name MonitorLogProfile#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_policy(self) -> "MonitorLogProfileRetentionPolicy":
        '''retention_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#retention_policy MonitorLogProfile#retention_policy}
        '''
        result = self._values.get("retention_policy")
        assert result is not None, "Required property 'retention_policy' is missing"
        return typing.cast("MonitorLogProfileRetentionPolicy", result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#id MonitorLogProfile#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def servicebus_rule_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#servicebus_rule_id MonitorLogProfile#servicebus_rule_id}.'''
        result = self._values.get("servicebus_rule_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#storage_account_id MonitorLogProfile#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MonitorLogProfileTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#timeouts MonitorLogProfile#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MonitorLogProfileTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorLogProfileConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorLogProfile.MonitorLogProfileRetentionPolicy",
    jsii_struct_bases=[],
    name_mapping={"enabled": "enabled", "days": "days"},
)
class MonitorLogProfileRetentionPolicy:
    def __init__(
        self,
        *,
        enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
        days: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#enabled MonitorLogProfile#enabled}.
        :param days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#days MonitorLogProfile#days}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99a48096d8e4bce92f1d35ec6b189395ac091391b4eb472e602fe6c4188d7a9d)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enabled": enabled,
        }
        if days is not None:
            self._values["days"] = days

    @builtins.property
    def enabled(self) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#enabled MonitorLogProfile#enabled}.'''
        result = self._values.get("enabled")
        assert result is not None, "Required property 'enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], result)

    @builtins.property
    def days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#days MonitorLogProfile#days}.'''
        result = self._values.get("days")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorLogProfileRetentionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorLogProfileRetentionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorLogProfile.MonitorLogProfileRetentionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__e299d8d1b7fda310f435a914576938e8b6448902698282cc841eeae17d9a47bd)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDays")
    def reset_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDays", []))

    @builtins.property
    @jsii.member(jsii_name="daysInput")
    def days_input(self) -> typing.Optional[jsii.Number]:
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "daysInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="days")
    def days(self) -> jsii.Number:
        return typing.cast(jsii.Number, jsii.get(self, "days"))

    @days.setter
    def days(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d658df2e9fad25d092abf639e29fb896cbec201be8d33147d8e28eadbd15cc6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "days", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__fe96675bbe5169b81c880f4ddbca2f61cba6f8f8538925465aa2eb4c1140383e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorLogProfileRetentionPolicy]:
        return typing.cast(typing.Optional[MonitorLogProfileRetentionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorLogProfileRetentionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ade057fee65ee56f0bc606682b1d170c80b2e6b792548f6f2631af2995cbbd51)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorLogProfile.MonitorLogProfileTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MonitorLogProfileTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#create MonitorLogProfile#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#delete MonitorLogProfile#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#read MonitorLogProfile#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#update MonitorLogProfile#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c25d9667a38ea13aae2666c8db76888ca485791d89e6c807a435a8ed69473c5a)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#create MonitorLogProfile#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#delete MonitorLogProfile#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#read MonitorLogProfile#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_log_profile#update MonitorLogProfile#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorLogProfileTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorLogProfileTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorLogProfile.MonitorLogProfileTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1c60a0afb2b894a5646e5e4f099f4b4c774fe3a82721f475f0ecc6b1ddea571e)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d5442543f04fe95dd58d5d33033fcae63ce1faf8bd49f89f11966160d8011e8b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b66f96dfc8bc99f039147e3b56ee1a72979c67190b3048bc63b94b44ee8641e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af9b4156fcd559dbd06ed915722de819e1d85643d46591ecfadd26d18f36caaa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d35149c9a038d3f8191b01332a7a70ef5a60010ee888daa3895c9d346741403a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitorLogProfileTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitorLogProfileTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitorLogProfileTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76f094120c5459db894105e5ff571a474938442159c91025cc7d4d134af457e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MonitorLogProfile",
    "MonitorLogProfileConfig",
    "MonitorLogProfileRetentionPolicy",
    "MonitorLogProfileRetentionPolicyOutputReference",
    "MonitorLogProfileTimeouts",
    "MonitorLogProfileTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f02b971740187832c3f674f0c727ac64e1fead010e1393579cd5dfc837808bf0(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    categories: typing.Sequence[builtins.str],
    locations: typing.Sequence[builtins.str],
    name: builtins.str,
    retention_policy: typing.Union[MonitorLogProfileRetentionPolicy, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    servicebus_rule_id: typing.Optional[builtins.str] = None,
    storage_account_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[MonitorLogProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__090c26b37865f9ca31ca8b3e7825f1323d73f9bbcc07e03825d8df1ddd569a8b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39635073893c43f3cafd066dd61f160baf28f487bb38205dd5e6fe28dc325a23(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b64a84990262f9114876833f7150f0f59904dba25a85b436e7962800f1c335(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e89cc38df8268f2c7592b973a3a3c466598066821111d4b6edebcac94f5b72d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6498d9b333b0365531dcb828cb6b0a2c3f69f8dc5d6abff5b8c5b9e266da224(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c14c35e78c04bb02a6c7f0415252b1d78af7cc45ecdc1f71307042713f3d9ca(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b0079ea9cc317390fa1c96989bae0114ff8a8e5b089c14b4fd3e2529b79ecc(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    categories: typing.Sequence[builtins.str],
    locations: typing.Sequence[builtins.str],
    name: builtins.str,
    retention_policy: typing.Union[MonitorLogProfileRetentionPolicy, typing.Dict[builtins.str, typing.Any]],
    id: typing.Optional[builtins.str] = None,
    servicebus_rule_id: typing.Optional[builtins.str] = None,
    storage_account_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[MonitorLogProfileTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99a48096d8e4bce92f1d35ec6b189395ac091391b4eb472e602fe6c4188d7a9d(
    *,
    enabled: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    days: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e299d8d1b7fda310f435a914576938e8b6448902698282cc841eeae17d9a47bd(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d658df2e9fad25d092abf639e29fb896cbec201be8d33147d8e28eadbd15cc6a(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe96675bbe5169b81c880f4ddbca2f61cba6f8f8538925465aa2eb4c1140383e(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ade057fee65ee56f0bc606682b1d170c80b2e6b792548f6f2631af2995cbbd51(
    value: typing.Optional[MonitorLogProfileRetentionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c25d9667a38ea13aae2666c8db76888ca485791d89e6c807a435a8ed69473c5a(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c60a0afb2b894a5646e5e4f099f4b4c774fe3a82721f475f0ecc6b1ddea571e(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5442543f04fe95dd58d5d33033fcae63ce1faf8bd49f89f11966160d8011e8b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b66f96dfc8bc99f039147e3b56ee1a72979c67190b3048bc63b94b44ee8641e7(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af9b4156fcd559dbd06ed915722de819e1d85643d46591ecfadd26d18f36caaa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d35149c9a038d3f8191b01332a7a70ef5a60010ee888daa3895c9d346741403a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76f094120c5459db894105e5ff571a474938442159c91025cc7d4d134af457e9(
    value: typing.Optional[typing.Union[MonitorLogProfileTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
