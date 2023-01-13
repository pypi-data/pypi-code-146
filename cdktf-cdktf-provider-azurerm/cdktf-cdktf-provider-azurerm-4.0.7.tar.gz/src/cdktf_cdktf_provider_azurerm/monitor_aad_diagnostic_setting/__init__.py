'''
# `azurerm_monitor_aad_diagnostic_setting`

Refer to the Terraform Registory for docs: [`azurerm_monitor_aad_diagnostic_setting`](https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting).
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


class MonitorAadDiagnosticSetting(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAadDiagnosticSetting.MonitorAadDiagnosticSetting",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting azurerm_monitor_aad_diagnostic_setting}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        log: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAadDiagnosticSettingLog", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        eventhub_authorization_rule_id: typing.Optional[builtins.str] = None,
        eventhub_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        log_analytics_workspace_id: typing.Optional[builtins.str] = None,
        storage_account_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["MonitorAadDiagnosticSettingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting azurerm_monitor_aad_diagnostic_setting} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param log: log block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#log MonitorAadDiagnosticSetting#log}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#name MonitorAadDiagnosticSetting#name}.
        :param eventhub_authorization_rule_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#eventhub_authorization_rule_id MonitorAadDiagnosticSetting#eventhub_authorization_rule_id}.
        :param eventhub_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#eventhub_name MonitorAadDiagnosticSetting#eventhub_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#id MonitorAadDiagnosticSetting#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#log_analytics_workspace_id MonitorAadDiagnosticSetting#log_analytics_workspace_id}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#storage_account_id MonitorAadDiagnosticSetting#storage_account_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#timeouts MonitorAadDiagnosticSetting#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6bbf118b7d9be50bf3eac487eb78ef33e60b1cda6188bb1d38cd49207cc3fd47)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitorAadDiagnosticSettingConfig(
            log=log,
            name=name,
            eventhub_authorization_rule_id=eventhub_authorization_rule_id,
            eventhub_name=eventhub_name,
            id=id,
            log_analytics_workspace_id=log_analytics_workspace_id,
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

    @jsii.member(jsii_name="putLog")
    def put_log(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAadDiagnosticSettingLog", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bdd9c5813e33923266dcb95395fce0e20b28a567b1e53d051981c71f06faac2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putLog", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#create MonitorAadDiagnosticSetting#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#delete MonitorAadDiagnosticSetting#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#read MonitorAadDiagnosticSetting#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#update MonitorAadDiagnosticSetting#update}.
        '''
        value = MonitorAadDiagnosticSettingTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetEventhubAuthorizationRuleId")
    def reset_eventhub_authorization_rule_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventhubAuthorizationRuleId", []))

    @jsii.member(jsii_name="resetEventhubName")
    def reset_eventhub_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEventhubName", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetLogAnalyticsWorkspaceId")
    def reset_log_analytics_workspace_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLogAnalyticsWorkspaceId", []))

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
    @jsii.member(jsii_name="log")
    def log(self) -> "MonitorAadDiagnosticSettingLogList":
        return typing.cast("MonitorAadDiagnosticSettingLogList", jsii.get(self, "log"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MonitorAadDiagnosticSettingTimeoutsOutputReference":
        return typing.cast("MonitorAadDiagnosticSettingTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="eventhubAuthorizationRuleIdInput")
    def eventhub_authorization_rule_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventhubAuthorizationRuleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="eventhubNameInput")
    def eventhub_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "eventhubNameInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceIdInput")
    def log_analytics_workspace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "logAnalyticsWorkspaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="logInput")
    def log_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAadDiagnosticSettingLog"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAadDiagnosticSettingLog"]]], jsii.get(self, "logInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="storageAccountIdInput")
    def storage_account_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "storageAccountIdInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["MonitorAadDiagnosticSettingTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["MonitorAadDiagnosticSettingTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="eventhubAuthorizationRuleId")
    def eventhub_authorization_rule_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventhubAuthorizationRuleId"))

    @eventhub_authorization_rule_id.setter
    def eventhub_authorization_rule_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6777898adc604949d78e6efd09b2ee8bf1e63d77248b332295ef0ef141b2b85b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventhubAuthorizationRuleId", value)

    @builtins.property
    @jsii.member(jsii_name="eventhubName")
    def eventhub_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "eventhubName"))

    @eventhub_name.setter
    def eventhub_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__721ea3e54f67cbff0da2287d78610f73e3713c4e1668bab0eea6bc7880fccddf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "eventhubName", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82479ccabfab36eb5bac1d630e93bfd8af184c062f1ab17b7a57852fe247d3d2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="logAnalyticsWorkspaceId")
    def log_analytics_workspace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "logAnalyticsWorkspaceId"))

    @log_analytics_workspace_id.setter
    def log_analytics_workspace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5bf0ed2980c3b4a1486b713ebbc1c5924e8958e78b19cc91086dc104924a946)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logAnalyticsWorkspaceId", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec450d7bd544b609ceb86edc800ab8dfcdef5fdaad1cb3f7943dcba348aac053)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="storageAccountId")
    def storage_account_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "storageAccountId"))

    @storage_account_id.setter
    def storage_account_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71e0a286ccd99419e2fd3bce2e43b21f30c3f9f866fde3fecb1a3358008ca619)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "storageAccountId", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAadDiagnosticSetting.MonitorAadDiagnosticSettingConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "log": "log",
        "name": "name",
        "eventhub_authorization_rule_id": "eventhubAuthorizationRuleId",
        "eventhub_name": "eventhubName",
        "id": "id",
        "log_analytics_workspace_id": "logAnalyticsWorkspaceId",
        "storage_account_id": "storageAccountId",
        "timeouts": "timeouts",
    },
)
class MonitorAadDiagnosticSettingConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        log: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorAadDiagnosticSettingLog", typing.Dict[builtins.str, typing.Any]]]],
        name: builtins.str,
        eventhub_authorization_rule_id: typing.Optional[builtins.str] = None,
        eventhub_name: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        log_analytics_workspace_id: typing.Optional[builtins.str] = None,
        storage_account_id: typing.Optional[builtins.str] = None,
        timeouts: typing.Optional[typing.Union["MonitorAadDiagnosticSettingTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param log: log block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#log MonitorAadDiagnosticSetting#log}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#name MonitorAadDiagnosticSetting#name}.
        :param eventhub_authorization_rule_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#eventhub_authorization_rule_id MonitorAadDiagnosticSetting#eventhub_authorization_rule_id}.
        :param eventhub_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#eventhub_name MonitorAadDiagnosticSetting#eventhub_name}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#id MonitorAadDiagnosticSetting#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param log_analytics_workspace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#log_analytics_workspace_id MonitorAadDiagnosticSetting#log_analytics_workspace_id}.
        :param storage_account_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#storage_account_id MonitorAadDiagnosticSetting#storage_account_id}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#timeouts MonitorAadDiagnosticSetting#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = MonitorAadDiagnosticSettingTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35673b089135f6da62c02b2bedd00add2c7e20635ebf651e9d325f84861d02de)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument log", value=log, expected_type=type_hints["log"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument eventhub_authorization_rule_id", value=eventhub_authorization_rule_id, expected_type=type_hints["eventhub_authorization_rule_id"])
            check_type(argname="argument eventhub_name", value=eventhub_name, expected_type=type_hints["eventhub_name"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument log_analytics_workspace_id", value=log_analytics_workspace_id, expected_type=type_hints["log_analytics_workspace_id"])
            check_type(argname="argument storage_account_id", value=storage_account_id, expected_type=type_hints["storage_account_id"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "log": log,
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
        if eventhub_authorization_rule_id is not None:
            self._values["eventhub_authorization_rule_id"] = eventhub_authorization_rule_id
        if eventhub_name is not None:
            self._values["eventhub_name"] = eventhub_name
        if id is not None:
            self._values["id"] = id
        if log_analytics_workspace_id is not None:
            self._values["log_analytics_workspace_id"] = log_analytics_workspace_id
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
    def log(
        self,
    ) -> typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAadDiagnosticSettingLog"]]:
        '''log block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#log MonitorAadDiagnosticSetting#log}
        '''
        result = self._values.get("log")
        assert result is not None, "Required property 'log' is missing"
        return typing.cast(typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorAadDiagnosticSettingLog"]], result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#name MonitorAadDiagnosticSetting#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def eventhub_authorization_rule_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#eventhub_authorization_rule_id MonitorAadDiagnosticSetting#eventhub_authorization_rule_id}.'''
        result = self._values.get("eventhub_authorization_rule_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def eventhub_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#eventhub_name MonitorAadDiagnosticSetting#eventhub_name}.'''
        result = self._values.get("eventhub_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#id MonitorAadDiagnosticSetting#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def log_analytics_workspace_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#log_analytics_workspace_id MonitorAadDiagnosticSetting#log_analytics_workspace_id}.'''
        result = self._values.get("log_analytics_workspace_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def storage_account_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#storage_account_id MonitorAadDiagnosticSetting#storage_account_id}.'''
        result = self._values.get("storage_account_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MonitorAadDiagnosticSettingTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#timeouts MonitorAadDiagnosticSetting#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MonitorAadDiagnosticSettingTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAadDiagnosticSettingConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAadDiagnosticSetting.MonitorAadDiagnosticSettingLog",
    jsii_struct_bases=[],
    name_mapping={
        "category": "category",
        "retention_policy": "retentionPolicy",
        "enabled": "enabled",
    },
)
class MonitorAadDiagnosticSettingLog:
    def __init__(
        self,
        *,
        category: builtins.str,
        retention_policy: typing.Union["MonitorAadDiagnosticSettingLogRetentionPolicy", typing.Dict[builtins.str, typing.Any]],
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param category: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#category MonitorAadDiagnosticSetting#category}.
        :param retention_policy: retention_policy block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#retention_policy MonitorAadDiagnosticSetting#retention_policy}
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#enabled MonitorAadDiagnosticSetting#enabled}.
        '''
        if isinstance(retention_policy, dict):
            retention_policy = MonitorAadDiagnosticSettingLogRetentionPolicy(**retention_policy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bfc90deab9e14d4cb147d486a8c77e75f939d5d78d486900546c54b1b77bef2)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument retention_policy", value=retention_policy, expected_type=type_hints["retention_policy"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "category": category,
            "retention_policy": retention_policy,
        }
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def category(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#category MonitorAadDiagnosticSetting#category}.'''
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def retention_policy(self) -> "MonitorAadDiagnosticSettingLogRetentionPolicy":
        '''retention_policy block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#retention_policy MonitorAadDiagnosticSetting#retention_policy}
        '''
        result = self._values.get("retention_policy")
        assert result is not None, "Required property 'retention_policy' is missing"
        return typing.cast("MonitorAadDiagnosticSettingLogRetentionPolicy", result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#enabled MonitorAadDiagnosticSetting#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAadDiagnosticSettingLog(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAadDiagnosticSettingLogList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAadDiagnosticSetting.MonitorAadDiagnosticSettingLogList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0b37247013823d68cfcbf7206d43c7e209c766fc8c092ab16a25182aaeeb6bb0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorAadDiagnosticSettingLogOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a5283941109e87500201bf3ec36d1363dfc5cb0d2ce96074efeba507e40f80e)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorAadDiagnosticSettingLogOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5270de6b9c9d8b0d002eb73aba062775c4e702e5dbe4b8d2d2309a9d43f1af20)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44bd1c45876b90a4e28bbd7d9c11ad5cc4dbf592a3ee3ed7f8cf4e508f073116)
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
            type_hints = typing.get_type_hints(_typecheckingstub__cb5dca36612fe5aa07ee8133b37d8db7d9148d00320997957e513be5b0078362)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAadDiagnosticSettingLog]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAadDiagnosticSettingLog]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAadDiagnosticSettingLog]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43d2f986640a3f1b7d3142508b1784e54683d5af66615f7e442a5167de6260f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitorAadDiagnosticSettingLogOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAadDiagnosticSetting.MonitorAadDiagnosticSettingLogOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bda789d511d2e306690f873348f4e2596d6963e7c3e47d2366070a9a46bff954)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="putRetentionPolicy")
    def put_retention_policy(
        self,
        *,
        days: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#days MonitorAadDiagnosticSetting#days}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#enabled MonitorAadDiagnosticSetting#enabled}.
        '''
        value = MonitorAadDiagnosticSettingLogRetentionPolicy(
            days=days, enabled=enabled
        )

        return typing.cast(None, jsii.invoke(self, "putRetentionPolicy", [value]))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicy")
    def retention_policy(
        self,
    ) -> "MonitorAadDiagnosticSettingLogRetentionPolicyOutputReference":
        return typing.cast("MonitorAadDiagnosticSettingLogRetentionPolicyOutputReference", jsii.get(self, "retentionPolicy"))

    @builtins.property
    @jsii.member(jsii_name="categoryInput")
    def category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "categoryInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="retentionPolicyInput")
    def retention_policy_input(
        self,
    ) -> typing.Optional["MonitorAadDiagnosticSettingLogRetentionPolicy"]:
        return typing.cast(typing.Optional["MonitorAadDiagnosticSettingLogRetentionPolicy"], jsii.get(self, "retentionPolicyInput"))

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @category.setter
    def category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf48e6e608cd97a10635c2f501d492f87f502eb7948a5cd29b3a62321c31c1a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "category", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__1fee12584c250265ded7277d18ffbbce3eb047a81de9a20d35d2295a36fe9e53)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitorAadDiagnosticSettingLog, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitorAadDiagnosticSettingLog, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitorAadDiagnosticSettingLog, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e1346675c41ee00214741e4ab8f231f663da1b079b39dbb38a98af29840612a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAadDiagnosticSetting.MonitorAadDiagnosticSettingLogRetentionPolicy",
    jsii_struct_bases=[],
    name_mapping={"days": "days", "enabled": "enabled"},
)
class MonitorAadDiagnosticSettingLogRetentionPolicy:
    def __init__(
        self,
        *,
        days: typing.Optional[jsii.Number] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param days: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#days MonitorAadDiagnosticSetting#days}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#enabled MonitorAadDiagnosticSetting#enabled}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be0674d1d1536043ff825f0c0929b442abbb92da4d722764b7a450f1255cf7a1)
            check_type(argname="argument days", value=days, expected_type=type_hints["days"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if days is not None:
            self._values["days"] = days
        if enabled is not None:
            self._values["enabled"] = enabled

    @builtins.property
    def days(self) -> typing.Optional[jsii.Number]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#days MonitorAadDiagnosticSetting#days}.'''
        result = self._values.get("days")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#enabled MonitorAadDiagnosticSetting#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAadDiagnosticSettingLogRetentionPolicy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAadDiagnosticSettingLogRetentionPolicyOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAadDiagnosticSetting.MonitorAadDiagnosticSettingLogRetentionPolicyOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a2002c097d6e6bec2cf27cbcb15deb72b20b2a76969c2ff08e1df19c45006a81)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetDays")
    def reset_days(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDays", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

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
            type_hints = typing.get_type_hints(_typecheckingstub__b22458cacbf0c8e65677e3e716d1ce661977498a3a5222bb95b5786f82cbecbe)
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
            type_hints = typing.get_type_hints(_typecheckingstub__683f3f7ff9fab665b66037eeec2a825102762a35c615c2f6808e9f9b0906f105)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorAadDiagnosticSettingLogRetentionPolicy]:
        return typing.cast(typing.Optional[MonitorAadDiagnosticSettingLogRetentionPolicy], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorAadDiagnosticSettingLogRetentionPolicy],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0acbb1e9f6f56d4b3247960f5551970593da3f90cfbde7be67a75dd60968fb79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorAadDiagnosticSetting.MonitorAadDiagnosticSettingTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MonitorAadDiagnosticSettingTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#create MonitorAadDiagnosticSetting#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#delete MonitorAadDiagnosticSetting#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#read MonitorAadDiagnosticSetting#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#update MonitorAadDiagnosticSetting#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__719d2d3117803084467a643881af1abb45f35ee36a6d5cf8ab751a18187920a6)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#create MonitorAadDiagnosticSetting#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#delete MonitorAadDiagnosticSetting#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#read MonitorAadDiagnosticSetting#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_aad_diagnostic_setting#update MonitorAadDiagnosticSetting#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorAadDiagnosticSettingTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorAadDiagnosticSettingTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorAadDiagnosticSetting.MonitorAadDiagnosticSettingTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9130302bc1208e71cba601855e29faa8d0244e91ea0a8e81b824d00e06de962c)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d609b059f20ffd5f909d7eb0030efea0a209ddd415db158f50e38e9941ee70eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e00ee99197d6263a949864fe819a3b359dbc7b4115f3c6b1c2003a2b934e4de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b93988736be771f9c6878cab9e3cda998ac30e7bd812cc9975c7d79ecf6c349a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__95f68c42e2f375a7fd29d2d56c730c18461cf4a8684ca380b24527cddc700781)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitorAadDiagnosticSettingTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitorAadDiagnosticSettingTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitorAadDiagnosticSettingTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea8d286d66423083238352287c81c7c2844f04f0c8238ba404c602f4b0904bb1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MonitorAadDiagnosticSetting",
    "MonitorAadDiagnosticSettingConfig",
    "MonitorAadDiagnosticSettingLog",
    "MonitorAadDiagnosticSettingLogList",
    "MonitorAadDiagnosticSettingLogOutputReference",
    "MonitorAadDiagnosticSettingLogRetentionPolicy",
    "MonitorAadDiagnosticSettingLogRetentionPolicyOutputReference",
    "MonitorAadDiagnosticSettingTimeouts",
    "MonitorAadDiagnosticSettingTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__6bbf118b7d9be50bf3eac487eb78ef33e60b1cda6188bb1d38cd49207cc3fd47(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    log: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAadDiagnosticSettingLog, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    eventhub_authorization_rule_id: typing.Optional[builtins.str] = None,
    eventhub_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    log_analytics_workspace_id: typing.Optional[builtins.str] = None,
    storage_account_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[MonitorAadDiagnosticSettingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__7bdd9c5813e33923266dcb95395fce0e20b28a567b1e53d051981c71f06faac2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAadDiagnosticSettingLog, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6777898adc604949d78e6efd09b2ee8bf1e63d77248b332295ef0ef141b2b85b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__721ea3e54f67cbff0da2287d78610f73e3713c4e1668bab0eea6bc7880fccddf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82479ccabfab36eb5bac1d630e93bfd8af184c062f1ab17b7a57852fe247d3d2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5bf0ed2980c3b4a1486b713ebbc1c5924e8958e78b19cc91086dc104924a946(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec450d7bd544b609ceb86edc800ab8dfcdef5fdaad1cb3f7943dcba348aac053(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71e0a286ccd99419e2fd3bce2e43b21f30c3f9f866fde3fecb1a3358008ca619(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35673b089135f6da62c02b2bedd00add2c7e20635ebf651e9d325f84861d02de(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    log: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorAadDiagnosticSettingLog, typing.Dict[builtins.str, typing.Any]]]],
    name: builtins.str,
    eventhub_authorization_rule_id: typing.Optional[builtins.str] = None,
    eventhub_name: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    log_analytics_workspace_id: typing.Optional[builtins.str] = None,
    storage_account_id: typing.Optional[builtins.str] = None,
    timeouts: typing.Optional[typing.Union[MonitorAadDiagnosticSettingTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bfc90deab9e14d4cb147d486a8c77e75f939d5d78d486900546c54b1b77bef2(
    *,
    category: builtins.str,
    retention_policy: typing.Union[MonitorAadDiagnosticSettingLogRetentionPolicy, typing.Dict[builtins.str, typing.Any]],
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0b37247013823d68cfcbf7206d43c7e209c766fc8c092ab16a25182aaeeb6bb0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a5283941109e87500201bf3ec36d1363dfc5cb0d2ce96074efeba507e40f80e(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5270de6b9c9d8b0d002eb73aba062775c4e702e5dbe4b8d2d2309a9d43f1af20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44bd1c45876b90a4e28bbd7d9c11ad5cc4dbf592a3ee3ed7f8cf4e508f073116(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb5dca36612fe5aa07ee8133b37d8db7d9148d00320997957e513be5b0078362(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43d2f986640a3f1b7d3142508b1784e54683d5af66615f7e442a5167de6260f0(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorAadDiagnosticSettingLog]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda789d511d2e306690f873348f4e2596d6963e7c3e47d2366070a9a46bff954(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf48e6e608cd97a10635c2f501d492f87f502eb7948a5cd29b3a62321c31c1a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fee12584c250265ded7277d18ffbbce3eb047a81de9a20d35d2295a36fe9e53(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e1346675c41ee00214741e4ab8f231f663da1b079b39dbb38a98af29840612a(
    value: typing.Optional[typing.Union[MonitorAadDiagnosticSettingLog, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be0674d1d1536043ff825f0c0929b442abbb92da4d722764b7a450f1255cf7a1(
    *,
    days: typing.Optional[jsii.Number] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2002c097d6e6bec2cf27cbcb15deb72b20b2a76969c2ff08e1df19c45006a81(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b22458cacbf0c8e65677e3e716d1ce661977498a3a5222bb95b5786f82cbecbe(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__683f3f7ff9fab665b66037eeec2a825102762a35c615c2f6808e9f9b0906f105(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0acbb1e9f6f56d4b3247960f5551970593da3f90cfbde7be67a75dd60968fb79(
    value: typing.Optional[MonitorAadDiagnosticSettingLogRetentionPolicy],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__719d2d3117803084467a643881af1abb45f35ee36a6d5cf8ab751a18187920a6(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9130302bc1208e71cba601855e29faa8d0244e91ea0a8e81b824d00e06de962c(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d609b059f20ffd5f909d7eb0030efea0a209ddd415db158f50e38e9941ee70eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e00ee99197d6263a949864fe819a3b359dbc7b4115f3c6b1c2003a2b934e4de(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b93988736be771f9c6878cab9e3cda998ac30e7bd812cc9975c7d79ecf6c349a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__95f68c42e2f375a7fd29d2d56c730c18461cf4a8684ca380b24527cddc700781(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea8d286d66423083238352287c81c7c2844f04f0c8238ba404c602f4b0904bb1(
    value: typing.Optional[typing.Union[MonitorAadDiagnosticSettingTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
