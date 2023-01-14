'''
# `azurerm_monitor_action_rule_action_group`

Refer to the Terraform Registory for docs: [`azurerm_monitor_action_rule_action_group`](https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group).
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


class MonitorActionRuleActionGroup(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroup",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group azurerm_monitor_action_rule_action_group}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        action_group_id: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        condition: typing.Optional[typing.Union["MonitorActionRuleActionGroupCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        scope: typing.Optional[typing.Union["MonitorActionRuleActionGroupScope", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorActionRuleActionGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group azurerm_monitor_action_rule_action_group} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param action_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#action_group_id MonitorActionRuleActionGroup#action_group_id}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#name MonitorActionRuleActionGroup#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#resource_group_name MonitorActionRuleActionGroup#resource_group_name}.
        :param condition: condition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#condition MonitorActionRuleActionGroup#condition}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#description MonitorActionRuleActionGroup#description}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#enabled MonitorActionRuleActionGroup#enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#id MonitorActionRuleActionGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scope: scope block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#scope MonitorActionRuleActionGroup#scope}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#tags MonitorActionRuleActionGroup#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#timeouts MonitorActionRuleActionGroup#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0ceb2339b9b4780b376bcad895eae028c35c40b2ffbfed7e56b9a93919f93a3)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitorActionRuleActionGroupConfig(
            action_group_id=action_group_id,
            name=name,
            resource_group_name=resource_group_name,
            condition=condition,
            description=description,
            enabled=enabled,
            id=id,
            scope=scope,
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

        jsii.create(self.__class__, self, [scope_, id_, config])

    @jsii.member(jsii_name="putCondition")
    def put_condition(
        self,
        *,
        alert_context: typing.Optional[typing.Union["MonitorActionRuleActionGroupConditionAlertContext", typing.Dict[builtins.str, typing.Any]]] = None,
        alert_rule_id: typing.Optional[typing.Union["MonitorActionRuleActionGroupConditionAlertRuleId", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[typing.Union["MonitorActionRuleActionGroupConditionDescription", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor: typing.Optional[typing.Union["MonitorActionRuleActionGroupConditionMonitor", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_service: typing.Optional[typing.Union["MonitorActionRuleActionGroupConditionMonitorService", typing.Dict[builtins.str, typing.Any]]] = None,
        severity: typing.Optional[typing.Union["MonitorActionRuleActionGroupConditionSeverity", typing.Dict[builtins.str, typing.Any]]] = None,
        target_resource_type: typing.Optional[typing.Union["MonitorActionRuleActionGroupConditionTargetResourceType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param alert_context: alert_context block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#alert_context MonitorActionRuleActionGroup#alert_context}
        :param alert_rule_id: alert_rule_id block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#alert_rule_id MonitorActionRuleActionGroup#alert_rule_id}
        :param description: description block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#description MonitorActionRuleActionGroup#description}
        :param monitor: monitor block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#monitor MonitorActionRuleActionGroup#monitor}
        :param monitor_service: monitor_service block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#monitor_service MonitorActionRuleActionGroup#monitor_service}
        :param severity: severity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#severity MonitorActionRuleActionGroup#severity}
        :param target_resource_type: target_resource_type block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#target_resource_type MonitorActionRuleActionGroup#target_resource_type}
        '''
        value = MonitorActionRuleActionGroupCondition(
            alert_context=alert_context,
            alert_rule_id=alert_rule_id,
            description=description,
            monitor=monitor,
            monitor_service=monitor_service,
            severity=severity,
            target_resource_type=target_resource_type,
        )

        return typing.cast(None, jsii.invoke(self, "putCondition", [value]))

    @jsii.member(jsii_name="putScope")
    def put_scope(
        self,
        *,
        resource_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param resource_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#resource_ids MonitorActionRuleActionGroup#resource_ids}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#type MonitorActionRuleActionGroup#type}.
        '''
        value = MonitorActionRuleActionGroupScope(resource_ids=resource_ids, type=type)

        return typing.cast(None, jsii.invoke(self, "putScope", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#create MonitorActionRuleActionGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#delete MonitorActionRuleActionGroup#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#read MonitorActionRuleActionGroup#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#update MonitorActionRuleActionGroup#update}.
        '''
        value = MonitorActionRuleActionGroupTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetCondition")
    def reset_condition(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCondition", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

    @jsii.member(jsii_name="resetScope")
    def reset_scope(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetScope", []))

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
    @jsii.member(jsii_name="condition")
    def condition(self) -> "MonitorActionRuleActionGroupConditionOutputReference":
        return typing.cast("MonitorActionRuleActionGroupConditionOutputReference", jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> "MonitorActionRuleActionGroupScopeOutputReference":
        return typing.cast("MonitorActionRuleActionGroupScopeOutputReference", jsii.get(self, "scope"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MonitorActionRuleActionGroupTimeoutsOutputReference":
        return typing.cast("MonitorActionRuleActionGroupTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionGroupIdInput")
    def action_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional["MonitorActionRuleActionGroupCondition"]:
        return typing.cast(typing.Optional["MonitorActionRuleActionGroupCondition"], jsii.get(self, "conditionInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="enabledInput")
    def enabled_input(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "enabledInput"))

    @builtins.property
    @jsii.member(jsii_name="idInput")
    def id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "idInput"))

    @builtins.property
    @jsii.member(jsii_name="nameInput")
    def name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "nameInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupNameInput")
    def resource_group_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupNameInput"))

    @builtins.property
    @jsii.member(jsii_name="scopeInput")
    def scope_input(self) -> typing.Optional["MonitorActionRuleActionGroupScope"]:
        return typing.cast(typing.Optional["MonitorActionRuleActionGroupScope"], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["MonitorActionRuleActionGroupTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["MonitorActionRuleActionGroupTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="actionGroupId")
    def action_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionGroupId"))

    @action_group_id.setter
    def action_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab47c3dde0597bb696cb1301a2e266ea404b17a285bbedef0671200db7d891d1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11a32ab3f8d26a26a7b43a811281b4e230da3fcea2bd0953564ccc550776e11d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

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
            type_hints = typing.get_type_hints(_typecheckingstub__737fa4522492195e1f401b5ff839055ed730ff9dfbd2d751c56f37bdd630c0fd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eac7bc6ecb2df2300959cd270384b64fbcaf7d17ae67c23b6a9cf4f9c2acb7a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b336308824b33556ad777622fb44a786db83740df8d46b3874470ba08deee260)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14ddc8b96b5d5bae9223da5a1c0fa27360d7d1ad3846fe1059cf1600fcf3e5aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7fcba2342b49a98f8d973e53746cdc214ba00ea0da1b5c29258e5742cbcdcdc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupCondition",
    jsii_struct_bases=[],
    name_mapping={
        "alert_context": "alertContext",
        "alert_rule_id": "alertRuleId",
        "description": "description",
        "monitor": "monitor",
        "monitor_service": "monitorService",
        "severity": "severity",
        "target_resource_type": "targetResourceType",
    },
)
class MonitorActionRuleActionGroupCondition:
    def __init__(
        self,
        *,
        alert_context: typing.Optional[typing.Union["MonitorActionRuleActionGroupConditionAlertContext", typing.Dict[builtins.str, typing.Any]]] = None,
        alert_rule_id: typing.Optional[typing.Union["MonitorActionRuleActionGroupConditionAlertRuleId", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[typing.Union["MonitorActionRuleActionGroupConditionDescription", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor: typing.Optional[typing.Union["MonitorActionRuleActionGroupConditionMonitor", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_service: typing.Optional[typing.Union["MonitorActionRuleActionGroupConditionMonitorService", typing.Dict[builtins.str, typing.Any]]] = None,
        severity: typing.Optional[typing.Union["MonitorActionRuleActionGroupConditionSeverity", typing.Dict[builtins.str, typing.Any]]] = None,
        target_resource_type: typing.Optional[typing.Union["MonitorActionRuleActionGroupConditionTargetResourceType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param alert_context: alert_context block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#alert_context MonitorActionRuleActionGroup#alert_context}
        :param alert_rule_id: alert_rule_id block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#alert_rule_id MonitorActionRuleActionGroup#alert_rule_id}
        :param description: description block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#description MonitorActionRuleActionGroup#description}
        :param monitor: monitor block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#monitor MonitorActionRuleActionGroup#monitor}
        :param monitor_service: monitor_service block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#monitor_service MonitorActionRuleActionGroup#monitor_service}
        :param severity: severity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#severity MonitorActionRuleActionGroup#severity}
        :param target_resource_type: target_resource_type block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#target_resource_type MonitorActionRuleActionGroup#target_resource_type}
        '''
        if isinstance(alert_context, dict):
            alert_context = MonitorActionRuleActionGroupConditionAlertContext(**alert_context)
        if isinstance(alert_rule_id, dict):
            alert_rule_id = MonitorActionRuleActionGroupConditionAlertRuleId(**alert_rule_id)
        if isinstance(description, dict):
            description = MonitorActionRuleActionGroupConditionDescription(**description)
        if isinstance(monitor, dict):
            monitor = MonitorActionRuleActionGroupConditionMonitor(**monitor)
        if isinstance(monitor_service, dict):
            monitor_service = MonitorActionRuleActionGroupConditionMonitorService(**monitor_service)
        if isinstance(severity, dict):
            severity = MonitorActionRuleActionGroupConditionSeverity(**severity)
        if isinstance(target_resource_type, dict):
            target_resource_type = MonitorActionRuleActionGroupConditionTargetResourceType(**target_resource_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc10dc3e51060957480bcf361027e6f9fb03feb4ab9a4e69ebba70f8cb9b8ffe)
            check_type(argname="argument alert_context", value=alert_context, expected_type=type_hints["alert_context"])
            check_type(argname="argument alert_rule_id", value=alert_rule_id, expected_type=type_hints["alert_rule_id"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument monitor", value=monitor, expected_type=type_hints["monitor"])
            check_type(argname="argument monitor_service", value=monitor_service, expected_type=type_hints["monitor_service"])
            check_type(argname="argument severity", value=severity, expected_type=type_hints["severity"])
            check_type(argname="argument target_resource_type", value=target_resource_type, expected_type=type_hints["target_resource_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if alert_context is not None:
            self._values["alert_context"] = alert_context
        if alert_rule_id is not None:
            self._values["alert_rule_id"] = alert_rule_id
        if description is not None:
            self._values["description"] = description
        if monitor is not None:
            self._values["monitor"] = monitor
        if monitor_service is not None:
            self._values["monitor_service"] = monitor_service
        if severity is not None:
            self._values["severity"] = severity
        if target_resource_type is not None:
            self._values["target_resource_type"] = target_resource_type

    @builtins.property
    def alert_context(
        self,
    ) -> typing.Optional["MonitorActionRuleActionGroupConditionAlertContext"]:
        '''alert_context block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#alert_context MonitorActionRuleActionGroup#alert_context}
        '''
        result = self._values.get("alert_context")
        return typing.cast(typing.Optional["MonitorActionRuleActionGroupConditionAlertContext"], result)

    @builtins.property
    def alert_rule_id(
        self,
    ) -> typing.Optional["MonitorActionRuleActionGroupConditionAlertRuleId"]:
        '''alert_rule_id block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#alert_rule_id MonitorActionRuleActionGroup#alert_rule_id}
        '''
        result = self._values.get("alert_rule_id")
        return typing.cast(typing.Optional["MonitorActionRuleActionGroupConditionAlertRuleId"], result)

    @builtins.property
    def description(
        self,
    ) -> typing.Optional["MonitorActionRuleActionGroupConditionDescription"]:
        '''description block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#description MonitorActionRuleActionGroup#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional["MonitorActionRuleActionGroupConditionDescription"], result)

    @builtins.property
    def monitor(
        self,
    ) -> typing.Optional["MonitorActionRuleActionGroupConditionMonitor"]:
        '''monitor block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#monitor MonitorActionRuleActionGroup#monitor}
        '''
        result = self._values.get("monitor")
        return typing.cast(typing.Optional["MonitorActionRuleActionGroupConditionMonitor"], result)

    @builtins.property
    def monitor_service(
        self,
    ) -> typing.Optional["MonitorActionRuleActionGroupConditionMonitorService"]:
        '''monitor_service block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#monitor_service MonitorActionRuleActionGroup#monitor_service}
        '''
        result = self._values.get("monitor_service")
        return typing.cast(typing.Optional["MonitorActionRuleActionGroupConditionMonitorService"], result)

    @builtins.property
    def severity(
        self,
    ) -> typing.Optional["MonitorActionRuleActionGroupConditionSeverity"]:
        '''severity block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#severity MonitorActionRuleActionGroup#severity}
        '''
        result = self._values.get("severity")
        return typing.cast(typing.Optional["MonitorActionRuleActionGroupConditionSeverity"], result)

    @builtins.property
    def target_resource_type(
        self,
    ) -> typing.Optional["MonitorActionRuleActionGroupConditionTargetResourceType"]:
        '''target_resource_type block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#target_resource_type MonitorActionRuleActionGroup#target_resource_type}
        '''
        result = self._values.get("target_resource_type")
        return typing.cast(typing.Optional["MonitorActionRuleActionGroupConditionTargetResourceType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleActionGroupCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupConditionAlertContext",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorActionRuleActionGroupConditionAlertContext:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc0914010d5d46edfb10228f0030f261a8351da83b0c4d19e8918d065f64f503)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleActionGroupConditionAlertContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleActionGroupConditionAlertContextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupConditionAlertContextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__07c737544b79248c95a9d41e71b935ad3b7a3001e604f6dd693c85d81c18fcf0)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b307a6370334b1283a8000408c0f9456f5790c91dff21494e30e84b376a9fddd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ea6c2fe948baf6d11f029c4057e5ec8a842ac2f021e016ca9b2b03fe2bc8b22)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorActionRuleActionGroupConditionAlertContext]:
        return typing.cast(typing.Optional[MonitorActionRuleActionGroupConditionAlertContext], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleActionGroupConditionAlertContext],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f1b92cdd65e319b8abfd2315f5d4ea37ee65ff4d47f12eabe625b840a353109)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupConditionAlertRuleId",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorActionRuleActionGroupConditionAlertRuleId:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88dcb2b643b12bffd69941e5ff0bc6c54815f90356a19833f95806707a8b1fb9)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleActionGroupConditionAlertRuleId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleActionGroupConditionAlertRuleIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupConditionAlertRuleIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__b3e10b34c404fbfb87e62d305be5ae0b461345b8a6054096deeb650b872e8653)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__793052f7cf36e437264500313fcd1ac66fedbd3edbdd98351c7ba67e6d2a1c87)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f38a2e5310d3be34c4efd4e8125da9ec4d6732f55d566ce5e3f418debe4ba99b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorActionRuleActionGroupConditionAlertRuleId]:
        return typing.cast(typing.Optional[MonitorActionRuleActionGroupConditionAlertRuleId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleActionGroupConditionAlertRuleId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe212657486c7173b35e211f391081de3239cafdb8e09be9140874202b6dc8b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupConditionDescription",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorActionRuleActionGroupConditionDescription:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75e6f2aab75de4086e12deb3b28e6218a8de4c890ea52ff51f8a23b857e5e5bd)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleActionGroupConditionDescription(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleActionGroupConditionDescriptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupConditionDescriptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1457a66f5e503b6d8b2b66ee0e609942b929ccf60959086cc7f6c42ffb5b07a8)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c96217d7ef3d69211e4f13750be833f9d87c8b00212e887b9ed252c2daf8549f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8283eabfee2e913bb643bd689fbb2027fa35ca520fe73f263f0bd6ce94f7da6b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorActionRuleActionGroupConditionDescription]:
        return typing.cast(typing.Optional[MonitorActionRuleActionGroupConditionDescription], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleActionGroupConditionDescription],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b580a40093c905dfa0ad487a1102a6477a622bf23506aeed90e6218824d67665)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupConditionMonitor",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorActionRuleActionGroupConditionMonitor:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fd6fd9b335c629f733ac4147ae4d16bf906a5e2a2bab7450f486bdd49e940d1)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleActionGroupConditionMonitor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleActionGroupConditionMonitorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupConditionMonitorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ee2e1150b8cdc699d3bcd01501c5369fe055ce7b6853bb62d17fd282f9a9c7a)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__41760e3e82e6acab1115b6f612408d42e411aae6ac310a4ac475b59c4982cda9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e13527f15742618114ea0c0748958115ac8a5d76d7aab7db40edcc325cb4789)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorActionRuleActionGroupConditionMonitor]:
        return typing.cast(typing.Optional[MonitorActionRuleActionGroupConditionMonitor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleActionGroupConditionMonitor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a95bb2d8433421b7d8e17ef8befaf07a54bb6242bc8e911a9f229b1487418703)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupConditionMonitorService",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorActionRuleActionGroupConditionMonitorService:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5b1b0580735dad0df50bb50d649a472074da6001113acf474836427be6aa71b)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleActionGroupConditionMonitorService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleActionGroupConditionMonitorServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupConditionMonitorServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a98524a3e939c6db971a7e5e2f503b7e44fe1b4ba1d8d137751ccfd886759ae5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10a25c1f6a5a384f09db75a7ee65400dee100592ca7d564d5295bfab86cf2438)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eee534c1f76e08473291f17b72bd5eaa22422b8ee5d869353e66c862a2c3d14)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorActionRuleActionGroupConditionMonitorService]:
        return typing.cast(typing.Optional[MonitorActionRuleActionGroupConditionMonitorService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleActionGroupConditionMonitorService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f226a94addff4afc9d6ebdded1aa9d9bdeca370f6d249b305b7fc48d44a269a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitorActionRuleActionGroupConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__45fd2fed910f38aee3ffb66525b32f55b5d37c5110081f8bb0166c1a11853702)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putAlertContext")
    def put_alert_context(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.
        '''
        value = MonitorActionRuleActionGroupConditionAlertContext(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putAlertContext", [value]))

    @jsii.member(jsii_name="putAlertRuleId")
    def put_alert_rule_id(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.
        '''
        value = MonitorActionRuleActionGroupConditionAlertRuleId(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putAlertRuleId", [value]))

    @jsii.member(jsii_name="putDescription")
    def put_description(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.
        '''
        value = MonitorActionRuleActionGroupConditionDescription(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putDescription", [value]))

    @jsii.member(jsii_name="putMonitor")
    def put_monitor(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.
        '''
        value = MonitorActionRuleActionGroupConditionMonitor(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putMonitor", [value]))

    @jsii.member(jsii_name="putMonitorService")
    def put_monitor_service(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.
        '''
        value = MonitorActionRuleActionGroupConditionMonitorService(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putMonitorService", [value]))

    @jsii.member(jsii_name="putSeverity")
    def put_severity(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.
        '''
        value = MonitorActionRuleActionGroupConditionSeverity(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putSeverity", [value]))

    @jsii.member(jsii_name="putTargetResourceType")
    def put_target_resource_type(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.
        '''
        value = MonitorActionRuleActionGroupConditionTargetResourceType(
            operator=operator, values=values
        )

        return typing.cast(None, jsii.invoke(self, "putTargetResourceType", [value]))

    @jsii.member(jsii_name="resetAlertContext")
    def reset_alert_context(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlertContext", []))

    @jsii.member(jsii_name="resetAlertRuleId")
    def reset_alert_rule_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAlertRuleId", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetMonitor")
    def reset_monitor(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitor", []))

    @jsii.member(jsii_name="resetMonitorService")
    def reset_monitor_service(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetMonitorService", []))

    @jsii.member(jsii_name="resetSeverity")
    def reset_severity(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSeverity", []))

    @jsii.member(jsii_name="resetTargetResourceType")
    def reset_target_resource_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetTargetResourceType", []))

    @builtins.property
    @jsii.member(jsii_name="alertContext")
    def alert_context(
        self,
    ) -> MonitorActionRuleActionGroupConditionAlertContextOutputReference:
        return typing.cast(MonitorActionRuleActionGroupConditionAlertContextOutputReference, jsii.get(self, "alertContext"))

    @builtins.property
    @jsii.member(jsii_name="alertRuleId")
    def alert_rule_id(
        self,
    ) -> MonitorActionRuleActionGroupConditionAlertRuleIdOutputReference:
        return typing.cast(MonitorActionRuleActionGroupConditionAlertRuleIdOutputReference, jsii.get(self, "alertRuleId"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(
        self,
    ) -> MonitorActionRuleActionGroupConditionDescriptionOutputReference:
        return typing.cast(MonitorActionRuleActionGroupConditionDescriptionOutputReference, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="monitor")
    def monitor(self) -> MonitorActionRuleActionGroupConditionMonitorOutputReference:
        return typing.cast(MonitorActionRuleActionGroupConditionMonitorOutputReference, jsii.get(self, "monitor"))

    @builtins.property
    @jsii.member(jsii_name="monitorService")
    def monitor_service(
        self,
    ) -> MonitorActionRuleActionGroupConditionMonitorServiceOutputReference:
        return typing.cast(MonitorActionRuleActionGroupConditionMonitorServiceOutputReference, jsii.get(self, "monitorService"))

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(
        self,
    ) -> "MonitorActionRuleActionGroupConditionSeverityOutputReference":
        return typing.cast("MonitorActionRuleActionGroupConditionSeverityOutputReference", jsii.get(self, "severity"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceType")
    def target_resource_type(
        self,
    ) -> "MonitorActionRuleActionGroupConditionTargetResourceTypeOutputReference":
        return typing.cast("MonitorActionRuleActionGroupConditionTargetResourceTypeOutputReference", jsii.get(self, "targetResourceType"))

    @builtins.property
    @jsii.member(jsii_name="alertContextInput")
    def alert_context_input(
        self,
    ) -> typing.Optional[MonitorActionRuleActionGroupConditionAlertContext]:
        return typing.cast(typing.Optional[MonitorActionRuleActionGroupConditionAlertContext], jsii.get(self, "alertContextInput"))

    @builtins.property
    @jsii.member(jsii_name="alertRuleIdInput")
    def alert_rule_id_input(
        self,
    ) -> typing.Optional[MonitorActionRuleActionGroupConditionAlertRuleId]:
        return typing.cast(typing.Optional[MonitorActionRuleActionGroupConditionAlertRuleId], jsii.get(self, "alertRuleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(
        self,
    ) -> typing.Optional[MonitorActionRuleActionGroupConditionDescription]:
        return typing.cast(typing.Optional[MonitorActionRuleActionGroupConditionDescription], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorInput")
    def monitor_input(
        self,
    ) -> typing.Optional[MonitorActionRuleActionGroupConditionMonitor]:
        return typing.cast(typing.Optional[MonitorActionRuleActionGroupConditionMonitor], jsii.get(self, "monitorInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorServiceInput")
    def monitor_service_input(
        self,
    ) -> typing.Optional[MonitorActionRuleActionGroupConditionMonitorService]:
        return typing.cast(typing.Optional[MonitorActionRuleActionGroupConditionMonitorService], jsii.get(self, "monitorServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(
        self,
    ) -> typing.Optional["MonitorActionRuleActionGroupConditionSeverity"]:
        return typing.cast(typing.Optional["MonitorActionRuleActionGroupConditionSeverity"], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceTypeInput")
    def target_resource_type_input(
        self,
    ) -> typing.Optional["MonitorActionRuleActionGroupConditionTargetResourceType"]:
        return typing.cast(typing.Optional["MonitorActionRuleActionGroupConditionTargetResourceType"], jsii.get(self, "targetResourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorActionRuleActionGroupCondition]:
        return typing.cast(typing.Optional[MonitorActionRuleActionGroupCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleActionGroupCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a25ce8416c863b0f32508984cfc8c120f0bfa5b7133d58898058888f0c492663)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupConditionSeverity",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorActionRuleActionGroupConditionSeverity:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1bc31d68caa4900f3c6fe84d64c70f3907e7a9fc2305c816ed33a3cbcbe59ca)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleActionGroupConditionSeverity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleActionGroupConditionSeverityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupConditionSeverityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__d0a7076348e3036456f872ed6f13a9e1e0ba43809c38a4ef0b8a3bfd72e3e9a9)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__440fb26a8ee53792f2dba64df6762cd9328b01d131cf145a0c1ca5741094078d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6a30f64b355e67900dc30c3c2247368bea96307e95a2944f054a21c404e81579)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorActionRuleActionGroupConditionSeverity]:
        return typing.cast(typing.Optional[MonitorActionRuleActionGroupConditionSeverity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleActionGroupConditionSeverity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c19bb022ebd3fdb6564f8b89e69d5dd20e4a7a222f66cf19374c4bf23a219e0a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupConditionTargetResourceType",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorActionRuleActionGroupConditionTargetResourceType:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b05b2fe0f47556504fe470ecd84d88fb4bf9c433fc6e7f16f127237e77ca6380)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#operator MonitorActionRuleActionGroup#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#values MonitorActionRuleActionGroup#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleActionGroupConditionTargetResourceType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleActionGroupConditionTargetResourceTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupConditionTargetResourceTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__96fdd269e339b7470ed0d96b99a22bf6de6ebe74e307ec892c8d1907ec8a2398)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="operatorInput")
    def operator_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operatorInput"))

    @builtins.property
    @jsii.member(jsii_name="valuesInput")
    def values_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "valuesInput"))

    @builtins.property
    @jsii.member(jsii_name="operator")
    def operator(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operator"))

    @operator.setter
    def operator(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1d3a3496bf223760f1279308abad75328120cac713e48682beb150a4b239f5f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cdcff6f467f2afc023438795c49108ccb266f52f31184c6a3e310168169efab)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorActionRuleActionGroupConditionTargetResourceType]:
        return typing.cast(typing.Optional[MonitorActionRuleActionGroupConditionTargetResourceType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleActionGroupConditionTargetResourceType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e08ba7a5ee0b3a3647f1ddf56653d8e27bc45f2c3a7228a17dfea185dd15953)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "action_group_id": "actionGroupId",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "condition": "condition",
        "description": "description",
        "enabled": "enabled",
        "id": "id",
        "scope": "scope",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class MonitorActionRuleActionGroupConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        action_group_id: builtins.str,
        name: builtins.str,
        resource_group_name: builtins.str,
        condition: typing.Optional[typing.Union[MonitorActionRuleActionGroupCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        scope: typing.Optional[typing.Union["MonitorActionRuleActionGroupScope", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorActionRuleActionGroupTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param action_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#action_group_id MonitorActionRuleActionGroup#action_group_id}.
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#name MonitorActionRuleActionGroup#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#resource_group_name MonitorActionRuleActionGroup#resource_group_name}.
        :param condition: condition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#condition MonitorActionRuleActionGroup#condition}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#description MonitorActionRuleActionGroup#description}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#enabled MonitorActionRuleActionGroup#enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#id MonitorActionRuleActionGroup#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scope: scope block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#scope MonitorActionRuleActionGroup#scope}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#tags MonitorActionRuleActionGroup#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#timeouts MonitorActionRuleActionGroup#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(condition, dict):
            condition = MonitorActionRuleActionGroupCondition(**condition)
        if isinstance(scope, dict):
            scope = MonitorActionRuleActionGroupScope(**scope)
        if isinstance(timeouts, dict):
            timeouts = MonitorActionRuleActionGroupTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c857432e4a61301db1916e6babc9deabba022e2263730ce34b302a1a438ef1cf)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument action_group_id", value=action_group_id, expected_type=type_hints["action_group_id"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_group_id": action_group_id,
            "name": name,
            "resource_group_name": resource_group_name,
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
        if condition is not None:
            self._values["condition"] = condition
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
        if scope is not None:
            self._values["scope"] = scope
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
    def action_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#action_group_id MonitorActionRuleActionGroup#action_group_id}.'''
        result = self._values.get("action_group_id")
        assert result is not None, "Required property 'action_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#name MonitorActionRuleActionGroup#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#resource_group_name MonitorActionRuleActionGroup#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition(self) -> typing.Optional[MonitorActionRuleActionGroupCondition]:
        '''condition block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#condition MonitorActionRuleActionGroup#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[MonitorActionRuleActionGroupCondition], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#description MonitorActionRuleActionGroup#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#enabled MonitorActionRuleActionGroup#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#id MonitorActionRuleActionGroup#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional["MonitorActionRuleActionGroupScope"]:
        '''scope block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#scope MonitorActionRuleActionGroup#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional["MonitorActionRuleActionGroupScope"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#tags MonitorActionRuleActionGroup#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MonitorActionRuleActionGroupTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#timeouts MonitorActionRuleActionGroup#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MonitorActionRuleActionGroupTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleActionGroupConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupScope",
    jsii_struct_bases=[],
    name_mapping={"resource_ids": "resourceIds", "type": "type"},
)
class MonitorActionRuleActionGroupScope:
    def __init__(
        self,
        *,
        resource_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param resource_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#resource_ids MonitorActionRuleActionGroup#resource_ids}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#type MonitorActionRuleActionGroup#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f2df093186a762e4b63b4a5ac26a0e3aaab166075700d7381807073b1d68f48)
            check_type(argname="argument resource_ids", value=resource_ids, expected_type=type_hints["resource_ids"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_ids": resource_ids,
            "type": type,
        }

    @builtins.property
    def resource_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#resource_ids MonitorActionRuleActionGroup#resource_ids}.'''
        result = self._values.get("resource_ids")
        assert result is not None, "Required property 'resource_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#type MonitorActionRuleActionGroup#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleActionGroupScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleActionGroupScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__2c79212b0bd635c7b3529ddbe93d7cfd0576a2ae7537e1341ce2c8cda13b9961)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @builtins.property
    @jsii.member(jsii_name="resourceIdsInput")
    def resource_ids_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceIdsInput"))

    @builtins.property
    @jsii.member(jsii_name="typeInput")
    def type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "typeInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceIds")
    def resource_ids(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceIds"))

    @resource_ids.setter
    def resource_ids(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__888e3eb827ef75599b3074701c804b268b3ffde412b53e11ad3426a8662bbcf4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceIds", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f7004f8207a95f7b43338e467d1e71879673d1bc4e97efbf314faf99fa8a44d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorActionRuleActionGroupScope]:
        return typing.cast(typing.Optional[MonitorActionRuleActionGroupScope], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleActionGroupScope],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c98bda15078df44508d05fb2c8d80fc32abe7ee3bf8d5433a817e51e5ea1d61b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MonitorActionRuleActionGroupTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#create MonitorActionRuleActionGroup#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#delete MonitorActionRuleActionGroup#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#read MonitorActionRuleActionGroup#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#update MonitorActionRuleActionGroup#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__facbd706cc31930677cf910811287238670efe7fde663b661011d21ba882dc14)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#create MonitorActionRuleActionGroup#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#delete MonitorActionRuleActionGroup#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#read MonitorActionRuleActionGroup#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_action_group#update MonitorActionRuleActionGroup#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleActionGroupTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleActionGroupTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleActionGroup.MonitorActionRuleActionGroupTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__3914b2c7d6fcdc8449445b97a9df686272cca3efde1d92db4e9bc9fd34ef3041)
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
            type_hints = typing.get_type_hints(_typecheckingstub__41ba659e41605eff659970973137dd00bc1219c2ddab02e182246b0777c11e83)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3f9f06dd4f409aad37ef1edeafc70fd5576f66cc34b7ffb4b2e26f603c27ebf)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15647bff539e24bb1be81861e1858ecb0ae212830aa81e9c3e11ff2a15e41cd5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c906b0db4dc365be9004502f5db01fcf01f920a8aa4001d12270e09acddd8eb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitorActionRuleActionGroupTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitorActionRuleActionGroupTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitorActionRuleActionGroupTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__22dc81804ea9a55f039eae3893a089869f40fbe92d5a36c3c0982c6f48b439aa)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MonitorActionRuleActionGroup",
    "MonitorActionRuleActionGroupCondition",
    "MonitorActionRuleActionGroupConditionAlertContext",
    "MonitorActionRuleActionGroupConditionAlertContextOutputReference",
    "MonitorActionRuleActionGroupConditionAlertRuleId",
    "MonitorActionRuleActionGroupConditionAlertRuleIdOutputReference",
    "MonitorActionRuleActionGroupConditionDescription",
    "MonitorActionRuleActionGroupConditionDescriptionOutputReference",
    "MonitorActionRuleActionGroupConditionMonitor",
    "MonitorActionRuleActionGroupConditionMonitorOutputReference",
    "MonitorActionRuleActionGroupConditionMonitorService",
    "MonitorActionRuleActionGroupConditionMonitorServiceOutputReference",
    "MonitorActionRuleActionGroupConditionOutputReference",
    "MonitorActionRuleActionGroupConditionSeverity",
    "MonitorActionRuleActionGroupConditionSeverityOutputReference",
    "MonitorActionRuleActionGroupConditionTargetResourceType",
    "MonitorActionRuleActionGroupConditionTargetResourceTypeOutputReference",
    "MonitorActionRuleActionGroupConfig",
    "MonitorActionRuleActionGroupScope",
    "MonitorActionRuleActionGroupScopeOutputReference",
    "MonitorActionRuleActionGroupTimeouts",
    "MonitorActionRuleActionGroupTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__c0ceb2339b9b4780b376bcad895eae028c35c40b2ffbfed7e56b9a93919f93a3(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    action_group_id: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    condition: typing.Optional[typing.Union[MonitorActionRuleActionGroupCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    scope: typing.Optional[typing.Union[MonitorActionRuleActionGroupScope, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorActionRuleActionGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__ab47c3dde0597bb696cb1301a2e266ea404b17a285bbedef0671200db7d891d1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11a32ab3f8d26a26a7b43a811281b4e230da3fcea2bd0953564ccc550776e11d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__737fa4522492195e1f401b5ff839055ed730ff9dfbd2d751c56f37bdd630c0fd(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eac7bc6ecb2df2300959cd270384b64fbcaf7d17ae67c23b6a9cf4f9c2acb7a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b336308824b33556ad777622fb44a786db83740df8d46b3874470ba08deee260(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14ddc8b96b5d5bae9223da5a1c0fa27360d7d1ad3846fe1059cf1600fcf3e5aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7fcba2342b49a98f8d973e53746cdc214ba00ea0da1b5c29258e5742cbcdcdc3(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc10dc3e51060957480bcf361027e6f9fb03feb4ab9a4e69ebba70f8cb9b8ffe(
    *,
    alert_context: typing.Optional[typing.Union[MonitorActionRuleActionGroupConditionAlertContext, typing.Dict[builtins.str, typing.Any]]] = None,
    alert_rule_id: typing.Optional[typing.Union[MonitorActionRuleActionGroupConditionAlertRuleId, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[typing.Union[MonitorActionRuleActionGroupConditionDescription, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor: typing.Optional[typing.Union[MonitorActionRuleActionGroupConditionMonitor, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor_service: typing.Optional[typing.Union[MonitorActionRuleActionGroupConditionMonitorService, typing.Dict[builtins.str, typing.Any]]] = None,
    severity: typing.Optional[typing.Union[MonitorActionRuleActionGroupConditionSeverity, typing.Dict[builtins.str, typing.Any]]] = None,
    target_resource_type: typing.Optional[typing.Union[MonitorActionRuleActionGroupConditionTargetResourceType, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc0914010d5d46edfb10228f0030f261a8351da83b0c4d19e8918d065f64f503(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07c737544b79248c95a9d41e71b935ad3b7a3001e604f6dd693c85d81c18fcf0(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b307a6370334b1283a8000408c0f9456f5790c91dff21494e30e84b376a9fddd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ea6c2fe948baf6d11f029c4057e5ec8a842ac2f021e016ca9b2b03fe2bc8b22(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f1b92cdd65e319b8abfd2315f5d4ea37ee65ff4d47f12eabe625b840a353109(
    value: typing.Optional[MonitorActionRuleActionGroupConditionAlertContext],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88dcb2b643b12bffd69941e5ff0bc6c54815f90356a19833f95806707a8b1fb9(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3e10b34c404fbfb87e62d305be5ae0b461345b8a6054096deeb650b872e8653(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793052f7cf36e437264500313fcd1ac66fedbd3edbdd98351c7ba67e6d2a1c87(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f38a2e5310d3be34c4efd4e8125da9ec4d6732f55d566ce5e3f418debe4ba99b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe212657486c7173b35e211f391081de3239cafdb8e09be9140874202b6dc8b5(
    value: typing.Optional[MonitorActionRuleActionGroupConditionAlertRuleId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75e6f2aab75de4086e12deb3b28e6218a8de4c890ea52ff51f8a23b857e5e5bd(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1457a66f5e503b6d8b2b66ee0e609942b929ccf60959086cc7f6c42ffb5b07a8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c96217d7ef3d69211e4f13750be833f9d87c8b00212e887b9ed252c2daf8549f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8283eabfee2e913bb643bd689fbb2027fa35ca520fe73f263f0bd6ce94f7da6b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b580a40093c905dfa0ad487a1102a6477a622bf23506aeed90e6218824d67665(
    value: typing.Optional[MonitorActionRuleActionGroupConditionDescription],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fd6fd9b335c629f733ac4147ae4d16bf906a5e2a2bab7450f486bdd49e940d1(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ee2e1150b8cdc699d3bcd01501c5369fe055ce7b6853bb62d17fd282f9a9c7a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41760e3e82e6acab1115b6f612408d42e411aae6ac310a4ac475b59c4982cda9(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e13527f15742618114ea0c0748958115ac8a5d76d7aab7db40edcc325cb4789(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a95bb2d8433421b7d8e17ef8befaf07a54bb6242bc8e911a9f229b1487418703(
    value: typing.Optional[MonitorActionRuleActionGroupConditionMonitor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5b1b0580735dad0df50bb50d649a472074da6001113acf474836427be6aa71b(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a98524a3e939c6db971a7e5e2f503b7e44fe1b4ba1d8d137751ccfd886759ae5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10a25c1f6a5a384f09db75a7ee65400dee100592ca7d564d5295bfab86cf2438(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eee534c1f76e08473291f17b72bd5eaa22422b8ee5d869353e66c862a2c3d14(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f226a94addff4afc9d6ebdded1aa9d9bdeca370f6d249b305b7fc48d44a269a(
    value: typing.Optional[MonitorActionRuleActionGroupConditionMonitorService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__45fd2fed910f38aee3ffb66525b32f55b5d37c5110081f8bb0166c1a11853702(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a25ce8416c863b0f32508984cfc8c120f0bfa5b7133d58898058888f0c492663(
    value: typing.Optional[MonitorActionRuleActionGroupCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1bc31d68caa4900f3c6fe84d64c70f3907e7a9fc2305c816ed33a3cbcbe59ca(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0a7076348e3036456f872ed6f13a9e1e0ba43809c38a4ef0b8a3bfd72e3e9a9(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__440fb26a8ee53792f2dba64df6762cd9328b01d131cf145a0c1ca5741094078d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6a30f64b355e67900dc30c3c2247368bea96307e95a2944f054a21c404e81579(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c19bb022ebd3fdb6564f8b89e69d5dd20e4a7a222f66cf19374c4bf23a219e0a(
    value: typing.Optional[MonitorActionRuleActionGroupConditionSeverity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b05b2fe0f47556504fe470ecd84d88fb4bf9c433fc6e7f16f127237e77ca6380(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96fdd269e339b7470ed0d96b99a22bf6de6ebe74e307ec892c8d1907ec8a2398(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1d3a3496bf223760f1279308abad75328120cac713e48682beb150a4b239f5f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cdcff6f467f2afc023438795c49108ccb266f52f31184c6a3e310168169efab(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e08ba7a5ee0b3a3647f1ddf56653d8e27bc45f2c3a7228a17dfea185dd15953(
    value: typing.Optional[MonitorActionRuleActionGroupConditionTargetResourceType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c857432e4a61301db1916e6babc9deabba022e2263730ce34b302a1a438ef1cf(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    action_group_id: builtins.str,
    name: builtins.str,
    resource_group_name: builtins.str,
    condition: typing.Optional[typing.Union[MonitorActionRuleActionGroupCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    scope: typing.Optional[typing.Union[MonitorActionRuleActionGroupScope, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorActionRuleActionGroupTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f2df093186a762e4b63b4a5ac26a0e3aaab166075700d7381807073b1d68f48(
    *,
    resource_ids: typing.Sequence[builtins.str],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c79212b0bd635c7b3529ddbe93d7cfd0576a2ae7537e1341ce2c8cda13b9961(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__888e3eb827ef75599b3074701c804b268b3ffde412b53e11ad3426a8662bbcf4(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f7004f8207a95f7b43338e467d1e71879673d1bc4e97efbf314faf99fa8a44d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c98bda15078df44508d05fb2c8d80fc32abe7ee3bf8d5433a817e51e5ea1d61b(
    value: typing.Optional[MonitorActionRuleActionGroupScope],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__facbd706cc31930677cf910811287238670efe7fde663b661011d21ba882dc14(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3914b2c7d6fcdc8449445b97a9df686272cca3efde1d92db4e9bc9fd34ef3041(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__41ba659e41605eff659970973137dd00bc1219c2ddab02e182246b0777c11e83(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3f9f06dd4f409aad37ef1edeafc70fd5576f66cc34b7ffb4b2e26f603c27ebf(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15647bff539e24bb1be81861e1858ecb0ae212830aa81e9c3e11ff2a15e41cd5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c906b0db4dc365be9004502f5db01fcf01f920a8aa4001d12270e09acddd8eb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__22dc81804ea9a55f039eae3893a089869f40fbe92d5a36c3c0982c6f48b439aa(
    value: typing.Optional[typing.Union[MonitorActionRuleActionGroupTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
