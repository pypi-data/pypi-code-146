'''
# `azurerm_monitor_activity_log_alert`

Refer to the Terraform Registory for docs: [`azurerm_monitor_activity_log_alert`](https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert).
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


class MonitorActivityLogAlert(
    _cdktf_9a9027ec.TerraformResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActivityLogAlert.MonitorActivityLogAlert",
):
    '''Represents a {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert azurerm_monitor_activity_log_alert}.'''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id_: builtins.str,
        *,
        criteria: typing.Union["MonitorActivityLogAlertCriteria", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        resource_group_name: builtins.str,
        scopes: typing.Sequence[builtins.str],
        action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActivityLogAlertAction", typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorActivityLogAlertTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
        connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
        count: typing.Optional[jsii.Number] = None,
        depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
        for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
        lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
        provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
        provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    ) -> None:
        '''Create a new {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert azurerm_monitor_activity_log_alert} Resource.

        :param scope: The scope in which to define this construct.
        :param id_: The scoped construct ID. Must be unique amongst siblings in the same scope
        :param criteria: criteria block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#criteria MonitorActivityLogAlert#criteria}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#name MonitorActivityLogAlert#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_group_name MonitorActivityLogAlert#resource_group_name}.
        :param scopes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#scopes MonitorActivityLogAlert#scopes}.
        :param action: action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#action MonitorActivityLogAlert#action}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#description MonitorActivityLogAlert#description}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#enabled MonitorActivityLogAlert#enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#id MonitorActivityLogAlert#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#tags MonitorActivityLogAlert#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#timeouts MonitorActivityLogAlert#timeouts}
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5079e60d877e29323ba976c824f1af2acc540815bc0d4292e57746d6c197ef5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id_", value=id_, expected_type=type_hints["id_"])
        config = MonitorActivityLogAlertConfig(
            criteria=criteria,
            name=name,
            resource_group_name=resource_group_name,
            scopes=scopes,
            action=action,
            description=description,
            enabled=enabled,
            id=id,
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

        jsii.create(self.__class__, self, [scope, id_, config])

    @jsii.member(jsii_name="putAction")
    def put_action(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActivityLogAlertAction", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d11bdfdf50a69aeb959b08a3ea03a1e980a76fa4ca436c34dda46e3befc4d72e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putAction", [value]))

    @jsii.member(jsii_name="putCriteria")
    def put_criteria(
        self,
        *,
        category: builtins.str,
        caller: typing.Optional[builtins.str] = None,
        level: typing.Optional[builtins.str] = None,
        operation_name: typing.Optional[builtins.str] = None,
        recommendation_category: typing.Optional[builtins.str] = None,
        recommendation_impact: typing.Optional[builtins.str] = None,
        recommendation_type: typing.Optional[builtins.str] = None,
        resource_group: typing.Optional[builtins.str] = None,
        resource_health: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActivityLogAlertCriteriaResourceHealth", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_id: typing.Optional[builtins.str] = None,
        resource_provider: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[builtins.str] = None,
        service_health: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActivityLogAlertCriteriaServiceHealth", typing.Dict[builtins.str, typing.Any]]]]] = None,
        status: typing.Optional[builtins.str] = None,
        sub_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param category: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#category MonitorActivityLogAlert#category}.
        :param caller: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#caller MonitorActivityLogAlert#caller}.
        :param level: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#level MonitorActivityLogAlert#level}.
        :param operation_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#operation_name MonitorActivityLogAlert#operation_name}.
        :param recommendation_category: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#recommendation_category MonitorActivityLogAlert#recommendation_category}.
        :param recommendation_impact: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#recommendation_impact MonitorActivityLogAlert#recommendation_impact}.
        :param recommendation_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#recommendation_type MonitorActivityLogAlert#recommendation_type}.
        :param resource_group: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_group MonitorActivityLogAlert#resource_group}.
        :param resource_health: resource_health block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_health MonitorActivityLogAlert#resource_health}
        :param resource_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_id MonitorActivityLogAlert#resource_id}.
        :param resource_provider: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_provider MonitorActivityLogAlert#resource_provider}.
        :param resource_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_type MonitorActivityLogAlert#resource_type}.
        :param service_health: service_health block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#service_health MonitorActivityLogAlert#service_health}
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#status MonitorActivityLogAlert#status}.
        :param sub_status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#sub_status MonitorActivityLogAlert#sub_status}.
        '''
        value = MonitorActivityLogAlertCriteria(
            category=category,
            caller=caller,
            level=level,
            operation_name=operation_name,
            recommendation_category=recommendation_category,
            recommendation_impact=recommendation_impact,
            recommendation_type=recommendation_type,
            resource_group=resource_group,
            resource_health=resource_health,
            resource_id=resource_id,
            resource_provider=resource_provider,
            resource_type=resource_type,
            service_health=service_health,
            status=status,
            sub_status=sub_status,
        )

        return typing.cast(None, jsii.invoke(self, "putCriteria", [value]))

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
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#create MonitorActivityLogAlert#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#delete MonitorActivityLogAlert#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#read MonitorActivityLogAlert#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#update MonitorActivityLogAlert#update}.
        '''
        value = MonitorActivityLogAlertTimeouts(
            create=create, delete=delete, read=read, update=update
        )

        return typing.cast(None, jsii.invoke(self, "putTimeouts", [value]))

    @jsii.member(jsii_name="resetAction")
    def reset_action(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetAction", []))

    @jsii.member(jsii_name="resetDescription")
    def reset_description(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetDescription", []))

    @jsii.member(jsii_name="resetEnabled")
    def reset_enabled(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEnabled", []))

    @jsii.member(jsii_name="resetId")
    def reset_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetId", []))

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
    @jsii.member(jsii_name="action")
    def action(self) -> "MonitorActivityLogAlertActionList":
        return typing.cast("MonitorActivityLogAlertActionList", jsii.get(self, "action"))

    @builtins.property
    @jsii.member(jsii_name="criteria")
    def criteria(self) -> "MonitorActivityLogAlertCriteriaOutputReference":
        return typing.cast("MonitorActivityLogAlertCriteriaOutputReference", jsii.get(self, "criteria"))

    @builtins.property
    @jsii.member(jsii_name="timeouts")
    def timeouts(self) -> "MonitorActivityLogAlertTimeoutsOutputReference":
        return typing.cast("MonitorActivityLogAlertTimeoutsOutputReference", jsii.get(self, "timeouts"))

    @builtins.property
    @jsii.member(jsii_name="actionInput")
    def action_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActivityLogAlertAction"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActivityLogAlertAction"]]], jsii.get(self, "actionInput"))

    @builtins.property
    @jsii.member(jsii_name="criteriaInput")
    def criteria_input(self) -> typing.Optional["MonitorActivityLogAlertCriteria"]:
        return typing.cast(typing.Optional["MonitorActivityLogAlertCriteria"], jsii.get(self, "criteriaInput"))

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
    @jsii.member(jsii_name="scopesInput")
    def scopes_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "scopesInput"))

    @builtins.property
    @jsii.member(jsii_name="tagsInput")
    def tags_input(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "tagsInput"))

    @builtins.property
    @jsii.member(jsii_name="timeoutsInput")
    def timeouts_input(
        self,
    ) -> typing.Optional[typing.Union["MonitorActivityLogAlertTimeouts", _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union["MonitorActivityLogAlertTimeouts", _cdktf_9a9027ec.IResolvable]], jsii.get(self, "timeoutsInput"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9e5fd804e6f68e06a57a4049e35362e8b491443f97342cc2ebc98e92666d9d64)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ef208f0cf1bcd015d084b181edcc90dae55c6835d6d9d208b864ae3cffd1917d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enabled", value)

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @id.setter
    def id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__458fe4f0f3468ab45ba869cf25fef9968aeb279e71c83c9d4a579cf67e66309d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "id", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__89637ba4c007b2a524d1d2f13e8419d08a8d417e2ba6c78c9b632c16f4a07815)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroupName")
    def resource_group_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroupName"))

    @resource_group_name.setter
    def resource_group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8706d8720948b555a1756590aeafa7fba9276cb4c1217f9b2361f84d08abc7b4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroupName", value)

    @builtins.property
    @jsii.member(jsii_name="scopes")
    def scopes(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "scopes"))

    @scopes.setter
    def scopes(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71d71709acbc9024ff2465e6dabdfb99ac6f4d011dbfad76c1306e3a8065199b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "scopes", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @tags.setter
    def tags(self, value: typing.Mapping[builtins.str, builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__abf00bba8d0b87bc26f1aa393775f7bcff50d6e26b6ee749da60e7364ae25c52)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActivityLogAlert.MonitorActivityLogAlertAction",
    jsii_struct_bases=[],
    name_mapping={
        "action_group_id": "actionGroupId",
        "webhook_properties": "webhookProperties",
    },
)
class MonitorActivityLogAlertAction:
    def __init__(
        self,
        *,
        action_group_id: builtins.str,
        webhook_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param action_group_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#action_group_id MonitorActivityLogAlert#action_group_id}.
        :param webhook_properties: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#webhook_properties MonitorActivityLogAlert#webhook_properties}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183da7fc40dc5cd38056b9861df054fa94f0a97d4952ba4f9eef1c436e92b6d8)
            check_type(argname="argument action_group_id", value=action_group_id, expected_type=type_hints["action_group_id"])
            check_type(argname="argument webhook_properties", value=webhook_properties, expected_type=type_hints["webhook_properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_group_id": action_group_id,
        }
        if webhook_properties is not None:
            self._values["webhook_properties"] = webhook_properties

    @builtins.property
    def action_group_id(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#action_group_id MonitorActivityLogAlert#action_group_id}.'''
        result = self._values.get("action_group_id")
        assert result is not None, "Required property 'action_group_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def webhook_properties(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#webhook_properties MonitorActivityLogAlert#webhook_properties}.'''
        result = self._values.get("webhook_properties")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActivityLogAlertAction(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActivityLogAlertActionList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActivityLogAlert.MonitorActivityLogAlertActionList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__0a061e56d7439f0e76b40af5a7049736c6509fb705908b7dfd547d0ec2dc6fa2)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(self, index: jsii.Number) -> "MonitorActivityLogAlertActionOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e5572846c25d5035d30ddf7a470d1a1834633c51deab1d0cb359ce7286b6f62)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorActivityLogAlertActionOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf4e2d097787e27071ddaf44b5bfed276055f4a0a0068e2110dca443687473c1)
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
            type_hints = typing.get_type_hints(_typecheckingstub__499e314ca537cba0d36c28b9c771bbe865e48af750db6ffab29c80e4315df6cc)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7d2210770b9ec9620952590438b0a2173969acd4deed5cac14d4f71a26963ae4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActivityLogAlertAction]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActivityLogAlertAction]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActivityLogAlertAction]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1311cf83d8766cf31c969b7aabc7d69737ffa04f659846b4c13fa0685a799b9b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitorActivityLogAlertActionOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActivityLogAlert.MonitorActivityLogAlertActionOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__a90cae928f6a91f72e30aaf6cb23ea1a879a2125b891f488c0a2cce853ce8903)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetWebhookProperties")
    def reset_webhook_properties(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetWebhookProperties", []))

    @builtins.property
    @jsii.member(jsii_name="actionGroupIdInput")
    def action_group_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "actionGroupIdInput"))

    @builtins.property
    @jsii.member(jsii_name="webhookPropertiesInput")
    def webhook_properties_input(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], jsii.get(self, "webhookPropertiesInput"))

    @builtins.property
    @jsii.member(jsii_name="actionGroupId")
    def action_group_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "actionGroupId"))

    @action_group_id.setter
    def action_group_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44e1896e6844fa475f61715e46bac10b93768e07e37d9aed3f8a8581cc7da792)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actionGroupId", value)

    @builtins.property
    @jsii.member(jsii_name="webhookProperties")
    def webhook_properties(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "webhookProperties"))

    @webhook_properties.setter
    def webhook_properties(
        self,
        value: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__feba7b1efbd55e1e0634c997176df18d1f680ab59494b3a50b7047677802d0e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "webhookProperties", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitorActivityLogAlertAction, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitorActivityLogAlertAction, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitorActivityLogAlertAction, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__96041d5665f99ca8e390a1e48d34a1724e588c3d24e4aa14beaf527dabcb26b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActivityLogAlert.MonitorActivityLogAlertConfig",
    jsii_struct_bases=[_cdktf_9a9027ec.TerraformMetaArguments],
    name_mapping={
        "connection": "connection",
        "count": "count",
        "depends_on": "dependsOn",
        "for_each": "forEach",
        "lifecycle": "lifecycle",
        "provider": "provider",
        "provisioners": "provisioners",
        "criteria": "criteria",
        "name": "name",
        "resource_group_name": "resourceGroupName",
        "scopes": "scopes",
        "action": "action",
        "description": "description",
        "enabled": "enabled",
        "id": "id",
        "tags": "tags",
        "timeouts": "timeouts",
    },
)
class MonitorActivityLogAlertConfig(_cdktf_9a9027ec.TerraformMetaArguments):
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
        criteria: typing.Union["MonitorActivityLogAlertCriteria", typing.Dict[builtins.str, typing.Any]],
        name: builtins.str,
        resource_group_name: builtins.str,
        scopes: typing.Sequence[builtins.str],
        action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActivityLogAlertAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
        id: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        timeouts: typing.Optional[typing.Union["MonitorActivityLogAlertTimeouts", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param connection: 
        :param count: 
        :param depends_on: 
        :param for_each: 
        :param lifecycle: 
        :param provider: 
        :param provisioners: 
        :param criteria: criteria block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#criteria MonitorActivityLogAlert#criteria}
        :param name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#name MonitorActivityLogAlert#name}.
        :param resource_group_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_group_name MonitorActivityLogAlert#resource_group_name}.
        :param scopes: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#scopes MonitorActivityLogAlert#scopes}.
        :param action: action block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#action MonitorActivityLogAlert#action}
        :param description: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#description MonitorActivityLogAlert#description}.
        :param enabled: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#enabled MonitorActivityLogAlert#enabled}.
        :param id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#id MonitorActivityLogAlert#id}. Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2. If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        :param tags: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#tags MonitorActivityLogAlert#tags}.
        :param timeouts: timeouts block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#timeouts MonitorActivityLogAlert#timeouts}
        '''
        if isinstance(lifecycle, dict):
            lifecycle = _cdktf_9a9027ec.TerraformResourceLifecycle(**lifecycle)
        if isinstance(criteria, dict):
            criteria = MonitorActivityLogAlertCriteria(**criteria)
        if isinstance(timeouts, dict):
            timeouts = MonitorActivityLogAlertTimeouts(**timeouts)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdc524144ca3109bf63d45a6e23b94dfe0b1404ea0bc4b68e9d86e3361b8e3c3)
            check_type(argname="argument connection", value=connection, expected_type=type_hints["connection"])
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
            check_type(argname="argument depends_on", value=depends_on, expected_type=type_hints["depends_on"])
            check_type(argname="argument for_each", value=for_each, expected_type=type_hints["for_each"])
            check_type(argname="argument lifecycle", value=lifecycle, expected_type=type_hints["lifecycle"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument provisioners", value=provisioners, expected_type=type_hints["provisioners"])
            check_type(argname="argument criteria", value=criteria, expected_type=type_hints["criteria"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_group_name", value=resource_group_name, expected_type=type_hints["resource_group_name"])
            check_type(argname="argument scopes", value=scopes, expected_type=type_hints["scopes"])
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument timeouts", value=timeouts, expected_type=type_hints["timeouts"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "criteria": criteria,
            "name": name,
            "resource_group_name": resource_group_name,
            "scopes": scopes,
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
        if action is not None:
            self._values["action"] = action
        if description is not None:
            self._values["description"] = description
        if enabled is not None:
            self._values["enabled"] = enabled
        if id is not None:
            self._values["id"] = id
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
    def criteria(self) -> "MonitorActivityLogAlertCriteria":
        '''criteria block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#criteria MonitorActivityLogAlert#criteria}
        '''
        result = self._values.get("criteria")
        assert result is not None, "Required property 'criteria' is missing"
        return typing.cast("MonitorActivityLogAlertCriteria", result)

    @builtins.property
    def name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#name MonitorActivityLogAlert#name}.'''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_group_name(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_group_name MonitorActivityLogAlert#resource_group_name}.'''
        result = self._values.get("resource_group_name")
        assert result is not None, "Required property 'resource_group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def scopes(self) -> typing.List[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#scopes MonitorActivityLogAlert#scopes}.'''
        result = self._values.get("scopes")
        assert result is not None, "Required property 'scopes' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def action(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActivityLogAlertAction]]]:
        '''action block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#action MonitorActivityLogAlert#action}
        '''
        result = self._values.get("action")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActivityLogAlertAction]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#description MonitorActivityLogAlert#description}.'''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enabled(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#enabled MonitorActivityLogAlert#enabled}.'''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#id MonitorActivityLogAlert#id}.

        Please be aware that the id field is automatically added to all resources in Terraform providers using a Terraform provider SDK version below 2.
        If you experience problems setting this value it might not be settable. Please take a look at the provider documentation to ensure it should be settable.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#tags MonitorActivityLogAlert#tags}.'''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def timeouts(self) -> typing.Optional["MonitorActivityLogAlertTimeouts"]:
        '''timeouts block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#timeouts MonitorActivityLogAlert#timeouts}
        '''
        result = self._values.get("timeouts")
        return typing.cast(typing.Optional["MonitorActivityLogAlertTimeouts"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActivityLogAlertConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActivityLogAlert.MonitorActivityLogAlertCriteria",
    jsii_struct_bases=[],
    name_mapping={
        "category": "category",
        "caller": "caller",
        "level": "level",
        "operation_name": "operationName",
        "recommendation_category": "recommendationCategory",
        "recommendation_impact": "recommendationImpact",
        "recommendation_type": "recommendationType",
        "resource_group": "resourceGroup",
        "resource_health": "resourceHealth",
        "resource_id": "resourceId",
        "resource_provider": "resourceProvider",
        "resource_type": "resourceType",
        "service_health": "serviceHealth",
        "status": "status",
        "sub_status": "subStatus",
    },
)
class MonitorActivityLogAlertCriteria:
    def __init__(
        self,
        *,
        category: builtins.str,
        caller: typing.Optional[builtins.str] = None,
        level: typing.Optional[builtins.str] = None,
        operation_name: typing.Optional[builtins.str] = None,
        recommendation_category: typing.Optional[builtins.str] = None,
        recommendation_impact: typing.Optional[builtins.str] = None,
        recommendation_type: typing.Optional[builtins.str] = None,
        resource_group: typing.Optional[builtins.str] = None,
        resource_health: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActivityLogAlertCriteriaResourceHealth", typing.Dict[builtins.str, typing.Any]]]]] = None,
        resource_id: typing.Optional[builtins.str] = None,
        resource_provider: typing.Optional[builtins.str] = None,
        resource_type: typing.Optional[builtins.str] = None,
        service_health: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActivityLogAlertCriteriaServiceHealth", typing.Dict[builtins.str, typing.Any]]]]] = None,
        status: typing.Optional[builtins.str] = None,
        sub_status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param category: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#category MonitorActivityLogAlert#category}.
        :param caller: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#caller MonitorActivityLogAlert#caller}.
        :param level: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#level MonitorActivityLogAlert#level}.
        :param operation_name: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#operation_name MonitorActivityLogAlert#operation_name}.
        :param recommendation_category: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#recommendation_category MonitorActivityLogAlert#recommendation_category}.
        :param recommendation_impact: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#recommendation_impact MonitorActivityLogAlert#recommendation_impact}.
        :param recommendation_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#recommendation_type MonitorActivityLogAlert#recommendation_type}.
        :param resource_group: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_group MonitorActivityLogAlert#resource_group}.
        :param resource_health: resource_health block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_health MonitorActivityLogAlert#resource_health}
        :param resource_id: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_id MonitorActivityLogAlert#resource_id}.
        :param resource_provider: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_provider MonitorActivityLogAlert#resource_provider}.
        :param resource_type: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_type MonitorActivityLogAlert#resource_type}.
        :param service_health: service_health block. Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#service_health MonitorActivityLogAlert#service_health}
        :param status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#status MonitorActivityLogAlert#status}.
        :param sub_status: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#sub_status MonitorActivityLogAlert#sub_status}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9c680eca68f55118237d8e04f64deba0ecc901ccc77adb441a06d4edf79b0294)
            check_type(argname="argument category", value=category, expected_type=type_hints["category"])
            check_type(argname="argument caller", value=caller, expected_type=type_hints["caller"])
            check_type(argname="argument level", value=level, expected_type=type_hints["level"])
            check_type(argname="argument operation_name", value=operation_name, expected_type=type_hints["operation_name"])
            check_type(argname="argument recommendation_category", value=recommendation_category, expected_type=type_hints["recommendation_category"])
            check_type(argname="argument recommendation_impact", value=recommendation_impact, expected_type=type_hints["recommendation_impact"])
            check_type(argname="argument recommendation_type", value=recommendation_type, expected_type=type_hints["recommendation_type"])
            check_type(argname="argument resource_group", value=resource_group, expected_type=type_hints["resource_group"])
            check_type(argname="argument resource_health", value=resource_health, expected_type=type_hints["resource_health"])
            check_type(argname="argument resource_id", value=resource_id, expected_type=type_hints["resource_id"])
            check_type(argname="argument resource_provider", value=resource_provider, expected_type=type_hints["resource_provider"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument service_health", value=service_health, expected_type=type_hints["service_health"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument sub_status", value=sub_status, expected_type=type_hints["sub_status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "category": category,
        }
        if caller is not None:
            self._values["caller"] = caller
        if level is not None:
            self._values["level"] = level
        if operation_name is not None:
            self._values["operation_name"] = operation_name
        if recommendation_category is not None:
            self._values["recommendation_category"] = recommendation_category
        if recommendation_impact is not None:
            self._values["recommendation_impact"] = recommendation_impact
        if recommendation_type is not None:
            self._values["recommendation_type"] = recommendation_type
        if resource_group is not None:
            self._values["resource_group"] = resource_group
        if resource_health is not None:
            self._values["resource_health"] = resource_health
        if resource_id is not None:
            self._values["resource_id"] = resource_id
        if resource_provider is not None:
            self._values["resource_provider"] = resource_provider
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if service_health is not None:
            self._values["service_health"] = service_health
        if status is not None:
            self._values["status"] = status
        if sub_status is not None:
            self._values["sub_status"] = sub_status

    @builtins.property
    def category(self) -> builtins.str:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#category MonitorActivityLogAlert#category}.'''
        result = self._values.get("category")
        assert result is not None, "Required property 'category' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def caller(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#caller MonitorActivityLogAlert#caller}.'''
        result = self._values.get("caller")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def level(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#level MonitorActivityLogAlert#level}.'''
        result = self._values.get("level")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def operation_name(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#operation_name MonitorActivityLogAlert#operation_name}.'''
        result = self._values.get("operation_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recommendation_category(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#recommendation_category MonitorActivityLogAlert#recommendation_category}.'''
        result = self._values.get("recommendation_category")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recommendation_impact(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#recommendation_impact MonitorActivityLogAlert#recommendation_impact}.'''
        result = self._values.get("recommendation_impact")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def recommendation_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#recommendation_type MonitorActivityLogAlert#recommendation_type}.'''
        result = self._values.get("recommendation_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_group(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_group MonitorActivityLogAlert#resource_group}.'''
        result = self._values.get("resource_group")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_health(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActivityLogAlertCriteriaResourceHealth"]]]:
        '''resource_health block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_health MonitorActivityLogAlert#resource_health}
        '''
        result = self._values.get("resource_health")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActivityLogAlertCriteriaResourceHealth"]]], result)

    @builtins.property
    def resource_id(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_id MonitorActivityLogAlert#resource_id}.'''
        result = self._values.get("resource_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_provider(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_provider MonitorActivityLogAlert#resource_provider}.'''
        result = self._values.get("resource_provider")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#resource_type MonitorActivityLogAlert#resource_type}.'''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_health(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActivityLogAlertCriteriaServiceHealth"]]]:
        '''service_health block.

        Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#service_health MonitorActivityLogAlert#service_health}
        '''
        result = self._values.get("service_health")
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActivityLogAlertCriteriaServiceHealth"]]], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#status MonitorActivityLogAlert#status}.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def sub_status(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#sub_status MonitorActivityLogAlert#sub_status}.'''
        result = self._values.get("sub_status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActivityLogAlertCriteria(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActivityLogAlertCriteriaOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActivityLogAlert.MonitorActivityLogAlertCriteriaOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__bb0a45364b40c9b010815d4e047c8318005b788d8aa77870f6ce0fea88d86180)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute])

    @jsii.member(jsii_name="putResourceHealth")
    def put_resource_health(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActivityLogAlertCriteriaResourceHealth", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ce0f0387ee4fd3595a4fc5b73351d8ad8591662c4a9b6906eda4d7ee502f12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putResourceHealth", [value]))

    @jsii.member(jsii_name="putServiceHealth")
    def put_service_health(
        self,
        value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union["MonitorActivityLogAlertCriteriaServiceHealth", typing.Dict[builtins.str, typing.Any]]]],
    ) -> None:
        '''
        :param value: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c298c16b40265d5d2222e0ec6bcd4b651e6dfec1c9944ac8585ea7f14523d06a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "putServiceHealth", [value]))

    @jsii.member(jsii_name="resetCaller")
    def reset_caller(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCaller", []))

    @jsii.member(jsii_name="resetLevel")
    def reset_level(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLevel", []))

    @jsii.member(jsii_name="resetOperationName")
    def reset_operation_name(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetOperationName", []))

    @jsii.member(jsii_name="resetRecommendationCategory")
    def reset_recommendation_category(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecommendationCategory", []))

    @jsii.member(jsii_name="resetRecommendationImpact")
    def reset_recommendation_impact(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecommendationImpact", []))

    @jsii.member(jsii_name="resetRecommendationType")
    def reset_recommendation_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetRecommendationType", []))

    @jsii.member(jsii_name="resetResourceGroup")
    def reset_resource_group(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceGroup", []))

    @jsii.member(jsii_name="resetResourceHealth")
    def reset_resource_health(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceHealth", []))

    @jsii.member(jsii_name="resetResourceId")
    def reset_resource_id(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceId", []))

    @jsii.member(jsii_name="resetResourceProvider")
    def reset_resource_provider(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceProvider", []))

    @jsii.member(jsii_name="resetResourceType")
    def reset_resource_type(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetResourceType", []))

    @jsii.member(jsii_name="resetServiceHealth")
    def reset_service_health(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServiceHealth", []))

    @jsii.member(jsii_name="resetStatus")
    def reset_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetStatus", []))

    @jsii.member(jsii_name="resetSubStatus")
    def reset_sub_status(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetSubStatus", []))

    @builtins.property
    @jsii.member(jsii_name="resourceHealth")
    def resource_health(self) -> "MonitorActivityLogAlertCriteriaResourceHealthList":
        return typing.cast("MonitorActivityLogAlertCriteriaResourceHealthList", jsii.get(self, "resourceHealth"))

    @builtins.property
    @jsii.member(jsii_name="serviceHealth")
    def service_health(self) -> "MonitorActivityLogAlertCriteriaServiceHealthList":
        return typing.cast("MonitorActivityLogAlertCriteriaServiceHealthList", jsii.get(self, "serviceHealth"))

    @builtins.property
    @jsii.member(jsii_name="callerInput")
    def caller_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "callerInput"))

    @builtins.property
    @jsii.member(jsii_name="categoryInput")
    def category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "categoryInput"))

    @builtins.property
    @jsii.member(jsii_name="levelInput")
    def level_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "levelInput"))

    @builtins.property
    @jsii.member(jsii_name="operationNameInput")
    def operation_name_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "operationNameInput"))

    @builtins.property
    @jsii.member(jsii_name="recommendationCategoryInput")
    def recommendation_category_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recommendationCategoryInput"))

    @builtins.property
    @jsii.member(jsii_name="recommendationImpactInput")
    def recommendation_impact_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recommendationImpactInput"))

    @builtins.property
    @jsii.member(jsii_name="recommendationTypeInput")
    def recommendation_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "recommendationTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceGroupInput")
    def resource_group_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceGroupInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceHealthInput")
    def resource_health_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActivityLogAlertCriteriaResourceHealth"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActivityLogAlertCriteriaResourceHealth"]]], jsii.get(self, "resourceHealthInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceIdInput")
    def resource_id_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceIdInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceProviderInput")
    def resource_provider_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceProviderInput"))

    @builtins.property
    @jsii.member(jsii_name="resourceTypeInput")
    def resource_type_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceTypeInput"))

    @builtins.property
    @jsii.member(jsii_name="serviceHealthInput")
    def service_health_input(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActivityLogAlertCriteriaServiceHealth"]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List["MonitorActivityLogAlertCriteriaServiceHealth"]]], jsii.get(self, "serviceHealthInput"))

    @builtins.property
    @jsii.member(jsii_name="statusInput")
    def status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "statusInput"))

    @builtins.property
    @jsii.member(jsii_name="subStatusInput")
    def sub_status_input(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "subStatusInput"))

    @builtins.property
    @jsii.member(jsii_name="caller")
    def caller(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "caller"))

    @caller.setter
    def caller(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74d1f4a5a2464a51814ffb3fd964346f8472a7ad84a04aec1153aed9391cb939)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "caller", value)

    @builtins.property
    @jsii.member(jsii_name="category")
    def category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "category"))

    @category.setter
    def category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2bf67c83978d3666c29763d4b467e74f59a34e3dd83b0b67b8638463d052ac0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "category", value)

    @builtins.property
    @jsii.member(jsii_name="level")
    def level(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "level"))

    @level.setter
    def level(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__686a0bc796b62bf6f64fe87feaa983e35f6d022bef138ee18a97b040a94ef58c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "level", value)

    @builtins.property
    @jsii.member(jsii_name="operationName")
    def operation_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "operationName"))

    @operation_name.setter
    def operation_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35dde6dd441e02ce3c78c3b8116a301085080607214f8e70e19fa4ad64a81c50)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "operationName", value)

    @builtins.property
    @jsii.member(jsii_name="recommendationCategory")
    def recommendation_category(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recommendationCategory"))

    @recommendation_category.setter
    def recommendation_category(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71859fb8a68d075e2554b1710c473c9cbc1f37ad32a76ad1347ddc612181fc58)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommendationCategory", value)

    @builtins.property
    @jsii.member(jsii_name="recommendationImpact")
    def recommendation_impact(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recommendationImpact"))

    @recommendation_impact.setter
    def recommendation_impact(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3756fa180ba3b62b2d219d6a79081647641bab011915c90af2fdeeebe34cec72)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommendationImpact", value)

    @builtins.property
    @jsii.member(jsii_name="recommendationType")
    def recommendation_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "recommendationType"))

    @recommendation_type.setter
    def recommendation_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5a3b54aecfc7496f6e8919ee011bf83689c1ef8015369fca8a6c8348fcbc1fc)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "recommendationType", value)

    @builtins.property
    @jsii.member(jsii_name="resourceGroup")
    def resource_group(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceGroup"))

    @resource_group.setter
    def resource_group(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__183f413fb75598e5a37e22920f7c8b85b4d863b1a40bb6be4a14a898c46f8f78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceGroup", value)

    @builtins.property
    @jsii.member(jsii_name="resourceId")
    def resource_id(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceId"))

    @resource_id.setter
    def resource_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e52a4b3f3b593d16b7b1e8534c4be4dca8f963e858235ebc0fb8508d60ded0ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceId", value)

    @builtins.property
    @jsii.member(jsii_name="resourceProvider")
    def resource_provider(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceProvider"))

    @resource_provider.setter
    def resource_provider(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01bef388d26d347e653585493e6ceb3fc072a582ac79f849ce266973e47b7271)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceProvider", value)

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6648325d062a636059fc92e88035072549189b8b76dd869acdfeb049fcad73a5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "status"))

    @status.setter
    def status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14266bae9e93ffc6d199142e9d3b0c5d1cfe514dcb06c8ad14a8c77ace823297)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)

    @builtins.property
    @jsii.member(jsii_name="subStatus")
    def sub_status(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "subStatus"))

    @sub_status.setter
    def sub_status(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05d2c3ffeb050e41a7b1a90385c801be487b6b5896fdc10f668fa0b2f250132c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subStatus", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(self) -> typing.Optional[MonitorActivityLogAlertCriteria]:
        return typing.cast(typing.Optional[MonitorActivityLogAlertCriteria], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[MonitorActivityLogAlertCriteria],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b3f691a9ad622ed40e8d7fa75f1ffbc9b23d734f230ba1e676932ebda8aa03e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActivityLogAlert.MonitorActivityLogAlertCriteriaResourceHealth",
    jsii_struct_bases=[],
    name_mapping={"current": "current", "previous": "previous", "reason": "reason"},
)
class MonitorActivityLogAlertCriteriaResourceHealth:
    def __init__(
        self,
        *,
        current: typing.Optional[typing.Sequence[builtins.str]] = None,
        previous: typing.Optional[typing.Sequence[builtins.str]] = None,
        reason: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param current: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#current MonitorActivityLogAlert#current}.
        :param previous: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#previous MonitorActivityLogAlert#previous}.
        :param reason: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#reason MonitorActivityLogAlert#reason}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3363badd8c357c5aebb0db65916cd3af35d0c30b0ae012f03c2552496666243)
            check_type(argname="argument current", value=current, expected_type=type_hints["current"])
            check_type(argname="argument previous", value=previous, expected_type=type_hints["previous"])
            check_type(argname="argument reason", value=reason, expected_type=type_hints["reason"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if current is not None:
            self._values["current"] = current
        if previous is not None:
            self._values["previous"] = previous
        if reason is not None:
            self._values["reason"] = reason

    @builtins.property
    def current(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#current MonitorActivityLogAlert#current}.'''
        result = self._values.get("current")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def previous(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#previous MonitorActivityLogAlert#previous}.'''
        result = self._values.get("previous")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def reason(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#reason MonitorActivityLogAlert#reason}.'''
        result = self._values.get("reason")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActivityLogAlertCriteriaResourceHealth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActivityLogAlertCriteriaResourceHealthList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActivityLogAlert.MonitorActivityLogAlertCriteriaResourceHealthList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__8f9821e6aa604b27a1f99d55442d77eb3ca656221d53c0648fb2b9d483166c00)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorActivityLogAlertCriteriaResourceHealthOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__21081d01030c436347194c37976827cd446401b94b1416c61e37bb2bf9b5767a)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorActivityLogAlertCriteriaResourceHealthOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__739816e7e3b01a8954578101ca92340eaf66d0bcc84f8ed5568710eef8b0e9aa)
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
            type_hints = typing.get_type_hints(_typecheckingstub__274f3d0d9145524ff78f212b86c8d993473d284939bc449ef51120a180614976)
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
            type_hints = typing.get_type_hints(_typecheckingstub__91e08e6043e02004bc596a64785828939dc92c87986d43131bbccf73bbff3c5b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActivityLogAlertCriteriaResourceHealth]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActivityLogAlertCriteriaResourceHealth]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActivityLogAlertCriteriaResourceHealth]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dae4603f8d527cc0e765097f9ae521c1b130ffc0919ffba0379d9dd24673e56)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitorActivityLogAlertCriteriaResourceHealthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActivityLogAlert.MonitorActivityLogAlertCriteriaResourceHealthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__48376941959bd692a8f87a0e648279b22d7cd94e3a277b83c7403da2bbfaec90)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetCurrent")
    def reset_current(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetCurrent", []))

    @jsii.member(jsii_name="resetPrevious")
    def reset_previous(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetPrevious", []))

    @jsii.member(jsii_name="resetReason")
    def reset_reason(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetReason", []))

    @builtins.property
    @jsii.member(jsii_name="currentInput")
    def current_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "currentInput"))

    @builtins.property
    @jsii.member(jsii_name="previousInput")
    def previous_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "previousInput"))

    @builtins.property
    @jsii.member(jsii_name="reasonInput")
    def reason_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "reasonInput"))

    @builtins.property
    @jsii.member(jsii_name="current")
    def current(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "current"))

    @current.setter
    def current(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc82bfe7e8dfcfdaf4ca126e7db43f672a7e646e24b24b2b6a8c2c341b28e88e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "current", value)

    @builtins.property
    @jsii.member(jsii_name="previous")
    def previous(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "previous"))

    @previous.setter
    def previous(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15fc7fd1b34e8de672d6af77c28f3cc7096b9bdaeb12c554b0fcbc65651f437a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "previous", value)

    @builtins.property
    @jsii.member(jsii_name="reason")
    def reason(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "reason"))

    @reason.setter
    def reason(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__11d2e191c0fa2fcdd23c78cc258ef41de472b2a2a0a6468afa23787eb8096ef8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "reason", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitorActivityLogAlertCriteriaResourceHealth, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitorActivityLogAlertCriteriaResourceHealth, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitorActivityLogAlertCriteriaResourceHealth, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f93f82fc91fef173050f9a95a67e17afccae6cec4a745858daa83e015b0c688d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActivityLogAlert.MonitorActivityLogAlertCriteriaServiceHealth",
    jsii_struct_bases=[],
    name_mapping={
        "events": "events",
        "locations": "locations",
        "services": "services",
    },
)
class MonitorActivityLogAlertCriteriaServiceHealth:
    def __init__(
        self,
        *,
        events: typing.Optional[typing.Sequence[builtins.str]] = None,
        locations: typing.Optional[typing.Sequence[builtins.str]] = None,
        services: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''
        :param events: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#events MonitorActivityLogAlert#events}.
        :param locations: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#locations MonitorActivityLogAlert#locations}.
        :param services: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#services MonitorActivityLogAlert#services}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ee9deea03dde2647c212b047a6605fa69a155dcb353e3a2eb56db482a879543)
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument locations", value=locations, expected_type=type_hints["locations"])
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if events is not None:
            self._values["events"] = events
        if locations is not None:
            self._values["locations"] = locations
        if services is not None:
            self._values["services"] = services

    @builtins.property
    def events(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#events MonitorActivityLogAlert#events}.'''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def locations(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#locations MonitorActivityLogAlert#locations}.'''
        result = self._values.get("locations")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def services(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#services MonitorActivityLogAlert#services}.'''
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActivityLogAlertCriteriaServiceHealth(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActivityLogAlertCriteriaServiceHealthList(
    _cdktf_9a9027ec.ComplexList,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActivityLogAlert.MonitorActivityLogAlertCriteriaServiceHealthList",
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
            type_hints = typing.get_type_hints(_typecheckingstub__9beec16e67f08fb6fbb88dc21c30f2c1690c6ac6162b0075ec2c9d3a0af615a5)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument wraps_set", value=wraps_set, expected_type=type_hints["wraps_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, wraps_set])

    @jsii.member(jsii_name="get")
    def get(
        self,
        index: jsii.Number,
    ) -> "MonitorActivityLogAlertCriteriaServiceHealthOutputReference":
        '''
        :param index: the index of the item to return.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7dea17836e17a987cbeffe1740f27b823398f458253aee597ce69fc89e202c25)
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        return typing.cast("MonitorActivityLogAlertCriteriaServiceHealthOutputReference", jsii.invoke(self, "get", [index]))

    @builtins.property
    @jsii.member(jsii_name="terraformAttribute")
    def _terraform_attribute(self) -> builtins.str:
        '''The attribute on the parent resource this class is referencing.'''
        return typing.cast(builtins.str, jsii.get(self, "terraformAttribute"))

    @_terraform_attribute.setter
    def _terraform_attribute(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74329cc00ad8a8c6aeb077c18e89df77d0c3f33cb88279435fd31b297fda01e2)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3540873658e94d861d407263b06972015adbf06a1cbb3b8c89215b45cdde7832)
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
            type_hints = typing.get_type_hints(_typecheckingstub__0ed6a8fa1dcfcb540b0e783b5c116370875f87e7087fd5a0e5f2e7a728093357)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "wrapsSet", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActivityLogAlertCriteriaServiceHealth]]]:
        return typing.cast(typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActivityLogAlertCriteriaServiceHealth]]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActivityLogAlertCriteriaServiceHealth]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad828c72b6c3e5ba0845e6b3e59d94b2b998aff35f92105d11f0e7c732f18695)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


class MonitorActivityLogAlertCriteriaServiceHealthOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActivityLogAlert.MonitorActivityLogAlertCriteriaServiceHealthOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__c6a946b44bbd86cd8c658ba8527e0fa78d822db374a7ea1de209bfa3609b5424)
            check_type(argname="argument terraform_resource", value=terraform_resource, expected_type=type_hints["terraform_resource"])
            check_type(argname="argument terraform_attribute", value=terraform_attribute, expected_type=type_hints["terraform_attribute"])
            check_type(argname="argument complex_object_index", value=complex_object_index, expected_type=type_hints["complex_object_index"])
            check_type(argname="argument complex_object_is_from_set", value=complex_object_is_from_set, expected_type=type_hints["complex_object_is_from_set"])
        jsii.create(self.__class__, self, [terraform_resource, terraform_attribute, complex_object_index, complex_object_is_from_set])

    @jsii.member(jsii_name="resetEvents")
    def reset_events(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetEvents", []))

    @jsii.member(jsii_name="resetLocations")
    def reset_locations(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetLocations", []))

    @jsii.member(jsii_name="resetServices")
    def reset_services(self) -> None:
        return typing.cast(None, jsii.invoke(self, "resetServices", []))

    @builtins.property
    @jsii.member(jsii_name="eventsInput")
    def events_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "eventsInput"))

    @builtins.property
    @jsii.member(jsii_name="locationsInput")
    def locations_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "locationsInput"))

    @builtins.property
    @jsii.member(jsii_name="servicesInput")
    def services_input(self) -> typing.Optional[typing.List[builtins.str]]:
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "servicesInput"))

    @builtins.property
    @jsii.member(jsii_name="events")
    def events(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "events"))

    @events.setter
    def events(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7684be8cb65333bac1803dd9816d18aa1b0e4d0b57c4b292d2434c216f3a68a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "events", value)

    @builtins.property
    @jsii.member(jsii_name="locations")
    def locations(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "locations"))

    @locations.setter
    def locations(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c3413980959cd7c75f62acd859ed7c7e3e9cfdc11f2ba2bb05a3aab6a8cc75a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "locations", value)

    @builtins.property
    @jsii.member(jsii_name="services")
    def services(self) -> typing.List[builtins.str]:
        return typing.cast(typing.List[builtins.str], jsii.get(self, "services"))

    @services.setter
    def services(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a401de6e61218b34504713e188a4901b4c63a8a07b212c5fb787e3876416b0b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "services", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitorActivityLogAlertCriteriaServiceHealth, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitorActivityLogAlertCriteriaServiceHealth, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitorActivityLogAlertCriteriaServiceHealth, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ffb37f8827cfd3841d76f39153f470979dd9ca4db9376f7c14d90c1b249856e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


@jsii.data_type(
    jsii_type="@cdktf/provider-azurerm.monitorActivityLogAlert.MonitorActivityLogAlertTimeouts",
    jsii_struct_bases=[],
    name_mapping={
        "create": "create",
        "delete": "delete",
        "read": "read",
        "update": "update",
    },
)
class MonitorActivityLogAlertTimeouts:
    def __init__(
        self,
        *,
        create: typing.Optional[builtins.str] = None,
        delete: typing.Optional[builtins.str] = None,
        read: typing.Optional[builtins.str] = None,
        update: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param create: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#create MonitorActivityLogAlert#create}.
        :param delete: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#delete MonitorActivityLogAlert#delete}.
        :param read: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#read MonitorActivityLogAlert#read}.
        :param update: Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#update MonitorActivityLogAlert#update}.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ef5b0e2abe5e68f66266429a084cf7989c2a4f9ad9488ba92ceb3593a86d0d1)
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
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#create MonitorActivityLogAlert#create}.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def delete(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#delete MonitorActivityLogAlert#delete}.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def read(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#read MonitorActivityLogAlert#read}.'''
        result = self._values.get("read")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def update(self) -> typing.Optional[builtins.str]:
        '''Docs at Terraform Registry: {@link https://www.terraform.io/docs/providers/azurerm/r/monitor_activity_log_alert#update MonitorActivityLogAlert#update}.'''
        result = self._values.get("update")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MonitorActivityLogAlertTimeouts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class MonitorActivityLogAlertTimeoutsOutputReference(
    _cdktf_9a9027ec.ComplexObject,
    metaclass=jsii.JSIIMeta,
    jsii_type="@cdktf/provider-azurerm.monitorActivityLogAlert.MonitorActivityLogAlertTimeoutsOutputReference",
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
            type_hints = typing.get_type_hints(_typecheckingstub__de61fb05b3f3d080c3bad209347eef4ab7ed063b362ad23d91ec03166afdbcc8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__749c1db43c142d619a8bbeb517daa9d539703e90964e955620afc1396dae7689)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "create", value)

    @builtins.property
    @jsii.member(jsii_name="delete")
    def delete(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "delete"))

    @delete.setter
    def delete(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88139e0a31d63909f2eb85ef895479c6ce31abc6502e7be25b17679f6ce1bb9f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "delete", value)

    @builtins.property
    @jsii.member(jsii_name="read")
    def read(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "read"))

    @read.setter
    def read(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d0e6c3e4a31b0e059194f9a5a5e6f7bac5c7a8979f3167443cfbea800907efe)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "read", value)

    @builtins.property
    @jsii.member(jsii_name="update")
    def update(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "update"))

    @update.setter
    def update(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d100d38c8a3662ebc009b86eb70cf9ba1b4231abbb54974feb90bfc70afe2479)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "update", value)

    @builtins.property
    @jsii.member(jsii_name="internalValue")
    def internal_value(
        self,
    ) -> typing.Optional[typing.Union[MonitorActivityLogAlertTimeouts, _cdktf_9a9027ec.IResolvable]]:
        return typing.cast(typing.Optional[typing.Union[MonitorActivityLogAlertTimeouts, _cdktf_9a9027ec.IResolvable]], jsii.get(self, "internalValue"))

    @internal_value.setter
    def internal_value(
        self,
        value: typing.Optional[typing.Union[MonitorActivityLogAlertTimeouts, _cdktf_9a9027ec.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bf61025aa024ee8a48f0341d36a167aa7c4a203cc68e2275070c4131182d6dfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "internalValue", value)


__all__ = [
    "MonitorActivityLogAlert",
    "MonitorActivityLogAlertAction",
    "MonitorActivityLogAlertActionList",
    "MonitorActivityLogAlertActionOutputReference",
    "MonitorActivityLogAlertConfig",
    "MonitorActivityLogAlertCriteria",
    "MonitorActivityLogAlertCriteriaOutputReference",
    "MonitorActivityLogAlertCriteriaResourceHealth",
    "MonitorActivityLogAlertCriteriaResourceHealthList",
    "MonitorActivityLogAlertCriteriaResourceHealthOutputReference",
    "MonitorActivityLogAlertCriteriaServiceHealth",
    "MonitorActivityLogAlertCriteriaServiceHealthList",
    "MonitorActivityLogAlertCriteriaServiceHealthOutputReference",
    "MonitorActivityLogAlertTimeouts",
    "MonitorActivityLogAlertTimeoutsOutputReference",
]

publication.publish()

def _typecheckingstub__f5079e60d877e29323ba976c824f1af2acc540815bc0d4292e57746d6c197ef5(
    scope: _constructs_77d1e7e8.Construct,
    id_: builtins.str,
    *,
    criteria: typing.Union[MonitorActivityLogAlertCriteria, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    resource_group_name: builtins.str,
    scopes: typing.Sequence[builtins.str],
    action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActivityLogAlertAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorActivityLogAlertTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
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

def _typecheckingstub__d11bdfdf50a69aeb959b08a3ea03a1e980a76fa4ca436c34dda46e3befc4d72e(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActivityLogAlertAction, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9e5fd804e6f68e06a57a4049e35362e8b491443f97342cc2ebc98e92666d9d64(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef208f0cf1bcd015d084b181edcc90dae55c6835d6d9d208b864ae3cffd1917d(
    value: typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__458fe4f0f3468ab45ba869cf25fef9968aeb279e71c83c9d4a579cf67e66309d(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__89637ba4c007b2a524d1d2f13e8419d08a8d417e2ba6c78c9b632c16f4a07815(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8706d8720948b555a1756590aeafa7fba9276cb4c1217f9b2361f84d08abc7b4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71d71709acbc9024ff2465e6dabdfb99ac6f4d011dbfad76c1306e3a8065199b(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__abf00bba8d0b87bc26f1aa393775f7bcff50d6e26b6ee749da60e7364ae25c52(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183da7fc40dc5cd38056b9861df054fa94f0a97d4952ba4f9eef1c436e92b6d8(
    *,
    action_group_id: builtins.str,
    webhook_properties: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a061e56d7439f0e76b40af5a7049736c6509fb705908b7dfd547d0ec2dc6fa2(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e5572846c25d5035d30ddf7a470d1a1834633c51deab1d0cb359ce7286b6f62(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf4e2d097787e27071ddaf44b5bfed276055f4a0a0068e2110dca443687473c1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__499e314ca537cba0d36c28b9c771bbe865e48af750db6ffab29c80e4315df6cc(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d2210770b9ec9620952590438b0a2173969acd4deed5cac14d4f71a26963ae4(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1311cf83d8766cf31c969b7aabc7d69737ffa04f659846b4c13fa0685a799b9b(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActivityLogAlertAction]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a90cae928f6a91f72e30aaf6cb23ea1a879a2125b891f488c0a2cce853ce8903(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44e1896e6844fa475f61715e46bac10b93768e07e37d9aed3f8a8581cc7da792(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__feba7b1efbd55e1e0634c997176df18d1f680ab59494b3a50b7047677802d0e5(
    value: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__96041d5665f99ca8e390a1e48d34a1724e588c3d24e4aa14beaf527dabcb26b3(
    value: typing.Optional[typing.Union[MonitorActivityLogAlertAction, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdc524144ca3109bf63d45a6e23b94dfe0b1404ea0bc4b68e9d86e3361b8e3c3(
    *,
    connection: typing.Optional[typing.Union[typing.Union[_cdktf_9a9027ec.SSHProvisionerConnection, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.WinrmProvisionerConnection, typing.Dict[builtins.str, typing.Any]]]] = None,
    count: typing.Optional[jsii.Number] = None,
    depends_on: typing.Optional[typing.Sequence[_cdktf_9a9027ec.ITerraformDependable]] = None,
    for_each: typing.Optional[_cdktf_9a9027ec.ITerraformIterator] = None,
    lifecycle: typing.Optional[typing.Union[_cdktf_9a9027ec.TerraformResourceLifecycle, typing.Dict[builtins.str, typing.Any]]] = None,
    provider: typing.Optional[_cdktf_9a9027ec.TerraformProvider] = None,
    provisioners: typing.Optional[typing.Sequence[typing.Union[typing.Union[_cdktf_9a9027ec.FileProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.LocalExecProvisioner, typing.Dict[builtins.str, typing.Any]], typing.Union[_cdktf_9a9027ec.RemoteExecProvisioner, typing.Dict[builtins.str, typing.Any]]]]] = None,
    criteria: typing.Union[MonitorActivityLogAlertCriteria, typing.Dict[builtins.str, typing.Any]],
    name: builtins.str,
    resource_group_name: builtins.str,
    scopes: typing.Sequence[builtins.str],
    action: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActivityLogAlertAction, typing.Dict[builtins.str, typing.Any]]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[typing.Union[builtins.bool, _cdktf_9a9027ec.IResolvable]] = None,
    id: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    timeouts: typing.Optional[typing.Union[MonitorActivityLogAlertTimeouts, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9c680eca68f55118237d8e04f64deba0ecc901ccc77adb441a06d4edf79b0294(
    *,
    category: builtins.str,
    caller: typing.Optional[builtins.str] = None,
    level: typing.Optional[builtins.str] = None,
    operation_name: typing.Optional[builtins.str] = None,
    recommendation_category: typing.Optional[builtins.str] = None,
    recommendation_impact: typing.Optional[builtins.str] = None,
    recommendation_type: typing.Optional[builtins.str] = None,
    resource_group: typing.Optional[builtins.str] = None,
    resource_health: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActivityLogAlertCriteriaResourceHealth, typing.Dict[builtins.str, typing.Any]]]]] = None,
    resource_id: typing.Optional[builtins.str] = None,
    resource_provider: typing.Optional[builtins.str] = None,
    resource_type: typing.Optional[builtins.str] = None,
    service_health: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActivityLogAlertCriteriaServiceHealth, typing.Dict[builtins.str, typing.Any]]]]] = None,
    status: typing.Optional[builtins.str] = None,
    sub_status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb0a45364b40c9b010815d4e047c8318005b788d8aa77870f6ce0fea88d86180(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ce0f0387ee4fd3595a4fc5b73351d8ad8591662c4a9b6906eda4d7ee502f12(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActivityLogAlertCriteriaResourceHealth, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c298c16b40265d5d2222e0ec6bcd4b651e6dfec1c9944ac8585ea7f14523d06a(
    value: typing.Union[_cdktf_9a9027ec.IResolvable, typing.Sequence[typing.Union[MonitorActivityLogAlertCriteriaServiceHealth, typing.Dict[builtins.str, typing.Any]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74d1f4a5a2464a51814ffb3fd964346f8472a7ad84a04aec1153aed9391cb939(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2bf67c83978d3666c29763d4b467e74f59a34e3dd83b0b67b8638463d052ac0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__686a0bc796b62bf6f64fe87feaa983e35f6d022bef138ee18a97b040a94ef58c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35dde6dd441e02ce3c78c3b8116a301085080607214f8e70e19fa4ad64a81c50(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71859fb8a68d075e2554b1710c473c9cbc1f37ad32a76ad1347ddc612181fc58(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3756fa180ba3b62b2d219d6a79081647641bab011915c90af2fdeeebe34cec72(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5a3b54aecfc7496f6e8919ee011bf83689c1ef8015369fca8a6c8348fcbc1fc(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__183f413fb75598e5a37e22920f7c8b85b4d863b1a40bb6be4a14a898c46f8f78(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e52a4b3f3b593d16b7b1e8534c4be4dca8f963e858235ebc0fb8508d60ded0ad(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01bef388d26d347e653585493e6ceb3fc072a582ac79f849ce266973e47b7271(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6648325d062a636059fc92e88035072549189b8b76dd869acdfeb049fcad73a5(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14266bae9e93ffc6d199142e9d3b0c5d1cfe514dcb06c8ad14a8c77ace823297(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05d2c3ffeb050e41a7b1a90385c801be487b6b5896fdc10f668fa0b2f250132c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b3f691a9ad622ed40e8d7fa75f1ffbc9b23d734f230ba1e676932ebda8aa03e8(
    value: typing.Optional[MonitorActivityLogAlertCriteria],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3363badd8c357c5aebb0db65916cd3af35d0c30b0ae012f03c2552496666243(
    *,
    current: typing.Optional[typing.Sequence[builtins.str]] = None,
    previous: typing.Optional[typing.Sequence[builtins.str]] = None,
    reason: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8f9821e6aa604b27a1f99d55442d77eb3ca656221d53c0648fb2b9d483166c00(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__21081d01030c436347194c37976827cd446401b94b1416c61e37bb2bf9b5767a(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__739816e7e3b01a8954578101ca92340eaf66d0bcc84f8ed5568710eef8b0e9aa(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__274f3d0d9145524ff78f212b86c8d993473d284939bc449ef51120a180614976(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__91e08e6043e02004bc596a64785828939dc92c87986d43131bbccf73bbff3c5b(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dae4603f8d527cc0e765097f9ae521c1b130ffc0919ffba0379d9dd24673e56(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActivityLogAlertCriteriaResourceHealth]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48376941959bd692a8f87a0e648279b22d7cd94e3a277b83c7403da2bbfaec90(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc82bfe7e8dfcfdaf4ca126e7db43f672a7e646e24b24b2b6a8c2c341b28e88e(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15fc7fd1b34e8de672d6af77c28f3cc7096b9bdaeb12c554b0fcbc65651f437a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__11d2e191c0fa2fcdd23c78cc258ef41de472b2a2a0a6468afa23787eb8096ef8(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f93f82fc91fef173050f9a95a67e17afccae6cec4a745858daa83e015b0c688d(
    value: typing.Optional[typing.Union[MonitorActivityLogAlertCriteriaResourceHealth, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ee9deea03dde2647c212b047a6605fa69a155dcb353e3a2eb56db482a879543(
    *,
    events: typing.Optional[typing.Sequence[builtins.str]] = None,
    locations: typing.Optional[typing.Sequence[builtins.str]] = None,
    services: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9beec16e67f08fb6fbb88dc21c30f2c1690c6ac6162b0075ec2c9d3a0af615a5(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    wraps_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7dea17836e17a987cbeffe1740f27b823398f458253aee597ce69fc89e202c25(
    index: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74329cc00ad8a8c6aeb077c18e89df77d0c3f33cb88279435fd31b297fda01e2(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3540873658e94d861d407263b06972015adbf06a1cbb3b8c89215b45cdde7832(
    value: _cdktf_9a9027ec.IInterpolatingParent,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ed6a8fa1dcfcb540b0e783b5c116370875f87e7087fd5a0e5f2e7a728093357(
    value: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad828c72b6c3e5ba0845e6b3e59d94b2b998aff35f92105d11f0e7c732f18695(
    value: typing.Optional[typing.Union[_cdktf_9a9027ec.IResolvable, typing.List[MonitorActivityLogAlertCriteriaServiceHealth]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6a946b44bbd86cd8c658ba8527e0fa78d822db374a7ea1de209bfa3609b5424(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
    complex_object_index: jsii.Number,
    complex_object_is_from_set: builtins.bool,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7684be8cb65333bac1803dd9816d18aa1b0e4d0b57c4b292d2434c216f3a68a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c3413980959cd7c75f62acd859ed7c7e3e9cfdc11f2ba2bb05a3aab6a8cc75a(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a401de6e61218b34504713e188a4901b4c63a8a07b212c5fb787e3876416b0b5(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffb37f8827cfd3841d76f39153f470979dd9ca4db9376f7c14d90c1b249856e(
    value: typing.Optional[typing.Union[MonitorActivityLogAlertCriteriaServiceHealth, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ef5b0e2abe5e68f66266429a084cf7989c2a4f9ad9488ba92ceb3593a86d0d1(
    *,
    create: typing.Optional[builtins.str] = None,
    delete: typing.Optional[builtins.str] = None,
    read: typing.Optional[builtins.str] = None,
    update: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de61fb05b3f3d080c3bad209347eef4ab7ed063b362ad23d91ec03166afdbcc8(
    terraform_resource: _cdktf_9a9027ec.IInterpolatingParent,
    terraform_attribute: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__749c1db43c142d619a8bbeb517daa9d539703e90964e955620afc1396dae7689(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88139e0a31d63909f2eb85ef895479c6ce31abc6502e7be25b17679f6ce1bb9f(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d0e6c3e4a31b0e059194f9a5a5e6f7bac5c7a8979f3167443cfbea800907efe(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d100d38c8a3662ebc009b86eb70cf9ba1b4231abbb54974feb90bfc70afe2479(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bf61025aa024ee8a48f0341d36a167aa7c4a203cc68e2275070c4131182d6dfb(
    value: typing.Optional[typing.Union[MonitorActivityLogAlertTimeouts, _cdktf_9a9027ec.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass
