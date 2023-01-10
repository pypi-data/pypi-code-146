'''
# `azurerm_monitor_action_rule_suppression`

Refer to the Terraform Registory for docs: [`azurerm_monitor_action_rule_suppression`](https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression).
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


class MonitorActionRuleSuppression(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppression",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression azurerm_monitor_action_rule_suppression}.'''

    def __init__(
        self,
        scope_: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        name: builtins.str,
        resource_group_name: builtins.str,
        suppression: typing.Union["MonitorActionRuleSuppressionSuppression", typing.Dict[builtins.str, typing.Any]],
        condition: typing.Optional[typing.Union["MonitorActionRuleSuppressionCondition", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        scope: typing.Optional[typing.Union["MonitorActionRuleSuppressionScope", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorActionRuleSuppressionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression azurerm_monitor_action_rule_suppression} Resource.

        :param scope_: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#name MonitorActionRuleSuppression#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#resource_group_name MonitorActionRuleSuppression#resource_group_name}.
        :param suppression: suppression block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#suppression MonitorActionRuleSuppression#suppression}
        :param condition: condition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#condition MonitorActionRuleSuppression#condition}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#description MonitorActionRuleSuppression#description}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#enabled MonitorActionRuleSuppression#enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#id MonitorActionRuleSuppression#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scope: scope block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#scope MonitorActionRuleSuppression#scope}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#tags MonitorActionRuleSuppression#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#timeouts MonitorActionRuleSuppression#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__786605ee84bfeb6453b55fa32008dbb66548c15d6a0c71df5e9dfc9aaf112ed0)
            check_type(argname="argument scope_", value=scope_, expected_type=type_hints["scope_"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitorActionRuleSuppressionConfig(
            name=name,
            resource_group_name=resource_group_name,
            suppression=suppression,
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
        alert_context: typing.Optional[typing.Union["MonitorActionRuleSuppressionConditionAlertContext", typing.Dict[builtins.str, typing.Any]]] = None,
        alert_rule_id: typing.Optional[typing.Union["MonitorActionRuleSuppressionConditionAlertRuleId", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[typing.Union["MonitorActionRuleSuppressionConditionDescription", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor: typing.Optional[typing.Union["MonitorActionRuleSuppressionConditionMonitor", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_service: typing.Optional[typing.Union["MonitorActionRuleSuppressionConditionMonitorService", typing.Dict[builtins.str, typing.Any]]] = None,
        severity: typing.Optional[typing.Union["MonitorActionRuleSuppressionConditionSeverity", typing.Dict[builtins.str, typing.Any]]] = None,
        target_resource_type: typing.Optional[typing.Union["MonitorActionRuleSuppressionConditionTargetResourceType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param alert_context: alert_context block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#alert_context MonitorActionRuleSuppression#alert_context}
        :param alert_rule_id: alert_rule_id block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#alert_rule_id MonitorActionRuleSuppression#alert_rule_id}
        :param description: description block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#description MonitorActionRuleSuppression#description}
        :param monitor: monitor block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#monitor MonitorActionRuleSuppression#monitor}
        :param monitor_service: monitor_service block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#monitor_service MonitorActionRuleSuppression#monitor_service}
        :param severity: severity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#severity MonitorActionRuleSuppression#severity}
        :param target_resource_type: target_resource_type block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#target_resource_type MonitorActionRuleSuppression#target_resource_type}
        '''
        value = MonitorActionRuleSuppressionCondition(
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
        :param resource_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#resource_ids MonitorActionRuleSuppression#resource_ids}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#type MonitorActionRuleSuppression#type}.
        '''
        value = MonitorActionRuleSuppressionScope(resource_ids=resource_ids, type=type)

        return typing.cast(None, jsii.invoke(self, "putScope", [value]))

    @jsii.member(jsii_name="putSuppression")
    def put_suppression(
        self,
        *,
        recurrence_type: builtins.str,
        schedule: typing.Optional[typing.Union["MonitorActionRuleSuppressionSuppressionSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param recurrence_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#recurrence_type MonitorActionRuleSuppression#recurrence_type}.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#schedule MonitorActionRuleSuppression#schedule}
        '''
        value = MonitorActionRuleSuppressionSuppression(
            recurrence_type=recurrence_type, schedule=schedule
        )

        return typing.cast(None, jsii.invoke(self, "putSuppression", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#create MonitorActionRuleSuppression#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#delete MonitorActionRuleSuppression#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#read MonitorActionRuleSuppression#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#update MonitorActionRuleSuppression#update}.
        '''
        value = MonitorActionRuleSuppressionTimeouts(
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
    def condition(self) -> "MonitorActionRuleSuppressionConditionOutputReference":
        return typing.cast("MonitorActionRuleSuppressionConditionOutputReference", jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="scope")
    def scope(self) -> "MonitorActionRuleSuppressionScopeOutputReference":
        return typing.cast("MonitorActionRuleSuppressionScopeOutputReference", jsii.get(self, "scope"))

    @builtins.property
    @jsii.member(jsii_name="suppression")
    def suppression(self) -> "MonitorActionRuleSuppressionSuppressionOutputReference":
        return typing.cast("MonitorActionRuleSuppressionSuppressionOutputReference", jsii.get(self, "suppression"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MonitorActionRuleSuppressionTimeoutsOutputReference":
        return typing.cast("MonitorActionRuleSuppressionTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="conditionInput")
    def condition_input(
        self,
    ) -> typing.Optional["MonitorActionRuleSuppressionCondition"]:
        return typing.cast(typing.Optional["MonitorActionRuleSuppressionCondition"], jsii.get(self, "conditionInput"))

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
    def scope_input(self) -> typing.Optional["MonitorActionRuleSuppressionScope"]:
        return typing.cast(typing.Optional["MonitorActionRuleSuppressionScope"], jsii.get(self, "scopeInput"))

    @builtins.property
    @jsii.member(jsii_name="suppressionInput")
    def suppression_input(
        self,
    ) -> typing.Optional["MonitorActionRuleSuppressionSuppression"]:
        return typing.cast(typing.Optional["MonitorActionRuleSuppressionSuppression"], jsii.get(self, "suppressionInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["MonitorActionRuleSuppressionTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["MonitorActionRuleSuppressionTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__250f1cd04f51c78e9ed4b5887f52047d24b7e2fe5b0a641073325bd8a29d0bc0)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44b4214e25ed276b5337f9831b518d9a65be1dce33df2fe2c2a3ba1ed3b76274)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74f03efbe87929f6023e8d2cbd3c58d7398e23cfca7d36cd592673fd7a6208e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d7c5f886b926f4341597d4345db22c36505d822236575cc8c44a51292914b0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30f9920701ec36084e8438e8e254a657022bd7b56ea334d4094a0d8b193594b6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afea1dcffdcf592a515649ef4ed351cb312f26923900e1364dd297462b505324)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionCondition",
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
class MonitorActionRuleSuppressionCondition:
    def __init__(
        self,
        *,
        alert_context: typing.Optional[typing.Union["MonitorActionRuleSuppressionConditionAlertContext", typing.Dict[builtins.str, typing.Any]]] = None,
        alert_rule_id: typing.Optional[typing.Union["MonitorActionRuleSuppressionConditionAlertRuleId", typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[typing.Union["MonitorActionRuleSuppressionConditionDescription", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor: typing.Optional[typing.Union["MonitorActionRuleSuppressionConditionMonitor", typing.Dict[builtins.str, typing.Any]]] = None,
        monitor_service: typing.Optional[typing.Union["MonitorActionRuleSuppressionConditionMonitorService", typing.Dict[builtins.str, typing.Any]]] = None,
        severity: typing.Optional[typing.Union["MonitorActionRuleSuppressionConditionSeverity", typing.Dict[builtins.str, typing.Any]]] = None,
        target_resource_type: typing.Optional[typing.Union["MonitorActionRuleSuppressionConditionTargetResourceType", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param alert_context: alert_context block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#alert_context MonitorActionRuleSuppression#alert_context}
        :param alert_rule_id: alert_rule_id block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#alert_rule_id MonitorActionRuleSuppression#alert_rule_id}
        :param description: description block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#description MonitorActionRuleSuppression#description}
        :param monitor: monitor block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#monitor MonitorActionRuleSuppression#monitor}
        :param monitor_service: monitor_service block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#monitor_service MonitorActionRuleSuppression#monitor_service}
        :param severity: severity block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#severity MonitorActionRuleSuppression#severity}
        :param target_resource_type: target_resource_type block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#target_resource_type MonitorActionRuleSuppression#target_resource_type}
        '''
        if isinstance(alert_context, dict):
            alert_context = MonitorActionRuleSuppressionConditionAlertContext(**alert_context)
        if isinstance(alert_rule_id, dict):
            alert_rule_id = MonitorActionRuleSuppressionConditionAlertRuleId(**alert_rule_id)
        if isinstance(description, dict):
            description = MonitorActionRuleSuppressionConditionDescription(**description)
        if isinstance(monitor, dict):
            monitor = MonitorActionRuleSuppressionConditionMonitor(**monitor)
        if isinstance(monitor_service, dict):
            monitor_service = MonitorActionRuleSuppressionConditionMonitorService(**monitor_service)
        if isinstance(severity, dict):
            severity = MonitorActionRuleSuppressionConditionSeverity(**severity)
        if isinstance(target_resource_type, dict):
            target_resource_type = MonitorActionRuleSuppressionConditionTargetResourceType(**target_resource_type)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d7ff5e83e341f208337bf9c0fb80c7f144de84fd4e817fa0c51c1f8873b359)
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
    ) -> typing.Optional["MonitorActionRuleSuppressionConditionAlertContext"]:
        '''alert_context block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#alert_context MonitorActionRuleSuppression#alert_context}
        '''
        result = self._values.get("alert_context")
        return typing.cast(typing.Optional["MonitorActionRuleSuppressionConditionAlertContext"], result)

    @builtins.property
    def alert_rule_id(
        self,
    ) -> typing.Optional["MonitorActionRuleSuppressionConditionAlertRuleId"]:
        '''alert_rule_id block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#alert_rule_id MonitorActionRuleSuppression#alert_rule_id}
        '''
        result = self._values.get("alert_rule_id")
        return typing.cast(typing.Optional["MonitorActionRuleSuppressionConditionAlertRuleId"], result)

    @builtins.property
    def description(
        self,
    ) -> typing.Optional["MonitorActionRuleSuppressionConditionDescription"]:
        '''description block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#description MonitorActionRuleSuppression#description}
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional["MonitorActionRuleSuppressionConditionDescription"], result)

    @builtins.property
    def monitor(
        self,
    ) -> typing.Optional["MonitorActionRuleSuppressionConditionMonitor"]:
        '''monitor block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#monitor MonitorActionRuleSuppression#monitor}
        '''
        result = self._values.get("monitor")
        return typing.cast(typing.Optional["MonitorActionRuleSuppressionConditionMonitor"], result)

    @builtins.property
    def monitor_service(
        self,
    ) -> typing.Optional["MonitorActionRuleSuppressionConditionMonitorService"]:
        '''monitor_service block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#monitor_service MonitorActionRuleSuppression#monitor_service}
        '''
        result = self._values.get("monitor_service")
        return typing.cast(typing.Optional["MonitorActionRuleSuppressionConditionMonitorService"], result)

    @builtins.property
    def severity(
        self,
    ) -> typing.Optional["MonitorActionRuleSuppressionConditionSeverity"]:
        '''severity block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#severity MonitorActionRuleSuppression#severity}
        '''
        result = self._values.get("severity")
        return typing.cast(typing.Optional["MonitorActionRuleSuppressionConditionSeverity"], result)

    @builtins.property
    def target_resource_type(
        self,
    ) -> typing.Optional["MonitorActionRuleSuppressionConditionTargetResourceType"]:
        '''target_resource_type block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#target_resource_type MonitorActionRuleSuppression#target_resource_type}
        '''
        result = self._values.get("target_resource_type")
        return typing.cast(typing.Optional["MonitorActionRuleSuppressionConditionTargetResourceType"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleSuppressionCondition(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionConditionAlertContext",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorActionRuleSuppressionConditionAlertContext:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57e37f98d1d162089bb307caefb43c6d7858d92a8af2dd6ce4f84a3b8e62f19d)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleSuppressionConditionAlertContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleSuppressionConditionAlertContextOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionConditionAlertContextOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f39b927be3d92b16d18d2f6f6597d2308bbe3baa72ff2167498e0f12306b0884)
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
            type_hints = typing.get_type_hints(_typecheckingstub__9255a7dd995fbf2868d3840c54dbda1400745c15053e53cf6a0c904feb960e29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54f97d12793b2e2e23c5adc1b22c9ebdbb9b7a65e82fb9f889572d925b8d3772)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorActionRuleSuppressionConditionAlertContext]:
        return typing.cast(typing.Optional[MonitorActionRuleSuppressionConditionAlertContext], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleSuppressionConditionAlertContext],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ae2ed5eb0d3dbc1975b05306696f811d1c30990912934ebac4d73dd090307e61)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionConditionAlertRuleId",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorActionRuleSuppressionConditionAlertRuleId:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e823f2f462317ae27d1b12e45cee7ec716268c94e3389b8db056a674d49e9acc)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleSuppressionConditionAlertRuleId(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleSuppressionConditionAlertRuleIdOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionConditionAlertRuleIdOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__403c232aa5434e47ef6162e75ccfff9a19f43ac7b9e8a6c00212d3ffc4532def)
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
            type_hints = typing.get_type_hints(_typecheckingstub__039c98c8a668d0d9cd118ecf2cdd51060dc5a37bcaa7abfb878f570c7ee05998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a8565ce64509361778b727f7bfdfca405b95f09c317293c6ad0e5232269c3ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorActionRuleSuppressionConditionAlertRuleId]:
        return typing.cast(typing.Optional[MonitorActionRuleSuppressionConditionAlertRuleId], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleSuppressionConditionAlertRuleId],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0759c90fbd9b87337c7c109a5009b020242c48eb510536a6deab97f65f95166)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionConditionDescription",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorActionRuleSuppressionConditionDescription:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d2787165a03845e6c904a0d49a7e8dbcf17b86bc840bbb08a3627a69ec97fec)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleSuppressionConditionDescription(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleSuppressionConditionDescriptionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionConditionDescriptionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__38ba90171e96ace8a587c9a40cd676aa86a8fe504532460393a7f6619fad801a)
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
            type_hints = typing.get_type_hints(_typecheckingstub__70298cc9437e54dcb5521316f5182362d6ea1cb355ea3a13fedb6e38134cfe4a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13fa68177a08c1ccd37bd8a28deeabac3c192fa7cbff6130cce4845900fce96a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorActionRuleSuppressionConditionDescription]:
        return typing.cast(typing.Optional[MonitorActionRuleSuppressionConditionDescription], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleSuppressionConditionDescription],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e74a5ba60d7971f4702f9e45816f5f6e71e502de5274eeec08488d20085d5998)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionConditionMonitor",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorActionRuleSuppressionConditionMonitor:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4faccc6e770a1e56c5f6d0424f18ba9b263974107bb7e5881b8a95836f7eacda)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleSuppressionConditionMonitor(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleSuppressionConditionMonitorOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionConditionMonitorOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__cd02ca6bcbdc00163bc405fd619f177d286b7471b67484e455be183bbefcafe8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__bd50ea26a07258a09e16877aea6bd32033ac368e86df676d780bbe811878e4ac)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c65bd823d1f6bcefe13c599db55b5637126dc72d5ae3d25ae5fc6aa9eb4f3314)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorActionRuleSuppressionConditionMonitor]:
        return typing.cast(typing.Optional[MonitorActionRuleSuppressionConditionMonitor], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleSuppressionConditionMonitor],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05a152df082e42bdaa8f4d0cb8e830c698e730d39256faf37b429218ef50a2de)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionConditionMonitorService",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorActionRuleSuppressionConditionMonitorService:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__03816f27bfd3950d94aeeae4a9e8f4ef5a889d4e113e976196b954036e1a77b1)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleSuppressionConditionMonitorService(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleSuppressionConditionMonitorServiceOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionConditionMonitorServiceOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__adbb84cb487ff92476fee272e3bac983afc31fe45359e2938ac7134059d45741)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f4a76bae8105fc217f22c0553e78fcca5af9f129a05da58c6e29e52881fc2c84)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5751c8b29260c17fd55ddb8c32013d82c410e7ea5cabbf0cb6cf4efd2460068f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorActionRuleSuppressionConditionMonitorService]:
        return typing.cast(typing.Optional[MonitorActionRuleSuppressionConditionMonitorService], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleSuppressionConditionMonitorService],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3272de13ea94e7ab810431d66d4c4d63de5308b960b980e15bb2dcd85dd8607f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitorActionRuleSuppressionConditionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionConditionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__1a963fabe0a778d97ec94ecf9c67ecd4c8447a448bdbff3e89a1380995d11161)
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
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.
        '''
        value = MonitorActionRuleSuppressionConditionAlertContext(
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
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.
        '''
        value = MonitorActionRuleSuppressionConditionAlertRuleId(
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
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.
        '''
        value = MonitorActionRuleSuppressionConditionDescription(
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
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.
        '''
        value = MonitorActionRuleSuppressionConditionMonitor(
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
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.
        '''
        value = MonitorActionRuleSuppressionConditionMonitorService(
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
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.
        '''
        value = MonitorActionRuleSuppressionConditionSeverity(
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
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.
        '''
        value = MonitorActionRuleSuppressionConditionTargetResourceType(
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
    ) -> MonitorActionRuleSuppressionConditionAlertContextOutputReference:
        return typing.cast(MonitorActionRuleSuppressionConditionAlertContextOutputReference, jsii.get(self, "alertContext"))

    @builtins.property
    @jsii.member(jsii_name="alertRuleId")
    def alert_rule_id(
        self,
    ) -> MonitorActionRuleSuppressionConditionAlertRuleIdOutputReference:
        return typing.cast(MonitorActionRuleSuppressionConditionAlertRuleIdOutputReference, jsii.get(self, "alertRuleId"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(
        self,
    ) -> MonitorActionRuleSuppressionConditionDescriptionOutputReference:
        return typing.cast(MonitorActionRuleSuppressionConditionDescriptionOutputReference, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="monitor")
    def monitor(self) -> MonitorActionRuleSuppressionConditionMonitorOutputReference:
        return typing.cast(MonitorActionRuleSuppressionConditionMonitorOutputReference, jsii.get(self, "monitor"))

    @builtins.property
    @jsii.member(jsii_name="monitorService")
    def monitor_service(
        self,
    ) -> MonitorActionRuleSuppressionConditionMonitorServiceOutputReference:
        return typing.cast(MonitorActionRuleSuppressionConditionMonitorServiceOutputReference, jsii.get(self, "monitorService"))

    @builtins.property
    @jsii.member(jsii_name="severity")
    def severity(
        self,
    ) -> "MonitorActionRuleSuppressionConditionSeverityOutputReference":
        return typing.cast("MonitorActionRuleSuppressionConditionSeverityOutputReference", jsii.get(self, "severity"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceType")
    def target_resource_type(
        self,
    ) -> "MonitorActionRuleSuppressionConditionTargetResourceTypeOutputReference":
        return typing.cast("MonitorActionRuleSuppressionConditionTargetResourceTypeOutputReference", jsii.get(self, "targetResourceType"))

    @builtins.property
    @jsii.member(jsii_name="alertContextInput")
    def alert_context_input(
        self,
    ) -> typing.Optional[MonitorActionRuleSuppressionConditionAlertContext]:
        return typing.cast(typing.Optional[MonitorActionRuleSuppressionConditionAlertContext], jsii.get(self, "alertContextInput"))

    @builtins.property
    @jsii.member(jsii_name="alertRuleIdInput")
    def alert_rule_id_input(
        self,
    ) -> typing.Optional[MonitorActionRuleSuppressionConditionAlertRuleId]:
        return typing.cast(typing.Optional[MonitorActionRuleSuppressionConditionAlertRuleId], jsii.get(self, "alertRuleIdInput"))

    @builtins.property
    @jsii.member(jsii_name="descriptionInput")
    def description_input(
        self,
    ) -> typing.Optional[MonitorActionRuleSuppressionConditionDescription]:
        return typing.cast(typing.Optional[MonitorActionRuleSuppressionConditionDescription], jsii.get(self, "descriptionInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorInput")
    def monitor_input(
        self,
    ) -> typing.Optional[MonitorActionRuleSuppressionConditionMonitor]:
        return typing.cast(typing.Optional[MonitorActionRuleSuppressionConditionMonitor], jsii.get(self, "monitorInput"))

    @builtins.property
    @jsii.member(jsii_name="monitorServiceInput")
    def monitor_service_input(
        self,
    ) -> typing.Optional[MonitorActionRuleSuppressionConditionMonitorService]:
        return typing.cast(typing.Optional[MonitorActionRuleSuppressionConditionMonitorService], jsii.get(self, "monitorServiceInput"))

    @builtins.property
    @jsii.member(jsii_name="severityInput")
    def severity_input(
        self,
    ) -> typing.Optional["MonitorActionRuleSuppressionConditionSeverity"]:
        return typing.cast(typing.Optional["MonitorActionRuleSuppressionConditionSeverity"], jsii.get(self, "severityInput"))

    @builtins.property
    @jsii.member(jsii_name="targetResourceTypeInput")
    def target_resource_type_input(
        self,
    ) -> typing.Optional["MonitorActionRuleSuppressionConditionTargetResourceType"]:
        return typing.cast(typing.Optional["MonitorActionRuleSuppressionConditionTargetResourceType"], jsii.get(self, "targetResourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorActionRuleSuppressionCondition]:
        return typing.cast(typing.Optional[MonitorActionRuleSuppressionCondition], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleSuppressionCondition],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd2acfee2031182590a880286f7aeaa0ea18010a61040a0085c0cb78388c7006)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionConditionSeverity",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorActionRuleSuppressionConditionSeverity:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56be2faed2ea0901bebbcdc6cd6d4436c00a1b0d6523642e13f38b78733fcb65)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleSuppressionConditionSeverity(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleSuppressionConditionSeverityOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionConditionSeverityOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0341b43282a35108d87a0ebd3bc5743cb3ca3d64c1f0f4499165b17c9f5c69b4)
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
            type_hints = typing.get_type_hints(_typecheckingstub__6b07a6551f044c1a8aecdb533e22d34ccec88079af2c4ed15fbabfbbb5acfeb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25b2fa75df4d009488ebf5665af418c13de70097174934ceab78f21b03878bf5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorActionRuleSuppressionConditionSeverity]:
        return typing.cast(typing.Optional[MonitorActionRuleSuppressionConditionSeverity], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleSuppressionConditionSeverity],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5aa3d58001f11919e5e8490ec219a1cb5c79c7d43b2c09e3b7f4de3f3193201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionConditionTargetResourceType",
    jsii_struct_bases=[],
    name_mapping={"operator": "operator", "values": "values"},
)
class MonitorActionRuleSuppressionConditionTargetResourceType:
    def __init__(
        self,
        *,
        operator: builtins.str,
        values: typing.Sequence[builtins.str],
    ) -> None:
        '''
        :param operator: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.
        :param values: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bb0743ac0e2cb5a9b3561ac7c229a07971708b365b913b93adf0f58ce5cd2b7)
            check_type(argname="argument operator", value=operator, expected_type=type_hints["operator"])
            check_type(argname="argument values", value=values, expected_type=type_hints["values"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "operator": operator,
            "values": values,
        }

    @builtins.property
    def operator(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#operator MonitorActionRuleSuppression#operator}.'''
        result = self._values.get("operator")
        assert result is not None, "Required property 'operator' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def values(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#values MonitorActionRuleSuppression#values}.'''
        result = self._values.get("values")
        assert result is not None, "Required property 'values' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleSuppressionConditionTargetResourceType(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleSuppressionConditionTargetResourceTypeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionConditionTargetResourceTypeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9caaa13229eb2c2821756e47d84d435fbefc3aa9aeb7f41da5ac7e3b0de44b26)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5b58bef49ed7a428b062af5dde5305d32a71be4ecc61b7ff21813402b320e41a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operator", value)

    @builtins.property
    @jsii.member(jsii_name="values")
    def values(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "values"))

    @values.setter
    def values(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__567b8dd2e8f5977da539ba198e25ede3f28e44621d093186249f8943ada36d12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "values", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorActionRuleSuppressionConditionTargetResourceType]:
        return typing.cast(typing.Optional[MonitorActionRuleSuppressionConditionTargetResourceType], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleSuppressionConditionTargetResourceType],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__271c79938ea64f3ba37dd56d8237aef299599c61dcf375c21b7eb367332f0dae)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "suppression": "suppression",
        "condition": "condition",
        "description": "description",
        "enabled": "enabled",
        "id": "id",
        "scope": "scope",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class MonitorActionRuleSuppressionConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        name: builtins.str,
        resource_group_name: builtins.str,
        suppression: typing.Union["MonitorActionRuleSuppressionSuppression", typing.Dict[builtins.str, typing.Any]],
        condition: typing.Optional[typing.Union[MonitorActionRuleSuppressionCondition, typing.Dict[builtins.str, typing.Any]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        scope: typing.Optional[typing.Union["MonitorActionRuleSuppressionScope", typing.Dict[builtins.str, typing.Any]]] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorActionRuleSuppressionTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#name MonitorActionRuleSuppression#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#resource_group_name MonitorActionRuleSuppression#resource_group_name}.
        :param suppression: suppression block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#suppression MonitorActionRuleSuppression#suppression}
        :param condition: condition block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#condition MonitorActionRuleSuppression#condition}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#description MonitorActionRuleSuppression#description}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#enabled MonitorActionRuleSuppression#enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#id MonitorActionRuleSuppression#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param scope: scope block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#scope MonitorActionRuleSuppression#scope}
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#tags MonitorActionRuleSuppression#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#timeouts MonitorActionRuleSuppression#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(suppression, dict):
            suppression = MonitorActionRuleSuppressionSuppression(**suppression)
        if isinstance(condition, dict):
            condition = MonitorActionRuleSuppressionCondition(**condition)
        if isinstance(scope, dict):
            scope = MonitorActionRuleSuppressionScope(**scope)
        if isinstance(timeouts, dict):
            timeouts = MonitorActionRuleSuppressionTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afa186c05479a499f7c3dc31de8a15827715b0d0bb1bfbac2b346157f72b5dfd)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument suppression", value=suppression, expected_type=type_hints["suppression"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "resource_group_name": resource_group_name,
            "suppression": suppression,
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
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#name MonitorActionRuleSuppression#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#resource_group_name MonitorActionRuleSuppression#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def suppression(self) -> "MonitorActionRuleSuppressionSuppression":
        '''suppression block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#suppression MonitorActionRuleSuppression#suppression}
        '''
        result = self._values.get("suppression")
        assert result is not None, "Required property 'suppression' is missing"
        return typing.cast("MonitorActionRuleSuppressionSuppression", result)

    @builtins.property
    def condition(self) -> typing.Optional[MonitorActionRuleSuppressionCondition]:
        '''condition block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#condition MonitorActionRuleSuppression#condition}
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[MonitorActionRuleSuppressionCondition], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#description MonitorActionRuleSuppression#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#enabled MonitorActionRuleSuppression#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#id MonitorActionRuleSuppression#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional["MonitorActionRuleSuppressionScope"]:
        '''scope block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#scope MonitorActionRuleSuppression#scope}
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional["MonitorActionRuleSuppressionScope"], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#tags MonitorActionRuleSuppression#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MonitorActionRuleSuppressionTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#timeouts MonitorActionRuleSuppression#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MonitorActionRuleSuppressionTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleSuppressionConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionScope",
    jsii_struct_bases=[],
    name_mapping={"resource_ids": "resourceIds", "type": "type"},
)
class MonitorActionRuleSuppressionScope:
    def __init__(
        self,
        *,
        resource_ids: typing.Sequence[builtins.str],
        type: builtins.str,
    ) -> None:
        '''
        :param resource_ids: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#resource_ids MonitorActionRuleSuppression#resource_ids}.
        :param type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#type MonitorActionRuleSuppression#type}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c102a622696f84ad3729133a93c37baaae2e6fca67f1bc99e8bfaf779f28afa7)
            check_type(argname="argument resource_ids", value=resource_ids, expected_type=type_hints["resource_ids"])
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource_ids": resource_ids,
            "type": type,
        }

    @builtins.property
    def resource_ids(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#resource_ids MonitorActionRuleSuppression#resource_ids}.'''
        result = self._values.get("resource_ids")
        assert result is not None, "Required property 'resource_ids' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#type MonitorActionRuleSuppression#type}.'''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleSuppressionScope(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleSuppressionScopeOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionScopeOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__7dcf74e33d4b2aff0d56b323cea1c93cdd0503b1198bc089b2915dd5b1444075)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3d1d9f1c8dde80d416222e2856e8bb567a7efa87c15ac27bea3bc715b763cce8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceIds", value)

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48daeb67102c478fc1318356a96be1e31b8648a50ab4c2cf9a6564bf8fbde773)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorActionRuleSuppressionScope]:
        return typing.cast(typing.Optional[MonitorActionRuleSuppressionScope], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleSuppressionScope],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db7b56ac22b0dfab7fffad027c9376babb464bd344ec85c0ef13a185770c10ba)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionSuppression",
    jsii_struct_bases=[],
    name_mapping={"recurrence_type": "recurrenceType", "schedule": "schedule"},
)
class MonitorActionRuleSuppressionSuppression:
    def __init__(
        self,
        *,
        recurrence_type: builtins.str,
        schedule: typing.Optional[typing.Union["MonitorActionRuleSuppressionSuppressionSchedule", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param recurrence_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#recurrence_type MonitorActionRuleSuppression#recurrence_type}.
        :param schedule: schedule block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#schedule MonitorActionRuleSuppression#schedule}
        '''
        if isinstance(schedule, dict):
            schedule = MonitorActionRuleSuppressionSuppressionSchedule(**schedule)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1832e27846902ba15abbd8a6cc3e32386c4a7ed09b1dd76261d808e1bff6e0e3)
            check_type(argname="argument recurrence_type", value=recurrence_type, expected_type=type_hints["recurrence_type"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "recurrence_type": recurrence_type,
        }
        if schedule is not None:
            self._values["schedule"] = schedule

    @builtins.property
    def recurrence_type(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#recurrence_type MonitorActionRuleSuppression#recurrence_type}.'''
        result = self._values.get("recurrence_type")
        assert result is not None, "Required property 'recurrence_type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def schedule(
        self,
    ) -> typing.Optional["MonitorActionRuleSuppressionSuppressionSchedule"]:
        '''schedule block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#schedule MonitorActionRuleSuppression#schedule}
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional["MonitorActionRuleSuppressionSuppressionSchedule"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleSuppressionSuppression(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleSuppressionSuppressionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionSuppressionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__25ba2b343ed6a937ccd8877522f82706c60e999109eb199b8cbdc9f5724f85b5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putSchedule")
    def put_schedule(
        self,
        *,
        end_date_utc: builtins.str,
        start_date_utc: builtins.str,
        recurrence_monthly: typing.Optional[typing.Sequence[jsii.Number]] = None,
        recurrence_weekly: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param end_date_utc: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#end_date_utc MonitorActionRuleSuppression#end_date_utc}.
        :param start_date_utc: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#start_date_utc MonitorActionRuleSuppression#start_date_utc}.
        :param recurrence_monthly: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#recurrence_monthly MonitorActionRuleSuppression#recurrence_monthly}.
        :param recurrence_weekly: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#recurrence_weekly MonitorActionRuleSuppression#recurrence_weekly}.
        '''
        value = MonitorActionRuleSuppressionSuppressionSchedule(
            end_date_utc=end_date_utc,
            start_date_utc=start_date_utc,
            recurrence_monthly=recurrence_monthly,
            recurrence_weekly=recurrence_weekly,
        )

        return typing.cast(None, jsii.invoke(self, "putSchedule", [value]))

    @jsii.member(jsii_name="resetSchedule")
    def reset_schedule(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSchedule", []))

    @builtins.property
    @jsii.member(jsii_name="schedule")
    def schedule(
        self,
    ) -> "MonitorActionRuleSuppressionSuppressionScheduleOutputReference":
        return typing.cast("MonitorActionRuleSuppressionSuppressionScheduleOutputReference", jsii.get(self, "schedule"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceTypeInput")
    def recurrence_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recurrenceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="scheduleInput")
    def schedule_input(
        self,
    ) -> typing.Optional["MonitorActionRuleSuppressionSuppressionSchedule"]:
        return typing.cast(typing.Optional["MonitorActionRuleSuppressionSuppressionSchedule"], jsii.get(self, "scheduleInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceType")
    def recurrence_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recurrenceType"))

    @recurrence_type.setter
    def recurrence_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fa68505d38f910875721aab6b30b56235d2a7cfd1ad836fe74549a9f825b1762)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrenceType", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorActionRuleSuppressionSuppression]:
        return typing.cast(typing.Optional[MonitorActionRuleSuppressionSuppression], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleSuppressionSuppression],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__075e8e24973eeafcc368b2db24d3419afa83fff22808e2dec6ec47dea442abe0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionSuppressionSchedule",
    jsii_struct_bases=[],
    name_mapping={
        "end_date_utc": "endDateUtc",
        "start_date_utc": "startDateUtc",
        "recurrence_monthly": "recurrenceMonthly",
        "recurrence_weekly": "recurrenceWeekly",
    },
)
class MonitorActionRuleSuppressionSuppressionSchedule:
    def __init__(
        self,
        *,
        end_date_utc: builtins.str,
        start_date_utc: builtins.str,
        recurrence_monthly: typing.Optional[typing.Sequence[jsii.Number]] = None,
        recurrence_weekly: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param end_date_utc: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#end_date_utc MonitorActionRuleSuppression#end_date_utc}.
        :param start_date_utc: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#start_date_utc MonitorActionRuleSuppression#start_date_utc}.
        :param recurrence_monthly: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#recurrence_monthly MonitorActionRuleSuppression#recurrence_monthly}.
        :param recurrence_weekly: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#recurrence_weekly MonitorActionRuleSuppression#recurrence_weekly}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd339b7bbc154ae3f9c06735503d1528d570b72443ea7e99074a763d6dd0b443)
            check_type(argname="argument end_date_utc", value=end_date_utc, expected_type=type_hints["end_date_utc"])
            check_type(argname="argument start_date_utc", value=start_date_utc, expected_type=type_hints["start_date_utc"])
            check_type(argname="argument recurrence_monthly", value=recurrence_monthly, expected_type=type_hints["recurrence_monthly"])
            check_type(argname="argument recurrence_weekly", value=recurrence_weekly, expected_type=type_hints["recurrence_weekly"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "end_date_utc": end_date_utc,
            "start_date_utc": start_date_utc,
        }
        if recurrence_monthly is not None:
            self._values["recurrence_monthly"] = recurrence_monthly
        if recurrence_weekly is not None:
            self._values["recurrence_weekly"] = recurrence_weekly

    @builtins.property
    def end_date_utc(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#end_date_utc MonitorActionRuleSuppression#end_date_utc}.'''
        result = self._values.get("end_date_utc")
        assert result is not None, "Required property 'end_date_utc' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def start_date_utc(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#start_date_utc MonitorActionRuleSuppression#start_date_utc}.'''
        result = self._values.get("start_date_utc")
        assert result is not None, "Required property 'start_date_utc' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def recurrence_monthly(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#recurrence_monthly MonitorActionRuleSuppression#recurrence_monthly}.'''
        result = self._values.get("recurrence_monthly")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def recurrence_weekly(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#recurrence_weekly MonitorActionRuleSuppression#recurrence_weekly}.'''
        result = self._values.get("recurrence_weekly")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleSuppressionSuppressionSchedule(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleSuppressionSuppressionScheduleOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionSuppressionScheduleOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__f694ce4469989642a1d5c6da71df60000a78590858f60c2ac3eff92b1f78feca)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="resetRecurrenceMonthly")
    def reset_recurrence_monthly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurrenceMonthly", []))

    @jsii.member(jsii_name="resetRecurrenceWeekly")
    def reset_recurrence_weekly(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecurrenceWeekly", []))

    @builtins.property
    @jsii.member(jsii_name="endDateUtcInput")
    def end_date_utc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "endDateUtcInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceMonthlyInput")
    def recurrence_monthly_input(self) -> typing.Optional[typing.List[jsii.Number]]:
        return typing.cast(typing.Optional[typing.List[jsii.Number]], jsii.get(self, "recurrenceMonthlyInput"))

    @builtins.property
    @jsii.member(jsii_name="recurrenceWeeklyInput")
    def recurrence_weekly_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "recurrenceWeeklyInput"))

    @builtins.property
    @jsii.member(jsii_name="startDateUtcInput")
    def start_date_utc_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "startDateUtcInput"))

    @builtins.property
    @jsii.member(jsii_name="endDateUtc")
    def end_date_utc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "endDateUtc"))

    @end_date_utc.setter
    def end_date_utc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7823727372f484ef86c64dbe58f769d48df1da4baebb0c2b3fe1c5e0145abf20)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "endDateUtc", value)

    @builtins.property
    @jsii.member(jsii_name="recurrenceMonthly")
    def recurrence_monthly(self) -> typing.List[jsii.Number]:
        return typing.cast(typing.List[jsii.Number], jsii.get(self, "recurrenceMonthly"))

    @recurrence_monthly.setter
    def recurrence_monthly(self, value: typing.List[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb63719f43862cebeafc82d728775b666f2eefbdfc0f6d904a4139f4c9fed6f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrenceMonthly", value)

    @builtins.property
    @jsii.member(jsii_name="recurrenceWeekly")
    def recurrence_weekly(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "recurrenceWeekly"))

    @recurrence_weekly.setter
    def recurrence_weekly(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2eb23f43e379c790865b7cc2c8a333d31fb7d67bd543c2227dc8a8afb6f7f755)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recurrenceWeekly", value)

    @builtins.property
    @jsii.member(jsii_name="startDateUtc")
    def start_date_utc(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "startDateUtc"))

    @start_date_utc.setter
    def start_date_utc(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57c95f5e48f8c750c2160c217e2eaab7a04e26c1560ec5bb7be591bc8cf6ee7c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "startDateUtc", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[MonitorActionRuleSuppressionSuppressionSchedule]:
        return typing.cast(typing.Optional[MonitorActionRuleSuppressionSuppressionSchedule], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActionRuleSuppressionSuppressionSchedule],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d61034b05e1ad4959f453e2a780ff8648317271084a48bf45ec77a21d425a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MonitorActionRuleSuppressionTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#create MonitorActionRuleSuppression#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#delete MonitorActionRuleSuppression#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#read MonitorActionRuleSuppression#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#update MonitorActionRuleSuppression#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3d8158cc020930e2c7ea1a6077088328cd62576db27f399dba0414ecdb163c6)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#create MonitorActionRuleSuppression#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#delete MonitorActionRuleSuppression#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#read MonitorActionRuleSuppression#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_action_rule_suppression#update MonitorActionRuleSuppression#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActionRuleSuppressionTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActionRuleSuppressionTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActionRuleSuppression.MonitorActionRuleSuppressionTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__88f52accf5545fa648c78d880e585865bf1885fba6d76e283a42fd5aa4dca9d3)
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
            type_hints = typing.get_type_hints(_typecheckingstub__64d4b54b98379bd05aa6677fb4435c3b177bfe90c68d749f7ac5ab3cf8e7f387)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e1bff48a78bb958a51fde66a713a6ce70369ff7983321c5676610ee8b4dae0ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__710cfc78cbcfecf759a17823550f6edbc1e794849d8b39c81bcf94ca131ad118)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feb3be387b936e473e83048ce28476bcc176b0303682ea4dd7807ee04c4e006a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitorActionRuleSuppressionTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitorActionRuleSuppressionTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitorActionRuleSuppressionTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25b4121f6a49a9f5b18fe2d3b3778a0dfbb6ef8c7825e9432fa152cbb82f6c30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MonitorActionRuleSuppression",
    "MonitorActionRuleSuppressionCondition",
    "MonitorActionRuleSuppressionConditionAlertContext",
    "MonitorActionRuleSuppressionConditionAlertContextOutputReference",
    "MonitorActionRuleSuppressionConditionAlertRuleId",
    "MonitorActionRuleSuppressionConditionAlertRuleIdOutputReference",
    "MonitorActionRuleSuppressionConditionDescription",
    "MonitorActionRuleSuppressionConditionDescriptionOutputReference",
    "MonitorActionRuleSuppressionConditionMonitor",
    "MonitorActionRuleSuppressionConditionMonitorOutputReference",
    "MonitorActionRuleSuppressionConditionMonitorService",
    "MonitorActionRuleSuppressionConditionMonitorServiceOutputReference",
    "MonitorActionRuleSuppressionConditionOutputReference",
    "MonitorActionRuleSuppressionConditionSeverity",
    "MonitorActionRuleSuppressionConditionSeverityOutputReference",
    "MonitorActionRuleSuppressionConditionTargetResourceType",
    "MonitorActionRuleSuppressionConditionTargetResourceTypeOutputReference",
    "MonitorActionRuleSuppressionConfig",
    "MonitorActionRuleSuppressionScope",
    "MonitorActionRuleSuppressionScopeOutputReference",
    "MonitorActionRuleSuppressionSuppression",
    "MonitorActionRuleSuppressionSuppressionOutputReference",
    "MonitorActionRuleSuppressionSuppressionSchedule",
    "MonitorActionRuleSuppressionSuppressionScheduleOutputReference",
    "MonitorActionRuleSuppressionTimeouts",
    "MonitorActionRuleSuppressionTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__786605ee84bfeb6453b55fa32008dbb66548c15d6a0c71df5e9dfc9aaf112ed0(
    scope_: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    name: builtins.str,
    resource_group_name: builtins.str,
    suppression: typing.Union[MonitorActionRuleSuppressionSuppression, typing.Dict[builtins.str, typing.Any]],
    condition: typing.Optional[typing.Union[MonitorActionRuleSuppressionCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    scope: typing.Optional[typing.Union[MonitorActionRuleSuppressionScope, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorActionRuleSuppressionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__250f1cd04f51c78e9ed4b5887f52047d24b7e2fe5b0a641073325bd8a29d0bc0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44b4214e25ed276b5337f9831b518d9a65be1dce33df2fe2c2a3ba1ed3b76274(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74f03efbe87929f6023e8d2cbd3c58d7398e23cfca7d36cd592673fd7a6208e8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d7c5f886b926f4341597d4345db22c36505d822236575cc8c44a51292914b0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30f9920701ec36084e8438e8e254a657022bd7b56ea334d4094a0d8b193594b6(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afea1dcffdcf592a515649ef4ed351cb312f26923900e1364dd297462b505324(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d7ff5e83e341f208337bf9c0fb80c7f144de84fd4e817fa0c51c1f8873b359(
    *,
    alert_context: typing.Optional[typing.Union[MonitorActionRuleSuppressionConditionAlertContext, typing.Dict[builtins.str, typing.Any]]] = None,
    alert_rule_id: typing.Optional[typing.Union[MonitorActionRuleSuppressionConditionAlertRuleId, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[typing.Union[MonitorActionRuleSuppressionConditionDescription, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor: typing.Optional[typing.Union[MonitorActionRuleSuppressionConditionMonitor, typing.Dict[builtins.str, typing.Any]]] = None,
    monitor_service: typing.Optional[typing.Union[MonitorActionRuleSuppressionConditionMonitorService, typing.Dict[builtins.str, typing.Any]]] = None,
    severity: typing.Optional[typing.Union[MonitorActionRuleSuppressionConditionSeverity, typing.Dict[builtins.str, typing.Any]]] = None,
    target_resource_type: typing.Optional[typing.Union[MonitorActionRuleSuppressionConditionTargetResourceType, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57e37f98d1d162089bb307caefb43c6d7858d92a8af2dd6ce4f84a3b8e62f19d(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f39b927be3d92b16d18d2f6f6597d2308bbe3baa72ff2167498e0f12306b0884(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9255a7dd995fbf2868d3840c54dbda1400745c15053e53cf6a0c904feb960e29(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54f97d12793b2e2e23c5adc1b22c9ebdbb9b7a65e82fb9f889572d925b8d3772(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ae2ed5eb0d3dbc1975b05306696f811d1c30990912934ebac4d73dd090307e61(
    value: typing.Optional[MonitorActionRuleSuppressionConditionAlertContext],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e823f2f462317ae27d1b12e45cee7ec716268c94e3389b8db056a674d49e9acc(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__403c232aa5434e47ef6162e75ccfff9a19f43ac7b9e8a6c00212d3ffc4532def(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__039c98c8a668d0d9cd118ecf2cdd51060dc5a37bcaa7abfb878f570c7ee05998(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a8565ce64509361778b727f7bfdfca405b95f09c317293c6ad0e5232269c3ca(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0759c90fbd9b87337c7c109a5009b020242c48eb510536a6deab97f65f95166(
    value: typing.Optional[MonitorActionRuleSuppressionConditionAlertRuleId],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d2787165a03845e6c904a0d49a7e8dbcf17b86bc840bbb08a3627a69ec97fec(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38ba90171e96ace8a587c9a40cd676aa86a8fe504532460393a7f6619fad801a(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70298cc9437e54dcb5521316f5182362d6ea1cb355ea3a13fedb6e38134cfe4a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13fa68177a08c1ccd37bd8a28deeabac3c192fa7cbff6130cce4845900fce96a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e74a5ba60d7971f4702f9e45816f5f6e71e502de5274eeec08488d20085d5998(
    value: typing.Optional[MonitorActionRuleSuppressionConditionDescription],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4faccc6e770a1e56c5f6d0424f18ba9b263974107bb7e5881b8a95836f7eacda(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd02ca6bcbdc00163bc405fd619f177d286b7471b67484e455be183bbefcafe8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd50ea26a07258a09e16877aea6bd32033ac368e86df676d780bbe811878e4ac(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c65bd823d1f6bcefe13c599db55b5637126dc72d5ae3d25ae5fc6aa9eb4f3314(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05a152df082e42bdaa8f4d0cb8e830c698e730d39256faf37b429218ef50a2de(
    value: typing.Optional[MonitorActionRuleSuppressionConditionMonitor],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__03816f27bfd3950d94aeeae4a9e8f4ef5a889d4e113e976196b954036e1a77b1(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adbb84cb487ff92476fee272e3bac983afc31fe45359e2938ac7134059d45741(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f4a76bae8105fc217f22c0553e78fcca5af9f129a05da58c6e29e52881fc2c84(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5751c8b29260c17fd55ddb8c32013d82c410e7ea5cabbf0cb6cf4efd2460068f(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3272de13ea94e7ab810431d66d4c4d63de5308b960b980e15bb2dcd85dd8607f(
    value: typing.Optional[MonitorActionRuleSuppressionConditionMonitorService],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a963fabe0a778d97ec94ecf9c67ecd4c8447a448bdbff3e89a1380995d11161(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd2acfee2031182590a880286f7aeaa0ea18010a61040a0085c0cb78388c7006(
    value: typing.Optional[MonitorActionRuleSuppressionCondition],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56be2faed2ea0901bebbcdc6cd6d4436c00a1b0d6523642e13f38b78733fcb65(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0341b43282a35108d87a0ebd3bc5743cb3ca3d64c1f0f4499165b17c9f5c69b4(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b07a6551f044c1a8aecdb533e22d34ccec88079af2c4ed15fbabfbbb5acfeb5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b2fa75df4d009488ebf5665af418c13de70097174934ceab78f21b03878bf5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5aa3d58001f11919e5e8490ec219a1cb5c79c7d43b2c09e3b7f4de3f3193201(
    value: typing.Optional[MonitorActionRuleSuppressionConditionSeverity],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bb0743ac0e2cb5a9b3561ac7c229a07971708b365b913b93adf0f58ce5cd2b7(
    *,
    operator: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9caaa13229eb2c2821756e47d84d435fbefc3aa9aeb7f41da5ac7e3b0de44b26(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b58bef49ed7a428b062af5dde5305d32a71be4ecc61b7ff21813402b320e41a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__567b8dd2e8f5977da539ba198e25ede3f28e44621d093186249f8943ada36d12(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271c79938ea64f3ba37dd56d8237aef299599c61dcf375c21b7eb367332f0dae(
    value: typing.Optional[MonitorActionRuleSuppressionConditionTargetResourceType],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afa186c05479a499f7c3dc31de8a15827715b0d0bb1bfbac2b346157f72b5dfd(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    name: builtins.str,
    resource_group_name: builtins.str,
    suppression: typing.Union[MonitorActionRuleSuppressionSuppression, typing.Dict[builtins.str, typing.Any]],
    condition: typing.Optional[typing.Union[MonitorActionRuleSuppressionCondition, typing.Dict[builtins.str, typing.Any]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    scope: typing.Optional[typing.Union[MonitorActionRuleSuppressionScope, typing.Dict[builtins.str, typing.Any]]] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorActionRuleSuppressionTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c102a622696f84ad3729133a93c37baaae2e6fca67f1bc99e8bfaf779f28afa7(
    *,
    resource_ids: typing.Sequence[builtins.str],
    type: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dcf74e33d4b2aff0d56b323cea1c93cdd0503b1198bc089b2915dd5b1444075(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d1d9f1c8dde80d416222e2856e8bb567a7efa87c15ac27bea3bc715b763cce8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48daeb67102c478fc1318356a96be1e31b8648a50ab4c2cf9a6564bf8fbde773(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db7b56ac22b0dfab7fffad027c9376babb464bd344ec85c0ef13a185770c10ba(
    value: typing.Optional[MonitorActionRuleSuppressionScope],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1832e27846902ba15abbd8a6cc3e32386c4a7ed09b1dd76261d808e1bff6e0e3(
    *,
    recurrence_type: builtins.str,
    schedule: typing.Optional[typing.Union[MonitorActionRuleSuppressionSuppressionSchedule, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25ba2b343ed6a937ccd8877522f82706c60e999109eb199b8cbdc9f5724f85b5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa68505d38f910875721aab6b30b56235d2a7cfd1ad836fe74549a9f825b1762(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__075e8e24973eeafcc368b2db24d3419afa83fff22808e2dec6ec47dea442abe0(
    value: typing.Optional[MonitorActionRuleSuppressionSuppression],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd339b7bbc154ae3f9c06735503d1528d570b72443ea7e99074a763d6dd0b443(
    *,
    end_date_utc: builtins.str,
    start_date_utc: builtins.str,
    recurrence_monthly: typing.Optional[typing.Sequence[jsii.Number]] = None,
    recurrence_weekly: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f694ce4469989642a1d5c6da71df60000a78590858f60c2ac3eff92b1f78feca(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7823727372f484ef86c64dbe58f769d48df1da4baebb0c2b3fe1c5e0145abf20(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb63719f43862cebeafc82d728775b666f2eefbdfc0f6d904a4139f4c9fed6f0(
    value: typing.List[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2eb23f43e379c790865b7cc2c8a333d31fb7d67bd543c2227dc8a8afb6f7f755(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57c95f5e48f8c750c2160c217e2eaab7a04e26c1560ec5bb7be591bc8cf6ee7c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d61034b05e1ad4959f453e2a780ff8648317271084a48bf45ec77a21d425a5(
    value: typing.Optional[MonitorActionRuleSuppressionSuppressionSchedule],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3d8158cc020930e2c7ea1a6077088328cd62576db27f399dba0414ecdb163c6(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88f52accf5545fa648c78d880e585865bf1885fba6d76e283a42fd5aa4dca9d3(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64d4b54b98379bd05aa6677fb4435c3b177bfe90c68d749f7ac5ab3cf8e7f387(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e1bff48a78bb958a51fde66a713a6ce70369ff7983321c5676610ee8b4dae0ef(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__710cfc78cbcfecf759a17823550f6edbc1e794849d8b39c81bcf94ca131ad118(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feb3be387b936e473e83048ce28476bcc176b0303682ea4dd7807ee04c4e006a(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25b4121f6a49a9f5b18fe2d3b3778a0dfbb6ef8c7825e9432fa152cbb82f6c30(
    value: typing.Optional[typing.Union[MonitorActionRuleSuppressionTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
