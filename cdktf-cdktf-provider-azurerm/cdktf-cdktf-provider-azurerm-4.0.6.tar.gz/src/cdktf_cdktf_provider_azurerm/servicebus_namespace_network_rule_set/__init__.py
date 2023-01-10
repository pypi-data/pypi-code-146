'''
# `azurerm_servicebus_namespace_network_rule_set`

Refer to the Terraform Registory for docs: [`azurerm_servicebus_namespace_network_rule_set`](https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set).
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


class ServicebusNamespaceNetworkRuleSet(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.servicebusNamespaceNetworkRuleSet.ServicebusNamespaceNetworkRuleSet",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set azurerm_servicebus_namespace_network_rule_set}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        namespace_id: builtins.str,
        default_action: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServicebusNamespaceNetworkRuleSetNetworkRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ServicebusNamespaceNetworkRuleSetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trusted_services_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set azurerm_servicebus_namespace_network_rule_set} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param namespace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#namespace_id ServicebusNamespaceNetworkRuleSet#namespace_id}.
        :param default_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#default_action ServicebusNamespaceNetworkRuleSet#default_action}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#id ServicebusNamespaceNetworkRuleSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_rules: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#ip_rules ServicebusNamespaceNetworkRuleSet#ip_rules}.
        :param network_rules: network_rules block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#network_rules ServicebusNamespaceNetworkRuleSet#network_rules}
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#public_network_access_enabled ServicebusNamespaceNetworkRuleSet#public_network_access_enabled}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#timeouts ServicebusNamespaceNetworkRuleSet#timeouts}
        :param trusted_services_allowed: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#trusted_services_allowed ServicebusNamespaceNetworkRuleSet#trusted_services_allowed}.
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df4b3bbd3054e0c9bda5b2006698a13c47b369f46c4b3fc6b2b23d2516878821)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = ServicebusNamespaceNetworkRuleSetConfig(
            namespace_id=namespace_id,
            default_action=default_action,
            id=id,
            ip_rules=ip_rules,
            network_rules=network_rules,
            public_network_access_enabled=public_network_access_enabled,
            timeouts=timeouts,
            trusted_services_allowed=trusted_services_allowed,
            connection=connection,
            count=count,
            depends_on=depends_on,
            for_each=for_each,
            lifecycle=lifecycle,
            provider=provider,
            provisioners=provisioners,
        )

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putNetworkRules")
    def put_network_rules(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServicebusNamespaceNetworkRuleSetNetworkRules", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bb8e8a5bc9a075f8cb2a18eaa844df7113f6b5275c6a55c9d06853c947705c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putNetworkRules", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#create ServicebusNamespaceNetworkRuleSet#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#delete ServicebusNamespaceNetworkRuleSet#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#read ServicebusNamespaceNetworkRuleSet#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#update ServicebusNamespaceNetworkRuleSet#update}.
        '''
        value = ServicebusNamespaceNetworkRuleSetTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetDefaultAction")
    def reset_default_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDefaultAction", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetIpRules")
    def reset_ip_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIpRules", []))

    @jsii.member(jsii_name="resetNetworkRules")
    def reset_network_rules(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetNetworkRules", []))

    @jsii.member(jsii_name="resetPublicNetworkAccessEnabled")
    def reset_public_network_access_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPublicNetworkAccessEnabled", []))

    @jsii.member(jsii_name="resetTimeouts")
    def reset_timeouts(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTimeouts", []))

    @jsii.member(jsii_name="resetTrustedServicesAllowed")
    def reset_trusted_services_allowed(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTrustedServicesAllowed", []))

    @jsii.member(jsii_name="synthesizeAttributes")
    def _synthesize_attributes(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "synthesizeAttributes", []))

    @jsii.python.classproperty
    @jsii.member(jsii_name="tfResourceType")
    def TF_RESOURCE_TYPE(cls) -> builtins.str:
        return typing.cast(builtins.str, jsii.sget(cls, "tfResourceType"))

    @builtins.property
    @jsii.member(jsii_name="networkRules")
    def network_rules(self) -> "ServicebusNamespaceNetworkRuleSetNetworkRulesList":
        return typing.cast("ServicebusNamespaceNetworkRuleSetNetworkRulesList", jsii.get(self, "networkRules"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "ServicebusNamespaceNetworkRuleSetTimeoutsOutputReference":
        return typing.cast("ServicebusNamespaceNetworkRuleSetTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="defaultActionInput")
    def default_action_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "defaultActionInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="ipRulesInput")
    def ip_rules_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "ipRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="namespaceIdInput")
    def namespace_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "namespaceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="networkRulesInput")
    def network_rules_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServicebusNamespaceNetworkRuleSetNetworkRules"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServicebusNamespaceNetworkRuleSetNetworkRules"]]], jsii.get(self, "networkRulesInput"))

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabledInput")
    def public_network_access_enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "publicNetworkAccessEnabledInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["ServicebusNamespaceNetworkRuleSetTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["ServicebusNamespaceNetworkRuleSetTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="trustedServicesAllowedInput")
    def trusted_services_allowed_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "trustedServicesAllowedInput"))

    @builtins.property
    @jsii.member(jsii_name="defaultAction")
    def default_action(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "defaultAction"))

    @default_action.setter
    def default_action(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9699d685b982a8fe9e4c683a0f2bfef4f2fdce6eb9ca361b40f1cce9cbb46f42)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAction", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58229bb4ae273c40b85c2c7d88a90327558afd25972291f0c6cd7f5d2e1eb69e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="ipRules")
    def ip_rules(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "ipRules"))

    @ip_rules.setter
    def ip_rules(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18dd37cbb050b0eeefca7fe6608f66e2f729acfc6bda0c28d1b7b9aa6b7851fb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ipRules", value)

    @builtins.property
    @jsii.member(jsii_name="namespaceId")
    def namespace_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "namespaceId"))

    @namespace_id.setter
    def namespace_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5db317a0bd15f572d9ccaabeda570338f80efd82ab06548815b15a5b7bee40c2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "namespaceId", value)

    @builtins.property
    @jsii.member(jsii_name="publicNetworkAccessEnabled")
    def public_network_access_enabled(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "publicNetworkAccessEnabled"))

    @public_network_access_enabled.setter
    def public_network_access_enabled(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84e38ae52e4b96332a9bdf916c2cea0381db9ec3c7cd11383397140e38b9fd77)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "publicNetworkAccessEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="trustedServicesAllowed")
    def trusted_services_allowed(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "trustedServicesAllowed"))

    @trusted_services_allowed.setter
    def trusted_services_allowed(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b0cf4101713709aeaea7b75188701d50147fe56bf6df769dfe7881cbe326d17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "trustedServicesAllowed", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.servicebusNamespaceNetworkRuleSet.ServicebusNamespaceNetworkRuleSetConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "namespace_id": "namespaceId",
        "default_action": "defaultAction",
        "id": "id",
        "ip_rules": "ipRules",
        "network_rules": "networkRules",
        "public_network_access_enabled": "publicNetworkAccessEnabled",
        "timeouts": "timeouts",
        "trusted_services_allowed": "trustedServicesAllowed",
    },
)
class ServicebusNamespaceNetworkRuleSetConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        namespace_id: builtins.str,
        default_action: typing.Optional[builtins.str] = None,
        id: typing.Optional[builtins.str] = None,
        ip_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["ServicebusNamespaceNetworkRuleSetNetworkRules", typing.Dict[builtins.str, typing.Any]]]]] = None,
        public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        timeouts: typing.Optional[typing.Union["ServicebusNamespaceNetworkRuleSetTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        trusted_services_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param namespace_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#namespace_id ServicebusNamespaceNetworkRuleSet#namespace_id}.
        :param default_action: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#default_action ServicebusNamespaceNetworkRuleSet#default_action}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#id ServicebusNamespaceNetworkRuleSet#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param ip_rules: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#ip_rules ServicebusNamespaceNetworkRuleSet#ip_rules}.
        :param network_rules: network_rules block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#network_rules ServicebusNamespaceNetworkRuleSet#network_rules}
        :param public_network_access_enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#public_network_access_enabled ServicebusNamespaceNetworkRuleSet#public_network_access_enabled}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#timeouts ServicebusNamespaceNetworkRuleSet#timeouts}
        :param trusted_services_allowed: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#trusted_services_allowed ServicebusNamespaceNetworkRuleSet#trusted_services_allowed}.
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(timeouts, dict):
            timeouts = ServicebusNamespaceNetworkRuleSetTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ac6b5b5a885eb955094e0e7f07b0ed5ee8063e52bb0fbbb6af46288b335793b)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument namespace_id", value=namespace_id, expected_type=type_hints["namespace_id"])
            check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument ip_rules", value=ip_rules, expected_type=type_hints["ip_rules"])
            check_type(argname="argument network_rules", value=network_rules, expected_type=type_hints["network_rules"])
            check_type(argname="argument public_network_access_enabled", value=public_network_access_enabled, expected_type=type_hints["public_network_access_enabled"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
            check_type(argname="argument trusted_services_allowed", value=trusted_services_allowed, expected_type=type_hints["trusted_services_allowed"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "namespace_id": namespace_id,
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
        if default_action is not None:
            self._values["default_action"] = default_action
        if id is not None:
            self._values["id"] = id
        if ip_rules is not None:
            self._values["ip_rules"] = ip_rules
        if network_rules is not None:
            self._values["network_rules"] = network_rules
        if public_network_access_enabled is not None:
            self._values["public_network_access_enabled"] = public_network_access_enabled
        if timeouts is not None:
            self._values["timeouts"] = timeouts
        if trusted_services_allowed is not None:
            self._values["trusted_services_allowed"] = trusted_services_allowed

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
    def namespace_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#namespace_id ServicebusNamespaceNetworkRuleSet#namespace_id}.'''
        result = self._values.get("namespace_id")
        assert result is not None, "Required property 'namespace_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def default_action(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#default_action ServicebusNamespaceNetworkRuleSet#default_action}.'''
        result = self._values.get("default_action")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#id ServicebusNamespaceNetworkRuleSet#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ip_rules(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#ip_rules ServicebusNamespaceNetworkRuleSet#ip_rules}.'''
        result = self._values.get("ip_rules")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def network_rules(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServicebusNamespaceNetworkRuleSetNetworkRules"]]]:
        '''network_rules block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#network_rules ServicebusNamespaceNetworkRuleSet#network_rules}
        '''
        result = self._values.get("network_rules")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["ServicebusNamespaceNetworkRuleSetNetworkRules"]]], result)

    @builtins.property
    def public_network_access_enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#public_network_access_enabled ServicebusNamespaceNetworkRuleSet#public_network_access_enabled}.'''
        result = self._values.get("public_network_access_enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["ServicebusNamespaceNetworkRuleSetTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#timeouts ServicebusNamespaceNetworkRuleSet#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["ServicebusNamespaceNetworkRuleSetTimeouts"], result)

    @builtins.property
    def trusted_services_allowed(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#trusted_services_allowed ServicebusNamespaceNetworkRuleSet#trusted_services_allowed}.'''
        result = self._values.get("trusted_services_allowed")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicebusNamespaceNetworkRuleSetConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.servicebusNamespaceNetworkRuleSet.ServicebusNamespaceNetworkRuleSetNetworkRules",
    jsii_struct_bases=[],
    name_mapping={
        "subnet_id": "subnetId",
        "ignore_missing_vnet_service_endpoint": "ignoreMissingVnetServiceEndpoint",
    },
)
class ServicebusNamespaceNetworkRuleSetNetworkRules:
    def __init__(
        self,
        *,
        subnet_id: builtins.str,
        ignore_missing_vnet_service_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    ) -> None:
        '''
        :param subnet_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#subnet_id ServicebusNamespaceNetworkRuleSet#subnet_id}.
        :param ignore_missing_vnet_service_endpoint: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#ignore_missing_vnet_service_endpoint ServicebusNamespaceNetworkRuleSet#ignore_missing_vnet_service_endpoint}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a0395e82942395f7a636e9cb49866676a1958e04dbf2cabe8a6985fc65ee6b2d)
            check_type(argname="argument subnet_id", value=subnet_id, expected_type=type_hints["subnet_id"])
            check_type(argname="argument ignore_missing_vnet_service_endpoint", value=ignore_missing_vnet_service_endpoint, expected_type=type_hints["ignore_missing_vnet_service_endpoint"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "subnet_id": subnet_id,
        }
        if ignore_missing_vnet_service_endpoint is not None:
            self._values["ignore_missing_vnet_service_endpoint"] = ignore_missing_vnet_service_endpoint

    @builtins.property
    def subnet_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#subnet_id ServicebusNamespaceNetworkRuleSet#subnet_id}.'''
        result = self._values.get("subnet_id")
        assert result is not None, "Required property 'subnet_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def ignore_missing_vnet_service_endpoint(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#ignore_missing_vnet_service_endpoint ServicebusNamespaceNetworkRuleSet#ignore_missing_vnet_service_endpoint}.'''
        result = self._values.get("ignore_missing_vnet_service_endpoint")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicebusNamespaceNetworkRuleSetNetworkRules(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServicebusNamespaceNetworkRuleSetNetworkRulesList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.servicebusNamespaceNetworkRuleSet.ServicebusNamespaceNetworkRuleSetNetworkRulesList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b65f5788c2f58be75673160ada4730d5ed7d4e8dbd3a4eb991c570c842dc53ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "ServicebusNamespaceNetworkRuleSetNetworkRulesOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60b18e674562e8bf5608d2a29e41a214083acb46abed316f020d96b02fd66eaf)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("ServicebusNamespaceNetworkRuleSetNetworkRulesOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38a43f40819066c7ee416f8c4de83fef4469feb17860ef780d542159b32a1ea)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d80958cdad9ef9f823cbb179807682002c71f8e5eadf1bded327ac1f018aef36)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d1274bc35c50046f96c39748395c8db83d8676d9b5741814fd74a766a8285094)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServicebusNamespaceNetworkRuleSetNetworkRules]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServicebusNamespaceNetworkRuleSetNetworkRules]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServicebusNamespaceNetworkRuleSetNetworkRules]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48da0eca8907d170a83127bfb4e6af0730cc2570e1c91534cc6772533be8aef9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class ServicebusNamespaceNetworkRuleSetNetworkRulesOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.servicebusNamespaceNetworkRuleSet.ServicebusNamespaceNetworkRuleSetNetworkRulesOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3e389d7ae1b8cc4a7a1c95f4646148edf8a5a904a9d5d2027a8d9ce41c1f67ab)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetIgnoreMissingVnetServiceEndpoint")
    def reset_ignore_missing_vnet_service_endpoint(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetIgnoreMissingVnetServiceEndpoint", []))

    @builtins.property
    @jsii.member(jsii_name="ignoreMissingVnetServiceEndpointInput")
    def ignore_missing_vnet_service_endpoint_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "ignoreMissingVnetServiceEndpointInput"))

    @builtins.property
    @jsii.member(jsii_name="subnetIdInput")
    def subnet_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subnetIdInput"))

    @builtins.property
    @jsii.member(jsii_name="ignoreMissingVnetServiceEndpoint")
    def ignore_missing_vnet_service_endpoint(
        self,
    ) -> typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]:
        return typing.cast(typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable], jsii.get(self, "ignoreMissingVnetServiceEndpoint"))

    @ignore_missing_vnet_service_endpoint.setter
    def ignore_missing_vnet_service_endpoint(
        self,
        value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54e0ebe9bf44f9f1b8311e4e2fc5d7eb46ae621c63f89a9da0c0c4c737619ff9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "ignoreMissingVnetServiceEndpoint", value)

    @builtins.property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subnetId"))

    @subnet_id.setter
    def subnet_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e03377b3fc3d7b12808a778b0091fe35def9c097a511a395c8c15b34a8297a9e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subnetId", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ServicebusNamespaceNetworkRuleSetNetworkRules, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ServicebusNamespaceNetworkRuleSetNetworkRules, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ServicebusNamespaceNetworkRuleSetNetworkRules, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1689e2d118d40f3d564769476949d6b9e94dd85f4005040e45ddb124c236484a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.servicebusNamespaceNetworkRuleSet.ServicebusNamespaceNetworkRuleSetTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class ServicebusNamespaceNetworkRuleSetTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#create ServicebusNamespaceNetworkRuleSet#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#delete ServicebusNamespaceNetworkRuleSet#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#read ServicebusNamespaceNetworkRuleSet#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#update ServicebusNamespaceNetworkRuleSet#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8402232621fc7bcbe1226679bba7ae06aa3eedd21100370ea9e839362d0ba0f5)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#create ServicebusNamespaceNetworkRuleSet#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#delete ServicebusNamespaceNetworkRuleSet#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#read ServicebusNamespaceNetworkRuleSet#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/servicebus_namespace_network_rule_set#update ServicebusNamespaceNetworkRuleSet#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicebusNamespaceNetworkRuleSetTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ServicebusNamespaceNetworkRuleSetTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.servicebusNamespaceNetworkRuleSet.ServicebusNamespaceNetworkRuleSetTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__4abd5f90aa2363118c90cfd1701672d1c581d08a1a8013729a834c72f7ec1139)
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
            type_hints = typing.get_type_hints(_typecheckingstub__a5171df5a666aebe4426219b888a6f462146bd1eb52586f8dd5d11b4da9523d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f26665c1ca57e9119c3f821db3dd81b90907c4916d0939cd0b2b842e9640da3d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c742310e413371b4704bf47a33d85425df5d65e4533fe7aa1d52e048a5186ab6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f0cd673376f0d4ccd9b9750949b26ff7c9a315efdd1304a490c715a44a39e83c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[ServicebusNamespaceNetworkRuleSetTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[ServicebusNamespaceNetworkRuleSetTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[ServicebusNamespaceNetworkRuleSetTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f133ddb94e9b4a6b194597aef68906a4710c5b9c03ae859596e5f1668d0650af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "ServicebusNamespaceNetworkRuleSet",
    "ServicebusNamespaceNetworkRuleSetConfig",
    "ServicebusNamespaceNetworkRuleSetNetworkRules",
    "ServicebusNamespaceNetworkRuleSetNetworkRulesList",
    "ServicebusNamespaceNetworkRuleSetNetworkRulesOutputReference",
    "ServicebusNamespaceNetworkRuleSetTimeouts",
    "ServicebusNamespaceNetworkRuleSetTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__df4b3bbd3054e0c9bda5b2006698a13c47b369f46c4b3fc6b2b23d2516878821(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    namespace_id: builtins.str,
    default_action: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServicebusNamespaceNetworkRuleSetNetworkRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ServicebusNamespaceNetworkRuleSetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trusted_services_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
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

def _typecheckingstub__2bb8e8a5bc9a075f8cb2a18eaa844df7113f6b5275c6a55c9d06853c947705c2(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServicebusNamespaceNetworkRuleSetNetworkRules, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9699d685b982a8fe9e4c683a0f2bfef4f2fdce6eb9ca361b40f1cce9cbb46f42(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58229bb4ae273c40b85c2c7d88a90327558afd25972291f0c6cd7f5d2e1eb69e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18dd37cbb050b0eeefca7fe6608f66e2f729acfc6bda0c28d1b7b9aa6b7851fb(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5db317a0bd15f572d9ccaabeda570338f80efd82ab06548815b15a5b7bee40c2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84e38ae52e4b96332a9bdf916c2cea0381db9ec3c7cd11383397140e38b9fd77(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b0cf4101713709aeaea7b75188701d50147fe56bf6df769dfe7881cbe326d17(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ac6b5b5a885eb955094e0e7f07b0ed5ee8063e52bb0fbbb6af46288b335793b(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    namespace_id: builtins.str,
    default_action: typing.Optional[builtins.str] = None,
    id: typing.Optional[builtins.str] = None,
    ip_rules: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_rules: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[ServicebusNamespaceNetworkRuleSetNetworkRules, typing.Dict[builtins.str, typing.Any]]]]] = None,
    public_network_access_enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    timeouts: typing.Optional[typing.Union[ServicebusNamespaceNetworkRuleSetTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
    trusted_services_allowed: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a0395e82942395f7a636e9cb49866676a1958e04dbf2cabe8a6985fc65ee6b2d(
    *,
    subnet_id: builtins.str,
    ignore_missing_vnet_service_endpoint: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b65f5788c2f58be75673160ada4730d5ed7d4e8dbd3a4eb991c570c842dc53ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60b18e674562e8bf5608d2a29e41a214083acb46abed316f020d96b02fd66eaf(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38a43f40819066c7ee416f8c4de83fef4469feb17860ef780d542159b32a1ea(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d80958cdad9ef9f823cbb179807682002c71f8e5eadf1bded327ac1f018aef36(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1274bc35c50046f96c39748395c8db83d8676d9b5741814fd74a766a8285094(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48da0eca8907d170a83127bfb4e6af0730cc2570e1c91534cc6772533be8aef9(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[ServicebusNamespaceNetworkRuleSetNetworkRules]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e389d7ae1b8cc4a7a1c95f4646148edf8a5a904a9d5d2027a8d9ce41c1f67ab(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54e0ebe9bf44f9f1b8311e4e2fc5d7eb46ae621c63f89a9da0c0c4c737619ff9(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e03377b3fc3d7b12808a778b0091fe35def9c097a511a395c8c15b34a8297a9e(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1689e2d118d40f3d564769476949d6b9e94dd85f4005040e45ddb124c236484a(
    value: typing.Optional[typing.Union[ServicebusNamespaceNetworkRuleSetNetworkRules, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8402232621fc7bcbe1226679bba7ae06aa3eedd21100370ea9e839362d0ba0f5(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4abd5f90aa2363118c90cfd1701672d1c581d08a1a8013729a834c72f7ec1139(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5171df5a666aebe4426219b888a6f462146bd1eb52586f8dd5d11b4da9523d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f26665c1ca57e9119c3f821db3dd81b90907c4916d0939cd0b2b842e9640da3d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c742310e413371b4704bf47a33d85425df5d65e4533fe7aa1d52e048a5186ab6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0cd673376f0d4ccd9b9750949b26ff7c9a315efdd1304a490c715a44a39e83c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f133ddb94e9b4a6b194597aef68906a4710c5b9c03ae859596e5f1668d0650af(
    value: typing.Optional[typing.Union[ServicebusNamespaceNetworkRuleSetTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
